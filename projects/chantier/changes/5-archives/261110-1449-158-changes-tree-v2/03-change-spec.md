# The changes tree, version 2: 3-ready, 4-batches with three states, 5-archives, 6-trash

## Goal

Chantier adopts the tree of the user's planning surface (planning-repo answer 1, "Chantier adopte
la surface"). In the project, `.agents/changes/` becomes:

```text
.agents/changes/
├── 1-inbox/<slug>/                             filed, not prioritized
├── 2-backlog/P1…P4/<slug>/                     prioritized by the user
├── 3-ready/<slug>/                             waiting for the next batch, specified or automatable
├── 4-batches/                                  the project's one current batch
│   ├── batch.json, events.jsonl, brief.md, .lock, STATUS.md, STATUS.json   the batch's own files, local
│   ├── 1-pending/<number>-<slug>/              in the batch, not started (queued)
│   ├── 2-actives/<number>-<slug>/              taken by a Driver: working, ready or blocked
│   └── 3-done/<number>-<slug>/                 merged (a release CR: released), until `close`
├── 5-archives/<YYMMDD-HHMM>-<number>-<slug>/   merged, after `close` (time of the merge, UTC)
└── 6-trash/<YYMMDD-HHMM>-<slug or number-slug>/   dropped on the user's word
```

Today's tree is `1-inbox`, `2-backlog`, `3-requests/batch-<n>/`, `4-archives`, `5-trash`. This CR
changes the tree only: the external mode (`planning-repo`, which depends on this CR) reuses it
as it is; it adds no setting for it.

Model: `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/`, which has
`1-inbox`, `2-backlog/P1..P3`, `3-stash`, `4-batches/{1-pending,2-actives,3-done}`, `5-archives`,
`6-trash`. The surface's `3-stash` is chantier's `3-ready` (the user's choice at the closing of
the grill).

## Decisions carried (planning-repo `02-answers.md`, "Grill of 2026-11-10")

- **Answer 1:** chantier adopts the surface's tree, in both modes. This CR does the in-project mode;
  the external mode is `planning-repo`.
- **Answer 4:** a running batch's own files (`batch.json`, `events.jsonl`, its STATUS files) stay
  on the steering machine, never shared. Only the result (the archive, the final state) is shared.
- **Answer 6:** the split into three CRs; this one is the first, "the new tree".
- **Answer 7:** CR folder names keep chantier's number (`156-diagrams-modes-griller`). The surface's
  `<issue>-<slug>` is not adopted; a tracker issue, when there is one, is a link inside the CR
  (as today: `file` keeps the request as received, with its link).
- **Answer 8:** no migration command. Chantier's own planning stays in-project.
- **Answer 9:** `3-ready` holds CRs that wait for the next batch ("Prête à lancer").
- **Answer 10 and the restatement:** `1-pending`, `2-actives` and `3-done` are the states of the
  CRs inside the batch. The CR folders of the current batch sit directly under the state folder;
  there is no `batch-<n>` level; one batch at a time per project.
- **The closing:** the folder is named `3-ready`. The text keeps two meanings apart (next section).
- **Answer 5:** no OKF: no frontmatter, no `index.md`, no `.gitkeep` is written.

## Words: the 3-ready folder and a PR ready to merge

"Ready" already names a CR status (`handback <cr> ready`, `🔵 ready`) and "a PR ready to merge"
(`concepts.md`, Words). Every text this CR writes keeps them apart:

- the folder is always written **`3-ready`** (with its number, in code font) or "the `3-ready`
  folder", never "the ready CRs" or "ready" alone;
- a CR in it is **"waiting for the next batch"** (in `3-ready`); a CR handed back `ready` is "ready
  to merge" or "handed back ready" and sits in `4-batches/2-actives/`, never in `3-ready`;
- the Griller's optional line `[griller→chief-of-staff] <CR> ready, spec written` becomes
  `[griller→chief-of-staff] <slug> specified` (`griller.md`, "Telling the Chief of Staff", and the
  Griller row of `routing.md`);
- in `concepts.md`, Words, add one entry **"`3-ready`"** that says the above in two lines.

## What changes, behaviour by behaviour

The CLI is `skills/chantier/scripts/cli/src/chantier/`. A CR folder still moves, never copied, by
one rename each time, and a collision is refused (exit 3) rather than overwritten.

### The stage folders (`lifecycle.py`)

`stage_layout` returns the new folders: `inbox` `1-inbox`, `backlog` `2-backlog`, `ready`
`3-ready`, `batches` `4-batches`, `pending` `4-batches/1-pending`, `actives`
`4-batches/2-actives`, `done` `4-batches/3-done`, `archives` `5-archives`, `trash` `6-trash`. The
`requests` key goes. `Repo.batches` (`state.py`) becomes `4-batches/`.

### `init`

Creates `1-inbox`, `2-backlog`, `3-ready`, `4-batches/1-pending`, `4-batches/2-actives`,
`4-batches/3-done`, `5-archives`, `6-trash`, empty (no `.gitkeep`); one line per folder, `created`
or `exists` (8 lines, under the 10-line limit). Its help in `cli.py`: "create the empty stage
folders of .agents/changes/; changes nothing else". It writes no `.gitignore` (unchanged: the
`.gitignore` line for `.agents/changes/` stays the user's, explained by the tour).

### `file`, `triage`, `abandon`: the `3-ready` folder

- `file` is unchanged (to `1-inbox/<slug>/`).
- `triage <folder> --ready` (new flag, exclusive with `--priority`; one of them is required) moves
  an inbox or backlog item to `3-ready/<slug>/`, on the user's word only (the Chief of Staff or a
  Griller runs it). It does **not** require a specification: a CR with no `03-change-spec.md` may
  go to `3-ready`; that is the **automatable** mode, where the Driver works from the request
  alone. It is refused (exit 2, nothing moved) only when `3-ready` already holds that slug.
  Output: `triaged 3-ready/<slug>` (with the path shown as today). Help: "move an inbox or
  backlog CR to a priority of the backlog, or to 3-ready for the next batch".
- `triage <3-ready/slug> --priority Pn` moves it back to the backlog. `--ready` on an item already
  in `3-ready` exits 2 ("already in 3-ready").
- `abandon` accepts an item of `1-inbox`, `2-backlog/P<n>` or `3-ready`, and an unclaimed CR of
  `4-batches/1-pending` or `4-batches/2-actives` (today's "unclaimed active CR"), to
  `6-trash/<stamp>-<name>/`.
- A CR in `3-ready` keeps no priority: it is one flat set, the next batch's candidates.

### `open` and `order add`

- `prepared_cr` accepts a folder (or its specification) in `1-inbox`, `2-backlog/P<n>` or
  `3-ready`; the Chief of Staff's plan proposes the `3-ready` CRs first. A folder under
  `4-batches/` is refused as today ("already active").
- A CR from `1-inbox` or `2-backlog` still needs a non-empty `03-change-spec.md` (today's refusal,
  unchanged). A CR from `3-ready` without one is accepted (automatable): its recorded
  `specification` is `intake/request.md` (the request as received), its title the request's
  first line; `take`, `round` and `handoff` print that file as the specification. The refusals
  for an empty or non-UTF-8 specification apply to whichever file is recorded; the QA-report
  refusal (`qa-` folder) stays.
- `add_cr` moves the CR to `4-batches/1-pending/<number>-<slug>/`; `cr["path"]` records it. The
  number is chosen as today (`next_cr_number`), its roots being `5-archives`, `6-trash` and the
  three state folders.
- `open` writes `brief.md` in `4-batches/`. It still exits 2 while a batch is not closed
  (`check_no_open_batch` reads `4-batches/batch.json`).
- The batch keeps its number and id `batch-<n>` (in `batch.json`, `.batch-number`, the branch
  `chantier/batch-<n>/<cr>-<slug>`, the worktree `<repo>.worktrees/batch-<n>-<cr>`, the Foreman's
  title and every output). Only the folder level goes. `--batch` still takes `4` or `batch-04`: a
  number that is not the current batch's exits 2 ("unknown batch").
- `depends.json` is read as today. A slug is met when its CR is merged in the batch (in `3-done`)
  or archived as merged in `5-archives` (`archived_merged`).

### A CR's state moves its folder

| Status change | Command | Folder |
| --- | --- | --- |
| added, `queued` | `open`, `order add` | → `4-batches/1-pending/` |
| `queued` → `working` | `take` | `1-pending/` → `2-actives/`, before the facts are printed |
| `working` ↔ `ready`, `blocked`, back to `working` | `handback`, `take --note` | stays in `2-actives/` |
| `merged` (a release CR: released) | `order merged`, `handback <release> ready` (`archive_merged` in `rails.py`, `handback`) | `2-actives/` → `3-done/` |
| `cancelled` | `order drop`, `cancel` | → `6-trash/<stamp>-<number>-<slug>/` at once, as today |

A CR folder never moves while a Driver holds it: it moves at `take` before the Driver gets its
facts, and at the merge or the drop after it has ended (as today). Record the merge time in the
CR (for example `merged_at`) for the archive's name at `close`.

`order merged`'s line says "moved to 3-done" where it said "archived"; `handback` of a release CR
says "released, in 3-done".

### `pause` and `close`

- `pause` is unchanged; its `report:` line names `4-batches/STATUS.md`.
- `close` refuses as today, and also while `1-pending/` or `2-actives/` holds a folder ("nothing
  was deleted"). Without `--yes` it lists what goes: the batch's own files, and each `3-done` CR
  that moves to `5-archives`. With `--yes`: each `3-done/<number>-<slug>` moves to
  `5-archives/<YYMMDD-HHMM>-<number>-<slug>`, the date being the CR's merge time (UTC), so the
  archives keep the merge order (README: "time of the merge, UTC"); the final CR pages are written
  in `5-archives` and `6-trash` (`write_final_pages`, as today for the pages that outlive the
  batch); then the batch's own files are deleted (everything in `4-batches/` but the three state
  folders, which stay, empty). Same all-or-nothing care as today: the moves roll back on a
  failure, and the delete is a rename first.
- Output: `closed batch-<n>: its files are deleted, <k> CRs archived`.

### The batch's own files, local

`batch.json`, `events.jsonl`, `brief.md`, `.lock`, `STATUS.md`, `STATUS.json` and the Demo
explorer's `demo/` live at the root of `4-batches/`, beside the three state folders. In-project
they are local like the whole of `.agents/changes/`, which stays out of git (the `.gitignore`
line of the tour; `pr-template.md`: "`.agents/changes/` is not in git"). This CR writes no
`.gitignore`; keeping them out of a shared surface is `planning-repo`'s, which finds them under
these fixed names. Recommendation for the Driver: no other file at the root of `4-batches/`.

`.batch-number`, `.lifecycle.lock`, `.long-gate.lock` and `seat.json` stay at the root of
`.agents/changes/`.

### STATUS files and the CR board

- The index (today `3-requests/STATUS.md|json`) moves to the root: `.agents/changes/STATUS.md`
  and `STATUS.json`. The batch's page is `4-batches/STATUS.md|json`; a CR's
  page stays in its folder.
- Links: a CR of the batch links its batch as `../../STATUS.md`; the batch page's "All change
  requests" is `../STATUS.md`; the index links `4-batches/STATUS.md`. Every path in the index's
  JSON (`folder`, `status`, `specification`, `backlog[].path`, `merged[].path`,
  `trashed[].path`) is relative to `.agents/changes/`. `cr_view`'s `batch` and the batch page's
  title show the batch id (`batch-09`), not the folder name.
- The index's backlog table lists `3-ready` first, its Priority cell `3-ready`, then P1…P4, then
  the inbox. Its "merged" list holds the current batch's `3-done` CRs, newest first, before the
  `5-archives` ones; `merged_total` counts both.
- `status.SCHEMA` goes from 2 to 3 (a field's base changed). The board: `hooks/register.tsx`
  reads `.agents/changes/STATUS.json`, resolves CR folders from `.agents/changes/`, and reads
  schema 3; `types/index.d.ts` says "Relative to `.agents/changes/`" and names the index's path;
  `hooks/register.test.tsx` follows. `CONTRIBUTING.md` part 4 says schema 3. An index with
  schema 2 shows the board's existing "has schema 2; this board reads schema 3" line: no
  fallback.

### The existing tree: converted in place by the CLI

No migration command (answer 8). Chantier's own tree (this repository: `3-requests/batch-09/`,
paused, with its batch history in `events.jsonl`; `4-archives/` with 50 CRs; `5-trash/`) and any
other user's tree keep working because the CLI converts an old tree itself, once, at the first
command run after the update, before anything else:

- **When:** `.agents/changes/` holds `3-requests/`, `4-archives/` or `5-trash/`.
- **What, under the lifecycle lock and the batch's lock, all or nothing (renames, rolled back on
  a failure):**
  1. `5-trash/` → `6-trash/`, then `4-archives/` → `5-archives/`. When the new name already
     exists, nothing moves: exit 2, naming both folders.
  2. The batch folder `3-requests/batch-<n>/`: its own files move to `4-batches/`. More than one
     batch folder: exit 2, nothing moved (one batch at a time was already the rule).
  3. Each CR folder of that batch moves to its state folder by its recorded status (`queued` →
     `1-pending`, `ready` or `blocked` → `2-actives`). A `working` CR stays where it is: its
     Driver has the old path in its prompt; its folder moves at its next move (`3-done` at the
     merge, `6-trash` at a drop), and `3-requests/` is removed once empty.
  4. Every `path` in `batch.json` is rewritten to the new place (archived ones `5-archives/…`,
     trashed ones `6-trash/…`), through `Batch`, with one event `tree` listing the moves.
     Older events keep their old paths: they are history.
  5. `3-requests/STATUS.md|json` are removed; the index is written at the root.
- **Output:** the command's own output, preceded by one line on stderr: `converted
  .agents/changes to the new tree: 3-requests -> 4-batches, 4-archives -> 5-archives, 5-trash ->
  6-trash`.
- `read_batch_json` already reads old words this way (`open`, `landed`): same kind of rule, in
  `state.py` or `lifecycle.py`, documented in the module's docstring.

### Cards (`skills/chantier/references/`)

- `concepts.md`: the CR folder entry's lifecycle line (the new path of each stage), Batch ("its
  folder `3-requests/batch-<n>/`" → its files in `4-batches/`, its CRs in the three state
  folders), STATUS (index at `.agents/changes/`, batch page in `4-batches/`), Dependencies ("a
  slug already archived as merged" → "merged, in `3-done` or `5-archives`"), the new `3-ready`
  word.
- `chief-of-staff.md`: the "status?" row (line 26) and **Status** (line 232) name
  `.agents/changes/STATUS.md`; "Backlog and grill" gives `triage <folder> --ready` and replaces
  "A specified CR stays in the inbox or the backlog until the user prioritises it and picks it
  for a batch" with the `3-ready` rule (on the user's word, specified or not); the
  **automatable** way of triage (same section) says such a CR may go to `3-ready` with no
  specification, the Driver working from the request alone; **Open** (line 185) says `open` moves
  each folder to `4-batches/1-pending/`; the `order drop` comment (line 272) says `6-trash/`;
  `order merged` (line 274) says "to 3-done"; **Closing** says `close --yes` moves the `3-done`
  CRs to `5-archives`; **Putting back** (line 383) names `6-trash/`; the release section (line
  511) reads `work/retro.md` "in the release CR's folder (`4-batches/3-done/`)"; the plan
  (Starting a batch, step 2) proposes the `3-ready` CRs first; the tip "Run the P2s" may become
  "Run what is in 3-ready".
- `griller.md`: the `specified` line (above); "You `abandon` an inbox, backlog or `3-ready` item";
  "In a worktree": the stage example stays `<stage>`.
- `routing.md`: the Griller row.
- `driver.md` (line 128, the stack): "Merged CRs are gone from it, moved to `3-done` at once and
  alone".
- `release-template.md` (line 33): "the merged CRs' `evidence/` folders (`4-batches/3-done/`,
  and `5-archives/` for earlier batches)".
- `worker.md` (line 108) and `chief-of-staff.md` (line 470): the Demo's `demo/demo.md` "in
  `4-batches/`".
- `init.md`: step 1 names the folders `init` creates; the tour's thread ends "`3-done`, then
  `5-archives` at `close`" and passes through `3-ready` after the specification.
- The skill's `SKILL.md` files: any path above, if they copy one.
- `agents/` and `com.github.copilot/agents/`: they name no path today; if one is touched, both
  hosts together, bodies identical.

### Docs, README, CONTRIBUTING, evals

- `README.md`: "Change Request lifecycle" (the tree block, lines 225-250, with `3-ready` and the
  three states, "A CR moves to `3-done` when it merges and to `5-archives` at `close`", "A dropped
  CR goes to `6-trash/`"), "The CR board" (index path), "three levels" of STATUS.
- `CONTRIBUTING.md` lines 31-34 and 47-52.
- `docs/`: `cr-folder-lifecycle.svg`, `cr-lifecycle.svg`, `cr-lifecycle-simple.svg`,
  `how-chantier-works.svg`, `batch-lifecycle.svg`, `how-chantier-works-simple-foreman.svg` and
  their `-texts.md` companions (the stage headers, the `chantier triage --ready` arrow into
  `3-ready`, `4-batches` with its three states, `close` into `5-archives`, `order drop` into
  `6-trash`), kept in step as the earlier diagram CRs did (a check script in the CR's `work/`);
  `use-cases.md`, `use-cases-foreman.md`, `use-cases-direct.md`, `tutorial-claude-code.md`
  (line 168: the folder moves to `3-done`, then `5-archives` at close), `release-process.md`
  (line 61). The six SVGs are redrawn in this CR; their PNG renders go in the PR for the user's review.
- `evals/kit/audit.py` (lines 252-287): the batch is `4-batches/batch.json`; a merged CR is in
  `4-batches/3-done/<number>-<slug>` before `close` (the audit runs before `close --yes`); a
  dropped one in `6-trash/`. `evals/*/RUNBOOK.md`: `3-done` before close, `6-trash`.
- Release notes: the user-facing change (the new tree, `triage --ready`, the conversion) goes in
  the notes of the next version, by the project's procedure (`just release-notes`).

## Out of scope

- The external mode (`planning-repo`): the surface, `checkout.yml`, its sync, its archives
  pointing to the delivering PR, any `.gitignore` written by chantier.
- The sync between several Chiefs of Staff (`planning-server`).
- OKF (frontmatter, `index.md`, `just validate`).
- A migration command, and moving chantier's own planning out of this repository.
- CR numbering, branch and worktree names, the batch's number and lifecycle words (running,
  paused, closed), the rails: unchanged.

## Evidence

At the pushed head, with their output:

1. `just check` passes (Linux, macOS, Windows by CI). `tests/test_structure.py`:
   `test_init_creates_the_five_folders_once…` becomes the eight folders of `init` (renamed to
   match); the direct-batch test reads `brief.md` and `STATUS.md` in `4-batches/`. No new
   workflow test there (AGENTS.md: the workflow belongs to `just scenario`).
2. `just scenario` passes on both forges, its existing checks moved to the new paths
   (`World.folder`, `reset`, the `-> 3-requests/batch-01/` line of `open`, the board and index
   checks of `status_files` and `board_index`, `/5-trash/` → `/6-trash/`, `/4-archives/` →
   `/4-batches/3-done/` before close and `/5-archives/` after, "no `batch-*` left" → "no batch
   file left in `4-batches/`"), and new checks:
   - `triage --ready`: accepted with a specification and without one; the item in `3-ready/`;
     `open` takes both from there, the one without a specification recorded with
     `intake/request.md` as its specification (shown by `take`); `open` still refuses a backlog
     item with no specification; `triage --priority P2` brings a `3-ready` item back.
   - The folder follows the status: `1-pending` after `open`, `2-actives` after `take`, still
     there after `handback ready` and `blocked`, `3-done` after `order merged`, `6-trash` after
     `order drop`; a release CR in `3-done` after its hand-back.
   - `close --yes`: refused while `2-actives` holds a CR; then each `3-done` CR in
     `5-archives/<merge time>-<number>-<slug>`, its STATUS saying the cost is final, the batch's
     files gone, the three state folders left, empty.
   - A step `old_tree` (beside `old_words`): an old tree written by hand (a paused or running
     batch in `3-requests/batch-01/` with a queued, a ready and a working CR, `4-archives/` and
     `5-trash/` with one CR each); the next command converts it (the stderr line), every
     recorded path exists, the working CR stays at its old path until `order merged` moves it
     to `3-done`, then `3-requests/` is gone; a second command converts nothing; a tree with
     both `4-archives/` and `5-archives/` exits 2 with nothing moved.
   - The index at `.agents/changes/STATUS.json` has `schema` 3 and every path in it resolves
     from `.agents/changes/`.
3. `claude plugin test .` (the board's `hooks/register.test.tsx`) passes.
4. On a copy of this repository's own `.agents/changes/` (in a temporary folder, never the main
   checkout): one `status` converts it; the output, `batch-09`'s `batch.json` paths all existing,
   `5-archives/` holding the 50 archives.
5. A search shows no `3-requests`, `4-archives`, `5-trash` or `batch-<n>/` path left in the
   cards, the docs, the README, CONTRIBUTING, the evals, the board and the CLI, except the
   conversion's code and its scenario step.
6. The SVGs and their `-texts.md` companions in step (the check script's output).

## Open questions

None. The user answered them on 2026-11-10 (`02-answers.md`, "The specification's open
questions"): `3-done` until `close`, a dropped CR to `6-trash` at once; `3-ready` on the user's
word, with or without a specification (automatable), no priority kept; the CLI converts the
existing tree itself; the diagrams in this CR, PNG renders in the PR. Left to the Driver as
recommended: `open` and `order add` also take from `3-ready`, proposed first; the index at
`.agents/changes/STATUS.md`.