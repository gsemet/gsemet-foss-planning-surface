# `chantier live`: a live terminal view, second client of the API

## Goal

The user wants a Python terminal client that tracks a surface's activity live, in the spirit of
Vercel Board's swarm screen, as the proof that the server's published API (protocol 1,
`docs/server-api.md`) serves a client other than the web board. It watches only: it writes
nothing and messages no agent.

After this CR, `chantier live` in a terminal draws one screen that updates as things happen: a
header with the live counts, a left column of projects, batches and Drivers, a centre flow of
events, a right column of tasks with each Driver's lease time left. It talks to a running
`chantier board` over the WebSocket, and over HTTP with the long-poll when the WebSocket does not
open.

Paths below are relative to the repository root; `src/` stands for
`skills/chantier/scripts/cli/src/chantier/` and `tests/` for `skills/chantier/scripts/cli/tests/`.

## What changes

### 1. The dependency

- `pyproject.toml`: add `rich==<the latest stable release on PyPI the day of the change>` to
  `dependencies`, pinned with `==` like the others, and `"rich"` to
  `[tool.ruff.lint.flake8-tidy-imports] banned-module-level-imports` (it loads only when `live`
  runs, like `starlette`). `uv.lock` is refreshed with `uv lock`; `just lint`'s `uv lock --check`
  proves it. Rich ships one `py3-none-any` wheel, so `[tool.uv] no-build = true` holds on Linux,
  macOS and Windows. No Textual, no other new dependency: the WebSocket client is
  `websockets.sync.client.connect` (already a dependency, already used by
  `tests/test_server_api_ws.py`), the HTTP client is `urllib.request` (as `src/board/address.py`).

### 2. The server: three additions to the data, protocol 1 unchanged

All three only add fields, so the protocol stays 1 and `src/board/api/protocol.json` does not
change (it holds the frames and the arguments, not the `data`).

- **`lease` on each CR row** (`src/board/crs.py`, `_row`): `null` when the CR never had a lease,
  else `{"n", "renewed", "expires", "ended", "holds", "gate"}`: the record's `Lease` fields `n`,
  `renewed`, `expires`, `ended` (`src/core/records.py`), `holds` the number of running `lease hold`
  of this lease, and `gate` (`"gate running"`, `"gate queued"` or `null`), both as
  `src/core/leases.py` computes them (`hold_records(repo, unit, drop=False)` filtered on the
  lease's number, and `gate_keeping`). The read stays read-only: `drop=False`, no hold record is
  removed by a state read. The server sends facts, never the word `live` or `not confirmed`: a
  state is kept by its fingerprint and that word changes with the clock alone.
- **`stack_lease` on the batch** (`src/board/state.py`, `_batch`): the same object for the unit
  `stack` (`BatchRecord.stack_lease`), `null` when there is none.
- **The fingerprint** (`src/board/fingerprint.py`): the `.lease-hold.*.run` files at the planning
  folder's root count in it (name, size, time; a `stat`, no read), so a hold that starts or ends
  moves the `project` topic's `rev`. A lease taken, renewed or ended already moves it
  (`batch.json` is under `4-batch/`).
- **`text` on each line of an `events` event** (`src/board/api/topics.py`, `_events`): the
  sentence of the line's type, from `src/hub/schemas.py`'s `PUBLISHED[type].text`, when the type
  is published and its payload is accepted; no `text` field otherwise (an unknown type, a newer
  version, a refused payload). The journal file is not changed: the field is added to the answer
  only.
- `docs/server-api.md`: the `project.state` row and the `events` row say these fields; the
  "Versions" rule already covers them.

### 3. The client: `src/clients/tui/`

A package beside `clients/web/`, in three parts so each is tested alone. It imports nothing of
chantier but itself, `chantier.__version__` and `chantier.core.errors` (the error type and the
exit codes): everything it shows comes through the API.

- **`link.py`, the transport.** One class that, given the board's base address and key, yields
  the events of a list of subscriptions, and the server's `now`.
  - WebSocket: `ws(s)://<base>/api/v1/ws`, the key in the `X-Chantier-Board-Key` header, then
    `hello` with `protocol: 1` and `client: "chantier-live/<version>"`; one `sub` per
    subscription; it reads `event`, `tick`, `result` (a refused `sub`) and `error`.
  - HTTP: `POST <base>/api/v1/poll` with the key in the same header, the subscriptions as `subs`
    with the last `rev` of each, again as soon as it answers.
  - `auto` (the default): the WebSocket first; when it does not open or gives no `welcome`
    within 5 s, the HTTP binding, for this connection. A refused key (HTTP 401, the error `key`,
    close 4401) and a refused protocol (close 4426) are never retried on the other transport:
    they end the run with the server's sentence.
  - Loss: a WebSocket with no frame for 15 s (three `tick`s missed), a close, or a failed poll is
    a lost link. It is retried every 5 s, without end, starting again by the WebSocket in `auto`.
    At each new connection the `events` subscriptions carry `after: <the last seq seen>` once a
    line was seen, so no journal line is lost or shown twice; the `project` and `board` values
    are whole values and are just taken again.
  - A refused `sub` (404 for a project that left the board) drops that project from the screen;
    it does not end the run.
  - Addresses are built relative to the base, so a board behind a proxy with a path prefix works.
    The local board is called with no proxy (as `probe` does); a `--url` board with the
    environment's proxies, as `urllib` and `websockets` read them.
  - It sends `hello`, `sub`, `unsub` and the poll, and nothing else: no `call`, no op.
- **`model.py`, the screen's data**, a plain object fed with each event, with no Rich and no
  network in it:
  - from `board`: the projects (each line's `id`, `batch` (`id`, `state`, `mode`), `inbox`,
    `backlog`, `by_priority`), the server's `version` and `served`;
  - from `project`: the batch's `crs` rows (`cr`, `title`, `state`, `to_review`, `phase`,
    `round`, `round_limit`, `blocked`, `handed_back_at`, `lease`), `stack_lease`, `slots`, and the
    record's `events` (the last 40 of the batch, each with `t`, `actor`, `kind`, `cr` and what it
    has of `result`, `round`, `note`, `order_kind`, `reason`, `pr`);
  - from `events`: the journal lines (`seq`, `t`, `type`, `source`, `text`).
  - The flow keeps the last 200 lines of all the projects shown, by time. A record event is new
    when it comes after the last one already shown for that project (matched on the whole
    object); at the first `project` event the 40 recorded ones fill the flow, so the screen does
    not start empty. A journal line with no `text` shows its `type`.
  - "Now" is the server's: the `now` of the last frame received plus the time elapsed since on the
    local monotonic clock, so a machine with a wrong clock shows the right time left.
  - The time left of a lease, from its facts: ended (`ended` set): no lease shown; `expires`
    after now: `mm:ss`; else `gate` set: that word; else `holds` above 0: `held`; else
    `not confirmed <n> min` (the words of `src/core/leases.py`).
- **`screen.py`, the drawing**: one function from the model and a size to a Rich renderable
  (`rich.layout.Layout`, `rich.table.Table`, `rich.text.Text`), and the loop that redraws it once
  a second with `rich.live.Live` (`screen=True`), so the lease times count down between events.
  - **Header**: `chantier live`, the board's `served` and version, the transport (`ws` or `http`),
    the link's state (`live`, or `reconnecting since HH:MM:SS`), the server's time, and the four
    counts over the running batches of the projects shown: **working** (rows whose `state` is
    `working`), **ready** (rows with `to_review`), **held** (rows whose `state` is `blocked`),
    **done** (rows whose `state` is `merged`).
  - **Left column**: "Projects": one line per project (its id, its batch's id, state and mode, or
    `no batch`; inbox, backlog and `3-ready` counts as the `board` line gives them); "Agents": one
    line per unit held, `Driver <cr> <phase>` for each working CR, and `Stack driver` when
    `stack_lease` is not ended.
  - **Centre, "Flow"**: newest at the bottom, as many lines as fit: the time (`HH:MM:SS`, UTC,
    like every chantier text), the project, who (a record event's `actor`, a journal line's
    `source`), the text (a record event: its `kind`, its CR and what it has of result, round,
    order kind, reason or note; a journal line: its `text`).
  - **Right column, "Tasks"**: the working CRs (id, title cut to fit, phase, `round n/limit`, the
    lease's time left); then the CRs to review (id, title, the age since `handed_back_at`); then
    the blocked ones (id, the reason cut to fit).
  - Under 100 columns the left column is not drawn. Text only cut with `…`, never wrapped onto a
    second line. No colour carries a meaning alone (each state has its word); `NO_COLOR` is
    Rich's own to respect.
  - A footer line: `Ctrl-C to quit`, and `<n> more projects not watched: <ids>` when the board
    has more than the 15 watched.

### 4. The command: `chantier live`

- `src/declare/live.py` (registered in `src/cli.py`'s list, scope `NO_BATCH`) and
  `src/commands/live.py` (the handler, loaded when it runs). Help line: "watch a running board
  live in the terminal, read-only: counts, projects and Drivers, the flow of events, the tasks
  with their lease time left".
- Options:
  - `--url <link>`: the board of that link (`http(s)://host:port/[prefix/]?k=<key>`), the key
    from its `k`. A link with no `k` is refused (usage exit 1): `--url: the link holds no key
    (?k=...): give the link the board printed`.
  - with no `--url`: the board recorded as running for this surface or project
    (`src/hub/state.py`'s `live_entry(git_dir, SERVER)` for the address, the record's key), found
    from the current folder like `board` finds its own (`open_projects()`), called on the loopback
    address. With none recorded live: exit 4 (`EXIT_EXTERNAL`), `live: no board runs for this
    surface: start one with chantier board, or pass --url <link>`. `live` never starts a board,
    never writes `server.json`.
  - `--only <project>` (repeatable): watch these projects' ids only. An id the board does not
    serve is refused once the `board` value is known: `--only <id>: the board serves <ids>` (exit
    1). With none: every project of the board, the first 15 in the board's order.
  - `--transport auto|ws|http` (default `auto`).
  - `--once`: connect, wait for the first event of every subscription (10 s at most, else exit 4
    with what is missing), print the screen once as plain text (no control code, 120 columns
    unless the terminal says its width) and exit 0. It is the form a test, the scenario and a
    bug report read.
- Without `--once`, a stdout that is not a terminal is refused (exit 1): `live draws a screen: run
  it in a terminal, or pass --once for one printed screen`.
- Ctrl-C leaves the screen, restores the terminal and exits 0. A refused key or protocol exits 4
  with `live: <the server's sentence>`.
- It prints through its own console; it returns no lines to `cli.main` (as `board` does while it
  serves).

### 5. Project rules and docs

- `AGENTS.md`: in the "CLI's scope" bullet, one named exception beside `access` and `wait`:
  "`live`: a read-only terminal client of the surface server's published API, shipped in
  `clients/tui/`; it reads the server only (never the planning folder, the forge or git), writes
  nothing and messages no agent; built on the user's request of 2026-11-20, with no measured
  cost." In the "no setup" bullet's list nothing changes (it writes nowhere). The sentence
  "the web client's files ..., one client among others" stays true.
- `docs/server-api.md`: the new fields (above), and a short section "A terminal client" naming
  `chantier live` as the second client and `src/clients/tui/` as the example of a client in
  Python.
- `docs/boards.md`: a section "The live terminal view" (what it shows, how to start it, `--url`
  for a board on another machine, `--once`), with one capture of `--once` as a text block;
  `README.md`'s documentation list gains its line; `CONTRIBUTING.md`'s tree names `clients/tui/`.
- No card changes, no change to `agents/`, `hooks/` or `types/`: `just mod` is not owed.

## Decisions carried from `02-answers.md`

1. Rich alone, pinned in `pyproject.toml` and `uv.lock`; no Textual (section 1).
2. Shipped in the wheel as `clients/tui/`, started by `chantier live`; not `watch --tui`, not
   `top` (sections 3, 4).
3. `live` is a named exception in `AGENTS.md` (section 5).
4. The client's package uses the published API only; a test proves its imports (section 3,
   evidence).
5. The board is the one recorded as running, or `--url <link>`; `live` never starts one
   (section 4).
6. Topics: `board`, then `project` and `events` per project; not `costs`, `prs`, `journal`
   (section 3).
7. All projects by default, `--only`, 15 at most (section 4).
8. One board per run; several surfaces at once is split out (below).
9. WebSocket first, then HTTP with the long-poll; `--transport`; a refused key is not retried on
   the other transport (section 3).
10. A lost link is retried every 5 s, `events` resumed with `after` (section 3).
11. `lease` on a CR row and `stack_lease` on the batch, additions of protocol 1; the client
    computes the time left (sections 2, 3).
12. `text` on each `events` line (section 2).
13. The four counts: working, ready (`to_review`), held (`blocked`), done (`merged`) (section 3).
14. Tasks: working with the lease time, then to review with their age, then blocked (section 3).
15. Agents: one line per held unit, the stack driver's included; no agent id (section 3).
16. `--once`; a non-terminal stdout is refused without it (section 4).
17. Read-only: `hello`, `sub`, `unsub` and the poll only; quit is Ctrl-C (sections 3, 4).
18. No card changes (section 5).

The batch choice of 2026-11-20 (P1, the batch after batch-29) is the CR's place, not a behaviour.

## Out of scope

- Several boards or surfaces in one screen, and any key or mouse input (scroll back in the flow,
  filter by project or CR, open a CR): split out as the inbox item
  `live-several-boards-and-keys`.
- Textual, a theme, a configuration key in `chantier.yaml`.
- Costs, the PR table, the board's rescan journal (`costs`, `prs`, `journal` topics).
- Any write: no backlog move, no configuration save, no seat registered.
- The leases of QA orders (`O-k` units), and the agent's id or model in the Agents column: the
  state does not give them and this CR does not add them.
- A replay of the journal's history at start: the flow starts with the batch's 40 recorded events
  and the journal lines that arrive from then on.
- Starting or stopping a board from `live`.
- The cards, the Claude Code pane, the web client.

## Evidence

No host and default matrix: nothing here depends on the host (Claude Code or Copilot) or on a
configured value against a shipped default.

Tests, few and parametrized (`just test` has a time budget; one server for the whole new module):

- `tests/test_live_model.py` (no network, no server): fed with prepared `board`, `project` and
  `events` events, the model gives the four counts; the time left of a lease, parametrized on its
  facts (`expires` ahead: `mm:ss`; past with `gate`; past with `holds`; past with none:
  `not confirmed <n> min`; `ended`: none), with "now" from the server's `now`, not the machine's;
  the flow's new record events on a second `project` event (no line twice); a journal line with
  and without `text`. Then the drawing, on a recording console of fixed size: the header's
  counts, a working CR's line with its lease time, a CR to review with its age, a blocked one
  with its reason, a flow line; at 90 columns, no left column.
- `tests/test_live_link.py`: one real server on `127.0.0.1`, port 0, in a thread, over a prepared
  planning folder with a running batch holding a working CR with a live lease (the fixture style
  of `tests/test_server_api_ws.py`), parametrized on the transport (`ws`, `http`): `live --once`
  called in-process through `cli.main` prints the working CR and its lease time, and after one
  line appended to the journal a second read of the link gives it once. `auto` against a server
  whose WebSocket route refuses the upgrade ends on `http`. A wrong key exits 4 with the server's
  sentence on both transports and is not retried on the other. `--url` with no `k`, and a
  non-terminal stdout without `--once`, exit 1 with their line; no recorded board exits 4 with
  its line.
- `tests/test_live_link.py` also holds the import check: every module of `src/clients/tui/`,
  read from the repository as it ships at the head under test, imports from `chantier` only
  `chantier.clients.tui`, `chantier.__version__` and `chantier.core.errors`.
- The server's additions, in the existing modules: `tests/test_board.py` (or
  `tests/test_leases.py`): a row's `lease` for a CR never taken (`null`), taken (the record's
  fields, `holds` 0, `gate` `null`) and handed back (`ended` set); `stack_lease`; a hold record
  written at the planning folder's root moves the fingerprint and is still there after the state
  read. `tests/test_server_api.py`: an `events` line of a published type carries `text`, a line
  of an unknown type carries none; `protocol.json` is unchanged (`tests/test_server_protocol.py`
  already refuses a file that is not `just protocol-schema`'s output).
- Shipped files: `docs/server-api.md` is checked where a test already reads it; any new check on
  it or on `AGENTS.md` reads the file from the repository as it ships, at the head under test.

Scenario (`scenario/run_scenario.py`, unit `surface-board`, and its bullet in
`scenario/README.md`'s Coverage list, which `tests/test_scenario_coverage.py` checks): with the
real `board --seat` of that unit running over a batch with a working CR, `chantier live --once`
and `chantier live --once --transport http` each exit 0 and print the CR in Tasks and the header's
`working 1`; the planning folder's `git status` and `forge-journal.jsonl` are unchanged by both
runs (read-only); once the board has stopped, `chantier live --once` exits 4 with `no board runs
for this surface`.

Gates, as `AGENTS.md` asks for a change under the CLI's `src/`: `just check` and
`just eval-dry-run` in the worktree at the rebased head before the first push; the pipeline's
`just scenario (ubuntu-latest)` green at the PR's head; the batch's top CR also passes
`chantier gate` locally (Windows). `just protocol-schema` leaves `protocol.json` unchanged.

In the PR's Deliverables: the output of `chantier live --once` against a real board with a
running batch, at the pushed head (the same capture as `docs/boards.md`), and one line saying the
live screen was opened in a real terminal on the Driver's machine, with its system, or that it was
not (then named in Known gaps: "live screen not seen in a real terminal").

## Open questions

None: every point of the request was settled in `02-answers.md` on 2026-11-20, without the user,
on his word.
