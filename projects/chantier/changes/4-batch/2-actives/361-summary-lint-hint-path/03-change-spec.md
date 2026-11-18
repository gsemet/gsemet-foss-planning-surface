# The summary lint hint gives a path summary set can read

## Goal

Every gap line `summary lint` prints ends with the `summary set` command that closes it. An agent
copies that command as is, and it must work. Today it fails: the line prints the CR's folder
relative to the session's root (the project's repository, or the planning surface), and
`summary set` reads a relative folder from the planning folder. The fix: the line prints the
folder in the form `summary set` reads, relative to the planning folder, the same form the other
commands take for a folder argument. `summary set` does not change.

## Reproduced (2026-11-18, external mode, read-only)

From `C:/Users/gaeta/Projets/gsemet-foss-planning-surface`, with
`uv run --no-sync --project C:/Users/gaeta/Projets/chantier chantier --project projects/chantier`:

- `summary lint` printed, for example:
  `projects/chantier/changes/2-backlog/P1/archive-in-pr-from-settings: no summary → summary set projects/chantier/changes/2-backlog/P1/archive-in-pr-from-settings --title "<title>" --summary "<the CR's state now>"`.
- Passing that printed path back to a command that reads a folder the way `summary set` does
  (`summary lint <path>`, which uses the same `_cr_folder`) exits 1 with
  `error: not a CR folder: projects/chantier/changes/projects/chantier/changes/2-backlog/P1/archive-in-pr-from-settings`.
- `summary lint 2-backlog/P1/archive-in-pr-from-settings` (relative to the planning folder) is
  read and reports the gap.

In-project mode fails the same way: the session root is the repository, so the line prints
`.agents/changes/<stage>/<slug>`, which `summary set` reads as
`.agents/changes/.agents/changes/<stage>/<slug>` (the request's report).

## Cause

`skills/chantier/scripts/cli/src/chantier/commands/summary.py`:

- `_gap_line(repo, gap)` builds the path with `shown(repo, gap.folder)`
  (`lifecycle/filing.py`): relative to `repo.session_root`.
- `_cr_folder(repo, paths, item)` reads the argument with `repo.planning_path(item, ...)`
  (`core/repo.py`): a relative value is read from `repo.changes`, the planning folder.

## What changes

1. `commands/summary.py`, `_gap_line`: the path the line prints is the CR's folder relative to the
   planning folder, built with `repo.rel(gap.folder)` (`core/repo.py`, "a path in the planning
   folder, as the record keeps it: relative to that folder"), in place of `shown(repo, ...)`. The
   line keeps one path for its label and for its command, so the whole line names the folder in
   one form, the one the command reads. The three kinds keep their wording: `no summary`,
   `summary.json unreadable (...)`, `summary late (...)`; only the path changes.
   Example, external mode: `2-backlog/P1/archive-in-pr-from-settings: no summary → summary set 2-backlog/P1/archive-in-pr-from-settings --title "<title>" --summary "<the CR's state now>"`.
2. Nothing else in the CLI changes: `summary set`, `_cr_folder`, `shown`, `summary set`'s own
   confirmation line and its `not a CR folder` error keep their current form.
3. Cards and docs: no change. `chief-of-staff.md` (line 202), `concepts.md` ("A CR's summary"),
   `griller.md` and `spec-writer.md` say that the line carries the command that closes the gap,
   with no path form; they stay true.

## Decisions carried from 02-answers.md

- First step: reproduce it. Done above; the Driver reproduces it again in its worktree before the
  fix (the new test, below, fails on the current code).
- The hint is the path form `summary set` reads (relative to the planning folder, as the other
  commands' folder arguments are), so it can be copied as is. `summary set` is unchanged.
- No spec critic: the change is the text of a hint and its test.

## Out of scope

- How `summary set`, `summary label`, `summary group` or any other command prints a path in its
  own output or errors (`shown`, relative to the session root).
- Reading the session-root-relative form in `summary set` or `planning_path` (the answers keep
  `summary set` unchanged).
- Any other command's hint or path form.

## Host and default matrix

The path form depends on the planning folder's place (in-project, the default, versus an external
planning surface), not on the host (Claude Code or Copilot). One line per cell:

- In-project (planning folder `<repo>/.agents/changes/`, session root the repository): the hint
  printed `.agents/changes/<stage>/<slug>`, refused; it prints `<stage>/<slug>`, read.
- External (planning folder `<surface>/projects/<name>/changes/`, session root the surface): the
  hint printed `projects/<name>/changes/<stage>/<slug>`, refused; it prints `<stage>/<slug>`, read.

## Evidence

- One new test in `skills/chantier/scripts/cli/tests/` (for example in `test_cli_runs.py`),
  in-process through the `chantier` fixture, parametrized over the two cells of the matrix: the
  `repo` fixture (in-project) and the `surface` fixture (external, one project, taken without
  `--project`). Each case: `chantier("file", "<title>")` files a CR with no summary;
  `chantier("summary", "lint")` exits 2; the test takes the path from the command part of the gap
  line (the text after `summary set ` up to the next space), asserts it is relative (no leading
  `.agents/` nor `projects/`), runs `chantier("summary", "set", <that path>, "--title", "T",
  "--summary", "S")` with exit 0, and `summary lint` then prints `no gap (1 CRs)` with exit 0. The
  test fails on the current code (the `summary set` exits 1 with `not a CR folder`) and passes
  after the fix. It keeps `just test` within its budget (one test, two cases).
- The scenario's existing summary checks (`scenario/run_scenario.py`, `summary_basics` and the
  surface unit's `summary set` and `lint` check, the archive's `delivery.md new` check) assert no
  path form and keep passing; no scenario step is added.
- `just check` passes; the change is under the CLI's `src/`, so `just eval-dry-run` before the
  first push, and `just scenario (ubuntu-latest)` green at the PR's head, as AGENTS.md asks.
- Manual check after merge, in this surface: a hint printed by `summary lint` copied as is into
  `summary set` (or `summary lint <path>`) is read.

## Open questions

None.
