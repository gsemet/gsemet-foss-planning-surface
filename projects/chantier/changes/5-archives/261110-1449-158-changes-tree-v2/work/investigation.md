# CR-158 investigation: the changes tree, version 2

Read only, on the worktree `chantier.worktrees/batch-09-CR-158`. CLI = `skills/chantier/scripts/cli/src/chantier/`.

## 1. Files and entry points

### CLI

- `lifecycle.py`
  - `stage_layout` (l.15): five keys now; becomes `inbox backlog ready batches pending actives done archives trash`. `init` loops `.values()` (commands.py l.253): it must skip the `batches` parent key or it prints 9 lines, not 8.
  - `prepared_cr` (l.45): `paths["requests"] in directory.parents` -> "already active" becomes "under `paths["batches"]`". Accept `3-ready` parent. The "missing/empty spec" refusals (l.67-76) apply only to inbox/backlog; for `3-ready` without `03-change-spec.md` fall back to `intake/request.md` (`PreparedCR.specification`, title = first line, which `add_cr` records through `prepared.specification.name`: today it records the bare name `03-change-spec.md` and `_facts`/`_documents` join it to the CR folder, so for the fallback the recorded `specification` must be `intake/request.md`, a relative path with a slash; `_facts` l.1205 and `status._documents` l.169/179 already join it with `/` and work).
  - `ensure_unclaimed` (l.82): iterates `batch_folders()` and `batch_dir.name` in the message; uses `cr["path"]`.
  - `_retire` / `archive_cr` / `trash_cr` (l.102-119): "already left" test `source.parent == batch.dir` is the batch-level test. New: `done_cr` (2-actives -> 3-done, name unchanged, no stamp, sets `merged_at`), `start_cr` (1-pending -> 2-actives), `trash_cr` keeps the stamp and the `<number>-<slug>` name -> `6-trash/<stamp>-<number>-<slug>`. `archive_cr` goes away from `rails.archive_merged` and `commands.handback`; `close` does the archive moves.
  - `move_backlog_item` (l.122): add the `--ready` branch (target `3-ready/<slug>`, refuse exit 2 "already holds"), accept a `3-ready` source for `--priority`, and "already in 3-ready" (exit 2). Note the existing "already Pn" uses `EXIT_PRECONDITION` (2): same code.
- `state.py`
  - `Repo.batches` (l.241) -> `4-batches`; `batch_folders()` (l.249) iterates children with `batch.json`: becomes `[4-batches]` if `4-batches/batch.json` exists else `[]`. Keep the list API to minimise the diff but every `.name` use of a folder as a batch id is now wrong (see risks).
  - `batch_dir(batch)` (l.254) and `Batch.dir` (l.285): no `batch-<n>` level. A different batch number must exit 2 "unknown batch": `Batch.__enter__` (l.292), `read_batch` (l.406) and `_cr_events`/`read_events(repo.batch_dir(batch))` (commands l.357, 1817, 1906) must compare the requested id with `batch.json`'s `id`.
  - `next_batch_number` (l.258): `re.search(r"\d+", d.name)` over batch folders: with `4-batches` it reads 4. Use the recorded `id` from `batch.json`.
  - `Batch.__exit__` (l.347): "a failed open leaves no empty folder" `rmtree(self.dir)` when no subfolder; with the state folders always there this never fires, and a naive rmtree would delete the state folders. Replace by deleting only the batch's own files (`.lock`, etc.) when no `batch.json` was written.
  - `read_batch_json` (l.74): docstring home for the old-words reading; the conversion needs a new function and a docstring (spec: "state.py or lifecycle.py").
  - `Batch.move` / `_rollback_moves`: reuse for `take`, `order merged`, `close`.
- `commands.py`
  - `init` (l.240): 8 folders; help text in `cli.py` l.33.
  - `triage` (l.308): `--ready`; message `triaged 3-ready/<slug>`.
  - `abandon` (l.316): `in_requests = source.parent.parent == paths["requests"]` -> source parent is `pending` or `actives`; add `3-ready`; trash target `6-trash/<stamp>-<name>`.
  - `add_cr` (l.384): `next_cr_number(repo, (archives, trash, b.dir, *batch_folders))` -> roots `5-archives`, `6-trash`, `pending`, `actives`, `done`; `cdir = pending / "<number>-<slug>"`; `origin` stays.
  - `archived_merged` (l.433) + `declare_dependencies` (l.446): also met when in `3-done` (the in-batch lookup already finds the CR by its `path` name, `dep["status"] == "merged"` -> met; the new part is a slug whose CR is merged in the batch: already handled, but `cr_slug` reads `Path(x["path"]).name` and the archived name has the date, handled by the regex).
  - `open_batch` (l.513): `brief = b.dir / "brief.md"` already right once `b.dir` is `4-batches`; `short()` (l.582) cuts at `changes/`; output line `-> 4-batches/1-pending/...`; the line cap (10) holds. `check_no_open_batch` (rails l.20).
  - `seat` (l.684): `Batch(repo, folder.name, ...)` passes the folder name as id: with `4-batches` this is "unknown batch". Must use the id in `batch.json`.
  - `take` (l.1246): move `1-pending` -> `2-actives` inside the batch context before `_facts` (the Batch rollback list covers it). `_work(repo, c).mkdir` follows the new path. A release CR re-taken after `release_merged` (status back to `queued`, rails l.194-198) already sits in `2-actives`: `take` must treat "already in 2-actives" as a no-op, and `close` must refuse by folder, not by status.
  - `handback` (l.1300): release branch (l.1326) `archive_cr` -> `done_cr`; message "released, in 3-done"; ready/blocked stay.
  - `order drop` (l.831) and `cancel` (l.1602): `trash_cr`; `order merged` (l.851-859) -> `archive_merged` (rails l.184) renamed behaviour: moves to `3-done`, line "moved to 3-done".
  - `pause` (l.1659): `report:` names `b.dir / 'STATUS.md'` (right once `b.dir` moves).
  - `close` (l.1681), `_close_target` (l.1662), `_final_pages` (l.1728), `_final_rows`: rewrite (see section 3). Today it deletes the whole batch folder with `.closing-<name>` rename then `rmtree`; the `held` check is "any subdirectory" (this also trips on the Demo explorer's `demo/` today).
- `rails.py`: `check_no_open_batch` (l.20, message uses `folders[0].name`), `archive_merged` (l.184), imports `archive_cr`.
- `status.py`
  - `SCHEMA = 2` -> 3; module docstring (`3-requests/`).
  - `cr_view` `"batch": d["folder"]` and `batch_view` `"folder": folder.name`, title `# {folder}: {state}` -> show the id.
  - `cr_markdown` l.217: `(../STATUS.md)` -> `(../../STATUS.md)`; the `in_batch` flag computed in `write_batch` l.415 (`cr_folder.parent == folder`) -> `cr_folder.parent.parent == folder` (a CR in `3-done`/`2-actives`/`1-pending`); a legacy working CR at `3-requests/batch-09/<cr>` would be shown not in batch (no link) until it moves: acceptable but note it.
  - `batch_markdown` l.291: `[All change requests](../STATUS.md)` is already right for `4-batches/STATUS.md` -> `.agents/changes/STATUS.md`.
  - `_row` l.249-250: `"folder": _link(folder, repo.batches)` -> `repo.changes`; `status`/`specification` use `start` (relative to the batch page): `start` for the index is now `repo.changes` as well, so the index's `status`/`specification` paths are relative to `.agents/changes/`. Spec JSON contract: every path relative to `.agents/changes/`.
  - `_backlog` l.318: add `3-ready` first (priority cell `3-ready`), then P1..P4, then inbox. `spec_state` gives `specified`/`None` (an automatable CR shows `-`).
  - `_past` l.337 reads `STATUS.json` of each archive; for the current batch's `3-done` CRs build the "merged" list from `batch.json` (`merged_at`), newest first, before the `5-archives` ones; `merged_total` = both. `_when` reads the `YYMMDD-HHMM` prefix: `3-done` has none, use `merged_at`.
  - `dashboard_view` l.359: `start = repo.batches` -> `repo.changes`; `dashboard_markdown` link `{folder}/STATUS.md` -> `4-batches/STATUS.md`; `write_dashboard` l.436 writes to `repo.batches` -> `repo.changes` (the index at the root; the old `3-requests/STATUS.*` removal belongs to the conversion).
  - `write_final_pages` l.421: `cr_folder.parent != folder` -> pages for CRs now in `5-archives`/`6-trash`; must run after the moves with the updated paths in the passed copy of `d`.
- `cli.py` l.33 (`init` help), l.39-41 (`triage`: `--priority` no longer `required`, add `--ready`, mutually exclusive, one of them required: `add_mutually_exclusive_group(required=True)`), l.43 (`abandon` help "trash" stays).
- Old-tree conversion: new function (suggest `convert_old_tree(repo)` in `state.py` or a small `lifecycle.py` section) called from `Repo.find` callers' common entry: `cli.py` main before dispatch, or at the top of `Repo.find()`. The 25+ commands each call `Repo.find()` (grep), so `Repo.find()` is the one choke point, but it is a classmethod without the lock helper (`changes_lock` is in `lifecycle.py`, importing `state`): put the call in `cli.main` (after argument parsing, skipping nothing) to avoid the import cycle.

### Board, types, tests, scenario, evals

- `hooks/register.tsx`: l.1 comment, `SCHEMA = 2` (l.19) -> 3, `INDEX` (l.23) -> `.agents/changes/STATUS.json`, `crUrl` (l.384) base -> `/.agents/changes/`, `PRIORITIES` (l.95: `['inbox','P1'..'P4']`) must gain `'3-ready'` first or the `3-ready` rows are silently not shown (the backlog table is `PRIORITIES.flatMap`, l.572). Sheet lookup l.287 `dir + '/STATUS.json'`: `dir` comes from the index's `folder`/`path`, unchanged logic.
- `types/index.d.ts` l.18, 39, 55, 59: "Relative to `3-requests/`" -> "`.agents/changes/`", the index's path.
- `hooks/register.test.tsx`: l.8 `INDEX`, l.10 `CR_DIR`, l.44/l.69 `schema: 2` -> 3, **l.314 uses `schema: 3` as the "other schema" case: it must become another number (2 or 4) and the l.317 expectation `schema 3` follows**, l.242/245 the plain-root path, l.421/513/514/537/538 fake paths `1-backlog/P1/idea` (they are test data; keep or tidy).
- `tests/test_structure.py` l.302-317: rename to the eight-folder test (`created` x8, top-level names `1-inbox 2-backlog 3-ready 4-batches 5-archives 6-trash`, `exists` x8, `rglob("*.*")` empty); l.241-245: `batch.parent / "brief.md"` and `STATUS.md` already follow `batch.json` (glob `**/batch.json`), so the direct test may pass unchanged; the spec says it reads from `4-batches/`: tighten the path.
- `scenario/run_scenario.py` (38 hits): `World.folder` l.148-149 (-> `self.state / "4-batches"`, no name), `reset` l.158-161 (`rmtree` of batch dirs: now must delete the batch's own files and every CR folder under the three state folders, not the state folders), l.496/499/515 (`open` line, `w.name`, `/3-requests/{w.name}/`), l.533/1062/1066/1074/1079 (board/index), l.604 and 1405 (`/5-trash/` -> `/6-trash/`), l.672-701 (`4-archives` collisions, `close`), l.1085-1146 (`board_index`: `start`/`3-requests` joins; the `spec` checks at l.1140-1146), l.1346/1368/2096/2352 ("no batch-* left"), l.1525/1562/1563 (`len(glob("batch-*")) == 1`, `path.startswith(.../{w.name}/)`), l.1580/1713/1752/1760 (`/4-archives/` -> `3-done` before close), l.2005 `old_words`, l.2071/2118 (`drawn`, batch STATUS path). `old_words` also does `close` then `w.folder().is_dir()` (l.2047-2049): `w.folder()` is now always a dir, assertions flip.
- `evals/kit/audit.py` l.252-288: batch found by `glob("*/batch.json")` under `3-requests`; use `4-batches/batch.json`; merged CR in `4-batches/3-done/<num>-*`; dropped in `6-trash/??????-????-{num}-*`; l.258 message. `evals/*/RUNBOOK.md`: claude-full l.61, l.65; copilot l.36; claude-smoke l.32.
- `scenario/fake_glab.py`: 2 hits for `batch-0`; they are branch names, not paths: check only.

### Cards, docs, SVGs

- `skills/chantier/references/`: `concepts.md` l.29-30, 37-38, 81, 114 + the new `3-ready` Words entry; `chief-of-staff.md` l.24 (add `--ready`), 26, 96, 111, 144-146 (automatable), 185, 232, 272, 274, 349, 383, 447, 470, 511 (+ **Closing** section for `close --yes`); `griller.md` l.13/38 (+ the abandon sentence); `routing.md` l.14; `driver.md` l.128; `release-template.md` l.33; `worker.md` l.108/119; `init.md` l.10-11, 34-38; `hosts/claude-code.md` (1 hit, check the context); `session-start.md` l.113 (batch id only, probably nothing). `SKILL.md` files (chantier, griller): only copy a path if they have one (no hit in the grep).
- `agents/` and `com.github.copilot/agents/`: no path hit by the grep; nothing to touch unless a role text is edited.
- `README.md` l.43 (leave), 106, 175, 225-250 (tree block, "A CR moves to `3-done`", "A dropped CR goes to `6-trash/`", STATUS three levels l.248); `CONTRIBUTING.md` l.31-34, l.47-52; `docs/release-process.md` l.61; `docs/tutorial-claude-code.md` l.80, 145, 168; `docs/use-cases.md` l.45-48, 87; `docs/use-cases-foreman.md` l.47, 51; `docs/use-cases-direct.md` (no hit, check "archive").
- SVGs + `-texts.md`: `cr-folder-lifecycle` (svg l.40, 44, 148; texts l.53-56, 84, 100, 130), `cr-lifecycle` (svg l.110-113, 177, 233, 259, 303; texts l.99-102, 179, 335, 448, 504), `cr-lifecycle-simple` (svg l.59, 65, 76, 98; texts l.69, 77, 96, 137), `how-chantier-works` (svg l.166; texts l.159), `batch-lifecycle.svg` and `how-chantier-works-simple-foreman.svg` (no path hit in the grep of `3-requests|4-archives|5-trash`: the spec lists them, so check their stage words by reading the -texts.md), `batch-pace.svg` (4 hits of `batch-0`: not a path, skip).
- Release notes: `just release-notes` procedure (docs/release-process.md).

## 2. The smallest change

1. `stage_layout`/`Repo.batches`/`Batch.dir` to the new layout; keep `batch_folders()` as a one-element list so call sites change little; fix every use of a folder name as a batch id (`seat`, `next_batch_number`, `check_no_open_batch`, `_close_target`, `ensure_unclaimed`, `status`).
2. Replace `_retire`/`archive_cr` by three small moves (`start_cr`, `done_cr`, `trash_cr`) keyed on the folder's current parent, tolerant of a CR that is already in the target.
3. `triage --ready`, `3-ready` in `prepared_cr`/`abandon`/`status`, automatable fallback to `intake/request.md`.
4. `close`: new sequence (section 3).
5. `status.py` schema 3 and the root index; board follows.
6. Conversion function (section 3), then texts, then tests/scenario/audit/docs/SVGs.

## 3. Risky points

### Conversion of an old tree (in place)

- **Idempotence with a working CR**: a `working` CR stays at `3-requests/batch-<n>/<cr>` after conversion (spec), so `3-requests/` still exists on the second command. The trigger must not be "3-requests exists"; it must be: `4-archives/` or `5-trash/` exists, or a `3-requests/*/batch.json` exists, or `3-requests/STATUS.*` exists. "More than one batch folder" counts only folders with a `batch.json`. Without this, either every command re-converts, or the second command (the scenario's "converts nothing") fails. Chantier's own tree is exactly this case: **CR-158 itself is `working` at `.agents/changes/3-requests/batch-09/158-changes-tree-v2/`** in the main checkout, so its folder moves only at its merge (`3-done`), and `order merged` must move it from a path outside any state folder.
- **`order merged` of a legacy-path CR**: `done_cr` cannot test "source.parent is 2-actives"; test "not already in done/archives/trash". Same for `trash_cr` (`order drop`, `cancel`).
- **`4-batches` already exists**: a user who ran the new `init` before any other command has empty `4-batches/{1-pending,2-actives,3-done}`, `5-archives/`, `6-trash/`: the "new name already exists -> exit 2" rule then refuses a perfectly good tree. Run the conversion before `init`'s mkdirs and treat an existing EMPTY target as replaceable (non-empty target: exit 2 naming both). Merge the old batch's files into an existing empty `4-batches/`.
- **Windows**: `.lock` of the batch is held open (msvcrt lock) while the conversion runs under the batch lock; renaming/moving an open file fails on Windows. Do not move `.lock`: create a new one in `4-batches/` and let the old one go with the empty folder (or release before the move). A directory rename also fails when another process has a CWD or open handle inside (a Driver's shell in a CR folder; the Windows eval): the all-or-nothing rollback must then leave the old tree intact and say which path is held (exit 4, `move_directory` already maps `OSError` to `EXIT_EXTERNAL`).
- **Concurrency**: many CLI processes run in parallel (Drivers, Foreman). The cheap detection (a few `is_dir`/`is_file`) runs without a lock; once positive take `changes_lock` then the batch lock, re-check, convert. Readers that run without any lock (`status`, `handoff`) must wait for the same detection or they see half a tree. Take the lifecycle lock first, then the batch lock: the same order as `take`/`handback` (`changes_lock` then `Batch`), to avoid a deadlock.
- **Lock order vs `Batch`**: the conversion edits `batch.json` paths "through `Batch`" but `Batch.dir` is now `4-batches` while the file is still in the old folder: do the file moves first (under a plain lock on the old `.lock`), then open `Batch` on the new place for the path rewrite and the `tree` event. Not a single `Batch` context: a failure between the two steps must roll back by renames only (the batch.json is then still the old one).
- **Path rewrite must be complete**: `cr["path"]` and nothing else? `batch.json` also keeps `c["worktree"]` (outside), `release`, `asks`/`orders`/`notes` text with paths (history, leave), `summary`. Rewrite `crs[].path` only; archived/trashed CRs already carry `4-archives/...`/`5-trash/...`: rewrite by prefix `.agents/changes/4-archives/` -> `5-archives/`, `5-trash/` -> `6-trash/`. A path that does not exist after conversion should fail the conversion (assert and roll back), not be written.
- **`working` CR's Driver holds the old path** in its prompt (`_work`/`cr_directory` read the recorded `path` from `batch.json`, so CLI calls still resolve it; the Driver's own notes under `work/` stay valid).
- **A `ready`/`blocked` CR** moves to `2-actives`: a Verifier or Reviewer running in a detached state is not a lock holder; the spec accepts this.
- Old events keep old paths; `brief.md` lists old paths too (history; don't rewrite).
- `.batch-number`, `.lifecycle.lock`, `.long-gate.lock`, `seat.json` stay at the root; `write_dashboard` must `unlink` `3-requests/STATUS.*` and then remove `3-requests/` only if empty (and the empty `batch-<n>/`).
- A paused batch with STATUS written before conversion: the first `Batch.__exit__` rewrite brings the new STATUS; with no write (read-only `status`) the old STATUS pages are stale but harmless. `status --refresh` rewrites.
- A tree with `batch.json` status `landed`/`open` goes through `read_batch_json` first (same bridge).

### Behaviour

- `take` before the facts are printed: the move is inside the `Batch` context; the facts' `folder:` line and `work/` mkdir follow the new path. A failed `take` rolls back via `_rollback_moves` (the Batch records the move).
- Release CR requeued after `release_merged` is in `2-actives` with status `queued`; `take` again must not fail on "source not in 1-pending". `close` must refuse on `2-actives` content by folder even if status says otherwise (not the other way).
- `close`: order = refuse (all checks, both folders) -> list -> with `--yes`: price, move each `3-done/<number>-<slug>` to `5-archives/<merged_at as YYMMDD-HHMM>-<number>-<slug>` (a collision exits 3, rolled back), update the paths in a copy of the record, `write_final_pages` (archives and trash), then rename the batch's own files to a `.closing-` folder and delete (everything in `4-batches/` but the three state folders; `demo/` is deleted with them: it is not a "held" CR folder, so the `held` check must look only at `1-pending`/`2-actives`). `merged_at` must be recorded for CRs merged before the update (legacy `merged` ones are already in `4-archives`, no issue) and for a release CR (`handback` sets it too). A CR with `merged_at` missing (should not happen) falls back to `now()`.
- Two CRs with the same merge minute: the number in the name keeps them apart (`<stamp>-<number>-<slug>`).
- `Batch.__exit__` failed-open cleanup (above).
- `abandon` of a CR in `pending/`/`actives` must still be unclaimed: `ensure_unclaimed` compares recorded paths.
- Backlog/ready `slug` collision with `3-ready`: `triage --ready` refuses (exit 2); `triage --priority` from `3-ready` refuses if the target holds the slug (exit 2 as today).
- `--batch 4`/`batch-04` of a number other than the current: exit 2 "unknown batch" (check in `Batch.__enter__`, `read_batch`, `batch_dir` users).
- The CR number allocation (`next_cr_number`) must still see the three state folders and both past stages; a failed `open` rolls back moves (`_rollback_moves`) as today.
- Windows rename of a directory into a non-existing parent: `move_directory` creates the parent (OK).

## 4. Questions only the user can answer

None. Notes for the Driver, no user question: the spec fixes the strings; the conversion's trigger and the empty-target tolerance above are design details the spec leaves open (decide as recommended here).

## 5. Evidence plan

Kind: a CLI change with a data-layout effect, a status schema bump, a board change, and docs/SVGs. Project rules: `just check` is the fast gate, `just scenario` the long gate (CLI/cards/scenario change), PNG renders of the SVGs for the user in the PR.

1. `just check` at the pushed head; output kept in `evidence/`.
2. `just scenario` on both forges (the log): the existing checks moved plus the new ones of the spec (triage --ready with/without spec, folder follows status, close sequence, `old_tree`, `schema` 3). Keep the scenario log tail with the check names.
3. `claude plugin test .` (board), output.
4. Before/after on a copy of the real tree: copy `C:/Users/gaeta/Projets/chantier/.agents/changes/` to a temp folder inside a throw-away git repo (the CLI finds its root via git; `CHANTIER_ROOT` can point to it), record `tree` before, run one `status` from the worktree's CLI (this is the "after"), record: the stderr conversion line, `tree` after, count of `5-archives` (50), `6-trash` (11), a script that opens `batch.json` and checks every `crs[].path` exists, and the CR-158 `working` path staying put. Never touch the main checkout.
5. The path search: `rg "3-requests|4-archives|5-trash"` over cards, docs, README, CONTRIBUTING, evals, board and CLI: only the conversion code and the `old_tree` step may remain.
6. SVGs: the check script in `work/` comparing each `-texts.md` with its SVG text nodes (as earlier diagram CRs did); render PNGs (`docs/` render tool of the project, see CONTRIBUTING) and attach them to the PR; screenshot of the board is not needed beyond the test (a board render needs the Claude Code UI; say it cannot be shown otherwise).
7. Cannot be shown: the board in a real session (test only), a Windows/macOS run (CI), a real `working` Driver mid-conversion.
