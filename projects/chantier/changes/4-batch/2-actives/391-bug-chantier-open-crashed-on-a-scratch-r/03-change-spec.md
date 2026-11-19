# Change Specification: `chantier open` crashes in a planning surface whose project has no clone

## Goal

`chantier open` must never end in a Python traceback. During the v0.14.0 release demo (CR-388, the
Foreman's ask A-43), `open` of a batch with no CR (factory) crashed on a scratch planning surface,
so the release notes' factory highlight has no capture. Find the cause, fix it, and cover it with a
test.

## Cause (found and reproduced)

The traceback was kept in CR-388's work folder
(`5-archives/261119-2217-388-release-v0-14-0/work/scratch/open.txt`):

```
opening.py:358 open_batch -> settings = open_settings(repo, args)
opening_record.py:24 open_settings -> git("remote", cwd=repo.root)
core/git.py:14 git -> subprocess.run(..., cwd=cwd)
NotADirectoryError: [WinError 267] (the directory name is not valid)
```

In external mode (`--project <surface>/projects/<name>`), `Repo._external`
(`skills/chantier/scripts/cli/src/chantier/core/repo.py`) sets `repo.root` to the project's clone:
`checkout.yml`'s `repo:`, by default `.repo` in the project's folder. Nothing checks that this
folder exists. `open_settings` (`commands/opening_record.py`) runs its first git command,
`git remote`, with `cwd=repo.root`. When the clone does not exist, `subprocess.run` raises
`NotADirectoryError` on Windows (`FileNotFoundError` on POSIX) before git starts. `core/git.py`'s
`git()` does not catch it, so the CLI ends in a traceback instead of a `ChantierError`.

Reproduced on 2026-11-20 in a scratch folder, not in a user's repository:

- In-project mode (a fresh `git init` with one empty commit, no remote): `open` and
  `open --factory` both end cleanly with `error: no remote 'origin': pass --remote <remote>`. No
  crash.
- External mode (a fresh git repository `surf` with `projects/demo/changes/` and no clone):
  `chantier --project surf/projects/demo open --factory` crashes with the traceback above.

The release Driver's scratch was an external surface whose project had no clone. Preflight
already detects that state (P8: "no clone of the project at <path> (remote <r>): clone it there",
`commands/preflight.py`, `_check_instructions`), but `open` runs without preflight and checks
nothing.

## What changes

### 1. `open` refuses a missing clone with preflight's words

- In `open_settings` (`commands/opening_record.py`), before the `git remote` call: when
  `repo.external` and `repo.clone` is not a directory, raise a `ChantierError` (code
  `EXIT_PRECONDITION`). Its message is the one P8 gives:
  `no clone of the project at <clone path, posix> (remote <remote from project.md, or "see project.md">): clone it there`.
- Write the message once. Move the text P8 builds (including how it reads the remote from
  `project.md`) into one function that preflight's P8 and `open` both call. Suggested place:
  `core/repo.py`, for example `Repo.missing_clone() -> str | None`, which returns the message, or
  None when the project is in-project or its clone exists. The Driver picks the final name and
  place. P8's output stays exactly as it is.
- The check runs before any folder moves or writes. `open_settings` already runs before
  `stage_layout` and before the record is written, so a refused `open` leaves the planning folder
  unchanged.

### 2. `git()` never lets a missing working folder through as a traceback

Other commands also pass `cwd=repo.root` to git: `order add` (`commands/orders.py`, line 123, via
`default_branch`) and the driver checks (`commands/driver_checks.py`). They would crash the same
way on a missing clone. In `core/git.py`'s `git()`: when `cwd` is given and is not a directory,
raise `ChantierError(f"no folder {cwd}: git cannot run there", EXIT_PRECONDITION)` (the wording
is the Driver's to settle) instead of calling `subprocess.run`. This applies whatever `check` is,
because the traceback came before git ran, and `check=False` callers crash too. `default_branch`
and every other helper in that module go through `git()`, so they are covered.

This is a clear refusal that names the folder. It is not a fallback: nothing is guessed and
nothing is retried.

### 3. Nothing else

No card changes: the cards say nothing about this crash. No scenario step changes. No change to
`Repo.find` or `_external`: a surface whose project has no clone yet must still work for the
commands that do not need the clone (`status`, `validate`, `board`, triage and the backlog).

## Host and default matrix

The clone's path comes from either the shipped default or a configured value (`checkout.yml`).
Both cells must give the same clean refusal:

- `checkout.yml` with no `repo:` (shipped default `.repo`), clone missing: `open` and
  `open --factory` exit `EXIT_PRECONDITION` with the "no clone of the project at
  `<project>/.repo`" line, and no traceback.
- `checkout.yml` with a configured `repo: <path>`, that path missing: the same refusal, naming the
  configured path.

The AI host (Claude Code or Copilot) plays no part.

## Evidence

- A new parametrized test, in `skills/chantier/scripts/cli/tests/test_open_empty_batch.py` or in
  a new small test file next to it. It uses the `surface` fixture (`tests/conftest.py`), removes
  the clone (`shutil.rmtree(surface.clone)`), and for the configured cell rewrites
  `projects/demo/checkout.yml` with a `repo:` that points at a missing folder. It then calls the
  CLI in-process (`chantier("open", ...)`, through the `chantier` fixture, with the open flags
  that `batch_helpers` uses). Cases: `open` with no CR, and `open --factory`, on the default cell;
  `open --factory` on the configured cell. Each case asserts:
  - the exit code is `EXIT_PRECONDITION`;
  - stderr holds `no clone of the project at` followed by the expected path, and holds no
    `Traceback`;
  - the planning folder is unchanged: no `4-batch/batch.json`, no new record in
    `5-archives/batches/`.
- One case in `tests/test_cli_units.py`: `git("status", cwd=<tmp_path / "missing">, check=False)`
  raises a `ChantierError` that names the folder, not an `OSError`.
- The existing preflight tests that cover P8, if any, still pass unchanged. That proves the shared
  message kept P8's text. If no test covers P8's no-clone line, add one assertion on it in the
  same new test, so that the shared message has both callers checked.
- `just check` on Linux, macOS and Windows. This is a change under the CLI's `src/`, so it also
  owes `just eval-dry-run` before the first push and the pipeline's `just scenario
  (ubuntu-latest)` job before the PR (AGENTS.md).
- Manual check, in a scratch folder only: rerun the reproduction above (an external scratch
  surface with no clone, `open --factory`). It must print the one-line refusal. Then create the
  clone (a `git init` at `projects/demo/.repo` with an `origin` remote and an `origin/HEAD`); the
  same `open --factory` must open the batch born paused.

## Out of scope

- Capturing the factory demo for the v0.14.0 release notes. That is a release task, not this fix.
- Making `open` work without a clone, or creating the clone: the user clones it, as P8 already
  says.
- `just tag`'s check-tag behaviour, noted in CR-388's retro: a separate item.

## Open questions

None.
