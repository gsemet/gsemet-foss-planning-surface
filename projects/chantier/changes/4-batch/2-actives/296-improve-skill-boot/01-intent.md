# Improve skill boot

## Request

On 2026-11-16, the user reviewed the initialization of Chantier's Chief of Staff
in VS Code, using the Copilot SDK harness and GPT-6.1 Sol. They requested
improvement proposals and an interview, not implementation:

> propose des améliorations dans /Users/az02065/Projects/DevTools/chantier/.agents/changes/2-backlog/improve-skill-boot.
>
> pose moi des questions

The interview was conducted in French. The user explicitly confirmed this local
destination rather than the external planning surface. No priority was selected.

## Observed initialization

The session log for the initialization showed:

- About 87 seconds from invocation to the final response.
- 48 tool calls, including 24 file or directory reads.
- Two initial reads rejected because the references were too large, followed by
  three truncated responses during segmented reading. Missing passages were then
  retrieved.
- Chief of Staff seat acquisition after checking that the seat was free.
- A detached board server and an authenticated local API request returning HTTP
  200 after following its authentication redirect.
- A verified autosync participant for the session.
- No batch or implementation started.
- `gh auth status` reporting an invalid keyring token. This was an observed
  authentication failure, not a diagnosis of the underlying credential problem.
- Bundle validation skipping Chantier because it had no root bundle index:
  successful command completion was not validation of that project's documents.

The server reported listening on the local network, but the agent tested only
local reachability. Foreman session tools were available, but no Foreman launch
was tested. The response did not sufficiently distinguish these evidence levels.

A screenshot prompted discussion of context consumption. It is not authoritative
telemetry of remaining model capacity. An invocation near the end reported
111,454 input tokens and a declared maximum prompt size of 272,000 tokens; these
figures do not establish a remaining reasoning budget.

## Requested outcome

Improve startup for all Chantier roles and hosts through a short mandatory core,
action-specific reference loading, explicit capability evidence, and deliberate
handling of startup effects.

The final decisions are in [the proposal](03-change-spec.md). The complete
question-and-answer record, including superseded choices, is in
[the interview](02-answers.md).

## Delivery boundary

The user selected saving the complete interview and proposal in this directory.
They did not authorize implementation, a batch, a PR, or a priority assignment.
This handoff does not stop or change services already running in the session.

## Subsequent lifecycle decisions

The user subsequently selected P1 and requested realization from the external
surface in direct mode on 2026-11-16. This supersedes the persistence-only
authorization above, not the functional interview decisions. See
[the answer record](02-answers.md). No batch has been opened; autosync remains
stopped by the user's instruction.
