## Summary

When the host stops background Driver agents (as Claude Code did at a manual compaction of the steering session in a recent session), the steering session tried to resume them with a message, the host refused ("Agent <id> was stopped and won't be resumed… only launch a new agent if the user explicitly asks"), and the batch then waited for the user. This PR makes the batch's go cover that case: a Driver stopped from outside is restarted as a fresh Driver at once, counts toward nothing, and `status` now flags a Driver that is recorded but stopped.

## Deliverables

Batch evidence the new rules rest on (steering session `91f1382a-eacd-437e-b5a8-f9e545753a8c`, 2026-11-16): at `20:33:02Z`, with the `compact_boundary` record (trigger `manual`), one record per Driver such as
`{"type":"attachment","attachment":{"type":"task_status","taskId":"a0106566b6aa3f0cb","taskType":"local_agent","description":"Driver CR-299","status":"killed",...,"canContinueAgent":true}}`
(also `a103955deaf241307` and `a164f7a02355addd0`); at `20:49:19Z` to `20:49:22Z` each `SendMessage` to them got `{"success":false,"message":"Agent <id> was stopped and won't be resumed. Treat its work as cancelled; only launch a new agent if the user explicitly asks."}`.

New `status` flag, shown on a CR's row, and on the `activity stack` / `activity <O-k> qa` lines of `status --refresh`:

| Before | After |
| --- | --- |
| a stopped Driver looks like a working one | `Driver <id> stopped from outside, no hand-back recorded` |

Choices: the stop is detected only by the compaction snapshot's `killed` record and the host's refusal of a message; the steering session's own stops are kept apart by clearing the recorded agent id; such a stop counts neither toward `driver ended twice` nor toward "blocked twice" and is restarted at each stop.

Reader cost: a new `agents_stopped` reader scans the steering transcript backward, bounded by the agents' start time. On a padded 291 MB, 85,000-line copy of a transcript: 0.005 s with the `killed` record last, 0.007 s with the Driver started after the last `task_status` record (reader alone).

## Blast radius

Grade: **1**. A text flag in `status`, new card rules and a new reader; a `git revert` restores the previous behaviour.

## Autonomous decisions

- The reader lives in a new module `costs/stopped.py` rather than `costs/sessions.py`, which already exceeds the size limit the tests enforce.
- The cards say "a message" and "the host's means" where the specification names `SendMessage` and `TaskStop`, because a test forbids host tool names in cards; the host reference keeps both names.

## Known gaps

- What a stop made by the user in the app leaves in the steering transcript is unproved; trial: in a session with a background subagent, the user stops it in the app, and records whether and when a `task_status` `killed` record or another record appears, before and after a compaction.
- Timing was measured on the reader alone, not on a whole `status` / `status --refresh` before and after the change.
- The Copilot host's outside stop is unproved.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/foreman.md`: proof of death becomes one of three; new "A Driver stopped from outside" rule (restart on the go, counts as nothing, said in the report); refused hand-back message and "silent end" adjusted; `status` flag listed.
- `skills/chantier/references/concepts.md`, `hosts/claude-code.md`, `hosts/copilot.md`, `chief-of-staff.md`: matching rows and sentences.
- `skills/chantier/scripts/cli/src/chantier/costs/stopped.py` (new), `commands/activity.py`, `commands/batch_status.py`: the reader and the flag.
- `scenario/run_scenario.py`: checks for the flag, the last record deciding, another agent, the start bound, no event written, cleared id and restart accepted, a second stop restarted.

## Human decisions

- The batch's go already covers restarting a Driver stopped from outside; no question to the user, and the restart is said in the report.
- Such a stop counts toward neither "driver ended twice" nor "blocked twice", and is restarted at each stop.
- Only stops the steering session did not make itself are covered; the user's stop in the app counts as from outside.
- Detected: the compaction snapshot's `killed` record and the host's refusal of a message; nothing else.

## Impacts

`status` text gains one flag; no `STATUS.json`, pane or board change.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario `driver_liveness` checks
- [x] Local gates at `e0e60c8` (carried over the restack): `just check` pass (382 tests); `just scenario --unit qa-driver` 68/68 (restacked; conflict resolved, inspector approved at `e0e60c8`)
- [x] Evidence: reader timing on a padded transcript, see Deliverables
- [x] Review: approved at `8f2b9cf`, committed as `e0e60c8`, carried from `e0e60c8` over a clean rebase to `e0e60c8` (restacked; conflict resolved, inspector approved at `e0e60c8`)
- [x] Verified at `e0e60c8` (restacked; conflict resolved, inspector approved at `e0e60c8`)
- [ ] CI green at `e0e60c8`: just check x3, eval-dry-run and just scenario (ubuntu-latest) pass (restacked; conflict resolved, inspector approved at `e0e60c8`)

## Internal references

- CR-318 (driver-resume-after-stop), batch-23.
</details>
