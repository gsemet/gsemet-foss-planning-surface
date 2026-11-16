CR-113. An audit of batch `cr-board`'s costs found chantier's arithmetic right, and this adds what it left out.

## The Chief of Staff's session

- `open` records `chief_transcript` from `$CLAUDE_CODE_SESSION_ID` or `$COPILOT_AGENT_SESSION_ID`.
- `cost` prints a `Chief of Staff:` line: since the batch's `open`, the whole session, and the last context size; `not measured` with no session id.
- That line never enters `spent_usd`, and the budget rail never reads it.

## The split

- `cost --by driver`: one line per Driver type, its workers included through `parentAgentId`; an unknown type gets its own line. `STATUS.md`'s Cost section gives these lines.
- `chief-of-staff.md`, "Cost": four lines per report from `cost --by role`.
- `chief-of-staff.md`, compacting: the auto-compact advice once per session, `/compact` above 100k at a change of subject.

## The audit's fixes

- A `<synthetic>` or token-less record is skipped, so `status --refresh` no longer stops.
- A batch keeps and sums every Foreman transcript across a relay (`foreman_transcripts`; an old batch falls back to `foreman_transcript`).
- A landed batch stops at its landing, so a reused Foreman does not count in the earlier batch.
- `since` compares times, not strings.
- `usage` counts only wakes inside the window.
- `evals/kit/audit.py` audits every Foreman of a relayed batch in one pass.

## To read closely

- **Auto-compact wording:** the specification says "turn on", but the host's documentation (code.claude.com/docs/en/model-config) gives no on/off switch: compacting is on by default and the window is what is set. The card says that, and names `/autocompact` and `autoCompactWindow`. It names no setting on Copilot, whose documentation was not fetched.
- **Copilot:** `cost` prints `Chief of Staff: not measured` even with a recorded id: `copilot_session_costs` has no timestamps or context size, and the specification prices the session with `session_costs`.

Compaction calls stay uncounted (about $0.12 each) and `STATUS.md` says so. Fast mode and `inference_geo` stay unpriced.

## Checks

`just check` and `just scenario` pass; the scenario covers a `<synthetic>` record, a relay's sum, a reused Foreman, the Chief of Staff's figures kept out of `spent_usd`, and `--by driver` with an unknown Driver type.
