Stacked on #210.

## Summary

Every retro found something to change, and the user had to sort the list. Now every list of changes that the Foreman or the Chief of Staff proposes on its own (a batch's or a release's retro, a report's suggestions, an answer such as "are the workers useful?") first goes through a new `retro-critic` role: a separate read-only subagent on the strongest model of the host. It reads the points and the evidence they cite, never the author's case, and answers keep, merge or drop per point, with one line why. Only kept points are written and offered; the user hears in one line how many were dropped. "Nothing worth changing" is a valid outcome.

## Deliverables

The critic's contract and where each parent uses it:

| Piece | What it does |
| --- | --- |
| `skills/chantier/references/retro-critic.md` (new card) | input bound, three tests (measured, changes an outcome, not already covered), verdict format `<n>. keep/merge/drop: <why>` and the `kept <k>, dropped <d>` line |
| `agents/retro-critic.md`, `com.github.copilot/agents/chantier-retro-critic.agent.md` (new) | one agent per host, Opus 5.5, identical bodies |
| `foreman.md` | runs the critic before writing `4-batch/retro.md`; the section holds kept points, header ends `(critic: kept k, dropped d)`; dropped points go to `4-batch/retro-dropped.md`, deleted at close |
| `chief-of-staff.md` | offers kept points and one line `<d> points dropped by the critic; the list is on request.`; same run in direct mode and for any unasked list or single suggestion |
| `playbook --batch` | prints the retro critic's first line for the Foreman |

Choices made: no cap in dollars (the critic is bounded by what it reads); a failing critic (twice) means nothing is offered that pause and the drafted points stay on request; a release Driver's retro points ride in the pause's single critic run.

## Blast radius

Grade: 1. Cards, two new agent files, one small CLI helper and tests; a `git revert` restores the previous retro flow.

## Autonomous decisions

- `playbook --batch` prints only the retro critic's line among the Chief of Staff's subagent lines (the specification left the others to the Driver's choice), selected by the agent file's "Started by" text so the CLI still knows no role.
- Kept release points are marked `(release)` in the Foreman's retro section.

## Known gaps

- The Foreman starting the retro critic and its model in a real transcript is unproved; the host reference row is marked unproved until the first pause after the merge.
- Fable through the `model` parameter is unproved.
- Area 7 deviation: the playbook line and the cost case live in pytest (`test_playbook_config.py`, `test_cost_reading.py`), not in the scenario, since CR-254 moved those cases; only the `close` case stays in the scenario.

<details>
<summary>Details</summary>

## Changes

- New card, two agent files; `plugin_files.chief_prompt_lines` takes an optional "started by" filter, used by `playbook --batch`.
- `foreman.md`, `chief-of-staff.md`, `concepts.md` (first-line row, subagent paragraph, restart rule), `status-layout.md` (Retro bullet), both host references, `CONTRIBUTING.md`.
- `test_plugin_files.py`: the role joins the chief, Claude Opus and Copilot Opus sets. `test_playbook_config.py` (playbook line, `--batch` prints only the retro critic's), `test_cost_reading.py` (cost case on the Foreman's own subagents), `scenario/run_scenario.py`: `close` deleting `retro-dropped.md`.

## Human decisions

- The Foreman runs the critic before writing the retro, so the batch's record holds only kept points; the Chief of Staff does the same in direct mode.
- No dollar cap on a critic run; its cost counts in the batch.
- Every unasked list of changes goes through the critic; a change the user asked for does not.

## Impacts

No visual change. Retros shrink to what matters; the user gets one dropped-count line.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates: `just scenario` passed at `9fd6d54` (carried over a clean rebase onto CR-264, CI green); `just check` passes at `eb14e28`
- [x] Evidence: none (cards and CLI helper, no visible change)
- [x] Review: approved at `9fd6d54`, carried from `9fd6d54` over the clean rebase (rounds approved before the rebase onto CR-254; the move to pytest re-reviewed)
- [x] Verified at `eb14e28`
- [x] CI green at `eb14e28`

## Internal references

- CR-259 retro-critic
- Round notes: `work/r1.md` in the CR's folder

</details>



