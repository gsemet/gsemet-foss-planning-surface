Head: fb7d936bd84323beeb173eb1198ba89486a6ef88

Verdict: VERIFIED (the under-300 s target is a known gap, not a failure).

(a) fb7d936: `just check` in the worktree -> ruff, mypy, uv lock, biome pass; "100 passed in 27.98s"; release-notes ok.
(b) fb7d936: `uv run --locked --project skills/chantier/scripts/cli pytest -q skills/chantier/scripts/cli/tests/test_scenario_coverage.py` -> "1 passed". On a scratch edit of scenario/README.md (a `(unit: X)` marker replaced by `bogus-unit`) -> "1 failed", "unit 'bogus-unit' is not a key of UNITS: ...". README restored with `git checkout`; `git status` clean.
(c) fb7d936: `uv run --locked python scenario/run_scenario.py --jobs 4 --unit qa-driver --unit gitlab` -> exit=0; table: qa-driver 42/42 88.8 s (budget 115) ok; gitlab 31/31 57.3 s (budget 95) ok; wall 88.8 s.
(d) test_cost_reading.py line 128 asserts `"$X so far"`, "(../../STATUS.md)", "- [x] Merged" on the paused CR page; the STATUS.md cost row is asserted in the same file (grep of those three strings found line 128 only; the row check was not confirmed by a separate grep).
(e) `git diff --stat origin/main -- skills/chantier/scripts/cli/src/` -> empty.
(f) `git diff --stat origin/main -- scenario/run_scenario.py` 711+/960-; with `-w` 702+/951-: 18 lines of whitespace-only difference, no whole-file reformat.

Known gap: wall time 449.8 s (jobs 4) / 354.0 s (jobs 8) on the loaded Windows machine, over 300 s; CI ubuntu 1m43s.

PR body (work/pr-body.md) judged against the diff: accurate (files, counts, "nothing under src/", 100 tests, Known gaps honest). One caveat: Test plan "Evidence" box is unticked, as stated.
