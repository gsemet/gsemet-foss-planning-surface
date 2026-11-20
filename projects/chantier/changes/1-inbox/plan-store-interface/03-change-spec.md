# Change Specification: the plan's storage behind a minimal interface (Part B of seven)

Origin: verbal (2026-11-10, Beads study; grilled 2026-11-20). No tracker issue.

This CR is Part B of the seven-part work the user split into seven CRs (planning-server-Q7,
2026-11-20). Its grill is `planning-server`'s: `2-backlog/P3/planning-server/02-answers.md` (the
user's decisions, Q1 to Q30), and its reference text is that CR's
`experiments/03-change-spec-all-parts.md`, "Part B", §1 to §4 and §5 to §9 where they name Part B,
with the storage study `experiments/plan-storage-comparison.md`. The two points that reference left
open are settled in this CR's own `02-answers.md` (2026-11-20, by the Chief of Staff): the
interface's byte and folder writes, and the project's configuration file. This file carries all of
it; a Driver needs nothing else.

## 1. Goal, in the user's terms

The plan lives outside the project, in a planning surface, as Markdown and JSON that anyone can
browse on the forge; "everything in Markdown is essential". Of the five ideas the user took from
Vercel Board ("tout", planning-server-Q3), this is the fifth: **the plan's storage behind a
minimal interface, with one conformance test that every backend passes** (the planning folder, a
dedicated branch, a server).

This CR builds that interface and puts every published write of the CLI and of the board behind
it, with no change of behaviour: the same files, the same commands, the same messages, and no
refusal. It is the base Part C (the writer, `planning-server`) needs to refuse a write while no
writer runs; and the base the pending P2 item `one-read-interface-over-the-planning-fol` builds its
read half on.

## 2. Dependencies and neighbours

This CR needs nothing merged first. It comes first with Part A (`1-inbox/typed-journal-events`);
the two are independent.

What comes after and what it needs from this CR:

| CR | What it needs from this one |
| --- | --- |
| C, `2-backlog/P3/planning-server` (approved, its `03-change-spec.md` §2) | the package `store/` (`PlanStore`, `FolderStore`, `SurfaceStore`, `Repo.store`), every published write of the CLI and the board going through `repo.store` and calling `check_publish` with its published paths before it changes anything, and `test_store_conformance.py`. Part C gives `SurfaceStore` the feature `refuses-without-publisher` and its refusal (its C.8), runs the conformance test's `refuses-without-publisher` case on `surface`, and turns this CR's command-table test into its refusal test `test_surface_writes.py` (its §6). |
| D, `1-inbox/driver-leases` | nothing of this CR's code: a lease lives in `batch.json`, local. |
| E, `1-inbox/typed-waits` | its published `waits.json` of a backlog CR is written through `repo.store` (its E.1). |
| G, `1-inbox/outside-contributions-archive` | its outside archive is written through `repo.store` (through Part C). |

Pending items this CR composes with (named so they align; none is edited by this CR):

- `2-backlog/P2/one-read-interface-over-the-planning-fol`: "one module `store`, the only way the
  board, the hub and `status` read the planning folder" (records, backlog, configuration, journal),
  reading the files on each call with no cache, so an index (SQLite, Dolt) can come later behind it,
  rebuilt from the files, the files staying the truth. **This CR builds the write half of that same
  module** and only the low-level reads the conformance test needs (`read_text`, `exists`,
  `listdir`). That item then adds the read half to the same protocol and the same backends, moves
  the readers onto it, and extends the same conformance test. One package, one `PlanStore`, one
  `Repo.store`, one conformance test; no second store module. Its intent's "no behaviour or output
  changes" holds here too.
- The dedicated-branch backend (the plan on a branch of the project's repository): a CR of its own,
  later (planning-server-Q19). Not filed by this CR.

## 3. Decisions carried from `planning-server/02-answers.md` and this CR's `02-answers.md`

| Decision (date) | Where it lands |
| --- | --- |
| Everything in Markdown, browsable on the forge; a dedicated branch is acceptable, a separate planning project is better; a hidden ref and a database as the store are ruled out (11-10) | §5: both backends keep the plain files; the dedicated branch is a later backend, declared and skipped in the conformance test; §10 |
| Dolt set aside "pour l'instant"; upstream churn rules out Beads as the store (11-10) | §10 |
| A running batch's state stays local to the steering machine (11-10, planning-repo answer 4) | §4 "local file"; §5.4: local files keep `core/files.py` and are never refused |
| Messages and plan storage are two things; no Board dependency, hosted or local (11-20, Q1-Q2) | §10: Board's ideas built in chantier |
| All five Board ideas go in this work, the fifth being "the storage behind a minimal interface with one conformance test that every backend (the planning folder, a dedicated branch, a server) passes" (11-20, Q3) | this CR |
| With no server, writes are refused; no fallback (11-20, Q5) | the refusal is Part C's; this CR gives it its one place, `check_publish`, called before any change (§5.4) |
| Q7: seven separate CRs; A and B first, then C, then D to G (11-20) | §2 |
| Q10: sessions write the surface's files under the CLI's locks; only the writer commits, rebases and pushes; "the other sessions talk to the Chief of Staff's session" and "thin client" superseded (11-20) | §5: every store writes the working tree directly, under the lifecycle lock (`lock()`); no write is sent to another process |
| Q11: the code's clone and worktrees never added under `projects/<name>/` (11-20) | Part C's (its C.5); here `published()` covers the planning folder only, which holds neither (§4) |
| Q17: the writer touches only `projects/` and the root `chantier.yaml` (11-20) | §4 "published path"; §5.1 `write_config`; §5.4 the board's configuration save |
| Q19: the conformance test runs on one real storage only for now; the interface stays; the test proves it the day a second backend is built; the dedicated branch becomes a CR of its own, later (11-20) | §5.3, §7 |
| This CR's answer 1: the interface adds `write_bytes(rel, data)` and `make_folder(rel, exist_ok)`; a copy and an append are a read then a write; every published write goes through the store, so Part C can refuse it; no write stays outside (11-20) | §5.1, §5.4, §7 |
| This CR's answer 2: the board's Configuration save goes through a named method, `write_config(data)`, published and checked by `check_publish`; the store's root stays the planning folder, and no path argument can leave it (11-20) | §5.1, §5.2, §5.4, §7 |
| A coherent split: each part changes the docs and SVGs (with their `-texts.md`) its change makes false, in the same CR (11-20) | §8 |

## 4. Words

- **Planning folder:** `repo.changes`: `.agents/changes/` of the project (in-project mode), or
  `projects/<name>/changes/` of the planning surface (external mode).
- **Store:** an object that implements `PlanStore` (§5.1) over one planning folder. Every path it
  takes is relative to its `root`, with forward slashes (as `repo.rel` gives them).
- **Backend:** one implementation of `PlanStore`: `folder`, `surface`, and later `dedicated-branch`.
- **Feature:** a word a backend declares in its `features`: `publishes`, `local-files`,
  `refuses-without-publisher`. The conformance test skips a case by feature, never fails it.
- **Local file:** a path of the planning folder matched by its `.gitignore` patterns, the tuple
  `IGNORED` of `core/files.py` (`batch.json`, `events.jsonl`, `brief.md` of `4-batch/`, the STATUS
  files, the locks, `seat.json`, the journals, `work/gates/`, `work/scratch/`, logs, ...). Never
  published, never refused.
- **Published path:** in the reference's words, a path of the surface's working tree that git does
  not ignore, under `projects/` or the surface root's `chantier.yaml` / `chantier.yml`, and not under
  a path a project's `checkout.yml` names. Inside the planning folder, which is all a store's
  `published()` answers for: every path not matched by `IGNORED`.
- **Published write:** a CLI or board write that creates, changes, moves or deletes a published
  path.
- Not "server", "writer", "sync", "commit" or "push" for anything this CR builds: the store writes
  files and knows no git. The writer is Part C's word.

## 5. What changes

### 5.1 The package `store/` and its protocol

New package `skills/chantier/scripts/cli/src/chantier/store/`, with `__init__.py`, `base.py`,
`folder.py`, `surface.py`.

`base.py` holds the protocol `PlanStore` (a `typing.Protocol`) and the feature words:

- `root: Path`: the planning folder (`repo.changes`). Every `rel` argument of every method is a
  path relative to it, and none can leave it: an absolute path, a drive, a NUL, or a path that
  resolves outside `root` (`..`, a symlink out) is refused before anything is read or written, with
  the text `core/repo.project_path` gives today (`path must be inside the planning folder: <rel>`,
  exit 1). This is a guard against a code fault: the commands already check their paths.
- `features: frozenset[str]`: among `publishes`, `local-files`, `refuses-without-publisher`.
- `read_text(rel) -> str`: as `core/files.read_text` (UTF-8, a byte-order mark read through).
- `exists(rel) -> bool`.
- `listdir(rel) -> list[str]`: the names directly in a folder, sorted.
- `write_text(rel, text)`: atomic (a reader never sees half a file), UTF-8 without a byte-order
  mark, the text's line endings written as given (`\n` stays `\n` on Windows), parents created:
  as `core/files.write_file` today.
- `write_json(rel, data)`: as `core/files.write_json` today, the same bytes (indent 2, a final
  newline, its `ensure_ascii` keyword kept, since `summaries/store.py` and
  `core/batch_records.write_record` write with `ensure_ascii=False`).
- `write_bytes(rel, data)` (this CR's answer 1): atomic, the bytes written as given (a byte-order
  mark or CRLF kept), parents created: as `core/files.write_bytes` today.
- `make_folder(rel, exist_ok)` (answer 1): creates the folder and its parents; with `exist_ok`
  false, refused when the folder exists, changing nothing (`new_request`'s exclusive
  `folder.mkdir()` today; its caller keeps its own refusal text, `CR folder already exists: ...`,
  exit 2, by catching the store's `FileExistsError` as it catches `mkdir`'s today).
- A copy and an append are a read then a write (answer 1): the caller reads the source (a direct
  read is allowed; the read half is the P2 item's) and writes through `write_bytes` or `write_text`.
  A copy keeps the source's bytes exactly (read as bytes, written with `write_bytes`), as
  `shutil.copyfile` does today.
- `write_config(data: bytes)` (answer 2): writes the project's configuration file, atomically, the
  bytes as given. In external mode that file is `projects/<name>/chantier.yaml`, or
  `projects/<name>/chantier.yml` when that one exists and the `.yaml` does not, as
  `playbook/edit._target` picks it today: the two file names become a constant of the store, which
  `playbook/config.FILES` reuses (playbook may import core; core may not import playbook). It takes
  no path argument. The file is published. `FolderStore` has no project configuration file (in
  in-project mode the board's Configuration page is read-only): its `write_config` raises the
  board's read-only refusal, the text `playbook/edit.READ_ONLY` holds today, exit 2; the text moves
  into the store and `playbook/edit.py` imports it, unchanged. The board never reaches it: it refuses
  first, as today (`_refuse_early`).
- `move(rel_src, rel_dst)`: a file or a CR folder, across stages; refused when the target exists,
  changing nothing, with today's refusal of `core/batch.move_directory` (`refusing to overwrite CR
  folder: <path>`, exit 3), and its other refusals and their texts and exit codes kept.
- `remove(rel)`: a file or an empty folder.
- `lock()`: the context manager of the planning folder's lifecycle lock, today
  `lifecycle/stages.changes_lock`: the same file (`.lifecycle.lock`), the same OS lock
  (`core/files.try_lock`), the same 30 s wait, the same refusal (`CR lifecycle is locked for over
  30 s`). `changes_lock(repo)` stays as a name its callers use and delegates to
  `repo.store.lock()`, or its callers move to `repo.store.lock()`: the Driver judges which reads
  better; there is one lock implementation.
- `published(rel) -> bool`: false when `rel` is matched by the `IGNORED` patterns (with the
  `.gitignore` meaning of each: a leading `/` anchors at the planning folder, a trailing `/` is a
  folder and everything under it, `**/` any depth, `*` within one name), true otherwise.
- `check_publish(rels, *, config=False)`: raises a refusal (a `ChantierError`) when one of `rels`
  is published, or `config` is true (the project's configuration file, always published), and the
  store cannot publish now; returns otherwise. Part C's calls with a list only
  (`check_publish(["3-ready/x/01-intent.md"])`) stay valid. In this CR no backend refuses: both return.
  Part C gives `SurfaceStore` its refusal (exit 2, its C.8 text, which names the command).

Shape constraints the code already enforces (`tests/test_code_targets.py`, CONTRIBUTING.md):

- No import cycle, imports inside functions included. `Repo.store` lives in `core/repo.py`, so
  `store/` sits in the `core/` layer: it imports only `core/` modules (`core/files.py`,
  `core/errors.py`) and the standard library, never `lifecycle/`. This is why the lock's body moves
  from `lifecycle/stages.py` into the store (or a `core/` module the store uses), and not the other
  way round.
- The start-up imports only the standard library and chantier (`test_the_start_up_imports_only_the_standard_library_and_chantier`):
  `store/` imports no pydantic at module level.
- Files at most 400 lines, functions at most 50.

### 5.2 The backends

- `folder.py`: `FolderStore(changes: Path)`: the in-project planning folder. Features:
  `local-files`. Publishes nothing, never refuses. In-project mode is unchanged.
- `surface.py`: `SurfaceStore(repo)`: the external planning folder (`projects/<name>/changes/`),
  the same files on disk, and the project's configuration file beside it (`write_config`). Features: `publishes`, `local-files`. This is the "server" backend of the
  user's list (planning-server-Q3): Part C's writer publishes what it writes. In this CR its
  `check_publish` returns, as `FolderStore`'s does.

Both backends write the same files the same way; they differ by their features and, from Part C on,
by `check_publish`. The Driver may share the file operations between them (a common base or
functions); the protocol is what the CLI sees.

### 5.3 `Repo.store`

`Repo.store` (in `core/repo.py`): the store of the repository, chosen by `repo.external`:
`SurfaceStore(repo)` when external, `FolderStore(repo.changes)` otherwise. One store per `Repo`
(built once, kept on the object). `Repo.find(readonly=True)` (the board, `validate`) returns a
`Repo` whose store writes nothing by itself: building the store creates no file and no folder.

### 5.4 Every published write goes through `repo.store`, checked first

Every published write of the CLI goes through `repo.store`, and each command calls
`repo.store.check_publish(<every published path it will touch>)` **before it changes anything**,
so that from Part C on a refused command leaves the planning folder and the batch's record as they
were. For a move, both the source and the target are touched paths.

The commands and code sites, as the code is today (the reference's list, with where each writes):

| Command | Today's write site(s) | Published paths |
| --- | --- | --- |
| `file` | `commands/intake.file_cr` → `lifecycle/backlog.file_idea` → `lifecycle/filing.new_request` | the new `1-inbox/<slug>/` (`make_folder`, `exist_ok` false) and its `intake/request.md`, kept as received (`write_bytes`) |
| `triage` | `lifecycle/backlog.move_item` → `lifecycle/stages.move_backlog_item` → `core/batch.move_directory` | the CR folder, source and target |
| `abandon`, `restore` | `commands/intake.py` (`move_directory` to and from `6-trash/`; `restore`'s `_remember` → `lifecycle/moveout.remember_cr`) | the CR folder, source and target; `restored.json`; the line `formerly <CR> of <batch>` appended to the folder's `01-intent.md` (or `notes.md`): read, then `write_text` with the line added |
| `init` | `commands/intake.py` (the stage folders) | the stage folders it creates (`make_folder`, `exist_ok` true) |
| `open` | `core/batch.py` (`Batch.move`), `core/batch_records.reserve_record` | the CRs' folders moved into `4-batch/1-pending/`; `5-archives/batches/batch-NN.json` |
| `take`, `handback` | `core/batch.py` (`Batch.move`, `consume`), `lifecycle/stages.start_cr`, `done_cr` | the CR folder's moves; a consumed published file |
| `order` (each kind that moves or writes a CR's folder: `add`, `merged`, `drop`) | `commands/orders*.py`, `lifecycle/stages.done_cr` (`delivery.md` in external mode), `trash_cr`, `lifecycle/moveout.py` (`formerly.json`), `commands/crs.filed_fix` (a fix's `03-change-spec.md` copied into a new inbox folder) | the CR folders moved; `delivery.md`; `formerly.json`; the fix's new inbox folder and its `03-change-spec.md` (a copy: the source's bytes, `write_bytes`) |
| `cancel` | `commands/release.py` and what it calls | the CR folders it moves |
| `close` | `commands/close_archive.archive_and_delete`, `core/batch_records.write_close` and `undo_close` | each `3-done` CR renamed into `5-archives/`; `batch-NN.md` and `batch-NN.json`; the final pages written where the CRs are now; on a failure, the record's old bytes put back (`write_bytes`) or the record removed (`remove`) |
| `summary set`, `summary label`, `summary group` | `summaries/store.write` (the CR's `summary.json`), through `commands/summary.py` and `summaries/edit.py` | each `summary.json` written |
| `verdict` | when it writes in a CR's folder | what it writes there |
| the release commands that write the archive | `commands/release.py` and what it calls | what they write in the planning folder |
| the board's backlog writes | `board/write_api.py` through `lifecycle/backlog.py` (`file_idea`, `move_item`, `edit_markdown`, `declare_next_batch`) and `summaries/edit.py` (labels, groups) | the inbox folder; the moves; the edited Markdown file, in its own line endings (`write_bytes`); `next-batch.json`; `summary.json` |
| the board's Configuration save | `board/config_api._put` → `playbook/edit.edit_surface_file` | the project's configuration file, through `write_config`, after `check_publish([], config=True)` |

The Driver reads each command's code and lists every published write it makes; a published write
of the CLI found outside this table goes through `repo.store` too and joins the table and its test
(§7). Parts D and E add their own published writes later through the same store (a QA order's lease
is local; a backlog CR's `waits.json` is published).

Local files (`batch.json`, `events.jsonl`, `brief.md`, STATUS files, locks, the journals,
`seat.json`, `.batch-number`, `.closing-*`, the gate files) may keep `core/files.py`'s functions
directly; they are never refused. `status/write.py` (STATUS files) and `hub/journal.py` are not
changed by this CR.

### 5.5 Messages

None new, none changed. Every output line and refusal of the commands in §5.4 stays byte for byte;
the store's refusals are today's (§5.1).

## 6. Host and default matrix

None: the store depends neither on the host (Claude Code, Copilot) nor on a configured value. It
runs on Linux, macOS and Windows as `core/files.py` does today (atomic replace with
`core/files.retry`, `msvcrt` and `fcntl` locks, UTF-8, LF kept); `just check` on the three systems
proves it.

## 7. Evidence

- `skills/chantier/scripts/cli/tests/test_store_conformance.py` (new): one test body parametrized
  over the backends `folder`, `surface` and `dedicated-branch`, the last skipped with the reason
  `dedicated-branch backend: a later CR (planning-server-Q19)`. A case whose feature the backend
  declares absent is skipped by feature, never failed. Each backend on a prepared planning folder
  (`tmp_path`; `surface` on a prepared external surface, `projects/<name>/changes/`):
  - UTF-8 round trip of a text with non-ASCII letters (`é`, `ü`, `日本`): `write_text` then
    `read_text` gives it back; the file's bytes start with no byte-order mark; a text with `\n`
    only is written with `\n` only on every system;
  - `write_json` then `read_text` gives the same JSON;
  - `move` of a CR folder from `2-backlog/P3/` to `3-ready/` keeps every file's bytes; a move onto
    an existing folder is refused and changes nothing (both trees' fingerprints unchanged);
  - `remove` of a file, and of an empty folder;
  - `write_bytes` then a byte read gives the same bytes, a byte-order mark and CRLF included;
  - `make_folder` with `exist_ok` false creates a folder and is refused on an existing one, which
    stays as it was; with `exist_ok` true it returns on an existing one;
  - every method refuses a `rel` that leaves the root (`../x`, an absolute path, a drive on
    Windows) with exit 1 and writes nothing outside;
  - `write_config`: on `surface`, writes `projects/<name>/chantier.yaml` with the given bytes, and
    writes `chantier.yml` instead when only that one exists; on `folder`, raises the read-only
    refusal and writes nothing;
  - `lock` is exclusive: a second `lock()` from another thread waits while the first holds it, and
    times out with the lifecycle lock's message. The test does not wait 30 s: it shortens the
    wait through the lock's named constant (monkeypatched), so `just test` stays in its budget;
  - `published` agrees with `IGNORED` for `seat.json`, `4-batch/batch.json`, `work/gates/x.log`
    (local) and `3-ready/x/01-intent.md`, `5-archives/batches/batch-01.json` (published);
  - `check_publish` returns for published and local paths alike, and with `config=True` (no
    backend refuses in this CR);
  - `refuses-without-publisher`: declared by no backend here, so skipped on both; Part C runs it on
    `surface` (its §6: with no live writer `check_publish(["3-ready/x/01-intent.md"])` raises exit 2
    with its C.8 text, `check_publish(["4-batch/batch.json"])` returns; with a live writer, both
    return). The case's body is written here, keyed on the feature, so Part C only declares the
    feature and gives the refusal.
- A test over the command table of §5.4 (in the same file or a sibling the Driver names), on a
  prepared external surface: parametrized over the table's rows, each command run in-process (as
  the tests call the CLI today) with a spy store on `repo.store` that records every call in order:
  `check_publish` is called with every published path the command then touches (and
  `config=True` for the Configuration save), before the first `write_text`, `write_json`,
  `write_bytes`, `make_folder`, `write_config`, `move` or `remove`; and the command makes no
  published write outside the store (every published path changed in the surface's tree, by its
  fingerprint before and after, is one the spy recorded). Part C turns the same table into its refusal test,
  `test_surface_writes.py`. The board's two rows are driven through their routes, as
  `test_board.py` and `test_board_config.py` drive them today.
- The existing suite passes unchanged: no output, file or refusal moves (`tests/test_triage_moves.py`,
  `test_external_archive.py`, `test_opening_and_restore.py`, `test_board.py`, `test_board_config.py`,
  `test_batch_end.py`, `test_summary_lint.py`, ...). A test that patched `changes_lock` or
  `core/files` writes for a published path is updated to the store only where it must.
- No shipped file is guarded by a new check (the conformance test reads `IGNORED` from the code
  under test, not a copy).
- The project's gates, AGENTS.md: `just check` (Linux, macOS, Windows); `just test` within its
  budget (at most 30 s above 18.5 s); `just eval-dry-run` (a change under the CLI's `src/`); `just
  scenario`, green on the pipeline's `just scenario (ubuntu-latest)` job before the PR (a change to
  the CLI), and locally on Windows (`chantier gate`) when this CR is the top of its batch's stack.
  No scenario step is added: the behaviour does not change. No CI job is added or changed.

## 8. Docs and diagrams

- `README.md`, `docs/` and the SVGs: none change. Searched for who writes the planning folder and
  for any name of the write path: `docs/planning-folder.md` (the CLI rewrites the STATUS files, an
  agent writes `summary.json` through `summary set`, `validate` writes nothing, the folder moves and
  is never copied), `docs/planning-modes.md` and `docs/web-board.md` (the board's backlog writes and
  its Configuration page). This CR changes no behaviour they describe: the same files, the same
  commands, and no refusal. No page, diagram (`docs/*.svg`) or `docs/*-texts.md` names a store or
  the write path (searched for `store`, `PlanStore`, `write`); the refusal with no writer is Part
  C's, documented in its C.14. In the reference's docs map (§2), Part B touches no file.
- `CONTRIBUTING.md`, the layers paragraph ("`core/` (errors, files, clock, git, the JSON records as
  pydantic models, the repository, the batch, the seat), then the domain modules ..."): it names
  what each layer holds; the new package `store/` is added to the `core/` layer's list ("the
  plan's store"), so the sentence stays true of the code.
- Cards: none change. The store is internal; no card names a write path or `changes_lock`.

## 9. Rollout

- No user-visible change; nothing to set up, nothing to migrate: the files on disk are the same.
- Mixed versions: none to weigh; two chantier versions on one planning folder write the same files
  under the same lock file.
- The release notes are written at release time (`docs/release-notes/<date>-vX.Y.Z/`, CONTRIBUTING.md);
  this CR writes none. Released alone, it is internal work; its value shows with Part C.

## 10. Out of scope

- The read half of `store` (records, backlog, configuration, journal) and moving the board, the hub
  and `status` onto it: `2-backlog/P2/one-read-interface-over-the-planning-fol`.
- Any refusal: `refuses-without-publisher` and `SurfaceStore`'s refusal are Part C's
  (`planning-server`, its C.8).
- The dedicated-branch backend: a CR of its own, later (planning-server-Q19).
- An index or cache behind the store (SQLite, Dolt): Dolt set aside (11-10); the P2 item names an
  index as later.
- Beads, Vercel Board (hosted or local, its `Backend` interface or `vb conformance`), a database or
  a hidden ref as the store (11-10, Q1-Q2).
- Git in the store: the store writes files and runs no git; committing and pushing is Part C's
  writer.
- Local files (§5.4): they keep `core/files.py`.

## 11. Open questions for the user

None. The two open points of the first draft are settled in this CR's `02-answers.md`.
