# Domain And Business Logic

## Domain Cốt Lõi

Domain của repo là "agent runtime for controlled software work".

Các khái niệm chính:

| Entity | Ý nghĩa |
|---|---|
| User Task | Yêu cầu gốc từ user/prompt file |
| Agent | Vai trò LLM hoặc deterministic department |
| Action | JSON object agent trả về |
| Tool Request | Tool name + args sau khi parse |
| Capability | Một khả năng thực thi qua kernel |
| Feature | Module cung cấp capabilities |
| MCP Server | Backend tool thực tế |
| Tool Result | Kết quả raw/normalized từ tool |
| CapabilityResult | Envelope chuẩn của kernel |
| Event | Log của message/action/tool/state/error |
| Artifact | File dài chứa analysis/spec/docs |
| Route Decision | Quyết định next agent/department |
| Validation Evidence | Kết quả test/probe chứng minh |
| Ledger Entry | Memory/audit JSONL |
| Issue | Task/bug/risk trong SQLite |
| Mini Repo | Experiment repo nhỏ chạy qua registry |
| User Directive | Chỉ đạo runtime từ người dùng khi run đang diễn ra |
| Evolution Proposal | Đề xuất thay agent/flow/skill/tool sau critical audit |
| Full Observable Trace | Artifact admin chứa prompt/raw outputs/public rationale/state |
| Understanding Report | Báo cáo đọc hiểu repo có evidence và confidence |

## State Machine Cơ Bản

### Single-Agent

```text
START
  -> LLM_CALL
  -> JSON_GATE
  -> if final: FINISH_GATE
  -> if tool: TOOL_CALL
  -> TOOL_RESULT
  -> CONTEXT_UPDATE
  -> LLM_CALL
```

### Code Task Finish Gate

```text
NO_CODE_CHANGE
  -> code edit tool
  -> PENDING_VALIDATION
  -> validation fail
  -> PENDING_VALIDATION
  -> validation pass
  -> VALIDATED
  -> final success allowed
```

### Failed-Test Repair

```text
Test fails
  -> extract last_failure
  -> increment repair_attempts[signature]
  -> route Code
  -> Code patch small span
  -> route Test
  -> pass or repeat until budget/blocker
```

### Self-Eval QA

```text
Question
  -> Plan tasks
  -> Worker agent outputs
  -> Evaluate outputs
  -> Critical audit
  -> Evolution proposal decision
  -> Final synthesis
```

### Live User Directive

```text
Run active
  -> User directive received
  -> classify scope
  -> orchestrator control point
  -> apply or reject
  -> log decision
  -> continue or stop
```

### Repo Understanding

```text
Target repo
  -> scan manifest
  -> read docs
  -> extract symbols
  -> map runtime
  -> build graphs
  -> synthesize answer/report
  -> write full trace
```

## Business Rules

### JSON And Tool Rules

- Agent output must be one JSON object.
- Tool action must include server-qualified tool name where possible.
- Tool args must be object.
- Unknown tool is not recoverable by execution; agent must correct name.
- Missing args must be corrected, not retried unchanged.

### File Rules

- Existing file should be read/viewed before edit.
- File mutation should use File Editor MCP.
- Generated long file should use `file_editor_write_lines`.
- Repair mode should patch, not rewrite whole failing file.

### Validation Rules

- Code change requires validation.
- Validation can be Python, lint_test, or narrow terminal validation.
- If validation cannot run due dependency/environment, final must say blocker.
- Test Agent owns validation in role split.

### Role Rules

| Role | Can | Cannot |
|---|---|---|
| Research | gather/read evidence | edit source |
| Planner | plan/update issues/ledger | implement |
| Architect | write design docs | implement |
| Code | edit/create files | approve final |
| Test | run validation | edit source |
| Review | inspect diff/risk | mutate git/edit |
| Ledger | record audit/issues | run terminal/edit code |
| Final | synthesize user answer | mutate project |

### Software Factory Rules

- No Protocol Strategy -> no product analysis.
- No Vision -> no BRD.
- No BRD -> no PRD.
- No Story + AC -> no technical design.
- No Business Logic Model -> no technical analysis.
- No Domain Analysis + Change Hotspots -> no pattern decision.
- No Pattern Decision evidence -> no code handoff.
- No Docs Verification -> not done.

### Mini Repo Rules

- Mini repo must have a runner and docs before it is considered registered.
- Root `main.py lab ...` may forward execution but should not absorb lab internals.
- Lab artifacts must go to lab-specific output directories.
- Experiment changes become root changes only after proposal, tests and explicit implementation.

### Self-Eval And Evolution Rules

- Agent room answers questions and delegates work; it must not generate code unless the lab explicitly changes purpose.
- Critical agent reviews observable trace, not hidden model internals.
- Evolution agent can propose add/remove/change agent/flow/skills/tools.
- Default policy: evaluate a batch of 20 cases before changing prompt/flow.
- Baseline comparison must be stored with the run.

### User Agent Rules

- User directive has higher priority than normal agent preference.
- Directive scope must be explicit: current run, future run, or proposal.
- Current-run directives must not persist into future config.
- If a directive is rejected, the reason must be logged.

### Repo Understanding Rules

- Report must cite evidence for claims about runners, flow, artifacts and tests.
- Confidence/score must be explicit.
- Scanner should exclude noisy runtime/cache dirs.
- Full trace must preserve observable raw output for admin review.

## Business Logic For Product-Build Prompts

Software Factory converts ambiguous prompt into executable intent:

```text
User idea
  -> Vision
  -> Business requirements
  -> Product requirements
  -> Stories
  -> Acceptance criteria
  -> Domain objects/workflows/hotspots
  -> Business invariants/decision table/state transitions
  -> Technical boundaries
  -> Pattern decisions with evidence
  -> Implementation spec
  -> Code handoff packet
```

Điều quan trọng: pattern không được chọn ở PRD. Pattern chỉ được chọn sau khi
có hotspot evidence.

## Invariants Của Hệ Thống Agent

- Tool side effect phải trace được từ event log.
- Capability result phải giữ shape ổn định.
- Core không phụ thuộc backend implementation cụ thể.
- Role không được bypass allowlist.
- Final success cho code phải có validation evidence.
- Long analysis phải nằm trong artifact, không nhồi vào JSON tool payload.
- Dependency failure không được gọi là code logic failure.
- User directive scope không được implicit.
- Evolution proposal không được tự mutate production flow nếu chưa được duyệt.
- Full trace là observable trace, không phải hidden internal chain-of-thought.
- Mini repo experiment không được phá contract của root runner.
