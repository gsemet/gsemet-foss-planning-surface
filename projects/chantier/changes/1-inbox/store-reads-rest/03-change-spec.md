# Change Specification: the last readers onto the store, run-time proof

Origin: verbal (2026-11-20, split from `one-read-interface-over-the-planning-fol`, CR-419, merged
2026-11-21 in PR 394). No tracker issue. Not grilled: the user delegated the night's
specification questions on 2026-11-21 ("plus de question"). Every open choice is a numbered
question in §11 (`store-reads-Q1`...), recommendation first; the text below is written on each
recommendation and is **provisional** where it cites one.

This file carries the intent (`01-intent.md`) and the answers of CR-419 that bind this item; a
Driver needs nothing else. There is no `02-answers.md`.

## 1. Goal, in the user's terms

The surface server "lit les fichiers mais on va bientot lui donner une persistance pour etre plus
rapide (dolt?)"; "poser des bases solides pour permettre ca plus tard" (CR-419's intent). CR-419
made the plan's store (`store/`, `PlanStore`, `Repo.store`) the one way the board, the hub and
`status` read the planning folder themselves; but they still call modules that read it directly
(`lifecycle/`, `core/batch.py`, the gate's files, `summaries/`). This CR moves those modules onto
the store and proves, at run time, that the board, `status` and the hub open or list no file of
the planning folder outside the store. Then an index can come behind the store and serve the
three of them whole.

**No index, no cache. No behaviour and no output changes.** One batch CR of at most 3 rounds.

## 2. What is there at main (measured 2026-11-21, `33d10454`)

Counted with `tests/test_store_reads.py`'s own finder (`direct_reads`) over every module not yet
in its list (the web client apart), the reads of other places included: 247 calls in 57 modules.
Of these, the modules that `board/`, `hub/` and `status/` import, directly or not, hold 174; the
ones that read the planning folder are:

| Module | Calls |
| --- | --- |
| `lifecycle/stages.py` | 17 |
| `lifecycle/layout_check.py` | 17 |
| `lifecycle/backlog.py` | 12 |
| `lifecycle/running_batch.py` (new since the request) | 11 |
| `core/batch.py` | 8 |
| `core/leases.py` | 6 |
| `commands/crs.py` | 6 |
| `summaries/sources.py` 4, `gaps.py` 3, `origin.py` 3, `title.py` 3 | 13 |
| `gate_queue.py` 3, `gate_slots.py` 3 | 6 |
| `rails.py` | 2 |

The rest of the 174 read other places: `playbook/` and `plugin_files.py` (the configuration and
the plugin's files), `costs/` (the hosts' transcripts), `autosync/records.py` (the git folder),
`writer/` and `core/git.py` (git), `core/files.py` (the helpers themselves), `store/` (the store).

Not reached by the three: `lifecycle/links.py` 4, `lifecycle/moveout.py` 4, `history.py` 1, and
`commands/`: 60 calls in 20 modules (`opening.py` 7, `close_archive.py`, `closing.py`,
`delivery.py`, `facts.py` 5 each, `gate.py`, `permissions.py` 4 each, `came_back.py`,
`gate_run.py`, `intake.py`, `joining.py`, `rules.py` 3 each, `preflight.py`, `waits.py` 2 each,
`driver_notes.py`, `endpause.py`, `opening_record.py`, `release.py`, `summary.py`, `validate.py`
1 each), some of them reads of other places (`settings.json`, `AGENTS.md`, a worktree).

The request's `lifecycle/filing.py` and `lifecycle/session.py` make no direct read today.

All paths below are under `skills/chantier/scripts/cli/src/chantier/` unless they start with
`tests/` (`skills/chantier/scripts/cli/tests/`) or name a root file.

## 3. What this CR takes (provisional, store-reads-Q1)

What fits one batch CR of 3 rounds (CR-419 moved about 100 calls in 3 rounds): everything the
board, `status` and the hub reach, and the run-time proof that needs it. So:

- moved: the whole `lifecycle/` package (its 65 calls: the 57 reached, and `links.py` and
  `moveout.py`'s 8 so the package joins the list whole), `core/batch.py`, `core/leases.py`,
  `gate_queue.py`, `gate_slots.py`, `rails.py`, `summaries/sources.py`, `gaps.py`, `origin.py`,
  `title.py`, `commands/crs.py`, and `history.py` (1 call, named by the request): 107 calls;
- the run-time proof (§6);
- the configuration's answer (§5.5, store-reads-Q3), which moves nothing on its recommendation.

Left, not built and not filed by this CR: the other 20 modules of `commands/` (60 calls).
Whether they become an inbox item is store-reads-Q2.

## 4. Decisions carried from CR-419's answers

CR-419's answers (2026-11-20, settled by the Chief of Staff, the user asking no questions) that
bind the readers it split out:

| CR-419 answer | Here |
| --- | --- |
| 2. File-level reads on the same `PlanStore` and the same two backends; no typed query; the parsers stay where they are and take their bytes from the store | §5.1 |
| 3. No cache, no index: each call reads the files | §5.1, §10 |
| 6. The configuration was not read through the store; carried here as a point to judge | §5.5, Q3 |
| 7. Reads of other places in a moved module stay direct, each named in the structure test with its reason | §5.4 |
| 8. Local files are read through the store like the published ones; their writes and appends stay | §5.2 |
| 9. A read refuses a path outside the planning folder as a write does | §5.1 |
| 11. The run-time proof goes with this item, since it passes only when every reader it observes has moved | §6 |
| 12. No output change, proved by the existing tests left unchanged; no scenario step, no card, no CI job | §5.6, §7 |
| 13. One board state and one `status` are timed before and after; more than 10 % slower is fixed in the CR | §7 |
| 14. Docs: `CONTRIBUTING.md` only | §8 |

## 5. What changes

### 5.1 The store

No new read on `PlanStore` (`store/base.py`): the reads CR-419 built (`read_text`, `read_bytes`,
`exists`, `is_file`, `is_dir`, `listdir`, `glob`, `stat`, `walk`) serve every module below. The
guard, the refusal's text and exit code, and "no cache" stay as they are. The store's own shape
rules stay (it imports only `core/files.py`, `core/errors.py`, `writer/lines.py` and the standard
library; files at most 400 lines, functions at most 50; no import cycle). A Driver who finds a
read the protocol cannot give stops and says so in the CR's notes, rather than reading around the
store; the gate's lock files are the one known case (§5.3, store-reads-Q4).

### 5.2 The modules moved

In each module below, every direct read of the planning folder goes through the project's store
(`repo.store`, or a store the caller passes; the Driver picks the signature). The values computed,
the order of what is listed, the exceptions caught and the bytes printed stay; a message that
prints a file's full path keeps it byte for byte (the store's `root` joined to the `rel`, as the
caller built it). A caller outside the list changes only how it calls a moved function.

- `lifecycle/stages.py` (the stage scans), `lifecycle/layout_check.py` (`_dirs`, `stage_crs`,
  `_nested`'s `os.walk` through `store.walk`, `_top_level`, `_backlog_and_batch`,
  `_outside_names`, `_entry`, `_has_request`, `_cr_shape`), `lifecycle/backlog.py`,
  `lifecycle/running_batch.py` (the running-batch mark, `work/specifying`, the specification's
  look, the listing of marked CRs), `lifecycle/links.py`, `lifecycle/moveout.py`; `filing.py` and
  `session.py` join the list with no change.
- `core/batch.py`: the source folder's look, the record's `exists` looks, `next_cr_number`'s
  listing of the stage folders (its `roots`, each under `repo.changes`, given to the store as
  `rel`s). The batch lock (`open(... ".lock", "a+")`) and the `events.jsonl` append are writes
  and stay (CR-419's answer 8).
- `core/leases.py`: the `.lease-hold.*.run` records (`glob`, their `stat` time) and the gate
  queue's tickets (`glob("[0-9]*")`).
- `gate_queue.py`: the queue's tickets and marks (`glob`), a ticket's text (`read_ticket`, its
  retry on `PermissionError` and `FileNotFoundError` kept: the store raises what the direct read
  raises).
- `gate_slots.py`: the listing of `.long-gate*.lock` and a lock's `stat` time through the store;
  the holder's text, read from byte 1 of a held lock, stays direct (§5.3).
- `rails.py`, `history.py`: their reads of the planning folder.
- `summaries/sources.py`, `gaps.py`, `origin.py`, `title.py`: the covered files' looks and the
  `intake/*.md` listing through the store; `gaps.py`, `origin.py` and `title.py` stop importing
  `core/files.read_text` (the structure test flags that import) and read through the store,
  `errors="replace"` kept.
- `commands/crs.py`: the inbox CR's request look and its heading read through the store.

### 5.3 The gate's lock files (provisional, store-reads-Q4)

`gate_slots.lock_text` opens a held `.long-gate*.lock` and reads from byte 1 ("byte 0 is the lock:
Windows refuses to read it"). The store has no read at an offset. On the recommendation, this one
read stays direct: the lock files are the OS's locks, not the plan's content, and no index would
hold them. It is an entry of the structure test's exemption table (`("gate_slots.py",
"lock_text")`, "a held OS lock file, read past its locked byte") and of the run-time proof's
(§6.2). The listing and the `stat` of the same files go through the store.

### 5.4 What stays a direct read

Reads of other places in the moved modules stay, each an entry of `tests/test_store_reads.py`'s
`EXEMPT` table with its reason (CR-419's answer 7), among them: a worktree's look
(`commands/crs.py`, `Path(c.worktree).is_dir()`; `rails.py`, `wt.is_dir()`), and §5.3's lock
text. The Driver adds one entry per such call it finds, and no entry for a read of the planning
folder.

Not touched: `playbook/`, `plugin_files.py`, `costs/`, `autosync/records.py`, `writer/`,
`core/git.py`, `core/files.py`'s helpers (other modules outside the list still call them), and
the 20 modules of `commands/` named in §3.

### 5.5 The configuration (provisional, store-reads-Q3)

The configuration's files stay read by `playbook/layers.py` and `playbook/edit.py`, directly: the
project's root `chantier.yaml`, the surface's root one, the project's folder's one
(`projects/<name>/chantier.yaml`) and the shipped `config/chantier.defaults.yml`. All four are
outside the planning folder, the store's root (CR-402's answer 2); the store keeps owning only the
write of the project's file (`config_path`, `write_config`, with the writer's publish check). No
code changes for it; `CONTRIBUTING.md`'s sentence (§8) says the configuration is read by
`playbook/`, not the store.

### 5.6 Messages, cards, CI

No message is added or changed; no command's output moves. No card changes. No CI job is added or
changed. No host and default matrix: nothing here depends on the host or on a configured value
(the run-time proof runs on every system the suite runs on).

## 6. The run-time proof (provisional, store-reads-Q5)

### 6.1 Where

A new test module, `tests/test_store_runtime.py`, in `just test`, calling the CLI in-process as
the suite does. It prepares a planning surface in a temporary folder (the suite's `surface`
fixture in `tests/conftest.py`; a project with CRs in the inbox, the backlog, `3-ready`, a running batch in
`4-batch/` with an order in each of `1-pending`, `2-actives`, `3-done`, a batch record in
`5-archives/batches/`, a `forge-journal.jsonl`, a lease hold record and a gate lock file), and
observes three runs, each its own parametrized case:

- the board: one `board/state.project_state` of that project;
- `status`: one `chantier status` in-process (`commands/batch_status.status`);
- the hub: one `hub/cycle.Hub.cycle` over that surface, with `connectors.read` replaced as
  `tests/test_forge_hub.py` does (no network, no `gh` or `glab`).

### 6.2 What it checks

An audit hook (`sys.addaudithook`) on the events `open`, `os.listdir` and `os.scandir`. While a
case runs, each event whose path resolves inside the planning folder (`repo.changes`) is recorded
unless:

- a frame of `store/` is on the call stack (a store method made it); or
- it is a write: the builtin `open`'s mode holds `w`, `a`, `x` or `+`, or `os.open`'s flags are
  not read-only (CR-402 left the writes; this proof is about reads); or
- it is in the proof's exemption table, which names each entry with its reason and starts with
  one: the gate's held lock files (§5.3). An entry that no event matches fails the case, so the
  table stays true.

The case fails on any recorded event, naming the path (relative to the planning folder), the
event and the innermost frame outside the standard library (module, function, line).

Rules:

- Python cannot remove an audit hook: the hook is installed once per test process and does
  nothing outside a case's window (a flag it reads), so it costs the rest of the suite nothing.
- `Path.exists`, `is_file`, `is_dir` and `stat` raise no audit event (`os.stat` has none): the
  run-time proof cannot see them; the static test (§7) covers them. The test's docstring says so.
  `Path.iterdir`, `glob` and `os.walk` call `os.listdir` or `os.scandir` and are seen.
- A prepared check proves the hook catches a direct read: inside a case's window, a direct
  `Path.read_text` of a file of the planning folder is recorded and a `store.read_text` of the
  same file is not.
- The proof observes the three runs only. The board's push loop, its file watch (CR-429's
  `board/watch_files.py`) and the watcher (`chantier watch`) are not observed (§10).

## 7. Evidence

- `tests/test_store_reads.py`: `PACKAGES` gains `lifecycle`; `MODULES` gains `core/batch.py`,
  `core/leases.py`, `gate_queue.py`, `gate_slots.py`, `rails.py`, `history.py`,
  `summaries/sources.py`, `summaries/gaps.py`, `summaries/origin.py`, `summaries/title.py`,
  `commands/crs.py`. Its `EXEMPT` table gains §5.3 and §5.4's entries, one per module and function
  with its reason. It still reads the shipped source at the head under test (`src/chantier/`,
  never a copy); its prepared-source cases stay, paired with that check.
- `tests/test_store_runtime.py` (new), §6: the three cases and the prepared check.
- `tests/test_store_conformance.py`: unchanged, unless §5.1's stop adds a read (then its case on
  both backends, as CR-419's §6 asks of a read).
- The existing suite passes with no expected output changed (CR-419's answer 12), among them
  `test_board*.py`, `test_validate.py`, `test_gate_*.py`, `test_leases.py`,
  `test_summary_lint.py`, `test_titles.py`, `test_forge_hub*.py`,
  `test_store_reads.py`, `test_store_command_table.py`, `test_surface_writes.py`. A test that calls
  a moved function with a path is updated to the new call only; `tests/store_spy.py`'s `Spy`
  passes the reads through as it does today.
- Speed (CR-419's answer 13), stated in the PR with both figures, same machine, before and after:
  one `board/state.project_state` and one `chantier status` on a prepared planning folder of at
  least 200 CR folders in the backlog (built in a temporary folder, outside the suite). More than
  10 % slower is fixed in this CR (a `store.reading()` pass around a scan, a `rel` built without
  resolving), not accepted.
- `just test` within its budget (at most 30 s above 18.5 s); the PR states the time the new module
  adds.
- The project's gates (AGENTS.md): `just check` on Linux, macOS and Windows; `just eval-dry-run`
  (a change under the CLI's `src/`); `just scenario`, green on the pipeline's
  `just scenario (ubuntu-latest)` job before the PR, and locally on Windows (`chantier gate`) when
  this CR is the top of its batch's stack. No scenario step is added: the behaviour does not
  change.

## 8. Docs

- `CONTRIBUTING.md`: the sentence CR-419 added after the layers paragraph (the modules listed in
  `tests/test_store_reads.py` read the planning folder only through the plan's store) gains the
  run-time proof (`tests/test_store_runtime.py`: the board, `status` and the hub open or list no
  file of the planning folder outside the store) and the configuration's place (read by
  `playbook/`, not the store).
- `README.md`, `docs/`, the SVGs and their `-texts.md`, the cards, `AGENTS.md`: none change. The
  Driver searches them for a sentence this CR makes false and says in the PR that none was found,
  or changes the one it finds.

## 9. Rollout and batch-30

Nothing to set up or migrate: the files on disk are the same and are read the same.

Destination batch-30 (running, stack mode). Its CRs that edit this CR's files, checked in their
specifications on 2026-11-21:

| CR | State | Shared files |
| --- | --- | --- |
| 433 `board-batch-chip-stale` | active | `lifecycle/stages.py` |
| 434 `board-batch-kanban` | active | `lifecycle/stages.py` |
| 428 `drop-to-next-batch` | active | `lifecycle/moveout.py`, `history.py` |
| 429 `board-fingerprint-cache` | active | new `board/watch_files.py`, a board module under the structure test that watches the planning folder through `watchfiles`: it needs a store read or an `EXEMPT` entry by its own CR; this CR's run-time proof does not run it |
| 443 `gate-hold-narrowing` | pending | `core/leases.py` |
| 442 `stack-git-chain` | pending | `rails.py` |
| 445 `board-history` | pending | `history.py` (and new board modules, `board/history_page.py`, `board/reads.py`, under the existing test) |
| 449 `board-griller` | pending | `lifecycle/backlog.py` (and the new `board/griller.py`, under the existing test) |
| 425, 427, 430, 431 | done | `lifecycle/backlog.py`, `lifecycle/stages.py`, `rails.py`: in the base this CR starts from |

444 `board-user-inbox` and 448 `dashboard-pages` add board modules (`board/needs.py`,
`board/dashboard_page.py`) and edit `status/views.py`; they share no file with this CR, and the
existing structure test already holds them. None of the CRs above edits `tests/test_store_reads.py`
or `store/`.

No dependency is declared for a shared file: in the stack, this CR rebases on those below it, or
they on it, and its Driver re-runs the finder of §2 over the moved modules after each rebase (a new
direct read from a CR below fails the structure test and is moved, not exempted).

## 10. Out of scope

- An index or a cache behind the store (SQLite, Dolt), and any typed query on the store.
- The 20 modules of `commands/` named in §2 (60 calls), not reached by the board, `status` or the
  hub (store-reads-Q2).
- The configuration's reads (store-reads-Q3, on its recommendation).
- Observing the board's push loop, its file watch, the watcher or any command other than
  `status` at run time.
- The writes: CR-402's; none moves here.
- `playbook/`, `plugin_files.py`, `costs/`, `autosync/records.py`, `writer/`, the git folder's
  files, the web client.

## 11. Open questions for the user

Each is written into the text above on its recommendation (option a).

- **store-reads-Q1. Which part this CR takes.**
  (a) Recommended: everything the board, `status` and the hub reach (`lifecycle/`, `core/batch.py`,
  `core/leases.py`, the gate's two files, `rails.py`, `history.py`, four `summaries/` modules,
  `commands/crs.py`: 107 calls) and the run-time proof, which needs exactly that; about CR-419's
  size, so 3 rounds. (b) `commands/` first (60 calls), the proof later: the proof stays out of
  reach. (c) All of it (167 calls and the proof): breaks the 3-round rule.
- **store-reads-Q2. What becomes of the 20 `commands/` modules left.**
  (a) Recommended: the Chief of Staff files one inbox item for them when this specification is
  accepted (this CR files nothing). (b) Nothing: the structure test's list says which modules are
  store-only, and the rest stay direct until an index needs them.
- **store-reads-Q3. The configuration.**
  (a) Recommended: it stays read by `playbook/`, directly; the store keeps only the project's
  file's write. Its four files are outside the planning folder and small; an index gains nothing.
  (b) The store also reads the project's folder's file (a `read_config()` beside `write_config`),
  the three others staying with `playbook/`. (c) The store reads all four, its root widened: goes
  against CR-402's answer 2.
- **store-reads-Q4. The gate's held lock files.**
  (a) Recommended: the holder's text, read from byte 1 of a held lock, stays a direct read,
  exempt by name in both tests; the listing and the time go through the store. (b) The store gains
  an offset read (`read_bytes(rel, offset=1)`), with its conformance case on both backends.
- **store-reads-Q5. Where the run-time proof runs.**
  (a) Recommended: a pytest module in `just test`, in-process, on a prepared surface, within the
  suite's time budget. (b) A step of `just scenario`, on a real batch's surface: slower, and only
  in the long gate. (c) Both.
