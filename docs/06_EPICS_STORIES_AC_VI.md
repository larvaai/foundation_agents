# Epics, Stories And Acceptance Criteria

## Epic E01 - Minimal Local Agent Runtime

### Story E01-S01: CLI Prompt Runner

As a builder, I want to run a prompt file through a CLI so that I can test the
agent loop locally.

Acceptance:

- `python main.py <prompt>` reads the file.
- Missing prompt arg uses default prompt.
- Final output is printed.

### Story E01-S02: LLM Adapter

As a builder, I want a small OpenAI-compatible adapter so that I can swap local
models without changing orchestrator logic.

Acceptance:

- Env overrides exist.
- LLM errors include base URL and model hint.
- Adapter accepts chat messages list.

## Epic E02 - JSON Protocol And Output Safety

### Story E02-S01: JSON Action Contract

As an orchestrator, I want every agent output to be a JSON action so that tool
execution is machine-checkable.

Acceptance:

- Tool action has `action`, `tool`, `args`.
- Final action has `action`, `message`.
- Invalid actions get retry prompt.

### Story E02-S02: JsonGate

As an operator, I want malformed LLM JSON to be repaired or rejected before
tools run.

Acceptance:

- Fenced JSON can be recovered.
- Trailing comma can be repaired.
- Python literal can be repaired.
- Tool args schema errors are reported with expected fields.
- Dry-run blocks unsafe paths and policies.

## Epic E03 - Kernel And Capabilities

### Story E03-S01: Capability Envelope

As a developer, I want every tool result wrapped in one envelope so that
orchestrators can reason consistently.

Acceptance:

- Result has `ok`, `capability`, `feature`, `data`, `error`, `metadata`.
- Unknown tool returns structured error.
- Disabled feature returns missing capability.

### Story E03-S02: Feature Registry

As a maintainer, I want tools registered through features so that tool backends
can be removed or replaced.

Acceptance:

- Feature descriptor includes name/version/category/capabilities/tests.
- Config can disable feature.
- Feature tests are discoverable.

## Epic E04 - Safe Tool Layer

### Story E04-S01: Workspace File Tools

As a Code Agent, I want safe file view/create/edit tools so that code changes
are auditable.

Acceptance:

- View returns line numbers.
- Create refuses overwrite unless allowed.
- str_replace checks expected replacement count.
- insert validates line range.

### Story E04-S02: Python Validation

As a Test Agent, I want to run Python files in a sandbox so that validation is
real but bounded.

Acceptance:

- Only `.py` files run.
- Path must stay in workspace.
- Timeout is clamped.
- stdout/stderr/returncode returned.

### Story E04-S03: Terminal Safe Runner

As a maintainer, I want controlled terminal probes without arbitrary shell.

Acceptance:

- Accepts `argv` list only.
- Blocks shell executables and shell tokens.
- Returns `command_metadata.summary` and `security_risk`.
- High-risk commands require env opt-in.

## Epic E05 - Validation And Finish Gate

### Story E05-S01: Code Change Tracking

As an orchestrator, I want to know when code changed so that final success can
require validation.

Acceptance:

- Code-edit tool call sets pending validation.
- Validation tool pass clears pending.
- Final success blocked while pending.

### Story E05-S02: Failed-Test Repair

As a Code Agent, I want failure summaries so that repairs are narrow.

Acceptance:

- Test failure extracts file/line/function/error where possible.
- Repair attempts counted by signature.
- Whole-file rewrite blocked in repair mode.

## Epic E06 - Role-Based Multi-Agent Runtime

### Story E06-S01: Role Allowlists

As a system owner, I want each role to have allowed tools so that responsibilities
stay separated.

Acceptance:

- Code can edit.
- Test can validate but not edit.
- Review can read git diff but not mutate.
- Ledger can write ledger/issues but not run terminal.

### Story E06-S02: LangGraph Pipeline

As an operator, I want a stateful multi-agent route so that complex tasks pass
through departments.

Acceptance:

- Pipeline starts at Research and ends at Final.
- Tool execution centralized in tool node.
- Test failure routes back to Code.
- Final requires validation for code tasks.

## Epic E07 - Product-To-Code Software Factory

### Story E07-S01: Product Spec Artifacts

As a product planner, I want Vision/BRD/PRD/Stories/AC before code so that
implementation has traceable intent.

Acceptance:

- Artifacts are written to factory run dir.
- Product validation checks required upstream artifacts.
- Long analysis is not inlined in JSON control envelopes.

### Story E07-S02: Business Logic Contract

As a Code/Test Agent, I want invariants and decision tables so that business
intent becomes executable checks.

Acceptance:

- Business logic model has invariants.
- Has decision table.
- Has state transitions.
- Has testable examples.
- Validator blocks technical analysis if missing.

### Story E07-S03: Pattern Decision With Evidence

As an architect, I want patterns chosen only from hotspots so that the design is
not overengineered.

Acceptance:

- Pattern decision lists change hotspots.
- Each pattern has problem, why now, if not used, risk, module, trace.
- Code handoff cannot happen before pattern decision.

## Epic E08 - Global Supervisor

### Story E08-S01: Intent Router

As a user, I want non-code questions not to trigger coding tools.

Acceptance:

- General knowledge routes to Knowledge.
- Current/source-backed questions route to Research.
- Code/repo/debug routes to Coding.
- Multi-file product prompts route to Software Factory.
- Mixed tasks produce execution plan.

### Story E08-S02: Safety Department

As a system owner, I want safety checks before tool-heavy routes.

Acceptance:

- Permission gate reports approvals required.
- Risk gate classifies repo/code/web.
- Prompt injection scanner can block.
- Tool scope validates department boundaries.

## Epic E09 - Observability And Testing

### Story E09-S01: Event Logs

As a debugger, I want to inspect what happened in each run.

Acceptance:

- Logs include messages, actions, observations, state/errors.
- Summary has status/metrics/final message.
- CLI can list/resolve/filter events.

### Story E09-S02: Smoke Suite

As a maintainer, I want deterministic checks before relying on LLM-heavy cases.

Acceptance:

- Kernel smoke pass.
- Feature tests pass.
- JsonGate smoke pass.
- Role permission smoke pass.
- LangGraph smoke pass.
- Company/Factory/Global Supervisor smoke pass.

## Epic E10 - Mini Repo Experiment System

### Story E10-S01: Mini Repo Registry

As a builder, I want root `main.py` to run mini repos so that experiments stay
small and isolated.

Acceptance:

- `python main.py lab list` shows registered labs.
- `python main.py lab <name> ...` runs that lab.
- Registry metadata includes name, path, docs and runner.
- Lab list does not import heavy runtime modules.

### Story E10-S02: Mini Repo Docs Tree

As a maintainer, I want each mini repo to carry its own docs so that the design
can evolve without polluting root docs.

Acceptance:

- Each mini repo has README/docs.
- Evolution proposals are stored as proposal artifacts.
- Tests and output directories are documented.

## Epic E11 - Self-Evaluating QA And Evolution

### Story E11-S01: Agent Room QA

As an operator, I want agents to delegate question-answering work to each other
so that a final answer has more than one perspective.

Acceptance:

- Planner creates tasks.
- Worker agents produce bounded outputs.
- Evaluator compares outputs.
- Final agent synthesizes a concise answer.

### Story E11-S02: Critical Agent

As a system owner, I want a critical agent to inspect the run so that loops and
weak reasoning are visible.

Acceptance:

- Critical audit sees the observable run trace.
- Audit outputs verdict, logic score and recommendation.
- Recommendations can propose add/remove/change agent/flow/skills/tools.
- No source mutation happens without a separate deployment command.

### Story E11-S03: Baseline Comparison

As an evaluator, I want to compare the agent answer with a ChatGPT/local
baseline so that improvements are evidence-based.

Acceptance:

- Baseline answer is stored.
- Comparison has winner or tie.
- Batch evaluation waits for enough cases, default 20, before changing prompts.

## Epic E12 - Live User Control And Dashboard

### Story E12-S01: User Agent Directive

As a user, I want to intervene while a run is active so that my latest
instruction can override the current agent plan.

Acceptance:

- Directive is captured while run is active.
- Directive has scope: this run, future run, or proposal.
- Applied/rejected status is logged.
- Temporary directives do not persist.

### Story E12-S02: Process Dashboard

As an operator, I want a UI for process state, logs and artifacts so that I can
debug without opening every JSONL file manually.

Acceptance:

- UI lists runs and run details.
- UI shows agents, state, timeline, warnings and artifacts.
- UI can submit directive text to User Agent.
- UI handles incomplete run dirs.

## Epic E13 - Repo Understanding Lab

### Story E13-S01: Repository Scan And Report

As a builder, I want a lab to read another repo so that I can judge whether the
agent understands project structure.

Acceptance:

- Scanner produces manifest.
- Docs reader maps README/docs.
- Symbol/runtime analyzers find entrypoints and output dirs.
- Report cites evidence and confidence.

### Story E13-S02: Business Prompt Lab Understanding

As a maintainer, I want the lab to understand `business_prompt_lab` so that the
mini repo system is self-auditable.

Acceptance:

- Report identifies lab runners.
- Report identifies agent-room flow.
- Report identifies output artifacts.
- Report maps related tests.
- Score is at least 4.0/5 for the current smoke prompt.
