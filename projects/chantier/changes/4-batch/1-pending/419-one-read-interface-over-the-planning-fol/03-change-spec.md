# Change Specification: the plan's store reads the planning folder

Origin: verbal (2026-11-18, split from `surface-server-one-elected-process-for-t`; grilled
2026-11-20 by the Chief of Staff alone, on the user's word). No tracker issue.

This file carries the intent and every answer of `02-answers.md`; a Driver needs nothing else.

## 1. Goal, in the user's terms

The surface server "lit les fichiers mais on va bientot lui donner une persistance pour etre plus
rapide (dolt?)"; "poser des bases solides pour permettre ca plus tard".

The base is one way to read the planning folder: the plan's store (`store/`, `PlanStore`,
`Repo.store`), which CR-402 built for the writes. This CR gives it its read half and moves onto it
the board, the hub and `status`, so that an index (SQLite, Dolt) can come later behind the store,
rebuilt from the files. The files stay the truth, in Markdown and JSON browsable on the forge.

Today the store reads the files on each call and keeps no cache. That stays. **No index is built.
No behaviour and no output changes.**

## 2. What is there at main (measured 2026-11-20, `4ed0d56c`)

CR-402 (`plan-store-interface`, merged) and CR-404 (`planning-server`, merged) are in. The store
is the write interface: `PlanStore` in `store/base.py`, `FolderStore` in `store/folder.py`,
`SurfaceStore` in `store/surface.py`, `Repo.store` in `core/repo.py`, the conformance test
`tests/test_store_conformance.py`. It has three reads, `read_text(rel)`, `exists(rel)` and
`listdir(rel)`, which no reader calls: they serve the conformance test.

Every reader still reads the files directly. Calls of a `Path` or `os` read (`read_text`,
`read_bytes`, `open`, `iterdir`, `glob`, `rglob`, `is_file`, `is_dir`, `exists`, `stat`,
`os.walk`, `os.scandir`), the reads of other places included:

| Where | Calls |
| --- | --- |
| the CLI's 239 modules (the web client apart) | 336 |
| the 165 modules that `board/`, `hub/` and `status/` import, directly or not | 269 |
| `board/` | 44 |
| `status/` | 21 |
| `core/repo.py` | 17 |
| `hub/` | 16 |
| `core/surface_batches.py` | 1 |
| `commands/cost/` | 0 (it reads through `core/batch.read_batch` and `core/records.read_events`) |

`autosync/reading`, named by the intent, no longer exists. So CR-402 did none of the read half:
this CR builds it (answer 1).

All paths below are under `skills/chantier/scripts/cli/src/chantier/` unless they start with
`tests/` (`skills/chantier/scripts/cli/tests/`) or name a root file.

## 3. Decisions carried from `02-answers.md`

All settled by the Chief of Staff (2026-11-20, the user asks no questions).

| Answer | Where it lands |
| --- | --- |
| 1. The whole read half is left: the protocol's reads and every reader's move | §2, §5 |
| 2. File-level reads on the same `PlanStore` and the same two backends; no second module, no typed query; the parsers stay where they are and take their bytes from the store | §5.1, §5.2 |
| 3. No cache, no index: each call reads the files | §5.1, §9 |
| 4. The readers moved here: `board/`, `hub/`, `status/`, `commands/cost/`, `core/surface_batches.py`, `core/repo.py` and the record readers they call; the rest is split out to `1-inbox/store-reads-rest` | §5.3, §5.4, §9 |
| 5. `autosync/reading` no longer exists; `autosync/records.py` reads the git folder, not the planning folder: not touched | §5.5 |
| 6. The configuration is not read through the store here; carried to `store-reads-rest` | §9 |
| 7. Reads of other places in the moved modules stay direct, each named by the structure test with its reason | §5.5, §6 |
| 8. Local files are read through the store like the published ones; their writes and appends stay | §5.3, §5.4 |
| 9. A read refuses a path outside the planning folder as a write does; the board's own answers stay | §5.1 |
| 10. Another project's batch is read through a store over that project's planning folder | §5.3 |
| 11. The structure test is static, over the moved modules; a prepared text proves it fails; the run-time proof goes with `store-reads-rest` | §6 |
| 12. No output change, proved by the existing tests left unchanged; no scenario step, no card, no CI job | §5.6, §6 |
| 13. The time of one board state and of `status` is measured before and after and stated in the PR; more than 10 % slower is fixed in this CR | §6 |
| 14. Docs: `CONTRIBUTING.md` only | §7 |

## 4. Words

- **Planning folder:** `repo.changes`: `.agents/changes/` of the project, or
  `projects/<name>/changes/` of the planning surface. It is the store's `root`.
- **Read:** anything that learns what is in the planning folder: a file's text or bytes, whether
  a path exists and what it is, a folder's names, a file's size and modification time.
- **Direct read:** a read made with `pathlib`, `os`, `open` or `core/files.py`'s readers, not
  through a store.
- **Store-only module:** a module of the list in §5.3 and §5.4: after this CR it makes no direct
  read of the planning folder.
- **Local file**, **published path:** as CR-402 defined them (`core/files.IGNORED`). A read is
  the same for both.

## 5. What changes

### 5.1 The protocol's reads (`store/base.py`)

`PlanStore` gains its read half. Every `rel` is relative to `root`, with forward slashes, and is
checked by the same guard as a write (`store/base.guard`): an absolute path, a drive, a NUL, or a
path that resolves outside the root is refused before anything is read, with the same text
(`path must be inside the planning folder: <rel>`) and the same exit code (answer 9). The root
itself (`""` or `"."`) is allowed where a folder is read.

| Method | What it gives | As today's |
| --- | --- | --- |
| `read_text(rel, errors="strict") -> str` | the file's text, UTF-8, a byte-order mark read through, retried on Windows; `errors` as `str.decode` takes it (`"replace"` for a damaged file) | `core/files.read_text(path, errors)`; the existing method gains `errors` |
| `read_bytes(rel, limit=None) -> bytes` | the file's bytes as they are; with `limit`, at most that many, without reading the rest | `Path.read_bytes`; `board/files._head` (1 MB) |
| `exists(rel) -> bool` | kept | `Path.exists` |
| `is_file(rel) -> bool`, `is_dir(rel) -> bool` | following a symlink | `Path.is_file`, `Path.is_dir` |
| `listdir(rel) -> list[str]` | kept: the names directly in a folder, sorted | `Path.iterdir` |
| `glob(rel, pattern) -> list[str]` | the names directly in the folder `rel` that match `pattern` (one level, `*` `?` `[...]`), sorted; an absent folder gives `[]`; the match is `Path.glob`'s on the system it runs on (its case rule on Windows included) | `Path.glob("*.md")`, `glob("batch-*.json")`, `glob("P[1-4]")` |
| `stat(rel) -> (size, mtime_ns) or None` | the size and the modification time in nanoseconds, following a symlink; None when the path is absent or cannot be read | `Path.stat` in `board/fingerprint.py`, `board/api/topics.py`, `board/files.py` |
| `walk(rel)` | as `os.walk`, top-down: `(folder's rel, folder names, file names)`, the folder names editable in place to prune, no symlinked folder entered; an absent folder gives nothing | `os.walk` in `board/backlog.count_files`, `board/files._listed`; `os.scandir` in `board/fingerprint._walk`; `rglob("*")` in `status/views._backlog` |

Rules:

- A missing file or folder raises what the direct read raises today (`FileNotFoundError`, an
  `OSError`), so each caller's `except` keeps its meaning; only a path outside the root raises
  the store's refusal.
- No cache: each call reads the files; nothing is kept between two calls (answer 3). The
  protocol's docstring says it: "reads the files on each call; an index may come later behind
  this interface, rebuilt from the files".
- The Driver may add one more listing read (a folder's tree with each entry's size and time in
  one call) when the measure of §6 asks for it; it then has its conformance case. No other read
  is added: a typed query (`records()`, `backlog()`) is not built (answer 2).
- The store's own shape rules stay (CR-402): `store/` imports only `core/files.py`,
  `core/errors.py` and the standard library (and `writer/lines.py`, as `store/surface.py` does
  today), never `core/repo.py`, and no pydantic at module level; files at most 400 lines,
  functions at most 50; no import cycle.
- `rglob("*")` in `status/views._backlog` follows a symlinked folder on Python 3.11 and 3.12 and
  not on 3.13 and later. Through `walk` it follows none on every version. This is the one place
  where the count of a CR's files can differ from today, on Python before 3.13, for a CR folder
  that holds a symlink to a folder; it is accepted and named in the PR's Known gaps.

### 5.2 The backends

`FolderStore` (`store/folder.py`) implements the reads over the files; `SurfaceStore`
(`store/surface.py`) inherits them unchanged. Both declare the same features as today. A read
never calls `check_publish` and is never refused for a missing writer: with no writer running, the
board, the hub and `status` read as today.

### 5.3 The readers moved: the three packages, `Repo` and the other batches

In each module below, every direct read of the planning folder goes through the project's store
(`repo.store`, or a store passed by the caller). The values computed and the bytes printed stay.

- `board/`: `state.py` (`_history`: the records of `5-archives/batches/`), `backlog.py`
  (`_candidates`, `description`, `count_files`, `depends_of`, the `02-answers.md` look),
  `archived.py`, `crs.py`, `files.py` (`_listed`, `tree`, `read`, `_head`), `fingerprint.py`
  (`_entry`, `_walk`, `fingerprint`), `journal.py` (`_lines`, `since_rescan`), `api/ops.py`,
  `api/topics.py` (`_journal`, `_entries`: the journals' size and time), `write_api.py` (the
  `03-change-spec.md` look, the edited file's bytes for its checksum), `projects.py` (the
  planning folder's own existence), `config_api.py` (`_open_batch`).
  - `core/files.inside`, called by `board/files.py`, `board/api/ops.py` and `board/write_api.py`,
    keeps the board's own answers (answer 9): a path outside the folder, an absent one or a lock
    gives 404, never the store's refusal; a symlink out is not served. `board/files.py` keeps its
    own check of each file's real place (`Path.resolve`, no read).
  - `board/fingerprint.py` keeps its promise: a walk of sizes and times, no file opened, the same
    hash for the same folder state as before this CR is not required (the hash is never stored),
    but the same hash for an unchanged folder between two calls is.
- `hub/`: `batch_prs.py` (`running_batch`), `watch.py` (`open_batch`), `journal.py` (`read`: the
  lines of `forge-journal.jsonl`).
- `status/`: `views.py` (the CR's documents and gate logs, `shown_title`, `spec_state`,
  `_backlog`, the stage scans, a CR's `STATUS.json`), `write.py` (the `is_dir` looks).
- `commands/cost/`: it has no direct read; it joins the list so it gains none.
- `core/repo.py`: `batch_folders`, `batch_ids`, `open_batches`, `paused_batches` and
  `next_batch_number` (`.batch-number`, the records of `5-archives/batches/`, `4-batch/batch.json`)
  read through `self.store`.
- `core/surface_batches.py`: another project's `4-batch/batch.json` is read through a store over
  that project's planning folder (`projects/<name>/changes/`), the same backend as the session's
  own (answer 10); building it creates no file. The line printed stays, `batch.json unreadable`
  included.

### 5.4 The record readers they call

These readers take a store (the Driver picks the signature: a store and a `rel`, or a `Repo`) and
read through it; every caller in the CLI passes it, the callers outside §5.3 included
(`read_batch_json` has 24 call sites, `read_events` 15, `read_seat` 8, `summaries/store.read` 7,
`waits.read_file` 5). A caller outside §5.3 changes only how it calls the reader.

- `core/records.py`: `read_batch_json`, `read_events`, `read_restored_number`.
- `core/seat.py`: `read_seat`.
- `core/waits.py`: `read_file`.
- `core/batch_records.py`: `read_record`, `last_closed`, `read_retro`.
- `summaries/store.py`: `read`, `read_or_new`; `summaries/view.py`: `summary_view`.
- `core/files.title_source` (a CR folder's title): it reads through a store; where it lives is
  the Driver's choice within the layers (`core/files.py` may not import the store's users).
- `core/records.py`'s `core/files.read_json` use goes with `read_batch_json`.

A message that prints a file's full path keeps it byte for byte (`<path> is not a valid batch
record: ...`, `<path> is not valid JSON: ...`): the path is the store's `root` joined to the
`rel`, as the caller built it today.

The writes and appends of local files (`batch.json`, `events.jsonl`, the journals' `open("ab")`,
the STATUS files in `status/write.py`) stay as CR-402 left them (answer 8).

### 5.5 What stays a direct read

Reads of other places, in the store-only modules, stay as they are (answer 7), each named in the
structure test with its reason:

- `core/repo.py`: `checkout.yml` and `project.md` (the project's folder, beside the planning
  folder), `surface_projects` (the surface's `projects/`), the looks made before a store exists
  (`Repo.find`, `_external`), the clone (`missing_clone`).
- `board/static.py`, `board/command.py`: the web client's files. `board/key.py`: the key in the
  git folder. `board/address.py`: an HTTP address. `board/state.py`: the code repository's folder
  (`origin_of`). `board/config_api.py`: the project's configuration file (`config_path`).
- `hub/state.py`, `hub/lock.py`: the git folder (`chantier/server.json`, the locks).

Not touched at all: `autosync/records.py` (the old autosync tool's state folder in the git
folder, answer 5), `playbook/` and `plugin_files.py` (the configuration, answer 6), `costs/` (the
hosts' transcripts), `writer/`, and every module of §9's split-out item.

### 5.6 Messages, cards, CI

No message is added or changed; no command's output moves. No card changes: no card names who
reads the planning folder. No CI job is added or changed. No host and default matrix: nothing
here depends on the host or on a configured value.

## 6. Evidence

- `tests/test_store_conformance.py`, extended, on both backends (`folder`, `surface`;
  `dedicated-branch` stays skipped):
  - `read_text` with `errors="replace"` reads a file with a byte that is not UTF-8, and raises
    without it; a byte-order mark is read through;
  - `read_bytes` gives the bytes written, a byte-order mark and CRLF included; with `limit`, the
    first `limit` bytes of a longer file;
  - `is_file` and `is_dir` on a file, a folder and an absent path;
  - `glob` gives the sorted matching names of one level, and `[]` for an absent folder;
  - `stat` gives the size written and a time that moves after a rewrite, and None for an absent
    path;
  - `walk` gives every folder and file of a small tree, and skips a folder pruned in place;
  - a missing file raises `FileNotFoundError` from `read_text` and `read_bytes`;
  - `test_every_method_refuses_a_path_outside_the_root` gains every new read; nothing is written
    outside;
  - a read on `surface` with no live writer returns (it is never refused);
  - two calls with a rewrite between them give the new content (no cache).
- `tests/test_store_reads.py` (new), the structure test (answer 11). It parses with `ast` the
  source of the store-only modules, read from the repository as it ships at the head under test
  (`src/chantier/`, never a copy): the packages `board/`, `hub/`, `status/`, `commands/cost/` and
  the modules `core/repo.py`, `core/surface_batches.py`, `core/records.py`, `core/seat.py`,
  `core/waits.py`, `core/batch_records.py`, `summaries/store.py`, `summaries/view.py`. It fails,
  naming the module, the function and the line, on:
  - a call of `read_text`, `read_bytes`, `iterdir`, `glob`, `rglob`, `is_file`, `is_dir`,
    `exists`, `stat`, `lstat`, `open` (a literal mode that writes or appends apart), `os.walk`,
    `os.scandir`, `os.listdir` or the builtin `open`, whose receiver is not a store;
  - an import of `core/files.py`'s `read_text` or `read_json`. `core/files.inside`, which
    `board/files.py`, `board/api/ops.py` and `board/write_api.py` call to turn a route's path into
    a file or a 404, stays: it is the board's own guard (§5.3), and what they then read of that
    file goes through the store.
  How the test knows a store's call (the receiver's name, or a marker) is the Driver's choice. The
  exemptions of §5.5 are a table in the test, one entry per module and function with its reason;
  an exemption that no longer matches a call fails the test, so the table stays true. One more
  case runs the same check on a prepared source text that holds a direct read and asserts it is
  found: a refusal the shipped files cannot hold, paired with the check on the shipped files above.
- The existing suite passes with no expected output changed (answer 12): `test_board*.py`,
  `test_server_api*.py`, `test_surface_batches.py`, `test_forge_hub*.py`, `test_watch*.py`,
  `test_cost*.py`, `test_titles.py`, `test_summary_lint.py`, `test_waits.py`,
  `test_store_command_table.py`, `test_surface_writes.py`, `test_code_targets.py`. A test that
  calls a reader of §5.4 with a path is updated to the new call only; `tests/store_spy.py`'s `Spy`
  passes the reads through (`__getattr__`) as it does today.
- Speed (answer 13), stated in the PR with both figures, same machine, before and after: the time
  of one `board/state.project_state` and of one `chantier status`, on a prepared planning folder
  of at least 200 CR folders in the backlog (built in a temporary folder, outside the test suite).
  More than 10 % slower is fixed in this CR (the guard resolved once per walk, a `rel` built
  without resolving, the one listing read §5.1 allows), not accepted.
- The project's gates (AGENTS.md): `just check` on Linux, macOS and Windows; `just test` within
  its budget (at most 30 s above 18.5 s), the PR stating the time it adds; `just eval-dry-run` (a
  change under the CLI's `src/`); `just scenario`, green on the pipeline's
  `just scenario (ubuntu-latest)` job before the PR, and locally on Windows (`chantier gate`) when
  this CR is the top of its batch's stack. No scenario step is added: the behaviour does not change.

## 7. Docs

- `CONTRIBUTING.md`, after the layers paragraph ("The code of `src/chantier/` is in layers ..."):
  one sentence for the rule and its test: the modules listed in `tests/test_store_reads.py` read
  the planning folder only through the plan's store (`Repo.store`); a new module of `board/`,
  `hub/` or `status/` follows it.
- `README.md`, `docs/`, the SVGs and their `-texts.md`, the cards, `AGENTS.md`: none change. The
  Driver searches them for a sentence this CR makes false ("reads the files", `store`) and says in
  the PR that none was found, or changes the one it finds.

## 8. Rollout

Nothing to set up, nothing to migrate: the files on disk are the same and are read the same. Two
chantier versions on one planning folder read and write the same files. This CR edits many files
of `board/`, `hub/`, `status/` and `core/`; a CR of the same batch that edits them rebases on it or
it on that one, with no dependency declared for it.

## 9. Out of scope

- An index or a cache behind the store (SQLite, Dolt), and any typed query on the store.
- The other modules that read the planning folder: `lifecycle/`, `core/batch.py`,
  `core/leases.py`, `gate_queue.py`, `gate_slots.py`, the rest of `summaries/` (`sources.py`,
  `gaps.py`, `origin.py`, `title.py`), `rails.py`, `history.py`, `commands/`; the run-time proof
  that the board, `status` and the hub open no file of the planning folder outside the store; and
  the configuration's files. All three are the inbox item `1-inbox/store-reads-rest`, filed
  2026-11-20. Until it is done, the board, the hub and `status` still reach those modules' direct
  reads; the structure test's list says exactly which modules are store-only.
- The writes: CR-402's; none moves here.
- `autosync/records.py`, `costs/`, `writer/`, the git folder's files, the web client.
- The dedicated-branch backend (planning-server-Q19).

## 10. Open questions for the user

None. The fourteen points are settled in `02-answers.md` (2026-11-20, by the Chief of Staff, the
user asking no questions).
