# Change Specification: the surface server

This CR makes one elected process per planning surface (or repository) and machine, started by
`chantier board`. That process runs the board's pages, the forge hub loop and the board's and the
hub's journal writes, and holds `<git>/chantier/hub.lock`. One state file in the git folder,
`chantier/server.json`, replaces `board.json` and `hub.json`. It is a foundation and adds nothing
else. The one read interface (old answer 5) has left this CR for its own
(`one-read-interface-over-the-planning-fol`, answer 13).

No tracker issue: the CR is verbal (the user, 2026-11-18, during batch-28; drawing:
`intake/architecture.svg`).

## Goal, in the user's terms

Later, the user wants one server in front of the watchers. It would buffer, filter and route
their wakes, read the files faster through an index, and watch the PRs for the Chief of Staff
(later for a Driver or the Foreman). It would serve the pages, maybe an API, notify the user and
take delegated actions. The user: "Don't do all of that, but let us lay solid bases to allow it
later."

This CR is the second base. Today's board and forge hub become one elected process, the surface
server. What the user sees:

- one process instead of two;
- one state file instead of two;
- a `forge hub:` line that says which process is the hub;
- the board's start question also names the forge reads.

## Stacking

`depends.json` puts this CR after `addressed-events-one-typed-journal-that-` (CR-385, answer 7).
CR-385 stacks on CR-383 and CR-384, and through CR-384 on CR-375. Everything below is as those
four CRs leave it. In particular:

- **The journal.** One journal per project, still named `forge-journal.jsonl`, in the planning
  folder and never published. Its one writer function is `hub/journal.py`
  `append(repo, events, source)`, with `source` one of `hub`, `board`, `cli`; it writes under the
  project's lifecycle lock. The board's writers are `board/prs.py`, `board/config_api.py` and
  `board/write_api.py`, all with source `"board"`. The hub's writer is `hub/cycle.py`, with source
  `"hub"`.
- **The watcher.** It has CR-375's per-session lock, `chantier/watch-<project>/<session>.lock`,
  and needs no batch (CR-384). Its start line is
  `watch: <project> from cursor <n> for <values>`. After it come the clauses `, the hub`,
  `; hub is chantier <v>`, CR-384's `; board is chantier <v>: its writes do not reach this
  watcher, restart it`, and CR-385's `; configuration: ...`. It also has `--once`, the seat end,
  CR-385's filter and `events.wake_every`.
- **`status`.** It has CR-384's `board: chantier <v> serves this surface, ...` line, and the
  `forge hub:` line, which prints for a running batch only.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where below |
|---|---|---|
| 1 | **Scope.** A foundation: one process and its election. No index, JSON API, notification, delegated action, new wake or new forge read. | Out of scope |
| 2 | **Rules kept.** The files stay the truth, in git. The server never edits a batch, never messages an agent and writes only today's board and hub writes. An order is always the Chief of Staff's. | 2 |
| 3 | **The election.** The server holds `hub.lock`, one per surface and machine. A watcher that finds the lock held only reads its journal. With no server, the first watcher takes the lock and is the hub, as today. No session depends on the server. | 2, 3 |
| 4 | **One process.** `chantier board` starts the server: its pages, the hub loop and the event writes. `board.json` and `hub.json` become `server.json`, with its readers named. | 1, 2 |
| 5 | **Moved** (answer 13) to `one-read-interface-over-the-planning-fol`. | Out of scope |
| 6 | **AGENTS.md.** The board and forge hub exceptions become one, the surface server. The limits stay the same: the same read-only forge reads at the same rates, and the same writes. The PR names the change. | 5 |
| 7 | **Order.** After CR-385. | Stacking |
| 8 | **`planning-server` (P3) stays open.** This CR takes none of its write path, sync or leases. The server is the planning folder's one HTTP server, and keeps the board's seat-tied start and stop rule. The store stays Markdown and JSON. | 2, Out of scope |
| 9 | **Proof.** A real run on the user's machine. | Evidence |
| 10 | **Who writes the journal.** Inside the server, the hub's and the board's lines go through `append`. CLI commands keep calling `append` in their own process. There is no server-only writer (that would need an API and a fallback). | 2 |
| 11 | **One ask for both.** The board's start question in `session-start.md` names the forge reads. A yes starts the server with its hub loop. There is no option to run the board without the hub. | 2, 5 |
| 12 | **The upgrade never runs two boards.** `board.json`'s `running` record moves with the key, so a second board is still refused with the stop command. CR-384's readers of the board's version read the `server` entry. | 1 |
| 13 | **`store` leaves this CR.** This CR keeps the one process, the election and `server.json`. | Out of scope |
| 14 | **CR-375's watcher locks stay named.** They appear in the scenario's git-folder check and in the AGENTS.md and CONTRIBUTING.md texts. | 5, Evidence |
| 15 | **The start line as the stacked CRs leave it.** The readers table includes CR-384's two readers of the board's version. | 1, 3 |
| 16 | **A yielded watcher elects again.** It stops electing while `server.json` names a live server, and elects again once none is named. | 3 |
| 17 | **A failed `server.json` write.** At the server's start, it gives a `board not started:` refusal. A hub entry that was not written is retried at the next cycle. | 1, 2 |
| 18 | **No open question.** | none |

## What changes

`chantier/` is `skills/chantier/scripts/cli/src/chantier/`.

### 1. The state file: `<git>/chantier/server.json`

`<git common dir>/chantier/server.json` replaces `board.json` and `hub.json`. Like `board.json`
today, it has mode 0600 because it holds the key; it is never in a working tree and never pushed.

```json
{
  "key": "<the board's key>",
  "created": "<when the key was made>",
  "server": {"pid": 0, "host": "", "port": 0, "version": "", "served": "", "started": ""},
  "hub": {"pid": 0, "version": "", "started": "",
          "projects": {"<name>": {"read_at": null, "error": null, "error_at": null}}}
}
```

**The entries.**

- `key` and `created` are kept across starts, as in `board.json` today. `--new-key` replaces
  them and keeps the rest.
- `server` is today's `board.json` `running` record. The server writes it when it binds and
  removes it when it stops, if it still names the server's PID.
- `hub` is today's `hub.json`. Only the process that holds `hub.lock` writes it: the server, or a
  watcher when no server runs. That process removes it when it releases the lock, if it still
  names its PID.
- An entry whose process has not been alive since `started` (`procs.alive_since`, as today) counts
  as no entry.

**Writes.**

- Every write reads the file, changes only the writer's own entry, and replaces the file
  atomically (`core.files.write_json`).
- Writes are serialized by a short OS lock on `<git>/chantier/server.json.lock`, taken with
  `try_lock` and retried for up to one second. A server and a watcher may write their two entries
  at the same moment.
- Readers take no lock: the replace is atomic.

**A failed write** (answer 17): an `OSError`, or the write lock not taken within one second.

- When the server writes its `server` entry at start, or migrates the file, the failure is a
  refusal. The message is `board not started: <path>: <reason>` (`EXIT_EXTERNAL`, through
  `board/command.py`'s `_not_started`). This happens before the socket is bound or any line is
  printed.
- `board --new-key` refuses the same way.
- When the `hub` entry is not written at the end of a cycle, the cycle's events are already in
  the journal. The hub keeps its lock and runs on, and the next cycle writes the entry again. This
  applies to the server and to a watcher-hub alike.
- Removing an entry at stop is best effort. An entry left behind names a dead process, which
  counts as no entry.

**Migration, once** (answer 12). A server start, or a `--new-key`, may find no `key` in
`server.json` and a `board.json` present. It then moves two things into `server.json`, in one
write, before anything else:

- `key` and `created`, so the user's link stays good;
- `board.json`'s `running` record, as the `server` entry, if there is one.

After that it deletes `board.json`.

A board of an older chantier that is still running is therefore still found live through the
`server` entry. A second board is then refused as today, with the stop command (`_recorded`,
`_another_version`), and CR-384's version readers name it. Deleting `board.json` does not break
the older board: its `KeyFile.current` keeps the key it holds when the file is gone.

The first holder of `hub.lock` that writes `server.json` deletes `hub.json`. Nothing else reads
either old file.

**What reads `server.json`:**

| Reader | What it reads | Where |
|---|---|---|
| `chantier board` | `key`; the `server` entry, to attach to or refuse a running server (today's `running.live` path) | `board/command.py`, `board/running.py`, `board/key.py` |
| the server's key check | `key`, read again when the file changes (`KeyFile`) | `board/key.py`, `board/context.py` |
| `chantier watch`'s election | the `server` entry: not electing, and yielding, while a live server runs | `hub/watch.py`, `hub/lock.py` |
| the watcher's start line | the `hub` entry's version (`; hub is chantier <v>`); the `server` entry's version, for CR-384's `; board is chantier <v>: ...` | `hub/watch.py` |
| `chantier status`, `forge hub:` line | the `hub` entry; the `server` entry's PID, to say which process the hub is | `commands/batch_status.py` `_hub_line` |
| `chantier status`, CR-384's `board:` line | the `server` entry's version | `commands/batch_status.py` |
| the pane | nothing | none |

The pane (`hooks/register.tsx`) reads `STATUS.json` only. It shows neither the board nor the hub,
and this CR adds nothing to it.

`board/key.py`'s `key_path`, `board/running.py`'s record functions and `hub/lock.py`'s `RECORD`
and record functions all move into one module of the state file. It is `chantier/hub/state.py`,
or a name the Driver picks, but one module. Every reader above uses it.

The git folder's `chantier/` then holds:

- `server.json` and `server.json.lock`;
- `hub.lock`;
- CR-375's `watch-<project>/<session>.lock` files.

### 2. The surface server: `chantier board`

**What stays.**

- The options: `--host`, `--port`, `--seat`, `--new-key`, `--clock`.
- The start lines.
- The seats rule (`board/seats.py`): it stops when no registered seat is held any more, or on
  Ctrl-C.
- The attach-or-refuse rule (`board/command.py`). It prints `board already running at <URL>` for
  a live server of this version that serves the folder, and refuses a server of another version,
  or one that does not answer. It now reads the `server` entry.
- It joins the surface's autosync only as today, through the board's explicit action. It runs no
  other git command, records nothing in a batch and messages no agent.
- It serves an in-project repository as today: one project, the repository's git folder.

**What is new.** In the same process:

- **The election.** Once the socket is bound, a thread tries `hub.lock` (`HubLock.acquire`, never
  waiting), at once and then every `hub_times.poll_s()`, until it holds it.
  - While a watcher holds the lock, the server serves its pages and the watcher stays the hub
    until it yields (section 3).
  - The server becomes the hub within one poll after the yield.
  - Once it holds the lock, it writes the `hub` entry with its own PID.
- **The forge hub loop.** While it holds the lock, the same thread runs `hub/cycle.py`'s
  `Hub.cycle` whenever `Hub.due` says so: every `hub_times.cycle_s()`, which is 20 s, and
  `CHANTIER_HUB_TEST_TIMES` still shortens it for the scenario. It covers every project of the
  surface, exactly as a watcher-hub does today:
  - one read-only forge query per project whose running batch has a PR the record does not hold
    merged or cancelled;
  - the events appended through `append(..., "hub")`;
  - a failed read noted in the `hub` entry.
- **The event writes** (answer 10). The hub loop and the board's writers (`board/prs.py`,
  `board/config_api.py`, `board/write_api.py`, each with source `"board"`) all go through
  `hub/journal.py` `append`.
  - Their writes are serialized by the lifecycle lock that `append` takes. That lock also holds
    between threads of one process: each call opens its own handle.
  - CLI commands keep calling `append` in their own process.
  - The PRs page keeps its own forge reads at its own rate: at most every 10 s per project and
    batch shown, plus one when the page opens and one when the batch shown changes. Answer 6 keeps
    both rates.
- **The stop.** When the server stops (seats gone, Ctrl-C, or `uvicorn` exiting):
  - the hub thread stops;
  - the lock is released;
  - the `hub` and `server` entries that name its PID are removed.

  A server killed hard leaves entries whose process is gone. They count as no entry, and the OS
  has already released the lock.

### 3. The watcher: `chantier watch`

`hub/watch.py` keeps all of this as CR-375, CR-384 and CR-385 leave it:

- its cursor, its subscription and filter, its quiet window and wake rule;
- its seat end, `--once`, its end lines, its refusals;
- CR-375's per-session lock, taken in `elect()`.

Only the hub election changes (answer 16):

- **Electing.** `Watch.elect` tries `hub.lock` only while `server.json` names no live server.
  While a live server is named, it does not try.
- **Yielding.** A watcher that is the hub checks `server.json` at each poll. When it names a live
  server, the watcher:
  - finishes its current cycle;
  - removes its `hub` entry;
  - releases `hub.lock`;
  - goes on reading its journal, and ends as it would otherwise.

  It never writes the `server` entry.
- **Electing again.** Once `server.json` names no live server (the server stopped, or was killed
  and its entry names a dead process), the watcher tries the lock again at its next poll, as
  today. The first watcher that takes the lock is the hub.
- **The start line** is CR-385's and CR-384's, with no new clause:
  - `, the hub` when this watcher holds `hub.lock`. A watcher started while a server runs never
    shows it.
  - `; hub is chantier <v>` from the `hub` entry's version.
  - `; board is chantier <v>: ...` from the `server` entry's version.
- `--once` takes no lock and reads `server.json` for nothing, as CR-384 leaves it.

### 4. `status`

`commands/batch_status.py` `_hub_line` reads the `hub` entry of `server.json`. The line still
prints for a running batch only (CR-384).

- No live entry: `forge hub: none running`, as today.
- The `hub` PID is the live server's: `forge hub: PID <n>, the surface server, last read <t>`,
  followed by today's failure and version parts.
- Any other live holder: `forge hub: PID <n>, a watcher, last read <t>`, followed by the same
  parts.

The words `the surface server` and `a watcher` are the only change to this line. CR-384's `board:`
line reads the `server` entry and is otherwise unchanged. The `watch:` lines are unchanged.

### 5. AGENTS.md, CONTRIBUTING.md, cards, docs

**AGENTS.md** (answers 6 and 14). The PR's description names the change.

- In "The plugin must work with no setup", the clause on the board's `board.json` and the forge
  hub's `hub.lock` and `hub.json` (as CR-375 leaves it, with the watchers' locks) becomes:
  > the surface server keeps its key and, while it runs, its PID, address and version, and the
  > forge hub's holder its PID, version and last reads, in one file of the repository's git
  > folder (`chantier/server.json`, written under `chantier/server.json.lock`), next to the hub's
  > lock (`chantier/hub.lock`) and each watcher's lock (`chantier/watch-<project>/<session>.lock`,
  > one per project and session that ran a watcher, held while it runs, empty and never removed)
- In "The CLI's scope", "Three named exceptions" becomes two:
  - the batch's end cleanup, kept word for word;
  - **the surface server**, one paragraph that merges today's second exception
    (`chantier board`) and third (the forge hub, as CR-375, CR-384 and CR-385 leave it). The
    limits do not change:
    - it is started by `chantier board` on the user's yes;
    - one runs per surface and machine, and it holds `chantier/hub.lock`;
    - it serves the record and the planning folder's files behind a key, and edits the backlog
      and the roles' configuration as today;
    - its PRs page reads the forge and writes its lines as today;
    - its hub loop reads the forge at most every 20 s, with one query per project whose running
      batch has a PR the record does not hold merged or cancelled, and writes its lines as today;
    - every journal line goes through the one append function, CLI commands included, in their
      own process;
    - with no server running, the watcher that holds the lock is the hub, with the same limits;
    - each session's watcher keeps its lock and reads only its project's journal, with CR-385's
      end rule;
    - the server records nothing in a batch, runs no git but its autosync join, messages no agent
      and knows no role.
- In "The CLI has two named git exceptions", "the board's server" becomes "the surface server".

**CONTRIBUTING.md**: the same changes in its lines about 85-120, covering the git folder's files
(the watchers' locks kept) and the board and forge hub exceptions as one.

**Cards.**

- `skills/chantier/references/session-start.md`, "The board" (answer 11): the question asked
  before starting `$CHANTIER board --seat <id>` also names the forge reads. While it runs, the
  board reads the forge of the surface's running batches every 20 s with the user's own `gh` or
  `glab`, and needs the network. A no starts nothing.
- `session-start.md`, "The watcher": a watcher started while the board runs is not the hub, and
  its start line has no `, the hub`.
- `chief-of-staff.md` (the "the hub (or the board)" lines, about 1061-1065) and `foreman.md` (the
  `forge hub:` line, about 772) are checked and kept true.
- The agent files (`agents/`, `com.github.copilot/agents/`) are not touched.

**Docs and docstrings.**

- `docs/web-board.md`, lines about 172-177 (the key and the running record): name
  `chantier/server.json`, and say that the board is also the forge hub while it runs.
- The docstrings of `hub/__init__.py`, `hub/lock.py`, `board/__init__.py` and `board/running.py`
  (or of the modules that replace them) say "the surface server" and `server.json`.

## Out of scope

- The one read interface (`store`) and its structure test: they belong to
  `one-read-interface-over-the-planning-fol` (answer 13).
- An index or cache of the files, SQLite or Dolt.
- A JSON API, user notifications, delegated actions.
- Any new wake, watcher, audience, event kind or forge read.
- A server-only journal writer (answer 10).
- A board without the hub loop (answer 11).
- `planning-server`'s write path, sync, commits, pushes, rebases and leases (answer 8).
- Any change to the pane, `STATUS.json`, `hooks/`, `types/` or `board/web/`. So: no `just mod`,
  no screenshot, no `DESIGN.md`.
- An older chantier's watcher-hub during an upgrade, beyond what the lock gives. The lock still
  keeps one hub. That older hub writes `hub.json`, which this version no longer reads, so `status`
  may say `forge hub: none running` until that older watcher ends.

## Evidence

**Scope of the proof.**

- No CI job is added or changed.
- There is no host and default matrix: the CLI is the same on Claude Code and Copilot, and no
  configuration key is added.
- The OS lock and the atomic replace differ between Windows and POSIX. The scenario runs on Linux
  in the pipeline; the local `chantier gate` and the real run cover the user's Windows machine.

**Gates.** This is a change under the CLI's `src/` and the cards:

- before the first push: `just check` and `just eval-dry-run` in the worktree, at the rebased
  head;
- before the PR: the pipeline's `just scenario (ubuntu-latest)` green at its head;
- the local `just scenario` (`chantier gate`) when this CR is the top of its batch.

### Tests (`skills/chantier/scripts/cli/tests/`, few, parametrized, in-process)

Extend the existing tests:

- `test_board_running.py`,
  `test_a_new_board_reuses_refuses_or_starts_by_what_the_surface_already_runs`, parametrized over
  the migration:
  - The `server` entry is read from `server.json`.
  - A `board.json` holding a key and a live `running` record of another version is migrated.
    `board.json` is gone afterwards, and the new board is refused with the stop command.
  - A `board.json` holding only a key is migrated, and the key is kept.
- `test_new_key_keeps_the_running_record_and_the_exit_removes_only_its_own`:
  - `--new-key` keeps `server` and `hub`.
  - A stopping server removes only its own entries.
  - A refused write (the write lock held, prepared as such) at start gives
    `board not started: <path>: ...`, with nothing bound.
- `test_forge_hub.py`, `test_one_watcher_holds_the_hub_lock_and_the_next_takes_it`, parametrized
  over (no server; a live server named in `server.json`):
  - With no server, the first watcher is the hub.
  - With a live server, no watcher elects.
  - A watcher-hub yields when a live server appears: the lock is released and its `hub` entry
    removed.
  - Once the server entry names a dead process, the yielded watcher takes the lock at its next
    poll.
- `test_a_forge_error_lands_in_the_hub_record_not_in_the_journal`: the error lands in the `hub`
  entry. A `hub` entry write that fails is written at the next cycle, and the events are in the
  journal either way.
- `test_status_and_the_start_line_name_the_journal_the_hub_and_its_version`:
  - the `forge hub:` line in its three forms (none, the surface server, a watcher);
  - the start line's `hub is chantier <v>` and CR-384's `board is chantier <v>`, both read from
    `server.json`.
- One test of two writers of `server.json` (the `server` and `hub` entries, interleaved): neither
  entry is lost.
- One test of the server's hub thread, driven by a fake clock as `Watch.poll` is, with
  `forge_read.read` replaced (the existing seam):
  - it elects;
  - it cycles when due;
  - a board write and a hub event both land in the journal once, with their sources;
  - it releases the lock on stop.
- `just test` stays within its budget (AGENTS.md).

### Scenario (`scenario/run_scenario.py`; `scenario/README.md`, "the forge hub and `chantier watch`", unit surface-board)

The steps run on the two-project surface, with the fake `gh` and `CHANTIER_HUB_TEST_TIMES`:

1. `chantier board --port 0` runs in the background.
   - `server.json` names its PID in `server` and, within one cycle, in `hub`.
   - `status` prints `forge hub: PID <board pid>, the surface server, ...`.
   - No `board.json` or `hub.json` is left.
2. A second `board --port 0` prints `board already running at`, also with `--seat` from the other
   project.
3. A migration case: a `board.json` prepared with a key and a live older-version `running` record.
   - `board` is refused with the stop command.
   - The key is now in `server.json`.
4. A watcher of project A starts without `, the hub`. A's PR is merged on the fake forge.
   - The watcher ends with `forge saw merged: ... order merged <cr>`.
   - The line is written once, with `source: "hub"`, by the server.
5. A watcher started before the board was the hub (`, the hub`). Then the board is started.
   - The watcher yields, and `status` names the server's PID within one cycle.
   - One process reads the forge: one `api graphql` per project per cycle, never two.
6. The board's process is killed hard.
   - A running watcher takes the lock at its next poll.
   - `status` prints `forge hub: PID <watcher pid>, a watcher, ...`.
   - The next merge still wakes the watcher.
7. Unchanged and absent:
   - The record (`batch.json`, `events.jsonl`) is unchanged by the server.
   - No `gh` call is made but read-only `api graphql` queries.
   - The git folder's `chantier/` holds only `server.json`, `server.json.lock`, `hub.lock`,
     CR-375's `watch-<project>/<session>.lock` files and nothing else (answer 14).

The existing steps that name `board.json` or `hub.json` (lines about 1695, 1809, 1988, 2200 and
2208, as the stacked CRs leave them) now name `server.json` and its entries.
`test_scenario_coverage.py` passes.

### Real run on the user's machine (answer 9)

On Windows, on the planning surface, at the PR's head. The commands and their output go in the
PR's Deliverables:

1. The server up (`$CHANTIER board --seat <id>`), with `status`'s `forge hub:` line naming its PID
   as the surface server.
2. A second `chantier board`, from another session or project: attached
   (`board already running at`) or refused (another version), as printed.
3. A watcher woken by a real forge merge through the server: its end lines.
4. The server killed (`taskkill /PID <n> /T /F`) and a watcher taking the hub back, with `status`
   naming the watcher's PID.
