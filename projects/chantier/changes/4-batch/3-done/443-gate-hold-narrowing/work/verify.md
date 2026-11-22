# Verify CR-443

Head: 187d6b601f35ccfc42718a94f99d834359bbf859

Restack move: 11f98d9 (base 648dac8) -> 187d6b6 (base 4c372daf). Judged again at 187d6b6.

- Patch: `git range-diff 648dac8...11f98d9 4c372daf...187d6b6`: commit 2 is `=`; commit 1 differs only in the four conflict files (AGENTS.md, docs/server-api.md, driver.md, hosts/claude-code.md); commit 3 differs in a driver.md context line. In the resolved files main's new text is kept (AGENTS.md forge-calls clause, `needs_you` row of `board.get`, `The CLI reads no forge`, the `--check` sync rule row) and the CR's text is present (no `.lease-hold.*.run` in AGENTS.md, no `holds` in `project.state`, "`gate` runs only the long gates ... `lease hold` runs nothing"). `git grep "<<<<<<<"` on the four files: no marker. PASS.
- Full CLI suite at 187d6b6, `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests -q -n 3`: `1801 passed, 20 skipped in 227.38s`. Holds the gate refusals, hold limits, no `.lease-hold.*` file, shipped files, startup manifest and allow rules. PASS.
- `uv run --no-sync python evals/kit/dry_run.py`: `dry run: 19 of 19 cases as expected`. PASS.
- `git grep -n "lease-hold\|HOLDS" -- skills/chantier/scripts/cli/src`: only `core/files.py:216` (`IGNORED`). `git grep "until the CR .gate-hold-narrowing"`: no output. PASS.
- Long suite: not run here (a local gate runs elsewhere); the pipeline `just scenario (ubuntu-latest)` must be green at the pushed head. Not claimed.
- PR description: carried from 11f98d9 (renders, matches diff); only SHAs stale, which the Driver updates. No images.

VERIFIED
