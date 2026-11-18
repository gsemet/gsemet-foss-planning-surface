# Answers

The user asked no questions on this CR: what the user's behaviour still needs is listed at the end
of `03-change-spec.md`, for the Chief of Staff to take to the user.

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
