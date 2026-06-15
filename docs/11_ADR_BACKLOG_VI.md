# ADR Backlog

## ADR-001 - Use JSON-Only Agent Protocol

Status: accepted.

Decision:

- Agent must return one JSON object for tool or final.

Reason:

- Orchestrator needs machine-checkable actions.
- Tool calls cannot depend on prose parsing.

Consequence:

- Need JsonGate and retry flow.

## ADR-002 - Use Agent Kernel And CapabilityResult Envelope

Status: accepted.

Decision:

- All tool calls go through `core.capabilities.call_tool()`.
- Results wrapped as `CapabilityResult`.

Reason:

- Decouple core orchestration from tool backend.
- Allow removable features.

Consequence:

- Adapters must normalize raw tool results.

## ADR-003 - MCP Tools As Removable Feature

Status: accepted.

Decision:

- MCP integration lives in `features/mcp_tools/`.
- Kernel knows only ToolPort/registry.

Reason:

- Avoid core depending on MCP implementation.

Consequence:

- Feature config and feature tests become required.

## ADR-004 - File Editor Is Primary Edit Path

Status: accepted.

Decision:

- Agent should edit via `file_editor.*`, not terminal.

Reason:

- Edits become auditable and scoped.
- `str_replace` can guard broad replacements.

Consequence:

- Generated long files need `write_lines` to avoid JSON string fragility.

## ADR-005 - Terminal Is Argv-Only

Status: accepted.

Decision:

- Terminal MCP accepts `argv` list, no shell string.

Reason:

- Shell is too broad and hard to audit.

Consequence:

- Some commands need dedicated MCP tools instead of shell hacks.

## ADR-006 - Finish Gate For Code Changes

Status: accepted.

Decision:

- Code change sets pending validation.
- Final success blocked until validation passes or blocker reported.

Reason:

- Prevent false "done".

Consequence:

- Orchestrator must detect code-change and validation tools.

## ADR-007 - Role Ownership

Status: accepted.

Decision:

- Code edits.
- Test validates.
- Review approves/requests changes.
- Ledger records.
- Final communicates.

Reason:

- Reduces self-approval and responsibility mixing.

Consequence:

- Role allowlists and route contracts required.

## ADR-008 - Artifact-First Software Factory

Status: accepted.

Decision:

- Long BRD/PRD/domain/logic/docs analysis goes into artifacts.
- JSON carries route and artifact refs only.

Reason:

- Long JSON payloads are fragile and hard to audit.

Consequence:

- Artifacts need path/hash/summary.
- Handoff packet points to artifacts.

## ADR-009 - Pattern Decisions Require Hotspot Evidence

Status: accepted.

Decision:

- Pattern Decision Agent cannot select pattern before Domain Analysis and
  Business Logic Validation.

Reason:

- Avoid overengineering from product prose.

Consequence:

- Implementation Spec depends on Pattern Decision.

## ADR-010 - Global Supervisor Routes Non-Code Tasks Away From Coding

Status: accepted.

Decision:

- IntentRouter classifies knowledge/research/code/product/mixed tasks.

Reason:

- Not every user request should enter repo/code tooling.

Consequence:

- Final Synthesis must merge department outputs.

## ADR-011 - Keep Experiments In Mini Repos

Status: accepted.

Decision:

- New agent workflows that are not yet root runtime should live under
  `business_prompt_lab/<mini_repo>/`.
- Root `main.py lab ...` can discover and run them through a registry.

Reason:

- The project needs to try many mini repos quickly without destabilizing the
  main orchestrator.

Consequence:

- Each mini repo needs its own docs, tests and artifacts.
- Registry metadata becomes part of the rebuild contract.

## ADR-012 - Full Trace Means Full Observable Trace

Status: accepted.

Decision:

- Admin trace artifacts store prompts, raw model outputs, public rationale,
  state, handoffs, warnings and artifact references without UI truncation.
- The system does not claim access to hidden internal chain-of-thought unless a
  model explicitly emits that text as normal output.

Reason:

- Debugging needs complete observable evidence, but docs must not promise data
  the runtime cannot access.

Consequence:

- UI can summarize, but must link to raw/admin trace.
- Tests should assert trace artifact existence and key events.

## ADR-013 - User Agent Directives Are Scoped

Status: accepted.

Decision:

- Live user instructions go through `User Agent`.
- Every directive has scope: current run, future run, or proposal.

Reason:

- Users need to intervene while agents run, but temporary changes must not
  silently become permanent configuration.

Consequence:

- Orchestrators need control points between steps.
- Applied/rejected directive decisions must be logged.

## ADR-014 - Process Dashboard Is Observability/Control Surface

Status: accepted.

Decision:

- Build a local process dashboard for run state, logs, artifacts and directive
  input.
- Keep CLI as the primary automation surface.

Reason:

- Long multi-agent runs are hard to debug from JSONL alone.

Consequence:

- Dashboard must tolerate incomplete run dirs.
- Dashboard should not mutate source files directly.

## ADR-015 - Evolution Agent Produces Proposals Before Mutations

Status: accepted.

Decision:

- Critical/evolution agents may propose add/remove/change of agents, flow,
  outputs, skills and tools.
- They do not mutate production source/config without an explicit deployment
  task.

Reason:

- Self-modifying agent flows can thrash if driven by one bad run.

Consequence:

- Evolution proposals live in docs/artifacts.
- Default evaluation cadence is batch-based, currently 20 cases per review.

## ADR-016 - Repo Understanding Lab Uses Evidence And Confidence

Status: accepted.

Decision:

- Repo understanding must produce manifest/docs/symbol/runtime/graph evidence
  and an explicit score/confidence.

Reason:

- A repo reader that only summarizes grep hits can overclaim understanding.

Consequence:

- Reports must cite evidence for runners, flows, artifacts and tests.
- Smoke tests should include `business_prompt_lab` as a target repo.

## ADR Candidates For Future

### ADR-F01 - Persistent MCP Process Pool

Problem:

- Current stdio-per-call is simple but slow.

Decision to make:

- Keep per-call for correctness or add session pool.

### ADR-F02 - Production Dashboard Auth/Permissions

Problem:

- Local dashboard exists, but production use needs auth, permissions and safe
  deployment posture.

Decision to make:

- Keep dashboard local-only or add authenticated multi-user deployment.

### ADR-F03 - RAG Source Line Ranges

Problem:

- Current RAG hits have source/chunk but not line ranges.

Decision to make:

- Add line range metadata at ingest.

### ADR-F04 - Agent Factory Real Implementation

Problem:

- Global Supervisor can route agent creation, but Agent Factory is placeholder.

Decision to make:

- Define plugin/skill/agent scaffolding contract.
