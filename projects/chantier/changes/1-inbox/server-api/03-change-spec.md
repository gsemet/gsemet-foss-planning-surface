# Change Specification: the server's API over a WebSocket, the web UI one client among others

Origin: verbal (2026-11-20, planning-server's grill, answer planning-server-Q29). No tracker issue.

This CR had no grill of its own. Its decisions come from the user's words in `intake/request.md`
and in `2-backlog/P3/planning-server/02-answers.md` (Q29, and the server, its key, its network and
its election as Q1 to Q30 leave them). Every choice those words leave open is written below as the
recommended answer and listed in section 16, for the user to confirm or change before this CR goes
to `3-ready`. Where a choice in the body is marked "(Q*n*)", it is section 16's question *n*.

## 1. Goal, in the user's terms

The surface server is the one writer of the surface: it keeps the state and exposes the server,
chantier's equivalent of Vercel Board (the user, 2026-11-20). Today `chantier board` also serves
the web UI, and the UI reads the server through private routes made for it. The user wants the UI
out of the server, so that "everything goes through a WebSocket, or HTTP as the degraded case
(behind a proxy, for instance)", and so that several UIs, or native Android or iOS apps, can be
built on it.

This CR gives:

- **One published API**, protocol version 1, with one message shape on two transports: a
  WebSocket (the normal case: calls, and the server pushing each change of what a client watches)
  and HTTP (the degraded case: the same calls, and a long-poll in place of the push).
- **The key on both**, for the web client and for any other client (another web UI, a script, a
  native app), on the machine and on the local network, behind a proxy too.
- **The web UI as one client among others**: it uses only the published API, and moves out of the
  server's code into a client folder the server serves as plain files (Part 2, §8).

## 2. Dependencies and neighbours

- **Needs `2-backlog/P3/planning-server` merged first** (`depends.json`: `after: planning-server`),
  and with it Parts A (`1-inbox/typed-journal-events`) and B (`1-inbox/plan-store-interface`),
  which that CR needs. From them this CR takes, as they leave the code:
  - Part C's writer: the `writer` field of `GET /api/board` (C.13) and the route `POST
    /api/writer/sync`, which become the op `writer.sync` and the `writer` field of the `board`
    topic (§5); the `sync-*@1` journal lines, which the `events` topic carries.
  - Part A's typed journal lines (`type: "name@N"`, `seq`, `journal.read`'s effective type), which
    the `events` topic carries as they are (§5.5).
  - Part C removes the autosync routes (`/api/autosync*`, `board/autosync_api.py`); this CR has
    none to port.
- If this CR is started before those land (the user's word only), the Driver ports the routes as
  `main` holds them then, and the later CR carries its routes into the API instead: the rule is
  "every route of the board is an op of protocol 1 when both are merged", whichever lands second.
- Pending items it composes with, not edited by it:
  - `2-backlog/P2/one-read-interface-over-the-planning-fol`: the read half of the `store`; the
    API's ops read the planning folder through whatever it adds, if it lands first.
  - `2-backlog/P3/board-griller`, `board-history`, `board-help-page`, `board-batch-view`,
    `board-triage-polish`: web UI work. Each that lands after this CR uses only published ops and
    topics, and adds an op or a topic to protocol 1 (an additive change, §6) when it needs one.
  - `1-inbox/forge-connectors` and `1-inbox/outside-poller`: an outside poller writes into the
    journal; its lines reach clients through the `events` topic with nothing more.
- From the Vercel Board study (`planning-server/experiments/vercel-board-study.md`, §2, §11, §13
  item 7): Board reads its one ordered log "over SSE or long-poll with a cursor", and checks every
  backend with a conformance kit. This CR borrows the cursor and the long-poll, and a published
  schema checked by a test; no Board dependency (planning-server Q1, Q2).

## 3. Decisions carried

| Decision (source) | Where it lands |
| --- | --- |
| The writer is the one that keeps the state and exposes the server, chantier's equivalent of Vercel Board (planning-server, 11-20) | §1; the API is how the server is exposed |
| The UI goes out of `chantier board`; everything goes through a WebSocket, or HTTP as the degraded case behind a proxy (planning-server-Q29, `intake/request.md`) | §4 to §8 |
| Goal: several UIs, native Android or iOS apps (Q29) | §5 (a published protocol, a schema file, a doc for client authors), §7 (the key for a client that is not the web page) |
| A CR of its own, after `planning-server`; until then the writer keeps the board's current HTTP API (Q29) | §2 |
| No Board dependency, hosted or local; chantier's journal, surface server and watchers stay the channel (planning-server Q1, Q2) | §2; the `events` topic reads the same journal |
| The board's key in its URL, the local network, plain HTTP; authentication beyond the key out of scope (planning-server §9, AGENTS.md) | §7 |
| Writes with no writer are refused (planning-server Q5, C.8) | §5.4: a write op answers the refusal C.8 gives today, status 409 |
| `uv` is the only tool to install; a dependency ships wheels for Linux, macOS and Windows and replaces hand-written code (AGENTS.md, CONTRIBUTING.md) | §9.1: one dependency, `websockets` |
| The board's page has no build step and no framework (CONTRIBUTING.md) | §8: none added |

## 4. Words

- **Server:** the surface server, `chantier board` (also run over an in-project planning folder).
  Its command name does not change (Q13).
- **Client:** any program that talks to the server through the API: the web client, the CLI's own
  calls (the probe and `seats.register`), a script, another UI, a native app.
- **Web client:** today's web board page (`board/web/`, HTML, CSS and ES modules).
- **Protocol:** the messages of the API, version 1 here (`PROTOCOL = 1`).
- **Op:** a named call, `<area>.<verb>` (`project.state`, `backlog.move`), with its arguments and
  its result.
- **Topic:** a named thing a client watches (`project`, `prs`); the server sends its whole value
  at the start and again each time it changes (§5.3).
- **Rev:** a topic's revision, an opaque string; equal revs mean an equal value.
- **WebSocket binding** and **HTTP binding:** the protocol on each transport (§5, §6).
- **Probe:** `GET /api/board`, the one route outside the protocol's versioning (§6.4).

## 5. The protocol, version 1

### 5.1 Frames

JSON text frames, UTF-8, one JSON object each, with its kind in `t`. A field the reader does not
know is ignored (§6, additive changes). Times are UTC, `YYYY-MM-DDTHH:MM:SSZ`, as `clock.now()`.

From the client:

| `t` | Fields | Meaning |
| --- | --- | --- |
| `hello` | `protocol` (integer), `client` (text, at most 100 characters, for the server's own lines, e.g. `chantier-web/0.15.0`), optional `key` | first frame on a WebSocket, within `HELLO_S` (10 s) |
| `call` | `id` (text, at most 64 characters, the client's), `op`, `args` (object, `{}` when none) | one op; answered by one `result` with the same `id` |
| `sub` | `id`, `topic`, `args` | watch a topic; answered by one `result` (`ok`, or the refusal), then `event` frames |
| `unsub` | `id` (the `sub`'s) | stop watching; answered by one `result` |

From the server:

| `t` | Fields | Meaning |
| --- | --- | --- |
| `welcome` | `protocol` (1), `server` (`version`, `pid`, `served`, `surface`), `ops` (the names, sorted), `topics` (the names, sorted), `now` | the answer to a good `hello` |
| `result` | `id`, `ok` (bool), `status` (an HTTP status number), `data` (object or null), `error` (text, when not `ok`), `now` | the answer to a `call`, `sub` or `unsub` |
| `event` | `sub` (the `sub`'s `id`), `topic`, `rev`, `data`, `now` | a topic's whole value: once at once after the `sub`'s `result`, then at each change |
| `tick` | `now` | every `TICK_S` (5 s) on each WebSocket: the client's clock and its "data is N s old" line |
| `error` | `code` (one word), `error` (text) | a fault of the connection; the server closes it right after (§5.6) |

`status` keeps the HTTP meaning the web client handles today: 200, 202 (accepted, `costs.recompute`),
400 (bad arguments), 403 (refused: §7.3), 404 (unknown project, op or topic), 409 (precondition or
conflict, with `data.stale: true` for a file changed since it was read, as `write_api._write` sets
today), 413 (too large), 415 (not JSON), 429 (too many subscriptions), 500 (the record could not
be read). A write op's `data` is the JSON body its route answers today (`{"ok", "lines", "results",
"journal"}` and the rest), unchanged.

### 5.2 Ops

Each op is today's route, with the route's query or body as `args` and its JSON answer as `data`
(no payload changes in this CR, so the web client's model and views do not change). `project` is
the project's id everywhere.

| Op | Args | Today's route |
| --- | --- | --- |
| `board.get` | none | `GET /api/board` (the full payload: projects, seats, `writer`, ...) |
| `project.state` | `project`, optional `rev` | `GET /api/projects/<id>/state`; with `rev` equal to the current one, `data` is `{"changed": false, "rev"}` (today's 304); else the state with `rev` |
| `project.tree` | `project`, `path` | `GET .../tree?path=` |
| `project.file` | `project`, `path` | `GET .../file?path=` for a text file: `data` `{text, cut, sha256}` (today's body and its `X-Chantier-Cut`, `X-Chantier-Sha256`); a file `files.kind_of` does not call text answers 415 "binary: read it over HTTP" (§6.3) |
| `costs.get` | `project` | `GET .../costs` |
| `costs.recompute` | `project` | `POST .../costs/recompute` (status 202) |
| `prs.get` | `project`, optional `batch` | `GET .../prs?batch=` (the 10 s cache, `prs.TTL_S`, as today) |
| `seats.register` | `project`, `session` | `POST /api/seats` |
| `backlog.new`, `backlog.move`, `backlog.labels`, `backlog.group`, `backlog.ungroup`, `backlog.file`, `backlog.next_batch` | the route's body | `POST .../backlog/new`, `move`, `labels`, `group`, `ungroup`, `PUT .../backlog/file`, `POST .../backlog/next-batch` |
| `journal.get` | `project` | `GET .../journal` (the board's own journal since the last rescan) |
| `journal.rescan` | `project` | `POST .../journal/rescan` |
| `config.get` | `project` | `GET .../config` |
| `config.put` | `project`, then the route's body (`changes`, `base_sha256`, `dry_run`) | `PUT .../config` |
| `writer.sync` | none | `POST /api/writer/sync` (planning-server C.13) |

An op's arguments are checked by its model (§5.7): a missing, extra or mistyped argument answers
400 naming it, as the routes' `_text` and `_texts` do today. The ops that write are the backlog's,
`journal.rescan`, `config.put`, `costs.recompute`, `seats.register` and `writer.sync`: the write
rule of §7.3 applies to them.

### 5.3 Topics

| Topic | Args | Value (`data`) | Rev |
| --- | --- | --- | --- |
| `board` | none | `board.get`'s data | a hash of the projects' lines, the seats and the `writer` entry |
| `project` | `project` | `project.state`'s data | the project's fingerprint (`board/fingerprint.py`, the same as today's ETag) |
| `costs` | `project` | `costs.get`'s data | the live figure's mark (`Live.mark()`) and the record's fingerprint |
| `prs` | `project`, optional `batch` | `prs.get`'s data | a hash of the answer |
| `journal` | `project` | `journal.get`'s data | the size and mtime of `board-journal.jsonl` |
| `events` | `project`, optional `after` (a `seq`, default: the last line's, so only new lines come) | `{"lines": [...]}`: the project's `forge-journal.jsonl` lines with `seq` above the cursor, as Part A's `journal.read` gives them (effective `type`, `seq`, `t`, `source`, `audience`, payload), at most 200 per event, oldest first | the last `seq` sent |

The `events` topic is new: it lets a client follow the journal (merges, red CI, the board's
writes, the configuration's changes, the writer's `sync-*@1` lines) with no reread. Its first
event after `sub` carries the lines after `after` (none by default); each later event carries only
the new lines.

How a change is seen (`board/api/push.py`, a thread beside the hub's, `PushLoop.poll(now)` as
`hub/loop.py`):

- Every `PUSH_EVERY_S` (2 s), for each topic and arguments that at least one client watches, the
  loop computes the rev; when it differs from the last one sent, it computes the value once and
  sends one `event` to every client that watches it. A topic nobody watches costs nothing.
- `project` and `costs`: while a client watches one, the loop calls the live figure's 5-minute
  rule (`Live.ask(running)`) at each check, as a page's read does today (`routes._state_of`).
- `prs`: the forge read follows today's rule, carried from "when the page asks" to "while a client
  watches": one read when the subscription starts, then at most once every 10 s per project and
  batch (`ForgeReads`, `prs.TTL_S`) while a PR of that batch is not done; none once every PR is
  merged or closed, until a PR joins the batch. However many clients watch, one read per project
  and batch per 10 s. The `merged` and landed lines the read appends to `forge-journal.jsonl`
  (`prs.answer`) are unchanged.
- A seat check (`Seats.gone()`, today at each request) also runs at each loop pass, so a board
  started with `--seat` stops as today when every seat has gone, whatever its clients do.

### 5.4 Writes with no writer

A write op in external mode with no live writer answers 409 with planning-server C.8's text, as
the routes do once that CR lands. Nothing else changes in the writer's rules.

### 5.5 Order and delivery

- On one WebSocket, `result` frames come in the order their `call` frames came for the calls of
  one client turn; the server may answer calls in parallel (a slow `prs.get` does not hold a
  `project.state`): a client matches `result` to `call` by `id`, never by order.
- An `event` always carries the topic's whole value (no diff), so a lost or skipped event never
  leaves a client wrong: the next one is whole (Q3).
- The `events` topic's lines are each sent once per subscription, in `seq` order; a client that
  reconnects subscribes again with `after` = the last `seq` it saw and gets every line it missed
  that the file still holds.

### 5.6 The connection

- The upgrade: `GET /api/v1/ws`, judged as an HTTP request (§7). A refused upgrade answers the
  HTTP status (401 with `guard.NEEDS_KEY`'s text, 403) and opens no socket. An upgrade that has no
  key yet (the key comes in `hello`, §7.1) is accepted, and the connection reads nothing but its
  `hello`.
- `hello` with the right `protocol` and a key (or after an upgrade that carried one): `welcome`.
  Another `protocol`: `error` `protocol`, text `this is chantier <version>, protocol 1; the client
  speaks protocol <n>: use a client of chantier <version>`, then close 4426. A bad or missing key:
  `error` `key`, text `guard.NEEDS_KEY`, then close 4401. No `hello` within `HELLO_S`: close 4408.
  Any frame before `welcome` but `hello`, a frame that is not a JSON object, or an unknown `t`:
  `error` `frame`, then close 4400.
- A `call` or `sub` with an unknown `op` or `topic`: a `result` 404, the connection stays.
- Limits (constants in `board/api/times.py`): a frame from a client at most 4 MiB (more: close
  1009); at most 32 subscriptions per connection (the 33rd: `result` 429); at most 64 WebSockets
  at once per server (the 65th upgrade: HTTP 503 `too many clients`). The server pings each socket
  every 20 s and closes one that does not answer within 20 s (the WebSocket library's own ping).
- The server stopping (Ctrl-C, its seats gone, the writer's final cycle): each socket is closed
  with 1001 after the final cycle; a client reconnects (§8.2).

### 5.7 The published schema

- `board/api/protocol.py`: one pydantic model per frame kind and per op's and topic's arguments
  (`model_config = ConfigDict(extra="forbid", frozen=True)`), `PROTOCOL = 1`, `OPS`, `TOPICS`.
- `board/api/protocol.json`, shipped: the JSON Schema of every frame and of every op's and topic's
  arguments, keyed by name, sorted, UTF-8, LF, as Part A's `hub/schemas.json`. A test fails when a
  model's schema differs from its entry (§10).
- The results' `data` are described in `docs/server-api.md` by their fields and an example each,
  not by a schema in this CR (Q5).

## 6. Versions and the HTTP binding

### 6.1 Versioning

- Protocol 1 changes only by addition: a new op, topic, frame field or `data` field. A client
  ignores what it does not know; the server ignores nothing it does not know in a client's frame
  but unknown fields of `hello` (so a newer client's `hello` is still read).
- A change that removes or changes the meaning of anything is protocol 2, served under
  `/api/v2/`; the CR that makes it decides whether the server also keeps protocol 1 (Q4). In this
  CR the server speaks protocol 1 only.
- `welcome.ops` and `welcome.topics` let a client see what this server has before it calls it.

### 6.2 The HTTP binding

The same ops and topics, for a client whose WebSocket cannot open (a proxy that refuses the
upgrade, a script, a client that wants no socket):

- `POST /api/v1/call/<op>`: the body is the op's `args` (JSON, `{}` when none); the answer's HTTP
  status is the result's `status`, its body the `result` frame without `t` and `id` (`{"ok",
  "status", "data", "error"?, "now"}`), `Content-Type: application/json; charset=utf-8`, and the
  header `X-Chantier-Now`, as today.
- `POST /api/v1/poll`, the long-poll: the body is `{"subs": [{"key": <the client's>, "topic", "args",
  "rev": <the last rev seen, or null>}, ...]}` (at most 32). The server answers at once with one
  event per sub whose rev is null or differs from the current one, else holds the request until
  one differs or `HOLD_S` (20 s) passes, and then answers `{"events": [{"key", "topic", "rev",
  "data"}, ...], "now"}` (empty at the hold's end). An `events` sub's `rev` is the last `seq` seen.
  The server keeps nothing about a poller between two requests: a proxy that reconnects, a server
  restart or a second machine changes nothing for the client. The `prs` read rule of §5.3 counts a
  poll's `prs` sub as watching for its hold; one read per project and batch per 10 s holds.
- `HOLD_S` is under the usual proxies' idle limit (60 s for nginx's `proxy_read_timeout` by
  default), so a held request is not cut.

### 6.3 Files

`GET /api/v1/projects/<id>/file?path=` answers the file's bytes as today's `GET .../file` (its
type, its `X-Chantier-Cut`, its `X-Chantier-Sha256`, the attachment header of `files._attachment`),
on both bindings: an image's `src` and a download's `href` need an address. It is the one `GET`
of protocol 1.

### 6.4 The probe, and the routes that go

- `GET /api/board` stays, outside the versioning, frozen: `{"board": true, "version", "pid",
  "served", "surface", "protocols": [1]}`. Every chantier version's `address.probe` reads `board`,
  `served`, `version` and `pid` from it to find a running board and to refuse one of another
  version (`board/command.py`'s `_recorded`, `_answering`, `_another_version`); it must answer the
  same to every version, older and newer. Its other fields of today (projects, seats, `writer`,
  `local_url`, `now`) move to `board.get`.
- `address.register_seat` calls `POST /api/v1/call/seats.register`; it only runs against a board
  of the same version (the probe refuses another before).
- Every other `/api/...` route of today goes (`routes.ROUTES`, `write_api.ROUTES`,
  `config_api.ROUTES`, and Part C's `/api/writer/sync`): its op replaces it (Q14). An old route
  answers 404 `not found` as any unknown `/api/` path.
- `GET /` and the web client's files, the `?k=` exchange and its cookie: §7 and §8.

## 7. The key

### 7.1 Where a client puts it

| Client | On HTTP | On the WebSocket |
| --- | --- | --- |
| the web client served by the server (same origin) | the cookie `chantier_board`, set by the `?k=` exchange (unchanged) | the cookie, sent with the upgrade |
| a script, a native app | the header `X-Chantier-Board-Key` (unchanged) | the same header on the upgrade, or `hello.key` |
| a web page served elsewhere (another origin) | the header `X-Chantier-Board-Key` (a browser sends it after the CORS preflight, §7.4) | `hello.key` (a browser cannot set a header on an upgrade) |

The key is checked by `key.is_good` (constant time), read through `KeyFile` (so `--new-key` while
the server runs refuses the old key from the next request, and closes every WebSocket that used
it with 4401 at the push loop's next pass).

### 7.2 The cookie counts only from the server's own origin

A browser sends the cookie with a request from any page of the same site, another port of the
same host included (`SameSite=Strict` is per site, not per origin), and a WebSocket upgrade is not
held back by CORS. So the cookie authorises a request or an upgrade only when it comes from the
server's own page:

- `Sec-Fetch-Site` absent or `same-origin`, and `Origin` absent or equal to `http://<host>` or
  `https://<host>`, where `<host>` is the request's `Host`, or its `X-Forwarded-Host` when it has
  one (a proxy that rewrites `Host`, §7.5).
- Otherwise the cookie is ignored: with no header key and no `hello.key`, the request answers 401
  (the upgrade: 401, no socket).

### 7.3 The rule for writes

- Authorised by the cookie: today's `guard.refusal` (403 when not from the board's own page, 415
  when the body is not JSON), on every `POST` of `/api/v1/` (reads and writes alike, since every
  op is a `POST` there), and on the WebSocket by §7.2's check at the upgrade.
- Authorised by the header or `hello.key`: no origin rule (the key itself is what a foreign page
  cannot have); the body must still be JSON (415).

### 7.4 CORS, for a web client served elsewhere

- `OPTIONS /api/v1/<anything>` answers 204 with `Access-Control-Allow-Origin: *`,
  `Access-Control-Allow-Methods: GET, POST`, `Access-Control-Allow-Headers: Content-Type,
  X-Chantier-Board-Key`, `Access-Control-Max-Age: 600`; every answer of `/api/v1/` carries
  `Access-Control-Allow-Origin: *`. `Access-Control-Allow-Credentials` is never sent, so a page of
  another origin never gets the cookie's answers: it needs the key (Q7).
- `guard.ALLOWED` gains `OPTIONS` for `/api/v1/` only; elsewhere `OPTIONS` stays 405.
- A page served over HTTPS cannot call a plain-HTTP server (the browser's mixed-content rule): such
  a client goes through a TLS proxy (§7.5). The server itself stays plain HTTP (Q8).

### 7.5 Behind a proxy

What the server supports, said in `docs/server-api.md`:

- The proxy terminates TLS and forwards to the server's address (often `127.0.0.1`, with
  `board.host: 127.0.0.1`); the WebSocket passes when the proxy forwards the `Upgrade` and
  `Connection` headers; when it does not, the web client works over the HTTP binding (§8.2).
- `Host` kept, or `X-Forwarded-Host` set (§7.2).
- A path prefix (the server at `https://example/chantier/`): the web client's addresses are all
  relative (today's rule), and the `?k=` exchange's `303` gets a relative `Location` (the request
  path's last segment and its query, `./` for the root), so the prefix is kept. Today's absolute
  `Location` (`guard.exchange`) changes for that.
- The key travels in clear over plain HTTP on the local network, as today (`BEYOND`'s start line
  says so); over a proxy, TLS protects it from the client to the proxy.

## 8. The web client

### 8.1 What changes in it (Part 1)

The page keeps its views, its model, its store, its words and its look; only how it reaches the
server changes.

- `js/core/transport.js` (new): the only module that opens a `WebSocket` or calls `fetch` (today
  `js/core/api.js` is the only one that calls `fetch`; the rule moves). It exports `call(op, args)`,
  `subscribe(topic, args, onEvent)` (returning the unsubscribe), `fileUrl(project, path)`, and the
  connection's state for the footer (`mode`: `live` or `http`, `heard`, `fails`, `denied`).
- `js/core/api.js`: the same exported functions as today (`board`, `projectState`, `costs`, `prs`,
  `tree`, `fileText`, `fileUrl`, `post`, `send`, `recompute`), each over `call`, so the views and
  `js/api/backlog.js`, `js/api/config.js` keep their imports. The route strings become op names.
- `js/core/refresh.js`: the 5-second read goes. It subscribes to `board`, and to `project` for the
  project shown (unsubscribing the one before), and writes each event into the store as a read
  does today. `reload()` after a write stays (one `project.state` call). The PRs view subscribes
  to `prs` for the batch shown and unsubscribes when the page is hidden or the view changes; the
  Costs view subscribes to `costs`. Hidden page (`visibilitychange`): the `prs` and `costs`
  subscriptions go and come back when the page shows again; `board` and `project` stay.
- The footer line (`js/ui/sidebar.js`'s `heard`): unchanged in live mode ("Data: N s ago" from the
  last frame, a `tick` included, so it reads "0 s" to "5 s"); in HTTP mode the same line gains
  " (HTTP)" (new i18n keys in every language file; `en` and `fr`); "Board unreachable" as today
  after two failures (Q15).
- `?transport=http` in the address forces the HTTP binding (kept by `js/core/router.js` as `lang`
  is), for a test and for a user behind a proxy that holds sockets open and silent.

### 8.2 Connecting

- At load, and at each reconnect: a WebSocket to `api/v1/ws` relative to the page (`ws:` for an
  `http:` page, `wss:` for `https:`), `hello` with `protocol: 1`. No `welcome` within 5 s, or the
  socket closed before it: the HTTP binding for the rest of the page's life (a reload tries the
  WebSocket again).
- Live mode, the socket closed after `welcome`: reconnect after 1, 2, 4, 8, 16, then every 30 s;
  each reconnect subscribes again (`events` with its last `seq`). Two failed reconnects in a row:
  "Board unreachable", as two failed reads do today.
- Close 4401 or HTTP 401: the "needs the link with its key" state of today (`denied`), no retry.
  Close 4426: the footer says the board was upgraded and to reload the page (new i18n key), no
  retry.
- HTTP mode: one `POST api/v1/poll` at a time, with the subscriptions and their revs; at once again
  after each answer; after a failure, again after 5 s.

### 8.3 Out of the server (Part 2)

The web client stops being part of the server's code (Q9):

- Its files move from `skills/chantier/scripts/cli/src/chantier/board/web/` to
  `skills/chantier/scripts/cli/src/chantier/clients/web/` (still package data of the one wheel, so
  `uvx --from <plugin>` and `uv run --project <checkout>` both have it, editable install included;
  `DESIGN.md` moves with it). `board/static.py` takes the folder it serves as a parameter
  (`Context.ui`), and knows nothing of the client but its files.
- `chantier board --ui <folder>` serves another client's files at `/` (any folder of static files:
  the user's own UI); `--ui none` serves the API only (`GET /` answers 404 `this server serves no
  UI: see docs/server-api.md`). Default: the shipped web client. The `?k=` exchange, the cookie and
  the page's security headers (`reply.HTML_POLICY`, `SECURITY`) apply to whatever folder is served.
- The server's code imports nothing from `clients/`; the web client calls nothing that is not in
  `protocol.json` (both checked, §10).
- No build step and no framework are added (Q10): the client stays hand-written HTML, CSS and ES
  modules, under the same targets (CONTRIBUTING.md, "The board's page").

### 8.4 Clients this CR ships

The web client, and the CLI's own two calls (the probe, `seats.register`). No other client and no
SDK; `docs/server-api.md` gives one short example per binding (Python with `websockets`'s sync
client, and browser JavaScript) (Q11). Native apps are out of scope.

## 9. The server's code

### 9.1 Dependency

`websockets` (pinned in the root `pyproject.toml`, locked in `uv.lock`; wheels for Linux, macOS
x86_64 and arm64, and Windows, and a pure-Python wheel) (Q12). It gives uvicorn its WebSocket
protocol (`board/app.py`'s `ws="none"` becomes the `websockets` implementation the pinned uvicorn
names; the Driver reads `uvicorn.Config`'s `ws` choices and takes the non-legacy one), and the
tests' and the scenario's client (`websockets.sync.client.connect`). It replaces hand-written
code: no WebSocket framing is written in chantier. It joins `starlette` and `uvicorn` in ruff's
`banned-module-level-imports` (loaded only when the board serves). `just lint` checks the lock.

### 9.2 Modules

New package `skills/chantier/scripts/cli/src/chantier/board/api/`:

- `protocol.py`, `protocol.json` (§5.7).
- `ops.py`: the op table, name to handler `(ctx, args) -> Result`. The handlers are today's route
  functions (`routes.board`, `state`, `tree`, `file`, `costs_of`, `recompute`, `prs_of`, `seats`,
  `write_api`'s and `config_api`'s), changed to take checked `args` instead of a `Request`;
  `write_api._write`'s status mapping and refusal shape are kept.
- `topics.py`: the topic table, name to (rev, value).
- `push.py`: `PushLoop.poll(now)`, the subscriptions of every connection and every held poll,
  `PushThread` started by `board/command.py`'s `_run` beside `HubThread` and stopped with it.
- `auth.py`: §7 (from `guard.py`: `authorised` learns where the key came from, `refusal` applies
  to the cookie only, the origin check of §7.2, CORS).
- `ws.py`: the Starlette WebSocket endpoint (`starlette` imported inside, as `app.py` does), the
  `hello` handshake, the frame loop, calls run in the thread pool (`run_in_threadpool`, as
  `app.endpoint`), events posted from `PushThread` to the event loop.
- `http.py`: `/api/v1/call/<op>`, `/api/v1/poll`, `/api/v1/projects/<id>/file`, `OPTIONS`, the
  probe.
- `times.py`: `PUSH_EVERY_S` 2, `HOLD_S` 20, `TICK_S` 5, `HELLO_S` 10, the limits of §5.6; test
  seam `CHANTIER_API_TEST_TIMES` (`<push_every>:<hold>:<tick>:<hello>`, read only there, as
  `CHANTIER_HUB_TEST_TIMES`).

`board/routes.py` keeps `handle` (the key, the method, then `http.py` or the static files);
`board/app.py` adds the WebSocket route `/api/v1/ws` before its catch-all route.

### 9.3 Start lines and messages

The start lines do not change (`board on <link> over <folder>`, `on this machine: ...`, `BEYOND`),
so `session-start.md`'s list of them holds. No new CLI message.

## 10. Evidence

### 10.1 pytest (`skills/chantier/scripts/cli/tests/`, in-process, few and parametrized)

- `test_server_api.py` (new), on a prepared two-project surface, through `ops`, `topics` and
  `PushLoop.poll(now)` with no socket and no sleep:
  - every op of `OPS`, parametrized: a good call answers the `data` today's route gave on the same
    prepared folder (the old route's test expectations, moved: `test_board.py`,
    `test_board_config.py`, `test_board_journal.py`, `test_board_prs*.py` call ops instead of
    routes; their cases do not drop); a missing, an extra and a mistyped argument answer 400
    naming it; an unknown op answers 404;
  - `project.state` with the current `rev` answers `{"changed": false}`;
  - topics: a `project` subscription gets one event at once; a file written under `1-inbox/` gives
    one event with a new rev at the next `poll`; no change, no event; two clients watching one
    topic cost one value computation; `events` with `after` gets only later lines, in `seq` order,
    and a line appended through `hub/journal.append` reaches it at the next `poll`; `prs` watched
    by three clients reads the forge (a fake reader, an injected clock) once per 10 s, and not at
    all once every PR is done;
  - the long-poll: null revs answer at once; current revs and no change answer empty at `HOLD_S`
    (the test seam); a change during the hold answers it;
  - the key: the cookie from a foreign `Origin` (another port of the same host) is refused, 401;
    the header key from a foreign origin is accepted and its write passes; the cookie from the
    page's own origin passes, `http` and `https` origins, `Host` and `X-Forwarded-Host`; the
    `?k=` exchange's `Location` is relative;
  - CORS: `OPTIONS /api/v1/call/board.get` answers 204 with §7.4's headers, never
    `Allow-Credentials`;
  - no writer in external mode: a write op answers 409 with C.8's text (a prepared case, the
    writer's entry absent).
- `test_server_api_ws.py` (new), one real server on `127.0.0.1` port 0 in a thread, through
  `websockets.sync.client` (one module, one server, at most 2 s): `hello` with the header key, then
  `welcome` (its `ops` and `topics` equal `OPS` and `TOPICS`); `hello.key` with no header; a
  `project` subscription, a file written, its event within 3 s; protocol 2: close 4426 with the
  text; a bad key: 4401; no `hello`: 4408 (the seam's `HELLO_S`); an upgrade with the cookie and a
  foreign `Origin`: 401; the 33rd subscription: 429; `GET /api/board` answers exactly the probe's
  fields.
- `test_server_protocol.py` (new): the shipped `board/api/protocol.json`, read from the repository
  at the head under test, equals the models' schemas; every op and topic name the web client's JS
  uses (the string literals passed to `call` and `subscribe` in the shipped `js/`, read from the
  repository) is in `OPS` or `TOPICS`, and no shipped JS file but `js/core/transport.js` contains
  `fetch(` or `WebSocket(`, nor a path under `api/` other than `api/v1/ws`, `api/v1/call/`,
  `api/v1/poll` and `api/v1/projects/` (the client uses only the published API).
- Part 2 adds to `test_server_protocol.py`: no module of `chantier/board/` imports or names
  `clients/`; `board --ui none` answers 404 at `/` and serves the API; `--ui <a temporary folder
  with an index.html>` serves it with the security headers.
- The existing structure tests that read the web client's files (`test_board_design.py`,
  `tests/test_code_targets.py`, the i18n keys test, `test_board.py`'s lazy-import test with
  `websockets` added to the banned list) keep reading the shipped files from the repository; Part
  2 changes only their path.
- `just test` stays within its budget (AGENTS.md: at most 30 s above its 18.5 s of 2026-11-14):
  the new tests add at most 3 s; the Driver reports `just test`'s time at the base and at the head
  on the same machine in the PR.

### 10.2 Scenario, unit `surface-board` (`scenario/run_scenario.py`)

Case `remote_board` rewritten for protocol 1 (its key, cookie and frame checks stay, on the new
paths), with these steps added, through `websockets.sync.client` and `urllib` against the real
`chantier board` process:

- the WebSocket with the cookie from the board's own origin: `welcome`; a `project` subscription,
  then `chantier file` run as a CLI command in the same project: an event with a new rev within
  `PUSH_EVERY_S` (shortened by `CHANTIER_API_TEST_TIMES`) plus 2 s;
- `backlog.move` over the WebSocket: the folder moved, one `board` line in `forge-journal.jsonl`,
  and an `events` subscription gets that line;
- the HTTP binding: `board.get`, a write, and a long-poll that answers when `chantier file` runs;
- the cookie from a foreign origin (another port): 401 on HTTP and on the upgrade; the header key
  from a foreign origin: accepted;
- `GET /api/board`: the probe's fields only; an old route (`GET /api/projects/<id>/state`): 404;
- the board stopped: the open WebSocket is closed with 1001.

Case `surface_server`: a second `board --seat` on the running board registers its seat through
`seats.register` (unchanged result). `scenario/README.md`'s Coverage list names each new check
with its test, as `test_scenario_coverage.py` checks. The unit's budget (500 s) holds: the steps
add at most 20 s; the Driver reports the unit's time at the base and at the head.

### 10.3 The transport and key matrix

Not a host matrix (the server does not depend on the host, nor on a configured value: `board.host`
changes where it listens, not the API). One line per cell, each proved by the test named:

| Binding | Key from | Origin | Expected | Proof |
| --- | --- | --- | --- | --- |
| WebSocket | cookie | the server's own | `welcome` | scenario, `test_server_api_ws.py` |
| WebSocket | cookie | another port of the host | 401, no socket | both |
| WebSocket | header | any | `welcome` | `test_server_api_ws.py` |
| WebSocket | `hello.key` | any | `welcome` | `test_server_api_ws.py` |
| HTTP | cookie | own | answered | scenario |
| HTTP | cookie | foreign | 401 | both |
| HTTP | header | foreign, after preflight | answered, CORS headers | `test_server_api.py` |
| either | none or bad | any | 401 / 4401 | both |
| either | in-project folder | own | the same ops (no `writer.sync` refusal: in-project answers as Part C says) | `test_server_api.py` |

### 10.4 By hand, before the push (the Driver)

- `just check`; `just eval-dry-run` (a change under the CLI's `src/`); `just scenario` green on the
  pipeline's `just scenario (ubuntu-latest)` job, and, as the batch's top CR, locally on Windows
  (`chantier gate`), as AGENTS.md says. No CI job is added or changed.
- `just docs-screenshots` at the head: the script talks to the board over the WebSocket (it rewrites
  the `board` topic's `served` with Playwright's WebSocket routing, `page.route_web_socket`, as it
  rewrites `GET /api/board` today, `fix_surface_path`); every picture of `docs/web-board/`, run at
  the base and at the head on the same machine, comes out the same file (the page looks the same
  in live mode), or the PR names each that differs and why.
- The web client opened in Chromium on the machine (live mode, `Data` line moving, a Triage move
  shown in a second tab within 3 s), with `?transport=http` (the " (HTTP)" line, the same move
  within `HOLD_S`), and on the user's phone over the local network (Safari or Chrome): the page
  loads and updates. A phone check the Driver cannot run is named in the PR's Known gaps ("no check
  on a phone"), and the Chief of Staff asks the user for it.
- Not proved by this CR, said in its Known gaps: a real proxy (nginx or Caddy) in front of the
  server; `docs/server-api.md` gives the proxy's needs, and the HTTP binding's test is the
  evidence for a proxy that refuses the upgrade.

## 11. Cards, project rules and docs

### 11.1 Cards

None changes: `session-start.md` names the start lines (unchanged) and the probe `GET /api/board`
(kept); `hosts/claude-code.md` and `hosts/copilot.md` name `GET /api/board` with the key (kept);
`coder.md`, `debugger.md` and `verifier.md` name the board's write paths in general;
`chief-of-staff.md`'s "board on my phone" row gives the link (unchanged). The Driver searches the
cards for `/api/` and `board/web` again at the head and changes any text the code makes false.
`routing.md` and `startup-manifest.json`: unchanged.

### 11.2 `AGENTS.md` (chantier's; the user's merge of the PR is their approval) (Q16)

As the text stands once planning-server has landed:

- "Second, the surface server, `chantier board`: the web board's server, for the user on this
  machine and the local network, behind a key in its URL: it serves the record and the planning
  folder's files, and it edits ..." becomes "Second, the surface server, `chantier board`, for the
  user on this machine and the local network, behind a key (in its URL for the web client; in a
  header or a WebSocket's first message for any other client): through one published API (a
  WebSocket, and HTTP as the degraded case, behind a proxy for instance: the same protocol, not a
  fallback) it serves the record and the planning folder's files, and it serves the web client's
  files, one client among others; it edits ...".
- "one named exception, its PRs page: when that page asks, at most once every 10 s per project
  and batch shown, while a PR of the batch shown is not done, plus one read when the page opens
  and one at once on each change of the batch shown, it reads the forge" becomes "one named
  exception, a batch's PRs: while a client asks for them (one read, or a subscription), at most
  once every 10 s per project and batch, while a PR of that batch is not done, plus one read when
  a subscription starts, it reads the forge".
- "and a second, from the same page:" becomes "and a second, from the same read:".
- "a third, from its Configuration page: a save appends" becomes "a third, from a configuration
  save (the web client's Configuration page, or any client's `config.put`): a save appends".
- The no-setup sentence's "except the board's PRs page and the forge hub" becomes "except the
  server's read of a batch's PRs and the forge hub".
- Part 2: "A change under `skills/chantier/scripts/cli/src/chantier/board/web/` reads its
  `DESIGN.md` first and keeps it true." names `.../chantier/clients/web/`.

### 11.3 `CONTRIBUTING.md`

- The board paragraph (item 2 of the parts list): the same edits as AGENTS.md's.
- "the web board reads the server's API, which the views of `status.py` feed: change them
  together" adds "(protocol 1, `docs/server-api.md`: an addition only; a change is protocol 2)".
- "The board's page" section: "`js/core/` (`api`, ...)" adds `transport`; the rule that only
  `js/core/api.js` calls `fetch` becomes: only `js/core/transport.js` calls `fetch` or opens a
  `WebSocket`; Part 2 changes the folder's path there, in the repository tree drawing (`its web
  board in board/web/`), and in the `just lint` Biome path (`justfile`'s `lint` recipe).
- The dependency paragraph needs no change (`websockets` meets it).

### 11.4 Docs (chantier's `docs/` and `README.md`)

- `docs/server-api.md` (new): for a client's author: the two bindings, the key (§7.1's table, the
  origin rule, CORS), the frames, every op and topic with its arguments and one example `data`,
  versioning (§6.1), limits and close codes, behind a proxy (§7.5), and one example per binding.
  `protocol.json` is named as the schema of record.
- `docs/web-board.md`: the first paragraph (the server serves an API, and the web page is one
  client of it, `docs/server-api.md`); "The views" ("The data refreshes by itself": live over a
  WebSocket; over HTTP, the line says "(HTTP)"); PRs, "Refresh" (reads while the page shows the
  PRs, as §5.3 says) and "The signal" (its "when a read finds" holds; "the page writes one second
  line" becomes "the read writes"); Configuration (unchanged but where it names the page's save);
  "Starting the board" (a bullet: other clients and the key in a header; a bullet: behind a
  proxy, pointing to `docs/server-api.md`); "Retaking the pictures" (the script and the
  WebSocket); Part 2: "Starting the board" names `--ui`.
- `docs/boards.md`, "The web board": one sentence: the server's API serves the web board and any
  other client (`docs/server-api.md`).
- `README.md`, "The CR board": "serves the CR board as a web page" adds "and an API for other
  clients"; the docs list gains `docs/server-api.md`.
- `docs/use-cases.md`, `docs/planning-modes.md`, `docs/planning-folder.md`, `docs/hosts.md`,
  `docs/costs.md`, `docs/agents-and-models.md`, `docs/gates.md`, `docs/release-process.md`,
  `docs/tutorial-claude-code.md`, `docs/use-cases-direct.md`, `docs/use-cases-foreman.md`: searched
  (`board`, `api/`, `HTTP`, `page`, `refresh`), no sentence made false; the Driver searches again
  at the head.
- **SVGs:** none changes. No diagram nor its `-texts.md` names the web board, its API, HTTP or a
  WebSocket (searched in every `docs/*-texts.md` and every `docs/*.svg`'s text and `<desc>`:
  `board`, `server`, `HTTP`, `web`, `browser`, `phone`). The diagrams `how-chantier-works`,
  `planning-modes` and the others stay as planning-server leaves them.
- Pictures: `docs/web-board/*.png` unchanged when §10.4's run gives the same files.
- `board/web/DESIGN.md` (Part 2: `clients/web/DESIGN.md`): its first paragraph names its folder;
  its rules and tokens do not change (no new colour: the "(HTTP)" text uses the footer's ink).
- `docs/release-notes/`: a new file for the release (§12), never an old one edited.

## 12. Rollout

- The release notes say: the server has a published API (protocol 1, `docs/server-api.md`) over a
  WebSocket, and over HTTP behind a proxy that refuses the upgrade; the web board uses it and
  updates live; the old `/api/...` routes are gone (a script of the user's that calls them moves
  to `/api/v1/call/<op>`), `GET /api/board` stays for the probe with fewer fields; a web page
  served elsewhere uses the key in a header; Part 2: `--ui`.
- Mixed versions: a board of another version is refused before any API call (the probe, kept for
  every version); a page left open across an upgrade gets close 4426 or a 404 and says to reload.

## 13. The cut (Q1)

Recommended: two CRs, in order.

| CR | What | Size |
| --- | --- | --- |
| `server-api` (this one) | §5 to §7, §8.1, §8.2, §8.4, §9, the docs and rules of §11 but Part 2's | the protocol, both bindings, the push, the key, the web client ported; most of the evidence |
| `web-client-out` (new inbox item, after `server-api`, filed by the Chief of Staff on the user's word) | §8.3: the folder move, `--ui`, Part 2's checks of §10.1, the paths in AGENTS.md, CONTRIBUTING.md, the justfile, `DESIGN.md`, `docs/web-board.md` | a move and one option; small |

Each half is coherent alone: after the first, the web client already uses only the published API
(checked by `test_server_protocol.py`), in its old folder; the second only moves it and lets the
server serve another. Splitting the first further (HTTP binding first, the WebSocket after) leaves
an intermediate web client to write twice; not recommended.

## 14. Out of scope

- A native Android or iOS app, another web UI, an SDK (the protocol makes them possible; none is
  built here).
- TLS in the server; authentication beyond the key (users, roles, a key per client); a key sent by
  QR code.
- A change to any op's result or to any view of the web client; the board's write scope (the
  backlog, the configuration, as AGENTS.md says).
- Diffs or patches in events; a result schema for every op (Q5).
- Renaming `chantier board` (Q13).
- The CR board pane in Claude Code (`hooks/`): it reads `STATUS.json`, not the server; untouched,
  so no pane screenshot is owed.

## 15. Self-containment notes for the Driver

- Seams to follow: `hub/loop.py` and `hub/times.py` (a thread with `poll(now)` and a test-times
  seam), `board/routes.py` (`handle`, `_judged`, `_dispatch`), `board/guard.py` (`exchange`,
  `authorised`, `refusal`), `board/key.py` (`KeyFile`, `is_good`, `HEADER`, `COOKIE`),
  `board/app.py` (the lazy imports, `run_in_threadpool`, `make_server`'s `ws`),
  `board/fingerprint.py` (`fingerprint`, `StateCache`), `board/costs.py` (`Live.ask`, `mark`),
  `board/prs.py` (`ForgeReads`, `TTL_S`, `answer`), `board/seats.py` (`gone`),
  `board/address.py` (`probe`, `register_seat`, `_call`), `board/command.py` (`_run`, where
  `HubThread` starts), `hub/journal.py` (`read`, Part A's types), `scripts/docs_screenshots.py`
  (`fix_surface_path`).
- Web client rules (CONTRIBUTING.md, "The board's page"): files at most 300 lines, functions at
  most 50, no global, relative addresses, `innerHTML` only in `js/core/dom.js`, words through
  i18n in every language file; Biome through `just lint`.
- Portability: no shell, UTF-8 frames, the WebSocket library's own framing; Windows' sockets
  (`board/command.py`'s `_bind` rules) unchanged.

## 16. Open questions for the user

Each has the answer this specification is written with; a different answer changes the sections
named.

1. **The cut.** Two CRs: this one (the protocol, both bindings, the push, the key, the web client
   ported), then `web-client-out` (the move and `--ui`)? *Recommended: yes, two (§13).*
   Alternatives: one CR; three (HTTP binding, then the WebSocket, then the move).
2. **The message shape.** One JSON envelope (`hello`, `call`, `sub`, `result`, `event`, `tick`) on
   both transports, with today's route answers unchanged as each op's `data`? *Recommended: yes
   (§5).* Alternative: redesign the payloads as resources now (every view rewritten).
3. **What a push carries.** The topic's whole value at each change (no diff), and a new `events`
   topic for the journal's typed lines with a `seq` cursor? *Recommended: yes (§5.3, §5.5).*
   Alternatives: diffs (smaller frames, a client wrong after a lost one); a bare "changed" notice
   the client rereads (one more round trip per change).
4. **Versions.** Protocol 1 changes only by addition; a breaking change is protocol 2 under
   `/api/v2/`, and the server of this CR speaks protocol 1 only, a client of another getting a
   clear refusal? *Recommended: yes; whether a later server keeps protocol 1 beside 2 is that
   CR's question (§6.1).* Alternative: commit now to serving the previous protocol for one
   release (a native app would survive one upgrade).
5. **Schemas.** `protocol.json` gives the frames and every op's and topic's arguments; the results
   are documented by fields and example in `docs/server-api.md`, not by schema? *Recommended: yes
   (§5.7).* Alternative: a schema for every result now (every payload of the board frozen as a
   model, a much larger CR).
6. **The degraded HTTP mode.** The same ops at `POST /api/v1/call/<op>`, and a stateless long-poll
   (`POST /api/v1/poll`, held up to 20 s) for the push? *Recommended: yes (§6.2).*
   Alternatives: Server-Sent Events (one-way push, but some proxies buffer them); plain polling
   every 5 s as today (simple, slower, more reads).
7. **The key on both bindings, and other origins.** Cookie only from the server's own origin;
   the `X-Chantier-Board-Key` header or `hello.key` from anywhere; CORS open for header-key
   requests (no credentials), so a UI hosted elsewhere works? *Recommended: yes (§7).*
   Alternative: no CORS (other UIs only as native apps, scripts, or served by this server with
   `--ui`).
8. **Behind a proxy.** The server stays plain HTTP (TLS at the proxy), accepts `X-Forwarded-Host`
   and an `https` origin for the cookie's origin check, and makes the key exchange's redirect
   relative so a path prefix works? *Recommended: yes (§7.5).* Alternative: TLS in the server
   (a certificate to make and keep: a setup step the plugin avoids).
9. **Where the web UI goes.** `chantier/clients/web/`, still in the one wheel, served by the
   server by default, with `board --ui <folder>|none`? *Recommended: yes (§8.3).* Alternatives:
   a top-level `clients/web/` folder of the repository (outside the Python package: an editable
   install would not ship it without more packaging); a separate repository or package that the
   user hosts (a setup step, against "no setup").
10. **A build step.** None: the web client stays hand-written ES modules with no framework?
    *Recommended: yes (CONTRIBUTING.md's rule; §8.3).* Alternative: a bundler and a framework (a
    Node toolchain to install, against "uv is the only tool").
11. **Clients shipped and tested.** The web client and the CLI's own probe and seat call; no SDK;
    the doc's two short examples? *Recommended: yes (§8.4).* Alternative: a Python client module
    (`chantier.client`) shipped and tested, for scripts.
12. **The WebSocket library.** `websockets` (uvicorn's WebSocket protocol, and the sync client the
    tests and scenario use)? *Recommended: yes (§9.1).* Alternative: `wsproto` (pure Python, no
    client: the tests would need a hand-written one, against the dependency rule).
13. **The command's name.** Keep `chantier board` (the cards, docs and hosts name it)? *Recommended:
    yes.* Alternative: `chantier server`, in a CR of its own (every card and doc that names it).
14. **The old routes.** Removed in this CR (only the web client and the same-version CLI call them),
    `GET /api/board` kept forever as the probe with its identity fields only? *Recommended: yes
    (§6.4).* Alternative: keep the old routes for one release (a user's script survives one
    upgrade; two APIs to test meanwhile).
15. **The degraded mode on screen.** The web client's footer adds " (HTTP)" in HTTP mode and
    nothing in live mode, so the pictures do not change? *Recommended: yes (§8.1).* Alternative:
    a visible marker in both modes (every picture retaken).
16. **AGENTS.md.** The edits of §11.2 (the server's API and its key; the PRs read "while a client
    asks"; the configuration save from any client; the no-setup sentence; Part 2's path)?
    *Recommended: yes, approved by the PR's merge as usual.*
