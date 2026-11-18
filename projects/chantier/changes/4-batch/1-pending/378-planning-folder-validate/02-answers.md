# Answers

The user was asked no questions on this CR: the spec-writer settled the points below with no
user-visible behaviour, and the Chief of Staff settled the spec-writer's questions (Q1, Q2) and the
spec-critic's findings in the sections that follow.

## Settled by the spec-writer (2026-11-18)

Points with no user-visible behaviour, or read directly from the request:

1. **One project per run.** `chantier validate` checks the planning folder `--project` names (or
   the project's own `.agents/changes/`, or a surface's only project), as every command resolves
   it. The surface's script keeps its loop over its projects. No positional argument: the whole
   planning folder, as the request says.
2. **Read-only.** The command writes nothing: no `.gitignore`, no lock, no STATUS file, no
   summary. It takes no lifecycle lock; a move made while it runs may show in its result, and the
   next run reads the new state.
3. **What a CR folder is.** As the CLI reads it today (`lifecycle/stages.py`): every folder directly
   in a stage folder (`1-inbox`, `2-backlog/P1`..`P4`, `3-ready`, `4-batch/1-pending`,
   `2-actives`, `3-done`, `5-archives`, `6-trash`); `5-archives/batches/` holds the batches'
   records and is no CR. A folder elsewhere is taken for a CR when it holds one of a CR's own
   entries (`intake/`, `01-intent.md`, `02-answers.md`, `03-change-spec.md`, `summary.json`).
   Entries whose name starts with a dot (`.gitkeep`, the locks, `.long-gate.queue`) are skipped
   everywhere. A stage folder that does not exist is not reported (the CLI creates it on use).
4. **Links.** Only relative links whose target is a Markdown file (`.md`), resolved from the file
   that holds them and landing inside the planning folder, are checked, as the request says
   ("links between Markdown files of the planning folder"); a link with a scheme, an absolute
   path, a target outside the planning folder, an image or another file is not. Code spans and
   fenced blocks are skipped; an anchor (`#...`) is not checked, only the file. The `STATUS.md`
   files are skipped: the CLI rewrites them at every state change.
5. **Exit codes.** 0: nothing found. 2: gaps only (the code `summary lint` already gives its
   gaps). 3: at least one error, with or without gaps. 1: the command could not run (no planning
   folder, a surface with several projects and no `--project`, outside a git repository), so a
   caller never reads a refusal as a gap.
6. **Output.** First line: the counts; then one line per finding, the errors first, each group
   sorted by path, paths relative to the planning folder (the form `summary set` reads), each
   line naming what closes it when there is a command for it. Every line is printed, never cut
   at ten.
7. **Summary lines.** A missing or late summary is reported with the very line `summary lint`
   prints for it (the same code builds both), so the two commands never disagree.

## Settled by the Chief of Staff (spec-writer's questions, 2026-11-18)
- Q1: as specified. Errors are only what chantier or the board misreads; broken links, a CR with
  no request, a stray file and an entry outside the layout are gaps, and gaps pass.
- Q2: no. Archives and trash get placement and summary format only, as specified; their old
  links are not checked.

## Settled by the Chief of Staff (spec-critic's findings, 2026-11-18)
- CLI scope: the user's request is the authority for the command; the PR names `validate` in
  AGENTS.md's CLI scope among "a few tools" (a planning-folder check the surface would otherwise
  keep in its own drifting script). No token measure is owed.
- Exit codes: gaps exit 0 (they pass; the first line still gives their count), errors exit 3,
  the command's own failures 1. Exit 2 is no longer used by `validate`, so an argparse or uvx
  failure (2) never reads as a pass. This replaces the spec-writer's point 5.
- Field limits and schema: a `summary.json` over `summary set`'s limits, with a bad label or a
  schema other than 1 is a gap, not an error (in line with Q1); only unreadable JSON or a JSON
  the board's model cannot read is an error. In `6-trash` no closing hint is printed for a
  summary gap (the CLI refuses `summary set` there).
- Whole: the broken-link check stays in this CR (the user listed the five checks in one request).
