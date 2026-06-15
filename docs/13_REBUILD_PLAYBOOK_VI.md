# Rebuild Playbook

## Cách Dùng

Playbook này là checklist thực thi. Khi bắt đầu repo mới, chỉ làm một tầng tại
một thời điểm. Không kéo code của tầng sau vào tầng trước.

Mỗi tầng có:

- Mục tiêu.
- Files cần tạo.
- Lệnh kiểm tra.
- Điều kiện pass.
- Điều không được làm ở tầng đó.

## Tầng 1 - CLI + Prompt Loader

Mục tiêu:

- Chạy được CLI.
- Đọc prompt file.
- Chưa cần LLM thật.

Files:

```text
main.py
tools/prompt_loader.py
prompts/user_prompt.md
prompts/system_prompt.md
requirements.txt
```

Implementation:

- `main.py` nhận optional `sys.argv[1]`.
- `read_user_prompt(path)` đọc UTF-8.
- Nếu không có path, đọc `prompts/user_prompt.md`.
- In prompt hoặc fake final để xác nhận wiring.

Check:

```powershell
python main.py
python main.py prompts/user_prompt.md
python -m compileall -q main.py tools
```

Pass:

- Không crash.
- Đọc đúng prompt.
- Không có LLM/tool/orchestrator logic phức tạp.

Không làm:

- Không thêm MCP.
- Không thêm multi-agent.
- Không thêm JsonGate.

## Tầng 2 - LLM Adapter + JSON Final

Mục tiêu:

- Gọi LLM OpenAI-compatible.
- Agent trả final JSON.

Files:

```text
llm.py
agents/tool_agent.py
orchestrator.py
```

Implementation:

- `llm.py` chứa `call_llm(messages)`.
- `tool_agent(messages)` render system prompt tối giản.
- `orchestrator.run_orchestrator(task)` gọi agent và parse JSON.
- Chỉ hỗ trợ `action=final` trước.

Check:

```powershell
python main.py prompts/user_prompt.md
```

Pass:

- Valid final JSON được parse.
- Invalid JSON trả lỗi rõ hoặc retry tối giản.

Không làm:

- Chưa gọi tool.
- Chưa cần MCP.

## Tầng 3 - Event Log

Mục tiêu:

- Mỗi run có audit trail.

Files:

```text
core/runtime_paths.py
tools/event_log.py
tools/event_reader.py
inspect_runs.py
```

Implementation:

- Runtime dirs: `var/workspace`, `var/agent_runs`, `var/test_runs`.
- Event types tối thiểu: `MessageEvent`, `ActionEvent`, `StateEvent`.
- Summary chứa status, metrics, final_message.

Check:

```powershell
python main.py prompts/user_prompt.md
python inspect_runs.py list
python inspect_runs.py events latest --limit 20
```

Pass:

- Có `events.jsonl`.
- Có `summary.json`.
- Inspect đọc được.

Không làm:

- Không đưa business logic vào event logger.

## Tầng 4 - Kernel + CapabilityResult

Mục tiêu:

- Tách core khỏi tool backend.

Files:

```text
core/schemas.py
core/events.py
core/state.py
core/ports/tool_port.py
core/registry.py
core/kernel.py
core/bootstrap.py
core/capabilities.py
tests/test_kernel_contracts.py
run_kernel_smoke.py
```

Implementation:

- `CapabilityResult` có envelope ổn định.
- `CapabilityRegistry` resolve exact tool hoặc null tool.
- `AgentKernel.execute_tool()` publish event và wrap result.

Check:

```powershell
python run_kernel_smoke.py
python -m unittest tests.test_kernel_contracts
```

Pass:

- Unknown tool không crash.
- Disabled feature/null tool trả structured failure.

Không làm:

- Core không import MCP/RAG/browser/docker.

## Tầng 5 - Minimal File/Python Tools

Mục tiêu:

- Agent có thể tạo file và chạy file Python trong workspace.

Files:

```text
mcp_servers/file_editor_server.py
mcp_servers/python_sandbox.py
```

Có thể bắt đầu bằng in-process adapter nếu chưa muốn MCP, nhưng contract tool
result phải giữ giống MCP.

Check:

```powershell
python -m compileall -q mcp_servers
```

Manual/smoke:

- Create `var/workspace/code/hello.py`.
- Run `python.run_python` và thấy stdout.
- Thử path `../x.py` phải bị block.

Pass:

- File chỉ nằm trong workspace.
- Chỉ `.py` được chạy.
- Timeout hoạt động.

Không làm:

- Không cho arbitrary shell.

## Tầng 6 - JsonGate + Schemas + Policy

Mục tiêu:

- Không tool nào chạy nếu JSON/action/args không hợp lệ.

Files:

```text
output_gate/json_gate.py
output_gate/repair_rules.py
output_gate/repair_loop.py
features/mcp_tools/schemas.py
features/mcp_tools/policy.py
run_json_gate_smoke.py
```

Check:

```powershell
python run_json_gate_smoke.py
```

Pass:

- Valid tool/final pass.
- Fenced JSON repaired.
- Unsafe path blocked.
- Git mutation blocked.

Không làm:

- JsonGate không execute tool thật.

## Tầng 7 - MCP Adapter Feature

Mục tiêu:

- Tool execution qua feature adapter.

Files:

```text
features/loader.py
features/contracts.py
features/mcp_tools/config.py
features/mcp_tools/client.py
features/mcp_tools/adapter.py
features/mcp_tools/feature.py
config/features.yaml
tests/test_feature_contracts.py
tests/test_mcp_tools_feature.py
run_feature_tests.py
```

Check:

```powershell
python run_feature_tests.py
```

Pass:

- Feature registers canonical tools.
- Alias registration can be disabled.
- Tool result wrapped by kernel.

Không làm:

- Không để orchestrator gọi MCP client trực tiếp.

## Tầng 8 - Validation Discipline

Mục tiêu:

- Code edit không được final nếu chưa validate.

Files:

```text
mcp_servers/lint_test_server.py
mcp_servers/terminal_server.py
orchestrator.py
run_mcp_chain_smoke.py
```

Implementation:

- Detect code-change tools.
- Detect validation tools.
- Pending validation flag.
- Repeated tool guard.
- Condense tool result before feeding back to LLM.

Check:

```powershell
python run_mcp_chain_smoke.py
python run_all_cases.py --group project --fail-fast
```

Pass:

- Code change requires validation.
- Terminal blocks shell.
- Tool failure repeated stops.

Không làm:

- Không dùng terminal để edit.

## Tầng 9 - Skills

Mục tiêu:

- Workflow instructions có thể gắn vào system prompt.

Files:

```text
skills/project-plan/SKILL.md
skills/code-edit/SKILL.md
skills/debug-traceback/SKILL.md
skills/run-test/SKILL.md
skills/git-review/SKILL.md
tools/skill_loader.py
```

Check:

```powershell
python run_all_cases.py --group skill --fail-fast
```

Pass:

- Project-plan không edit.
- Git-review không mutate git.

Không làm:

- Skill không phải tool; không đặt skill name vào `tool`.

## Tầng 10 - Role Agents

Mục tiêu:

- Tách quyền theo role.

Files:

```text
agents/base_agent.py
agents/role_agents.py
agents/lenses/
run_agent_role_smoke.py
```

Check:

```powershell
python run_agent_role_smoke.py
```

Pass:

- Role gọi forbidden tool bị block.
- Role allowlist expand đúng.

Không làm:

- Chưa cần LangGraph nếu role smoke chưa ổn.

## Tầng 11 - LangGraph Pipeline

Mục tiêu:

- Multi-agent state machine cho coding task.

Files:

```text
orchestration/agent_state.py
orchestration/langgraph_orchestrator.py
main_langgraph.py
run_langgraph_smoke.py
```

Check:

```powershell
python run_langgraph_smoke.py
```

Pass:

- Graph compile.
- Failure summary capture.
- Repair guard hoạt động.
- Finish gate hoạt động.

Không làm:

- Không cho từng role tự execute tool ngoài tool node.

## Tầng 12 - Company Agents v0.5

Mục tiêu:

- Department contract deterministic.

Files:

```text
agents/department_v05.py
agents/*_agent.py
orchestration/code_test_orchestrator.py
orchestration/company_orchestrator.py
run_code_test_agents_smoke.py
run_company_agents_smoke.py
```

Check:

```powershell
python run_code_test_agents_smoke.py
python run_company_agents_smoke.py
```

Pass:

- Code writes scoped file.
- Test runs validation.
- Review approves only after pass.
- Ledger records.
- Final routes done.

Không làm:

- Không thay thế LangGraph real runtime vội; dùng làm contract target.

## Tầng 13 - Software Factory

Mục tiêu:

- Product prompt dài sinh spec artifacts trước coding.

Files:

```text
agents/artifact_protocol.py
agents/software_factory_agents.py
orchestration/software_factory_orchestrator.py
run_software_factory_smoke.py
run_software_factory_demo.py
```

Check:

```powershell
python run_software_factory_smoke.py
```

Pass:

- Đủ Vision/BRD/PRD/Stories/AC/Domain/Logic/Technical/Pattern/Spec/Handoff/Docs artifacts.
- Pattern decision có hotspot evidence.
- Implementation spec có requested files.

Không làm:

- Software Factory không claim đã implement source code.

## Tầng 14 - Global Supervisor

Mục tiêu:

- Route đúng request ngoài coding.

Files:

```text
orchestration/intent_router.py
orchestration/global_supervisor.py
agents/knowledge/
agents/research_department/
agents/safety/
agents/final_synthesis_agent.py
run_global_supervisor_smoke.py
```

Check:

```powershell
python run_global_supervisor_smoke.py
python run_capability_suite.py
```

Pass:

- Knowledge không dùng repo write tools.
- Research no-network mặc định.
- Product build route Software Factory.
- Safety blocks prompt injection.

Không làm:

- Không bật real coding/network mặc định nếu chưa cần.

## Tầng 15 - Hardening Before Daily Use

Mục tiêu:

- Làm repo mới đủ ổn để dùng hằng ngày.

Checklist:

- Fix encoding docs/prompts.
- Add docs index.
- Add traceability matrix.
- Add ADRs.
- Add dev quick/full checks.
- Add cleanup policy cho runtime artifacts.
- Decide MCP process pooling.

Check:

```powershell
python run_dev_checks.py --quick
python run_dev_checks.py --full
```

Pass:

- Quick pass trước mỗi change.
- Full pass trước milestone lớn.

## Tầng 16 - Mini Repo Registry + Business Prompt Lab

Mục tiêu:

- Repo chính có thể chứa nhiều mini repo độc lập dưới `business_prompt_lab`.
- `main.py` vẫn là entrypoint thống nhất để liệt kê và chạy mini repo.
- Mỗi mini repo có docs, tests, runner và output artifacts riêng.

Files:

```text
tools/mini_repo_registry.py
business_prompt_lab/README.md
business_prompt_lab/self_eval_qa_lab/
business_prompt_lab/repo_understanding_lab/
```

Implementation:

- Thêm subcommand `python main.py lab list`.
- Registry khai báo `name`, `description`, `path`, `runner`, `docs`, `default_args`.
- Mini repo không được phụ thuộc ngược vào logic riêng của root ngoài public runner contract.
- Mỗi mini repo có cây docs nội bộ trước khi code.

Check:

```powershell
python main.py lab list
python main.py lab repo-understanding --mock ask "How does PlannerAgent work?"
python -m unittest tests.test_mini_repo_registry
```

Pass:

- `lab list` thấy được các mini repo.
- Chạy mini repo qua root `main.py` được.
- Mini repo vẫn chạy trực tiếp bằng `business_prompt_lab/<repo>/main.py`.

Không làm:

- Không nhét code thử nghiệm trực tiếp vào root orchestrator nếu có thể để trong mini repo.
- Không để mini repo ghi đè config/runtime của root.

## Tầng 17 - Self-Evaluating QA Lab + Evolution Proposals

Mục tiêu:

- Agent nói chuyện với nhau, giao việc, phản biện và tổng hợp câu trả lời mà không sinh code.
- So sánh output của agent system với baseline ChatGPT/local baseline.
- Lưu toàn bộ quá trình quan sát được để admin soi lại.
- Critical agent đề xuất chỉnh sửa agent/flow/skills/tools cho lần sau nhưng không tự sửa code nếu chưa được duyệt.

Files:

```text
business_prompt_lab/self_eval_qa_lab/main.py
business_prompt_lab/self_eval_qa_lab/docs/
business_prompt_lab/self_eval_qa_lab/docs/evolution_proposals/
experiments/self_eval_qa_lab/main.py
```

Implementation:

- Workflow tối thiểu: planner -> worker agents -> evaluator -> critical agent -> decision/evolution proposal -> final synthesis.
- Mọi agent output phải ghi vào run dir: public reasoning/rationale, result, confidence, handoff, warnings.
- `admin/full_trace.json` giữ raw model outputs không truncate cho admin.
- Ghi rõ trong docs: full trace là full observable trace, không claim đọc được hidden internal chain-of-thought của model.

Check:

```powershell
python experiments\self_eval_qa_lab\main.py --llm-provider fake --chatgpt-mode fake --workflow assisted --propose-updates "Explain why JSON-only agents get brittle."
```

Real LLM check qua LM Studio:

```powershell
$env:LLM_BASE_URL="http://127.0.0.1:1234/v1"
$env:LLM_API_KEY="lm-studio"
python experiments\self_eval_qa_lab\main.py --llm-provider local --model "qwen3.5-9b-claude-4.6-opus-uncensored-distilled" --chatgpt-mode local --baseline-mode local --workflow assisted --propose-updates --llm-timeout 600 --max-tokens 1024 --temperature 0.1 --out-dir var\self_eval_qa_lab\qwen35_real "Question here"
```

Pass:

- Có `summary.md`.
- Có `admin/full_trace.json`.
- Có warning rõ khi parse/schema fail và repair succeed/fail.
- Critical agent trả verdict, logic score, recommendation.
- Evolution proposal chỉ là artifact được đề xuất, chưa tự mutate repo.

Không làm:

- Không cho decision/evolution agent tự sửa source code production nếu chưa có command triển khai riêng.
- Không dùng một case đơn lẻ để sửa prompt ngay; gom batch, ví dụ sau mỗi 20 case mới đánh giá.

## Tầng 18 - User Agent Live Control

Mục tiêu:

- Người dùng có thể nhập chỉ đạo trong lúc run đang diễn ra.
- User directive có quyền ưu tiên rất cao trong lượt chạy hiện tại.
- Hỗ trợ directive tạm thời như: "lượt này bỏ agent X, lượt sau vẫn cần".

Files:

```text
agents/user_agent.py
orchestrator.py
main.py
docs/*USER_AGENT*.md
tests/test_user_agent*.py
```

Implementation:

- Tạo hàng đợi directive/event để orchestrator poll giữa các step.
- Phân loại scope: `this_run_only`, `future_runs`, `config_proposal`.
- Directive có thể yêu cầu add/remove/skip agent, thêm skill/tool, đổi priority, dừng/summarize.
- Mọi directive được log cùng thời điểm nhận, step đang chạy, action áp dụng và lý do nếu không áp dụng.

Check:

```powershell
python -m unittest tests.test_user_agent
python main.py --max-steps 6 prompts\JSON_fix_01.md
```

Manual check:

- Trong lúc run, gửi directive: "Trong lượt này bỏ bớt vai trò reviewer; lượt sau vẫn cần".
- Xác nhận trace ghi scope là `this_run_only`.
- Xác nhận lượt sau config mặc định không mất reviewer.

Pass:

- User directive không bị agent khác bỏ qua.
- Scope tạm thời không làm hỏng cấu hình lâu dài.
- Log đủ để audit sau run.

Không làm:

- Không để user agent chạy tool mutation trực tiếp nếu orchestrator chưa approve.
- Không biến mọi directive thành sửa code/config vĩnh viễn.

## Tầng 19 - Process Dashboard UI

Mục tiêu:

- Người dùng nhìn được toàn bộ process: run hiện tại, agent đang chạy, state, log, artifacts, LangGraph/company flow.
- Người dùng nhập directive cho User Agent từ UI.
- UI là observability/control surface, không thay thế CLI.

Files:

```text
run_process_ui.py
ui/process_dashboard/
docs/20_PROCESS_DASHBOARD_UI.md
tests/test_process_dashboard*.py
```

Implementation:

- Server local đọc `var/agent_runs`, `var/self_eval_qa_lab`, `var/repo_understanding_lab`.
- API tối thiểu: list runs, get run detail, stream/poll events, post user directive.
- UI hiển thị:
  - active run/process state
  - agents and step status
  - event log
  - artifacts
  - warnings/parse repairs/tool failures
  - directive input
- Nếu có LangGraph state thì render node/status; nếu chưa có thì hiển thị fallback linear timeline.

Check:

```powershell
python run_process_ui.py --port 8765
```

Mở:

```text
http://127.0.0.1:8765
```

Pass:

- UI load được run cũ và run mới.
- Log không bị mất event quan trọng.
- Directive từ UI được ghi vào run trace.
- Server không crash khi run dir thiếu optional artifact.

Không làm:

- Không dùng UI để sửa source file trực tiếp.
- Không che mất raw/admin log; UI có thể rút gọn, nhưng phải link tới artifact đầy đủ.

## Tầng 20 - Repo Understanding Lab v0.4

Mục tiêu:

- Mini repo tự đọc hiểu code project khác, đặc biệt là `business_prompt_lab`.
- Sinh manifest, docs map, symbols, graphs, runtime map, context pack, understanding report và full trace.
- Trả lời câu hỏi về runner, agent room, output artifacts, tests liên quan.

Files:

```text
business_prompt_lab/repo_understanding_lab/main.py
business_prompt_lab/repo_understanding_lab/repo_understanding/
business_prompt_lab/repo_understanding_lab/docs/
business_prompt_lab/repo_understanding_lab/tests/test_repo_understanding_lab.py
```

Implementation:

- Scanner đọc repo target và bỏ qua cache/runtime không cần thiết.
- Docs reader map README/docs nội bộ.
- Symbol extractor map functions/classes/imports.
- Runtime analyzer tìm entrypoints, argparse/subcommands, output dirs.
- Graph builder tạo dependency/call-ish graph ở mức đủ dùng.
- Understanding engine synthesize flow và confidence score.
- Observer ghi `admin/full_trace.json`.

Check:

```powershell
python main.py lab repo-understanding --repo business_prompt_lab --out-dir var\repo_understanding_lab\business_prompt_lab_v04_test ask "Doc hieu business_prompt_lab: repo nay co nhung runner nao, agent room chay ra sao, output artifacts nam dau, va test nao lien quan?"
python -m unittest tests.test_repo_understanding_lab
```

Pass:

- Score đạt tối thiểu 4.0/5 cho `business_prompt_lab`.
- Report nhận ra flow chính của self-eval/agent-room.
- Report map được output artifacts và tests liên quan.
- Có `reports/understanding_report.json`.
- Có `admin/full_trace.json`.

Không làm:

- Không claim hiểu semantic sâu nếu chỉ dựa trên grep; phải ghi confidence và evidence.
- Không bỏ qua docs nội bộ của mini repo.

## Tầng 21 - Real LLM Production Evidence Loop

Mục tiêu:

- Chạy thật qua LM Studio/OpenAI-compatible model.
- Log đủ để phân tích JSON discipline, repair, tool calls, critical audit và baseline comparison.
- Có quy trình đánh giá trước khi chỉnh prompt/flow tiếp theo.

Model discovery:

```powershell
Invoke-RestMethod http://127.0.0.1:1234/v1/models
```

Root orchestrator real run:

```powershell
$env:LLM_BASE_URL="http://127.0.0.1:1234/v1"
$env:LLM_API_KEY="lm-studio"
$env:LLM_MODEL="qwen3.5-9b-claude-4.6-opus-uncensored-distilled"
$env:LLM_TIMEOUT="600"
$env:LLM_MAX_TOKENS="1536"
$env:ORCH_MAX_STEPS="6"
python main.py --max-steps 6 prompts\JSON_fix_01.md
```

Expected artifacts:

```text
var/agent_runs/<run_id>/events.jsonl
var/agent_runs/<run_id>/summary.json
var/self_eval_qa_lab/<run_id>/summary.md
var/self_eval_qa_lab/<run_id>/admin/full_trace.json
```

Pass:

- Run `completed` hoặc fail có blocker rõ.
- Metrics ghi `steps`, `llm_calls`, `tool_calls`, `parse_errors`, `tool_failures`.
- Parse errors/repairs được log thay vì mất dấu.
- Critical audit không chỉ khen; phải chỉ ra chỗ loop kém thông minh hoặc luẩn quẩn.
- Chỉ chỉnh prompt/flow sau batch đủ lớn, mặc định 20 case/lần đánh giá.

Không làm:

- Không sửa prompt theo cảm tính sau một output xấu.
- Không xóa log cũ trước khi đánh giá.
- Không nhầm danh sách model với guess; phải lấy từ `/v1/models` khi chạy local.
