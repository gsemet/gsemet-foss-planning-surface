# Change Specification: `just check` runs ruff's lint rules on `scripts/`

## Goal

`just check` lints the repository's own tooling scripts (`scripts/`) with the same ruff rules as
`skills/`, so a script that breaks a rule fails the check locally and in CI instead of being found
by hand. The findings ruff reports on `scripts/` today are fixed in the same change, with no
change in what any script does.

Origin: left out of CR-308 (`just check` format-checks `scripts`, PR #261, merged 2026-11-17);
filed verbally. No issue.

## State today (main at `3a9afc2c`, v0.13.0)

- `justfile`, recipe `lint`, first two lines:

  ```
  uvx {{ruff}} format --check skills scripts
  uvx {{ruff}} check skills
  ```

  with `ruff := "ruff@0.17.5"` (line 5). `check: lint test release-notes`.
- The root `pyproject.toml`'s `[tool.ruff]` / `[tool.ruff.lint]` (line-length 100, `select` E, W,
  F, I, B, UP, SIM, C90, PL, RUF, PGH004, preview with `extend-select` PLR1702 and TID253, the
  pylint limits) applies to any path checked from the repository's root; it has no
  `per-file-ignores`.
- `uvx ruff@0.17.5 check scripts`, from the root, reports 9 findings (the intake's 15 were counted
  before CR-308's formatting):

  | File | Line | Rule | Finding |
  |---|---|---|---|
  | `scripts/copilot_models.py` | 43 | RUF100 | unused `# noqa: S310` (S is not enabled) |
  | `scripts/docs_screenshots.py` | 149 | PLC0207 | `url.split("#")[0]` splits more than needed |
  | `scripts/docs_screenshots.py` | 224 | E501 | comment line of 101 characters |
  | `scripts/mod.py` | 1 | E501 | module docstring's first line of 101 characters |
  | `scripts/release_notes.py` | 123 | B905 | `zip()` without `strict=` |
  | `scripts/release_notes.py` | 152 | PLR2004 | magic value `3` in `len(value) >= 3` |
  | `scripts/release_notes.py` | 212 | RUF005 | `images(notes) + [thread_image]` |
  | `scripts/version.py` | 95 | PLR0911 | `main` has 7 returns (limit 6) |
  | `scripts/version.py` | 111 | PLW1510 | `subprocess.run` without `check=` |

## What changes

1. **`justfile`, recipe `lint`:** the lint line covers `scripts` too:

   ```
   uvx {{ruff}} check skills scripts
   ```

   The ruff pin, the format line and the other lines of `lint` and `tools` do not change.
   `pyproject.toml` does not change (no rule dropped, no `per-file-ignores`; answers S1).
2. **The nine findings, fixed in the code** (answers S1 to S5); no new `# noqa` anywhere:
   - `copilot_models.py:43`: delete the `# noqa: S310` comment (S2).
   - `docs_screenshots.py:149`: `url.split("#", 1)[0]` (or `url.partition("#")[0]`): the same
     result.
   - `docs_screenshots.py:224`: rewrap the comment over two lines within 100 characters; same words.
   - `mod.py:1`: shorten the docstring's first line to 100 characters at most, saying the same
     (for example "Check the mod from the repository's root: `claude plugin validate .`, then
     `claude plugin test .`."). Nothing reads `mod.py`'s `__doc__`.
   - `release_notes.py:123`: `zip(*[iter(...)] * 2, strict=False)`: today's pairing, unchanged (S3).
   - `release_notes.py:152`: a module constant (for example `MIN_IDENTITY_LENGTH = 3`) used in
     `len(value) >= MIN_IDENTITY_LENGTH`.
   - `release_notes.py:212`: `[*images(notes), thread_image]`.
   - `version.py:111`: `subprocess.run(..., check=False)`: a failing `git log` still gives an empty
     subject and the same "expected" message and exit 1 (S4).
   - `version.py:95`: move the `check-tag` branch of `main` into a function (for example
     `check_tag(version: str) -> int`) that `main` returns, which leaves `main` six returns; the
     printed messages and exit codes of `show`, `check-tag`, `set` and `bump` do not change (S5).

   Run `uvx ruff@0.17.5 format scripts` after the edits so the format check stays clean.
3. **`CONTRIBUTING.md`, "Code standards"** (line 295 onward): one sentence saying that the
   repository's tooling scripts (`scripts/`) meet the **Style** target too, `ruff format` and
   `ruff check` clean through `just lint`; the other targets stay for the plugin's Python under
   `skills/` (S6). The `just check` line at 213 still holds.

Nothing else: no card, no CLI code, no test, no agent file, no release note.

## Decisions carried from `02-answers.md`

- No user question; the intake names the change.
- S1: findings fixed, not silenced; `pyproject.toml` unchanged; no new `# noqa`.
- S2: the unused `# noqa: S310` is deleted.
- S3: `strict=False` on the `zip`, keeping today's pairing.
- S4: `check=False` on `check-tag`'s `subprocess.run`, keeping today's outcome.
- S5: `check-tag` moved out of `version.py`'s `main`; same messages and exit codes.
- S6: `CONTRIBUTING.md` names `scripts/` under the Style target only.
- S7: the out-of-scope list below.

## Out of scope

- `mypy` over `scripts/` (the `mypy` line of `lint` keeps its file set).
- `ruff check` over any other folder (`scenario/`, `evals/`, `tests/`, `hooks/`).
- The file and function size targets of `tests/test_code_targets.py` for `scripts/`.
- Any change in what a script prints, writes or returns.

## CI environment

The change alters what the existing `just check` job of `.github/workflows/ci.yml` runs (matrix
`ubuntu-latest`, `macos-latest` on `macos-15-intel`, `windows-latest`; `astral-sh/setup-uv@v6`,
`extractions/setup-just@v3`; `just tools` fetches the pinned `ruff@0.17.5` before `just check`).
The new path uses the same pinned ruff through `uvx`, from the checkout's root with the same
`pyproject.toml`: no extra cache, credential, tool or network. Ruff's lint results do not depend
on the system, so the local Windows run proves the step; nothing is left for the job's first CI
run to prove beyond the three systems' green `just check`. No host or default matrix: nothing here
depends on a host or a configured value.

## Evidence

- E1. Before the fixes: with only the `justfile` change, `just lint` fails at the `ruff check`
  line naming the nine findings above (proves the check now covers `scripts`).
- E2. After the fixes: `uvx ruff@0.17.5 check skills scripts` and
  `uvx ruff@0.17.5 format --check skills scripts` both pass; `git grep -n "noqa" -- scripts`
  shows no new `# noqa`; `git diff --stat` shows `justfile`, `CONTRIBUTING.md` and the five scripts
  only, and `pyproject.toml` unchanged.
- E3. The scripts still behave as before, run on the repository as it ships at the head under test:
  - `just version-show` prints the current version (0.13.0 or later, as at the head).
  - `uv run --script scripts/version.py check-tag` gives the same exit code and message as on
    main at the same `origin/main` (run both; compare).
  - `just release-notes` passes (part of `just check`; exercises `validate_tweet`'s pairing and
    the identity scan's length filter).
  - `uv run --script scripts/version.py --help` and
    `uv run --script scripts/copilot_models.py --help` exit 0.
  - `scripts/docs_screenshots.py` and `scripts/mod.py` need a browser or a `claude` binary: each
    is parsed (`uv run --no-project python -c "import ast; ast.parse(open('scripts/<f>.py',
    encoding='utf-8').read())"` exits 0), and `just mod` runs when a `claude` is at hand.
- E4. `just check` passes on the Windows machine, and the PR's `just check` jobs pass on Linux,
  macOS and Windows. The change touches neither the CLI, the cards nor the scenario, so the
  project's rules ask no `just scenario` beyond the pipeline's job, and no `just eval-dry-run`.

## Open questions

None.
