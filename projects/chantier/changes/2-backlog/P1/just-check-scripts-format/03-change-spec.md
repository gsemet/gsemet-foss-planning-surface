# Change Specification: `just check` format-checks `scripts`

## Goal

`just check` checks the format of the repository's own tooling scripts (`scripts/`) as it does for
`skills/`, so that an unformatted script fails the check locally and in CI instead of being found
by hand. The three scripts that fail the format check today are formatted in the same change.

Origin: the retro of batch-22 (2026-11-17, record `5-archives/batches/batch-22.md`), a point the
retro critic kept; the user put it in the next batch (P1). No issue.

## State today (main at 3df17b9, v0.11.0)

- `justfile`, recipe `lint` (line 56 onward), first two lines:

  ```
  uvx {{ruff}} format --check skills
  uvx {{ruff}} check skills
  ```

  with `ruff := "ruff@0.17.5"` (line 5). `check: lint test release-notes`.
- `scripts/` holds five files: `copilot_models.py`, `docs_screenshots.py`, `mod.py`,
  `release_notes.py`, `version.py`.
- `uvx ruff@0.17.5 format --check scripts` (run from the repository root, so the root
  `pyproject.toml`'s `[tool.ruff]` applies: `line-length = 100`) reports
  "3 files would be reformatted, 2 files already formatted": `scripts/mod.py`,
  `scripts/release_notes.py`, `scripts/version.py`. The diffs are pure layout (long lists, calls
  and strings split over lines, one blank line after `release_notes.py`'s module docstring).

## What changes

1. **`justfile`, recipe `lint`:** the format check covers `scripts` too. The first line becomes

   ```
   uvx {{ruff}} format --check skills scripts
   ```

   The second line (`uvx {{ruff}} check skills`) does not change. The ruff pin and the other
   lines of `lint` do not change.
2. **`scripts/mod.py`, `scripts/release_notes.py`, `scripts/version.py`:** formatted with the
   pinned ruff from the repository root: `uvx ruff@0.17.5 format scripts`. Only what the formatter
   writes changes; no hand edit, no behaviour change. `copilot_models.py` and
   `docs_screenshots.py` are already formatted and stay as they are.

Nothing else: no card, no CLI code, no test, no doc. `CONTRIBUTING.md` already says `ruff format`
clean for the code, and its `just check` line ("lint (ruff, mypy, the lock) and structure tests")
still holds.

## Decisions carried from `02-answers.md`

- No grill question: the retro point names the whole change (`just check` format-checks
  `scripts`; the three files are formatted). Both parts are above.
- No spec critic: the change touches a check of the repository's own tooling, no behaviour of
  chantier.

## Out of scope

- `ruff check scripts` (the lint rules, not the format). Today it reports 15 findings over the five
  scripts (E501, RUF005, PLR2004, PLC0207, PLW1510, PLR0911, RUF100, B905); formatting removes
  some of the E501 lines only. Adding `scripts` to the `ruff check` line is not part of this CR.
- `mypy` over `scripts/` (the `mypy` line of `lint` keeps its current file set).
- Any other folder (`scenario/`, `evals/`, `tests/`, `hooks/`).

## CI environment

The change alters what the existing `just check` job of `.github/workflows/ci.yml` runs (matrix
`ubuntu-latest`, `macos-latest` on `macos-15-intel`, `windows-latest`; `astral-sh/setup-uv@v6`,
`extractions/setup-just@v3`). The new step uses the same pinned `ruff@0.17.5` through `uvx` as
the existing `format --check skills` line, from the checkout's root with the same
`pyproject.toml`; it needs no cache, credential or network beyond what `uvx ruff@0.17.5` already
fetches there. The ruff formatter's output does not depend on the system, so the local Windows run
proves the step; the line endings come from the checkout (git's autocrlf on Windows), which the
existing `skills` format check already meets the same way. Nothing here is left for the job's
first CI run to prove beyond the three systems' green `just check`.

## Evidence

- E1. Before the format: in the worktree, with the `justfile` change and the three scripts not yet
  formatted, `just lint` fails at the format line naming the three scripts (proves the check now
  covers `scripts`).
- E2. After `uvx ruff@0.17.5 format scripts`: `uvx ruff@0.17.5 format --check skills scripts`
  prints that all files are already formatted, and `git diff --stat` shows changes in `justfile`,
  `scripts/mod.py`, `scripts/release_notes.py`, `scripts/version.py` only.
- E3. The formatted scripts still run: `just version-show` prints the current version,
  `just release-notes` passes (it is part of `just check`), and
  `uv run --script scripts/version.py --help` exits 0. `scripts/mod.py` needs a `claude` binary;
  `uv run --no-project python -c "import ast,sys; ast.parse(open('scripts/mod.py',encoding='utf-8').read())"`
  exits 0 when no `claude` is at hand.
- E4. `just check` passes on the Windows machine, and the PR's `just check` jobs pass on Linux,
  macOS and Windows. No `just scenario` is needed by the project's rules beyond the pipeline's
  job (the change touches neither the CLI, the cards nor the scenario).

## Open questions

None.
