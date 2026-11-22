# Remote CLI commands through the surface server: `login`, profiles, `cli.run`

Change Specification, written 2026-11-22 from `intake/request.md` and `02-answers.md`
(remote-cli-Q1 to Q14, the user's answers of 2026-11-22, and the Chief of Staff's decisions of the
same day; the user said "grilled enough"). Rewritten 2026-11-22 after Q11 split the work in three
stacked CRs in batch-30: A `rename-the-surface-server-command-to-ser` (`serve`, `webui`), B
`two-board-keys-a-public-read-only-key-an` (the private and read-only keys, the
`X-Chantier-Access` header), and this CR, C, on top of B, before CR-447 docs-gardening (which
documents all three). No issue. One Driver, at most 5 rounds. It touches the CLI's `src/`, the
cards, the eval kit and the scenario: `just check` and `just eval-dry-run` before the first push,
`just scenario (ubuntu-latest)` green before the PR. No change under `hooks/` or `types/`, none to
the web client's files.

## Goal

In the user's words: other agents act from the command line, remotely, through the surface server
("take, ..."). Once a machine is logged in to a server (`chantier login <link>`, like `gh auth
login`), every chantier command run there goes to that server, which runs it in its planning
folder, on its own machine, and gives back the output and the exit code. On the server's machine,
with no login, everything stays local, as today; and the server itself never forwards.

## Decisions carried (02-answers.md)

1. Q2, Q5: every CLI command runs remotely, batch commands included (`order`, `open`, `cancel`);
   AGENTS.md's "never edits a batch" gets a named exception.
2. Q4, Q7: a login like `gh auth login`; profiles, one the default; with an active default every
   command goes to the server; `--profile local` or `chantier logout` runs it locally again.
3. Q8: one file in the user's config folder, a named exception to "writes only in the planning
   folder".
4. Q9 (and B): `cli.run` needs the private key; a read-only profile serves `live` only.
5. Q10: a forwarded command reads the server's machine (worktrees, transcripts, tools, paths).
6. Q12: the server sends its launch form; the client puts its own in the printed lines.
7. Q13: `file @<path>` is kept; through a profile it reads the server's file.
8. The Chief of Staff: `gate` and `lease … hold` are refused under a profile, `preflight` runs on
   the server; `login` makes the new profile the default, `--no-default` stores it without; a
   `cli.run` counts as a client for the idle stop's 30 minutes. (The earlier refusal of `watch`
   under a profile is replaced by fix (1) of the critic's round: `watch` never reads the profiles
   and always runs locally, see section 3.)

## What changes

### 1. Profiles (new `clients/profiles.py`: the profiles file and nothing else)

- Folder: on Windows `%APPDATA%\chantier\`; elsewhere `$XDG_CONFIG_HOME/chantier/` when set, else
  `~/.config/chantier/`. One function `config_dir(platform, environ)` decides.
- File `profiles.json`, UTF-8, written atomically (a temporary file in the folder, then
  `os.replace`), mode 0600 on POSIX (it holds keys); the folder is made at the first login:
  `{"default": "<name>" | null, "profiles": {"<name>": {"url": "<base>", "key": "<key>",
  "access": "write" | "read", "project": "<id>" | null, "served": "<folder>", "version": "<v>",
  "saved": "<UTC stamp>"}}}`. `url` is the base `commands/live.from_link` returns. A file that
  does not parse: `error: profiles: <path>: <reason>: fix or delete it`, exit 2, for every command
  that reads it (no silent local run).
- The active profile: `--profile <name>` when given (`local`: none), else the file's `default`,
  else none. `--profile` is a root option (`cli.py`'s `_parser`) and, like `--project`, accepted
  after the command (`commands/registry.add_command`). Unknown name: `error: --profile <name>: no
  such profile (<names>, or local)`, exit 1.
- **Who reads the file**: only `cli.main` for a command that may forward, `login`, `logout` and
  `live` (for its link). `serve`, `webui`, `watch` and the child a `cli.run` starts never read it:
  a default profile on the server's machine, or a broken file there, changes nothing for them.

### 2. `chantier login` and `chantier logout` (new `declare/remote.py`, `commands/login.py`, NO_BATCH)

- `login <link> [--profile NAME] [--project ID] [--no-default]`: either link of the server's (B);
  parsed with `commands/live.from_link` (same refusals); probes `POST <base>api/v1/call/board.get`
  with the key in `X-Chantier-Board-Key`, 10 s; reads the key's access from `X-Chantier-Access`.
  On success it stores the profile (`NAME`, default `default`; `local` refused, exit 1) and makes
  it the default, unless `--no-default` (the default stays as it was; with none, none is set).
  - No `X-Chantier-Access`: `error: login: the server at <base> runs an older chantier (<v>):
    stop it and start it again (chantier serve) from this version`, exit 4.
  - `--project` must be one of the projects `board.get` lists (else `error: login: --project
    <id>: the server serves <ids>`, exit 1); omitted, none is stored (the server's home project).
  - 401: `error: login: the server refused the key: give the link it printed (chantier webui
    prints it)`, exit 4; no answer: `error: login: no chantier server answers at <base>:
    <reason>`, exit 4. Nothing stored.
  - Output, the key never printed: `logged in: profile <name> → <base> (chantier <v> over
    <served>), private|read-only, the default|not the default`, then, private default: `every
    chantier command now runs on that server; --profile local runs one here, chantier logout ends
    it`; read-only: `read-only: live uses it; every other command needs the private link`;
    `--no-default`: `--profile <name> runs a command there`.
- `login` with no link: one line per profile, `<name> → <base> (private|read-only, project <id> |
  the server's home project)`, the default marked `(default)`, or `no profile: commands run
  here`; no network, no write.
- `logout [--profile NAME]`: removes the named profile, or the default; when it was the default,
  none remains. `logged out: profile <name>; commands run here again` (or `...; the default stays
  <name>`). No such profile: `logout: no profile <name>`, exit 0. No network.

### 3. The client (`cli.py`, new `clients/remote.py`)

`cli.main` parses the arguments as today (`--help` and usage errors stay local). Then:

- **Never forwarded, the profiles never read**: `serve`, `webui`, `watch` (local whatever the
  profile: a watcher watches this machine's sessions). **Never forwarded, read the profiles for
  their own use**: `login`, `logout`, `live` (section 5). **Refused under an active profile**:
  `gate` and `lease <unit> hold` (they run work on this machine and write its records): `error:
  <cmd> runs on the server's machine, not through a profile: run it there, or here with --profile
  local`, exit 1. **Forwarded**: every other command (`open`, `order`, `cancel`, `take`, `round`,
  `handback`, `close`, `preflight`, `file`, `summary`, `journal add` ...). Under a read-only
  profile a forwarded command is refused before any request: `error: remote: profile <name> holds
  the read-only key: commands need the private link (chantier login <private link>)`, exit 1.
- **The request**: `POST <base>api/v1/call/cli.run`, the key in the header, the HTTP means and
  proxy rule of `clients/tui/link.py`, a client timeout of 630 s, the body:
  - `argv`: the command line with `--profile`, `--project` and `--skill` removed, in their `--opt
    value` and `--opt=value` forms and their argparse prefixes (`--proj`, `--pro=...`, `--sk` ...:
    any token that argparse would take for one of them, judged with `cli.py`'s parser), before or
    after the command;
  - `project`: the `--project` given, as its last path component (`projects/chantier`, an
    absolute folder and `chantier` all give `chantier`), else the profile's, else null;
  - `env`: only the `FORWARDED_ENV` names set in this process (`CHANTIER_BATCH`, `CHANTIER_HOST`,
    `CLAUDE_CODE_SESSION_ID`, `CLAUDE_CODE_ENTRYPOINT`, `COPILOT_AGENT_SESSION_ID`, `COPILOT_CLI`,
    `AI_AGENT`); one constant, shared with the server;
  - `stdin`: only for `journal add --json -`, the client's stdin decoded `utf-8-sig`; else null.
- **The answer**: a 200 carries `{"code", "stdout", "stderr", "version", "launch"}`. `launch` is
  the server's launch form (`plugin_files.cli_command` on the server, with its `--project` when
  the project is in an external surface). The client replaces each occurrence of that exact text
  in `stdout` and `stderr` with its own form (its own `cli_command`, plus `--profile <name>` when
  one was named, plus the `--project` it was given), so a Driver block's `cli:` line or a
  `watch:` line printed through a profile works on the client (Q12); it then writes them as they
  are and exits with `code`. Paths in the output stay the server machine's (Q10).
- **Refusals**, one `error: remote: ...` line on stderr, exit 4, nothing run locally:
  - no answer: `profile <name>: no chantier server answers at <base>: <reason>; run it here with
    --profile local, or chantier logout`;
  - 401: `the server at <base> refused the key of profile <name>: log in again with the link it
    prints (chantier webui)`;
  - 403: `the server at <base> takes profile <name>'s key as read-only: log in with the private
    link`;
  - 404 `unknown op`: `the server at <base> runs an older chantier with no remote commands: stop it
    and start it again (chantier serve) from this version`;
  - 404 project, 400, 504: `<the server's error>`.

### 4. The server: the `cli.run` op (new `board/cli_run.py`)

- `board/api/protocol.py`: `CliRunArgs` (`argv: list[str]`, at least one item; `project: str |
  None`; `env: dict[str, str] = {}`; `stdin: str | None`), in `OP_ARGS` as `"cli.run"`;
  `protocol.json` rewritten with its `just` recipe; `HANDLERS` gains it. Not in B's `READ_OPS`:
  private key only, with nothing to add.
- Its checks, the server's own (it never trusts the client's), each a 400 with nothing run:
  - `argv` parsed with the CLI's real parser (`cli._parser`, no `exit`): an argparse error answers
    400 with its message; a command of `serve`, `webui`, `watch`, `live`, `login`, `logout`,
    `gate`: `cli.run: <cmd> does not run through the server`; `lease`'s argv judged by `lease`'s
    own subparser, `hold` refused the same way;
  - a token that is `--project`, `--profile` or `--skill`, or an argparse prefix of one, in either
    form: `cli.run: argv holds <opt>: the server names the project from "project"`;
  - an `env` name outside `FORWARDED_ENV`;
  - a NUL character in `argv`, `env`, `project` or `stdin`.
  An unknown project: 404, `not found`.
- The child: `[sys.executable, "-m", "chantier", "--profile", "local", "--skill",
  <plugin_files.skill_dir()>, *(["--project", <folder>] for a project of an external surface),
  *argv]`, cwd the served folder, stdin the given text or empty, stdout and stderr captured as
  UTF-8, timeout 600 s (then killed, 504, `cli.run: <cmd> ran past 600 s; stopped`). Its
  environment: `child_env(server_env, client_env)` drops every `FORWARDED_ENV` name of the
  server's, then sets the client's, so a command never speaks for the session that started the
  server. `--profile local` and the child's never reading the file (section 1) make a loop
  impossible even with a default profile on the server's machine.
- The answer: 200, `{"code", "stdout", "stderr", "version", "launch"}` whatever the child's code;
  then `ctx.settle(project)`. The command writes the planning folder as it does locally (its
  records, its journal lines with source `cli`, its git cleanup at a batch's end); the server adds
  nothing of its own.
- The idle stop (`board/idle.py`): a running `cli.run` counts as an observer, and the 30 minutes
  count from the end of the last one, so a server `webui` or a watcher started with
  `--stop-idle` serving remote commands only does not stop under them.
- `docs/server-api.md`: one section for `cli.run` (arguments, answer, refusals), in the others'
  style.

### 5. `chantier live` and the profile

`commands/live.py`: with no `--url` and an active profile (private or read-only), `live` watches
the profile's server in place of the recorded one; `--profile local` gives today's behaviour.
`live` uses the profile for its link only and sends no write.

### 6. AGENTS.md: four sentences

1. The "no setup" bullet's network exceptions: after "the forge calls of `ship`, `take`, `round`,
   `handoff` and `forge-stack`, made with the user's own `gh` or `glab` (below)" add "and a command
   run through a profile (`chantier login`), which reaches the profile's server".
2. Its list of what chantier writes: after "the surface server keeps its two keys" (B's wording)
   add "and the user's profiles (`chantier login`, `logout`), in one file outside any project,
   `chantier/profiles.json` in the user's config folder (`$XDG_CONFIG_HOME` or `~/.config` on
   Linux and macOS, `%APPDATA%` on Windows), mode 0600".
3. The CLI's scope bullet, after the surface server's last named exception at the head (the third,
   the configuration save, or CR-449's fourth, the Griller, when merged: the Driver counts at its
   head and writes "a fourth" or "a fifth"): "a fourth, a client's command: for a client logged in
   with `chantier login`, the `cli.run` op runs one chantier command (any but `serve`, `webui`,
   `watch`, `live`, `login`, `logout`, `gate` and `lease … hold`) as a child process of the
   server's own build, never forwarded again, in its planning folder on the server's machine (its
   worktrees, transcripts and paths), with the client's arguments and its batch, host and session
   variables, behind the private key, and returns its output, its exit code and its launch form;
   that command edits the batch and the planning folder exactly as when run locally; built on the
   user's answers remote-cli-Q2, Q5, Q10 and Q12 (2026-11-22), with no measured cost".
4. The named tools: "`login` and `logout`: `login` stores a server's address and key in a profile
   of the user's config folder, after which every command but `serve`, `webui`, `watch`, `live`,
   `login` and `logout` runs on that server (`gate` and `lease … hold` are refused there), and
   `logout` removes it; built on the user's answers remote-cli-Q4, Q7 and Q8 (2026-11-22), with no
   measured cost"; and in the `live` paragraph "it reads the server only" becomes "it reads the
   server only (the recorded one, or the active profile's)".

### 7. The Chief of Staff's card

`chief-of-staff.md`'s routing table, one row: "run chantier from another machine", "log in to the
board" → `$CHANTIER webui` gives the links (the private one to the user only); on the other
machine `chantier login <private link>`, after which every command there runs on this server;
the read-only link shows the board and acts on nothing; `--profile local` or `chantier logout`
runs locally again; the server must listen on the local network (`board.host: network`).

### 8. The eval kit

`evals/kit/dry_run.dry_environment` sets `XDG_CONFIG_HOME` and `APPDATA` to its temporary folder
(restored at the end, like the rest), so the maintainer's own profile never turns a dry run
remote. A real eval under a profile is untested (named in the PR's Known gaps).

## Overlaps in batch-30

- CR-446 (live-several-boards-and-keys) edits `commands/live.py` (`--url` repeatable, up to four
  boards); section 5 touches the same function. Whichever lands second rebases: with CR-446 in,
  the profile's server is the one board `live` watches when no `--url` is given.
- CR-449 (board-griller): the numbering of section 6's sentence 3; its `griller.*` ops are not
  run by `cli.run` (they are ops, not commands).

## Out of scope

- The web UI's move to its own project; docs beyond the `cli.run` section (CR-447).
- Reads on the client's machine (worktrees, transcripts, `file @<path>`, tools): later (Q10).
- Paths other than the launch form in a forwarded command's output: the server's, unchanged.

## Evidence

Tests, few and parametrized, in-process:

- `tests/conftest.py`: an autouse fixture points `XDG_CONFIG_HOME` and `APPDATA` at a temporary
  folder.
- New `tests/test_remote_cli.py`:
  - `config_dir` on three cells: (`win32`, `APPDATA`), (`linux`, `XDG_CONFIG_HOME`), (`darwin`,
    unset).
  - login, the probe faked: default set, mode 0600 on POSIX; a second `--profile work` becomes the
    default; `--no-default` leaves it; a read link stores `access: read`; no `X-Chantier-Access`
    refused; the list prints no key; `logout` of the default leaves none; refusals parametrized
    (`--profile local`, 401, no answer, a project not served, a malformed file: exit 2).
  - forwarding, the HTTP call faked: `status --batch 3 --project projects/x --profile p` sends
    `argv == ["status", "--batch", "3"]`, `project == "x"`, only `FORWARDED_ENV`; `--proj=x` and
    `--prof p` are removed too; the answer's `launch` text is replaced by the client's form in
    stdout and stderr; code and streams come back; `--profile local` sends nothing; `serve`,
    `webui`, `watch`, `live`, `login`, `logout` send nothing; `gate` and `lease U hold` exit 1;
    `journal add --json -` sends stdin; a read-only profile sends nothing (exit 1) while `live`
    uses it; the five remote refusals exit 4 and write nothing locally.
  - no loop: with a default profile (and, in a second cell, a malformed file) in the server
    machine's config folder, one real `cli.run` of `status` on the test world's server context
    returns code 0 and the lines of a local `status`, no request made by the child; `serve`'s and
    `watch`'s start read no profile.
  - the op's refusals parametrized: an argparse error, `serve`, `watch`, `lease X hold`, `--proj`,
    `--sk=y`, an env name outside the list, a NUL in `argv` and in `stdin`: 400; an unknown
    project: 404; under the read key: 403 (B's test covers it by iterating `OP_ARGS`);
    `child_env` drops the server's `CLAUDE_CODE_SESSION_ID` and sets the client's.
  - the idle stop: a `cli.run` running at the 30-minute mark keeps the server; the count restarts
    at its end (the clock faked).
- `protocol.json`'s test passes with `cli.run`.
- `just eval-dry-run` passes with the kit's isolation.

Scenario (`scenario/run_scenario.py`): `World.env` sets `XDG_CONFIG_HOME` and `APPDATA` under the
world's root. A new case `remote_cli` in the `surface-board` unit (its budget raised by the case's
measured time), on the running server: `login <private link>` writes the profile; a remote `file
"Remote idea"` lands in the server's inbox; a remote `note <cr> "from afar"` shows in the record;
a remote `status` prints what `status --profile local` prints; `gate` is refused; `watch --once`
(or its shortest form) runs locally with the profile set; `login <read link> --profile ro
--no-default` then `note --profile ro ...` is refused with nothing written; `logout`; the server
stopped and a profile set again, a remote `status` exits 4 with its `error: remote:` line.
`tests/test_scenario_coverage.py` (or what maps the cases) knows the new case.

Host and default matrix:

| Cell | Host | Profile | Expected |
| --- | --- | --- | --- |
| 1 | any | none | every command local, as today |
| 2 | Windows client | private default | profile in `%APPDATA%\chantier`; commands forwarded |
| 3 | Linux or macOS client | private default | profile in `$XDG_CONFIG_HOME` or `~/.config`; forwarded |
| 4 | server machine | a default profile present | `serve`, `watch`, `webui`, the child: local, no loop |
| 5 | any | read-only | `live` uses it; every forwarded command refused, exit 1 |

## Open questions

None.
