# Test Strategy

## Test Philosophy

Repo này cần test theo tầng, không chỉ unit test. Lý do: phần khó nhất không
phải từng function riêng lẻ, mà là contract giữa LLM output, JsonGate, tool
schema, kernel, MCP server, orchestrator, role routing và final evidence.

## Test Pyramid Cho Rebuild

```text
Contract/unit tests
  -> deterministic smoke scripts
  -> MCP chain tests
  -> role/orchestration tests
  -> prompt regression tests
  -> optional real LLM/manual demos
```

## Required Gates Per Layer

| Layer | Gate |
|---|---|
| CLI/prompt | main reads prompt, exits clean |
| LLM adapter | mock/manual call |
| JSON loop | parse final/tool, retry invalid |
| Event log | events and summary written |
| Kernel | capability envelope tests |
| Feature loader | enabled/disabled feature tests |
| File/Python tools | path sandbox and execution tests |
| JsonGate | repair and block smoke |
| MCP adapter | registration + mocked adapter call |
| Validation | compile/run file/smoke suite |
| Role agents | allowlist permission smoke |
| LangGraph | compile, failure capture, repair guard |
| Company v0.5 | deterministic full chain smoke |
| Software Factory | artifact completeness smoke |
| Global Supervisor | router/safety/factory route smoke |
| Mini Repo Registry | root lab list/run smoke |
| Self-Eval QA Lab | fake + optional real LLM trace smoke |
| User Agent | directive priority and scope tests |
| Process Dashboard UI | server/API/UI smoke |
| Repo Understanding Lab | report/full-trace/score smoke |
| Real LLM Evidence Loop | LM Studio model discovery + metrics trace |

## Existing Test Commands

Quick:

```powershell
python run_dev_checks.py --quick
```

Full:

```powershell
python run_dev_checks.py --full
```

Individual:

```powershell
python run_kernel_smoke.py
python run_feature_tests.py
python run_json_gate_smoke.py
python run_agent_role_smoke.py
python run_langgraph_smoke.py
python run_mcp_chain_smoke.py
python run_code_test_agents_smoke.py
python run_company_agents_smoke.py
python run_software_factory_smoke.py
python run_global_supervisor_smoke.py
python run_capability_suite.py
```

Mini repo and UI:

```powershell
python main.py lab list
python main.py lab repo-understanding --mock ask "How does PlannerAgent work?"
python main.py lab repo-understanding --repo business_prompt_lab --out-dir var\repo_understanding_lab\business_prompt_lab_v04_test ask "Doc hieu business_prompt_lab: repo nay co nhung runner nao, agent room chay ra sao, output artifacts nam dau, va test nao lien quan?"
python run_process_ui.py --port 8765
```

Real LM Studio evidence:

```powershell
$env:LLM_BASE_URL="http://127.0.0.1:1234/v1"
$env:LLM_API_KEY="lm-studio"
$env:LLM_MODEL="qwen3.5-9b-claude-4.6-opus-uncensored-distilled"
$env:LLM_TIMEOUT="600"
$env:LLM_MAX_TOKENS="1536"
$env:ORCH_MAX_STEPS="6"
Invoke-RestMethod http://127.0.0.1:1234/v1/models
python main.py --max-steps 6 prompts\JSON_fix_01.md
```

Prompt regression:

```powershell
python run_all_cases.py --list
python run_all_cases.py --group capability --fail-fast
python run_all_cases.py --group chain --fail-fast
python run_all_cases.py --case orchestrator_01_json_only
```

## What To Assert

### JsonGate

- Pass valid tool/final.
- Recover common malformed JSON.
- Reject unknown tool.
- Reject missing required args.
- Reject unsafe path.
- Reject git mutation.
- Reject terminal shell shape.

### Tools

- Result has `ok`, `tool`, useful error.
- Sandbox escape blocked.
- Timeout returns structured failure.
- Dependency missing returns `dependency_failure`.
- Mutation tools require env opt-in.

### Orchestrator

- Logs every step.
- Condenses large tool results.
- Blocks repeated same tool call.
- Blocks final after code change without validation.
- Allows final blocker when validation impossible.

### Role Pipeline

- Role cannot call forbidden tool.
- Test failure routes to Code.
- Review does not approve without validation evidence.
- Ledger records only after useful evidence.
- Final does not mutate project.

### Software Factory

- All required artifact keys exist.
- Each artifact path exists.
- Implementation spec includes requested files.
- Business Logic Validation passes only when sections exist.
- Pattern Decision contains hotspot evidence.
- Code Handoff Packet uses artifact refs.

### Mini Repo Registry

- `lab list` includes each registered mini repo.
- Root runner forwards args without swallowing errors.
- Direct mini repo runner and root runner produce compatible artifacts.
- Registry does not import heavy/runtime-only modules at list time.

### Self-Eval QA Lab

- Agent outputs are saved with role, step, public rationale/result and warnings.
- `admin/full_trace.json` preserves raw observable model output without truncation.
- Parse/schema repair is visible in logs.
- Critical agent identifies loops, weak reasoning or unnecessary agents.
- Evolution proposal is saved as proposal-only unless explicitly deployed.

### User Agent

- Directive accepted while run is active.
- User directive priority beats normal agent preference.
- `this_run_only` scope does not leak into future runs.
- Rejected directive includes reason and evidence.

### Process Dashboard UI

- Run list loads when some run dirs are incomplete.
- Timeline/event log shows parse errors, tool failures and repairs.
- Artifact links point to existing files.
- Directive input writes into the same control channel used by CLI/manual tests.

### Repo Understanding Lab

- Manifest excludes noisy runtime/cache dirs.
- Docs reader maps README/docs per mini repo.
- Runtime analyzer finds CLI entrypoints and output dirs.
- Understanding report cites evidence for runners, flow, artifacts and tests.
- Confidence/score is explicit; no unsupported semantic claim.

### Real LLM Evidence

- Model name comes from `/v1/models`, not from memory.
- Metrics include `steps`, `llm_calls`, `tool_calls`, `parse_errors`, `tool_failures`.
- Real run artifacts remain in `var/agent_runs` or lab-specific `var/*` dirs.
- Prompt/flow changes are evaluated in batches, default 20 cases before next edit.

## Definition Of Done For Rebuild

A layer is done only when:

- Code compiles.
- Its smoke passes.
- Its docs mention files and commands accurately.
- Failures are structured, not tracebacks.
- No unrelated refactor is mixed into the layer.
