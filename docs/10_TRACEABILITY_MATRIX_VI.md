# Traceability Matrix

## Purpose

Matrix này giúp bạn kiểm soát rebuild: mỗi business goal phải trace được tới
product requirement, epic/story, code module và test/smoke tương ứng.

## Matrix

| Business Goal | PRD Requirement | Epic/Story | Code Modules | Tests/Smoke |
|---|---|---|---|---|
| BG-01 Local coding-agent | FR-01, FR-02 | E01-S01, E01-S02 | `main.py`, `llm.py`, `tools/prompt_loader.py` | CLI smoke, compile |
| BG-02 Tool action có schema/policy/log | FR-04, FR-06, FR-11 | E02, E04, E09 | `output_gate/`, `features/mcp_tools/`, `tools/event_log.py` | `run_json_gate_smoke.py`, `run_mcp_chain_smoke.py` |
| BG-03 Code change phải validate | FR-09, FR-10 | E05 | `orchestrator.py`, `lint_test_server.py`, `python_sandbox.py` | agent fix bug case, finish gate smoke |
| BG-04 Role ownership | FR-12, FR-13, FR-14 | E06 | `agents/base_agent.py`, `agents/role_agents.py`, `orchestration/langgraph_orchestrator.py` | `run_agent_role_smoke.py`, `run_langgraph_smoke.py` |
| BG-05 Product prompt có BRD/PRD trước code | FR-15 | E07 | `agents/software_factory_agents.py`, `orchestration/software_factory_orchestrator.py` | `run_software_factory_smoke.py` |
| BG-06 Rebuild theo tầng | Docs | Roadmap | `docs/rebuild_from_zero/` | docs review |
| BG-07 Local-first dễ đọc | NFR-01, NFR-09 | all | toàn repo | `run_dev_checks.py --quick` |
| BG-08 Mini repo experiments | FR-17 | E10 | `tools/mini_repo_registry.py`, `business_prompt_lab/` | `tests/test_mini_repo_registry.py` |
| BG-09 Self-evaluating QA | FR-18 | E11 | `experiments/self_eval_qa_lab/`, `business_prompt_lab/self_eval_qa_lab/` | fake run, real LM Studio run |
| BG-10 Live user control | FR-19 | E12-S01 | `agents/user_agent.py`, `orchestrator.py` | `tests/test_user_agent*.py` |
| BG-11 Process dashboard | FR-20 | E12-S02 | `run_process_ui.py`, `ui/process_dashboard/` | dashboard server/API smoke |
| BG-12 Repo understanding | FR-21 | E13 | `business_prompt_lab/repo_understanding_lab/` | `tests/test_repo_understanding_lab.py` |

## Product Artifact Trace

| Artifact | Producer | Consumer | Gate |
|---|---|---|---|
| Protocol Strategy | Intake Protocol Agent | Product Vision Agent | Long analysis uses artifacts |
| Vision | Product Vision Agent | BRD Agent | No Vision -> no BRD |
| BRD | BRD Agent | PRD Agent | No BRD -> no PRD |
| PRD | PRD Agent | Epic Story Agent | Product requirements known |
| Epics/Stories | Epic Story Agent | AC Agent | Stories exist |
| Acceptance Criteria | AC Agent | Product Validator, Domain Analyst | No AC -> no technical design |
| Product Validation | Product Spec Validator | Product Critic | Product spec complete |
| Product Critique | Product Spec Critic | Domain Analyst | No early pattern selection |
| Domain Analysis | Domain Analyst | Business Logic, Technical, Pattern | Hotspots identified |
| Business Logic Model | Business Logic Model Agent | Validator, Implementation Spec | Executable intent |
| Business Logic Validation | Validator | Technical Analyst | No logic contract -> no technical |
| Technical Analysis | Technical Analyst | Pattern Decision | Boundaries known |
| Pattern Decision | Pattern Decision Agent | Implementation Spec | Pattern traces to hotspot |
| Implementation Spec | Implementation Spec Agent | Code Handoff, Coding runtime | Code contract |
| Code Handoff Packet | Packager | Company/LangGraph Code Agent | Artifact refs and must/must-not |
| Docs Verification | Docs Verifier | Factory Final | No docs verification -> not done |

## Lab Artifact Trace

| Artifact | Producer | Consumer | Gate |
|---|---|---|---|
| Lab Registry Entry | `tools/mini_repo_registry.py` | root `main.py lab ...` | Lab cannot run if missing runner/docs path |
| Self-Eval Summary | Self-Eval QA Lab | Operator/Critical review | Must include workflow, verdict, comparison |
| Self-Eval Full Trace | Observer | Admin/debugger | Raw observable outputs retained without UI truncation |
| Evolution Proposal | Critical/Decision agent | Future implementation task | Proposal-only until explicitly deployed |
| User Directive Event | User Agent | Orchestrator/UI/admin | Must include scope and applied/rejected status |
| Repo Understanding Report | Repo Understanding Lab | User/future agents | Must cite evidence and confidence |

## Test Coverage Map

| Area | Current Test |
|---|---|
| Kernel contract | `tests/test_kernel_contracts.py` |
| Feature contract | `tests/test_feature_contracts.py` |
| MCP feature registration | `tests/test_mcp_tools_feature.py` |
| JsonGate | `run_json_gate_smoke.py` |
| Role permission | `run_agent_role_smoke.py` |
| LangGraph | `run_langgraph_smoke.py` |
| MCP chain | `run_mcp_chain_smoke.py` |
| Code/Test v0.5 | `run_code_test_agents_smoke.py` |
| Company v0.5 | `run_company_agents_smoke.py` |
| Software Factory | `run_software_factory_smoke.py` |
| Global Supervisor | `run_global_supervisor_smoke.py` |
| Overall capability | `run_capability_suite.py` |
| Prompt regression | `run_all_cases.py` |
| Mini Repo Registry | `tests/test_mini_repo_registry.py` |
| User Agent | `tests/test_user_agent*.py` |
| Process Dashboard UI | dashboard server/API smoke |
| Repo Understanding Lab | `tests/test_repo_understanding_lab.py` |
| Real LLM evidence | LM Studio root/self-eval smoke |
