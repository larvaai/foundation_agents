# Rebuild Roadmap

## Nguyên Tắc Rebuild

- Không copy toàn bộ repo ngay.
- Mỗi milestone có một runtime chạy được.
- Mỗi milestone có smoke test.
- Không thêm multi-agent trước khi single-agent + tools + validation ổn.
- Không thêm Software Factory trước khi artifact protocol rõ.
- Không thêm UI trước khi event log và inspect ổn.

## Milestone M0 - Project Baseline

Scope:

- Repo skeleton.
- Runtime paths.
- Prompt loader.
- Dev check compile.

Exit criteria:

- `python -m compileall -q .` pass.
- `python main.py` chạy được ở fake mode.

## Milestone M1 - Single-Agent JSON Runtime

Scope:

- LLM adapter.
- Tool Agent prompt.
- Orchestrator parse final/tool JSON.
- Simple retry.

Exit criteria:

- Prompt final JSON pass.
- Invalid JSON retry pass.

## Milestone M2 - Event Log And Inspect

Scope:

- EventLogger.
- events.jsonl.
- summary.json.
- inspect CLI.

Exit criteria:

- Một run có MessageEvent/ActionEvent/StateEvent.
- `inspect_runs.py list/events latest` chạy được.

## Milestone M3 - Kernel And Capability Contract

Scope:

- AgentKernel.
- CapabilityRegistry.
- ToolPort.
- CapabilityResult.
- Feature loader.

Exit criteria:

- Kernel tests pass.
- Disabled feature không crash.

## Milestone M4 - Minimal Tools And Sandbox

Scope:

- file_editor view/create/write_lines/replace/insert.
- python sandbox.
- path safety.

Exit criteria:

- Create file, read/view file, run Python file.
- Path escape blocked.

## Milestone M5 - JsonGate And Tool Schemas

Scope:

- JsonGate parse/repair.
- Tool schema registry.
- Tool alias resolution.
- Policy dry-run.

Exit criteria:

- JsonGate smoke pass.
- Unsafe path/git mutation blocked.

## Milestone M6 - MCP Adapter

Scope:

- MCP server config.
- MCP stdio client.
- Adapter feature.
- Schema/policy integrated.

Exit criteria:

- Kernel -> MCP tool call works.
- Tool result normalized.

## Milestone M7 - Validation Discipline

Scope:

- lint_test server.
- terminal safe runner.
- finish gate.
- context condenser.
- repeated tool/failure guards.

Exit criteria:

- Code edit requires validation.
- Failed tool twice stops.
- Same tool loop blocked.

## Milestone M8 - Test Harness

Scope:

- run_all_cases.
- run_dev_checks.
- deterministic smoke scripts.

Exit criteria:

- Quick checks pass.
- Prompt cases can be run by group/case.

## Milestone M9 - Role Agents

Scope:

- BaseAgent.
- Role registry.
- Tool allowlists.
- Lenses as prompt/spec.

Exit criteria:

- Role permission smoke pass.
- Code/Test/Review/Ledger boundaries enforced.

## Milestone M10 - LangGraph Multi-Agent Runtime

Scope:

- AgentState.
- Role nodes.
- Tool node.
- route_next.
- last_failure repair flow.

Exit criteria:

- LangGraph compile smoke pass.
- Failed-test repair guard pass.

## Milestone M11 - Company Agents v0.5

Scope:

- Deterministic department agents.
- Department result contract.
- Code/Test orchestrator.
- Full company orchestrator.

Exit criteria:

- Code/Test smoke pass.
- Company smoke pass.

## Milestone M12 - Software Factory v0.7

Scope:

- Artifact protocol.
- Factory agents.
- Product/business/domain/logic/technical/docs artifacts.
- Handoff packet.

Exit criteria:

- Software Factory smoke pass.
- Required artifact keys exist.
- Implementation spec can be fed to coding path.

## Milestone M13 - Global Supervisor

Scope:

- Intent router.
- Knowledge agents.
- Research department skeleton.
- Safety department.
- Final synthesis.

Exit criteria:

- Global supervisor smoke pass.
- Product prompt routes to Software Factory.
- Prompt injection blocked.

## Milestone M14 - Hardening

Scope:

- Encoding cleanup.
- RAG health and failure quality.
- More test coverage.
- Docs verification.
- MCP process pooling design.

Exit criteria:

- `run_dev_checks.py --full` pass.
- Docs and traceability updated.

## Milestone M15 - Mini Repo Registry

Scope:

- `business_prompt_lab` as experiment workspace.
- `tools/mini_repo_registry.py`.
- Root `main.py lab list` and `main.py lab <name> ...`.
- Docs/tests per mini repo.

Exit criteria:

- Mini repos can run through root `main.py`.
- Each mini repo can also run directly.
- Registry test pass.

## Milestone M16 - Self-Evaluating QA Lab

Scope:

- Agent room for question answering, delegation and final synthesis.
- Critical agent.
- Baseline comparison.
- Evolution proposal docs folder.
- Observable full trace for admin.

Exit criteria:

- Fake/deterministic run pass.
- Real LM Studio run writes `summary.md`, outputs and `admin/full_trace.json`.
- Critical audit gives actionable recommendation.
- Proposed changes remain proposals unless explicitly deployed.

## Milestone M17 - User Agent Live Control

Scope:

- `agents/user_agent.py`.
- Directive queue/event model.
- Scope handling: current run, future run, proposal.
- Orchestrator integration.

Exit criteria:

- User directive can skip/remove/add an agent for current run.
- Temporary directive does not persist to the next run.
- Directive appears in run trace with applied/rejected status.

## Milestone M18 - Process Dashboard UI

Scope:

- Local dashboard server.
- Run list/detail.
- Agent/state/timeline/log/artifact views.
- Directive input into User Agent.

Exit criteria:

- `python run_process_ui.py --port 8765` serves UI.
- UI can inspect existing `var/agent_runs` and lab run dirs.
- UI handles missing optional files without crashing.

## Milestone M19 - Repo Understanding Lab v0.4

Scope:

- Scanner, docs reader, symbols, graphs, runtime map.
- Context pack and understanding report.
- Full observable trace.
- Specialized answers for runner/agent-room/artifact/test questions.

Exit criteria:

- `business_prompt_lab` understanding run reaches score >= 4.0/5.
- Report identifies main runners, flow, artifacts and tests.
- `reports/understanding_report.json` and `admin/full_trace.json` exist.

## Milestone M20 - Real LLM Evidence Loop

Scope:

- LM Studio model discovery.
- Root orchestrator real run.
- Self-eval real run.
- Batch evaluation before prompt/flow edits.

Exit criteria:

- `/v1/models` confirms selected model.
- Root run completes or records clear blocker.
- Metrics include parse/tool/LLM counts.
- Self-eval records baseline winner, flow verdict and critical recommendation.
- Prompt/flow edits are based on a batch, default 20 cases.

## Suggested Work Order For New Repo

Sprint 1:

- M0, M1, M2.

Sprint 2:

- M3, M4.

Sprint 3:

- M5, M6.

Sprint 4:

- M7, M8.

Sprint 5:

- M9, M10.

Sprint 6:

- M11.

Sprint 7:

- M12.

Sprint 8:

- M13, M14.

Sprint 9:

- M15, M16.

Sprint 10:

- M17, M18.

Sprint 11:

- M19, M20.

Không chuyển sprint nếu exit criteria của milestone trước chưa pass.
