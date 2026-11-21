# CR-419 investigation (map for splitting)

Paths under `skills/chantier/scripts/cli/src/chantier/` (tests: `skills/chantier/scripts/cli/tests/`).
Head `a391c1eb`. Rules read (`rules`): no rule touches this beyond AGENTS.md (gates, 400/50 limits).

## 1. store/ today
| file | lines | shape |
| --- | --- | --- |
| store/base.py | 111 | `PlanStore` Protocol (reads: `read_text(rel)`, `exists`, `listdir`; writes), `guard(root, rel, root_ok)`, `inside_path`, `is_published`, `_matches`. Imports core.errors, core.files.IGNORED |
| store/folder.py | 122 | `FolderStore`; `_p(rel, root_ok)` = guard; `read_text` -> `core.files.read_text(self._p(rel))`; `exists`, `listdir` (sorted iterdir); writes, `lock`, `move` |
| store/surface.py | 53 | `SurfaceStore(FolderStore)`: `check_publish`, `config_path`, `write_config`; reads inherited (nothing to add). Imports `writer.lines` (which imports board.running, hub.state: so store/ must never be imported at module level by those, use TYPE_CHECKING) |
| store/__init__.py | 7 | exports |
Room: base +~12 protocol lines, folder +~50 (7 methods; `walk` is the longest, keep it < 50 lines, `stat`/`glob` 5-8 each). Fits in 400/50. `read_text` needs `errors`; `core.files.read_text(path, errors)` already takes it.

Files near the 400 cap (watch when adding a param/import): core/records.py 382, status/views.py 375, hub/journal.py 368, board/write_api.py 292, core/repo.py 302.

## 2. Direct reads in the store-only modules (file:line, receiver)
`folder`/`path`/`base` are Paths built by the caller; all are planning-folder reads unless marked EXEMPT (spec 5.5).
- board/archived.py:36 `folder.is_dir()`
- board/backlog.py:45-46 `folder.glob("*.md")`, `(folder/"intake").glob`; :54 `path.is_file()` + `read_text(path,"replace")`; :65 `os.walk(folder)`; :75 `path.is_file()` + `read_text`; :90 `.is_file()`. Also :96 `summary_view(folder)`, :115 `waits.read_file(folder)` (5.4 callers)
- board/crs.py:88 `folder.is_dir()`; also `read_batch/events` via state
- board/files.py:54 `os.walk`, :60 `real.stat()`, :63 `real.is_file()`, :75 `target.is_dir()`, :81 `path.open("rb")` (`_head`, 1 MB), :94 `.is_file()`, :97 `.stat()`
- board/fingerprint.py:27 `path.stat()`, :36 `os.scandir`, :44 `e.is_dir(follow_symlinks=False)`, :54 `base.glob(HOLDS)`
- board/journal.py:22 `.is_file()` + `read_text` (import :12); :47 `open("ab")` stays (write)
- board/projects.py:94 `projects.home.changes.is_dir()`
- board/state.py:132 `(changes/RECORDS).glob("batch-*.json")` (+ `read_text` import :21 used for record files); :205 `root.is_dir()` EXEMPT (code repo, `origin_of`)
- board/write_api.py:121 `(folder/"03-change-spec.md").is_file()`; :243 `target.read_bytes()`; :130,:150 `summary_view`
- board/api/ops.py:83 `target.is_file()`; board/api/topics.py:89,:100 `path.stat()` (journals' size/time)
- board/config_api.py:44 `path.is_file()` EXEMPT? (`config_path`, config file) but `_open_batch` -> `read_batch_json(path)` :47 is a planning read
- board/static.py, command.py, key.py, address.py: EXEMPT (5.5)
- hub/batch_prs.py:29 `path.is_file()` + `read_batch_json` :32; hub/watch.py:60 `is_file`, :63 `read_batch_json`, :43 `read_seat`; hub/journal.py:107 `.is_file()` + `read_text` (import :43); :280 `open("ab")` stays; hub/lock.py, hub/state.py EXEMPT
- status/views.py: :93 `work.glob("*.md")`, :94 `(work/"gates").glob("*.log")`, :97 `p.exists()`, :98 `spec.is_file()`, :103 `target.is_file()`, :227 `folder.is_dir()`, :233 `.exists()`, :235 `.is_file()`, :240 `paths["backlog"].glob("P[1-4]")`, :244-245 `stage.iterdir()/is_dir()`, :254 `item.rglob("*")` + `is_file()` (-> `walk`), :278-279 `stage.iterdir()/is_dir()`, :285 `stage.is_dir()`; calls to 5.4: :190 `read_events`, :219 `title_source`, :314,:338 `read_batch_json`, :340 `read_events`
- status/write.py:34,:51 `cr_folder.is_dir()`; :23 `read_events`
- core/repo.py: :45 `read_keyed` EXEMPT? (`read_text(path)`: check which file: `.batch-number`/key file, decide); :62-65 `base.iterdir()` EXEMPT (surface_projects); :116,:139,:156 EXEMPT (project.md, Repo.find); :197-202 EXEMPT (clone); :263 `(self.batches/"batch.json").is_file()` (batch_folders) MOVE; :283 `.batch-number` is_file+read_text MOVE; :286 `(changes/RECORDS).glob` MOVE; :269,:295,:301 `read_batch_json`
- core/surface_batches.py:16 `path.is_file()`, :19 `read_batch_json(path)`; no Repo for the other project: build `SurfaceStore(surface_root/projects/<name>/changes, project_folder, repo.git_dir)` (building creates nothing).
- 5.4 readers' own reads: records.py:332 `read_json(path)`, :377 `path.exists()`+`read_text` (:373 read_events), :359 read_restored_number `read_text`; seat.py:15; waits.py:75; batch_records.py:100 `exists`, :113 `glob`, :134 `is_file`+`read_bytes`, :144,:162 `exists` (writers' looks: in scope for the test, move too); summaries/store.py:37; core/files.py:53 `title_source` (:57 `is_file`, `read_text`).

## 3. Callers of the 5.4 readers (call lines, grep `name(` excluding defs; my count differs from spec's: spec counts by file lines it measured)
- read_batch_json 34 calls: core/repo 4 (269,295,301 + lazy imports), core/batch 5 (119,265,277,298 ...), board 4 (config_api 47, costs 29, state 164), commands 4 (closing 112, intake 94,140), hub 2, status/views 2 (314,338), gate_queue 74, lifecycle/stages 167, surface_batches 19; tests 7 (4 files).
- read_events 15: board/state 166, commands (activity 112, batch_status 336, cost/breakdown 36,156, cost/sessions 269, crs 58, orders_reorder 15), status/views 190,340, status/write 23.
- read_restored_number 3: core/batch 290, lifecycle/moveout 55.
- read_seat 11: board/seats 68, board/state 149, commands/access 59, commands/seat 96,109,139, hub/watch 43, writer/surface 49. Already take `repo`.
- waits.read_file 6: board/backlog 115, commands/joining 72, commands/waits 245,324, lifecycle/layout_check 174.
- summaries store.read/read_or_new 8: commands/summary 73, summaries/edit 64, format 57, gaps 36,61, title 31, view 29.
- summary_view 5: board/backlog 96, board/write_api 130,150.
- title_source 2: status/views 219, summaries/title 36. read_record 3 / last_closed 3 / read_retro 1: inside batch_records, commands/batch_status 334, commands/closing 237.
- Outside spec 5.3 callers touching only call form: commands/* (9 files), lifecycle (3), core/batch.py, gate_queue.py, writer/surface.py, summaries/{edit,format,gaps,title}.

## 4. Proposed signatures and layering
Layers (CONTRIBUTING): core/ (errors, files, records, repo, store...) below domain below commands/board. `core/repo.py` imports `core.records` lazily (pydantic) so `records` must not import `Repo`. `core/files.py` is below `store/` (store imports it), so `title_source` cannot take a store at runtime import: use a `PlanStore` type under `TYPE_CHECKING` only (no import cycle, structural Protocol), or move it to `summaries/title.py` (already imports it) / `core/records.py`.
Proposal, one rule: **`(store, rel)` for the pure record readers, `repo` where a Repo already is the argument.**
- `core/records.py`: `read_batch_json(store, rel)`, `read_events(store, rel_folder)`, `read_restored_number(store, rel)`; `PlanStore` imported under TYPE_CHECKING. The error text keeps the full path: `store.root / rel`.
- `core/waits.read_file(store, rel_folder)`, `summaries/store.read(store, rel_folder)` / `read_or_new`, `summaries/view.summary_view(store, rel_folder)`; `core/files.title_source` becomes `title_source(store, rel_folder)` with TYPE_CHECKING import (or relocate; Driver picks; relocating changes 2 callers).
- Keep `read_seat(repo)`, `last_closed(repo)`; `read_record(store, rel)`, `read_retro(store, rel_folder)`. Existing writers already use `(repo, folder: Path)` + `repo.rel(...)` (summaries/store.write), so an alternative `(repo, folder: Path)` is the least diff for callers that have a repo, but impossible for records.py/files.py (layering) and for surface_batches (no Repo of the other project). Hence (store, rel).
- Rel building: `Repo.rel(path)` resolves twice (cost on 200 CRs). Add a pure helper `store/base.rel_in(root, path) -> str` (no resolve, as_posix) or build `rel` as strings from `repo.rel(batches)`; avoid `Repo.rel` in hot loops (spec 6 speed gate).
- Board/status functions that took `changes: Path` or `folder: Path` (`fingerprint(changes)`, `since_rescan`, `backlog_items(changes, rows)`, `recovered_after(changes, rec)`, `count_files/description/depends_of(folder)`, `files.tree/read(root, rel)`, hub `journal.read(changes)`) take `store` first, folder stays a Path or becomes rel (Driver fixes one rule before C/D start: suggested `(store, folder: Path)` + `rel_in(store.root, folder)` inside, to keep their ~40 callers).

## 5. Parts (disjoint files)
Order: **A first (protocol)**, then B, C, D, E in parallel, then F.
- **A. store protocol + backends** (store/base.py, folder.py, [surface.py unchanged], `rel_in` helper, tests/test_store_conformance.py extended). ~170 lines. Blocks all; at least the base.py signatures must be agreed first so B-E can code in parallel against them; tests of B-E need A merged.
- **B. 5.4 readers + callers outside C/D/E** : core/records.py (382 lines: make room, move import line only), core/seat.py, core/waits.py, core/batch_records.py, core/files.py (title_source), summaries/{store,view,edit,format,gaps,title}.py, commands/*, lifecycle/{stages,moveout,layout_check}.py, core/batch.py, gate_queue.py, writer/surface.py; tests: test_batch_end.py:243, test_came_back.py:105, test_leases.py:321,357,367 (also the two `fingerprint(found.changes)` at 388-391 of the same file: B owns the whole file, uses C's chosen fingerprint signature).
- **C. board/** (all files in 5.3 except those not reading): state, backlog, archived, crs, files, fingerprint, journal, api/ops, api/topics, write_api, projects, config_api, costs, seats (call-form for 5.4 readers in these). Tests: test_board_archived.py (recovered_after(tmp_path,...)), test_board_description.py:41, test_board_waits.py:45, test_board_prs.py:394-400, tests/store_spy.py:51 (uses `fingerprint` of its own, test helper; unaffected unless named same).
- **D. hub/ + status/**: hub/batch_prs.py, watch.py, journal.py (368 lines), status/views.py (375 lines), status/write.py. Tests: every `forge_journal.read(x.changes)` call: forge_world.py:100, test_board_config.py:130,231, test_board_journal.py:54,93, test_event_audience.py:96, test_event_types.py:217,258, plus callers src: board/api/topics 106, commands/batch_status 270, hub/{autostart 62, journal_add 117, lines 20, watch 148,193,219} (hub ones in D; topics in C; batch_status 270 in B).
- **E. core/repo.py + core/surface_batches.py** (+ tests/test_surface_batches.py unchanged). Owns repo.py's lines 263-301. Small; can be given to B's coder or to D's if size matters.
- **F. structure test + docs + measure** (last: needs all done): tests/test_store_reads.py, CONTRIBUTING.md sentence after the layers paragraph (line ~336), the speed script (outside tests), PR text.
Not parallel-safe: test_leases.py (B only); any file listed in two parts above (none after assignments). `board/api/topics.py`: C.

Risks: (1) rel computation cost; (2) `walk` in status/views `_backlog` replaces `rglob` (symlink difference on 3.11/3.12, Known gap); (3) `board/files.py` keeps `Path.resolve` real-place check and `core.files.inside` (404 semantics, not store refusal); (4) `stat` None vs OSError at fingerprint/topics callers: `except OSError` branches become `if None`; (5) read_bytes limit for `_head`; (6) core/repo.py `batch_ids` loops call a reader per read: no cache so no new perf cost; (7) messages with full paths: `store.root/rel` must equal caller's old path text (`repo.changes` is not resolved; `Repo.rel` resolves, so build with `store.root / rel`, not resolve); (8) tests pass bare `tmp_path` as folder to board helpers, they must now build `FolderStore`; (9) store/surface.py imports writer.lines -> board.running; new imports of store from core.records must stay TYPE_CHECKING or an import cycle appears; (10) 400-line caps listed in 1.

Questions for the user: none.

## 6. Evidence plan
Kind: internal refactor, no output change; nothing to see on screen (no pane change, no screenshot).
- Before/after golden: on a prepared planning folder (200+ CR folders in backlog, a batch with events, journals, a summary, waits), capture `chantier status` stdout and `board/state.project_state` JSON, at main head (a391c1eb) and at the CR head; `diff` empty. Saved in `evidence/` (`status-before.txt`, `status-after.txt`, `state-before.json`, `state-after.json`, `diff.txt`).
- Timing: same script, 5 runs median, both figures in `evidence/speed.txt` (and PR); more than 10 % slower = fix.
- Structure: `evidence/structure-test.log`: `pytest tests/test_store_reads.py` green on shipped files, plus the prepared-source case showing the refusal (module, function, line); plus a grep count of direct reads in the store-only modules before (269-ish spec figure) and after (exempt list only).
- Conformance: `pytest tests/test_store_conformance.py` log on `folder` and `surface`.
- Gates: `just check`, `just test` with its time (budget 18.5 s + 30 s), `just eval-dry-run`, `just scenario` pipeline job; Windows `chantier gate` if top of stack.
Cannot be shown: run-time proof that nothing is opened outside the store (carried to `store-reads-rest`); macOS/Linux timings from this Windows machine.
