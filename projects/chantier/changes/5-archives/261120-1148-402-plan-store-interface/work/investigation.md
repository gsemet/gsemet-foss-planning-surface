# CR-402 investigation (before round 1)

Read-only; `$CHANTIER rules` read (AGENTS.md, CONTRIBUTING.md layers/size rules apply).

## 1. Write sites vs spec 5.4

Grep over `src/chantier` (hub/ and status/write.py excluded by the spec). Published sites, all in the table:
`lifecycle/filing.new_request` (mkdir exclusive, `intake/` mkdir, request.md write_bytes), `core/batch.move_directory`
(callers: `commands/intake.py:131,197`, `lifecycle/stages.py:298`, `core/batch.py:202`, `commands/close_archive.py:195`),
`Batch._rollback_moves` (`batch.py:217` `retry(destination.rename, source)` plus `source.parent.mkdir`),
`lifecycle/backlog.py:131` (write_bytes), `:161` next-batch.json, `lifecycle/stages.py:236` delivery.md,
`lifecycle/moveout.py:58` (append, open "a") and `:77` formerly.json, `core/records.py:352` restored.json
(`path.write_text`, not atomic, no CRLF care), `core/batch_records.py:50,155,161-165`, `summaries/store.py:51`,
`commands/crs.py:278` (`shutil.copyfile`), `commands/driver.py:146,183` (`work/` mkdir), `commands/intake.py:49,56` (init),
`playbook/edit.py:381` (config write_bytes), `core/files.ensure_gitignore`.

NOT in (or only half in) the table:
- `commands/close_archive.py:157-208`: `going = .closing-*` mkdir, `retry(p.rename, going/p.name)` (a 3-done CR leaves a
  published path), `retry(target.rename, source)` (undo, :174), `shutil.rmtree(going)` (:208). The table says "renamed into
  5-archives"; the real shape is rename out to a local `.closing-*` folder, then `move_directory`. `.closing-*` is IGNORED,
  but the rename's SOURCE is published, so it needs `move`/`remove` (or `move` to the ignored name) and `check_publish`.
  rmtree of an ignored folder is local, keep `shutil` there.
- `core/batch.py:50` `destination.parent.mkdir` and `:217` `source.parent.mkdir` (implicit mkdir inside move, becomes `move`'s parents).
- `lifecycle/stages.py:85` `repo.changes.mkdir` in `changes_lock` (goes in `lock()`); `commands/intake.py:49`.
- `commands/crs.filed_fix` goes through `new_request`-like code plus copyfile: two writes, row exists.
- `core/batch_records.undo_close` `unlink` of record and report: `remove`.
- Local, may stay: `batch.json` (`batch.py:148`), `events.jsonl`, `.batch-number` (:162, ignored), `brief.md` (`opening.py:332`,
  `commands/factory.py:40-46` rewrites brief.md in place), seat.json, gate_*, `.tmp`, `work/gates`.
- Board: no direct write site in `board/` except via `lifecycle/backlog.py`, `summaries/edit.py` and `playbook/edit.edit_surface_file`
  (config). No other board write found.
- Also read paths using `retry(...read_bytes)` (`backlog.py:124`, `edit.py:80`): reads, allowed.

## 2. Live code and layer constraints

- `core/repo.py` (284 lines): `Repo.find` calls `repo.ensure_gitignore()` (:125), which calls `core.files.ensure_gitignore(changes)`
  (module-level `_ignored_done` set); `project_path` (:34) holds the "path must be inside the planning folder" text.
- `core/files.py` (184 lines, 216 free): `write_file/write_bytes/write_json`, `retry`, `try_lock/unlock`, `IGNORED`, `ensure_gitignore`.
  `.gitignore` meaning of IGNORED (`/`, `/dir/`, `**/`, `*`): a small matcher (about 25 lines) is new; put it in `store/base.py`
  or a `core/` helper, not `files.py` if it pushes near 400 (it will not).
- `lifecycle/stages.changes_lock` (:81-98): mkdir, `repo.ensure_gitignore()`, `.lifecycle.lock` `a+`, 30 s deadline, `time.sleep(0.05)`.
  Move body into `store` with a module constant (e.g. `LOCK_WAIT = 30`) that the conformance test monkeypatches; the lock needs the
  gitignore ensured first: the store's `lock()` calls the `.gitignore` write itself (store imports only `core.files`), so `changes_lock`
  becomes `with repo.store.lock(): yield`.
- `core/batch.move_directory(source, dest)` takes absolute paths and is imported by `commands/intake.py`, `close_archive.py`,
  `stages.py`; it lives in a module that imports `core.repo`. Keep the function as thin wrapper over `repo.store.move(rel, rel)` is
  impossible (no repo arg). Smallest: change its signature to `move_directory(repo, source, dest)` (5 callers) or move the checks into
  `store.move` and have callers call `repo.store.move(repo.rel(a), repo.rel(b))`. Texts/exit codes (3 usage/conflict/external) must
  move verbatim; the "CR folder not found" text uses the absolute path, so `move` must format the absolute `root / rel`.
- `playbook/edit.py` is 382 lines (18 free): `_target` (:69-) and `READ_ONLY` (:35); moving the text out and importing frees lines, ok.
  `playbook/config.py` is 397 lines (3 free): replacing `FILES = (...)` by an import must not add lines (`FILES = store.CONFIG_FILES`).
- `core/records.py` 366 (34 free), `core/batch.py` 309, `lifecycle/stages.py` 313: ok.
- `test_code_targets.py`: every import counted, functions inside included, cycle test over the whole graph, 400 lines/50 lines;
  startup import test (no pydantic in `store/`). `store/` may import `core.files`, `core.errors` only. Careful: `core/repo.py`
  importing `store` and `store` never importing `core.repo` keeps it acyclic.

## 3. Proposed split (sequential, each green)

1. Round 1: `store/` package (base protocol, shared ops, FolderStore, SurfaceStore), `Repo.store`, `lock()` moved with
   `changes_lock` delegating, `.gitignore` write via store, `config_path`/`write_config` + constants (`FILES`, `READ_ONLY`) moved,
   `project_path` text single-sourced, and `test_store_conformance.py` (folder, surface, dedicated-branch skipped). No call site
   other than `changes_lock`/`ensure_gitignore`/edit.py moves yet. Suite stays green.
2. Round 2: route every published write through the store (move_directory/rollback, new_request, backlog, moveout, records,
   batch_records, summaries store, stages delivery, crs.filed_fix, driver work/, intake init, close_archive) with `check_publish`
   calls before the first change in each command (a thin helper in each command, `command` passed from the dispatch: one seam,
   set once per CLI call on the store, e.g. `repo.store.command = args.cmd...` set in the command's entry or a `Repo` attribute).
3. Round 3: the command-table spy test, board rows, CONTRIBUTING.md layers sentence, timing measurement of `just test`.

## 4. Spy test, smallest design

- A `SpyStore` wrapper class (in the test file) delegating to the real store and appending `(name, args)` to a list; `check_publish`
  additionally stores `fingerprint(root)` (dict path -> bytes over `rglob`). Install by monkeypatching `Repo.store` property (or the
  cached attribute) on the class so every `Repo` made during the command gets the spy; the test compares each fingerprint with the
  pre-command one, asserts that `check_publish` precedes every write method in the log, that its union of paths covers the published
  paths changed (diff of before/after fingerprints filtered by `store.published`), and `config=True` for the config row.
- Rows as data: `(id, setup(surface), argv)`; setup uses the cached `tests/conftest.py::surface_template` (already exists, session
  scope, copied per test by the `surface` fixture), plus one cheap shared state (an opened batch) built by copytree of a second
  session-scoped template derived from `surface_template` (`open` run once), never per row. Board rows call the route functions
  as `test_board.py`/`test_board_config.py` do.
- Seam for `command`: simplest is one attribute set by the dispatch (`main` sets `repo.COMMAND = args.cmd` beside `repo.PROJECT`,
  already a module global pattern in `cli.py:131`), and board routes pass their own name in each `check_publish`. Needs the Driver's pick.

## Risks
- `close_archive` rename-to-`.closing-*` shape (see 1) and `restored.json` byte equality (`write_text` of `json.dumps(...)+"\n"`:
  default text mode on Windows writes `\r\n`? `Path.write_text` translates `\n` to `\r\n` on Windows; keep bytes "as today" by
  checking what Windows produced, the spec says keep as `write_restored_number` makes them; use the `\n` form via write_bytes is a
  behavior change on Windows only: pick `\n`, atomic, and note it).
- `_ignored_done` cache keyed by path: the store's `.gitignore` write must keep it (a test patching files may depend).
- `playbook/config.py` has 3 lines of slack.

## Questions for the user
None.

## Evidence plan
Kind: internal refactor with no visible change. Evidence: `just check` and `just test` output (time before/after on the same machine,
logged in `evidence/`), the new conformance and command-table tests passing, `just eval-dry-run`, `just scenario`. Nothing to see in a
screenshot; the spy log of one command (check_publish before writes) can be saved as a text excerpt. Cannot be shown: the refusal
(Part C's).
