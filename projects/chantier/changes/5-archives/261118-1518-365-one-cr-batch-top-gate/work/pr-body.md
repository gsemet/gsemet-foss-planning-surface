## Summary

A project rule can ask the top of a stack to also pass the long gate locally before a merge. In a batch with no stack (parallel, series, a single change) no card said which change is "the top", so the ready ask reached the user without that run, and the change was sent back for the gate afterwards. This PR defines the batch's top for a batch with no stack and wires the local run, the ask and the user's message to it.

## Deliverables

The batch's top, and who does what:

| Moment | Who | What |
| --- | --- | --- |
| Before the ready hand-back of the top | Driver | reads a plain `status`, runs the local gate at the pushed head, hands back with no `--no-gate` |
| Each ready hand-back; each merge, drop or cancel that leaves one open change or only ready ones | Foreman | sends the top back with `take <cr> --note "long gate: the batch's top runs <command> locally"` when no gate passed at its head (inside the rebase `take` after a merge) |
| The top's ready ask | Foreman, Chief of Staff | `ready-to-merge <cr> <link>[ gaps: …] local gate <cr> at <sha7>: passed|failed|not run`, sent only with `passed` (a `deliver by` time excepted); the user is told what it says |

- The top is the last open change other than a release change (a fix change counts; a one-change batch's change from the start), or, when the last open ones are all ready together, the last of them in `status`'s order.
- A waiver does not waive the local run unless its words name that gate.

## Blast radius

Grade: **1**. Three instruction files change, with no code; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The new Foreman text sits as an extra paragraph after the existing stack-top check, with the stack wording left untouched, so the two rules stay independent.

## Known gaps

- The Copilot host's path is unproved (the Foreman's top check, as for the stack's top today); no Copilot batch has run it.
- The behaviour is unproved until a real batch with no stack ends under the rule; trial: the top's Driver runs `gate` before its hand-back (a `gate` event at its head before the `handback ready` event), and its ask carries `local gate <cr> at <sha7>: passed`; and one batch where the top changes after a merge: the gate `take` comes before any ask of that change's new head.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/driver.md`: the long-gate bullet defines the batch's top and the Driver's check before its ready hand-back; the hand-back bullet keeps the local run for a waived top.
- `skills/chantier/references/foreman.md`: the boundaries check at two moments, the waiver check, the asks list, the `order merged` rebase `take`, and "Deliver by a time".
- `skills/chantier/references/chief-of-staff.md`: the clause in the ready message, merges recorded with the top last, the gates forecast counting the top once.

## Human decisions

- Series batches follow the same definition; a release change is never the top; a fix change counts.
- A follow-up waiver does not waive the local run unless its text names that gate.
- When the last open changes are all ready together, the last in the batch's order is the top, and the others are offered as mergeable only together with it or before it.

## Impacts

No visual change. Maintainers: a project with such a rule gets its local gate on the batch's last change before the user is asked to merge.

## Test plan

- [x] No behaviour change in code (cards only)
- [x] Local gates at `c586ff0`: `just check` pass
- [x] Evidence: none (cards only)
- [x] Review: approved at `c586ff0`
- [x] Verified at `c586ff0`
- [x] CI green at `c586ff0`: all 5 jobs pass, `just scenario (ubuntu-latest)` included

## Internal references

- CR-365 one-cr-batch-top-gate; follows CR-359 partial-stack-ask-windows-gate.

</details>
