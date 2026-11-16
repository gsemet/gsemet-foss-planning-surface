## Summary

chantier is still a proof of concept, so it keeps no backward compatibility. The planning folders on disk were migrated once, by a throwaway script that is not part of this PR, and the CLI no longer carries the readers that converted an older tree, backfilled old batch records, accepted the old batch status words or accepted `.agents/changes/`-prefixed record paths. The scenario cases that guarded those readers go with them. The long gate was also run on `main` first and passed, which is the baseline for the scenario work that follows.

## Deliverables

Removed from the CLI (`skills/chantier/scripts/cli/src/chantier/`) and the scenario:

| Before | After |
|---|---|
| `lifecycle/convert.py` (`old_tree`, `convert_old_tree`, `open_repo`) | deleted; every caller uses `Repo.find(...)` with the same arguments |
| `lifecycle/backfill.py` | deleted; `blank_record` no longer writes a `backfill` key |
| `BatchRecord._old_words` (`open`, `landed`) | deleted |
| `planning_path` and `archive_of` strip `.agents/changes/` | no strip |
| a record with no close date reads `(backfilled, no close date)` | reads `(no close date)` |
| scenario cases `old_words`, `old_tree`, `backfill_cases`, `release_on_stack` section 15 | deleted, with `plant_archive` which only they used |

Proof that the CLI reads the same data before and after: the same migrated copy of this project's planning folder and of the four planning-surface projects was read by `main`'s CLI at `ce00ec3` (before) and by this branch's CLI at its head (after; the head SHA is in the Evidence box below) (`status` and the board state of each project): the outputs are identical, and no run printed `converted` or `backfilled`.

## Blast radius

Grade: 2. Shared lifecycle code and the scenario change, but the removed readers were no-ops on the migrated data. Rolling back is a `git revert`; an older planning tree would then need converting again.

## Autonomous decisions

- The scenario checks `close_batch` and `opened_record` read `rec["backfill"] is None`; new records carry no `backfill` key, so they now read `"backfill" not in rec`.
- `plant_archive` is deleted with `backfill_cases`, its only caller.

## Known gaps

- Long gate waived by the user at `a6760ca`: it passed at `6081bb8`, and the later changes are the eval kit's paths and the rebase onto CR-256 (one conflict, in `delivery.py`); `just check` and `just eval-dry-run` pass at `a6760ca`.
- The long gate ran on Windows; Linux and macOS are covered by CI alone.
- `cost --batch batch-17` cannot be read from a copy of the planning folder (a closed batch has no folder), so it is not part of the before and after comparison.

<details>
<summary>Details</summary>

## Changes

- `lifecycle/convert.py` and `lifecycle/backfill.py` deleted; `open_repo` replaced by `Repo.find` in 16 modules; `intake.py` `init`, `stages.py` `_relocate`, `core/repo.py`, `core/records.py`, `core/batch_records.py` and `history.py` lose their legacy branches.
- `scenario/run_scenario.py`: the four legacy cases removed, `World.at` reads the path as written.
- Eval kit (`evals/kit/dry_run.py`, `evals/kit/setup.py`, the RUNBOOKs of `full`, `real-foreman`, `copilot`, `claude-planted`): paths given to the CLI are planning-folder-relative (`3-ready/<slug>`), as `Repo.planning_path` no longer strips `.agents/changes/`; `just eval-dry-run` passes 8 of 8 cases locally.
- `scenario/README.md`: the three lines that described those cases removed.

## Human decisions

- No backward compatibility: chantier is a proof of concept, and the folders on disk are migrated once by a script that is not kept.
- The 14 archived status files that carried an old batch id are rewritten once; the batch records keep their `backfill` data as the trace.
- The planning surface's own stage names follow the renamed folders, and its autosync commits that change.

## Impacts

No visual change. A planning folder in an older format is no longer converted; a record path written in the `.agents/changes/...` form no longer resolves.

## Test plan

- [x] No behaviour change for migrated data; the removed cases are deleted with their code
- [x] Local gates at `a6760ca`: `just check`, `just eval-dry-run` (8 of 8); `just scenario` (GitHub 877/877, GitLab 855/855) passed at `6081bb8`, carried (the user waived a new long gate)
- [x] Evidence: before at `ce00ec3`, after at `6081bb8`, carried to `a6760ca` (the move touched the eval kit and one line of `delivery.py`)
- [x] Review: approved at `a6760ca`
- [x] Verified at `a6760ca`
- [x] CI green at `a6760ca`

## Internal references

CR-253 baseline-and-legacy. Evidence in the CR folder: `evidence/long-gate-main.md`, `evidence/migration/`.

</details>
