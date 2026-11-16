## Summary

When a batch is closed, `chantier close --yes` used to delete the batch's retro (the list of problems met, each with its long-term fix), so the only record of a batch's lessons disappeared. Now `close` keeps it: the retro moves, whole, into the archive of the batch's last merged change request, and is never deleted.

## Deliverables

Where the retro goes at `close --yes`:

| Situation | Result |
| --- | --- |
| Batch archives at least one change | `retro.md` moves to the top of the archive folder that sorts last (the latest merge) |
| Batch archives none (all cancelled) | new folder `5-archives/<YYMMDD-HHMM>-<batch id>/` holding only `retro.md` |
| No retro, or an empty or whitespace-only one | nothing created; an empty file goes with the batch's files as before |

`close` prints one `retro:` line in both forms (`retro: 4-batch/retro.md moves to 5-archives/<archive>/retro.md`, then `retro: kept in ...`, or `retro: no retro`). The move is a rename, part of `close`'s all-or-nothing: a target that already exists refuses the whole close and everything is put back. The board does not list or count a retro-only folder. The cards (`concepts.md`, `status-layout.md`, `chief-of-staff.md`) and the README no longer say `close` deletes the retro.

## Blast radius

Grade: 1. Local to `close` and the board's archive listing; a `git revert` restores the previous behaviour (the retro is deleted again at close).

## Autonomous decisions

- The "next CR number" scenario check for an all-cancelled batch is made on the next `open` rather than `file`, because in this repository `file` gives inbox items no number.

<details>
<summary>Details</summary>

## Changes

- `commands.py`: `_retro_target()` picks the destination; `close()` prints the `retro:` line and leaves a kept retro out of the deleted list; `_archive_and_delete()` renames the retro after the CR moves, records it for rollback, refuses without overwriting.
- `status.py`: `_past()` skips a `<stamp>-batch-<n>` folder on the archives stage.
- Cards, README, `docs/cr-lifecycle-texts.md`, `scenario/README.md` updated.
- `scenario/run_scenario.py`: retro checks in `close_batch`, a new `retro_cases()` (all cancelled, no retro, whitespace-only), and an external-mode check.

## Human decisions

- Retros are kept in the last change request of the batch, not deleted.
- A batch with no merged change request keeps its retro in a folder named for the batch.
- A retro collision is an error, never an overwrite.
- A change's archive in its pull request never carries the batch's retro.

## Impacts

Users who close a batch find the retro in the newest archive folder. No visual change.

## Test plan

- [x] New or changed tests (they fail on the previous code): scenario checks listed above
- [x] Local gates at `e8d079d`: `just check`, `just scenario` passed
- [x] Evidence: no visual change; checks are in the scenario
- [x] Review: approved at `24cc7eb` (diff), committed as `9f77e7e`, rebased to `e8d079d`
- [x] Verified at `e8d079d`
- [x] CI green at `e8d079d`

## Internal references

- CR-179 retro-kept-at-close

</details>

