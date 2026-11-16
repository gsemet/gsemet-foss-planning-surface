# Change Specification: a green long gate on main, and no backward compatibility

Origin: verbal (the user, 2026-11-14). No tracker issue.

Grill: `1-inbox/fast-scenario/02-answers.md` (Scen-Q1, Scen-Q5, Scen-Q6 and the user's words
"pas besoin de backward compatibilité on est encore en PoC"), then this CR's `02-answers.md`
(BL-Q1, BL-Q2). Analysis: `1-inbox/fast-scenario/analysis/scenario-analysis.md` (section F and the
legacy rows of A.2) and `analysis/fable-advice.md`. This is the first of three CRs
(`baseline-and-legacy`, then `fast-scenario`, then `gate-rules`). It holds no part of the other two.

## Goal

Two things, in the user's terms:

1. **The long gate passes on main again.** From about 12:50 on 2026-11-14, batch-17's PRs were
   merged without the local long gate (GitHub CI green was accepted in its place). Run it on main
   on the user's Windows machine, GitHub and GitLab, and fix what fails. This green run is also the
   baseline `fast-scenario` needs, to show that its restructure loses no coverage.
2. **No backward compatibility: chantier is still a PoC.** The planning folders on disk are
   migrated once, by a script that is not kept, and the CLI drops every reader of an older format,
   with the scenario cases that guard them. The docs stop promising the conversion of an older tree.

Done when the long gate passes on main on Windows for both forges, the CLI reads both planning
folders (this project's `.agents/changes/` and the surface
`C:\Users\gaeta\Projets\gsemet-foss-planning-surface`) with no conversion code left, and the
surface's own validator places its CRs in the renamed folders (BL-Q1).

## The order of the work

The order matters: each step's proof is taken before the next step changes anything.

1. The long gate at main's head, and its fixes (Part A).
2. The one-off migration on both planning folders, with the surface's two stage-name edits, and
   the surface's autosync commit of them (Part B).
3. A snapshot of both folders, read by the current CLI: the "before" outputs (Part C).
4. The legacy readers and their scenario cases removed (Parts D and E), the docs (Part F).
5. The same snapshot read by the new CLI: the "after" outputs, compared with the "before" (Part C).
6. `just check`, then `just scenario` at the PR's head (Evidence).

## Part A: the long gate at main's head

- In the CR's worktree, at `origin/main`'s head before the CR's first commit, run `just check`
  then `just scenario` (both forges: the recipe runs `scenario/run_scenario.py --forge github`
  then `--forge gitlab`) on the user's Windows machine. Record main's SHA (seven characters) and
  each result.
- Fix each failure **one commit per cause**, each commit naming the failing check and its cause.
  Then run the long gate again, until it is green at the CR's head with the fixes alone (before
  Part D starts).
- A failure inside a scenario case this CR removes (`old_words`, `old_tree`, `backfill_cases`,
  `release_on_stack` section 15) is recorded and not fixed: its removal is its fix.
- A failure whose fix changes what chantier does for its user (not a bug against the cards, the
  README or the scenario's README) is not the Driver's to decide: it stops and asks, through the
  Foreman, with the failing check and the choices.
- No change to the gate rules (queue order, early push, clean rebase, stack waiver): those are
  `gate-rules`. No change to the scenario's structure, runner or timings: those are `fast-scenario`.

## Part B: the one-off migration

### Where the script lives

The script is written and run from the CR's work folder while the CR runs:
`4-batch/2-actives/<number>-baseline-and-legacy/work/migrate-legacy.py`, a PEP 723 script with no
dependency (`uv run --script <path> <planning folder>...`). It is never added to the CLI, the
repository, `scripts/` or the scenario, and it is not in the PR. It is not kept after the CR:
`work/` stays out of the archive's cleaned copy. Its outputs go to the CR's `evidence/migration/`
(below), which the archive keeps.

The script is plain Python, UTF-8 everywhere (`encoding="utf-8"` on every read and write), uses
`pathlib` only, and runs the same on Windows and POSIX. It does no git write: no `git add`,
`git mv`, commit or push. Its renames are plain file-system renames, which git sees as moves.

It has two modes: `--dry-run` (prints what it would change, writes nothing) and the real run.
It is idempotent: a second real run prints that there is nothing to do, and changes nothing.

### What it refuses (exit non-zero, nothing written)

- In a chantier planning folder: a `3-requests/` or `4-archives/` folder, or a `5-trash/` folder
  that holds anything but `.gitkeep`; any `batch.json` whose `status` is `open` or `landed`
  (none today). The running batch of this very CR is no refusal: its `batch.json` uses the current
  words, and the script never touches `4-batch/`.
- An old batch id in a `STATUS.json` that the records' map does not name.
- On the surface: a rename source that holds anything but `.gitkeep` files and empty folders, or a
  rename target that already exists with files in it; and uncommitted changes (`git status
  --porcelain`) under a path it would rename.

### This project's planning folder (`C:\Users\gaeta\Projets\chantier\.agents\changes`)

- **Rewrite the archived `STATUS.json` files that carry an old batch id** (Scen-Q6). The map comes
  from the records, `5-archives/batches/batch-NN.json`: each record whose `backfill.former_id` is
  set maps that id to its `batch` value. Today, five entries: `01-eval-real` -> `batch-01`,
  `02-eval-heavy` -> `batch-02`, `03-eval-real-050` -> `batch-03`, `04-cr-board` -> `batch-04`,
  `05-batch-folder` -> `batch-05`.
- Only the files at `5-archives/<cr folder>/STATUS.json` and `6-trash/<cr folder>/STATUS.json`
  (one level, a CR's own STATUS) are read. Today, 14 match: 10 in `5-archives` (CR-101, 106, 107,
  108, 109, 110, 111, 112, 113, 114) and 4 in `6-trash` (CR-102 to 105, all `02-eval-heavy`).
- Only the `batch` value changes. The edit replaces that one value in the text, so each file's diff
  is one line; the rest of the file stays byte for byte (no re-dump of the JSON). `STATUS.md`
  files are not touched.
- The records keep their `backfill` object, `former_id` included, as the trace (Scen-Q6). The
  script writes nothing in `5-archives/batches/`.
- This one-off write of archived `STATUS.json` files is the user's own decision (Scen-Q6): the
  cards' "the CLI writes them, never by hand" still holds for every other write.
- The planning folder is untracked in the chantier repository (`git status` shows `?? .agents/`):
  there is no commit to make. The proof is the evidence files.

**The stray capture, looked at by hand.** The intake names `5-archives/work/captures`. Its real
path is `5-archives/261107-1906-152-release-0-8-0/work/captures/`: a set of captures (HTML, PNG,
`status.txt`, `batch-STATUS.md`) in CR-152's work folder, with a `STATUS.json` whose `batch` is
empty. It is a capture, not a CR's STATUS, and the script's one-level rule skips it. The Driver
checks that `status`, `cost` and the board's state ignore it (no CR row, no warning), writes what
it found in `evidence/migration/captures.md` (three lines), and changes nothing there. If one of
those reads does show it, that is a question for the user, not a fix.

### The planning surface (`C:\Users\gaeta\Projets\gsemet-foss-planning-surface`)

There are no chantier records there to migrate (no `batch.json`, no `5-archives/batches/`, no
`STATUS.json` with an old id). The script renames the old, empty stage folders of its four
projects to chantier's layout (`3-ready`, `4-batch/{1-pending,2-actives,3-done}`, `5-archives`,
`6-trash`; `lifecycle/stages.py` `stage_layout`). Only the inboxes hold files; they do not move.

| Project (`projects/<name>/changes/`) | Renames |
|---|---|
| `agentic-planning-surface` | `3-batches/` -> `4-batch/` (with its `1-pending`, `2-actives`, `3-done` and `.gitkeep`); `4-archive/` -> `5-archives/`; `5-trash/` -> `6-trash/` |
| `chantier` | `3-stash/` -> `3-ready/`; `4-batches/` -> `4-batch/` (with its three state folders) |
| `markdown-okf-schema-studio` | the same as `chantier` |
| `okf-schema` | the same as `chantier` |

- The `.gitkeep` files move with their folders. The script creates no other folder (no `3-ready`
  or `P1`..`P4` where none exists): the CLI makes the stage folders it needs.
- The rename of `agentic-planning-surface`'s `5-trash/` also ends a live hazard: today
  `old_tree()` (`lifecycle/convert.py`) returns true on that folder, so the first chantier command
  on that project would "convert" it. **Until the migration has run there, no chantier command
  runs on that project** (the intake's rule), not even the verify step.

**The surface's own stage names follow the renames (BL-Q1).** In the same window as the renames,
the Driver edits two files of the surface by hand, so its validator places the CRs moved into the
renamed folders:

- `AGENTS.md` l.44-46 ("Stage and priority come from the folder"): `3-stash` becomes `3-ready`,
  `4-batches/1-pending` becomes `4-batch/1-pending`; the rest of the sentence (`2-actives`,
  `3-done`, `5-archives`, `6-trash`) stays.
- `scripts/validate-bundles.py`, `STAGES`: the key `3-stash` becomes `3-ready` (its stage label
  `ready`), and the three `4-batches/...` keys become `4-batch/1-pending`, `4-batch/2-actives`,
  `4-batch/3-done` (labels unchanged). No other line of the script changes.
- A search of the surface outside `projects/` (`README.md`, `justfile`, `tests/`, `_schemas/`,
  `.agents/`) for `3-stash`, `4-batches`, `3-batches`, `4-archive`, `5-trash` found nothing else
  today; the Driver runs it again after its edits and it finds nothing.

**Who commits the surface's changes (BL-Q2).** The surface's autosync does: its own commit carries
the renames and the two edits. No session commits or pushes the surface by hand
(`concepts.md`, "Planning surface"), and a Driver never joins the autosync group.

- After the script's real run and the two edits, the Driver checks
  `git -C <surface> status --porcelain -- projects/*/changes AGENTS.md scripts/validate-bundles.py`
  until it is empty and `git -C <surface> log` shows the autosync commit carrying them.
- If the autosync is stopped or blocked (the changes stay uncommitted), the Driver does not commit
  them: it waits, and says so in its hand-back (what is uncommitted, since when). The Chief of
  Staff restarts the autosync on the user's yes. No commit by hand, in any role.
- Part C's snapshot is taken only once the surface's changes are committed, so both CLI runs read
  the committed layout.

### What proves the migration ran, on both folders

In the CR's `evidence/migration/`:

- `chantier-run.txt`: the script's output on `.agents/changes/`: the map it read, then one line
  per file changed (`<path>: <old id> -> batch-NN`), 14 lines, then the count. Then the output of a
  second real run: nothing to do.
- `surface-run.txt`: the same for the surface: one line per rename (9 renames), then a second
  run's "nothing to do".
- `scan.txt`: a scan after the run, by the script, of both folders: no `STATUS.json` (at a CR's
  level) names a batch outside `batch-NN`; no `crs[].path` or `archive` value in any `batch.json`
  or record starts with `.agents/changes/`; no folder `3-requests`, `4-archives`, `5-trash`,
  `3-stash`, `4-batches`, `3-batches` or `4-archive` in any planning folder of the two.
- `surface-git.txt`: `git -C <surface> log --stat` of the autosync commit(s) carrying the renames
  and the two edits (`AGENTS.md`, `scripts/validate-bundles.py`), and the `git status --porcelain`
  above empty after them.
- `surface-validate.txt`: `just validate` run at the surface's root after that commit: every CR
  is placed in a stage, with no "not in a stage folder" line. A failure with another cause (the
  surface's own bundles or schemas) is recorded there and not fixed: it is the surface's business.

## Part C: the CLI reads everything, before and after the removal

The comparison runs on **one snapshot per planning folder**, taken after the migration (and, for
the surface, after its autosync commit), so both runs read the same files whatever the live batch
does in between:

- Copy each planning folder into a temporary folder outside both repositories (the session's
  scratch or `%TEMP%`), each in a fresh `git init` repository with the same layout:
  `<tmp>/chantier-snap/.agents/changes/` for this project; for the surface,
  `<tmp>/surface-snap/` with `projects/<name>/changes/` and each `projects/<name>/project.md` and
  `checkout.yml`, without the surface's `AGENTS.md` and `scripts/`, so no autosync is seen. In
  this project's copy, leave out the live batch's own files (`batch.json`, `events.jsonl`,
  `brief.md`, locks, `seat.json`, `STATUS.*` at the root) and the content of `4-batch/`, so the
  snapshot holds no running batch.
- Read each snapshot with **main's CLI** (before Part D), then with **the PR head's CLI** (after
  Part D), each time with `uv run --locked --project <the checkout> chantier`:
  - `status` (this project's snapshot says `last closed: batch-17`);
  - `cost --batch batch-17` (this project's snapshot);
  - for each surface project, `--project <snapshot>/projects/<name> status`;
  - the board's state of each project: `chantier.board.state.project_state(<id>, Repo.find(...),
    <surface>, None)` called in-process, or `GET /api/projects/<id>/state` from a `chantier board`
    started on the snapshot; the time fields (`now` and any read time) are removed before saving.
- Save each output to `evidence/migration/verify-before-<folder>.txt` and
  `verify-after-<folder>.txt`, stdout and stderr both.
- **What must hold:** no stderr line `converted .agents/changes...` or
  `backfilled 5-archives/batches...` in the "before" run (the readers were already no-ops on the
  migrated data); and the "after" output identical to the "before" output, but for one expected
  difference: a record with no close date now reads `(no close date)` where it read
  `(backfilled, no close date)` (Part D, `history.py`), which only shows if such a record is the
  last closed one. Any other difference is a defect to fix before the PR.

## Part D: the legacy readers removed

All paths are under `skills/chantier/scripts/cli/src/chantier/`. `lifecycle_regressions` is not
legacy (it guards `open --remote`'s check and the write-scope rule): it stays.

- **Old tree conversion.** Delete `lifecycle/convert.py` whole (`old_tree`, `convert_old_tree`,
  its helpers, its private index write, and `open_repo`).
  - `open_repo` becomes `Repo.find` for its importers: each `from chantier.lifecycle.convert
    import open_repo` and each `open_repo(...)` call becomes `Repo.find(...)` from
    `chantier.core.repo`, with the same arguments (`preflight.py`'s `_open_project` keeps
    `Repo.find(Path(os.getcwd()))`). The importers: `commands/batch_status.py`, `closing.py`,
    `cost/command.py`, `delivery.py`, `driver.py`, `facts.py`, `forge_stack.py`, `gate.py`,
    `intake.py`, `opening.py`, `orders.py`, `preflight.py`, `release.py`, `rules.py`, `seat.py`,
    `summary.py`.
  - `commands/intake.py` `init`: drop the `convert_old_tree(repo)` call and its import.
  - `lifecycle/stages.py`: `_relocate` loses the `3-requests` cleanup (the `old = ...` line and
    the loop that removes emptied folders under it); `start_cr`'s docstring loses "or still at the
    path of an older tree".
  - `core/repo.py`: `Repo.find`'s docstring loses its last sentence on the old tree and
    `open_repo`.
- **Records backfill.** Delete `lifecycle/backfill.py` whole. `core/batch_records.py`
  `blank_record` loses its `"backfill": None` key (new records no longer carry it; the records on
  disk keep theirs as data, read as plain dicts). `history.py` `last_closed_text`: the text for a
  record with no close date becomes ` (no close date)` (analysis F.1).
- **Old batch status words.** `core/records.py`: delete `BatchRecord._old_words` (the
  `model_validator`) and the docstring's sentence on `open` and `landed`; drop `model_validator`
  from the imports if nothing else uses it.
- **`.agents/changes/`-prefixed record paths.** `core/repo.py` `planning_path`: drop the prefix
  strip and the docstring's "the older record's form, `.agents/changes/...`, still reads".
  `history.py` `archive_of`: drop `.removeprefix(".agents/changes/")`.
- **Kept on purpose.** `pr_draft` read as draft when absent (`core/records.py`, `stacks.py`): it
  is also the safe reading of a hand-edited record (analysis F.1); display strings that name
  `.agents/changes/` (`cli.py`'s help, `plugin_files.py`, `stages.py`'s archive line,
  `status/views.py`'s comment) are not readers.
- No change under `hooks/` or `types/`, so no `just mod`; no change to the pane's fields.

## Part E: the scenario

In `scenario/run_scenario.py`:

- Delete the cases `old_words` (l.5472), `old_tree` (l.5625) and `backfill_cases` (l.2684), their
  calls in the case sequence (l.1023, 1025, 1027), and any helper or fixture left with no caller.
- In `release_on_stack`, delete section 15, "a batch opened by the older CLI" (l.5373-5388, the
  `confirmed` check). The other `confirmed` checks (`release_last`, section 12) are about today's
  `order confirm` and stay.
- `World.at` (l.181-183): read `self.state / str(path)`, with no prefix strip, and its docstring
  without "the older `.agents/changes/` form reads too".
- `lifecycle_regressions` and `next_number` stay as they are (`next_number` moves to pytest in
  `fast-scenario`, not here). No other case moves, merges or shortens in this CR.

## Part F: the docs and cards

- `scenario/README.md`: remove "an older batch's `confirmed` giving no go;" (l.135-136), the
  bullet "an old batch: `batch.json` written by hand with `status: "landed"`..." (l.145-147), and
  "the backfill of the earlier batches, once;" (l.159-160), keeping each sentence around them whole.
- A search of the cards (`skills/chantier/references/`), `README.md`, `CONTRIBUTING.md`, `docs/`,
  `agents/` and `com.github.copilot/agents/` for `convert`, `backfill`, `older tree`, `old words`,
  `3-requests`, `4-archives` found no promise of a conversion today (the hits are unrelated:
  "converted to Markdown", a time zone note). The Driver runs the search again at its head and
  removes any line that promises it. Past release notes under `docs/release-notes/` are history and
  stay.

## Decisions carried from the grill

- Scen-Q1: the long gate on main and its fixes are part of this work (`long-gate-after-batch-17`,
  folded); its four gate rules go to `gate-rules` (Scen-Q5).
- Scen-Q5 (Fable's plan, taken whole): three CRs in order; this one holds the long gate on main
  and its fixes, the one-off migration, and the legacy readers removed with their scenario cases.
- Scen-Q6: the 14 archived `STATUS.json` files with old batch ids are rewritten to `batch-NN` by the
  migration script; the records keep `backfill.former_id` as the trace.
- The user: no backward compatibility, still a PoC.
- The intake (filed on the user's word): the script runs once and is never kept in the CLI; it
  renames the surface's old, empty stage folders; no chantier command on
  `agentic-planning-surface` until that has run; the stray capture is looked at by hand.
- BL-Q1: this CR also updates the surface's `AGENTS.md` (l.44-46) and
  `scripts/validate-bundles.py` (`STAGES`) to `3-ready` and `4-batch`, so its validator places the
  CRs moved into the renamed folders.
- BL-Q2: the surface's autosync commits its renames and edits. If it is stopped or blocked, the
  Driver waits and says so in its hand-back; the Chief of Staff restarts the autosync on the user's
  yes. No commit by hand.

## Out of scope

- The scenario's restructure: units, the parallel runner, the moves to pytest, the cut waits, the
  README's coverage contract, GitLab reduced, the step-0 timing run (`fast-scenario`).
- The four gate rules, their display in `status`, the pane and the board, `just mod`, the pane
  screenshot (`gate-rules`).
- `STATUS.md` text in the archives, the records' `backfill` objects, the `pr_draft` reading.
- Any change to the surface's own tooling beyond the folder renames and the two stage-name edits
  (BL-Q1); a failure of the surface's `just validate` with another cause.
- A CI job: none added or changed.

## Evidence

- `evidence/long-gate-main.md`: main's SHA, `just check` and `just scenario` (GitHub, GitLab) at
  that SHA on Windows, each failure with its cause and the SHA of the commit that fixes it, and the
  green run at the CR's head with the fixes alone. The full transcripts stay in
  `scenario/results/` (not committed); the evidence quotes each run's last summary lines.
- `evidence/migration/`: `chantier-run.txt`, `surface-run.txt`, `scan.txt`, `surface-git.txt`,
  `surface-validate.txt`, `captures.md`, and the `verify-before-*` / `verify-after-*` outputs with
  their comparison (Part C).
- The code is gone: a search of `skills/chantier/scripts/cli/src/` and `scenario/` for
  `open_repo`, `convert_old_tree`, `old_tree`, `backfill_history`, `_old_words`, `3-requests` and
  `removeprefix(".agents/changes/")` finds nothing, and `lifecycle/convert.py` and
  `lifecycle/backfill.py` no longer exist.
- At the PR's head: `just check` (Linux, macOS and Windows through CI; on Windows locally), then
  `just scenario` on the user's Windows machine, GitHub and GitLab, both green: a CLI and scenario
  change (`AGENTS.md`). Done is this long gate green on main after the merge, on Windows, both
  forges.

## Risks

- The long gate on main may fail for causes unrelated to legacy, of unknown size: each is its own
  commit, and one that needs a behaviour decision stops for the user (Part A).
- The surface's autosync may be stopped or blocked when the migration runs: the Driver then waits
  (BL-Q2), and the CR stalls until the user says yes to its restart. Part C cannot start before.
- Between the autosync committing the renames and the two edits (if it commits them apart), the
  surface's validator and its folders disagree for a moment; no CR sits in a renamed folder today,
  so nothing is misplaced.
- The Driver writes in a second repository (the surface) besides its worktree; if the host refuses
  that write, the Driver says so at once and does not work around it.
- A record path written in the `.agents/changes/...` form by hand after this CR no longer
  resolves; the scan shows none exist today.

## Open questions

None.
