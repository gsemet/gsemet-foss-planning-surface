# CR-104, stack restack on CR-101

Worktree `C:/Users/gaeta/Projets/okf-schema.worktrees/batch-01-CR-104`. New base 41fcd6d
(CR-101). Old head 7a33d92 (base 2f09cef), new head 1a03994: ad55758 (was 1ae8870) and 1a03994
(was 7a33d92). Rebase finished, tree clean, nothing pushed.

## Conflicted hunks

One hunk, on commit 1 of 2: `requirements/tiers/log.md`, under `## 2026-11-25`.

- Sides: the base added `### Show a concept by name, inside the bundle` (CR-101); the commit added
  `### Trust tier actor forms` (CR-104), each under a new day heading at the same place.
- Choice: both entries kept word for word under a single `## 2026-11-25` heading, CR-104 first
  (newest), then CR-101. No byte-order mark (first bytes `23 20 55 70`), no marker left.

Commit 2 applied with no conflict.

## Automatic merges checked

- `git range-diff 2f09cef..7a33d92 41fcd6d..HEAD`: commit 2 is identical; commit 1 differs only in
  the context of the `log.md` hunk. So the CR's changes to the other files are the ones it had.
- `skills/okf-schema/SKILL.md`: the CR-101 `show` row (line 135) and the CR-104 W10 row (line 367)
  are both present.
- `tests/test_api.py`, `tests/test_cli_remaining.py`: both sets of tests present; they pass (below).

## Fast gate

No fast gate: the project's rules name none (the long gate, `just preflight`, is the Driver's and
was not run).

## Other checks run (not a gate)

Run on the resolved tree of commit 1, before `rebase --continue` (commit 2 changes only
`CHANGELOG.md`). `<wt>` is the worktree path above.

| Command | Result |
|---|---|
| `just --justfile <wt>/justfile requirements-lint` | pass: 0 indexes, 0 projections, 0 files would change |
| `uv run --no-sync --directory <wt> -- okfreq validate requirements --prose --check-links --project-root .` | pass: 36 requirements, 0 errors, 0 warnings |
| `uv run --no-sync --directory <wt> -- pytest -q -p no:cacheprovider --no-cov tests/test_api.py tests/test_cli_remaining.py tests/test_okf2_compliance.py tests/test_kb_scaffold.py tests/test_project_contract.py tests/test_edge_cases.py` | pass: 361 passed |
| `uv run --no-sync --directory <wt> -- ruff check src tests examples/okfreq-examples/showcase.py` | pass |
| `uv run --no-sync --directory <wt> -- ruff format --check src tests examples/okfreq-examples/showcase.py` | pass: 67 files already formatted |
| `just --justfile <wt>/justfile typecheck` | pass (ty, mypy) |

Not run: full test suite, coverage, `just refresh-all-examples`, `just requirements-report`,
`just docs`, `okfreq trace`.

## For the Driver

1. `CHANGELOG.md` is behind the new base. `uv run --no-sync --directory <wt> -- cz changelog
   --dry-run` (writes nothing), run at 1a03994, prints under `## Unreleased` a second line,
   `- **show**: accept names without .md and stay inside the bundle`, which the committed file
   lacks (CR-101's branch does not carry it). `just preflight` runs `just changelog`, so expect it
   to leave `CHANGELOG.md` modified. Not edited here: the rebase left no conflict in it.
2. The CR-104 log entry's Verification bullet (`1118 passed, 14 skipped, 8 failed`, `WinError
   1314`) records round 1 on the old base 2f09cef. Kept as written; it does not describe 1a03994.
