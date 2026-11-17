## Summary

`close` used to read every subagent transcript of the steering session and refuse on each one that read as running, including grill, spec and critic subagents and agents chantier had already replaced. A batch could not close until the user declared a dozen stopped agents by hand. Now only the agents the batch holds can block `close`: each agent id recorded with `agents set` and not cleared, and the current Foreman. The session's other subagents and the replaced Foremans are listed apart, as information, and need no word from the user.

## Deliverables

What blocks `close` before and after:

| Transcript | Before | After |
| --- | --- | --- |
| Agent recorded by `agents set` (CR or QA order), reads as running | refuses | refuses (`--stopped` hint) |
| Recorded agent with no transcript found | not judged | refuses as `cannot be read`, naming `agents set <cr> - --epoch <n>` |
| Current Foreman's main transcript, reads as running | refuses | refuses |
| Replaced Foreman's main transcript, running | refuses | listed apart |
| Any other subagent (grill, spec, critics, replaced Drivers, a Driver's own subagents), running or unreadable | refuses | listed apart under a heading saying they are not judged and that their calls are counted only up to now |
| Recorded stack agent | refuses | refuses (always, `--stopped` never passes it) |

`close --stopped NAME` now accepts only a held agent that reads as running (or the current Foreman's session id); any other name is refused with `not an agent <batch> holds; it does not block close, drop the flag`.

The scenario's close steps cover each row (running, cleared, never recorded, QA order, two Foremans, a Driver's child, missing transcript, `--stopped` variants, record causes).

## Blast radius

Grade: 2. `close` is the batch's final step and prices from transcripts, so a wrong split could let a batch close with an agent still running; the split is covered by the scenario and revert is a plain `git revert`.

## Autonomous decisions

- The transcript reading moved into a new module, `costs/endings.py`, beside `costs/sessions.py`, to keep the split readable; the reader of one transcript is unchanged.
- The scenario's stack, release, series, direct and surface-board units clear their recorded agent ids before `close`, since a recorded id with no transcript now refuses.

## Known gaps

- A cut-JSON subagent that was never recorded is not proven as "listed apart": the final-cost pricing refuses any cut line of any session transcript and the specification leaves pricing unchanged, so the scenario proves the unreadable-listed case with a subagent that has no user or assistant record, and the cut-JSON case for held agents.
- Local scenario run on Windows only so far; the Linux job runs in CI.

<details>
<summary>Details</summary>

## Changes

- `rails.py`: `running`, `check_idle` and `_declared` judge only held agents and the current Foreman; a held id with no transcript is `cannot be read`.
- `costs/sessions.py`, `costs/endings.py`: the held agents' endings and the other transcripts' endings, read once.
- `commands/closing.py`: lists the other running or unreadable transcripts under one heading at a passing `close`; nothing about them is recorded.
- `declare/closing.py`: `close` and `--stopped` help.
- Cards `concepts.md` and `chief-of-staff.md` (Closing, Recovery): the new rule, and `close` offered only after the retro critic has handed back.
- Docs and `scenario/README.md`, `scenario/run_scenario.py`.

## Human decisions

- Only agents the batch recorded and still holds block `close`; the session's other subagents are listed apart with no word needed.
- The current Foreman's main transcript still blocks; earlier Foremans' are listed apart.
- A held agent with no transcript is refused as unreadable, with the way out named.
- Only other subagents still running or unreadable are listed; ended ones are not.
- At a passing `close`, the heading says their calls are counted only up to now in the final cost.

## Impacts

No visual change. Closing a batch no longer needs the user's `--stopped` for agents chantier replaced.

## Test plan

- [ ] New or changed tests: scenario `close_refusals` and `close_batch` steps cover the new split
- [x] Local gates: `just check` pass and `just scenario` pass (Windows), carried from `a17f0fc` (clean rebase, same patch)
- [x] Evidence: none (no visible change)
- [x] Review: approved, carried from `2d2de57`
- [x] Verified at `6548570`, carried from `a17f0fc` (`just scenario`: pass; evidence items proved) (restacked; patch carried)
- [x] CI green at `6548570`: all five jobs pass, `just scenario (ubuntu-latest)` included (restacked; patch carried)

## Internal references

- CR-316 close-batch-agents-only.

</details>
