# Two board keys: a public read-only key and a private key

Change Specification, written 2026-11-22 from `intake/request.md` and `02-answers.md` (copied from
the parent CR `remote-cli-commands-through-the-surface-`: remote-cli-Q9 and its correction, Q11,
the Chief of Staff's decision; the user said "grilled enough"). No issue. Part B of three stacked
CRs in batch-30, on top of A (`rename-the-surface-server-command-to-ser`: it uses `serve` and
`webui`), under C (`remote-cli-commands-through-the-surface-`, which reads this CR's access
header), before CR-447. One Driver, at most 4 rounds. CLI `src/`, cards, scenario: `just check`,
`just eval-dry-run`, `just scenario (ubuntu-latest)` before the PR. No change under `hooks/` or
`types/`, none to the web client's files.

## Goal

The user (Q9): "une clé publique en lecture seule et une privée qui peut agir". The surface server
gets a public read-only key, which can be shared: it shows the board (the page, `live`, the
subscriptions) and acts on nothing; and a private key, today's, which reads and acts: every write
of the backlog, the configuration, and every op that is not a read (C's `cli.run`, CR-449's
Griller included). Nobody holding today's link loses anything.

## Decisions carried (02-answers.md)

1. Q9: two keys; the read key opens the reads and subscriptions; the private key every write;
   `webui` prints both links, the private one for the user only.
2. The correction: `project.file` reads (read key); `backlog.file` writes (private key).
3. The Chief of Staff: the read key opens an allow-list of read ops only; every other op, present
   or future (CR-449's `griller.send` and `griller.stop` included), needs the private key.
4. Q11: part B, between A and C.

## What changes

### 1. The keys in `chantier/server.json`

- `key` stays and is the **private key**, unchanged: every link, cookie (30 days), watcher, script
  and `live --url` made before this CR keeps full rights, with no step from the user.
- A new field `read_key` is the **public read-only key** (`secrets.token_urlsafe(32)`), made by
  `board/key.load_or_create` at a server's start when it is missing (a new
  `hub/state.set_read_key`, under the same lock as `set_key`; `reassert_server` and `migrate`
  keep it). `--new-key` replaces both (its help says so). An older build's server ignores
  `read_key`; the watcher, `probe`, `live`'s recorded server and `webui` keep reading `key`.
- `board/key.KeyFile` gives both: `current()` the private key, a new `read_current()`; both read
  again when the file changes.

### 2. The access of a request

- `board/api/auth.source_of`, `upgrade`, `guard.exchange`, `guard.authorised` and the
  WebSocket's `hello` (`board/api/ws.py`) accept either key, in the header, the cookie (the
  exchange sets the cookie to the key the link held) or `hello`, and say which: `write` for the
  private key, `read` for the public one. A WebSocket keeps its connection's access.
- Every `/api/v1/` answer carries `X-Chantier-Access: read|write`; `auth.CORS` gains
  `Access-Control-Expose-Headers: X-Chantier-Access` (so a page served elsewhere reads it); the
  `welcome` frame gains `access: "read" | "write"` (`protocol.py`'s `Welcome`; `protocol.json`
  rewritten with its `just` recipe).
- The allow-list, one constant in `board/api/ops.py`: `READ_OPS = {"board.get", "project.state",
  "project.tree", "project.file", "costs.get", "prs.get", "dashboard.get", "journal.get",
  "config.get"}`, and in `board/api/topics.py` `READ_TOPICS` = today's six topics (`board`,
  `project`, `costs`, `prs`, `journal`, `events`). Under the read key, any op not in `READ_OPS`
  (today the `backlog.*` ops, `config.put`, `journal.rescan`, `costs.recompute`, `writer.sync`,
  `seats.register`; tomorrow C's `cli.run`, CR-449's `griller.*` and any op added later, with no
  change here) and any topic not in `READ_TOPICS` answers 403, `refused: the read-only key acts on
  nothing: use the private link`, over HTTP and as the WebSocket's `result` or `error`, and runs
  nothing. The HTTP file route (`GET /api/v1/projects/<id>/file`) and the static page take either
  key. The legacy routes `routes.py` still serves, if any write, follow the same rule (a write
  needs the private key).
- `docs/server-api.md`'s section on the key (the protocol's section 7): the two keys, the header,
  the exposed header, `welcome.access`, the allow-list and the 403.

### 3. The links

- `board/address.url` builds either link. `serve`'s start lines (`board on <link> over <folder>`,
  `board already running at <link>`, `on this machine: <link>`) keep the private link, for the
  user only, and gain one line after the link lines: `read-only: <read link> (it shows the board
  and acts on nothing; it can be shared)`, in its loopback form too when it differs (`on this
  machine, read-only: <link>`). `webui` prints the same lines (A's `_running_lines` and start
  lines carry it). The network line (`BEYOND`) says "the private link acts: give it to the user
  only, plain HTTP".
- `chantier live --url` takes either link (it only reads).

### 4. AGENTS.md

- The surface server's sentence "behind a key (in its URL for the web client, in a header or a
  WebSocket's first message for any other client)" becomes "behind two keys, a private one that
  reads and acts and a public one that reads only (either in its URL for the web client, in a
  header or a WebSocket's first message for any other client): the public key opens an allow-list
  of reads and subscriptions and acts on nothing; every other op, a write of the backlog or the
  configuration included, needs the private key (the user's answer remote-cli-Q9, 2026-11-22)".
- "the surface server keeps its key" becomes "keeps its two keys".
- CR-449 (board-griller), if merged first, adds the fourth named exception, whose text says "any
  client holding the board's key" and "every holder of the key": each becomes "the private key"
  / "every holder of the private key", and its "`chantier board --new-key` revokes the key"
  becomes "`chantier serve --new-key` replaces both keys". If CR-449 lands after this CR, its
  Driver writes it so (the Chief of Staff tells it). This CR adds no named exception; C adds the
  next one and numbers it against the text at its head (a fifth when CR-449's fourth is there).

### 5. Cards

- `chief-of-staff.md`: the row "board on my phone", "where is the board?" says the link it gives
  is the private one (to the user only) and that the `read-only:` link can be shared and acts on
  nothing; the row "a new board key", "the board's link leaked": `--new-key` replaces both keys.
- `session-start.md` where it quotes the start lines: the `read-only:` line is passed on with them.

## Overlaps in batch-30

- CR-449: its `griller.*` ops need the private key through the allow-list, with nothing to write
  here; its AGENTS.md text, as in section 4.
- CR-446 (live): `live --url` with a read link needs nothing of CR-446; its several `--url` each
  take either key.

## Out of scope

- A read-only mode of the web page (hiding its write controls): a write refused under the read
  key reaches the page as any refused write does today; the page's own mode goes with the web UI's
  move to its own project.
- The profiles and the remote commands (part C).

## Evidence

- Tests, parametrized (`tests/test_server_api*.py`, `test_board_exposure.py`): every op of
  `protocol.OP_ARGS` not in `READ_OPS` answers 403 under the read key, over HTTP and over the
  WebSocket, and writes nothing (the test iterates `OP_ARGS`, so a future op is covered with no
  edit); every op of `READ_OPS` and every topic of `READ_TOPICS` answers under the read key; both
  keys pass in the header, the cookie and `hello`; the answers carry `X-Chantier-Access`, the
  CORS answers `Access-Control-Expose-Headers`, `welcome` carries `access`; a `server.json` with
  only `key` gets a `read_key` at the start and keeps its `key`; `--new-key` replaces both; the
  start lines and `webui` hold the `read-only:` line (`board/command.py`'s shipped constant).
- `protocol.json`'s test passes with `welcome.access`.
- Scenario (`surface-board` unit, the running server): the `read-only:` line is read from the
  start lines; with its link `board.get` and a `project` subscription answer, `backlog.move` and
  `config.put` answer 403 and change no file; `live --once --url <read link>` prints the screen;
  the private link writes as before.

Host and default matrix: none; the keys do not depend on the host or on a configured value.

## Open questions

None.
