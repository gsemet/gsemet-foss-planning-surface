# Investigation: CR-484 one board per surface, and a watcher that reaches the forge hub

Read in the worktree (`origin/main`), under `skills/chantier/scripts/cli/src/chantier/` (below `src/`).
Nothing was run or changed. The project's rules (AGENTS.md, CONTRIBUTING.md, scenario/README.md) say
nothing more on evidence than what is quoted here.

## Findings that shape the change

1. The server already says who it is, on both transports. `GET /api/board` (`board/routes.py`
   `probe`) answers `pid`, `version`, `served`; the WebSocket's `welcome` (`board/api/ws.py`
   `_welcome`, `protocol.ServerInfo`) carries `server.pid`. Nothing to add on the server side.
   What is missing is on the client: `clients/tui/link.py` `Linked` holds only `transport`, `now`,
   `reason`, and `Link._socket` drops the welcome's pid (`yield Linked("ws", welcome.get("now"))`).
2. `hub.lock` is already "the surface is held by a serving process, for its whole life" in all but
   name: only `chantier serve` takes it (`HubLoop`, `hub/loop.py`), it is an OS lock released at
   exit or death, and the scenario's file-list check (`scenario/run_scenario.py` ~3783) and
   AGENTS.md already name it. Its flaw is that it is taken by a thread after the bind and the
   `server` entry, so a process that never wins it still serves (the observed stray).
3. `Watch._take` (`hub/watch.py`) counts any `Linked` with a transport as linked. That is the
   whole watcher-side gap, plus: `Watch._link` never re-reads `server.json` while a link lives, so
   a link that stays up to a non-recorded process is never questioned.

## Where each change goes

### A. One server per surface: the claim (`board/command.py`, `hub/loop.py`, `hub/lock.py`)

Reuse `hub.lock` (class `lock.HubLock`), no new file, so AGENTS.md needs no new lock name and the
scenario's "chantier/ holds only ..." assertion (run_scenario.py ~3783) stays true.

- `board()` in `board/command.py` (lines 338-387): take `lock.HubLock(git_dir).acquire()` before
  the `state.live_entry` / `_recorded` / `_answering` check, hold it through bind and
  `write_server`, and pass the held lock to `HubLoop(projects.home, lock=held)` (a new optional
  argument; `HubLoop.__init__` builds its own when none is given, so `test_surface_server.py` and
  `test_board_idle.py` keep working). `HubLoop.poll` then never needs to elect: `self.hub is None
  and self.lock.acquire()` stays true at once because `acquire()` returns True when the handle is
  already held (`_FileLock.acquire`, line 45).
- Order: acquire; then the existing check. If the check finds a live board, release the lock and
  return its "board already running" lines (the existing branch, lines 353-365). If the lock is not
  won (another process starts, or serves), wait up to a bound (suggest 20 s, `START_S`'s value,
  step 0.2 s) for `server.json` to name a live server that answers, then take the join branch; past
  the bound, raise `_silent(...)` (today's silent-board text) when an entry exists, else
  `_not_started` with a new one-line "another start holds the surface".
- Why the loser then "joins": a start that loses is the second `serve`; the watcher's detached
  spawn that loses exits with no output (stdout is DEVNULL) and the watcher's `start_board` already
  waits for a live recorded server that answers the probe. No change needed there.
- `serve --restart` (CR-478): `restart.restart` already waits until the old PID is dead
  (`_ended`), and the OS releases the lock at death, so the new start wins it. `_migrated` runs
  `restart_with_key` before the claim; keep that order (the claim comes after it, before the
  check at line 352).
- `--forge-always`, `--stop-idle`, `--seat`: unaffected; `_observer` unchanged.
- The `finally` of `_run` (line 211-222) already stops the hub, which releases the lock via
  `HubLoop.stop`. With the claim held by `board()`, release it in the same `finally`/on every
  early `raise` between claim and `_run` (`files.stop(); sock.close()` branch at line 374-377, a
  refused bind in `_listen`). Use one `try/finally` around claim..`_run`.

### B. "Port held" on any address (`board/binding.py`)

- Windows: in `_open`, set `SO_EXCLUSIVEADDRUSE` (`socket.SO_EXCLUSIVEADDRUSE`) before `bind`. The
  wildcard-versus-specific coexistence is the cause; with it a second bind raises WSAEACCES (10013)
  or WSAEADDRINUSE (10048), both already treated as held by `_held`.
- Portable, and the one the "step 2" test should assert on all three systems: a held-anywhere
  check inside `bind()` before `_open`: `connect_ex` to the requested host (loopback when it is
  `0.0.0.0` or `::`) and to loopback on that port with a short timeout (0.2 s); a connect that
  succeeds counts as held and goes through `_stop_or_walk` exactly as an `EADDRINUSE`. It does not
  depend on `SO_REUSEADDR` semantics, which differ on macOS (specific bind can coexist with a
  wildcard listener when both set it), Linux (refuses) and Windows (allows). A real-socket test on
  an ephemeral port fails today on Windows and macOS and passes on Linux, which is what the spec's
  step 2 needs. Do both: the exclusive option for Windows, the connect check for the rest.
- Risk: `SO_EXCLUSIVEADDRUSE` refuses a bind while connections of an earlier listener on the same
  port are in TIME_WAIT on some Windows builds; `serve --restart` on the same port is the case. The
  existing scenario step `restart_board` (16d1c, run_scenario.py 2924) rebinds the same port after a
  clean stop, so it is the check; the walk (default port) would hide a failure, a named port would
  show it (that step names `--port`, good).
- The new check must keep `tests/test_serve_webui.py` green: it monkeypatches `binding._open` and
  `bind("h", 8765, ...)` with a fake host `"h"`. Put the connect check in a separate function
  (`_held_elsewhere(host, port)`) called from `bind`, patchable, and make the fake-host tests
  patch it out (or skip it for a host that does not parse as an address).

### C. A stray server stops by itself (`board/command.py` `_run`, `hub/state.py`)

- Use the existing tick: `PushThread` calls `on_pass` every `push_every_s()`
  (`board/api/push.py`; `command._run` passes `state.reassert_server`). Add a second small callable
  (or extend the lambda) `stray(git_dir) -> bool`: read `server.json`; the `server` entry names a
  pid other than `os.getpid()` and `state.live_entry(git_dir, SERVER)` says that process is live
  -> `stop()` (sets `server.should_exit`, the clean stop path, writer's last cycle included).
  Never write `server.json` (only `remove_entry`, which already removes by PID, runs in `finally`).
- `reassert_server` already refuses to put its own entry "over another process's entry"
  (state.py line 262): the stray check is the same read, so put the helper beside it
  (`state.recorded_other(git_dir) -> int | None`).
- Bound: one `push_every_s()` pass plus the server's stop time; name it "within about 5 s" after
  checking `times.push_every_s()`'s default. A loser that stops should print one stderr line
  (`board: another server (PID n) holds this surface; stopping`).
- With A in place a duplicate cannot appear after the fix; this covers a leftover from an older
  build, whose process holds neither `hub.lock` (new build holds it: the old one only tries it)
  nor, necessarily, the claim. A process of the previous build does not run this check, so it
  never stops itself; only a stray of the new build does. Say so in the PR.

### D. The watcher confirms the server (`clients/tui/link.py`, `hub/feed.py`, `hub/watch.py`, `hub/watch_lines.py`)

- `link.py`: add `pid: int | None = None` to `Linked`; in `Link._socket` pass
  `welcome.get("server", {}).get("pid")`. In `_http`, the poll answer has no server info; leave
  `pid` None there. `link.py` has an import-only-itself test (`test_live_link.py` line 345): no new
  import.
- `feed.py`: `LinkFeed._pass` already forwards `Linked`. For an HTTP transport (`pid` None) the
  watcher confirms with `Board.probe(host, port, key)`, which returns the dict with `pid`
  (already faked by `FakeBoard.probe`).
- `watch.py` `_take`: on `Linked` with a transport, compare its pid (probe's, when None) with the
  recorded entry's pid (`self.board.recorded(git_dir)` re-read, not the `self.entry` from connect
  time). Equal: `unlinked_since = None` as today. Different: close the feed, set `lost_at = now`,
  keep `unlinked_since` (the clock to `SILENT_S` keeps running), remember the pid seen
  (`self.stray = pid`). `_link` at `SILENT_S`: when `self.stray`, end with a new line
  `STRAY` (in `watch_lines.py`) naming both PIDs and the remedy (stop the stray with
  `running.stop_command(pid)`, then start the watcher again: `{watch}`) instead of
  `running.silent_text`.
- Relink after a restart: in `_link`, while a feed is up, re-read `recorded` every `RETRY_S` (cheap:
  a file read and one psutil call); if its pid differs from the linked server's pid (or it is gone),
  close the feed and `connect(now)` from the cursor. This is the only new poll. A server's death
  already yields `Linked(None)` and a relink at `RETRY_S`; the new read covers a restart where the
  old process lingers, and a stray that the `Linked` check missed. The cursor is kept (`self.cursor`
  is passed in `link(...)`), so no line is lost or told twice (existing test
  `test_a_lost_link_is_opened_again_from_the_cursor_and_repeats_no_line`).
- The Foreman's watcher takes the same code (`connect` raises `FOREMAN_NO_SERVER` when none is
  recorded; unchanged).
- "A watcher never says it runs while it receives nothing": covered by the `SILENT_S` end; the
  start line (`Watch.start`) says "started the board" only when `connect` returned a started pid:
  also require the recorded pid to equal the started one (`found[0]["pid"]` is read from
  `server.json` after the spawn: with A, a spawned loser leaves the winner's entry, and the line
  "started the board (PID n)" would name the winner's pid although this watcher did not start it).
  Compare with the spawned process: `subprocess.Popen` returns a `pid`; `Board.spawn` returns None
  today (feed.py `spawn`): make `spawn` return the Popen pid and print "started the board" only
  when it equals the recorded entry's pid, else "board already running" (the spec's last bullet
  of "The hub entry and status"). `FakeBoard.spawn` must return a pid; `serving()` sets
  `PID = 4242`, so return 4242 there.

### E. `status` (`hub/lines.py`, `hub/state.py`, `hub/cycle.py`)

- `hub_line` stays. `watch_lines()` (lines 16-36) gets the new case: this session's watcher lock is
  held and (`hub` entry `idle` is true, or the recorded `server` pid differs from the `hub` pid, or
  no hub entry): print one line instead of "watch: this session's watcher runs" next to
  "forge hub: idle". New text, e.g. `watch: this session's watcher runs but the forge hub sees no
  client (hub PID n, server PID m): the watcher is not subscribed to the hub; stop the stray with
  <stop_command>, then restart the watcher`. Keep the existing pull-path suffix.
- Two live servers: `status` can see a live server that is not recorded only through a probe of
  the recorded port (a connect to a process that answers with another pid). Smallest: no probe
  in `status` (it reads files only; `watch_lines` is called on every `status`). Instead the
  stray is named by the watcher's end line (D) and the stray's own stderr line (C); `status` covers
  "recorded server pid != hub pid" (possible after a crash of one) and the watcher-without-hub
  case. State that the second bullet's "if `status` can see them" is not met by a file read and is
  left to D and C.
- `hub/cycle.py`: the spec allows a client count; not needed (pr-conflict-Q4: the subscription is
  the signal). Keep `idle`. No change to `hub/state.py` beyond the helper in C. `PushLoop` has a
  `_subs`/`_polls` count if the Driver wants `clients: n` in the hub entry; it costs a publish per
  change, so leave it out.

### F. AGENTS.md and cards

- AGENTS.md: sentences at lines 30-35 (git-folder files; no new file if `hub.lock` is reused),
  ~139-150 (the hub: "the same process is the forge hub ... it holds the OS file lock
  (`chantier/hub.lock`)": say it is taken at start and held for the process's life, the single-server
  claim), ~174-185 (the watcher: confirms the recorded server, relinks, ends with the stray line),
  ~223-232 (the writer, unchanged), ~244-253 (`serve`'s start lines). Add: one serving process per
  surface and machine; a second start joins or refuses; a server that finds another recorded
  stops by itself; "port held" on any address. Keep every exception (`--forge-always`, key rules).
- Cards: the double start comes from `session-start-chief-of-staff.md` ("The watcher", ~line
  100-111: "A yes starts both ... the watcher starts the board") and the host references' "Run the
  board" and "Run the watcher" ("On a surface, `$CHANTIER serve --seat <id>` ..." and the
  `--restart` offer, ~lines 84-92), plus `chief-of-staff.md` line 34 and `chief-of-staff.md` ~265
  ("its own `serve --seat <id> --forge-always`"). With A the race is harmless; add one sentence to
  the session-start card: starting the board by hand and the watcher in the same turn is safe, the
  later start prints `board already running` and joins. Both-host agent files: grep found none
  naming this (re-check `agents/` and `com.github.copilot/agents/` for "serve" before the PR; this
  investigation did not open them).
- `docs/boards.md` and `scenario/README.md` (line ~483 lists the git-folder files; the new step
  needs its own section there; `test_scenario_coverage.py` ties the scenario's steps to the README).

## Tests to extend (in `skills/chantier/scripts/cli/tests/`, few, parametrized)

- Bind: `test_serve_webui.py` (has `_hold`, `Refused`, the walk tests). Add a parametrized real-socket
  test: a socket listening on `0.0.0.0:<p>` (and the reverse), `binding.bind("127.0.0.1", p, held,
  None)` raises the held text; with `holder` it walks to `p+1`. Runs on the three systems. It fails
  today on Windows (and probably macOS).
- Double start: `test_board_running.py` (`test_a_new_board_reuses_refuses_or_starts_by_what_the_surface_already_runs`,
  `_prepare_board`, monkeypatches `command._bind`). Add a case: the claim held by another handle
  (`lock.HubLock(git).acquire()` in the test) with a live recorded entry: "board already running",
  nothing bound; and with no entry for longer than the (shortened, patched) bound: `_silent` or the
  new refusal. Use a thread to take the lock and write the entry after 0.2 s for the race.
  A real two-process test is the scenario's.
- Stray stop: `test_surface_server.py` or `test_board_idle.py` (idle stop tests with `IdleStop`
  and a fake `stop`): call the stray helper with a `server.json` naming another live PID (the
  test process's parent or `os.getpid()` with a patched `getpid`), assert `stop` called and
  `server.json` bytes unchanged.
- Watcher: `test_watch_board.py` with `watch_fakes.FakeBoard`: extend `JournalFeed` with a `pid`
  and `Linked(transport, pid=...)`; cases: the feed answers with another pid -> not linked, relink,
  `STRAY` line after `SILENT_S` naming both PIDs; recorded pid changes mid-run -> new `link()` from
  the cursor (`board.feeds` records the `after`), no repeated line.
- `status`: `test_forge_hub.py` line ~352 (hub_line) and the `status` tests near
  `test_status_index_services.py`/`test_watcher_autostart.py`: a prepared `server.json` (hub idle)
  plus a held `lock.WatcherLock` -> the new line, never both old lines.
- `test_code_targets.py` (function and file size, import cycle) will bite: `board/command.py` is
  387 lines and `hub/watch.py` 387; new code goes to small helpers in new modules
  (`board/claim.py`, `hub/watch_confirm.py`) rather than growing them.

## Evidence plan

Kind: a change to the CLI's `src/` (server start, bind, watcher, status), no UI, no pane. No
screenshot owed (no `hooks/register.tsx` change, no web client change).

- Before/after: the tests above (each fails on `origin/main`: the bind test on Windows and macOS,
  the double start on every system, the stray, the watcher confirm, the status line). Capture the
  failing run at the pre-fix head as `evidence/before-tests.log` (run `just test` with only the new
  tests applied to the old code, or `git stash`-free: write the tests first, run, commit).
- Live (spec's step 3): quote the listening table, the two command lines and the `server.json`
  entries (keys removed) from the specification into the PR. They cannot be reproduced now (PID
  37316 stopped).
- Scenario step (`scenario/run_scenario.py`, new function `one_board`, registered near
  `restart_board` at lines 123 and 11891, section note "16d1d" like the existing ones; add its README
  section): with `SurfaceWorld` and `BoardProc`: start `serve --host 127.0.0.1` and, at once,
  a `watch` of a seat that would spawn one (the watcher needs the seat/transcript as the 16d1c step
  does with `seat take`); assert exactly one `serve` process for the surface
  (`surface_pid`, plus `psutil` children listing or a connect to the port that answers one pid),
  the second one printed `board already running` and exited, the watcher's start line, the `hub`
  entry `idle` absent after the watcher subscribes (`surface_entry` reads the file), a merge of
  the scenario's PR journalled (`fake_gh.py`; see the existing `forge_hub` step for a merged PR)
  and told by the watcher. Then `serve --restart` on the same port and assert the same watcher
  process (same PID) prints its next event once and the `hub` entry pid is the new server's. The
  running scenario is the Windows run of `chantier gate <cr> scenario` that AGENTS.md owes this
  batch's CRs, and the ubuntu job the other.
- `just check` (Linux, macOS, Windows in the pipeline), `just eval-dry-run` (change under `src/`),
  `just scenario` as above. No `just mod` (no `hooks/` or `types/` change).

Cannot be shown: the real macOS bind behaviour before the fix (only the pipeline's macOS run shows
the bind test failing or passing), the live double server of 2026-11-24, and a live board with a
real forge.

## Risks

- `HubLock` held by `board()` for the process's life changes who can hold the hub: any code that
  assumes `HubLoop` elects (tests `test_surface_server.py` lines 95-125 take a second `HubLock` and
  expect the loop to elect when the other lets go). The optional `lock=` argument keeps those.
- A claim that waits (up to the bound) while a first start is slow: a `chantier serve` that is the
  loser can block 20 s; `watch` spawns detached, so it never shows. A user's `serve` in a terminal
  shows the delay: print nothing, or one line after 2 s.
- A live recorded server of another version: `_recorded` / `_answering` raise
  `_another_version` as today, now after the claim: release the lock on that raise.
- Search for the old value: nothing measures from sizes here. The values that derive from the
  port-held rule: `WSAEACCES`/`WSAEADDRINUSE` in `binding._held`, `WAY_OUT`, `TAKES_PORT`
  (printed by the walk), and the tests in `test_serve_webui.py` / `test_board.py` line 112 (named
  port held text). The connect check must not change those texts.
- `connect_ex` to a port the board itself is not yet bound to: nothing listens, so it is not
  held; but a probe against a board of another project on that port makes the walk go on, as an
  `EADDRINUSE` would today.
- `Linked(transport, pid)` is a frozen dataclass with positional `now` second: add `pid` last, so
  `test_live_link.py` stays valid.
- File sizes: `board/command.py`, `hub/watch.py`, `clients/tui/link.py` (398) are near the
  `test_code_targets.py` limits: check the limit before adding more than a few lines.

## Questions only the user can answer

None. Two choices for the Driver, not the user: the claim reuses `hub.lock` (recommended, no new
file); the server's identity is the existing `pid` of `welcome` and of `/api/board` (no
protocol change), with a probe for the HTTP transport.
