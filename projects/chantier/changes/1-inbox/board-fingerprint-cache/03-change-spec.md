# The server watches the planning files; boards and watchers subscribe

Spec v4 (2026-11-21): v3 plus the spec critic's second run's no-user fixes 3 to 6 and the
user's answers fp-cache-Q17 (the no-client delay: 30 minutes, decision 18), Q18 (no idle stop for
a board started by hand or by a session, decision 19), Q19 (a board started by hand on a host
that cannot run the watcher keeps reading the forge every 20 s, decision 20) and Q20 (the watcher
ends by itself after 2 h with no event, decision 21). v3 carried the first critic run's fixes 3 to
13 and the answers Q15 (a watcher-started board stops by itself) and Q16 (a host that cannot run
the watcher).

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
default bind `127.0.0.1`, its `board.host: network`, and its `BEYOND` and `NO_NETWORK` lines (see
"Consistency with board-exposure").

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
   journal themselves; only the server reads the forge, and only while at least one client
   observes. Issues: PRs and MRs only (decision 13).
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
12. **The v1 spec's questions 3 to 8 (the Fable advisor, 2026-11-21, settled unless the user
    objects).**
    - (3) A board started by a watcher follows the session's seat (`--seat`): it stops when the
      seat leaves, as the session's own board does.
    - (4) Both delays are accepted: about 1 s after the last write with notifications, up to 5 s
      where no notification works; a stream of changes that never pauses shows 5 s after its first
      change.
    - (5) A board started by a watcher listens as `chantier.yaml` says (board-exposure's default
      `127.0.0.1`, or `board.host: network`), and the Chief of Staff passes on its
      `board: listens on the local network (...)` line (board-exposure Q7): the watcher, whose
      output the Chief of Staff reads, prints it (section 4).
    - (6) With the watcher declined, the forge is not read: the pull path is no observer (no
      half-observer).
    - (7) "The server alone reads the planning files" means the live readers (the board, the
      watchers, `chantier live`); the one-shot commands (`status`, `order`, `take`, ...) keep
      reading the planning folder.
    - (8) The notifications are trusted: no safety scan in the notification mode.
      `docs/web-board.md` names network shares and WSL `/mnt` folders as a known limit.
13. **Issues (fp-cache-Q13, A).** The server reads PRs and MRs only; issues stay with the outside
    poller (`journal add`, `issue@1`); watching issues can be its own CR later.
14. **Consent (fp-cache-Q14, A).** One question at the session's start covers the watcher and the
    board it starts ("I start the watcher, which starts the board if it is not running?"); yes
    starts both, no starts neither.
15. **The spec critic's no-user fixes 3 to 13 (02-answers, "Spec critic run (2026-11-21, v2)").**
    Each is carried in the section named: (3) the seat rule of the board's start, section 4;
    (4) the Windows flags, section 4 and the matrix; (5) the host rows written as unproved, with a
    trial, section 6; (6) the PID from `server.json`, section 4; (7) the `NO_NETWORK` line,
    section 4; (8) a silent server and a refused key, section 4; (9) the "no" path's merges,
    section 6; (10) the further edits (scenario README and steps, concepts, chief-of-staff's
    hand-over, session-start's error bullets), sections 6 and 8 and Evidence; (11) the 5 s check
    named the user's decision in AGENTS.md, section 7; (12) the dependency's basis, section 1;
    (13) the seat registered on a running board, section 4.
16. **A watcher-started board outlives the session (fp-cache-Q15, A).** It stops by itself after a
    delay with no subscriber (no watcher, no page, no `chantier live`), after its writer's last
    cycle; the cards name the stop command (`board/running.py:stop_command`) to stop it by hand.
    The delay is the user's: **30 minutes** (decision 18; section 1, "The idle stop").
17. **A host that cannot run the watcher (fp-cache-Q16, A).** The Chief of Staff asks the board
    question alone, as today, and starts `board --seat` by the host's means.
18. **The no-client delay (fp-cache-Q17, A).** 30 minutes (six writer cycles), the user's choice
    on the v3 spec's reasons (section 1, "Why 30 minutes").
19. **A board started by hand or by a session (fp-cache-Q18, A).** No idle stop: it stops only
    when its seat moves, as today. Only the board a watcher starts (`--stop-idle`) stops idle.
20. **The forge on a host with no watcher (fp-cache-Q19, A).** A board started by hand with
    `--seat` on a host that cannot run the watcher keeps reading the forge every 20 s, as today,
    with or without a client (section 1, "The forge always", and section 3), so the pull path
    still gets the forge's merges there.
21. **An orphaned watcher (fp-cache-Q20, A).** The watcher also ends by itself after a long spell
    with no event, so that a watcher left running by an ended session stops observing the board
    and the board's idle stop always fires. The exact value is this spec's choice: **2 hours**,
    no configuration key (section 4, "The idle end").
22. **The spec critic's second run's no-user fixes 3 to 6 (02-answers, "Spec critic run 2
    (2026-11-21, v3)").** (3) the `forge hub:` line keeps `the surface server`, only its
    `a watcher` branch goes: sections 3 and 5 and the Evidence; (4) decisions 18 and 19 in the
    header, decision 16's last sentence reworded: above; (5) a seat with no transcript, or a
    watcher keyed `none`, starts nothing and ends with its own line: section 4 and the Evidence;
    (6) session-start's `chief-of-staff` row: section 6.

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
  with no live server, wins `hub.lock` and runs `Hub.cycle` (the watcher-hub). It ends on a moved
  seat with `watch: the seat of <project> is another session's now; ended` (`Watch.lines`).
- `chantier live` (`commands/live.py`, `clients/tui/link.py:Link`) is already an API client: the
  recorded server on its loopback address, the key from `server.json`, WebSocket then long-poll,
  reconnection every 5 s with `events` resubscribed from `after: <last seq>`.
- `board/seats.py:Seats`: a board started with `--seat` follows the seats registered on it and
  stops (`ctx.stop`, the same path as Ctrl-C) when none is still held; `board/command.py:_run`'s
  `finally` runs the writer's final cycle (`writer.stop()`) before removing the `server` entry.
  A second `board --seat <id>` registers its seat on a running board
  (`board/address.py:register_seat`, the `seats.register` op).
- `hub/autostart.py:holds_seat(transcript)` tells whether the seat's transcript is this CLI run's
  own session key; `autostart.session_key()` is `none` (`autostart.NONE`) when the host gives no
  session id (a bare terminal), and `core/seat.py:read_seat` may return a seat whose `transcript`
  is empty.
- `hub/lines.py:hub_line` prints `forge hub: PID <n>, <who>, last read <t>`, `<who>` being
  `the surface server` or `a watcher`.
- `hub/watch.py:Watch.poll` ends on `EVENTS` (`quiet_s()` after the last waking event, no sooner
  than `events.wake_every`, 20 s by default in `config/chantier.defaults.yml`) or `SEAT`; with no
  waking event it runs for ever.

## What changes

### 1. The server's file watch (new module `board/watch_files.py`)

- **Dependency.** Add `watchfiles` (Rust `notify`: inotify, FSEvents, ReadDirectoryChangesW; wheels
  for Linux, macOS and Windows; needs `anyio`, already locked through `starlette`) to the root
  `pyproject.toml` `dependencies`, pinned like the others, and to `uv.lock` (`uv lock`). Add
  `"watchfiles"` to `banned-module-level-imports`: it loads only once the board serves. Its basis
  is the user's rule of entry 13 (decision 11): the OS's change notifications on the three systems,
  which no hand-written code of the CLI gives. `board/fingerprint.py:fingerprint()` stays: the
  settle rule and the check mode call it.
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
  `revs: dict[str, str]`, under a lock), and wakes the push loop (section 2). A stream of changes
  that never goes quiet is settled at the latest 5 s after its first change (decision 12 (4)), so
  a Driver writing `work/` files steadily cannot freeze the board.
- **The mode (decisions 5 and 11).** Notifications are the mode wherever `watchfiles` starts on the
  folder. When starting the notification watch raises (no backend, the OS watch limit reached,
  `OSError` of the backend), the thread switches to the check mode: one `fingerprint()` per project
  every 5 s (`CHECK_S = 5.0`, in `board/api/times.py`, under the test seam), a changed fingerprint
  being the change; the settle rule then needs no extra second (the 5 s already spaces the
  checks). The check mode is the user's own decision for a system with no notification (Q3,
  entry 13), not a fallback. No timer walk in the notification mode. A notification watch that
  dies while the server runs (the backend raising) moves to the check mode with one stderr line
  `board: file notifications stopped (<reason>); checks every 5 s`.
- **The start line (decision 5)**, printed by `_announce` after the `board on ...` lines (and their
  `on this machine:` and `BEYOND`/`NO_NETWORK` lines from board-exposure), word for word, constants
  in `board/command.py`:
  - `WATCHES = "board: watches the planning files"`;
  - `CHECKS = "board: no file notifications here; checks every 5 s"`.
  The mode is decided before the line is printed (the watch is started, or has failed, first).
  `server.json`'s `server` entry gains `"files": "notify" | "check"` (written by
  `state.write_server` or updated once the mode is known), so `status`, a watcher and a second
  `board --seat` can say it too: the "already running" path of `board()` appends the same line.
- **The start of the server.** The first fingerprint of each project is computed once at start
  (before serving), so the first page needs no walk.
- **The idle stop (decision 16).** New option `board --stop-idle` (a flag; the watcher passes it,
  section 4; a board started by hand or by a session's `board --seat` has none and stops as
  today). With it, the board stops once no client has observed it (`PushLoop.observed()` false,
  section 3) for `IDLE_STOP_S = 1800.0` seconds (30 minutes; `board/api/times.py`, under the test
  seam), counted from its start or from the last moment a client observed it. The stop is
  `ctx.stop()`, the path the seat rule and Ctrl-C take, so `_run`'s `finally` runs the writer's
  final cycle (commit, rebase, push of the published paths) before the `server` entry is removed;
  a final cycle that cannot push leaves the commits local, and the next writer pushes them (as
  today). The seat rule holds beside it: such a board stops at whichever comes first, its seat
  leaving or 30 minutes with no subscriber. Seats registered do not count as observers. The
  `server` entry gains `"stop_idle": 1800` (absent without the flag); the "already running" path of
  `board()` then appends one line, `board: stops by itself after 30 min with no client (a watcher
  started it)` (constant `STOPS_IDLE`), so a session that runs `board --seat` by hand on such a
  board knows it. On stop the board prints `board: no client for 30 min; stopped` (to its own
  output, discarded when a watcher started it; seen by whoever runs it by hand with the flag).
  **Why 30 minutes:** the gap with no subscriber in a live session is the time between a
  watcher's end and its restart by the Chief of Staff, which runs inside the Chief of Staff's turn
  (a long turn, a compaction, a host whose watcher's end waits for the user's next message), plus a
  page reload or a laptop's short sleep; a short delay (minutes) would stop the board in those
  gaps, and the session's next write to the surface would be refused until a watcher started it
  again. Thirty minutes covers those gaps with room to spare, is six times the writer's 5-minute
  cycle (so the writer's commits are long pushed, and the final cycle pushes the rest), and still
  stops a board left by an ended session within the half hour. An idle board reads no forge
  (section 3), so what it costs while it waits is a listening process, not network. The user
  chose this value on these reasons (decision 18). The stop always comes: a watcher left behind by
  an ended session, still subscribed, ends by itself 2 h after its start with no event (section 4,
  "The idle end", decision 21), so such a board stops at most about 2 h 30 min after the last
  event of its last watcher.
- **The forge always (decision 20).** New option `board --forge-always` (a flag). With it, the
  hub reads the forge every 20 s whether or not a client is subscribed, as today (section 3). The
  Chief of Staff passes it only on a host that cannot run the watcher (section 6); the watcher
  never passes it. The `server` entry gains `"forge": "always"` (absent without the flag). It does
  not combine with `--stop-idle` (`board` refuses both, a usage error: an idle stop would stop a
  board the pull path relies on). A second `board --seat <id> --forge-always` that finds a board
  running without it (another session's, started by its watcher) registers its seat as today and
  appends one line, `board: the running board reads the forge only while a client is subscribed
  (a watcher started it); the pull path gets no forge event until one is` (constant
  `FORGE_WHEN_OBSERVED`); the Chief of Staff tells the user once, in one line. Changing a running
  board's mode is out of scope (it would need a new op).
- **The test seam.** `CHANTIER_API_TEST_TIMES` takes two more optional fields,
  `<push_every>:<hold>:<tick>:<hello>[:<check>:<idle_stop>]`; four fields keep today's meaning.

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
  with notifications (today: up to 2 s); with the check mode, up to about 5 s (decision 12 (4)).
- `docs/server-api.md`, "The topics" (line ~119): "The server looks every 2 s, and only at what a
  client watches" becomes: the server is told of a change of the planning files by the system (or
  checks every 5 s where it cannot), publishes 1 s after the last change, and looks every 2 s at
  the values that are not files (the live cost, the seats, the writer, the PRs). The protocol does
  not change (no new op, no new topic, `rev` stays a token): protocol 1.

### 3. The forge is read only while a client subscribes (decisions 4, 9)

- New `PushLoop.observed() -> bool`: true while at least one subscription is held (WebSocket
  `sub`s, any topic, any project), or a long-poll client polled within the last `2 * HOLD_S`
  seconds (a long-poll client between two polls still observes). `sockets` not yet welcomed do not
  count. The idle stop (section 1) reads the same predicate.
- `hub/loop.py:HubLoop.poll` takes a predicate `observed: Callable[[], bool]` (from `_run`:
  `ctx.push.observed`, or `lambda: True` with `--forge-always`, decision 20); `Hub.cycle` runs
  only when `observed()` and `due(now)`. With no observer the hub keeps `hub.lock` and its `hub`
  entry but reads nothing; the entry's new field `idle: true` says so, and `hub/lines.py` prints
  `forge hub: PID <n>, the surface server, idle (no client subscribed)` instead of
  `last read ...` (fix 3 of the second critic run: `the surface server` stays, as today). The
  first observer after an idle spell gets a cycle at once (`last` reset when idle).
- **A host that cannot run the watcher (decision 20).** A board started with `--forge-always`
  reads the forge every 20 s with or without a client, as today: its `hub` entry is never `idle`,
  and its `forge hub:` line stays `forge hub: PID <n>, the surface server, last read <t>`.
- `prs` topic: unchanged (it reads only while subscribed already).
- The cadence stays: the hub at most every 20 s, the `prs` read at most every 10 s per project and
  batch.

### 4. `chantier watch` subscribes to the server (decisions 4, 8, 14, 15, 16)

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
- **The seat on a running board (fix 13).** When this session holds the project's seat
  (`autostart.holds_seat(seat.transcript)`), a watcher that subscribes to a running board first
  registers the seat on it (`address.register_seat(host, port, key, project, seat.session)`, the
  `seats.register` op), as a second `board --seat` does today, so a board started by another
  session also follows this one. With no seat, or a seat that is not this session's, it registers
  nothing.
- `poll(now)` stays the test seam: it takes the lines `Link` delivered since the last call (a
  queue fed by a reader thread, or `Link.items()` drained with a timeout), so tests drive it with
  no sleep, `Link` replaced by a fake.
- **No server running: the seat rule (decisions 8, 12 (3); fix 3).** At its start, and whenever the
  link is lost and `server.json` names no live server (`state.live_entry`), the watcher reads the
  project's `seat.json` (`core/seat.py:read_seat`):
  - **The seat is this session's** (`autostart.holds_seat(seat.transcript)`): it starts the board
    (next bullet).
  - **The seat is another session's:** it starts nothing and ends with the existing line
    `watch: the seat of <project> is another session's now; ended` (exit 0, as `Watch.lines` for
    `SEAT`).
  - **No seat:** it starts nothing and ends (exit 1) with
    `watch: no seat for <project>, so no board started; ended: for the Chief of Staff, take the
    seat (<cli> seat take <session id>), then start again: <watch command>`, where `<cli>` is
    `cli_command(repo)` and `<watch command>` is `autostart.watch_command(repo, cursor)`.
  - **A seat with no transcript** (`read_seat` returns a seat whose `transcript` is empty once kept
    to `[A-Za-z0-9-]`; fix 5 of the second critic run): it starts nothing and ends (exit 1) with
    `watch: the seat of <project> records no session transcript, so it cannot be told this
    session's; no board started; ended: for the Chief of Staff, take the seat again from this
    session (<cli> seat take <session id>), then start again: <watch command>`.
  - **A watcher keyed `none`** (`autostart.session_key()` is `autostart.NONE`: the host gave no
    session id; fix 5): it cannot hold a seat, so it starts nothing and ends (exit 1) with
    `watch: this run has no session key (the host gave no session id), so it cannot hold the seat
    of <project>; no board started; ended: for the Chief of Staff, start the watcher from the
    session's own background command, or the board by hand (<cli> board --seat <session id>)`.
  The order of the checks: keyed `none` (the seat is not read), no seat, a seat with no
  transcript, the seat this session's, another session's. With a live server recorded, the
  watcher subscribes whatever the seat and whatever its key (registering the seat only when it is
  this session's, above).
- **The detached start (decision 8; fix 4).** The command is `cli_command(repo) board --seat
  <seat.session> --stop-idle` (the board follows that seat, decision 12 (3), and stops after 30
  minutes with no subscriber, decision 16), started with `subprocess.Popen(..., stdin=DEVNULL,
  stdout=DEVNULL, stderr=DEVNULL, close_fds=True)`, never waited on, so it outlives the watcher:
  - POSIX: `start_new_session=True`;
  - Windows: `creationflags=CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW`, and **not**
    `DETACHED_PROCESS`: Windows ignores `CREATE_NO_WINDOW` when `DETACHED_PROCESS` is set, and the
    board's children (the writer's `git`, the hub's `gh`/`glab`) would then each open a console
    window. With `CREATE_NO_WINDOW` the board has a hidden console of its own, which its children
    inherit, and the watcher's console closing does not end it. Unproved until a `chantier gate`
    Windows run shows a watcher-started board's writer pushing with no console window appearing
    (the user at the screen; the PR's Known gaps names it until then).
  The watcher then waits up to 20 s for `server.json` to name a live server that answers the probe
  (`address.probe` with the key), and subscribes.
- **The start line (fix 6).** `watch: <project> from cursor <n> for <audiences>; started the board
  (PID <pid>)`, where `<pid>` is the `pid` of `server.json`'s `server` entry (the board's own
  Python process), not the `Popen`'s (which is `uv`'s launcher on a checkout or `uvx` install).
  The cards' stop command uses the same PID.
- **The board that does not come up (fix 8).** Three endings, each exit 1, each tested:
  - No live server in `server.json` within 20 s of the start: `watch: the board did not start
    within 20 s: for the Chief of Staff, start it with <cli> board --seat <id> and read its error`.
  - A live-recorded server (its PID alive) that gives no `welcome` for about 20 s (it holds the
    surface and does not answer): the watcher ends with `_silent`'s sentence, from the same
    function (`board/command.py:_silent`'s text moved to a shared helper so both say it word for
    word), prefixed `watch: `: `watch: a chantier board <v> (PID <n>) holds this surface at
    <host>:<port> and does not answer: stop it (<stop command>), then run board again`.
  - A server that refuses the key of `server.json` (HTTP 401, or the WebSocket's refusal of the
    key): `watch: the board at <host>:<port> refused the key of server.json: for the Chief of
    Staff, restart it: stop it (<stop command>), then start again: <watch command>`.
  Two watchers racing to start one: the second `board` finds the first (its "already running"
  path) and exits; harmless.
- **The board's lines the watcher passes on (decisions 5, 12 (5); fix 7).** The started board's own
  output is discarded, so the watcher, once that board answers, prints after its start line what
  the Chief of Staff must pass on, read from `server.json`'s `server` entry and the project's
  `chantier.yaml` (`playbook.layers.load_board`):
  - board-exposure's `BEYOND` line, word for word (`board.command.BEYOND` with the entry's
    `host`), when that host is not loopback (`address.is_loopback`);
  - board-exposure's `NO_NETWORK` line, word for word (`board.command.NO_NETWORK`), when
    `board.host` is `network` and the entry's host is loopback (the board found no local network
    address);
  - the file-watch line (`WATCHES` or `CHECKS`, from the entry's `files`).
  The link itself is not printed by the watcher: the Chief of Staff gives it from `status` or
  `board --seat` (its "already running" path). The same lines follow the start line when the
  watcher subscribes to a board already running.
- **The idle end (decision 21).** The watcher also ends once `IDLE_END_S = 7200.0` seconds
  (2 hours; `hub/times.py`) have passed since its start with no event for it that wakes (a waking
  event already ends it `quiet_s()` later, so this end comes only when none came), and no sooner
  than `events.wake_every` after its start (as the `EVENTS` end). New reason `IDLE`
  (`hub/watch.py`), exit 0, its last line (a constant in `hub/watch.py`):
  `watch: no event for <name> in 2 h; ended, so a session that has ended leaves no board running:
  for the Chief of Staff, start again in the background now: <watch command>`, `<name>` as in the
  `EVENTS` line (the open batch's id, or `<project> (no batch)`). The events received that do not
  wake are printed before it, as at the other ends. The test seam: `CHANTIER_HUB_TEST_TIMES`
  takes a third optional field, `<cycle>:<quiet>[:<idle_end>]`; two fields keep today's meaning.
  **Why 2 hours, and no configuration key:** the user gave "about 2 h"; the value only has to be
  long against a live session's quiet spells, since each end costs the Chief of Staff a turn to
  start the watcher again (at most 12 a day in a session where nothing happens), and short enough
  that a board an ended session left behind does not run for most of a day (it stops at most
  2 h 30 min after its last watcher's last event: this end plus the board's 30 minutes). A live
  session's watcher, ended by it, is started again within the Chief of Staff's turn, well inside
  the board's 30 minutes, so the board keeps running. No key: it is a stop for an ended session,
  not a tuning of how the session is woken (`events.wake_every` stays the watcher's one key); no
  user need to change it has been stated, and a key would be one more value on the board's
  Configuration page and in `config@1` lines; a later CR can add one from a measured need.
- **The session's yes (decision 14).** The watcher starts the board only under the session's yes
  to the one question (section 6); a no starts neither, and the pull path runs as today.
- **Another version's server.** It speaks protocol 1: the watcher subscribes anyway and keeps the
  `board is chantier <v>` clause of its start line (`autostart.board_clause`), now saying
  `board is chantier <v>: restart it to run this version`. A server that refuses protocol 1: the
  watcher ends with the server's sentence and the restart hint.
- **The pull path (`watch --once --after SEQ`) and `status`.** Unchanged in this spec: one-shot
  reads of the journal file, no process, no lock; the pull path is no observer, so with the
  watcher declined the forge is not read (decision 12 (6)). The CLI's commands (`status`, `order`,
  `take`, `driver`, `facts`, `journal add`, `autostart.not_running_line`) keep reading the
  planning folder and the journal as today (decision 12 (7)).
- **The writer's start hint.** `writer/lines.py:START` ("start the surface server ($CHANTIER board
  --seat <session id>)") becomes `start the watcher, which starts the surface server (the "watch:
  not running" line's command), or, on a host that cannot run the watcher, $CHANTIER board --seat
  <session id> --forge-always` (decisions 17 and 20); tests that match it read the constant.
- `hub/watch.py`'s docstring and `hub/__init__.py`'s are rewritten to the new model (the server is
  the only hub; watchers subscribe, and start the board when none runs and the seat is theirs).

### 5. The hub lock

`hub.lock` stays, held only by the server's `HubLoop` (one forge reader per surface and machine).
No watcher takes it any more. `status`'s `forge hub:` line names `the surface server` (as today)
or says `forge hub: none running`; only the `a watcher` branch of `hub/lines.py:hub_line` goes
(fix 3 of the second critic run), with its docstring's mention. Its two forms:
`forge hub: PID <n>, the surface server, last read <t>` (with a client subscribed, or with
`--forge-always`) and `forge hub: PID <n>, the surface server, idle (no client subscribed)`.

### 6. Cards (both hosts read the same cards; no agent file changes)

- `skills/chantier/references/session-start.md`:
  - **One question (decision 14).** The Chief of Staff asks once, at the session's start, on the
    `watch: not running` line of `seat take`, one question that covers the watcher and the board
    it starts, in the user's language, in substance "I start the watcher, which starts the board
    if it is not running?", explaining both as the two paragraphs do today (the board's persistent
    process, which stops by itself 30 minutes after its last client or when the seat leaves, its
    configured network exposure, its forge reads while a client is subscribed, its writer that
    commits and pushes the plan; the watcher's background run). Yes starts both (the watcher
    starts the board, detached, when none runs); no starts neither: the session's writes to the
    surface are refused (as with a declined board today), merges go back to the user's word
    (fix 9: nothing reads the forge, so no `forge saw merged` line comes), and the pull path runs
    at each user message. The role table's `chief-of-staff` row (line ~52; today "take the
    free/own seat, then ask before starting the board") says "take the free/own seat, then ask
    the one watcher-and-board question (the board question alone on a host that cannot run the
    watcher)" (fix 6 of the second critic run). A yes holds for the session, as
    today, and covers starting the watcher again after the board stopped by itself (a refused
    write to the surface naming no running writer, or a `watch: not running` line: start the
    watcher, which starts the board).
  - **A host that cannot run the watcher (decision 17).** On a host whose reference says the
    watcher cannot run (no background command whose end starts a turn), the Chief of Staff asks
    the board question alone, as today ("Ask before starting `$CHANTIER board --seat <own session
    id> --forge-always` in the background ..."), and starts it by the host's means (the host's
    reference, "Run the board"), with `--forge-always` and no `--stop-idle`: that board stops
    when the seat moves, as today (decision 19), and reads the forge every 20 s with or without a
    client, as today (decision 20), so the pull path, run at each user message, still prints its
    `forge saw merged` lines. Its "already running" line `FORGE_WHEN_OBSERVED` (a board another
    session's watcher started): tell the user once, in one line, that merges come only while a
    client is subscribed. A host with no background command at all: one line with the reason, as
    today.
  - **The board** (line ~70): "it reads the forge every 20 s ... (only the PRs a running batch
    waits for)" becomes "while a client is subscribed (an open board page, a session's watcher,
    `chantier live`), or always when started with `--forge-always` on a host that cannot run the
    watcher, it reads the forge every 20 s ...". Add the two start lines (`board:
    watches the planning files`, `board: no file notifications here; checks every 5 s`): pass the
    line on, in one line; the second means the board shows a change up to about 5 s late. Add the
    `board: stops by itself after 30 min with no client (a watcher started it)` line of the
    "already running" path: tell the user once, in one line.
  - **The board's error bullets (fix 10).** The `already serves this surface` / `does not answer`
    bullet and the `board not started` bullet also cover the watcher's `did not start within 20
    s`, `does not answer` and `refused the key` lines; when the user's word asks for a board
    started by hand (`board --seat <id>`, as the watcher's line prints it), the Chief of Staff
    runs it by the host's background means (the host's reference, "Run the board"), never in the
    foreground (a board that starts never returns), and reads its first lines.
  - **The watcher** (lines ~105-122): the watcher subscribes to the board and starts it, detached,
    when none runs and the seat is this session's (the one question says so, decision 14); "its
    hub reads the forge of every project of the surface" becomes "the board reads the forge while
    the watcher is subscribed"; remove "A watcher started while the board runs is not the hub (its
    start line has no `, the hub`): the board reads the forge" and the `hub is chantier <v>`
    sentence; add the `started the board (PID <n>)` clause (say once that the board was started,
    with its link from `status` or `board --seat`), the `BEYOND`, `NO_NETWORK` and file-watch
    lines that may follow it (pass each on, in one line, as the board's own), and the
    `did not start within 20 s`, `does not answer`, `refused the key` and `no seat for <project>`
    lines, and the `records no session transcript` and `has no session key` lines (one line to
    the user with the printed command or reason; no workaround; for `no seat` and `records no
    session transcript`, take the seat as printed only when the session is the Chief of Staff by
    the role rules above, then start the watcher again). The `no event for <name> in 2 h` end
    (decision 21): start the watcher again at once with the printed command, saying nothing to
    the user.
  - **Stopping the board by hand (decision 16).** The board a watcher starts is no background task
    of the session: the host's stop of a background task does not reach it. It stops by itself
    when the seat leaves or 30 minutes after its last client; to stop it sooner, on the user's
    word, run the stop command with the PID of the watcher's start line or of `status`'s `forge
    hub:` line: `taskkill /PID <pid> /T /F` on Windows, `kill <pid>` elsewhere (as
    `board/running.py:stop_command` prints it).
- `skills/chantier/references/chief-of-staff.md`:
  - **The watcher** (lines ~1386-1437): "It prints the project's forge events ..." keeps; add that
    it reads them from the board, which it starts when none runs and the seat is this session's;
    the end rule (line ~1391) gains "or 2 h after its start with no event for it that wakes (the
    `no event for <name> in 2 h` line: start it again at once, nothing to tell the user)"; the
    `board:` line paragraph names the new restart wording. Row line ~35 (`watch: not
    running`): unchanged command, the yes now covering the board's start (decision 14).
  - **The pull path** paragraph (line ~1429, fix 9): add "after the user's no, merges go back to
    the user's word: no board reads the forge".
  - **The hand-over** (line ~1922, fix 10): "Its board stops by itself when the seat moves; the new
    one starts its own at its `seat take`" becomes "Its board stops by itself when the seat moves
    (or 30 minutes after its last client); the new one's watcher, started from the line of its
    `seat take` on its yes, registers its seat on a board still running, or starts one".
- `skills/chantier/references/concepts.md` line ~15: "the forge hub reads only the PRs and MRs (a
  running ...)" gains "while a client is subscribed". Lines ~744-747 (the background tasks' stop
  rule, fix 10): "stops itself (at its end, or when the seat is another session's)" becomes
  "stops itself (at its end, 2 h after its start with no event, or when the seat is another
  session's)"; after "the watcher is started on the user's yes, started again after each end,
  and stops itself ...", add "the board a watcher starts is a detached process, no background task
  of the session: it stops itself when its seat leaves or 30 minutes after its last client, and
  by hand only with the stop command `session-start.md` names".
- `skills/chantier/references/foreman.md` line ~845: "the `forge hub:` and `watch:` lines" stays
  true; no change unless the `forge hub:` wording is quoted (check at implementation).
- `skills/chantier/references/hosts/claude-code.md` and `hosts/copilot.md` (fix 5):
  - Row "Run the watcher" (claude-code.md line ~53, copilot.md line ~45): add "The watcher may
    start the board as a detached process (`board --seat <id> --stop-idle`), which is not a
    background task of the session: unproved that it outlives the watcher and that the host does
    not see it as a background task; trial: with no board running, start the watcher, see its
    `started the board (PID <n>)` line; stop the watcher's background task, then ask `GET
    /api/board` with the key: it answers, and the host lists no board task; end the session, ask
    again: it answers (until the seat leaves or 30 minutes with no client); the trial, when run,
    records its date and result in this row."
  - Row "The board when the session ends" (claude-code.md line ~55, copilot.md line ~46): add "A
    board a watcher started is no background task: it stops when the seat moves or 30 minutes
    after its last client (the CLI), which does not depend on the host."
  - Row "The watcher when the session ends" (claude-code.md line ~54): add "if the host leaves it
    running, it ends by itself 2 h after its start with no event (the CLI), and the board it
    observed stops 30 minutes later".
  - Row "Run the board" (claude-code.md line ~48, copilot.md line ~42): the command becomes
    "`$CHANTIER board --seat <id>`, with `--forge-always` on a host that cannot run the watcher
    (`session-start.md`)".
  - copilot.md row "Run the watcher": where the host's watcher end does not start a turn and the
    Chief of Staff starts no watcher, it asks the board question alone (decision 17), as the
    session-start card says.

### 7. AGENTS.md (every sentence this CR changes)

In the CLI-scope bullet ("The CLI's scope: ..."):

- "the surface server, `chantier board`: ... it serves the record and the planning folder's files"
  gains: "it alone reads the planning files for the live clients, told of changes by the system's
  file notifications (inotify, FSEvents, ReadDirectoryChangesW), or, on a system where none works,
  by a check every 5 s (the user's own decision of 2026-11-21, not a fallback), and publishes 1 s
  after the last change" (fix 11).
- "The same process is the forge hub while it runs (one per planning surface and machine, started
  by the Chief of Staff on the user's yes)" becomes "... started by a session's watcher, detached,
  when none runs and the session holds the seat, on the user's one yes for the watcher and the
  board, or by the Chief of Staff on a host that cannot run the watcher; one a watcher started
  stops by itself when its seat leaves or 30 minutes after its last subscribed client, after its
  writer's last cycle".
- "and, with none running, the one watcher of the surface that holds that lock is the hub and
  yields it when a server starts": removed.
- "The hub reads the forge ... at most once every 20 s" gains "while at least one client is
  subscribed to the server (a board page, a session's watcher, `chantier live`), and not
  otherwise, but for a board started with `--forge-always` by the Chief of Staff on a host that
  cannot run the watcher, which reads it every 20 s with or without a client (the user's answer
  of 2026-11-21)".
- "each session's watcher, run for the Chief of Staff's whole session, with or without a batch,
  reads only its project's journal (the hub's lines, the board's, the writer's and an outside
  poller's `issue@1` lines), never the forge" becomes "... subscribes to the surface server's
  `events` topic for its project (the hub's lines, the board's, the writer's and an outside
  poller's `issue@1` lines), never reads the journal file or the forge, and starts the server,
  detached, when none runs and its session holds the seat"; and "ends 20 s after the last new
  event for it that wakes, and no sooner than `events.wake_every` after its start, which wakes its
  session, or when the project's seat is another session's" gains ", or 2 h after its start with
  no event for it that wakes (so a watcher an ended session left behind stops)".
- "the hub records nothing in a batch, runs no git and messages no agent": unchanged.
- "a batch's PRs: while a client asks for them ... at most once every 10 s": unchanged.

In the "chantier writes only in the planning folder ..." bullet: unchanged (no new file; the
`files` and `stop_idle` fields join the existing `server` entry of `server.json`). The new
dependency is covered by the `pyproject.toml` bullet (wheels for the three systems).

### 8. Docs (every sentence this CR changes)

- `docs/web-board.md` **Starting the board**, "The board is also the surface's forge hub while it
  runs ... it reads the forge, read-only, every 20 s" (line ~181): "while a page, a session's
  watcher or `chantier live` is subscribed, it reads the forge ...". Add one item: **How it sees
  changes**: the system's file notifications, else a check every 5 s, the start line naming which;
  a change shows about 1 s after the last write (up to 5 s in the check mode, or while writes never
  pause). Known limit (decision 12 (8)): on a network share or a WSL `/mnt` folder (`/mnt/c`), the
  system may accept the watch and send no notification; the board then does not update there
  (keep the planning folder on a local disk). Add, to **Starting the board**, that a session's
  watcher starts the board, detached, when none runs, on the session's one yes, and that such a
  board stops by itself when the seat leaves or 30 minutes after its last client (the stop
  command stops it sooner). Line ~62 "The forge hub of `chantier watch` writes the same lines"
  becomes "The forge hub (the board itself) writes the same lines". Lines ~86 and ~167: unchanged.
  The forge sentence above also says that a board started with `--forge-always` (a host that
  cannot run the watcher) reads every 20 s with or without a client, and the watcher's paragraph
  that a watcher ends by itself 2 h after its start with no event.
- `docs/planning-folder.md` line ~126 `source`: `hub` "(the forge hub: the surface server)"; lines
  ~158-162 "`chantier watch` reads the lines for it" becomes "`chantier watch` receives, from the
  surface server's `events` topic, the lines for it" (the rest unchanged).
- `docs/forge-connectors.md` **The budget** (line ~49): "The forge hub reads at most once every 20
  s ..." gains "and only while a client is subscribed to the server (always, for a board started
  with `--forge-always` on a host that cannot run the watcher)". Line ~31 unchanged.
- `docs/server-api.md` "The topics": as in section 2.
- `CONTRIBUTING.md` lines ~89-91 and ~122-134 (the same hub and watcher sentences as AGENTS.md):
  the same changes as section 7.
- `hub/__init__.py` docstring (shipped code text): as section 4.
- `scenario/README.md`: the hub-and-watch block (lines ~330-365) and the surface server block
  (lines ~390-422, fix 10) rewritten as in Evidence, their `(test: ...)` references renamed with
  the tests.

## Out of scope

- The pull path and the one-shot commands' reads (decision 12 (6), (7)).
- Reading issues on the forge (decision 13): the outside poller and `journal add` stay as they
  are; watching issues can be its own CR later.
- A safety scan in the notification mode (decision 12 (8)).
- The web client (`clients/web/`): no change; it already reads only the API.
- The protocol: no new op or topic; protocol stays 1 (`seats.register` is used as it is).
- The board's bind and key (board-exposure's).
- An idle stop for a board started by hand or by a session's own `board --seat` (decisions 16
  and 19).
- Switching a running board to `--forge-always` (or back): a new op; the "already running" path
  only says it (section 1).
- A configuration key for the watcher's 2 h idle end (decision 21).
- Skipping `4-batch/**/work/` from the fingerprint (the audit's "then, if needed"): not needed once
  walks happen only per settled change.

## Consistency with board-exposure

- The watcher reaches the server on its loopback address (`loopback_base`), so it works with the
  default `127.0.0.1` and with `board.host: network` (`0.0.0.0`).
- The server a watcher starts is a plain `board --seat <id> --stop-idle`: it binds as
  `chantier.yaml` says (default `127.0.0.1`; `network` opens it to the local network); its own
  output is discarded (decision 8), and the watcher prints board-exposure's `BEYOND` line, or its
  `NO_NETWORK` line, for it, which the Chief of Staff passes on (decision 12 (5), section 4).
- The new start line comes after board-exposure's `on this machine:`, `BEYOND` or `NO_NETWORK`
  line, in `_announce` and in the "already running" path, in that order; the `STOPS_IDLE` line
  comes last in the "already running" path.

## Host and default matrix

- Linux (inotify), macOS (FSEvents), Windows (ReadDirectoryChangesW), the planning folder on a
  local disk: notifications; `board: watches the planning files`; `server.json` `files: notify`.
- Any system where `watchfiles` cannot start its watch (watch limit, no backend): `board: no file
  notifications here; checks every 5 s`; `files: check`.
- A network share or a WSL `/mnt` folder: the watch may start yet send nothing (`files: notify`,
  no update): the known limit of `docs/web-board.md`, no test.
- POSIX, watcher-started board: `start_new_session=True`; proved by the scenario on
  `ubuntu-latest` (the board alive after the watcher's end).
- Windows, watcher-started board: `CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW`, no
  `DETACHED_PROCESS`; the board alive after the watcher's end is proved by `chantier gate`'s
  Windows run; "no console window when its writer pushes" is unproved until the user sees that run
  (the PR's Known gaps).
- Claude Code and Copilot: "the watcher-started board outlives the watcher" and "the host does not
  see it as a background task": unproved, with the trial of section 6.
- `board.host` default (`127.0.0.1`): no `BEYOND` and no `NO_NETWORK` line from the watcher;
  `board.host: network` with an address: the `BEYOND` line; with none: the `NO_NETWORK` line.
- A server started by hand, by the session (`board --seat`, a host that cannot run the watcher),
  or by a watcher (detached, `--stop-idle`): the same file-watch lines and mode; only the
  watcher-started one stops after 30 minutes with no client; its `BEYOND`, `NO_NETWORK` and
  file-watch lines reach the Chief of Staff through the watcher's output.
- No client subscribed: no forge read (hub `idle`); one client subscribed: hub cycle every 20 s;
  a board started with `--forge-always` (a host that cannot run the watcher): a cycle every 20 s,
  client or not.
- A watcher with no waking event: ends 2 h after its start (the shipped constant, no key); with
  `events.wake_every` set above 2 h, no sooner than that value.
- A watcher with a server running (this version or another of protocol 1): subscribes, and
  registers the seat when it is this session's; with none: the seat this session's: starts one,
  then subscribes; another session's: ends with the seat line; none: ends with the `no seat` line;
  a seat with no transcript: ends with the `records no session transcript` line; a watcher keyed
  `none`: ends with the `has no session key` line (with a server running, it subscribes).

## Evidence

### Tests (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized)

Every check of a shipped text (`WATCHES`, `CHECKS`, `STOPS_IDLE`, `FORGE_WHEN_OBSERVED`, `BEYOND`,
`NO_NETWORK`, `START`, the `_silent` sentence, the watcher's new end lines) reads the constant from
the package as it ships at the head under test, never a copy.

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
  the `CHECKS` line is printed, a change is seen by the next check (times shortened through the
  `CHANTIER_API_TEST_TIMES` seam's `check` field).
- **The start lines**: `_announce` with each mode prints the exact `WATCHES` / `CHECKS` text after
  the existing lines; the "already running" path prints the line from `server.json`'s `files`, and
  `STOPS_IDLE` last when the entry holds `stop_idle`.
- **The idle stop**: a board context with `--stop-idle` and `observed()` driven by a fake, the time
  passed in: false for `IDLE_STOP_S` minus a second: no stop; one observed moment resets the
  count; false for `IDLE_STOP_S`: `ctx.stop` called once, and the writer's `stop()` (its final
  cycle) runs before the `server` entry is removed (call order recorded); without the flag, no
  stop however long; seats registered and not observing do not count.
- **The forge only while observed**: `HubLoop.poll` with `observed` false for 60 s of passed time:
  `connectors.read` (the seam) never called, the `hub` entry `idle: true`; observed true: a cycle
  at once, then every 20 s. `PushLoop.observed` true with one WebSocket sub, with a long-poll
  within `2*HOLD_S`, false otherwise. With `--forge-always`, `observed` false for 60 s: a cycle
  at once, then every 20 s, the entry never `idle`. `hub_line` prints `forge hub: PID <n>, the
  surface server, idle (no client subscribed)` for an idle entry and `forge hub: PID <n>, the
  surface server, last read <t>` otherwise, and never `a watcher`. `board --stop-idle
  --forge-always`: a usage error. A second `board --seat <id> --forge-always` on a running entry
  with no `forge`: the seat registered, the `FORGE_WHEN_OBSERVED` line.
- **The watcher** (rework `test_watch_events.py`, `test_watcher_step.py`, `test_watcher_autostart.py`,
  `test_forge_hub.py`, `test_surface_server.py::test_one_watcher_holds_the_hub_lock_...` removed or
  rewritten): `Watch` with a fake `Link` feeding `events` lines: filters by audience, ends 20 s
  after the last waking line and no sooner than `wake_every`, ends on a moved seat, cursor moves
  past lines for others; a reconnection resubscribes with `after: <cursor>`; the watcher never
  takes `hub.lock`. Parametrized over the seat and the server:
  - no live server, the seat this session's (`holds_seat` true): the `Popen` seam called once,
    its arguments holding `board --seat <seat.session> --stop-idle`, `DEVNULL` for the three
    streams, `start_new_session=True` on POSIX, or on Windows `creationflags` equal to
    `CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW` with the `DETACHED_PROCESS` bit absent; the
    start line says `started the board (PID <n>)` with the `pid` of the `server.json` entry the
    test writes, which differs from the fake `Popen`'s pid (fix 6);
  - no live server, another session's seat: no `Popen`, the `another session's now; ended` line,
    exit 0;
  - no live server, no seat: no `Popen`, the `no seat for <project>, so no board started; ended:
    ...` line with the `seat take` and `watch --after <cursor>` commands, exit 1;
  - no live server, a seat with an empty transcript: no `Popen`, the `records no session
    transcript` line with the `seat take` and watch commands, exit 1 (fix 5);
  - no live server, the watcher keyed `none` (no host session id): no `Popen`, the seat not read,
    the `has no session key` line, exit 1; a live server and the key `none`: the subscription, no
    `register_seat` (fix 5);
  - a live server, the seat this session's: `register_seat` called once with the project and the
    seat's session, then the subscription (fix 13); a live server, no seat or another's: no
    `register_seat`, the subscription;
  - the server never recorded within the (shortened) 20 s: the `did not start within 20 s` line,
    exit 1; a live-recorded server that never sends `welcome`: the `_silent` sentence, prefixed
    `watch: `, exit 1; a server that refuses the key: the `refused the key of server.json` line
    with the stop and watch commands, exit 1 (fix 8);
  - an entry whose `host` is `0.0.0.0`: the `BEYOND` line follows the start line; `127.0.0.1`
    with `board.host` unset: no `BEYOND`, no `NO_NETWORK`; `127.0.0.1` with `board.host: network`
    in the fixture's `chantier.yaml`: the `NO_NETWORK` line (fix 7); the `WATCHES` or `CHECKS`
    line per `files`.
  - **The idle end** (decision 21), the time passed in and the idle end shortened by the seam's
    third field: no waking event for the idle end minus a second: still running; for the idle
    end: ends with `IDLE` and the `no event for <name> in 2 h` line (the constant), exit 0; a
    waking event before it: the `EVENTS` end, as today; `events.wake_every` above the idle end:
    no end before `wake_every`; `CHANTIER_HUB_TEST_TIMES` with two fields: the shipped 7200 s.
- `just test` stays within its time budget (AGENTS.md).

### Scenario (`scenario/run_scenario.py`, `forge_hub` and `surface_server`; `scenario/README.md`)

- The board's start prints `board: watches the planning files` on `ubuntu-latest` (inotify), and
  the line is in `chantier gate`'s local Windows run too.
- A move through the board's API (`backlog.move`) with a `project` subscription open: the event
  with a new `rev` arrives within 3 s.
- `forge_hub` (README lines ~330-365): with no board, project A's session holding A's seat, A's
  watcher starts one (detached; its start line `started the board (PID <n>)` with the PID
  `server.json` names); B's watcher subscribes to the same board; no watcher holds `hub.lock`; the
  `hub` entry names the board's PID; each cycle one `api graphql` per project with an open PR;
  A's PR merged on the fake forge: A's watcher ends with `forge saw merged ...` and its restart
  line, the merge written once (`source: hub`); B keeps running; two merges within the quiet give
  one end; `--after <n>` replays nothing; checks red at the watcher's end only; the board's PRs
  page first: one line; with every watcher ended and no page, the hub goes idle (`forge hub: PID
  <n>, the surface server, idle (no client subscribed)`) and the fake `gh` is called no more; a
  board started by hand with `--forge-always`, no client: the fake `gh` still called each cycle
  and a merge still written once (`source: hub`), which `watch --once --after <n>` prints;
  a watcher of a project with no seat and no board ends with the `no seat for <project>` line and starts nothing.
- `surface_server` (README lines ~390-422, fix 10): the steps "a watcher of A started while the
  board runs has no `, the hub`", "a watcher that was the hub when the board starts yields" and
  "the board killed hard, a running watcher takes the lock ... `a watcher`" go. In their place: a
  watcher of A started while the board runs subscribes, registers A's seat (the board's
  `seats` count grows) and ends on A's merge with `forge saw merged: ... order merged <cr>`, the
  line written once with `source: "hub"`; the board killed hard (`kill_server`), A's watcher,
  holding A's seat, starts a new board within its next reconnection, resubscribes from its cursor,
  `status` prints `forge hub: PID <new board pid>, the surface server, ...`, and the next merge
  still wakes
  it; the git folder's `chantier/` holds only `server.json`, `server.json.lock`, `hub.lock`,
  `writer.lock`/`writer.wake` where a writer ran, and the `watch-<project>/<session>.lock` files.
- The board started by the watcher is still alive after the watcher's end (decision 8), stops when
  its seat is released (decision 12 (3)), and, in a second run with the `idle_stop` seam field
  shortened, stops by itself with no subscriber after the watcher's end, its `server` entry
  removed and its writer's final cycle recorded (`writer` entry, a pushed commit of a change made
  just before) (decision 16); in that run, with the watcher's idle end shortened too
  (`CHANTIER_HUB_TEST_TIMES`'s third field), a watcher left running with no event ends with the
  `no event for <name> in 2 h` line (the constant's text), and the board then stops idle
  (decision 21).

### Before/after measure (decision 3, in the PR's Deliverables)

On the user's real surface (four projects), the same script before and after: a board serving,
one page open (subscriptions `board`, `project chantier`, `costs`, `prs`), 60 s idle: the number
of `fingerprint()` calls and the total CPU time of the push thread (or `os.times()` of the
process). Before: about 0.65 to 1 s per 2 s pass (the audit). Expected after: no walk while
idle; one walk of one project per settled change. The PR quotes both tables and the head's SHA.

### Gates

`just check` and `just eval-dry-run` in the worktree (a change under the CLI's `src/`); the
pipeline's `just scenario (ubuntu-latest)` green at the PR's head (CLI and cards change); the
batch's top CR runs `chantier gate` locally on Windows (AGENTS.md), which also carries the
Windows no-window observation of section 4. No `hooks/` or `types/` change, so no `just mod`.

## Open questions

None.
