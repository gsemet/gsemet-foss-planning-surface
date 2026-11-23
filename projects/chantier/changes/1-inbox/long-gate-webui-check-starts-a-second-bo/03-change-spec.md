# Board on the next free port from 8765; long gate beside the user's board

Short name: `dynamic-port`. Destination: the running batch batch-31 (dynamic-port-Q2).

## Goal

In the user's words (2026-11-23, own-gate-Q6, carried as dynamic-port-Q1 A): "set up a dynamic
port system: the port is incremented by 1 until a free one is found". The board, `webui` and the
scenario's `webui` check never depend on 8765 being free, so the local long gate
(`chantier gate <cr> scenario`, `just scenario`) passes on Windows while the user's own board holds
8765. Scope: the board's start (default port 8765, then 8766, ...), `webui`'s reuse of a running
board, and the scenario's `webui` check.

This CR absorbs two inbox items, trashed with it when it closes (their goal is this CR's):

- `1-inbox/scenario-s-surface-board-webui-step-must`, with the user's constraint of 2026-11-22:
  "Il faudra rebustifier ce test en CR apres, il faut que ce soit dynamique ou que le tests teste
  plusieurs ports" (make the test robust afterwards, in a CR: dynamic, or the test tries several
  ports), and its wanted outcome: "the step passes with another chantier board already running on
  the machine, with no sleep, retry or skip, and still checks what it checks today". Met: the board
  itself walks the ports (dynamic), the step's skip is removed, no sleep or retry is added, and
  every check of the step stays (part 3).
- `1-inbox/local-just-scenario-passes-while-the-use` (batch-30's retro: the scenario's serve and
  webui cases bind 8765 and expect no board): met by part 3.

## What failed (the evidence this CR starts from)

Gate log `4-batch/3-done/465-agents-update-a-cr-branch-by-rebase-only/work/gates/20261123-142108.log`
(at 37f0cb0, Windows, the user's board listening on `127.0.0.1:8765`, PID 18292):

- `FAIL surface-board (github): \`webui\` on a running server prints \`board already running at <link>\``.
- The unit transcript (`surface-board-github.md`, lines 844-849) shows the path: the step
  `serve_and_webui` (`scenario/run_scenario.py`, about line 2770) starts its first server with an
  explicit `--port DEFAULT_PORT`; an explicit port held is refused (`board not started`), so the
  step notes "the default port 8765 is held by another program here", skips the second-surface
  step and restarts the first server on `free_port()`, reading one stdout line with no check that it
  is the start line. `chantier webui` then found no live `server` entry for that surface
  (`state.live_server`) and started a second board (`board on http://127.0.0.1:65141/...` with the
  idle-stop line) instead of printing `board already running at`.
- Why the restarted first server was not live and recorded when `webui` ran is not known: the
  scenario captures its stderr but never prints it (part 0).

Today's code (read at main `b4cb7066`):

- `board/address.py`: `DEFAULT_PORT = 8765`; `settings()` takes `--port`, else `board.port` of
  `chantier.yaml`, else the default.
- `board/binding.py`: `bind(host, port, held, other)` binds once; on "address in use" it takes an
  OS-picked port (`bind(host, 0)`) and prints `TAKES_PORT` only when `other()` names another
  chantier board; any other holder refuses with `held()`'s text.
- `board/command.py`: `_listen()` passes `other` only when the port is the default (no `--port`, no
  `board.port`); `_other_board()` and `_held_by()` probe the port's holder.
- `commands/webui.py`: reads the surface's `server.json` record (`Board.recorded` →
  `state.live_server`), prints `_running_lines` for a live board, else spawns
  `<cli> serve --stop-idle` (no `--port`) and waits up to 20 s for its record.

## What changes

### 0. First, the reproduction (dynamic-port-Q5 A)

Before any change, the Driver reproduces the failure on Windows at the batch's base: the user's
board on 8765 (or, absent it, a plain socket held on `127.0.0.1:8765`),
`just scenario --unit surface-board`, with the restarted first server's stderr captured and written
to the transcript (its `BoardProc.p.stderr`, and its stdout lines past the first). The PR's
description names the cause found (for instance: the restart's start line came after the 20 s
`line()` wait; the restart refused; its record was not live). When that cause is not the port
itself (it would survive parts 1 and 3), the CR fixes it too, and the PR says how. The reproduction
log is kept in the CR's `work/` folder.

### 1. The board's start: the next free port from the default (`board/binding.py`, `board/command.py`)

- When the port is the default one (no `--port`, no `board.port` in any `chantier.yaml` layer: the
  case `_listen()` already calls `default`), the start tries 8765, then 8766, 8767, ..., one bind
  each, and keeps the first port it binds. A port counts as held, and the walk goes on, on
  "address in use" (`errno.EADDRINUSE`, Windows `WSAEADDRINUSE` 10048) and, on Windows, on
  "access denied" (`WSAEACCES` 10013, the error of a port in a reserved range or held exclusively).
  Any other bind error refuses as today (`board not started: <reason>`).
- The walk no longer depends on who holds the port: another chantier board (another surface's,
  or one behind another key) or another program both make it go on. The OS-picked port
  (`bind(host, 0)`) of today's takeover is gone from this path.
- The walk ends at port 65535 (`MAX_PORT`, `playbook/board_check.py`). With no free port up to
  there it refuses with one line, exit 4 (`EXIT_EXTERNAL`):
  `board not started: no free port from 8765 to 65535 on <host>: pass --port <n> (0: any free port)`.
- When the port kept is not the default, the start prints one line before its start line,
  naming only the default port's holder (one probe of 8765, as `_other_board` does today; the
  ports skipped after it are not probed):
  `board: port 8765 is held by <holder>: this one takes port <n>`, where `<holder>` is
  `another chantier board (<served folder>)` (a board that answers this surface's key but serves
  another folder), `another chantier board (another project's key)` (a board that refuses this
  key: the usual case of another surface's board, each surface having its own key) or
  `another program`. The first two keep today's text, so a reader of today's line still parses it.
- Unchanged: an explicit `--port <n>` or a configured `board.port` is used as is, and a held one
  still refuses with `_held_by()`'s text and its way out (`pass --port <n> (0: any free port)`, `or
  change board.port in chantier.yaml`); `--port 0` stays the system's pick.
- A board of this same surface that already runs is found before any bind by its record
  (`_recorded`, `server.json`), or at 8765 (`_answering`, the default address), and the start
  prints `board already running at`. A board of this surface on a walked port whose record is lost
  is not found, and a second one may start: an accepted risk (dynamic-port-Q6 A).
- `server.json` records the port actually bound (it already does: `state.write_server(..., bound,
  ...)`), so every reader of the record (`webui`, a watcher, `live`, `status`) reaches the board
  wherever the walk put it.
- Each `.py` file stays under 400 lines: `board/command.py` is at 381 lines today, so the walk and
  the holder's naming go in `board/binding.py` (52 lines), `command.py` only passing what it knows
  (the default case, the probe).

### 2. `webui` (`commands/webui.py`)

No change of behaviour is owed: `webui` already reads the record, so it reuses a running board on
any port, and the board it spawns (`serve --stop-idle`, no `--port`) walks as in part 1. Its 20 s
wait for the record stays. The Driver confirms it by the checks below and changes this file only
if a check, or part 0's cause, shows a need.

### 3. The scenario's `serve_and_webui` step (`scenario/run_scenario.py`)

- The first server starts with no `--port` (`serve --host 127.0.0.1`, the default walk), never
  `--port DEFAULT_PORT`. Its output is read line by line: when the default port is held (the user's
  board, or anything else), the first line is the `board: port 8765 is held by ...: this one takes
  port <n>` line and the next is the start line on `<n>`; else the start line on 8765. Its stderr
  goes to the transcript when its start line does not come.
- A check, before any other in the step, that the first server's start line came and parses
  (`Link(...).ok`), with its port at or above `DEFAULT_PORT`, and, when its port is not 8765, that
  the takes-port line came first and names that port. A slow or failed start then fails on its own
  label, never as the `webui` check.
- The fallback (`the default port 8765 is held by another program here: the second-surface step is
  skipped`) is removed: the second surface's server (no `--port`) always runs. Its check becomes:
  its first line starts with `board: port 8765 is held by ` and ends with `this one takes port
  <n>`, its start line is on `<n>`, `<n>` is at or above 8765 and differs from the first's port;
  when the first holds 8765, the holder named is `another chantier board (another project's key)`
  (the second surface probes 8765 with its own key, which the first refuses). The cookie checks
  that follow are unchanged.
- The `webui` check is unchanged in what it asserts (`board already running at
  http://127.0.0.1:<the recorded port>/?k=<key>`); it now runs against a first server known to be
  up and recorded.
- The rest of the step (kill, `webui` starting `serve --stop-idle`, `two_keys`) is unchanged; the
  board `webui` starts walks from 8765 like any default start.
- No sleep, retry or skip is added to the step (the 2026-11-22 constraint).
- No other scenario board depends on 8765: the others pass `--port 0` or a `free_port()`, or write
  a free `board.port` (`board_port()`); they are left as they are. The Driver greps
  `run_scenario.py` for `DEFAULT_PORT` and `8765` and leaves none that asserts 8765 is free.

### 4. Tests (`skills/chantier/scripts/cli/tests/`)

- `test_serve_webui.py::test_a_default_port_held_by_another_surfaces_board_takes_a_free_one`
  becomes the walk's test: a default port held by another surface's board, by a board behind
  another key, or by a plain program now starts on the next free port above it, with the
  takes-port line naming the holder (`another program` for the plain one) and the port bound; a
  named `--port` held still refuses (`is held by` / `is in use`, exit 4, nothing printed on stdout).
  It asserts the port taken is the first free one above the held one (two held in a row skip
  both), not just "another port".
- One case for the end of the walk: no free port up to 65535 refuses with the `no free port`
  line, exit 4 (a prepared bind that always says "in use", named as such: a real machine cannot
  hold every port).
- One case for Windows' `WSAEACCES` counted as held (a prepared bind raising it), since a Linux
  run cannot produce it.
- `test_board.py` (an explicit `--port` held refuses) and `test_board_exposure.py`
  (`settings()` still returns 8765 as the default) stay as they are and still pass.
- The tests stay few and parametrized; `just test` within its time limit.

### 5. Text that names the behaviour

- `declare/serve.py`, `--port`'s help: `the port, or 0 for a free one the system picks (default:
  chantier.yaml's board.port, used as is, else 8765 or the next free port above it)`.
- `docs/web-board.md`:
  - line 206, "The link": the link reads `http://<address>:<port>/?k=<key>` (no longer `:8765`),
    with one clause that the port is 8765 unless held, then the next free one above it, as the
    start line prints;
  - the `chantier.yaml` example (about line 274): `port: 8765  # default: 8765, or the next free
    port above it when held; a port set here is used as is`.
- `evals/README.md`, lines 88-91 (step 2, "No board left running from an earlier run"): a board
  left running no longer makes the next run's board fail (it takes the next free port), but it
  still serves the old surface and holds its writer: the step keeps "stop any `chantier serve`
  still running", drops "its port (8765 by default) in use made run 2's board fail", and checks for
  a running board on 8765 and the ports just above it (`Get-NetTCPConnection -State Listen` /
  `lsof -iTCP -sTCP:LISTEN`, filtered on the `chantier` process), or by the surface's
  `server.json`.
- `scenario/README.md`, the `serve` and `webui` bullet (CR-456): the second surface's `serve` takes
  the next free port from 8765 and prints `board: port 8765 is held by ...: this one takes port
  <n>`; the first server also starts on the default walk.
- `AGENTS.md` (dynamic-port-Q4 A: this CR may reword it): "one that finds the default port held by
  another chantier board takes a free port and prints it" becomes "one that finds the default port
  held (by another chantier board or any program) takes the next free port above it and prints
  it".

## Decisions carried

- dynamic-port-Q1 A: the default port 8765 is tried, then +1 until a free one is found; the board,
  `webui` and the scenario's `webui` check never depend on 8765 being free (parts 1 to 3).
- dynamic-port-Q2 A: specified for the running batch batch-31.
- dynamic-port-Q3 A: Windows' exclusive bind (`SO_EXCLUSIVEADDRUSE`) is out of scope; it is not
  set here. Its follow-up is the inbox item `1-inbox/two-surface-servers-run-at-once-on-one-p`
  (two servers of one surface on `127.0.0.1:8765` and `0.0.0.0:8765` at once on Windows).
- dynamic-port-Q4 A: this CR rewords AGENTS.md's sentence on the default port (part 5).
- dynamic-port-Q5 A: the Driver first reproduces on Windows with the first server's stderr
  captured, names the cause in the PR, and fixes it if it is not the port (part 0).
- dynamic-port-Q6 A: a board of this surface on a walked port with no record is an accepted risk;
  a running board is found by its record, or at 8765 (part 1).

## Out of scope

- The `stack` unit's 769.0 s over its 750 s budget in the same run: seen once, on a loaded machine
  (four units at once, other sessions running); `scenario/README.md` says a unit over its budget
  only warns, and the run's status for it was `over budget`, not `FAIL`. This CR changes neither the
  unit nor its budget. A second sighting is a CR of its own, with a measurement.
- `SO_EXCLUSIVEADDRUSE` on Windows (dynamic-port-Q3 A; follow-up
  `two-surface-servers-run-at-once-on-one-p`).
- An explicit `--port` or a configured `board.port`: no walk (part 1).
- Other ports of chantier (the eval kit's sandbox, `scripts/docs_screenshots.py`): untouched.
- The watcher's start of a board, `live`, `status`: unchanged; they read the record.

## Host and default matrix (evidence, one line per cell)

- Windows, default port held by the user's board (`127.0.0.1:8765`): the board starts on the next
  free port, prints the takes-port line naming `another chantier board (another project's key)`;
  `just scenario --unit surface-board` passes all its checks (the reproducer of this CR).
- Windows, default port free: the board starts on 8765, no takes-port line (scenario and tests
  when nothing holds 8765).
- Linux (CI `ubuntu-latest`), default port free or held: the same two behaviours; the long gate's
  `scenario` job green at the PR's head.
- macOS: covered by `just check` only (`EADDRINUSE` path); the walk not exercised in a scenario
  there: untested.
- Configured `board.port` or explicit `--port` held, any host: refuses as today
  (`test_board.py`, the scenario's "a port held by another program exits 4" check).
- Windows `WSAEACCES` (reserved range): only the prepared-bind test; not exercised on a real
  reserved port.

## Evidence

- Part 0's reproduction log in `work/`, and the cause named in the PR.
- `just check` passes (Linux, macOS, Windows), and `just eval-dry-run` in the worktree (a change
  under the CLI's `src/`).
- The tests of part 4.
- On the user's Windows machine, with the user's board running on 8765 (or, absent it, a plain
  socket held on `127.0.0.1:8765` for the run): `just scenario --unit surface-board` passes every
  check, the transcript showing the first server's takes-port line and `webui` printing `board
  already running at` the first server's link. Then, per AGENTS.md, the CR on top of the batch's
  stack passes `chantier gate <cr> scenario` locally.
- The pipeline's long gate `just scenario (ubuntu-latest)` green at the PR's head (a CLI change).
- `wc -l` of every changed `.py` under `src/` below 400.

## Open questions

None.
