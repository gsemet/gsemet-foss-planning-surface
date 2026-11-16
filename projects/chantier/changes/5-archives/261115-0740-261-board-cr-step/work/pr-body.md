Stacked on #212.

## Summary

A working change request showed only its round ("r3/6"), so a reader could not tell whether it was in review, in its gate, in CI or rebasing. Each working CR now shows the step it is at ("coder r3", "inspector r3", "gate scenario", "CI", "rebase", "verifier"...), and a blocked CR shows "waits for the user". The web board also marks the next CR to start.

## Deliverables

A new `chantier phase <cr> <phase> [detail]` command records the step; every surface copies one text drawn by `phase_text`.

| Surface | What is added |
| --- | --- |
| `STATUS.json`, `STATUS.md` | `phase` on the CR view and on batch and dashboard rows; a `Step` column; a `**Step:**` line |
| `chantier status` | `\| step: <text>` after the state, round and PR |
| Web board (Batch view, Kanban) | the step on each working CR; a "next to start" tag; Slots line "N queued · next: CR-n" |
| CR board pane | a `Step` column and a `Step:` line on the CR sheet |

Choices: the new field is named `phase` so it does not clash with the existing `step` field; `round` records `coder`, `take` and `handback` clear it; the "next to start" reading is by order, from the record only, and shown on the board alone.

**UNVERIFIED:** the pane and board screenshots (not yet captured, see Known gaps).

## Blast radius

Grade: 2. The record, the status files, the board and the pane all gain a field; older `STATUS.json` files without `phase` draw `-`. Revert restores the previous behaviour.

## Autonomous decisions

- The schema stays at 3: the fields are added and none changes meaning.
- The CLI refuses the `phase` command on a CR that is not working, and `review` with no detail.

## Known gaps

- No screenshot of the pane from a real session.
- No screenshots of the web board's Batch view and Kanban showing the step and the "next to start" tag, and the documentation screenshots are not retaken.

<details>
<summary>Details</summary>

## Changes

- Record: `core/records.py` (`phase`, `phase_detail`, `phase_at`), `core/phases.py`; `status/words.py` (`phase_text`, `next_to_start`).
- Command: `declare/driver.py`, `commands/driver.py`; side effects in `round`, `take` and `handback`.
- Status: `status/views.py`, `status/markdown.py`, `commands/batch_status.py`.
- Board: `board/crs.py`, the Batch view, Kanban, i18n files and CSS.
- Pane: `hooks/register.tsx`, `types/index.d.ts`, `hooks/register.test.tsx`.
- Cards and docs: `skills/chantier/references/driver.md`, `concepts.md`, `docs/web-board.md`, `docs/boards.md`, the demo batch.
- Tests: unit tests for `phase_text` and `next_to_start`, a pytest case for the `phase` refusals (`tests/test_rail_refusals.py`); scenario checks in `scenario/run_scenario.py`, listed in `scenario/README.md`.

## Human decisions

- The Driver records the step at each step through a small CLI command; the surfaces read it.
- The step shows on the board, `chantier status`, the status files and the pane.
- The board also shows the next CR to start.

## Impacts

Working CRs show their step everywhere; no other visible change.

## Test plan

- [x] New or changed tests: unit tests for `phase_text` and `next_to_start`, the `phase` refusals test, pane test, scenario checks
- [x] Local gates at `6c75aaa`: `just check` (pass), `just scenario` (pass, Windows); `just mod` passed earlier (`hooks/` and `types/` untouched since)
- [ ] Evidence: no screenshot of the pane from a real session and no web board screenshots (Known gaps)
- [x] Review: approved at `6c75aaa`
- [x] Verified at `6c75aaa`
- [x] CI green at `6c75aaa`: `gh pr checks 208`, 5 checks pass

## Internal references

- CR-261 board-cr-step; `.agents/changes/4-batch/2-actives/261-board-cr-step/`

</details>
