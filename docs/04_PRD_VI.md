# Product Requirements Document

## 1. Product Vision

Xây một framework local cho coding-agent có thể chuyển từ yêu cầu tự nhiên sang
hành động có kiểm soát: đọc/sửa file, chạy validation, dùng tools, sinh spec,
ghi audit và báo cáo final dựa trên evidence.

## 2. Personas

| Persona | Mục tiêu |
|---|---|
| Builder | Muốn hiểu và rebuild từng tầng |
| Agent operator | Muốn chạy prompt và nhận kết quả có evidence |
| Developer | Muốn thêm MCP/agent/skill/test dễ dàng |
| Reviewer | Muốn biết thay đổi gì, test gì, rủi ro gì |
| Product planner | Muốn BRD/PRD/story/AC trước khi code |

## 3. Functional Requirements

### FR-01 CLI Prompt Runner

User có thể chạy:

```powershell
python main.py prompts/user_prompt.md
```

Acceptance:

- Đọc prompt file hoặc prompt mặc định.
- In final result.
- Không crash khi prompt path hợp lệ.

### FR-02 LLM Adapter

System gọi được OpenAI-compatible chat completions API.

Acceptance:

- Có default LM Studio config.
- Env override được model/base URL/token/timeout.
- Lỗi LLM được wrap thành message rõ.

### FR-03 JSON Action Protocol

Agent chỉ trả một JSON object:

- `action=tool`
- `action=final`

Acceptance:

- Không cần markdown.
- Parse bằng `json.loads` sau JsonGate.
- Có retry khi invalid.

### FR-04 JsonGate

System validate output trước khi gọi tool.

Acceptance:

- Repair được fenced JSON/trailing comma/Python literal/unquoted simple key.
- Chặn unknown tool.
- Chặn missing/wrong args.
- Chặn unsafe path.
- Chặn terminal không phải argv.
- Chặn git mutation theo policy.

### FR-05 Agent Kernel

Tool execution đi qua kernel.

Acceptance:

- `call_tool()` trả CapabilityResult envelope.
- Feature disable không làm kernel crash.
- Unknown tool trả structured error.

### FR-06 MCP Tool Integration

Agent gọi tools qua MCP adapter.

Acceptance:

- Resolve alias và server-qualified name.
- Validate schema.
- Normalize result.
- Có metadata risk/category.

### FR-07 Workspace Sandbox

File tools chỉ thao tác trong workspace.

Acceptance:

- Relative path resolve vào workspace.
- `..`, absolute drive path, path ngoài workspace bị chặn.
- Python/RAG/document/ledger/issue tự enforce sandbox.

### FR-08 File Editing

Agent edit file qua File Editor MCP.

Acceptance:

- View line-numbered file.
- Create/write_lines file.
- str_replace có expected replacement count.
- insert theo line.
- Không cần terminal để edit.

### FR-09 Validation

System hỗ trợ validation có cấu trúc.

Acceptance:

- Chạy Python workspace file.
- Compile Python project path.
- Run selected Python file.
- Ruff check optional, báo dependency failure nếu thiếu.
- Smoke suite chạy được.

### FR-10 Finish Gate

Coding task không final success nếu chưa validate.

Acceptance:

- Sau code change, pending validation bật.
- Validation pass tắt pending.
- Final bị block nếu còn pending, trừ blocker rõ.

### FR-11 Event Logging

Mỗi run có audit log.

Acceptance:

- Ghi MessageEvent, ActionEvent, ObservationEvent, StateEvent/ErrorEvent.
- Có summary JSON.
- Có CLI inspect/search.

### FR-12 Role-Based Agents

System có role agents với tool allowlist.

Acceptance:

- Research/Planner/Architect/Code/Test/Review/Ledger/Final.
- Role không gọi tool ngoài quyền.
- Role prompt ghi rõ trách nhiệm.

### FR-13 LangGraph Orchestration

System chạy được pipeline role-based.

Acceptance:

- State có required/missing files, tests_run, last_failure, repair_attempts.
- Tool node tập trung thực thi.
- Failed test route về Code.
- Budget/repeated tool guard hoạt động.

### FR-14 Company Agents v0.5

System có deterministic department contract runner.

Acceptance:

- Department result có `agent`, `version`, `lens_results`, `synthesis`, `records`, `route`.
- Code/Test cycle route rõ.
- Review/Ledger/Final gate rõ.
- Smoke pass.

### FR-15 Software Factory v0.7

System sinh artifact spec trước khi code.

Acceptance:

- Sinh Protocol Strategy, Vision, BRD, PRD, Epics/Stories, AC.
- Sinh Product Validation/Critique.
- Sinh Domain Analysis, Business Logic Model/Validation.
- Sinh Technical Analysis, Pattern Decision.
- Sinh Implementation Spec, Code Handoff Packet.
- Sinh Docs Plan, Repo Scan, API Inventory, ADR Candidates, Docs Package, Docs Verification, Final.

### FR-16 Global Supervisor

System route request tổng quát.

Acceptance:

- Classify knowledge/research/code/product-build/mixed/agent-creation.
- Safety Department chạy khi cần repo/code/web.
- Final Synthesis là owner final answer.
- Product-build route sang Software Factory.

### FR-17 Mini Repo Registry

System chạy được nhiều mini repo thử nghiệm qua root CLI.

Acceptance:

- `python main.py lab list` liệt kê mini repo.
- `python main.py lab <name> ...` forward args tới runner.
- Mỗi mini repo có docs/tests/output artifacts riêng.
- Registry không import runtime nặng khi chỉ list.

### FR-18 Self-Evaluating QA Lab

System có agent room chuyên hỏi đáp, giao việc, phản biện và tổng hợp mà không sinh code.

Acceptance:

- Có planner/worker/evaluator/critical/final synthesis flow.
- Có baseline comparison với ChatGPT/local baseline.
- Có `summary.md`, outputs và `admin/full_trace.json`.
- Critical agent đề xuất add/remove/change agent/flow/skills/tools dưới dạng proposal.

### FR-19 User Agent Live Control

Người dùng có thể nhập directive trong lúc model đang chạy.

Acceptance:

- Directive có priority cao hơn agent thường.
- Hỗ trợ scope `this_run_only` và future/proposal.
- Orchestrator ghi applied/rejected status.
- Directive tạm thời không leak sang run sau.

### FR-20 Process Dashboard UI

System có UI local để quản lý process và nhập directive.

Acceptance:

- UI hiển thị run list, active run, agents, state, timeline, logs, artifacts.
- UI đọc được run dirs cũ và mới.
- UI post directive vào User Agent control channel.
- UI không crash khi thiếu optional artifact.

### FR-21 Repo Understanding Lab

System có mini repo tự đọc hiểu project khác.

Acceptance:

- Scanner/docs/symbol/runtime/graph/context pack chạy được.
- Sinh `reports/understanding_report.json`.
- Sinh `admin/full_trace.json`.
- Với `business_prompt_lab`, report nhận ra runners, agent-room flow, output artifacts và tests liên quan.

## 4. Non-Functional Product Requirements

Tóm tắt; chi tiết ở `05_NFR_SECURITY_RISK_VI.md`.

- Local-first.
- Deterministic smoke tests.
- Strict schema boundaries.
- No broad shell access.
- Auditability.
- Extensibility bằng feature/port/adapter.
- Graceful dependency failure.

## 5. Key User Journeys

### Journey A: Chạy một code task nhỏ

```text
User prompt
  -> main.py
  -> Tool Agent
  -> file read/edit
  -> validation
  -> final with evidence
```

### Journey B: Multi-agent code task

```text
User prompt
  -> LangGraph
  -> Research/Planner/Architect
  -> Code edit
  -> Test validation
  -> Review
  -> Ledger
  -> Final
```

### Journey C: Product build lớn

```text
User product prompt
  -> Global Supervisor
  -> Software Factory
  -> implementation spec + handoff packet
  -> Company/LangGraph real coding path
```

### Journey D: Research/current-info

```text
User asks current/source-backed question
  -> Intent Router
  -> Safety
  -> Research Department
  -> Search/Fetch/PDF/Citation
  -> Final Synthesis
```

### Journey E: Mini repo experiment

```text
User chooses lab
  -> python main.py lab list
  -> python main.py lab <name> ...
  -> mini repo runner
  -> lab-specific artifacts
```

### Journey F: Self-evaluating QA

```text
User question
  -> agent room
  -> delegated agent outputs
  -> evaluator + critical agent
  -> baseline comparison
  -> final synthesis + full trace
```

### Journey G: Live user intervention

```text
Run is active
  -> user sends directive
  -> User Agent classifies scope
  -> orchestrator applies/rejects at control point
  -> trace records decision
```

### Journey H: Repo understanding

```text
Target repo
  -> repo-understanding lab
  -> scan docs/symbols/runtime/graphs
  -> understanding report
  -> answer with evidence and confidence
```

## 6. Product Backlog Summary

| Priority | Item |
|---|---|
| P0 | Rebuild minimal CLI + JSON loop |
| P0 | Kernel + capability envelope |
| P0 | File/Python tools + workspace sandbox |
| P0 | JsonGate + schemas |
| P0 | Validation + finish gate |
| P1 | MCP adapter/server set |
| P1 | Event log and inspect CLI |
| P1 | Role agents + allowlists |
| P1 | LangGraph repair path |
| P2 | Software Factory artifacts |
| P2 | Global Supervisor |
| P2 | Mini repo registry |
| P2 | Self-Eval QA Lab |
| P2 | User Agent live control |
| P2 | Repo Understanding Lab |
| P3 | Process Dashboard UI |
| P3 | Real LLM evidence batches |
| P3 | Persistent MCP server pool |
| P3 | RAG reranker/line ranges |
