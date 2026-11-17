# Change Specification: a progress board that works in remote

## Goal

In remote (Remote Control on a phone) the user has no view of the plan: the CR board pane
(`/chantier-board`, the Claude Code mod) does not show there, and the only way to know where a
batch stands is to ask "status?". The user wants "un genre de mini jira": a small read-only web
page, served by chantier, that the phone opens through the user's private network (Tailscale) and
that shows the batch, its CRs, the inbox and the backlog of the project's planning folder.

It is generic: it works in any project with no setup, in-project (`.agents/changes/`) or on an
external planning surface (`projects/<name>/changes/`), on any host that can run a background
command, with nothing about a given machine, network or project written in chantier.

## Summary of the decisions (from `02-answers.md`)

| # | Decision | Where it lands below |
| --- | --- | --- |
| 1 | The board is a small web server; the phone reaches it through the user's private network (Tailscale); it has no authentication, a risk the user accepts | Reach and risk |
| 2 | Read only: the board only shows; to act, the user talks to the Chief of Staff | The command, Out of scope |
| 3 | Listening on all interfaces (`0.0.0.0`) is allowed, on the user's word | Reach and risk |
| 4 | The Chief of Staff starts it in the background when its session starts; it stops when that session ends or the seat passes to a new Chief of Staff | Lifetime |
| 5, 6 | It ships as a CLI command, `chantier board`; the CR amends AGENTS.md's CLI-scope line to name it | AGENTS.md and the docs |
| 7 | The exception is bounded in that line: reads only, writes no file, standard library only, knows no role; anything more is another CR | AGENTS.md and the docs |
| 8 | Default address `127.0.0.1`; another address only when asked: an option of the command, or once for the project in `chantier.yaml` | Configuration |
| 9 | When the board listens beyond the local machine, the Chief of Staff says so once at start, with the address and "no password" | The Chief of Staff's card |
| 10 | A board that cannot start never blocks the session: one line says why; a board already running for this project is reused, not doubled | The command, Lifetime |
| 11 | It follows the planning folder wherever it is, and today's layout only (`4-batch`); the prototype's older folder names are dropped | What the board shows |
| 12 | Check the overlap with the backlog item `planning-server` (P3) | Overlap with `planning-server` |

## Overlap with `planning-server` (P3)

Checked against `.agents/changes/2-backlog/P3/planning-server/` (`01-intent.md`, `02-answers.md`,
`study/plan-storage-comparison.md`).

- **They do not serve the same pages, so they stay two CRs.** `planning-server` is a writer: a
  `chantier serve` owned by the Chief of Staff that applies the writes of every session, commits,
  rebases and pushes the external surface. Its HTTP/MCP "ticket tracking" was dropped by the user
  on 2026-11-10 ("Reads: the files are directly readable on the forge. Tracking over HTTP/MCP is
  no longer named"). The board writes nothing, syncs nothing and serves pages. No page of one is a
  page of the other.
- **What they share, and how this CR keeps it from doubling later:**
  - *Lifetime.* `planning-server`'s point 3 ("a chat session is not a daemon: who restarts the
    server") is the question this CR answers for a reader: a process started by the Chief of
    Staff, tied to the seat, reused when already running, stopping when the seat moves. When
    `planning-server` is specified, it takes this rule or replaces it for both (its point 7,
    leases), never a second rule beside it.
  - *Reach.* `planning-server`'s point 4 (localhost first, then a team with authentication) would
    apply to the board too. Authentication is out of scope here; if a later CR adds it, it adds it
    to the board's server.
  - *One HTTP server per planning folder.* If a later CR ever needs pages over the planning folder
    again (the tracking `planning-server` once named), it adds them to `chantier board`, not to a
    second server. This specification records that constraint; the Chief of Staff carries it into
    `planning-server`'s intent when that CR is next grilled.
- **Order:** independent. The board ships first; it needs nothing of `planning-server` and does
  not block it.

## What changes

### 1. The CLI: `chantier board` (new module `skills/chantier/scripts/cli/src/chantier/board.py`)

A new subcommand in `cli.py`, with no `--batch` (like `seat`), taking the global `--project`:

```
chantier [--project <folder>] board [--host <address>] [--port <n>] [--seat <session-id>]
```

- **What it serves**, over HTTP, `GET` (and `HEAD`) only; any other method answers 405:
  - `/`: the board page (below), which reloads itself every 30 seconds;
  - `/api/status`: the same data as JSON;
  - `/file?p=<path>`: a file or a folder of the planning folder, given relative to it: a folder
    as a list of links, a file as its text, escaped, in a `<pre>`. A path that resolves outside
    the planning folder (`..`, an absolute path, a symlink out) or that does not exist answers 404.
    Nothing outside the planning folder is ever served: not the project's code, not the surface's
    other projects.
  - anything else: 404.
- **Read only, absolutely.** The command writes no file and takes no lock, before, while and after
  serving: no `STATUS` rewrite, no `.gitignore` completion, no conversion of an old tree, no
  event. `Repo.find` today always completes the planning folder's `.gitignore` and may convert an
  old tree: the board finds its planning folder through `Repo.find` with both of those writes
  skipped (a new parameter of `Repo.find`, used by `board` only). It reads `batch.json`,
  `events.jsonl` and the CR folders without the batch's lock: they are written by atomic rename
  (and `read_events` already skips a half-written last line), and a read refused for an instant on
  Windows is retried as `state._retry` does.
- **Its data is computed in memory at each request, by the functions that write the STATUS
  files**, never by the functions that write them to disk: `status.dashboard_view(repo,
  lifecycle.stage_layout(repo))` for the index (batches, backlog with `3-ready` and the inbox,
  merged, trashed) and `status.batch_view` for the batch, plus the tail of the batch's
  `events.jsonl` (the last dozen events, `heartbeat` and `cost` left out). So the board always
  says what the next `STATUS.json` would say, works before any `STATUS.json` exists, and shows a
  backlog item's spec state (`specifying`, `specified`) as soon as the folder changes.
  `/api/status` returns that view (`schema` as in `status.SCHEMA`) plus three fields of its own:
  `planning_folder` (absolute path), `seat` (the session the board was started for, or null) and
  `board: true`, which the reuse check below reads.
- **Its start line.** On a successful start it prints, flushed at once (the command does not
  return while it serves, so the line is printed before serving, not at the command's end):
  `board on http://<address>:<port>/ over <planning folder>`, and, when the address is not a
  loopback address, a second line:
  `board: listens beyond this machine (<address>), no password`.
  For `0.0.0.0` (or `::`), `<address>` in the first line is the address given and the second line
  says "on every network of this machine".
- **Reuse, not double (answer 10).** Before binding, the command asks
  `http://<address or 127.0.0.1>:<port>/api/status`:
  - a chantier board over the same planning folder, started for the same seat (or both without
    one), answers: print `board already running at http://<address>:<port>/` and exit 0;
  - a chantier board over the same planning folder but started for another seat (a Chief of Staff
    that has left it) answers: wait for it to stop (it stops at its next seat check, below), at
    most twice that check's period, then bind;
  - anything else holds the port, or binding fails (the port taken, the address not on this
    machine, a permission refused): `error: board not started: <the reason, in one line>` on
    stderr, exit 4 (`EXIT_EXTERNAL`). Nothing is retried on another port: the port is the user's
    to choose (Configuration).
- **Stopping with the seat (answer 4).** With `--seat <session-id>`, the board reads the planning
  folder's `seat.json` (as `commands._read_seat` does, read only) at each request and at least
  every 30 seconds; when the seat no longer names that session (left, or taken over), it stops
  serving and exits 0. Without `--seat` (a user running it by hand), it serves until it is killed.
  It also exits 0 on Ctrl+C / termination, printing nothing more.
- **Standard library only** (`http.server.ThreadingHTTPServer`, `html`, `json`, `urllib.parse`,
  `socket`), portable to Linux, macOS and Windows, UTF-8 on the wire (`charset=utf-8`).
- **Hardening of a page with no password:** every response carries `Cache-Control: no-store`,
  `X-Content-Type-Options: nosniff` and a `Content-Security-Policy` that allows no script and only
  the page's own inline style; every text from the record or a file is HTML-escaped; a link is
  drawn only for an `http(s)` URL (a CR's PR) or a path inside the planning folder. The server
  logs no request line.

### 2. What the board shows (from the prototype, kept to today's layout)

`prototype/board.py` is the reference for the look: one column, phone first, light and dark
from the system, a card per section. What it shows, all from the view above:

- a header: the project's name (the repository's folder name, or the project's folder name in a
  surface) and "updated <time>, refreshes every 30 s", with a link to `/api/status`;
- **the batch** (`4-batch`), when there is one: its id, state, who steers (`steering_word`) and
  its shape (`shape_word`), the spend against the budget as a bar and figures (`unknown` when not
  priced, never `$0`), the slots taken and free, the heartbeat's age, the unread asks ("<n>
  question(s) waiting") and the pending orders; then one row per CR: its number and slug, the
  subject (the title without a leading byte-order mark, `#` and "Change Specification:"), the
  `label` exactly as `status` draws it (the same icon and words as `STATUS.md` and the CR board
  pane, never re-judged), the round, the cost (`-` when unknown), the PR or MR as a link (the word
  from `status.forge_word`), the blocked reason and what it waits for; the title links to its
  specification; then the recent events, folded;
- "No batch." when there is none;
- **3-ready, the backlog by priority (P1 to P4) and the inbox**: each item by its slug, linking
  to its folder, with its title and its spec state; the backlog sections folded;
- **the last merged and trashed CRs** (as the index lists them, with their totals), folded.

The prototype's older names (`3-requests`, `4-batches`, `01-request.md`) and its own title and
folder scanning are dropped: the board reads only what `status.py` reads today.

### 3. Configuration: `chantier.yaml` gains a `board` key (`playbook.py`)

```yaml
board:
  host: 0.0.0.0      # or the machine's Tailscale address; default 127.0.0.1
  port: 8765         # default 8765
```

- Both keys are optional; with no `board` key, or no `chantier.yaml`, the board listens on
  `127.0.0.1:8765` (answer 8). Nothing names a machine, a network or Tailscale in the code.
- `playbook.load` accepts `board` beside `roles` and validates it with its line numbers, as for
  `roles`: `host` one string with no whitespace; `port` an integer from 1 to 65535; any other key
  under `board` refused. The message for an unknown top-level key becomes "the top-level keys are
  `roles` and `board`". An invalid `board` makes `playbook` and the preflight's configuration
  check report it like an invalid role (exit 2), and makes `board` refuse to start with that line.
- The command's `--host` and `--port` win over the file, for that run only. The CLI reads the file;
  the Chief of Staff never reads or completes the values itself, it runs `$CHANTIER board`.
- `chantier.yaml` is edited only on the user's word (the rule of `chief-of-staff.md`, The
  project). The address is set once per project, per answer 8; then every Chief of Staff start
  follows it.
- In a surface, `chantier.yaml` is the project's, read where `read_playbook` reads it today
  (`repo.root`); two projects of one surface steered at the same time each set their own `port`.

### 4. Reach and risk (answers 1, 3, 8, 9)

- Default `127.0.0.1`: the board is then reachable only from the machine itself. That default
  holds because the Chief of Staff starts the board by itself in every project, and an open board
  on an office or public network would show the whole planning folder with no password.
- To reach it from a phone, the user sets `board.host` (or asks for it for one session): the
  machine's Tailscale address (reachable from the user's tailnet only), or `0.0.0.0` (every
  network the machine is on, the LAN included). Both are allowed, on the user's word.
- The board has no authentication. The risk is said by the board's second start line and, each
  session, by the Chief of Staff (section 5).

### 5. The Chief of Staff's card and the session start

`skills/chantier/references/session-start.md`, section 2:

- The row "`chief-of-staff` | none, or this session's own" becomes: `seat take`, rename, **start
  the board**, the introduction; no question. A Griller, a Foreman, a Driver and the router before
  a role is chosen never start the board.
- A paragraph "The board": right after `seat take` (and after every later `seat take` of this
  session, including a take-over and a hand-over received), the Chief of Staff runs
  `$CHANTIER board --seat <own session id>` (plus `--project` in a surface, as for every command)
  in the background, by its host's means (the host's reference, "Run the board"), and reads its
  first lines:
  - `board on ...` alone (a loopback address): nothing to say;
  - with `board: listens beyond this machine ...`: one line to the user, once in the session, in
    their language: the board's address (with the port) and that it has no password;
  - `board already running at ...`: nothing to say, or the same line as above if it listens
    beyond the machine and the user was not told yet in this session;
  - `error: board not started: ...`, or a host that cannot run a background command: one line
    with the reason, then go on. The board never blocks the session, a preflight, a batch or a
    report.
- A reload (section 5) starts nothing: the board survives a compaction; at the next skill
  invocation the Chief of Staff's `board` run is a reuse.

`skills/chantier/references/chief-of-staff.md`:

- The opening paragraph's "You start no Driver or background agent" gains: "the board, a
  background command of the CLI, is not an agent ([session-start](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/session-start.md))".
- "Handing the seat over": one line: the old Chief of Staff's board stops by itself when the seat
  moves; the new one starts its own at its `seat take`.
- Tips, "After a status" examples: in remote, when the board listens on `127.0.0.1` only, the
  user may say "board on my phone" to have `board.host` set in `chantier.yaml` (on their word).
- Entry points table: a row "board on my phone", "where is the board?": the board's address, and
  on the user's word `board.host` in `chantier.yaml`, then the board started again (stop the
  running one by the host's means, then `$CHANTIER board --seat <id>`).

The cards name no host tool (the structure test `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool`
holds).

### 6. The host references

`skills/chantier/references/hosts/claude-code.md`, Tools table, new rows, each **unproved** with
its trial:

- "Run the board": `Bash` with `run_in_background: true` and the command `$CHANTIER board --seat
  <id>`; its first lines read from the background task's output; stopped with the host's stop of a
  background shell. Trial: a Chief of Staff starts it, `/api/status` answers from the machine, the
  output shows the start line.
- "The board when the session ends": whether the host ends a background command when the
  session ends (closed, or stopped). Trial: start the board, end the session, ask
  `/api/status`. Until proved, the board stops when the seat moves (CLI), which does not depend
  on it.

"Surfaces and options" table, a row "The remote board (`chantier board`)": Desktop typed yes;
Remote Control yes, when `board.host` is an address the phone reaches (Tailscale or the LAN);
Terminal yes; unproved; trial: open the board from the phone over Tailscale during a batch.

`skills/chantier/references/hosts/copilot.md`, Tools table: the same two rows with the host's
background shell; unproved, same trials. If the host has no background command, the row says so
and the Chief of Staff gives the one line of section 5 (no workaround).

### 7. AGENTS.md and the docs (answers 5, 6, 7)

- `AGENTS.md`, the CLI-scope line becomes:

  > The CLI's scope: the CR lifecycle, the batch's frame (limits, record, STATUS files), the
  > means to synchronise, and a few tools. The agents do the work, git and the forge included; a
  > new CLI tool comes from measured token-costly behaviour, never from speculation. One named
  > exception: `chantier board`, a read-only web view of the record the CLI already keeps, for the
  > user in remote: it writes no file, uses the standard library only and knows no role; anything
  > more (answering an ask, filing an item) is another CR.

- `CONTRIBUTING.md`, part 2 (the CLI): name `board` among the tools, with the same bound in one
  sentence; part 4 (the mod): one sentence that the CR board pane and `chantier board` show the
  same view (`schema` 3), and change with `status.py`.
- `README.md`: a section "The remote board" after "The CR board (Claude Code)": what it shows,
  that the Chief of Staff starts it, the default `127.0.0.1:8765`, the `board:` keys of
  `chantier.yaml`, Tailscale or the LAN to reach it from a phone, read only, no password; and the
  `chantier.yaml` reference where `roles` is described gains `board`.
- The docstrings that list the CLI's scope (`commands.py` module docstring,
  `src/chantier/__init__.py`) name the board.
- The docs' SVG diagrams are not changed by this CR.

## Out of scope

- Any write from the board: answering an ask, filing or triaging an item, an order (answer 7:
  another CR).
- Authentication, TLS, or a public exposure (a tunnel, a forge page): the reach is the user's
  private network (answer 1).
- A board for the whole surface (all its projects on one page): one board per planning folder,
  started by that project's Chief of Staff (see the open question).
- Turning the board off for a project, or a port picked automatically.
- Rendering Markdown as HTML: files are shown as text.
- Any change to the CR board pane (`hooks/register.tsx`), its contract (`types/index.d.ts`) or to
  `STATUS.json`'s schema.
- The prototype file itself is not shipped; it stays in the CR's `prototype/` folder.
- `planning-server`'s writer, sync and leases.

## Evidence

### `just check`

- Passes on Linux, macOS and Windows. The structure tests stay few: no new test unless a structure
  test enumerates what changes (the cards' links, both hosts' references); the behaviour is proved
  by the scenario.

### `just scenario` (both forges), a new step `remote_board(w)` in `scenario/run_scenario.py`

Run against a repository with a running batch (CRs queued, working, blocked, one with a PR), items
in the inbox, the backlog and `3-ready`, and the seat taken by `s-1`; a free port found by the
scenario.

1. `chantier board --host 127.0.0.1 --port <p> --seat s-1` started as a background process: its
   first line is `board on http://127.0.0.1:<p>/ over <planning folder>` and no second line.
2. `GET /` answers 200, `text/html; charset=utf-8`: it holds each active CR's number and its
   `label` exactly as in `4-batch/STATUS.json` after `status --refresh`, the inbox, backlog and
   `3-ready` slugs, and no raw `<` from a CR title (a title with `<b>` in it is escaped).
3. `GET /api/status` answers JSON whose `batches`, `backlog`, `merged` and `trashed` equal those of
   the index `STATUS.json` written by `status --refresh` (the `updated` time aside), plus
   `planning_folder`, `seat: "s-1"` and `board: true`.
4. `GET /file?p=<a CR's 03-change-spec.md>` answers 200 with its text; `/file?p=../AGENTS.md`,
   an absolute path and a missing path answer 404; `POST /` answers 405.
5. Nothing was written: the planning folder's files, their sizes and their modification times are
   the same before step 1 and after step 7, and `git status --porcelain` of the planning folder is
   unchanged.
6. A second `board` with the same host, port and seat prints `board already running at ...` and
   exits 0 at once. A `board` on a port held by a plain socket of the scenario exits 4 with one
   `error: board not started: ...` line.
7. `seat take s-2 --over s-1`, then one `GET /`: the first board exits 0 within a few seconds.
   A `board --seat s-2` on the same port then starts.
8. `--host 0.0.0.0` prints the second line, `board: listens beyond this machine ...`.
9. `chantier.yaml` with a `board` block (`host: 127.0.0.1`, `port: <q>`, one key per line): `board` with no option
   listens on `<q>`. A `port: abc` and an unknown key under `board` are reported by `playbook` with
   their line (exit 2), and `board` refuses to start with the same line.
10. In the external-surface step (`external_surface`): `board --project <name>` serves that
    project's `changes/`, and `/file` cannot reach the surface's other project nor the clone.

### By hand, before the PR (the Driver says it in the PR, it is not a gate)

- The board opened from a phone over Tailscale with `board.host` set, during a batch; the two
  host-reference rows stay unproved until the user runs their trials.

## Open questions

None. The one raised is settled in `02-answers.md`: one board per project, started by that
project's Chief of Staff, on its own port.
