# Answers

## 2026-11-20, the batch after batch-29

The user: "on va mettre en P1 les taches du batch d apres", and chose one-read-interface, live-activity-tui and copilot-close-end-event for it. Moved to P1.

- one-read-interface now waits on plan-store-interface (CR-402, the `store` package) and planning-server (CR-404), which edit the same files; its former dependency, CR-386, is archived.

## 2026-11-20, the grill, by the Chief of Staff alone

The user, 2026-11-20: "tu es maintenant autonome. plus de question. tu grilles tout seul". Each
answer below carries the line "Settled by the Chief of Staff (2026-11-20, the user asks no
questions)" and its reason. The rule for each: the narrowest choice that meets the request, no
behaviour or output change, no index.

Measured at main (`4ed0d56c`), with CR-402 (`store/`) and CR-404 merged: `PlanStore` is the write
interface, with three low-level reads (`read_text`, `exists`, `listdir`) that no reader calls
(they serve the conformance test). Every reader still reads the files directly: 336 calls of a
`Path` or `os` read in the CLI's 239 modules (the web client apart), 269 of them in the 165
modules that `board/`, `hub/` and `status/` import, directly or not. Direct calls in the modules
the intent names: `board/` 44, `hub/` 16, `status/` 21, `core/repo.py` 17, `core/surface_batches.py`
1, `commands/cost/` 0 (it reads through `core/batch.read_batch` and `core/records.read_events`);
`autosync/reading` no longer exists. So the read half is whole to build; CR-402 did none of it.

1. **What is left.** The whole read half: the reads of the protocol and every reader's move.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): the measure above; CR-402's
   specification names this CR for it ("That item then adds the read half to the same protocol and
   the same backends, moves the readers onto it, and extends the same conformance test").
2. **The interface's shape.** File-level reads on the same `PlanStore` protocol and the same two
   backends: text, bytes, existence, a folder's names, a file's size and time, a walk. No second
   module, no typed query (`records()`, `backlog()`). The parsers stay where they are and take
   their bytes from the store.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): one package, one
   protocol and one conformance test are CR-402's recorded terms; a typed query would move the
   parsers under `store/`, which may import no pydantic at start-up, and would risk an output change.
3. **No cache, no index.** Each call reads the files; nothing is kept between two calls.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): the intent ("Not built:
   the index") and the files stay the truth.
4. **Which readers move in this CR.** The direct reads of the planning folder in `board/`, `hub/`,
   `status/`, `commands/cost/`, `core/surface_batches.py` and `core/repo.py`, and the record
   readers they call: `core/records.py` (`read_batch_json`, `read_events`, `read_restored_number`),
   `core/seat.py`, `core/waits.py` (`read_file`), `core/batch_records.py` (`read_record`,
   `last_closed`, `read_retro`), `summaries/store.py` (`read`), `summaries/view.py`,
   `core/files.title_source`, `hub/journal.read` and `board/journal`. The other modules that read
   the planning folder (`lifecycle/`, `core/batch.py`, `core/leases.py`, the gate's files, the rest
   of `summaries/`, `commands/`) are split out to the inbox item `store-reads-rest`.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): the modules the intent
   names, and no more than one batch CR of 3 rounds holds; CR-402 took 3 rounds for the writes.
5. **`autosync/reading`.** Named by the intent, it no longer exists; `autosync/records.py` reads
   the old autosync tool's state folder in the git folder, not the planning folder. Not touched.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): the store's root is
   the planning folder.
6. **The configuration.** Not read through the store in this CR: its files are outside the
   planning folder (the project's root, the surface's root, the project's folder, the shipped
   defaults), read by `playbook/`. Carried to `store-reads-rest` as a point to judge.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): the store's root stays
   the planning folder (CR-402's answer 2); four small files gain nothing from a later index.
7. **Reads of other places** in the moved modules (the git folder, the web client's files, an
   HTTP address, `checkout.yml`, `project.md`, the clone) stay direct; the structure test names
   each with its reason.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): they are not the
   planning folder.
8. **Local files** (`batch.json`, `events.jsonl`, `seat.json`, the journals, the STATUS files) are
   read through the store like the published ones. Their writes and appends stay as CR-402 left them.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): the intent names the
   records and the journal; a read needs no publisher, so nothing can be refused.
9. **The path guard.** A read refuses a path that leaves the planning folder, as a write does,
   with the same text and exit code; the board's own answers (a 404 for a path outside, a lock
   never served) stay.
   Settled by the Chief of Staff (2026-11-20, the user asks no questions): CR-402's conformance
   test already asks it of `read_text`, `exists` and `listdir`.
10. **Another project's batch** (`core/surface_batches.py`) is read through a store over that
    project's planning folder.
    Settled by the Chief of Staff (2026-11-20, the user asks no questions): one store per planning
    folder; no path of a store leaves its root.
11. **The structure test** is static: over the list of moved modules, it reads the shipped source
    and fails on a direct read; each exemption is named with its reason; a prepared text proves it
    fails. The run-time proof (no file opened outside the store while the board, `status` and the
    hub run) goes with `store-reads-rest`, since it can pass only when every reader has moved.
    Settled by the Chief of Staff (2026-11-20, the user asks no questions): the intent ("A
    structure test follows those modules").
12. **No output change, proved by the existing tests** left unchanged, every message byte for byte
    (those that print a file's full path included). No scenario step, no card, no CI job.
    Settled by the Chief of Staff (2026-11-20, the user asks no questions): the intent.
13. **Speed.** The time of one board state and of `status` is measured before and after on the
    same machine and stated in the PR; more than 10 % slower is fixed in this CR, not accepted.
    Settled by the Chief of Staff (2026-11-20, the user asks no questions): the user wants the
    surface server faster later; the base must not slow it now.
14. **Docs.** `CONTRIBUTING.md` only (the rule and its test). No page, diagram or card names who
    reads the planning folder.
    Settled by the Chief of Staff (2026-11-20, the user asks no questions): no behaviour changes.
