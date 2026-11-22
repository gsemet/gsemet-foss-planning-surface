# Rename the surface server's command to `serve`; add `webui`

Change Specification, written 2026-11-22 from `intake/request.md` and `02-answers.md` (copied from
the parent CR `remote-cli-commands-through-the-surface-`: remote-cli-Q1, Q3, Q6, Q11, Q14 and the
Chief of Staff's decision; the user said "grilled enough"). No issue. Part A of three stacked CRs
in batch-30 (A, this one; B `two-board-keys-a-public-read-only-key-an`; C
`remote-cli-commands-through-the-surface-`), before CR-447 docs-gardening, which documents them.
One Driver, at most 4 rounds. It touches the CLI's `src/`, the cards and the scenario: `just
check` and `just eval-dry-run` before the first push, `just scenario (ubuntu-latest)` green before
the PR. No change under `hooks/` or `types/`, none to the web client's files.

## Goal

The user's names (Q1): `chantier serve` starts the surface server, today's `chantier board`;
`chantier live` stays the terminal client; `chantier webui` prints the web board's link with its
key and, when no server runs, starts one (Q3, Q14), with no further question: typing it is the yes.

## Decisions carried (02-answers.md)

1. Q1: `serve`, `live`, `webui`.
2. Q3: `webui` prints the board's link with its key, and starts the server when none runs.
3. Q14: always, with no further yes; AGENTS.md names `webui` as a third starter of the server and
   its forge hub.
4. The Chief of Staff: a server `webui` starts has no seat and stops 30 minutes after its last
   client (`--stop-idle`).
5. Q6, Q11: batch-30, first of the stack A→B→C, before CR-447.

## What changes

### 1. The command

- `declare/board.py` becomes `declare/serve.py`: `add_command(sub, "serve",
  "chantier.board.command:board", HELP, NO_BATCH)`, the same options (`--host`, `--port`,
  `--seat`, `--clock`, `--ui`, `--new-key`, `--stop-idle`, `--forge-always`) and help text.
  `cli.py` imports it in place of `board`; its `if args.cmd != "board"` (no writer notes) reads
  `"serve"`. No alias: `chantier board` is argparse's "invalid choice" (no fallback).
- The package keeps its name (`chantier.board.*`, `clients/web`); `chantier.yaml`'s `board:` key
  (host, port) keeps its name; the web page's title "chantier board" names the product and stays.
- The printed prefixes, which name the web board and which the cards, the watcher and the scenario
  quote, stay: `board on <link> over <folder>`, `board already running at <link>`, `board not
  started: ...`, `board: ...`, the watcher's `started the board (PID <n>)`. Only the words that
  name the command to run change:
  - `board/command.py` `_another_version`: `chantier serve <v> (PID <n>) already serves this
    surface at <link>; this is chantier <v>: to replace it, stop it (<stop>), then run serve
    again`.
  - `board/running.py` `silent_text`: `..., then run serve again`; `find_pid` matches a command
    line holding `chantier` and `serve` or `board` (an older build's server still running is still
    found).
  - `writer/lines.py` `START`: `$CHANTIER serve --seat <session id> --forge-always`; `older_text`:
    `chantier serve <v> (PID <n>) serves this surface with no writer`.
  - `hub/watch_lines.py` `NO_KEY` and `NOT_STARTED`: `{cli} serve --seat ...`.
  - `commands/live.py` `NO_BOARD`: `start one with chantier serve (or chantier webui), or pass
    --url <link>`.
  - `declare/watch.py` help: `(chantier serve)`.
- The watcher's autostart: `hub/feed.py` `board_argv` becomes `serve_argv`, returning `[*cli,
  "serve", "--seat", session, "--stop-idle"]`; `hub/watch.py` calls it.
- Docstrings naming the command: `chantier/__init__.py`, `board/__init__.py`, `board/command.py`,
  `board/static.py`, `board/address.py`, `commands/__init__.py`, `hub/__init__.py`, `hub/lock.py`,
  `hub/loop.py`, `hub/state.py`, `hub/watch.py`, `playbook/board_check.py`, `playbook/layers.py`.

### 2. `chantier webui` (new `declare/webui.py`, `commands/webui.py`, NO_BATCH)

Help: "print the web board's link, with its key; start the surface server, detached, when none
runs (it stops by itself 30 minutes after its last client)".

- A server recorded live for this surface or project (`hub/state.live_server`) that answers the
  probe (`board/address.probe`): the lines of `board/command._running_lines` (`board already
  running at <link>`, `on this machine: <link>` when it differs, the network line, the file-watch
  line, the idle-stop line), exit 0.
- None: it starts `serve --stop-idle` detached, with no `--seat`, through the watcher's means
  (`hub/feed.spawn`, argv `[*shlex.split(cli_command(repo)), "serve", "--stop-idle"]`, cwd the
  served folder); it waits up to 20 s (the watcher's `START_S`) for `server.json` to name a live
  server answering the probe with its key, then prints `board on <link> over <folder>`, `on this
  machine: <link>` when it differs, the network line when not loopback, and `board: stops by
  itself after 30 min with no client (webui started it)`. Past 20 s: `error: webui: the server did
  not start within 20 s: run <cli> serve and read its error`, exit 4. A recorded server that does
  not answer: `error: webui: <running.silent_text>`, exit 4. It asks nothing, takes no seat and
  opens no browser.
- A server `webui` started is not the session's own (its command line holds no `--seat`): the
  dev-mode sync's step 6 (session-start.md) does not offer to stop it; it stops by its idle rule.

### 3. AGENTS.md

- "The surface server, `chantier board`:" becomes "`chantier serve`:"; every other `board` there
  stays a word for the process.
- The forge hub's starters: "started by a session's watcher, detached, when none runs and the
  session holds the seat, on the user's one yes for the watcher and the board, or by the Chief of
  Staff on a host that cannot run the watcher" gains ", or by `chantier webui` when none runs (the
  user's typing it is the yes; that server has no seat and stops by itself 30 minutes after its
  last client)"; "one a watcher started stops by itself ..." becomes "one a watcher or `webui`
  started stops by itself ...".
- The named tools: "`webui`: prints the web board's link with its key, and starts the surface
  server, detached, when none runs; built on the user's answers remote-cli-Q1, Q3 and Q14
  (2026-11-22), with no measured cost".

### 4. Cards, hosts and docs

- Every `$CHANTIER board`, `chantier board` and backticked `board --<flag>` becomes `serve`, in:
  `session-start.md` (lines 82, 87, 98, 115, 125, 129, 137, 141, 167, 172 and step 6 at 328: the
  holders' subcommand `board` becomes `serve`, the own server's rule keeps `--seat <this
  session's id>`, and a `webui`-started server is named as not own), `chief-of-staff.md` (the
  routing rows "board on my phone" and "a new board key", line 47's `--new-key` included, and the
  seat hand-over at line 2020, `board --seat <id> --forge-always`), `hosts/claude-code.md` (line
  39, the holders' subcommand; the "Run the board" row; line 54's `board --seat <id>
  --stop-idle`; the remote board row), `hosts/copilot.md` (the "Run the board" row and line 46),
  `coder.md`, `concepts.md`, `debugger.md`, `verifier.md`. The `chief-of-staff.md` row "board on
  my phone", "where is the board?" adds: "`$CHANTIER webui` prints the link (and starts the server
  when none runs)". `agents/` and `com.github.copilot/agents/` hold no such mention today; if one
  appears, both hosts change together.
- Docs, the command's name only (CR-447 rewrites the rest): `README.md`, `CONTRIBUTING.md`,
  `docs/boards.md`, `docs/demo/AGENTS.md`, `docs/planning-modes.md`, `docs/server-api.md`,
  `docs/web-board.md`, `evals/README.md`, `scenario/README.md`, `scripts/docs_screenshots.py`
  (its start command and docstring). `docs/release-notes/` is history: untouched.

### 5. Tests and scenario

- Every CLI call of `board` becomes `serve` in `tests/` (`test_board*.py`,
  `test_surface_server.py`, `test_surface_writes.py`, `test_writer_lines.py`, `test_access.py`,
  `test_watch_board.py` and what `git grep` finds) and in `scenario/run_scenario.py`
  (`BoardProc(sw, "board", ...)`).

## Overlaps in batch-30

- CR-446 (live-several-boards-and-keys) edits `commands/live.py`; this CR changes one constant
  there (`NO_BOARD`): whichever lands second rebases it.
- CR-449 (board-griller) writes `chantier board --new-key` in AGENTS.md, `docs/web-board.md` and
  the panel's text. If it lands first, this CR renames it (the check below finds it); if it lands
  after, its Driver writes `chantier serve --new-key` (the Chief of Staff tells it).

## Out of scope

- The keys (part B), the profiles and the remote commands (part C), the web UI's move to its own
  project, and the docs beyond the command's name (CR-447).

## Evidence

- A test that reads, from the repository at the head under test, the cards
  (`skills/chantier/references/**/*.md`), the agent files of both hosts, `AGENTS.md`,
  `CONTRIBUTING.md`, `README.md`, `docs/**/*.md` but `docs/release-notes/`, `evals/README.md` and
  `scenario/README.md`, and finds none of: `$CHANTIER board`, `` `chantier board `` followed by
  a space or a backtick, `` `board --`` (a backticked `board` with a flag). Paired with one
  prepared text holding each form, to prove the check finds it.
- The renamed lines are checked from the shipped constants (`test_board_running.py`,
  `test_writer_lines.py`, `test_watch_board.py`), not copies; `serve_argv` returns `serve --seat
  <s> --stop-idle`; `find_pid` finds a process whose command line holds `serve`, and one holding
  `board`.
- `webui`, in-process with the spawn, the record and the probe faked (parametrized): a running
  server prints `board already running at`; none starts `serve --stop-idle` with no `--seat` and
  prints `board on` and the idle-stop line; no record within 20 s exits 4 with its sentence; a
  silent recorded server exits 4.
- `chantier board` exits with argparse's invalid choice.
- Scenario: in the `surface-board` unit, `webui` on the running server prints `board already
  running at <link>`; after the server is stopped (`surface_kill`), `webui` starts one (its
  command line holds `serve --stop-idle`, no `--seat`), prints `board on`, and the server answers
  `board.get`; it is then stopped. The watcher's start still starts `serve --seat ...
  --stop-idle`, seen by its command line.

Host and default matrix: none; nothing here depends on the host or on a configured value (the
`board.host` key works as today, under the new command's name).

## Open questions

None.
