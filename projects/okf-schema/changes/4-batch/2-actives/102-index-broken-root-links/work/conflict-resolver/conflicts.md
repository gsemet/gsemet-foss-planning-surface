# CR-102, restack on CR-104

Worktree `C:/Users/gaeta/Projets/okf-schema.worktrees/batch-01-CR-102`. New base 1a03994
(CR-104, on CR-101). Old head 8537709 (base 2f09cef), new head d9e1b30: 9f9bebf (was 4b38782)
and d9e1b30 (was 8537709). Rebase finished, tree clean, nothing pushed.

## Conflicted hunks

Commit 1 (4b38782):

- `requirements/tiers/log.md`, under `## 2026-11-25`. The base had `### Trust tier actor forms`
  and `### Show a concept by name, inside the bundle`; the commit had `### Index summaries and
  broken links`. All three kept word for word under the one day heading, newest first: Index
  (CR-102), Trust tier (CR-104), Show (CR-101).
- `skills/okf-schema/SKILL.md`, CLI table. `show` row from the base (CR-101); `index` and `stats`
  rows from the commit (CR-102). The base's W10 row and the commit's W2 row merged on their own.

Commit 2 (8537709):

- `CHANGELOG.md`, `## Unreleased` / `### Fix`. Both lines kept: `**index**` (CR-102) above
  `**validate**` (CR-104), newest first.

No byte-order mark added (the three files start with the same text as before), no marker left.

## Silent mis-merge fixed (no conflict reported by git)

- `CHANGELOG.md`, commit 1: its one-line change renames the old base's `## Unreleased` to
  `## v0.18.1 (2026-11-25)`. The base already has that heading, so git applied the rename to the
  base's new `## Unreleased`, putting the CR-104 line under a second `v0.18.1` heading. Restored
  `## Unreleased`. Commit 1 therefore no longer touches `CHANGELOG.md` (15 files, was 16).

## Automatic merges checked

- `git range-diff 2f09cef..8537709 1a03994..HEAD` and the diff against 1a03994 of `src`, `docs`,
  `requirements` and `skills`: the CR's changes are present beside the base's.

## Fast gate

No fast gate: the project's rules name none (the long gate, `just preflight`, is the Driver's and
was not run).

## Other checks run (not a gate)

Run on d9e1b30. `<wt>` is the worktree path above; the `uv` commands are
`uv run --no-sync --directory <wt> -- <command>`.

| Command | Result |
|---|---|
| `pytest -q -n 4 -p no:cacheprovider --no-cov` | pass: 1236 passed, 12 skipped |
| `okfreq lint requirements --check --check-links --project-root .` | pass: 0 indexes, 0 projections would change |
| `okfreq update-coverage requirements --check` | pass: 0 files would change |
| `okfreq validate requirements --prose --check-links --project-root .` | pass: 36 requirements, 0 errors, 0 warnings |
| `ruff check src tests examples/okfreq-examples/showcase.py` | pass |
| `ruff format --check src tests examples/okfreq-examples/showcase.py` | pass: 67 files already formatted |
| `just --justfile <wt>/justfile typecheck` | pass (ty, mypy) |

Not run: coverage, `just refresh-all-examples`, `just requirements-report`, `just docs`,
`okfreq trace`.

## For the Driver

1. `cz changelog --dry-run` (writes nothing) at d9e1b30 prints under `## Unreleased` a third line,
   `- **show**: accept names without .md and stay inside the bundle`, which the committed file
   lacks (already missing on the base). `just preflight` runs `just changelog`, so expect it to
   leave `CHANGELOG.md` modified. Not added here.
2. The CR-102 log entry's Verification bullet (`1187 tests passed`, coverage 95.68%) records the
   run on the old base. Kept as written; it does not describe d9e1b30.
