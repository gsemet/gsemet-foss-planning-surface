# CR-254 rebase onto origin/main (06dfb10)

Note: origin/main resolved to 06dfb10 in the worktree (not a6760ca); the branch is now 5 commits on it.

## Commit 1/4 (timing) - scenario/run_scenario.py
- One hunk, the case-call list at the end of `main`. Main had dropped `old_words`, `old_tree`,
  `backfill_cases`; this CR wraps each call in `with timed(...)`. Kept the timed form, without the
  three dropped calls.

## Commit 2/4 (nine units) - scenario/run_scenario.py
- One hunk, the same call list. This CR moves the calls into `UNITS`: kept this CR's side (calls gone
  from `main`). UNITS had no reference to the three dropped cases.

## Commit 3/4 (pytest + README contract)
Commit 3 also ran ruff format on run_scenario.py (later undone by commit 4), so main's side was unformatted.
- scenario/README.md: whole file conflicted. Took this CR's version, then applied main's removals:
  the "older batch's `confirmed` giving no go" clause, the "old batch" bullet (`legacy: old_words,
  old_tree`), the backfill bullet reduced to its external-mode part (unit: surface-board), and the
  `(legacy: <case>)` sentence.
- run_scenario.py hunks 1-2 (`rec["backfill"] is None`): this CR's text with main's
  `"backfill" not in rec`.
- Hunk 3 (`failed_opening`, `playbook_config` on main's side; `plant_archive`, `backfill_cases` on
  this CR's): neither kept. Main did not change the first two (this CR moved them to pytest), and
  main dropped the other two.
- Hunks 4-6 (the "15." older-CLI `confirmed` block, `old_words`, `old_tree`): deleted, as main did.
- Auto-merged and checked: main's verdict wording check, `rel = "1-inbox/..."`.

## Commit 4/4 (own formatting) - run_scenario.py
- Six hunks, same pattern: backfill checks and "formatted vs own style" took this CR's style with
  `"backfill" not in rec`; `plant_archive`, "15." block, `old_words`, `old_tree` deleted.

## Fix commit 6c5c55d
- test_scenario_coverage.py: removed the `legacy` marker kind and `runner_functions` (no README
  bullet uses it any more).

## Gates
- `just check`: pass (ruff, mypy, lock, biome, 100 pytest passed, release notes).
- `uv run --locked python scenario/run_scenario.py --jobs 4 --unit parallel`: 172/172 checks, 183.7 s,
  375 commands; over its 150 s budget (warning only, machine loaded; the table marks it "over
  budget"). Transcript: scenario/results/scenario-20261115-010849-10832.md in the worktree.
- Not run: the full scenario (all units).
