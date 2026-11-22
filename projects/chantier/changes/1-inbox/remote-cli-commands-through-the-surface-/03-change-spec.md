# Remote CLI commands through the surface server; `chantier serve`

Change Specification, written 2026-11-22 from `intake/request.md` and `02-answers.md`
(remote-cli-Q1 to Q8, the user's answers of 2026-11-22; no `01-intent.md`; the user said "grilled
enough"). No issue. Batch-30, placed right before CR-447 docs-gardening, which waits for it and
documents it: this CR keeps the cards, the help texts, AGENTS.md and the API reference true, and
renames the command in the docs mechanically, nothing more. One Driver, at most 6 rounds. It
touches the CLI's `src/`, the cards and the scenario: `just check`, `just eval-dry-run` before the
first push, and `just scenario (ubuntu-latest)` green before the PR. No change under `hooks/` or
`types/`. No change to the web client's files.

## Goal

In the user's words: turn the terminal client into a family of CLI commands, so that other agents
act from the command line, remotely, through the surface server ("take, ..."). Once a machine is
logged in to a server (`chantier login <link>`, like `gh auth login`), every chantier command run
there goes to that server, which runs it in its planning folder and gives back the output and the
exit code. The server's command becomes `chantier serve`; `chantier live` stays the terminal
client; `chantier webui` prints the web board's link with its key, and starts the server when none
runs. On the server's own machine, with no login, everything stays local, as today.

## Decisions carried (02-answers.md)

1. Q1: `chantier serve` starts the surface server (today's `chantier board`); `chantier live` stays
   the terminal client; `chantier webui` is the web UI's command.
2. Q2: the batch commands go through the server too, in this CR; AGENTS.md's rule that the server
   "never edits a batch" gets a named exception.
3. Q3: `chantier webui` prints the board's link with its key, and starts the server when none runs.
4. Q4: a login like `gh auth login`; once logged in the commands remember the server; profiles,
   one of them the default.
5. Q5: every CLI command runs remotely, `order`, `open` and `cancel` included (see "What runs
   where" for the few that cannot by nature, and the open question 1).
6. Q6: batch-30, right before CR-447 docs-gardening.
7. Q7: with an active default profile, every command goes to the server; `--profile local` (or
   `chantier logout`) runs it locally again. On the server's machine no login is needed.
8. Q8: one file in the user's config folder (`~/.config/chantier/`, `%APPDATA%\chantier\` on
   Windows), like `gh`; a named exception to AGENTS.md's rule that chantier writes only in the
   planning folder.
9. From the brief (the summary the user approved): the web UI moves to its own project later (out
   of scope); the rename touches the cards, the watcher's autostart, the docs and the scenario.

## What changes

### 1. `chantier board` becomes `chantier serve`

- `declare/board.py` becomes `declare/serve.py`: `add_command(sub, "serve",
  "chantier.board.command:board", HELP, NO_BATCH)`, same options (`--host`, `--port`, `--seat`,
  `--clock`, `--ui`, `--new-key`, `--stop-idle`, `--forge-always`), same help text. `cli.py`
  imports it in place of `board`; its `if args.cmd != "board"` (no writer notes) reads `"serve"`.
  No `board` alias: `chantier board` becomes an argparse "invalid choice" (no fallback).
- The internal package keeps its name (`chantier.board.*`, `clients/web`): only the command is
  renamed.
- The server's printed lines keep their prefixes, which name the web board and which the cards,
  the watcher and the scenario quote: `board on <link> over <folder>`, `board already running at
  <link>`, `board not started: ...`, `board: ...`. Only the words that name the command to run
  change, `board` to `serve`:
  - `board/command.py` `_another_version`: `chantier serve <v> (PID <n>) already serves this
    surface at <link>; this is chantier <v>: to replace it, stop it (<stop>), then run serve
    again`.
  - `board/running.py` `silent_text`: `... then run serve again`; `find_pid` matches a process
    whose command line holds `chantier` and `serve` or `board` (a server of an older build, still
    running, is still found).
  - `writer/lines.py` `START`: `$CHANTIER serve --seat <session id> --forge-always`; `older_text`:
    `chantier serve <v> (PID <n>) serves this surface with no writer`.
  - `hub/watch_lines.py` `NO_KEY` and `NOT_STARTED`: `{cli} serve --seat ...`.
  - `commands/live.py` `NO_BOARD`: `start one with chantier serve, or pass --url <link>`.
  - `declare/watch.py` help: `(chantier serve)`.
- The watcher's autostart: `hub/feed.py` `board_argv` returns `[*cli, "serve", "--seat", session,
  "--stop-idle"]` (rename the function `serve_argv`, its docstring too).
- Docstrings that name the command: `chantier/__init__.py`, `board/__init__.py`,
  `board/command.py`, `board/static.py`, `board/address.py`, `commands/__init__.py`,
  `hub/__init__.py`, `hub/lock.py`, `hub/loop.py`, `hub/state.py`, `hub/watch.py`,
  `playbook/board_check.py`, `playbook/layers.py`. `chantier.yaml`'s `board:` key (host, port)
  keeps its name.
- Cards, every `$CHANTIER board` and `chantier board` to `serve`: `chief-of-staff.md` (the two
  routing rows of lines 46 and 47), `coder.md`, `concepts.md`, `debugger.md`, `verifier.md`,
  `session-start.md` (five places, the quoted error line included), `hosts/claude-code.md` (the
  "Run the board" row and the remote board row), `hosts/copilot.md`. `agents/` and
  `com.github.copilot/agents/` hold no such mention today (check with `git grep`); if one does,
  both hosts change together.
- Docs, mechanical rename of the command only (CR-447 rewrites the rest): `README.md`,
  `CONTRIBUTING.md`, `docs/boards.md`, `docs/demo/AGENTS.md`, `docs/planning-modes.md`,
  `docs/server-api.md`, `docs/web-board.md`, `evals/README.md`, `scenario/README.md`,
  `scripts/docs_screenshots.py` (its start command and docstring). The release notes under
  `docs/release-notes/` are history: not touched.
- Tests and scenario: every CLI call of `board` becomes `serve` (`tests/test_board*.py`,
  `test_surface_server.py`, `test_surface_writes.py`, `test_writer_lines.py`, `test_access.py`,
  `test_watch_board.py` and the others `git grep` finds; `scenario/run_scenario.py`'s
  `BoardProc(sw, "board", ...)` calls).

### 2. `chantier webui`

New `declare/remote.py` (with `login` and `logout`, section 3) and `commands/webui.py`, NO_BATCH.
Help: "print the web board's link, with its key; start the surface server, detached, when none
runs (with a profile: the profile's server's link, nothing started)".

- With an active profile (section 3): one line, `board at <base>?k=<key> (profile <name>)`;
  nothing started, nothing read on the network.
- Without one, a server recorded live for this surface or project (`hub/state.live_server`) that
  answers the probe (`board/address.probe`): the lines of `board/command._running_lines` (`board
  already running at <link>`, `on this machine: <link>` when it differs, the network line, the
  file-watch line, the idle-stop line), exit 0.
- Without one and no server running: it starts `serve --stop-idle` detached, with the watcher's
  means (`hub/feed.spawn`, argv `[*shlex.split(cli_command(repo)), "serve", "--stop-idle"]`, cwd
  the served folder), no `--seat`; it waits up to 20 s (the watcher's `START_S`) for
  `server.json` to name a live server that answers the probe with its key, then prints `board on
  <link> over <folder>`, `on this machine: <link>` when it differs, the network line when it is
  not loopback, and `board: stops by itself after 30 min with no client (webui started it)`.
  Past 20 s: `error: webui: the server did not start within 20 s: run <cli> serve and read its
  error`, exit 4. A recorded server that does not answer: `error: webui: <running.silent_text>`,
  exit 4. It opens no browser.
- `webui` never forwards (section 4).

### 3. Profiles: `chantier login` and `chantier logout`

New module `clients/profiles.py`: the profiles file and nothing else.

- Folder: on Windows `%APPDATA%\chantier\`; elsewhere (Linux and macOS, like `gh`)
  `$XDG_CONFIG_HOME/chantier/` when set, else `~/.config/chantier/`. One function
  `config_dir(platform, environ)` decides, so a test covers the three cells.
- File: `profiles.json`, plain JSON, UTF-8, written atomically (a temporary file in the folder,
  then `os.replace`), mode 0600 on POSIX (it holds keys); the folder is created on the first
  login. Content:
  `{"default": "<name>" | null, "profiles": {"<name>": {"url": "<base>", "key": "<key>",
  "project": "<id>" | null, "served": "<folder>", "version": "<v>", "saved": "<UTC stamp>"}}}`.
  `url` is the base address `commands/live.from_link` returns (scheme, host, port, path prefix,
  trailing `/`). An unreadable or malformed file is `error: profiles: <path>: <reason>: fix or
  delete it`, exit 2, for every command that reads it (no silent local run).
- The active profile of a run: `--profile <name>` when given (`local`: none, the run is local),
  else the file's `default`, else none. `--profile` is a root option (`cli.py`'s `_parser`) and,
  like `--project`, accepted after the command (`commands/registry.add_command`). An unknown name:
  `error: --profile <name>: no such profile (<the names>, or local)`, exit 1.
- `chantier login <link> [--profile NAME] [--project ID]`: parses the link with
  `commands/live.from_link` (same refusals), probes the server with the `board.get` op over HTTP
  (`POST <base>api/v1/call/board.get`, the key in the `X-Chantier-Board-Key` header, 10 s), and on
  success stores the profile (`NAME`, default `default`; `local` refused, exit 1) and makes it the
  default (the last login wins, like `gh`). `--project` must be one of the projects `board.get`
  lists (else `error: login: --project <id>: the server serves <ids>`, exit 1); omitted, none is
  stored and the server's home project is used. Output, two lines, the key never printed:
  `logged in: profile <name> → <base> (chantier <v> over <served>), the default` and `every
  chantier command now runs on that server; --profile local runs one here, chantier logout ends
  it`. Refusals, nothing stored: a 401, `error: login: the server refused the key: give the link
  it printed (chantier webui prints it)`, exit 4; no answer, `error: login: no chantier server
  answers at <base>: <reason>`, exit 4.
- `chantier login` with no link: the profiles, one line each, `<name> → <base> (project <id> |
  the server's home project)`, the default marked `(default)`, or `no profile: commands run here`;
  no network, writes nothing.
- `chantier logout [--profile NAME]`: removes the named profile, or the default one; when it was
  the default, no default remains (the commands run locally). Output: `logged out: profile <name>;
  commands run here again` (or `...; the default stays <name>` when another one was removed). No
  such profile: `logout: no profile <name>`, exit 0. It never reaches the server.

### 4. The client: a command forwarded to the server (`cli.py`, new `clients/remote.py`)

`cli.main` parses the arguments as today (so `--help` and argparse's usage errors stay local, from
the client's own version), then reads the active profile. With none, the run is local, exactly as
today. With one:

- **What runs where.** Never forwarded, run locally whatever the profile: `serve`, `webui`,
  `live`, `login`, `logout` (the server itself, its clients and the profiles). Refused under an
  active profile, because they run something on the caller's machine and write local records:
  `watch`, `gate`, `lease <unit> hold`: `error: <cmd> runs on the server's machine, not through a
  profile: run it there, or here with --profile local`, exit 1. Every other command is forwarded,
  `open`, `order`, `cancel`, `take`, `round`, `handback`, `close`, `preflight`, `file`, `summary`,
  `journal add` included.
- **The request.** `POST <base>api/v1/call/cli.run`, the key in the header, a JSON body
  `{"argv": [...], "project": <id> | null, "env": {...}, "stdin": <text> | null}`, with the same
  HTTP means and proxy rule as `chantier live`'s long-poll (`clients/tui/link.py`), a client
  timeout of 630 s:
  - `argv`: the command line as given, with `--profile`, `--project` and `--skill` (each in its
    `--opt value` and `--opt=value` forms, before or after the command) removed; the rest as text,
    unchanged.
  - `project`: the `--project` given, as its last path component (`projects/chantier`, an absolute
    folder or the bare name `chantier` all give `chantier`), else the profile's `project`, else
    null (the server's home project).
  - `env`: of this process's environment, only these names, when set: `CHANTIER_BATCH`,
    `CHANTIER_HOST`, `CLAUDE_CODE_SESSION_ID`, `CLAUDE_CODE_ENTRYPOINT`,
    `COPILOT_AGENT_SESSION_ID`, `COPILOT_CLI`, `AI_AGENT` (the batch, the host and the session the
    command speaks for). One constant, `FORWARDED_ENV`, shared with the server.
  - `stdin`: only for `journal add --json -` (today's one reader of stdin), the client's stdin
    decoded `utf-8-sig`; null otherwise.
- **The answer.** A 200 carries `{"code": int, "stdout": str, "stderr": str, "version": str}`: the
  client writes `stdout` to its stdout and `stderr` to its stderr as they are (the server's child
  has already cut its lines and added its writer notes; the client adds neither) and exits with
  `code`. A refusal is one `error: remote: ...` line on stderr, exit 4, and nothing run locally
  (no fallback):
  - no answer: `error: remote: profile <name>: no chantier server answers at <base>: <reason>;
    run it here with --profile local, or chantier logout`;
  - 401: `error: remote: the server at <base> refused the key of profile <name>: log in again with
    the link it prints (chantier webui)`;
  - 404 `unknown op`: `error: remote: the server at <base> runs an older chantier with no remote
    commands: stop it and start it again (chantier serve) from this version`;
  - 404 project, 400, 504: `error: remote: <the server's error>`.

### 5. The server: the `cli.run` op (new `board/cli_run.py`)

- `board/api/protocol.py`: `CliRunArgs(_Model)` with `argv: list[str]` (at least one item),
  `project: str | None = None`, `env: dict[str, str] = {}`, `stdin: str | None = None`; added to
  `OP_ARGS` as `"cli.run"`; `protocol.json` rewritten with its `just` recipe. `board/api/ops.py`'s
  `HANDLERS` gains `"cli.run"`. The op is on both bindings, like every op (HTTP `POST
  /api/v1/call/cli.run`, the WebSocket `call`), behind the same key.
- Its checks, each a refusal with nothing run: an `argv[0]` that is not one of the CLI's commands,
  or is `serve`, `webui`, `live`, `login`, `logout`, `watch`, `gate`, or a `lease ... hold` (400,
  `cli.run: <cmd> does not run through the server`); an `argv` holding `--project`, `--skill` or
  `--profile` in any form (400, `cli.run: argv holds <opt>: the server names the project from
  "project"`); an `env` name outside `FORWARDED_ENV` (400); an unknown project (404, `not found`).
  The server judges these itself; it never trusts the client's own checks.
- It runs the command as a child process of its own build: `[sys.executable, "-m", "chantier",
  "--skill", <plugin_files.skill_dir()>, *(["--project", <project folder>] when the project is in
  an external surface), *argv]`, cwd the served folder (`ctx.projects.served`: the surface's root,
  or the in-project repository), stdin the given text or empty, stdout and stderr captured as
  UTF-8, timeout 600 s (past it, the child is killed and the op answers 504, `cli.run: <cmd> ran
  past 600 s; stopped`). Its environment: the server's own, with every `FORWARDED_ENV` name
  removed, then the client's values set (a pure function `child_env(server_env, client_env)`), so
  a command never inherits the session id of the session that started the server.
- The answer: 200, `{"code", "stdout", "stderr", "version"}`, whatever the child's exit code;
  then `ctx.settle(project)` so the next read shows what the command wrote.
- The command writes the planning folder exactly as it would locally (its records, its
  `forge-journal.jsonl` lines with source `cli`, its git cleanup at a batch's end); the server
  adds no journal line and records nothing of its own for a `cli.run`.
- `docs/server-api.md`: one section for `cli.run` (its arguments, its answer, its refusals), in
  the style of the others.

### 6. `chantier live` and the profile

`commands/live.py`: with no `--url` and an active profile, `live` watches the profile's server
(its base and key) in place of the recorded one; `--profile local` gives today's behaviour.

### 7. AGENTS.md

- The "no setup" bullet: in the network exceptions add "a command run through a profile
  (`chantier login`), which reaches the profile's server"; in what chantier writes add "and the
  user's profiles (`chantier login`, `logout`) in one file outside any project,
  `chantier/profiles.json` in the user's config folder (`$XDG_CONFIG_HOME` or `~/.config` on
  Linux and macOS, `%APPDATA%` on Windows)".
- The CLI's scope bullet: "The surface server, `chantier board`" becomes "`chantier serve`"; after
  its third named exception (the configuration save) add: "a fourth, a client's command: for a
  client logged in with `chantier login`, the `cli.run` op runs one chantier command (any but
  `serve`, `webui`, `live`, `login`, `logout`, `watch`, `gate` and `lease ... hold`) as a child
  process of the server's own build, in its planning folder, with the client's arguments and its
  batch, host and session variables, and returns its output and exit code; that command edits the
  batch and the planning folder exactly as it does when run locally; built on the user's answers
  remote-cli-Q2 and Q5 (2026-11-22), with no measured cost". In the list of named tools add:
  "`webui`, `login` and `logout`: `webui` prints the web board's link and starts the server,
  detached, when none runs; `login` stores a server's address and key in a profile, after which
  every command but those named above runs on that server, and `logout` removes it; built on the
  user's answers remote-cli-Q1, Q3, Q4, Q7 and Q8 (2026-11-22), with no measured cost". The
  `live` paragraph: "it reads the server only (the recorded one, or the active profile's)".
- Every other `chantier board` of AGENTS.md (the forge hub's "started by ...", the dev-mode
  paragraph's "board server") stays a word for the process; only command names change.

### 8. The Chief of Staff's card

`chief-of-staff.md`'s routing table, one row: "run chantier from another machine", "log in to the
board" → `$CHANTIER webui` gives the link with its key (to the user only); on the other machine
`chantier login <link>`, after which every command there runs on this server; `--profile local`
or `chantier logout` to run locally again; the server must listen on the local network
(`board.host: network`, the row above). Reference: this section of AGENTS.md.

## Out of scope

- Moving the web UI to its own project (later, per the user).
- Docs beyond the mechanical rename and the `cli.run` section of `docs/server-api.md`: CR-447.
- Running, on the client's machine, what a command reads there: a CR's worktree (`take`'s path,
  `round`, `verdict`, `handback`'s checks), the transcripts (`cost`, `close`), the host's tools
  (`preflight`), `file @<path>` and CR folder paths: through a profile they are the server
  machine's (open question 2).
- A key or permission of its own for `cli.run`: the board's key grants it (open question 5).
- The printed `$CHANTIER`-style commands in a forwarded command's output name the server's
  launch form and paths; not rewritten.

## Evidence

Tests, few and parametrized, calling the CLI in-process (`just test` stays within its budget):

- `tests/conftest.py`: an autouse fixture points `XDG_CONFIG_HOME` and `APPDATA` (and `HOME`,
  `USERPROFILE` if `config_dir` reads them) at a temporary folder, so a developer's own profile
  never turns a test remote.
- New `tests/test_remote_cli.py`:
  - `config_dir` on the three cells: (`win32`, `APPDATA`), (`linux`, `XDG_CONFIG_HOME` set),
    (`darwin`, unset: `~/.config/chantier`).
  - login, the probe faked: the file is written with the profile as default, mode 0600 on POSIX;
    a second login `--profile work` becomes the default; `login` with no link lists both, no key
    printed; `logout` removes the default and leaves none; refusals parametrized: `--profile
    local` at login, a 401, no answer, a `--project` the server does not serve; a malformed file
    (exit 2).
  - forwarding, the HTTP call faked: `status --batch 3 --project projects/x --profile p` sends
    `argv == ["status", "--batch", "3"]`, `project == "x"`, `env` only `FORWARDED_ENV` names;
    stdout, stderr and the exit code come back as the server gave them; `--profile local` runs
    locally (no request); parametrized: `serve`, `webui`, `live`, `login`, `logout` never send;
    `watch`, `gate`, `lease <unit> hold` refused (exit 1, the sentence); `journal add --json -`
    sends the stdin; the four `error: remote:` refusals (exit 4), nothing written in the local
    planning folder.
  - the op, on the test world's server context: one real `cli.run` of `status` returns code 0 and
    the same lines as a local `status`; refusals parametrized (an argv with `--project`, `serve`,
    `lease X hold`, an env name outside the list: 400; an unknown project: 404); `child_env`
    drops the server's `CLAUDE_CODE_SESSION_ID` and sets the client's.
- `protocol.json`'s existing test passes with `cli.run`; the existing tests of the renamed lines
  (`test_board_running.py`, `test_writer_lines.py`, `test_watch_board.py`) read the shipped
  strings, not copies.
- A check that no card nor shipped doc (but `docs/release-notes/`) still says `$CHANTIER board` or
  `chantier board ` as a command: it reads the files from the repository at the head under test.

Scenario (`scenario/run_scenario.py`):

- `World.env` sets `XDG_CONFIG_HOME` and `APPDATA` to a folder under the world's root.
- Every `board` start becomes `serve`; the watcher still starts its server (`serve --seat ...
  --stop-idle`), seen by its command line.
- A new case `remote_cli` in the `surface-board` unit (its budget raised by the case's measured
  time), on a running server over the surface: `webui` prints `board already running at <link>`;
  `login <link>` writes the profile under the world's config folder; a remote `file "Remote idea"`
  lands in the server's inbox; a remote `note <cr> "from afar"` on a batch CR shows in its record;
  a remote `status` prints what `status --profile local` prints; `gate` under the profile is
  refused; `logout`; then, the server stopped and a profile set again, a remote `status` exits 4
  with the `error: remote:` line and writes nothing.
- `tests/test_scenario_coverage.py` (or what maps the cases) knows the new case.

Host and default matrix:

- No profile (the shipped default), Linux, macOS, Windows: every command local, as today: the
  whole existing suite and `just scenario` (`just check` on the three systems in CI; the
  scenario on ubuntu-latest in CI and on Windows at the top of the stack, `chantier gate`).
- A profile, Windows (`%APPDATA%\chantier\profiles.json`): the `config_dir` test and the local
  `just scenario` run at the top of the stack.
- A profile, Linux (`$XDG_CONFIG_HOME` or `~/.config`): the `config_dir` test and the CI
  scenario.
- A profile, macOS (`~/.config`, like `gh`): the `config_dir` test only; untested in a scenario.
- Host Claude Code: the forwarded `CLAUDE_CODE_SESSION_ID` and `CLAUDE_CODE_ENTRYPOINT`, in-process
  test and scenario; host Copilot: `COPILOT_AGENT_SESSION_ID` and `COPILOT_CLI`, in-process test
  only; untested from a real Copilot session.
- Two machines on a real local network (a login from another machine to `board.host: network`):
  untested; the scenario runs client and server on one machine over loopback.

## Open questions (for the user)

1. Under a profile, `watch`, `gate` and `lease ... hold` are refused (they run something on the
   caller's machine and keep local records), and `serve`, `webui`, `live`, `login`, `logout` run
   locally; every other command, `preflight` included, runs on the server. Is that the "toutes"
   you meant, or should `gate` run on the server's machine too?
2. Through a profile, a command reads the server machine's worktrees, transcripts, tools and
   paths: a remote Driver whose worktree is on its own machine gets `round`, `verdict` and
   `handback`'s worktree checks against the server's checkout, and `cost` reads the server's
   transcripts. Is that acceptable for this CR (agents on other machines plan and drive through
   the server; worktrees stay on the server's machine), with a later CR for client-side reads?
3. `chantier login` makes the profile it stores the default (the last login wins, like `gh`).
   Do you want a login that stores a profile without making it the default?
4. Anyone holding the board's link can now run every chantier command on the server's planning
   folder, over plain HTTP when it listens on the local network. Keep the one key, or a separate
   key or a switch (`board.remote_commands: yes`) for `cli.run`?
5. `chantier webui` starts the server with `--stop-idle` and no seat: it stops 30 minutes after
   its last client (the open page counts). Is that the lifetime you want?
