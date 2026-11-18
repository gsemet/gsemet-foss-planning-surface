# Change Specification: the planning folder ignores every CR's work/gates/

## Goal

A raw log a role keeps in `<CR folder>/work/gates/` must never be published with the planning
surface. Today it is: the planning folder's `.gitignore` holds `work/gates/`, and git anchors a
pattern with a slash in the middle to the `.gitignore`'s own folder, so it only matches
`<planning folder>/work/gates/`, a folder that never exists. A CR's `work/gates/out.txt` is not
ignored (checked on this machine's planning surface on 2026-11-18: `git check-ignore` matches
`work/gates/x.log` only through `*.log`, and does not match `work/gates/out.txt`). CR-328 (PR 287)
found it and wrote its own new entry as `**/work/scratch/`. This CR fixes `work/gates/` the same
way and checks the rest of the list.

## What changes

### The CLI: `skills/chantier/scripts/cli/src/chantier/core/files.py`

- In `IGNORED`, the entry `"work/gates/"` becomes `"**/work/gates/"`. Nothing else in the tuple
  changes (see the sweep below).
- `ensure_gitignore` stays as it is. It appends every `IGNORED` entry missing from the existing
  file line by line, so an existing planning folder whose `.gitignore` holds the old `work/gates/`
  line gets `**/work/gates/` appended at the next CLI call that runs `ensure_gitignore` (any
  non-read-only `Repo` open, `init`, intake, a batch's open). The old `work/gates/` line stays: it
  is harmless, and the CLI removes no line from that file. No migration code is added.

### The sweep (decision of `02-answers.md`)

Every other `IGNORED` entry with a slash in the middle and no leading `**/` was checked:

- `/4-batch/batch.json`, `/4-batch/events.jsonl`, `/4-batch/brief.md`: anchored on purpose
  with a leading `/`. These files live only at `<planning folder>/4-batch/`, so they are correct
  as they are.
- `.long-gate.queue/`: the only slash is the trailing one, so git matches it at any depth. It is
  correct as it is.
- `**/work/scratch/`: already fixed by CR-328.
- Every other entry has no slash and matches at any depth.

So `work/gates/` is the only entry with this bug, and the only line that changes. If the Driver
finds an entry added to `IGNORED` after this spec was written that has a slash in the middle and
no leading `/` or `**/`, it fixes that entry the same way in this CR and says so in its delivery.

### The scenario: `scenario/run_scenario.py`

- The check "`init` makes the planning folder and its .gitignore of local files" (around line
  8331) tests `"work/gates/" in ignore` as a substring, which `**/work/gates/` would also pass.
  It becomes a line check: `"**/work/gates/" in ignore.splitlines()`.
- The same step adds a check that git ignores a log under a CR's folder: `git check-ignore -q
  --no-index <planning folder>/2-backlog/P1/<any CR>/work/gates/out.txt`, run in the surface,
  must exit 0. The file name has no `.log` or `.tmp` suffix, so only the fixed entry can match it.
  The path does not need to exist.
- `surface_publishes`'s filter (`"/work/gates/" in f`, around line 8103) stays: it is the
  scenario's own list of local files, not the shipped pattern.

### Tests: `skills/chantier/scripts/cli/tests/test_driver_prompt.py`

Change the existing test
`test_the_planning_folder_ignores_a_scratch_project_and_a_call_there_leaves_the_live_one_alone`
(or parametrize its first half over `scratch` and `gates`), so that it also asserts:

- `"**/work/gates/"` is a line of the `.gitignore` the CLI wrote in the test's planning folder;
- `git check-ignore -q` exits 0 on a file named without a log suffix (for example
  `out.txt`) under `<planning folder>/4-batch/2-actives/101-one/work/gates/`.

Add one more case, in the same file or a neighbouring one, for an existing planning folder
whose `.gitignore` predates the fix. The test writes a `.gitignore` holding the old `work/gates/`
line and not `**/work/gates/`. This prepared text is for a case the shipped default cannot hold:
an existing folder written by an older CLI. The test then runs one CLI command that opens the
repository for writing and asserts:

- `**/work/gates/` is now a line of the file, once;
- the old `work/gates/` line is still there;
- `git check-ignore` matches a file under a CR's `work/gates/`.

`ensure_gitignore` caches the folders it has done in `files._ignored_done` per process. The test
must not depend on an earlier call having filled that cache: it uses a fresh folder or clears that
cache for its own path. Both cases read the `.gitignore` the CLI actually writes from `IGNORED` as
it ships at the head under test, not a copy of it.

Keep `just test` within its budget (AGENTS.md): no new fixture, and at most one new test
function.

## Out of scope

- The prose that names the folder (`work/gates/` in `concepts.md`, `driver.md`, `coder.md`,
  `verifier.md`, `debugger.md`, `investigator.md`, `conflict-resolver.md`, `docs/planning-folder.md`,
  `docs/planning-modes*.md`, `docs/planning-modes.svg`). There it names a folder inside a CR's
  folder, which is correct, not a git pattern, so it is left as it is.
- Removing the old `work/gates/` line from existing `.gitignore` files.
- Any file already published under a CR's `work/gates/` in a planning surface: this CR stops new
  ones from being published. It does not clean the history or remove tracked files (git keeps
  tracking a file that was committed before it was ignored).
- Any other change to `IGNORED` or `ensure_gitignore`.

## Evidence

- `just check` passes (lint, types, `just test` with the changed and added tests).
- `just eval-dry-run` passes in the worktree, since the change is under the CLI's `src/`
  (AGENTS.md).
- `just scenario` is green at the PR's head on the pipeline's `just scenario (ubuntu-latest)` job,
  with the changed init check and the new `git check-ignore` check passing.
- There is no host or default/configured matrix: git applies ignore patterns the same way on Linux,
  macOS and Windows, and the `.gitignore` is the same in-project and with an external surface.
  No configuration value changes it.
- No CI job is added or changed.

## Open questions

None.
