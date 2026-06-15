# Architecture

## High-Level Architecture

```text
User / prompt file
  -> CLI entrypoint
  -> orchestrator / supervisor
  -> agent role
  -> LLM adapter
  -> JSON action
  -> JsonGate
  -> Agent Kernel
  -> Capability Registry
  -> feature adapter
  -> MCP client
  -> MCP server
  -> sandboxed side effect or read
  -> normalized CapabilityResult
  -> event log
  -> next agent step or final
```

## Kiến Trúc Theo Tầng

### 1. Interface Layer

Entry points:

- `main.py`: chạy single-agent orchestrator.
- `main_langgraph.py`: chạy LangGraph multi-agent pipeline.
- `run_*_smoke.py`: deterministic smoke runners.
- `run_*_demo.py`: manual demo runners.
- `run_all_cases.py`: prompt-based test runner.
- `main.py lab ...`: chạy mini repo qua registry.
- `run_process_ui.py`: local dashboard cho process/log/directive.
- `experiments/self_eval_qa_lab/main.py`: runner cho self-evaluating QA lab.
- `business_prompt_lab/*/main.py`: runner trực tiếp của từng mini repo.

Tầng này không nên chứa logic agent phức tạp. Nó chỉ đọc prompt, cấu hình
encoding/env, gọi runtime và in kết quả.

### 2. LLM Adapter Layer

File:

- `llm.py`

Trách nhiệm:

- Bọc OpenAI-compatible API.
- Mặc định trỏ tới LM Studio `http://localhost:1234/v1`.
- Cho phép override bằng env: `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`,
  `LLM_TIMEOUT`, `LLM_MAX_TOKENS`.

Không nên để tool policy hoặc orchestration ở tầng này.

### 3. Agent Prompt And Role Layer

Files:

- `agents/base_agent.py`
- `agents/role_agents.py`
- `agents/lenses/`
- `prompts/system_prompt.md`
- `tools/prompt_loader.py`
- `tools/skill_loader.py`

Trách nhiệm:

- Render system prompt.
- Gắn tool prompt và skill prompt.
- Gắn role boundary và tool allowlist.
- Chặn output gọi tool ngoài quyền role.

Role chính:

- Research
- Planner
- Architect
- Code
- Test
- Review
- Ledger
- Final
- Tool Agent legacy

### 4. Output Gate Layer

Files:

- `output_gate/json_gate.py`
- `output_gate/repair_rules.py`
- `output_gate/repair_loop.py`

Trách nhiệm:

- Extract JSON từ raw LLM output.
- Repair deterministic lỗi phổ biến.
- Validate action schema.
- Resolve tool alias.
- Validate tool args theo schema.
- Dry-run safety cho path, terminal, git mutation, content size.

JsonGate là contract gate trước khi tool chạy thật.

### 5. Orchestration Layer

Files:

- `orchestrator.py`
- `orchestration/langgraph_orchestrator.py`
- `orchestration/company_orchestrator.py`
- `orchestration/software_factory_orchestrator.py`
- `orchestration/global_supervisor.py`
- `orchestration/intent_router.py`
- `agents/user_agent.py`

Runtime hiện có:

```text
single-agent:
main.py -> orchestrator.py -> Tool Agent -> tool loop

langgraph:
main_langgraph.py -> research -> planner -> architect -> code -> test -> review -> ledger -> final

company v0.5:
ResearchAgent -> PlannerAgent -> ArchitectAgent -> CodeAgent -> TestAgent -> ReviewAgent -> LedgerAgent -> FinalAgent

software factory v0.7:
Vision -> BRD -> PRD -> Stories -> AC -> Domain -> Business Logic -> Technical -> Pattern -> Implementation Spec -> Handoff -> Docs

global supervisor:
IntentRouter -> Safety -> selected department(s) -> FinalSynthesisAgent

self-eval QA lab:
Question -> Planner -> Worker Agents -> Evaluator -> Critical Agent -> Evolution Proposal -> Final Synthesis

repo understanding lab:
Target repo -> Scanner -> Docs Reader -> Symbols -> Runtime Map -> Graphs -> Context Pack -> Understanding Report

live user control:
User Directive -> User Agent -> Orchestrator Control Point -> Applied/Rejected Event
```

### 6. Agent Kernel Layer

Files:

- `core/kernel.py`
- `core/registry.py`
- `core/capabilities.py`
- `core/schemas.py`
- `core/bootstrap.py`
- `core/events.py`
- `core/state.py`
- `core/ports/`

Contract:

```text
core.capabilities.call_tool()
  -> AgentKernel.execute_tool()
  -> CapabilityRegistry.resolve_tool()
  -> ToolPort.execute()
  -> CapabilityResult envelope
```

Core không biết chi tiết browser, RAG, Docker, PDF, Obsidian. Những thứ đó nằm
sau feature adapter.

### 7. Feature Adapter Layer

Files:

- `features/loader.py`
- `features/contracts.py`
- `features/mcp_tools/`
- `config/features.yaml`

Hiện chỉ có feature chính:

- `mcp_tools`: routes kernel tool request sang MCP client/server.

Thiết kế đúng:

- Feature có descriptor.
- Feature khai báo capabilities.
- Feature khai báo tests.
- Feature removable.
- Nếu disable feature, kernel vẫn boot và trả missing capability thay vì crash.

### 8. MCP Tool Layer

Files:

- `features/mcp_tools/config.py`
- `features/mcp_tools/client.py`
- `features/mcp_tools/schemas.py`
- `features/mcp_tools/policy.py`
- `mcp_servers/*.py`

Luồng:

```text
tool name
  -> resolve alias/server.tool
  -> validate schema
  -> policy check
  -> normalize path/env
  -> start MCP stdio server
  -> call tool
  -> normalize result
```

MCP servers hiện có:

| Server | Vai trò |
|---|---|
| filesystem | External MCP, thao tác workspace |
| file_editor | edit có audit |
| python | chạy Python trong workspace |
| terminal | argv-only validation/probe |
| lint_test | compile/ruff/run file/smoke suite |
| git | git read-only, mutation bị block |
| code_index | index symbol/reference/import graph |
| rag | Qdrant ingest/search |
| fetch/search | web retrieval |
| document/pdf_text_extraction | document extraction/writing |
| ledger | JSONL audit memory |
| issue | SQLite issue tracker |
| docker | Docker status/logs, mutation opt-in |
| obsidian | local markdown vault |
| playwright | browser text/screenshot |
| context7 | library docs |

### 9. Persistence And Runtime Data Layer

Runtime directories:

- `var/workspace/`: sandbox workspace.
- `var/agent_runs/`: event logs.
- `var/test_runs/`: test run logs.
- `var/self_eval_qa_lab/`: self-evaluation run artifacts.
- `var/repo_understanding_lab/`: repo-understanding reports and admin traces.
- `var/qdrant_storage/`: local Qdrant storage if configured.
- `workspace/`: legacy/generated workspace artifacts still present.

Artifact outputs:

- Software Factory: `var/workspace/factory_runs/<run_id>/`.
- Ledger: `var/workspace/ledger/ledger.jsonl` by default.
- Issues: `var/workspace/issues/issues.db` by default.
- Self-Eval QA Lab: `var/self_eval_qa_lab/<run_id>/summary.md`, `outputs/`, `admin/full_trace.json`.
- Repo Understanding Lab: `var/repo_understanding_lab/<run_id>/reports/understanding_report.json`, `admin/full_trace.json`.
- Root orchestrator: `var/agent_runs/<run_id>/events.jsonl`, `summary.json`.

### 10. Quality Layer

Files:

- `run_dev_checks.py`
- `run_capability_suite.py`
- `run_all_cases.py`
- `tests/`
- `run_*_smoke.py`

Quality gates:

- compileall
- kernel contract tests
- feature contract tests
- JsonGate smoke
- role permission smoke
- MCP chain smoke
- LangGraph smoke
- Code/Test v0.5 smoke
- Company v0.5 smoke
- Software Factory smoke
- Global Supervisor smoke
- Mini repo registry tests
- User Agent directive scope tests
- Process Dashboard API/UI smoke
- Repo Understanding Lab smoke
- Optional real LM Studio evidence run

### 11. Experiment And Mini Repo Layer

Files:

- `tools/mini_repo_registry.py`
- `business_prompt_lab/`
- `experiments/self_eval_qa_lab/`

Trách nhiệm:

- Cách ly experiment khỏi runtime chính.
- Cho phép chạy mini repo qua root CLI hoặc trực tiếp.
- Mỗi mini repo có docs, tests và output artifacts riêng.
- Dùng proposal/evidence trước khi kéo thay đổi vào root.

Mini repo không nên import ngược module nội bộ không ổn định của root nếu chỉ cần public runner contract.

### 12. Observability And Control Layer

Files:

- `run_process_ui.py`
- `ui/process_dashboard/`
- `agents/user_agent.py`
- `var/**/admin/full_trace.json`

Trách nhiệm:

- Hiển thị run, agent, state, timeline, warnings, artifacts.
- Nhận directive từ người dùng khi run đang chạy.
- Ghi full observable trace cho admin.
- Phân biệt log rút gọn cho UI và raw/admin artifact không truncate.

Lưu ý: full trace là full observable trace gồm prompt, raw model output, public rationale/result và handoff. Nó không claim đọc được hidden internal chain-of-thought nếu model/runtime không xuất ra.

## Core Data Contracts

### Agent Action

```json
{
  "action": "tool",
  "plan": "brief observable plan",
  "tool": "server.tool_name",
  "args": {}
}
```

```json
{
  "action": "final",
  "finish_reason": "validated|handoff|blocker|dependency_failure",
  "message": "..."
}
```

### Capability Result

```json
{
  "ok": true,
  "capability": "python.run_python",
  "feature": "mcp_tools",
  "data": {},
  "error": null,
  "metadata": {}
}
```

### Department Result v0.5

```json
{
  "agent": "code_agent",
  "version": "v0.5",
  "lens_results": [],
  "synthesis": {},
  "records": {},
  "route": {
    "next_agent": "test_agent",
    "reason": "Implementation is ready for QA validation."
  }
}
```

### Software Factory Stage Result

```json
{
  "agent": "BRD Agent",
  "department": "Business Analysis Department",
  "version": "v0.7",
  "ok": true,
  "decision": "artifact_created",
  "artifact_refs": [],
  "missing_inputs": [],
  "route": {
    "next_agent": "PRD Agent"
  }
}
```

## Các Boundary Quan Trọng

- Prompt rule không phải security boundary.
- JsonGate là contract gate, nhưng tool server vẫn phải tự sandbox.
- Code Agent được edit nhưng không tự approve.
- Test Agent validate nhưng không edit.
- Review Agent review nhưng không mutate git.
- Ledger ghi memory/audit nhưng không chạy code.
- Software Factory tạo spec, không claim đã implement.
- Global Supervisor route request, không tự bypass safety.
- User Agent có priority cao, nhưng vẫn đi qua orchestrator control point.
- Process Dashboard quan sát/điều khiển run, không tự sửa source.
- Mini repo được phép thử nghiệm mạnh, nhưng thay đổi root phải đi qua proposal/test.
- Full trace giữ raw observable output; không dựa vào hidden internal reasoning.

## Architecture Khi Rebuild

Khi viết lại repo mới, architecture đích nên giữ cùng boundary nhưng triển khai
ít hơn trước:

```text
Phase 1: CLI + LLM + JSON action
Phase 2: Event log + run summary
Phase 3: Kernel + capability result
Phase 4: File/Python tools tối thiểu
Phase 5: JsonGate
Phase 6: MCP adapter + schemas + policy
Phase 7: Test harness
Phase 8: Role agents
Phase 9: LangGraph/company orchestration
Phase 10: Software Factory artifacts
Phase 11: Global Supervisor
Phase 12: Mini repo registry
Phase 13: Self-evaluating QA/evolution proposals
Phase 14: User Agent live control
Phase 15: Process Dashboard UI
Phase 16: Repo Understanding Lab
Phase 17: Real LLM evidence loop
```
