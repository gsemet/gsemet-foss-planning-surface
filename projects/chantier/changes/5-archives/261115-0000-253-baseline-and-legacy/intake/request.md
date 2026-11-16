# A green long gate on main, and no backward compatibility

Filed 2026-11-14 by the Chief of Staff, on the user's word (Scen-Q5, the Fable plan taken
whole): the first of three CRs; then `fast-scenario`, then `gate-rules`. Its grill is in
`1-inbox/fast-scenario/02-answers.md` (Scen-Q1, Scen-Q5, Scen-Q6) and its analysis in
`1-inbox/fast-scenario/analysis/`.

## What it does

1. Run the long gate (`just check`, `just scenario`, GitHub and GitLab) on main on the user's
   Windows machine and fix what fails, one commit per cause. From about 12:50 on 2026-11-14,
   batch-17's PRs were merged without it (GitHub CI green accepted in its place).
2. No backward compatibility (the user: "pas besoin de backward compatibilité on est encore en
   PoC"). In order:
   - a one-off migration script, run once and never kept in the CLI, on this project's
     `.agents/changes/` and on the planning surface `gsemet-foss-planning-surface`:
     - rewrite the 14 archived `STATUS.json` files (5-archives and 6-trash) that carry old batch
       ids (e.g. `01-eval-real`) to `batch-NN`, from the records' `backfill.former_id`;
     - on the planning surface, rename the old, empty stage folders of its four projects
       (`3-stash`, `4-batches`, `3-batches`, `4-archive`, `5-trash`...) to the current layout;
       only their inboxes hold files;
   - check that the current CLI reads everything (`status`, `cost`, the board's index) with no
     "converted" or "backfilled" line;
   - remove the legacy readers and their scenario cases: `old_words` (`core/records.py`
     `_old_words`), `old_tree` (`lifecycle/convert.py` but `open_repo`, `commands/intake.py`,
     `lifecycle/stages.py`), `backfill_cases` (`lifecycle/backfill.py`, `convert.py`,
     `core/batch_records.py`), the `.agents/changes/` path-prefix reading (`core/repo.py`,
     `history.py`), and the scenario's `confirmed` check in `release_on_stack`; `open_repo`
     becomes `Repo.find` for its importers. `lifecycle_regressions` is not legacy: it stays.
   - look by hand at `5-archives/work/captures` (a stray folder with an empty `batch`).
3. Docs and cards stop promising the conversion of an older tree.

Until this CR merges, no chantier command runs on the planning surface's
`agentic-planning-surface` project: its `5-trash/` would be "converted".

Done when the long gate passes on main on Windows, both forges, and the CLI reads both planning
folders with no conversion code left.
