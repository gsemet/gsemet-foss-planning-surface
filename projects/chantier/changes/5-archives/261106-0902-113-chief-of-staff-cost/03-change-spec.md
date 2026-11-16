# The Chief of Staff's session is priced, and each report splits the cost

A subagent recomputed the costs of batch `cr-board` from the raw transcripts on 2026-11-06:
chantier's arithmetic and its prices are right, to the cent. This CR adds what it leaves out and
fixes what the audit found.

## The Chief of Staff's session

`open` records the Chief of Staff's session in `batch.json`, as `chief_transcript`, from
`$CLAUDE_CODE_SESSION_ID` or `$COPILOT_AGENT_SESSION_ID`. `chantier cost` prices it with
`session_costs`, so its subagents count, and gives two figures: since the batch's `open`, and the
whole session. An empty variable leaves the line `Chief of Staff: not measured`, never a guess.

It stays apart: it never enters `spent_usd`, and the budget rail never reads it. The line also
gives the session's last context size. `STATUS.md` drops "Not counted: the Chief of Staff's own
session".

## The split

- `chantier cost --by driver` gives one line per Driver type, as named by the agent's type: its own
  calls plus those of the workers it started (`parentAgentId`). A Driver the user brings gets its
  own line with no change. `STATUS.md`'s Cost section gives these lines at the end of a batch.
- The CLI knows no role, so the rest is in `chief-of-staff.md`, "Cost". Each report, on a CR ready
  or merged, on "status?" and at landing, gives four lines from `cost --by role`: orchestration,
  the Foreman; review, the Inspector, the Verifier and a QA driver; implementation, all the rest,
  an unknown agent included; and the Chief of Staff's two figures.

## Advice on compacting

In `chief-of-staff.md`:

- Once per session, advise the user to turn on the host's auto-compact. Name the setting only as
  the host's documentation gives it; prove that first.
- When the talk moves to another subject and the context is above 100k, advise `/compact`, with a
  line ready to copy that says what to keep: the running batch, the open CRs, the decisions not
  yet written. Never in the middle of a subject.

## What the audit found

In `costs.py` and `commands.py`:

- A record of model `<synthetic>` (an API error, a session limit) has an all-zero usage and raises
  in `_family`: `status --refresh` then stops updating `spent_usd`, and the budget rail reads a
  stale figure. A record without tokens is skipped.
- `foreman` relay clears `foreman_transcript`, and the next `spent_usd` holds the new session
  alone. A batch keeps every Foreman transcript and sums them.
- `since` has no upper bound: a Foreman reused for a later batch would count in the earlier one.
  A landed batch stops at its landing.
- `since` compares strings, so a call in the opening second can be dropped. Compare times.
- `usage` latches a wake from before the window: count only wakes inside it.

Compaction calls leave no record, about $0.12 each. They stay out, and `STATUS.md` says so. Fast
mode and `inference_geo` are not priced: none occurred, and this CR leaves them out.

## Done when

- `just check` and `just scenario` pass; the scenario covers a `<synthetic>` record, a relay's sum,
  a reused Foreman, the Chief of Staff's two figures kept out of `spent_usd`, and `--by driver`
  with an unknown Driver type.
