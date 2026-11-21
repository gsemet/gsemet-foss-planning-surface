# The server watches the planning files; boards and watchers subscribe

From the code audit of 2026-11-21 (finding 3, high, measured): while one board page is open, the
surface server walks each project's planning folder several times per 2-second push pass (one
`stat` per file of `1-inbox`, `2-backlog`, `3-ready`, `4-batch`: 194 ms for chantier alone, 0.65
to 1 s of work per pass under the GIL). The grill widened the fix: the server becomes the one live
reader of the planning files and of the forge, told of changes by the operating system, and every
live client (the web board, the session watchers, `chantier live`) subscribes to it.

Proposed title (02-answers, Q12): **The server watches the planning files; boards and watchers
subscribe** (replaces "Board: one fingerprint walk per project per pass"; short name `fp-cache`
kept).

Depends on `board-exposure` (`depends.json`: `after`): same server, and this spec relies on its
default bind `127.0.0.1` and its `board.host: network` (see "Consistency with board-exposure").

## Goal

In the user's words: the surface server reads the planning texts, the board reads only the API
("C'est maintenant le serveur d'état qui doit lire les textes, plus la board. La board ne lit que
l'api"); no blind scans of the files: where the system can notify a change it must be used, a
check every 5 s only where it cannot; the watchers subscribe to the server; only the server reads
the forge, and only while someone observes. An open page then costs one walk per project per real
change, not several per 2 s.

## Decisions carried (02-answers.md)

1. **fp-cache-Q1, Q2, Q5**: not answered; asked again as Q3, Q4 and Q8. Nothing carried from them.
2. **What to fix (Q3, Other).** The surface server reads the planning files; the web board reads
   only the published API. The server learns of changes from the file system's change
   notifications; where those are not available, it checks every 5 s.
3. **Proof (Q4, A).** An automatic test plus a before/after measure in the PR (see Evidence).
4. **Scope (Q6, Other).** The session watchers subscribe to the server instead of reading the
   journal themselves; only the server reads the forge (PRs, MRs, issues), and only while at least
   one client observes. (Issues: see open question 1.)
5. **The start line (Q7, A).** The server says, in one start line, how it watches:
   `board: watches the planning files`, or `board: no file notifications here; checks every 5 s`.
   The Chief of Staff passes it on.
6. **When the board updates (Q8, A).** After a change the server waits for 1 s with no new change,
   then publishes (about 1 s after a move, never a half-done state).
7. **Here, not apart (Q9, B).** All in this CR: the watchers' change and the forge rule included.
8. **No server running (Q10, Other).** The watcher starts the server when none runs, as a detached
   process: it outlives the watcher, and its output does not show in the watcher's.
9. **Who observes (Q11, A).** Any subscribed client: an open board page, a session's watcher,
   `chantier live`.
10. **Grilled enough (Q12, A).** Spec-writer, then the critic; destination the next batch, after
    board-exposure; the title adjusted (above).
11. **No blind file scans (entry 13, the user's own words).** Change notifications are required
    wherever the OS offers them: inotify on Linux, FSEvents (or kqueue) on macOS,
    ReadDirectoryChangesW on Windows. The 5 s check runs only where none of them works. The
    server never walks the planning folder on a timer while notifications work.

## What exists today (read, not rebuilt)

- The web client (`clients/web/js/`) already talks only to the published API (`core/ws-link.js`,
  `core/http-link.js`, the file route `GET /api/v1/projects/<id>/file`); it reads no planning file
  itself. Decision 2's "the board reads only the API" holds already: this CR keeps it (no change
  to `clients/web/`, so `DESIGN.md` is untouched) and moves the cost to the server side.
- `board/api/push.py:PushLoop.poll` runs every `PUSH_EVERY_S` (2 s, `board/api/times.py`) and,
  per watched topic, calls `board/api/topics.py:read`. `_project`, `_costs` and `_prs` call
  `board/reads.py:state_of`, and `_board` calls `reads.board_data`, which calls `state_of` for every
  project; each `state_of` calls `board/fingerprint.py:fingerprint` (the `stat` walk). The state
  itself is cached per fingerprint (`StateCache`), so the walk is the cost.
- The forge is read in two places of the server: the hub thread (`hub/loop.py:HubThread`, every
  `CYCLE_S` 20 s, whatever the clients) and the `prs` topic (`board/prs.py:ForgeReads`, at most
  every 10 s per project and batch, while subscribed).
- `chantier watch` (`hub/watch.py:Watch`) reads `forge-journal.jsonl` itself every `POLL_S`, and,
  with no live server, wins `hub.lock` and runs `Hub.cycle` (the watcher-hub).
- `chantier live` (`commands/live.py`, `clients/tui/link.py:Link`) is already an API client: the
  recorded server on its loopback address, the key from `server.json`, WebSocket then long-poll,
  reconnection every 5 s with `events` resubscribed from `after: <last seq>`.

## What changes

### 1. The server's file watch (new module `board/watch_files.py`)

- **Dependency.** Add `watchfiles` (Rust `notify`: inotify, FSEvents, ReadDirectoryChangesW; wheels
  for Linux, macOS and Windows; needs `anyio`, already locked through `starlette`) to the root
  `pyproject.toml` `dependencies`, pinned like the others, and to `uv.lock` (`uv lock`). Add
  `"watchfiles"` to `banned-module-level-imports`: it loads only once the board serves. It replaces
  hand-written polling (AGENTS.md: a dependency replaces hand-written code).
- **What is watched.** Per served project, its planning folder (`project.repo.changes`), recursive,
  lock files left out (`core.files.is_lock`), plus, on a planning surface, the surface's
  `projects/` folder (a project added or removed is seen; `Projects.refresh` then runs). Nothing
  outside the planning folders (never `.git`, never a worktree). The set of paths a change counts
  for is what `fingerprint.py` covers today (`SINGLE`, `HOLDS`, `DEEP`, `SHALLOW`); a change
  elsewhere in the folder is ignored.
- **One thread, `FileWatchThread`,** started in `board/command.py:_run` beside the hub, push and
  writer threads, stopped in its `finally`. It runs `watchfiles.watch(..., stop_event=...,
  force_polling=False, ignore_permission_denied=True)` (or `rust_notify` directly) and maps each
  changed path to its project.
- **The settle rule (decision 6).** Per project, a change opens a window; each new change of that
  project restarts it; once 1 s passes with no new change, the project is **settled**: the server
  computes its fingerprint once (`fingerprint()`, one walk), keeps it in `Context` (new field
  `revs: dict[str, str]`, under a lock), and wakes the push loop (below). A stream of changes that
  never goes quiet is settled at the latest 5 s after its first change (see open question 4), so a
  Driver writing `work/` files steadily cannot freeze the board.
- **The mode (decisions 5 and 11).** Notifications are the mode wherever `watchfiles` starts on the
  folder. When starting the notification watch raises (no backend, the OS watch limit reached,
  `OSError` of the backend), the thread switches to the check mode: one `fingerprint()` per project
  every 5 s (`CHECK_S = 5.0`, in `board/api/times.py` with the test seam), a changed fingerprint
  being the change; the settle rule then needs no extra second (the 5 s already spaces the
  checks). No timer walk in the notification mode. A notification watch that dies while the server
  runs (the backend raising) moves to the check mode with one stderr line
  `board: file notifications stopped (<reason>); checks every 5 s`.
- **The start line (decision 5)**, printed by `_announce` after the `board on ...` lines (and their
  `on this machine:` and `BEYOND`/`NO_NETWORK` lines from board-exposure), word for word, constants
  in `board/command.py`:
  - `WATCHES = "board: watches the planning files"`;
  - `CHECKS = "board: no file notifications here; checks every 5 s"`.
  The mode is decided before the line is printed (the watch is started, or has failed, first).
  `server.json`'s `server` entry gains `"files": "notify" | "check"` (written by
  `state.write_server` or updated once the mode is known), so `status` and a second
  `board --seat` can say it too: the "already running" path of `board()` appends the same line.
- **The start of the server.** The first fingerprint of each project is computed once at start
  (before serving), so the first page needs no walk.

### 2. The server's reads use the kept fingerprint

- `board/reads.py:state_of` stops calling `fingerprint()`: it takes `ctx.revs[project.id]` (the
  settled fingerprint) combined with `live.mark()` (the live cost's mark, which is in-process, not a
  file: the fingerprint's `extra` today), e.g. `sha256(rev + "\n" + mark)`. A project with no kept
  rev yet (just added) gets one computed then and kept. So `board`, `project`, `costs` and `prs`
  reads walk no folder; `board_data` for N projects walks none.
- `board/api/topics.py:_entries` and `_journal` keep their `stat` of one file (cheap); with the
  watch, they may read the kept rev instead, at the Driver's choice.
- `board/api/push.py`: `PushLoop` gains `wake()` (a `threading.Event`), called by the file watch
  when a project settles; `PushThread._run` waits on `wake` or `push_every_s()`, whichever first.
  The 2 s pass stays for what is not a file (the live cost's mark, the seats, the writer's state,
  the `prs` topic's forge read), and costs no walk. So a change shows about 1 s after it settles
  with notifications (today: up to 2 s); with the check mode, up to about 5 s (see open question
  4: the intent's "no later than today" does not hold in the check mode, which the user chose in
  Q3).
- `docs/server-api.md`, "The topics" (line ~119): "The server looks every 2 s, and only at what a
  client watches" becomes: the server is told of a change of the planning files by the system (or
  checks every 5 s where it cannot), publishes 1 s after the last change, and looks every 2 s at
  the values that are not files (the live cost, the seats, the writer, the PRs). The protocol does
  not change (no new op, no new topic, `rev` stays a token): protocol 1.

### 3. The forge is read only while a client subscribes (decisions 4, 9)

- New `PushLoop.observed() -> bool`: true while at least one subscription is held (WebSocket
  `sub`s, any topic, any project), or a long-poll client polled within the last `2 * HOLD_S`
  seconds (a long-poll client between two polls still observes). `sockets` not yet welcomed do not
  count.
- `hub/loop.py:HubLoop.poll` takes a predicate `observed: Callable[[], bool]` (from `_run`:
  `ctx.push.observed`); `Hub.cycle` runs only when `observed()` and `due(now)`. With no observer
  the hub keeps `hub.lock` and its `hub` entry but reads nothing; the entry's new field
  `idle: true` says so, and `hub/lines.py` prints `forge hub: PID <n>, the board, idle (no client
  subscribed)` instead of `last read ...`. The first observer after an idle spell gets a cycle at
  once (`last` reset when idle).
- `prs` topic: unchanged (it reads only while subscribed already).
- The cadence stays: the hub at most every 20 s, the `prs` read at most every 10 s per project and
  batch.

### 4. `chantier watch` subscribes to the server (decisions 4, 8)

- `hub/watch.py:Watch` stops reading `forge-journal.jsonl` and stops being a hub: remove `elect`'s
  `HubLock` part, `yield_hub`, the `Hub` import and the `, the hub` / `hub is chantier <v>` start
  clauses. It keeps: its own `WatcherLock` (so `status`, `open`, `take`, `order` and the switch to
  direct mode still see it), the audience filter (`subscription`, `journal.for_subscription`), the
  waking rule (`journal.waking`), the end rules (`quiet_s()` after the last waking event, no sooner
  than `events.wake_every`, or the seat moved: `seat_moved`), its output (`journal.event_text`) and
  its last line with the restart command.
- **The subscription.** The watcher finds the recorded server as `commands/live.py:recorded` does
  (`state.live_entry(git_dir, SERVER)`, the key of `server.json`, `address.loopback_base`: works for
  a `127.0.0.1` bind and an every-address bind alike) and subscribes, through
  `clients/tui/link.py:Link` (moved or shared, so `hub/` does not import `clients.tui.screen`), to
  the `events` topic of its project with `after: <cursor>`. Each event's `lines` go through the same
  filter and waking rule as the file's lines today; the cursor is the last `seq` received (lines
  for others move it, as today). `Link`'s reconnection carries `after`, so a lost link loses no
  line and repeats none.
- `poll(now)` stays the test seam: it takes the lines `Link` delivered since the last call (a
  queue fed by a reader thread, or `Link.items()` drained with a timeout), so tests drive it with
  no sleep, `Link` replaced by a fake.
- **No server running (decision 8).** At its start, and whenever the link is lost and
  `server.json` names no live server, the watcher starts one: `cli_command(repo) board --seat
  <session>` (the session the project's `seat.json` names), as a detached process:
  `subprocess.Popen(..., stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL, close_fds=True)`, with
  `start_new_session=True` on POSIX and `creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
  | CREATE_NO_WINDOW` on Windows; never waited on, it outlives the watcher. The watcher then waits
  up to 20 s for `server.json` to name a live server that answers the probe, and subscribes. Its
  start line says it: `watch: <project> from cursor <n> for <audiences>; started the board (PID
  <n>)`, or, when the server does not come up in time,
  `watch: the board did not start within 20 s: for the Chief of Staff, start it with <command>
  board --seat <id> and read its error`, and the watcher ends (exit 1). Two watchers racing to
  start one: the second `board` finds the first (its "already running" path) and exits; harmless.
  How the session's yes covers it, the bind and the seat: open questions 2, 3 and 5.
- **Another version's server.** It speaks protocol 1: the watcher subscribes anyway and keeps the
  `board is chantier <v>` clause of its start line (`autostart.board_clause`), now saying
  `board is chantier <v>: restart it to run this version`. A server that refuses protocol 1: the
  watcher ends with the server's sentence and the restart hint.
- **The pull path (`watch --once --after SEQ`) and `status`.** Unchanged in this spec: one-shot
  reads of the journal file, no process, no lock (see open question 6). The CLI's commands
  (`status`, `order`, `take`, `driver`, `facts`, `journal add`, `autostart.not_running_line`) keep
  reading the planning folder and the journal as today: decision 2 is about the live readers, not
  the one-shot commands (open question 7 asks the user to confirm).
- `hub/watch.py`'s docstring and `hub/__init__.py`'s are rewritten to the new model (the server is
  the only hub; watchers subscribe).

### 5. The hub lock

`hub.lock` stays, held only by the server's `HubLoop` (one forge reader per surface and machine).
No watcher takes it any more. `status`'s `forge hub:` line names `the board` or `none running`;
the `a watcher` wording (`hub/lines.py`) goes.

### 6. Cards (both hosts read the same cards; no agent file changes)

- `skills/chantier/references/session-start.md`:
  - **The board** (line ~70): the board no longer reads the forge on a timer: "it reads the forge
    every 20 s ... (only the PRs a running batch waits for)" becomes "while a client is subscribed
    (an open board page, a session's watcher, `chantier live`), it reads the forge every 20 s ...".
    Add the two start lines (`board: watches the planning files`, `board: no file notifications
    here; checks every 5 s`): pass the line on, in one line; the second means the board shows a
    change up to about 5 s late.
  - **The watcher** (lines ~105-122): the watcher subscribes to the board and starts it, detached,
    when none runs (the question to the user says so, per open question 2); "its hub reads the
    forge of every project of the surface" becomes "the board reads the forge while the watcher
    is subscribed"; remove "A watcher started while the board runs is not the hub (its start line
    has no `, the hub`): the board reads the forge" and the `hub is chantier <v>` sentence; add the
    `started the board (PID <n>)` clause (say once that the board was started, with its link from
    `status` or `board --seat`) and the `the board did not start within 20 s` line (one line to the
    user with the printed command; no workaround).
- `skills/chantier/references/chief-of-staff.md`, **The watcher** (lines ~1386-1437): "It prints
  the project's forge events ..." keeps; add that it reads them from the board, which it starts
  when none runs; the `board:` line paragraph names the new restart wording. Row line 35 (`watch:
  not running`): unchanged command, the yes now covering the board's start (open question 2).
- `skills/chantier/references/foreman.md` line ~845: "the `forge hub:` and `watch:` lines" stays
  true; no change unless the `forge hub:` wording is quoted (check at implementation).
- `skills/chantier/references/concepts.md` line ~15: "the forge hub reads only the PRs and MRs (a
  running ...)" gains "while a client is subscribed".
- `skills/chantier/references/hosts/claude-code.md` row "Run the watcher" (line 53) and
  `hosts/copilot.md` row "Run the watcher" (line 45): add that the watcher may start the board as
  a detached process, which the host does not see as a background task (it is not the watcher's
  output, decision 8). Row "The watcher when the session ends" (claude-code.md line 54): an
  orphaned board started by a watcher ends when the seat leaves (with `--seat`, open question 3).

### 7. AGENTS.md (every sentence this CR changes)

In the CLI-scope bullet ("The CLI's scope: ..."):

- "the surface server, `chantier board`: ... it serves the record and the planning folder's files"
  gains: "it alone reads the planning files for the live clients, told of changes by the system's
  file notifications (inotify, FSEvents, ReadDirectoryChangesW), or, where none works, by a check
  every 5 s, and publishes 1 s after the last change".
- "The same process is the forge hub while it runs (one per planning surface and machine, started
  by the Chief of Staff on the user's yes)" becomes "... started by the Chief of Staff on the
  user's yes, or by a session's watcher when none runs (detached)".
- "and, with none running, the one watcher of the surface that holds that lock is the hub and
  yields it when a server starts": removed.
- "The hub reads the forge ... at most once every 20 s" gains "while at least one client is
  subscribed to the server (a board page, a session's watcher, `chantier live`), and not
  otherwise".
- "each session's watcher, run for the Chief of Staff's whole session, with or without a batch,
  reads only its project's journal (the hub's lines, the board's, the writer's and an outside
  poller's `issue@1` lines), never the forge" becomes "... subscribes to the surface server's
  `events` topic for its project (the hub's lines, the board's, the writer's and an outside
  poller's `issue@1` lines), never reads the journal file or the forge, and starts the server,
  detached, when none runs".
- "the hub records nothing in a batch, runs no git and messages no agent": unchanged.
- "a batch's PRs: while a client asks for them ... at most once every 10 s": unchanged.

In the "chantier writes only in the planning folder ..." bullet: unchanged (no new file; the
`files` field joins the existing `server` entry of `server.json`). The new dependency is covered
by the `pyproject.toml` bullet (wheels for the three systems).

### 8. Docs (every sentence this CR changes)

- `docs/web-board.md` **Starting the board**, "The board is also the surface's forge hub while it
  runs ... it reads the forge, read-only, every 20 s" (line ~181): "while a page, a session's
  watcher or `chantier live` is subscribed, it reads the forge ...". Add one item: **How it sees
  changes**: the system's file notifications, else a check every 5 s, the start line naming which;
  a change shows about 1 s after the last write. Line ~62 "The forge hub of `chantier watch`
  writes the same lines" becomes "The forge hub (the board itself) writes the same lines".
  Line ~86 and ~167 ("a Chief of Staff whose watcher (or pull path) runs hears each write within
  about 20 s"): unchanged meaning, "reads" stays true.
- `docs/planning-folder.md` line ~126 `source`: `hub` "(the forge hub: the surface server)"; lines
  ~158-162 "`chantier watch` reads the lines for it" becomes "`chantier watch` receives, from the
  surface server's `events` topic, the lines for it" (the rest unchanged).
- `docs/forge-connectors.md` **The budget** (line ~49): "The forge hub reads at most once every 20
  s ..." gains "and only while a client is subscribed to the server". Line ~31 "The forge hub reads
  them" unchanged.
- `docs/server-api.md` "The topics": as in section 2.
- `CONTRIBUTING.md` lines ~89-91 and ~122-134 (the same hub and watcher sentences as AGENTS.md):
  the same changes as section 7.
- `hub/__init__.py` docstring (shipped code text): as section 4.
- `scenario/README.md`: the hub-and-watch block (lines ~330-365) rewritten as in Evidence.

## Out of scope

- The pull path and the one-shot commands' reads (unless open questions 6 or 7 say otherwise).
- Reading issues on the forge (unless open question 1 says otherwise): the outside poller and
  `journal add` stay as they are.
- The web client (`clients/web/`): no change; it already reads only the API.
- The protocol: no new op or topic; protocol stays 1.
- The board's bind and key (board-exposure's).
- Skipping `4-batch/**/work/` from the fingerprint (the audit's "then, if needed"): not needed once
  walks happen only per settled change.

## Consistency with board-exposure

- The watcher reaches the server on its loopback address (`loopback_base`), so it works with the
  default `127.0.0.1` and with `board.host: network` (`0.0.0.0`).
- The server a watcher starts is a plain `board --seat <id>`: it binds as `chantier.yaml` says
  (default `127.0.0.1`; `network` opens it to the local network), prints board-exposure's lines,
  which nobody reads (its output is discarded, decision 8). Open question 5.
- The new start line comes after board-exposure's `on this machine:`, `BEYOND` or `NO_NETWORK`
  line, in `_announce` and in the "already running" path, in that order.

## Host and default matrix

- Linux (inotify), macOS (FSEvents), Windows (ReadDirectoryChangesW), the planning folder on a
  local disk: notifications; `board: watches the planning files`; `server.json` `files: notify`.
- Any system where `watchfiles` cannot start its watch (watch limit, no backend): `board: no file
  notifications here; checks every 5 s`; `files: check`.
- A server started by hand, by the session (`board --seat`), or by a watcher (detached): the same
  lines and mode; the watcher-started one's lines are not shown to anyone.
- No client subscribed: no forge read (hub `idle`); one client subscribed: hub cycle every 20 s.
- A watcher with a server running (this version or another of protocol 1): subscribes; with none:
  starts one, then subscribes.

## Evidence

### Tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized)

- **The settle rule** (new `test_file_watch.py`): the watch thread's logic driven with a fake event
  source and the monotonic time passed in (as `HubLoop.poll`): changes at 0, 0.4, 0.8 s settle at
  1.8 s with one `fingerprint()` call (count it with a monkeypatched `fingerprint`); a change at
  0.0 then every 0.5 s settles at 5.0 s; changes in two projects settle each once; a lock file's
  change settles nothing.
- **No walk per pass** (the automatic proof, decision 3): with a two-project fixture, a
  `PushLoop` with subscriptions to `board`, `project`, `costs` (and `prs` with a fake forge), ten
  `poll(now)` passes with no file change call `fingerprint()` zero times (today: several per
  pass); one real file change plus its settle calls it once for that project; the event carries
  the new `rev`.
- **The real notification backend**: one test with a temp planning folder and the real
  `watchfiles` on the runner's system: write a file in `2-backlog/P2/`, the project settles within
  a few seconds (bounded wait), mode `notify`. Runs on the three CI systems (`just check`).
- **The check mode**: `watchfiles` start monkeypatched to raise `OSError`: the mode is `check`,
  the `CHECKS` line is printed, a change is seen by the next 5 s check (test times shortened via
  `CHANTIER_API_TEST_TIMES`-style seam extended with `CHECK_S`).
- **The start lines**: `_announce` with each mode prints the exact `WATCHES` / `CHECKS` text after
  the existing lines, read from the constants as shipped; the "already running" path prints the
  line from `server.json`'s `files`.
- **The forge only while observed**: `HubLoop.poll` with `observed` false for 60 s of passed time:
  `connectors.read` (the seam) never called, the `hub` entry `idle: true`; observed true: a cycle
  at once, then every 20 s. `PushLoop.observed` true with one WebSocket sub, with a long-poll
  within `2*HOLD_S`, false otherwise.
- **The watcher** (rework `test_watch_events.py`, `test_watcher_step.py`, `test_watcher_autostart.py`,
  `test_forge_hub.py`, `test_surface_server.py::test_one_watcher_holds_the_hub_lock_...` removed or
  rewritten): `Watch` with a fake `Link` feeding `events` lines: filters by audience, ends 20 s
  after the last waking line and no sooner than `wake_every`, ends on a moved seat, cursor moves
  past lines for others; a reconnection resubscribes with `after: <cursor>`; the watcher never
  takes `hub.lock`; with no live server, it calls the detached start (the `Popen` seam
  monkeypatched: the arguments hold `board --seat <id>`, `DEVNULL` for the three streams,
  `start_new_session` on POSIX or the detached flags on Windows) and prints `started the board`;
  with the server never answering, the `did not start within 20 s` line and exit 1.
- `just test` stays within its time budget (AGENTS.md).

### Scenario (`scenario/run_scenario.py`, the hub-and-watch steps; `scenario/README.md`)

- The board's start prints `board: watches the planning files` on `ubuntu-latest` (inotify), and
  the line is in `chantier gate`'s local Windows run too.
- A move through the board's API (`backlog.move`) with a `project` subscription open: the event
  with a new `rev` arrives within 3 s.
- The hub-and-watch block becomes: with no board, project A's watcher starts one (detached; its
  start line `started the board`; `server.json` names it); B's watcher subscribes to the same
  board; no watcher holds `hub.lock`; the `hub` entry names the board's PID; each cycle one
  `api graphql` per project with an open PR; A's PR merged on the fake forge: A's watcher ends with
  `forge saw merged ...` and its restart line, the merge written once (`source: hub`); B keeps
  running; two merges within the quiet give one end; `--after <n>` replays nothing; checks red at
  the watcher's end only; the board's PRs page first: one line; with every watcher ended and no
  page, the hub goes idle (`forge hub: ... idle`) and the fake `gh` is called no more.
- The watcher outlives nothing it should not: the board started by the watcher is still alive after
  the watcher's end (decision 8), and stops when its seat is released (per open question 3).

### Before/after measure (decision 3, in the PR's Deliverables)

On the user's real surface (four projects), the same script before and after: a board serving,
one page open (subscriptions `board`, `project chantier`, `costs`, `prs`), 60 s idle: the number
of `fingerprint()` calls and the total CPU time of the push thread (or `os.times()` of the
process). Before: about 0.65 to 1 s per 2 s pass (the audit). Expected after: no walk while
idle; one walk of one project per settled change. The PR quotes both tables and the head's SHA.

### Gates

`just check` and `just eval-dry-run` in the worktree (a change under the CLI's `src/`); the
pipeline's `just scenario (ubuntu-latest)` green at the PR's head (CLI and cards change); the
batch's top CR runs `chantier gate` locally on Windows (AGENTS.md). No `hooks/` or `types/`
change, so no `just mod`.

## Open questions (behaviour, scope, risk)

1. **Issues on the forge.** Q6's words name issues ("Seul le serveur ... les PR ou les issues").
   Today chantier reads no issue: an outside poller (the user's own program) writes `issue@1`
   lines through `journal add`. A: this CR keeps that; the server reads PRs and MRs only (this
   spec). B: the server also reads the issues the CRs' `issue:` lines name, and the outside poller
   becomes unneeded (a new forge read, wider scope; AGENTS.md's planning-server-Q24 sentence
   changes).
2. **The user's yes.** Today the session asks once for the board and once for the watcher. The
   watcher now starts the board (which runs the surface's writer, which commits and pushes, and
   reads the forge). A: one question covers both ("the watcher, which starts the board if none
   runs"); B: two questions stay, and after a no to the board the watcher does not run (the pull
   path instead); C: two questions, and the watcher starts the board even after a no to it.
3. **How long a board started by a watcher lives.** A: like the session's board, it follows the
   session's seat (`--seat`) and stops when the seat leaves (this spec); a session with no seat of
   its own starts no board and its watcher ends saying so. B: it serves until stopped by hand.
   C: it stops after some minutes with no client subscribed.
4. **Delays.** With notifications a change shows about 1 s after the last write (today up to
   2 s). In the 5 s check mode, up to about 5 s (later than today, which the intent excluded but
   Q3 chose). And a stream of changes that never pauses is shown at the latest 5 s after its first
   change. Accept both?
5. **Where a watcher-started board listens.** A: as `chantier.yaml` says (with
   `board.host: network`, open to the local network, though nobody sees its start lines); B:
   always this machine only (`--host 127.0.0.1`), the local network only through a board the
   session starts itself.
6. **The pull path.** With the watcher declined, `watch --once` reads the journal file at each
   user message; no client subscribes, so the server reads no forge and no merge line comes unless
   a page is open. A: accept (merges come from the user's word and `status`); B: `--once` also
   needs the server and counts as an observer for a short while (then the forge is read only at
   the user's messages).
7. **"The server alone reads the planning files."** This spec reads it as: among the live
   readers (the board, the watchers, `chantier live`). The CLI's one-shot commands (`status`,
   `order`, `take`, ...) keep reading the planning folder directly. Confirm, or say which of them
   must go through the server.
8. **Missed notifications.** On some disks (a network share, a WSL `/mnt/c` folder) the system may
   accept the watch yet send no notification, and the board would then never update. A: trust the
   notifications (no timer walk, entry 13); B: in the notification mode, one extra check every
   60 s as a safety net.
