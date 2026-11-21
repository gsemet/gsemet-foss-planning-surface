# Downloaded CI artifacts stay out of the published plan

## Goal

Raw CI artifacts that a Driver, a debugger or a verifier downloads into a CR's `work/` folder are
never published by the surface server's writer, and never block it. Seen on 2026-11-20 in the
Studio project: about 360 files under `work/**/artifacts-<run id>/` (20 MB in one CR, paths up to
358 characters) made the writer's `git add` fail on Windows with "Filename too long", and the
blocked line named neither a usable file nor what to do.

Three things change:

1. The cards send a downloaded CI artifact to `<CR folder>/work/scratch/artifacts-<run id>/`
   (already ignored).
2. The planning folder's managed `.gitignore` also ignores `**/work/**/artifacts-*/`, for an agent
   that misses the rule.
3. When `git add` fails on a path too long, the writer's blocked line names the file and the rule.

All paths below are relative to the repository root; `src/` stands for
`skills/chantier/scripts/cli/src/chantier/`, `tests/` for `skills/chantier/scripts/cli/tests/`.

## What changes

### A. The managed `.gitignore` (`src/core/files.py`)

- `IGNORED` gains one line, `**/work/**/artifacts-*/`, next to `**/work/scratch/`. Nothing else in
  the tuple changes. (Q1)
- `ensure_gitignore` is unchanged: it already adds a missing line to an existing `.gitignore` at
  the next command that writes in the planning folder, so every existing planning folder gets the
  line with no migration. (Q8)

### B. The CLI's own reading of the patterns (`src/store/base.py`)

- `_matches` reads a `**` name inside a pattern as zero or more folders, as git does. Today it
  takes `**/` only at a pattern's start, and `fnmatchcase` would read a middle `**` as exactly one
  folder. With the change, `is_published` (and so `PlanStore.published`, `store/folder.py` and
  `store/surface.py`) answers as git does for the new line. (Q2)
- What it must answer, `rel` relative to the planning folder:

  | `rel` | published |
  |---|---|
  | `3-ready/x/work/artifacts-1/a.txt` | no |
  | `3-ready/x/work/debugger/artifacts-99/deep/a.bin` | no |
  | `4-batch/x/work/a/b/artifacts-7/x` | no |
  | `3-ready/x/work/artifacts-1/` (a folder) | no |
  | `3-ready/x/work/artifacts-1` (a file of that name) | yes |
  | `3-ready/x/work/artifacts.md` | yes |
  | `3-ready/x/evidence/artifacts-1/a.txt` | yes |
  | `3-ready/x/artifacts-1/a.txt` | yes |

- Every pattern already in `IGNORED` keeps its present answers.

### C. The writer's blocked line for a path too long (`src/writer/`, `src/hub/schemas.py`)

- A new blocked reason, `path-too-long`. `SyncBlocked1.reason` is a free string
  (`src/hub/schemas_sync.py`): no new event type, no change to `src/hub/schemas.json`. (Q5)
- Recognition (`src/writer/git_ops.py`, beside `network_failure` and `refused`): a failed
  `git add` whose message holds `Filename too long` (git for Windows) or `File name too long`
  (Linux, macOS), and from which the path git quotes can be read (`open("<path>")`, or
  `unable to index file '<path>'`). The messages are read under `LC_ALL=C`, as the writer's other
  readings of git's text. A failed `git add` with neither phrase, or with no path to read, stays a
  `git-error` with git's text, exactly as today. The writer measures no path itself and has no
  length limit of its own: git decides. (Q6)
- It is a failed git step, handled by the same machinery as `git-error` (`Writer._failed`,
  `_finish`, `_block_git_error` in `src/writer/cycle.py`): the failure is remembered, the step is
  retried at each cycle, the state is `blocked` at the second cycle in a row
  (`CYCLES_TO_BLOCK`), one `sync-blocked@1` line per episode, and `sync-resumed@1`
  (`after: blocked`) when a cycle next completes its git steps. Only the reason, the text and the
  line's audience differ. `Writer._preconditions` must not tell `sync-resumed@1` for it either:
  where it excludes `GIT_ERROR` today, it excludes both failed-step reasons. (Q5)
- The text (the `text` of the `writer` entry in `chantier/server.json` and of the
  `sync-blocked@1` line), at most `TEXT_MAX` (200) characters:
  `<n> characters: <path>` where `<n>` is the length of the absolute path (the surface's root
  joined with the path git names) and `<path>` is the path as git names it, relative to the
  surface's root, whole when it is at most 150 characters, else its first 150 characters followed
  by `...`. The start is kept because it names the project, the CR and the folder to move.
- The audience of the `sync-blocked@1` line: the projects that hold the path (`self._holding`),
  else those with a seat, as the preconditions' lines do.
- The way out, a new entry of `WAY_OUT` in `src/hub/schemas.py`:

  ```
  "path-too-long": (
      "move it, or the folder that holds it, under its CR's `work/scratch/` (downloaded CI "
      "artifacts go there, never published), or shorten it; the next cycle that completes "
      "its git steps ends it (`sync now` runs one at once)"
  ),
  ```

  `_blocked` (`src/writer/lines.py`), `sync_blocked_text` (`src/hub/schemas.py`) and
  `src/board/command.py` read `WAY_OUT` by reason and need no other change. The line then reads:

  ```
  writer: blocked (path-too-long): 358 characters: projects/studio/changes/4-batch/...; for the Chief of Staff: move it, or the folder that holds it, under its CR's `work/scratch/` (downloaded CI artifacts go there, never published), or shorten it; the next cycle that completes its git steps ends it (`sync now` runs one at once)
  ```

- The writer's git commands stay those `AGENTS.md` lists: no new command, no `git config`, no
  `git rm`, nothing moved or deleted by the CLI. (Q7)

### D. The cards (`skills/chantier/references/`)

Cards only; `agents/` and `com.github.copilot/agents/` do not change. (Q3, Q4)

- `driver.md`, "Means: the record and the workers", the "Logs" bullet, gains:
  "A CI artifact you download (`gh run download`, `glab job artifact`, or the forge's equivalent)
  goes under `<CR folder>/work/scratch/artifacts-<run id>/`, never elsewhere in the CR's folder:
  it stays on this machine, never published. What proves a claim is copied from it, small, into
  `evidence/`. A brief that asks a `debugger` or a `verifier` to read an artifact names that
  folder."
  The "a CI failure" bullets (`gh run view <run> --log-failed > <work folder>/ci-<run>.log`, in
  "Means: context and your folder" and "Means: CI beside the long gate") stay as they are: a
  `*.log` file is already ignored.
- `debugger.md`, the bullet "Keep your notes in `<work folder>/debugger/` ...", gains:
  "A CI artifact you download goes under `<CR folder>/work/scratch/artifacts-<run id>/`, never
  under `<work folder>/debugger/` or `evidence/`: it stays on this machine, never published; copy
  into `evidence/` only the small part that proves your finding."
- `verifier.md`, the bullet "Keep your notes in `<work folder>/verifier/` ...", gains the same
  sentence with its own folder: "A CI artifact you download goes under the `scratch:` folder
  (`<CR folder>/work/scratch/artifacts-<run id>/`), never under `<work folder>/verifier/` or
  `evidence/`: it stays on this machine, never published; copy into your evidence only the small
  part that proves a claim." Its existing rules for the scratch folder (inside its writes, a path
  too long for Windows is a stop) apply unchanged.
- `concepts.md`: the two sentences that list what stays out of git say it too. In "A CR's folder
  holds its work" ("Kept out by design: ..."): after "a Verifier's scratch project stays in
  `work/scratch/`", add "a downloaded CI artifact stays in `work/scratch/artifacts-<run id>/`".
  In "Planning folder": after "the Verifier's scratch folder (`work/scratch/`)", add "and any
  `artifacts-*/` folder under a `work/` folder".
- The cards must keep `tests/test_startup_manifest.py` green (the startup limit); none of the
  passages above is in a "Startup core" section.

### E. The docs

- `docs/planning-folder.md` ("What is published and what stays local") and
  `docs/planning-modes.md` ("What stays local, what is pushed"): add to the list of what git
  ignores "the scratch folder (`work/scratch/`) and downloaded CI artifacts (any `artifacts-*/`
  folder under a `work/` folder)".
- `docs/planning-folder.md`, in the same paragraph, after the sentence on the writer: "A path too
  long for git blocks the writer with the reason `path-too-long`; its line names the file and the
  way out."

## Decisions carried from `02-answers.md`

| | Decision | Where |
|---|---|---|
| Q1 | The pattern is `**/work/**/artifacts-*/`, nothing wider | A |
| Q2 | `_matches` reads a middle `**` as git does | B |
| Q3 | Downloads go to `<CR folder>/work/scratch/artifacts-<run id>/`; proof is copied small into `evidence/`; the failed-jobs log keeps its place | D |
| Q4 | Cards changed: `driver.md`, `debugger.md`, `verifier.md`, two sentences of `concepts.md`; two docs pages; not the investigator, the coder or the inspector | D, E |
| Q5 | Reason `path-too-long`, a failed git step like `git-error`: length and start of the path in the text, the rule in the way out | C |
| Q6 | The file is read from git's message; no path to read stays `git-error`; no length check by the CLI | C |
| Q7 | No `core.longpaths`, no untracking, no folder moved by the CLI | C, Out of scope |
| Q8 | Existing planning folders get the line through `ensure_gitignore` | A |
| Q9 | Nothing split out | - |

## Out of scope

- Setting `core.longpaths`, or any git configuration, in a surface.
- Untracking or deleting artifacts a surface already committed, and moving a folder to
  `work/scratch/`: by hand, as Studio did. Removing Studio's line from the surface's
  `.git/info/exclude` is also by hand, once the managed line is there.
- Removing downloaded artifacts at a CR's or a batch's end (they stay local, ignored).
- A size limit on what a CR publishes, and a path-length check in `validate` or before `git add`.
- The investigator's, the coder's and the inspector's cards.
- The web client: it shows the writer's line as given, with no change of its own.
- No new CLI command, no new journal type, no change to `AGENTS.md` (the list of what chantier
  writes and of the writer's git commands holds as written).

## Evidence

No CI job is added or changed. No host or shipped-default dependency: no matrix. The one
dependency is the system, for C: git refuses a long path on Windows with `core.longpaths` unset
or false (the limit is 260 characters); on Linux and macOS the path of the test is not too long.

Checks (`tests/`, in-process, few and parametrized, as the project's rules ask):

1. `tests/test_store_conformance.py`, `test_published_agrees_with_the_ignored_files`: extended
   with the rows of B's table, for both stores.
2. Agreement with git, one test: in a temporary git repository, the `.gitignore` as
   `ensure_gitignore` writes it (the shipped `IGNORED`, not a text the test prepares), then for
   each row of B's table and one row per kind of older pattern (`seat.json`,
   `4-batch/batch.json`, `3-ready/x/work/gates/a.md`, `3-ready/x/work/scratch/a`,
   `3-ready/x/01-intent.md`), `git check-ignore` and `is_published` give the same answer.
3. The writer leaves the folder out (`tests/test_writer_edges.py`, with `tests/writer_rig.py`):
   a file written under `projects/demo/changes/1-inbox/idea/work/debugger/artifacts-123/` beside
   a published `01-intent.md`; after the cycle the state is `synced`, the commit holds
   `01-intent.md` and no path under `artifacts-123/`.
4. Recognition, one parametrized test on prepared git messages (a prepared text, named as such:
   a refusal no shipped file can hold): the Windows message
   (`error: open("<path>"): Filename too long`, then `error: unable to index file '<path>'`, then
   `fatal: adding files failed`), the POSIX spelling, a message with the phrase and no path, and
   another git error; the first two give the path, the last two give none.
5. The real refusal, one test that runs on Windows only (`sys.platform == "win32"`, skipped
   elsewhere; it runs in the `just check (windows-latest)` job and on the Driver's own Windows
   machine): in the rig's surface, `git config core.longpaths false` (local to the rig's
   repository: a CI runner's system configuration may set it true), a file whose absolute path is
   above 300 characters, created through Windows' extended-length path prefix (`\\?\`) under a
   folder that is not ignored (for instance `.../1-inbox/idea/work/notes/...`); two cycles:
   `pending` with `failure.cycles == 1` and no journal line, then `blocked` with reason
   `path-too-long`, a text that starts with
   `<n> characters: projects/demo/changes/1-inbox/idea/work/notes/` and is at most 200
   characters; a third cycle adds no second `sync-blocked@1`; the file removed (through the same
   prefix), the next cycle is `synced` and tells one `sync-resumed@1` with `after: blocked`. This
   test proves git's real message against check 4's prepared one: if the real text differs, the
   recognition follows the real text and check 4's sample is corrected. Its first run on
   `windows-latest` is what proves it there; the Driver runs it on Windows before the push and
   quotes its output in the PR.
6. The lines (`tests/test_writer_lines.py`): `state_line` for a blocked entry of reason
   `path-too-long`, and `sync_blocked_text` for the same payload, each hold the text and the way
   out with `work/scratch/`; `git-error`'s lines are unchanged.
7. The cards, one parametrized test that reads `driver.md`, `debugger.md` and `verifier.md` from
   the repository as shipped, at the head under test: each holds
   `work/scratch/artifacts-<run id>/`.

Gates:

- `just check` in the worktree at the rebased head, before the first push; `just eval-dry-run`
  too (the change is under the CLI's `src/`).
- The long gate: the pipeline's `just scenario (ubuntu-latest)` job, green at the PR's head. No
  scenario step is added: the scenario's own checks of the `.gitignore` must stay green.
- No `just mod` (nothing under `hooks/` or `types/`), no pane screenshot, no web client change.

Known limit, to state in the PR if it holds: whether the writer's
`git status --untracked-files=all` on Windows lists a too-long untracked path (so that it reaches
`git add`) is proved only by check 5. If check 5 shows the cycle never reaches `git add` for such
a path, the Driver reports what git does instead, with its text, and hands the point back rather
than measuring paths in the CLI.

## Open questions

None.
