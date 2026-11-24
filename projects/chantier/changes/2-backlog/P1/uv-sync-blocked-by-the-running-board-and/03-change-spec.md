# Restart the board on this checkout's build, and keep it there

Short name: `board-restart`. Origin: the user's report of 2026-11-22 (batch-30, Windows), P1,
next batch. Folds in the inbox item `which-build-starts-the-surface-server-wi`
(board-restart-Q2). Facts checked against `main` at 3c29dd7c.

## Goal

In the user's terms: after a merge that touches the board, the board must run the new code, by a
documented, one-step way, without hunting the process; and on a surface shared by several projects,
the chantier dev session's own build serves the surface, instead of Studio's cached build coming
back every time it is stopped.

## Where it stands

- **Item 1 of the request is done.** `uv sync --locked` blocked by the board or a watcher holding
  `.venv` was handled by 56f753e6 (`feat(sync): a blocked uv sync names chantier's holders, waits,
  never kills`): `skills/chantier/references/sync-checkout.md` (six steps: check, name the holders,
  `sync pending`, the 3-minute message, the offer to stop the session's own board and watcher on
  the user's yes), the "Name the holders" rows of `hosts/claude-code.md` and `hosts/copilot.md`,
  AGENTS.md's sentence "a sync that chantier's own processes block names them and waits, never
  stopping or killing one but the session's own board and watcher on the user's yes". This CR does
  not reopen it and changes none of `sync-checkout.md`'s steps.
- **No clean stop exists.** A board stops by itself (its seats gone, `Seats._loop` in
  `board/seats.py`; or 30 minutes idle with `--stop-idle`, `board/idle.py`), or by the host's stop
  of the background shell that started it, or hard: every refusal names `running.stop_command`
  (`taskkill /PID <n> /T /F` on Windows, `kill <n>` elsewhere; `board/running.py`), which skips the
  `finally` of `_run` in `board/command.py` (the Griller runs' stop, the writer's final cycle,
  `writer.stop()`, the removal of the `server` entry). The published API (`board/api/ops.py`,
  `protocol.json`) has no stop op.
- **Any seated watcher starts the board from its own build.** `Watch.connect` (`hub/watch.py`)
  calls `start_board` whenever `server.json` names no live server, for its own project's seat
  (`seat_rule`), spawning `serve --seat <session> --stop-idle` of its own CLI (`hub/feed.py`,
  `serve_argv`). A lost link is retried every `RETRY_S` (5 s), so after any stop the first seated
  watcher of any project, Studio's included, starts the board again from its build.
- **What the session is told.** `hub/lines.py` (`board_lines`, `foreign_build_clause`: `board runs
  another build of chantier <v> (<source>), not this checkout's`, `board runs a build of chantier
  <v> older than this notice (source unknown), not this checkout's`), the watcher's start line
  clause `; board is chantier <v>: restart it to run this version` (`hub/watch_lines.py`,
  `OTHER_VERSION`), and `serve`'s refusal `chantier serve <v> (PID <n>) already serves this surface
  ...: to replace it, stop it (<stop command>), then run serve again` (`board/command.py`,
  `_another_version`). The cards then forbid acting: `session-start-chief-of-staff.md` ("`board
  already running at <URL>`" item: "say it once to the user as printed, never stop or restart the
  board"; the `error: board not started: chantier serve <v> ... already serves this surface` item:
  "Never stop it yourself ..."), and `chief-of-staff.md`, watcher paragraph "*When it starts:*"
  ("never stop or restart the board yourself", "say it once to the user as printed; never stop or
  restart the board").
- **The seat records no build.** `SeatRecord` (`core/records.py`: `session`, `transcript`, `env`,
  `title`, `link`; unknown keys kept) is written by `seat take` only (`commands/seat.py`, `_take`).
  `seat.json` is local (the planning folder's `.gitignore`), never published.

## What changes

### 1. A clean stop: the private-key op `server.stop` (board-restart-Q1)

- New op `server.stop` in `board/api/ops.py` and `board/api/protocol.json`, over the WebSocket and
  over HTTP as every op. Not in `READ_OPS`: the public key gets the existing `READ_ONLY` refusal.
- It refuses with one line while a client's `cli.run` command runs (`ctx.runs`, `board/idle.py`
  `Runs`): `refused: a client's command runs on this board; try again when it ends`, so a command
  is never cut. Otherwise it answers `{"stopping": true, "pid": <pid>}`, then sets the board's stop
  (`ctx.stop`, the `_Stopper` of `board/command.py`, Ctrl-C's path). The existing `finally` of
  `_run` does the rest in its order: the board's Griller runs stopped (`stop_all("the board
  stopped")`), the idle thread, the writer's final cycle (`writer.stop()`), the file watch, the
  push, the hub, the `server` entry removed. Nothing is added to that order.
- It messages no agent and records nothing in a batch.

### 2. The one action: `chantier serve --restart` (board-restart-Q1)

- New flag `--restart` on `serve` (`declare/serve.py`, `board/command.py` `board()`), with every
  other `serve` option as today (`--seat`, `--forge-always`, `--host`, `--port`, `--ui`, ...);
  `--restart` with `--stop-idle` is a usage error (a restarted board is the session's own,
  foreground in its background shell, as "Run the board" starts it).
- Steps:
  1. The Q2 guard (section 3): when it holds for this build, refuse (exit precondition) with one
     line: `error: board not restarted: a chantier dev session (<session>) holds its seat; its
     build (<source>) serves this surface`. Nothing is stopped.
  2. No live recorded board (`state.live_entry(git_dir, state.SERVER)` is none, and none answers
     at the configured address): print `board: none was running` and go on as plain `serve`.
  3. A live board: send it `server.stop` with the private key of `server.json`. Its refusals,
     each one line, exit precondition, nothing stopped:
     - an unknown op (a board older than this change): `error: board not restarted: chantier serve
       <v> (PID <n>) has no clean stop; the user stops it by hand (<stop command>), then run serve
       --restart again`;
     - the key refused, or no answer within 20 s (the board is silent): the same sentence, with
       `refused the key` or `does not answer` in place of `has no clean stop`;
     - the `cli.run` refusal of section 1, passed on as is.
  4. Wait for the stopped process to end: its PID no longer alive and the `server` entry gone (or
     naming another PID), polled every 0.5 s, at most 120 s (the writer's last cycle may fetch and
     push). Past 120 s: `error: board not restarted: chantier serve <v> (PID <n>) is still
     stopping after 120 s (its writer's last cycle); run serve --restart again later`, nothing
     killed.
  5. Print `board stopped: chantier <v> (PID <n>, <source>)`, then run as plain `serve` does today
     with the options given (the stopped board's options are not copied), on this process's
     build: the usual start lines, `board on ...` and the rest. When another board was started in
     the gap (a watcher of this build, or a race), `serve`'s existing `board already running`
     path prints its lines, and the foreign-build line when it is another build, as today.
- `serve` is not run through a profile and is excluded from `cli.run` (AGENTS.md); `--restart`
  keeps both exclusions.
- The help text of `serve` (`declare/serve.py` `HELP`) names `--restart` in one line: "stop the
  running board cleanly, after its writer's last cycle, then serve on this build".

### 3. Which build serves a shared surface (board-restart-Q2)

- `seat take` (`commands/seat.py`, `_take`) writes a new optional field `build` in `seat.json`:
  `state.build_source()` when the run is in the dev mode (`plugin_files.is_dev_mode(repo)`),
  nothing otherwise. `SeatRecord` gains `build: str | None = None`. An older seat without `build`
  claims nothing until the seat is taken again.
- "A chantier dev session holds its seat" is read as: the surface's project that
  `launch.is_chantier_project` names (the project folder `chantier`) has a `seat.json` naming a
  session with a `build`, and that session's watcher lock is held now
  (`hub/lock.py` `watchers(git_dir, <that project>)` holds the seat transcript's key, kept as
  `autostart.session_key` keeps it). The live lock is the evidence the seat is held now, so a seat
  an ended session left behind blocks nothing. One function in `hub/autostart.py` (for example
  `dev_build(repo) -> tuple[str, str] | None`, the session and the build) reads it, from any
  project of the surface; off a planning surface it returns none.
- The guard holds for a process when `dev_build` returns a build that is not
  `state.build_source()` of that process.
- **Other projects' watchers start no other board.** In `Watch.connect`, when no live server is
  recorded and the guard holds, the watcher spawns nothing: it keeps no link, sets `lost_at` and
  tries again every `RETRY_S` as on a lost link, until a board runs (it links and registers its
  seat as today), the guard stops holding (it then starts the board as today), or one of its usual
  ends. Its start line, when it starts this way, ends with the clause `; no board started: a
  chantier dev session holds its seat and its build serves this surface; linking when its board
  runs` (a constant in `hub/watch_lines.py`). A watcher whose build is the dev build (the dev
  session's own) starts the board as today.
- `serve --restart` refuses under the guard (section 2, step 1). Plain `serve`, `webui` and the
  watcher of the dev session itself are unchanged (open question 1).
- A board already running on another build is not stopped by the guard: the dev session is told by
  today's lines (`board runs another build ...`) and the Chief of Staff offers the restart
  (section 4).

### 4. The cards

The cards are cut by CR-471 (`slim-the-startup-cards-of-the-three-role`, batch-31): every edit
below is made at the rebased head, in whichever piece holds the quoted text then.

- `skills/chantier/references/session-start-chief-of-staff.md`, item "`board already running at
  <URL>`": replace "say it once to the user as printed, never stop or restart the board" with: say
  it once to the user as printed, with the offer of the restart (below). Item "`error: board not
  started: chantier serve <v> (PID <n>) already serves this surface ...`": the user's choice now
  includes the restart; "never start one on another port to get round it" stays. Add one short
  paragraph, "Restart the board": on a `board runs another build`, `board runs a build of chantier
  <v> older than this notice`, `board is chantier <v>: restart it to run this version` or `board:
  chantier <v> serves this surface ...` line, or after a merge that changes the board's code
  (`skills/chantier/scripts/cli/src/chantier/board/`, `hub/`, `writer/`, `clients/web/`) in the
  dev mode, offer once, in one line with its cost: the board, the surface's writer and the hub are
  off for every project of the surface for the stop's length (up to two minutes), and a board
  Griller run in progress ends. On the user's yes, each time (a yes covers one restart, never the
  next): run `$CHANTIER serve --restart --seat <id>` (with `--forge-always` on a host that cannot
  run the watcher) by the host's background means ("Run the board" row), read its first lines and
  pass them on as the board's start lines are. A refusal: one line to the user with the printed
  stop command, never run by the agent. No answer or a no: say nothing more until the next such
  line. While `sync pending` holds, the sync goes first (`sync-checkout.md`); the restart is not a
  sync's stop and `sync-checkout.md` is unchanged.
- `skills/chantier/references/chief-of-staff.md`, watcher paragraph "*When it starts:*": "say it
  once to the user with the restart; never stop or restart the board yourself" and "say it once to
  the user as printed; never stop or restart the board" become: say it once to the user with the
  offer of the restart (`session-start-chief-of-staff.md`, "Restart the board"); the board is
  stopped only by that restart, on the user's yes. Add, in the same paragraph, the watcher's new
  clause (`no board started: a chantier dev session holds its seat ...`): pass it on once; the
  watcher links by itself when the board runs.
- `skills/chantier/references/hosts/claude-code.md` and `hosts/copilot.md`, row "Run the board":
  add that `serve --restart --seat <id>` runs by the same means.
- `skills/chantier/references/startup-manifest.json`: none, unless CR-471's cut places
  "Restart the board" in a piece that an action must name; then that action names it.

### 5. AGENTS.md

- The stop rule: the surface server's sentence "one a watcher or `webui` started stops by itself
  when its seat leaves or 30 minutes after its last subscribed client, after its writer's last
  cycle" gains: and any board, whoever started it, stops on a private-key client's `server.stop`
  (refused while a client's command runs), after its writer's last cycle; `chantier serve
  --restart` sends it, then serves on its own build, run by the Chief of Staff on the user's yes
  each time (board-restart-Q1).
- The hub's start sentence "started by a session's watcher, detached, when none runs and the
  session holds the seat" gains: and no chantier dev session of the surface holds its seat with
  another build (its `seat.json`'s `build`, its watcher's lock held); such a watcher waits and
  links when the board runs (board-restart-Q2).
- The build paragraph ("The board server, its writer and the forge hub, started from another
  project's session, run that build ... until stopped by hand and started again from a chantier
  session"): rewrite to say that while a chantier dev session holds its seat its checkout's build
  serves the surface, other projects' watchers start no board, and a board of another build is
  replaced by `serve --restart` on the user's yes; the notice of another build stays.
- The sync sentence ("never stopping or killing one but the session's own board and watcher on
  the user's yes") is unchanged.

### 6. Files the CR touches

- CLI: `board/api/ops.py`, `board/api/protocol.json`, `board/command.py`, `declare/serve.py`,
  `core/records.py`, `commands/seat.py`, `hub/autostart.py`, `hub/watch.py`,
  `hub/watch_lines.py` (all under `skills/chantier/scripts/cli/src/chantier/`); `board/options.py`
  for the `--restart`/`--stop-idle` usage error.
- Cards: `session-start-chief-of-staff.md`, `chief-of-staff.md`, `hosts/claude-code.md`,
  `hosts/copilot.md` (and `startup-manifest.json` only as section 4 says).
- `AGENTS.md`.
- Tests and scenario: below.

## Overlaps and order

- **CR-471** (`slim-the-startup-cards-of-the-three-role`, in batch-31): cuts `chief-of-staff.md`
  and moves its rules into pieces. This CR's card edits are made after CR-471 is merged, at the
  rebased head, by quoted text, not by line number.
- **`watcher-runs-through-several-events-inst`** (P1 backlog, `watcher-limit`): changes the
  watcher's end (no 2 h limit while a batch runs) in `hub/watch.py`, the Chief of Staff card,
  `hosts/claude-code.md` and AGENTS.md's watcher sentence. Both change the watcher's start and its
  life around the board: ordered, not in parallel (`02-answers.md`); this CR's guard in
  `Watch.connect` and its retry must hold under that CR's longer-lived watcher (a watcher waiting
  for the dev build's board ends only by the rules in force at the rebased head).
- **`two-surface-servers-run-at-once-on-one-p`** (inbox): not folded in unless the user says so
  (open question 2).

## Out of scope

- Item 1 of the request (the blocked `uv sync`): done by 56f753e6.
- Any change to `sync-checkout.md`'s steps, or a restart used to free a sync.
- Stopping or killing a board by PID from the agent or the CLI: the hard stop stays the user's.
- Copying the stopped board's options into the new one; a board restarted by itself on a merge
  (the restart is always on the user's yes).
- The web client: no restart button.

## Host and default matrix

| Host | Mode | What holds |
|---|---|---|
| Claude Code | dev (chantier's checkout, project chantier) | `seat take` writes `build`; the restart runs by `Bash`/`PowerShell` `run_in_background`; the new board runs `uv run --no-sync` code |
| Claude Code | plugin (another project) | no `build` in its seat; its watcher waits under the guard; its restart refuses under the guard, works otherwise on its plugin build |
| Copilot | dev / plugin | the same, by the host's background shell ("Run the board" row) |
| any | no planning surface (in-project) | the guard never holds; the restart works as above |

## Evidence

- `tests/test_server_api*.py` (or a new parametrized `test_board_restart.py`): `server.stop` with
  the public key gets `READ_ONLY`; while `ctx.runs` counts a running command it gets the
  `cli.run` refusal and the stop is not set; with the private key it answers `stopping` with the
  PID and the stopper is set. The protocol's op count moves from 27 to 28 in
  `tests/test_server_protocol.py` and in `scenario/run_scenario.py` ("the 27 ops and 8 topics").
- `serve --restart` refusals, parametrized, on a prepared `server.json` and a fake probe: the guard
  line; an older board's unknown op; a refused key; a silent board; the 120 s wait (with a fixed
  clock); `--restart --stop-idle` usage error; no board running prints `board: none was running`.
- `tests/test_watcher_autostart.py` / `tests/test_watch_board.py` (with `watch_fakes.py`):
  parametrized over (a chantier seat with `build` and its watcher lock held, without the lock,
  without `build`, the watcher's build equal to it): spawn or no spawn as section 3 says; under the
  guard the start line ends with the new clause and the watcher links once the fake board appears.
- `seat take` in the dev mode writes `build` equal to `state.build_source()`; in the plugin mode
  writes none (`tests/test_launch_modes.py` or the seat tests).
- A check on the shipped cards, reading the files from the repository at the head under test:
  `session-start-chief-of-staff.md` and `chief-of-staff.md` (or their CR-471 pieces) no longer hold
  "never stop or restart the board" and name `serve --restart`; `hosts/claude-code.md` and
  `hosts/copilot.md` name it in "Run the board".
- `just scenario`, the surface server unit (16d, "The forge hub"): a watcher starts the board; a
  `serve --restart --seat <id>` run in the background stops it (the old PID ends, its `writer`
  entry and `server` entry are gone before the new start line), then prints `board stopped:` and
  `board on ...`, the new PID answers the probe with the same key. A second step: a seat of the
  surface's `chantier` project with a `build` not this run's and a held watcher lock; another
  project's watcher started with no board prints the new clause and spawns nothing. Runs in the
  long gate on Linux (CI) and, as AGENTS.md says, locally on Windows for the CR on top.
- `just check`; `just eval-dry-run` (the change is under the CLI's `src/`).

## Open questions

1. Q2 names the watchers only. Should plain `serve` (the Chief of Staff's on a host with no
   watcher, or the user's by hand) and `webui` refuse too under the guard, as `serve --restart`
   does here, or stay as today?
2. Fold in the inbox item `two-surface-servers-run-at-once-on-one-p` (a second start on
   `0.0.0.0` beside one on `127.0.0.1` on Windows), or leave it to its own CR (`02-answers.md`:
   the user decides)?
3. "Holds its seat" is read here as `seat.json` naming the dev session and that session's watcher
   lock held now, so a stale seat blocks nothing; but while the dev session's watcher is down
   (between two runs), another project's watcher may start its own build's board. Confirm this
   reading.
