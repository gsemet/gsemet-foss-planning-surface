# Change Specification: planning-folder.md says the archive in the PR defaults to no

## Goal

Two pages of the docs disagree on whether a CR's cleaned archive goes into its PR when the project
says nothing. The CLI decides **no**. Make the page that says **yes** say **no**, so the docs match
the CLI and each other. Docs only.

## Where it lands

On `main` now, in the page as it is on `main` (decision of 2026-11-20, `02-answers.md`). CR-382
(PR #347, now back in backlog P2 as `docs-style-guide`) is not waited for: it rebases over this fix
when it comes back. The paths named in `01-intent.md` (`docs/explanation/planning-modes.md`,
`docs/reference/planning-folder.md`) are PR #347's; on `main` the pages are:

- `docs/planning-folder.md`: says **yes** (the page to fix).
- `docs/planning-modes.md`: says **no** (already right; unchanged).

## What the CLI does (the reference, unchanged)

- `skills/chantier/scripts/cli/src/chantier/core/repo.py` (around line 155): in external mode,
  reads one line of the surface's `projects/<name>/project.md`, `- Archive in the PR: yes|no`
  (case-insensitive); `archive_in_pr` is true only for `yes`. No file, no line, or `no`: false.
- `skills/chantier/scripts/cli/src/chantier/plugin_files.py`, `archive_path` (around line 135):
  returns no archive path when the mode is in-project or the project does not set
  `- Archive in the PR: yes`.
- Covered already by `skills/chantier/scripts/cli/tests/test_external_archive.py`.
- Since v0.13.0 (`docs/release-notes/2026-11-18-v0.13.0/release-notes.md`, "Change of default").

Note: `01-intent.md` says the line is read from the project's `AGENTS.md`; the code reads it from
the surface's `projects/<name>/project.md`, which is what both pages already say. Nothing in the
docs changes on that point.

## What changes

One file, one line: `docs/planning-folder.md`, line 55, in the paragraph that starts
"What is published and what stays local":

- now: `by the project's setting (default yes), a cleaned copy in the CR's PR, in external mode.`
- after: `by the project's setting (default no), a cleaned copy in the CR's PR, in external mode.`

Nothing else in that page or any other page changes. Checked on `main` (4fdf6fc9): this is the only
"default yes" about the archive outside the release notes; `docs/planning-modes.md` (table row
"Archive in the PR": `by the project's setting, default no`; and "`no` when absent"), `README.md`
and the cards (`concepts.md`, `driver.md`) already agree with the CLI or name no default. The
release notes stay as published (v0.13.0 documents the change of default itself).

## Out of scope

- Any change to the CLI, its tests, the cards, the scenario or the SVGs.
- `docs/planning-modes.md`, `README.md` and the release notes.
- PR #347's page moves and wording (`docs-style-guide`, backlog P2).
- Correcting `01-intent.md`'s mention of `AGENTS.md` beyond the note above.

## Evidence

- At the PR's head: `git grep -n -i "default yes" -- docs ':!docs/release-notes'` prints nothing,
  and `git grep -n "(default no), a cleaned copy" docs/planning-folder.md` prints line 55. These
  read the shipped page from the repository at the head under test.
- `git diff --stat main...HEAD` shows one file, `docs/planning-folder.md`, one line changed.
- `just check` passes (AGENTS.md: before hand back). No `just eval-dry-run` (no change under the
  CLI's `src/` or the eval kit) and no `just scenario` gate (a change to the docs alone needs none).
- No new test: the CLI's behaviour is already covered by `test_external_archive.py`; the fix adds
  no check of its own.

## Open questions

None.
