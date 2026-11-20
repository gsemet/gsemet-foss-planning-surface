## Summary

The surface server's board speaks through ad-hoc HTTP routes that only its own web page knows, so no other program can read or drive a planning surface, and the page depends on a polling loop. This adds one published API, protocol 1, with one message shape on two transports: a WebSocket (`/api/v1/ws`, with server push) and, as the degraded case behind a proxy that cuts upgrades, plain HTTP (`POST /api/v1/call/<op>` and a long-poll `POST /api/v1/poll`). The web board is now one client of that API (WebSocket by default, `?transport=http` for the degraded mode), and the old ad-hoc routes are gone: `GET /api/board` remains only as the identity probe.

## Deliverables

Where the API sits in the server (new package `board/api/`; the old routes are removed):

```mermaid
flowchart LR
  C1[WebSocket client] --> WS[api/ws.py]
  C2[HTTP client] --> H[api/http.py]
  WS --> A[api/auth.py]
  H --> A
  WS --> OPS[api/ops.py: 20 ops]
  H --> OPS
  OPS --> W[write_api, config_api, writer_api, reads]
  WS --> P[api/push.py: PushLoop]
  H --> P
  P --> T[api/topics.py: 6 topics]
  UI[web board: core/transport.js] --> WS
  UI --> H
  P --> Z[1001 close at shutdown, 4401 on key rotation]
  PR[api/protocol.py -> protocol.json] -.-> WS
  PR -.-> H
```

The wire shape, in one sketch (frames of `protocol.json`):

```text
client: {"t":"hello","protocol":1,"key":"..."}        server: {"t":"welcome", ...}
client: {"t":"call","id":"7","op":"backlog.move","args":{...}}   server: {"t":"result","id":"7","ok":true,"data":{...}}
client: {"t":"sub","id":"8","topic":"board","args":{...}}        server: {"t":"result",...} then {"t":"event","sub":"8","rev":"...","data":{...}}
close codes: 4401 key, 4408 no hello in time, 4426 protocol, 1001 server stopping; 429 over 32 subscriptions, 503 over 16 unwelcomed sockets
```

Choices made: one `call` shape for all 20 ops, with schemas published as `protocol.json` (generated from the models, checked by a test); six topics pushed by one loop that computes each (topic, args) once for all watchers; the `prs` topic reads the forge at most once per 10 s per project and not at all once every PR is done; the cookie is honoured only from the server's own origin, a header key from any origin, and CORS answers `*` without credentials; the key exchange redirects to a relative `Location`.

## Blast radius

Grade: 3. The board's whole wire changes: every page of the web board, the identity probe (`/api/board`, now only its identity fields) and the scenario move to the new API in one PR, and `websockets` becomes a dependency. Rollback is a revert of this PR, with no data migration; programs that read the removed routes break.

## Autonomous decisions

- An extra `http.poll` schema in `protocol.json`, for the long-poll body.
- The seats check also runs on early 401 and 405 answers of `/api/v1/`, so a client that only gets refusals still counts as a seat.
- The two scenario `remote_board` checks on `Location` now expect the relative form the exchange now gives.
- A write with no live writer is refused by the existing 409 path, not a new check.

## Known gaps

- No release-notes entry: they are written at the version PR, a draft is kept in the CR's work folder.
- Pictures: `scripts/docs_screenshots.py` now routes the new API, but it was not run and no picture was retaken; no screenshot of the board from a real browser was taken (UNVERIFIED in a real browser: live updates, the `?transport=http` footer, a UI served from another origin, a phone on the LAN).
- A long-poll holds one worker thread for up to 20 s; the cap is 16 at once (the 17th gets a 429 result).
- `just test` time at base and head is not measured here.

<details>
<summary>Details</summary>

## Changes

- `board/api/`: `protocol.py` (frames, 20 op argument models, 6 topics) and generated `protocol.json`; `ops.py`; `topics.py`; `push.py` (loop, thread, subscriptions, key-rotation close, long-poll cap); `auth.py`; `http.py`; `ws.py`; `times.py`.
- `app.py`: `/api/v1/ws` route, `make_server` with `ws="websockets-sansio"`, 1001 close at shutdown, 413 cap on bodies. `routes.py`, `write_api.py`, `config_api.py`, `writer_api.py`: the old route tables removed; `/api/board` is the probe.
- Web client: `core/transport.js`, `ws-link.js`, `http-link.js`, and `api.js`, `refresh.js`, `prs-feed.js`, `costs-action.js`, `writer-events.js`, `sidebar.js`, `router.js`, `main.js`, i18n en/fr; `board/web/DESIGN.md` has the "One transport" rule.
- Scenario: `remote_board` and the cases that used old routes now call ops; `board_api` checks the API on a real process. `docs/server-api.md` is new; `AGENTS.md`, `CONTRIBUTING.md` and the board docs are updated.
- `websockets` added to `pyproject.toml` and `uv.lock`; `just protocol-schema` regenerates `protocol.json`.

## Impacts

No visual change.

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_server_api.py`, `test_server_api_calls.py` (a good call for each of the 20 ops), `test_server_api_ws.py` (real server), `test_server_protocol.py` (schema and JS structure); old-route tests moved to ops
- [ ] Local gates at the uncommitted round-4 tree over 9841318: `just check` pass (1348 passed, 13 skipped), `just eval-dry-run` pass (18 of 18), `just scenario --unit surface-board` pass (281/281)
- [ ] Evidence: none yet (no picture retaken)
- [ ] Review: not yet approved
- [ ] Verified: not yet
- [ ] CI green: not yet pushed

## Internal references

CR-406 server-api.

</details>
