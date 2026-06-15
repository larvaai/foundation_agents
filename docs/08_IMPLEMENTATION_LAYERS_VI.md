# Implementation Layers To Reach Current Repo

Tài liệu này là bản phân tầng để rebuild repo mới từ con số 0 đến trạng thái
gần repo hiện tại. Mỗi tầng phải chạy được và có smoke test trước khi lên tầng.

## Layer 0 - Repo Skeleton

Mục tiêu:

- Tạo cấu trúc Python project tối thiểu.
- Có `requirements.txt`, `README.md`, `docs/`, `tests/`.

Deliverables:

- `main.py` placeholder.
- `core/runtime_paths.py`.
- `run_dev_checks.py` tối giản chạy compile.

Quality gate:

```powershell
python -m compileall -q .
```

## Layer 1 - CLI And Prompt Loader

Mục tiêu:

- CLI đọc prompt file.
- Có prompt mặc định.
- Encoding ổn trên Windows.

Files:

- `main.py`
- `tools/prompt_loader.py`
- `prompts/system_prompt.md`
- `prompts/user_prompt.md`

Quality gate:

- Chạy `python main.py` không crash khi dùng fake final/echo mode.

## Layer 2 - LLM Adapter

Mục tiêu:

- Gọi OpenAI-compatible API.
- Env override model/base URL.

Files:

- `llm.py`

Quality gate:

- Unit/smoke mock adapter hoặc manual LM Studio call.

## Layer 3 - JSON-Only Single-Agent Loop

Mục tiêu:

- Orchestrator gọi LLM.
- Parse `action=final`.
- Retry invalid JSON đơn giản.

Files:

- `orchestrator.py`
- `agents/tool_agent.py`

Quality gate:

- Test parse final JSON.
- Test invalid JSON retry.

## Layer 4 - Event Log

Mục tiêu:

- Mọi run có run_id, events.jsonl, summary.json.

Files:

- `tools/event_log.py`
- `tools/event_reader.py`
- `inspect_runs.py`

Quality gate:

- Run tạo event log.
- Inspect list/events được.

## Layer 5 - Agent Kernel

Mục tiêu:

- Tách core khỏi tool backend.
- Chuẩn hóa CapabilityResult.

Files:

- `core/kernel.py`
- `core/registry.py`
- `core/schemas.py`
- `core/capabilities.py`
- `core/bootstrap.py`
- `core/events.py`
- `core/state.py`
- `core/ports/tool_port.py`

Quality gate:

- Kernel accept task.
- Unknown tool trả missing/structured error.

## Layer 6 - Minimal Local Tools

Mục tiêu:

- Có tool file và python tối thiểu, chưa cần MCP đầy đủ.
- Workspace sandbox.

Files:

- `mcp_servers/file_editor_server.py`
- `mcp_servers/python_sandbox.py`

Nếu muốn rebuild chậm hơn, tầng này có thể là in-process tools trước, sau đó
mới chuyển sang MCP.

Quality gate:

- Tạo/read file trong workspace.
- Chạy Python file `.py`.
- Path escape bị chặn.

## Layer 7 - JsonGate

Mục tiêu:

- Output LLM phải qua gate trước tool.

Files:

- `output_gate/json_gate.py`
- `output_gate/repair_rules.py`
- `output_gate/repair_loop.py`

Quality gate:

- Fenced JSON/trailing comma/Python literal repair pass.
- Unsafe path blocked.
- Git mutation policy blocked.

## Layer 8 - MCP Feature Adapter

Mục tiêu:

- Kernel gọi tool qua removable feature.
- MCP servers config/schema/policy tách riêng.

Files:

- `features/loader.py`
- `features/contracts.py`
- `features/mcp_tools/config.py`
- `features/mcp_tools/client.py`
- `features/mcp_tools/schemas.py`
- `features/mcp_tools/policy.py`
- `features/mcp_tools/adapter.py`
- `features/mcp_tools/feature.py`
- `config/features.yaml`

Quality gate:

- Feature registers tools.
- Disable aliases works.
- Disable feature still boots kernel.

## Layer 9 - Core MCP Server Set

Mục tiêu:

- Đủ tools cho coding-agent thực dụng.

Implement order:

1. file_editor
2. python
3. lint_test
4. terminal
5. git read-only
6. code_index
7. document
8. ledger
9. issue
10. rag
11. search/fetch
12. docker/obsidian/playwright/pdf/context7

Quality gate:

- `run_mcp_chain_smoke.py`
- schema validation tests.

## Layer 10 - Finish Gate And Repair Loop

Mục tiêu:

- Code change phải validate.
- Failed validation route repair.

Files:

- `orchestrator.py`
- later `orchestration/langgraph_orchestrator.py`

Quality gate:

- Tạo bug, chạy fail, sửa, chạy pass.
- Final bị block nếu chưa validate.

## Layer 11 - Skills

Mục tiêu:

- Markdown skills là workflow instruction, không phải tool.

Files:

- `skills/*/SKILL.md`
- `tools/skill_loader.py`

Skills:

- project-plan
- code-edit
- debug-traceback
- run-test
- git-review

Quality gate:

- Skill loaded prompt.
- Project-plan không edit file.
- Git-review không mutate git.

## Layer 12 - Role Agents

Mục tiêu:

- Tách role boundary và tool allowlists.

Files:

- `agents/base_agent.py`
- `agents/role_agents.py`
- `agents/lenses/`

Quality gate:

- Role cannot call forbidden tool.
- Tool Agent legacy vẫn allowed all.

## Layer 13 - LangGraph Pipeline

Mục tiêu:

- Stateful multi-agent code runtime.

Files:

- `orchestration/agent_state.py`
- `orchestration/langgraph_orchestrator.py`
- `main_langgraph.py`

Quality gate:

- Compile graph.
- Failure capture.
- Repair guard.
- Required/missing file tracking.

## Layer 14 - Department Runtime v0.5

Mục tiêu:

- Deterministic department contract, dễ test.

Files:

- `agents/department_v05.py`
- `agents/research_agent.py`
- `agents/planner_agent.py`
- `agents/architect_agent.py`
- `agents/code_agent.py`
- `agents/test_agent.py`
- `agents/review_agent.py`
- `agents/ledger_agent.py`
- `agents/final_agent.py`
- `orchestration/code_test_orchestrator.py`
- `orchestration/company_orchestrator.py`

Quality gate:

- Code/Test smoke.
- Company smoke.

## Layer 15 - Software Factory v0.7

Mục tiêu:

- Product/business prompt dài đi qua artifacts trước code.

Files:

- `agents/artifact_protocol.py`
- `agents/software_factory_agents.py`
- `orchestration/software_factory_orchestrator.py`
- `run_software_factory_demo.py`
- `run_software_factory_smoke.py`

Quality gate:

- Sinh đủ artifacts.
- Implementation spec có requested files.
- Handoff packet có artifact refs.

## Layer 16 - Global Supervisor

Mục tiêu:

- Không phải request nào cũng đi vào coding graph.

Files:

- `orchestration/intent_router.py`
- `orchestration/global_supervisor.py`
- `agents/knowledge/`
- `agents/research_department/`
- `agents/safety/`
- `agents/final_synthesis_agent.py`

Quality gate:

- Knowledge no tool write.
- Research deterministic no-network by default.
- Product build route Software Factory.
- Prompt injection blocked.

## Layer 17 - Docs And Traceability

Mục tiêu:

- Docs không chỉ mô tả, mà map tới code/test.

Deliverables:

- Architecture.
- BRD.
- PRD.
- Epics/stories/AC.
- NFR/security/risk.
- Rebuild roadmap.
- ADRs.
- Test strategy.
- Traceability matrix.

Quality gate:

- Docs verifier kiểm artifact paths/commands hiện có.

## Layer 18 - Mini Repo Registry

Mục tiêu:

- Root repo chạy được nhiều mini repo thử nghiệm mà không làm bẩn orchestrator chính.

Files:

- `tools/mini_repo_registry.py`
- `business_prompt_lab/README.md`
- `business_prompt_lab/<mini_repo>/main.py`
- `business_prompt_lab/<mini_repo>/docs/`

Quality gate:

- `python main.py lab list` thấy mini repo.
- `python main.py lab <name> ...` chạy được runner của mini repo.
- Mini repo có docs/tests/output dirs riêng.

## Layer 19 - Self-Evaluating QA Lab

Mục tiêu:

- Agent giao việc, phản biện, tổng hợp câu trả lời và so với baseline mà không sinh code.

Files:

- `business_prompt_lab/self_eval_qa_lab/`
- `experiments/self_eval_qa_lab/main.py`
- `business_prompt_lab/self_eval_qa_lab/docs/evolution_proposals/`

Quality gate:

- Fake/deterministic run pass.
- Real local LLM run ghi `summary.md` và `admin/full_trace.json`.
- Critical agent có verdict/recommendation.
- Evolution proposal không tự mutate source khi chưa được duyệt.

## Layer 20 - User Agent Live Control

Mục tiêu:

- Người dùng can thiệp vào run đang chạy với quyền ưu tiên cao.

Files:

- `agents/user_agent.py`
- `orchestrator.py`
- `main.py`
- `tests/test_user_agent*.py`

Quality gate:

- Directive được log với timestamp, scope, step hiện tại.
- Scope `this_run_only` không làm thay đổi run sau.
- Orchestrator áp dụng hoặc reject directive với lý do rõ.

## Layer 21 - Process Dashboard UI

Mục tiêu:

- UI quản lý/quan sát run, agent, state, log, artifacts và directive input.

Files:

- `run_process_ui.py`
- `ui/process_dashboard/`
- `docs/20_PROCESS_DASHBOARD_UI.md`

Quality gate:

- `python run_process_ui.py --port 8765` chạy local.
- UI đọc được run dirs cũ và mới.
- Directive từ UI đi vào User Agent trace.

## Layer 22 - Repo Understanding Lab v0.4

Mục tiêu:

- Mini repo đọc hiểu repo khác, tạo report có evidence thay vì chỉ grep rời rạc.

Files:

- `business_prompt_lab/repo_understanding_lab/main.py`
- `business_prompt_lab/repo_understanding_lab/repo_understanding/`
- `business_prompt_lab/repo_understanding_lab/docs/`
- `business_prompt_lab/repo_understanding_lab/tests/test_repo_understanding_lab.py`

Quality gate:

- Chạy được qua root `main.py lab repo-understanding`.
- Sinh `reports/understanding_report.json`.
- Sinh `admin/full_trace.json`.
- Đọc hiểu `business_prompt_lab` đạt score >= 4.0/5.

## Layer 23 - Real LLM Evidence Loop

Mục tiêu:

- Chạy thật với LM Studio/OpenAI-compatible model và dùng log làm cơ sở chỉnh tiếp.

Files:

- `llm.py`
- `var/agent_runs/<run_id>/`
- `var/self_eval_qa_lab/<run_id>/`
- `docs/rebuild_from_zero/13_REBUILD_PLAYBOOK_VI.md`

Quality gate:

- Lấy model list từ `http://127.0.0.1:1234/v1/models`.
- Root orchestrator real run ghi metrics `steps`, `llm_calls`, `tool_calls`, `parse_errors`.
- Self-eval real run ghi baseline comparison và critical audit.
- Không chỉnh prompt/flow tiếp nếu chưa có batch evidence, mặc định 20 cases/lần đánh giá.
