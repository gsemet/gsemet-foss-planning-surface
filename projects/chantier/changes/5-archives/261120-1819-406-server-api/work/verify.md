# Verify, CR-406 (the server's API over a WebSocket)

Head: daed507b4ff2ec749b016fb6a87db3519a77eb09

Claim 7 judged again at daed507. The other claims are `carried from fea5a03: only docs changed` (`git diff fea5a03b daed507b --stat`: docs/server-api.md only, 5 insertions, 4 deletions). Raw logs of the real-process runs: `work/verifier/real-process-1.log`, `real-process-2.log`, script `probe.py.log` (a throwaway board over a scratch project, `--host 127.0.0.1 --port 0`, removed at the end).

Verdict: VERIFIED at daed507 (claim 7 fixed). Gap, not a failure: 1001 on stop with a real process.

## 1. The 20 ops over HTTP (fea5a03) VERIFIED
- `uv run --locked --group dev pytest -q -n auto skills/chantier/scripts/cli/tests/test_server_api.py .../test_server_api_calls.py .../test_server_api_ws.py .../test_server_protocol.py` -> `39 passed in 5.77s` (17+6+13+3 tests; the names include `test_a_good_call_of_every_op_answers_the_data_its_route_gave_or_the_store_holds`, `test_every_op_refuses_what_its_arguments_do_not_allow`).
- Real process, key in header: `POST /api/v1/call/nope.nope` -> 404 `unknown op 'nope.nope'`; `project.state {"zzz":1}` -> 400 `'project': Field required`; extra arg -> 400 `Extra inputs are not permitted`; `project.state` with equal rev -> 200 `{"changed":false,"rev":...}`; board.get, costs.get, project.tree, journal.get, config.get, prs.get -> 200 (real-process-1.log). Welcome of the WebSocket lists 20 ops.

## 2. WebSocket (fea5a03) VERIFIED, except 1001 on a real process
- Tests above (`test_server_api_ws.py`, 13 passed), incl. `test_a_stopping_server_closes_each_socket_with_1001`, `test_subscriptions_are_limited_to_32_and_waiting_sockets_to_16`.
- Real process, websockets.sync.client (real-process-2.log): `welcome welcome 1 20 ['board','costs','events','journal','project','prs']`; `call result True 200`; `sub` -> `order result event True` (result before event); after `chantier file` an `event` for the `project` topic arrived `event after file in 1.4s`; 34 subs -> `[('x31',429),('x32',429),('x33',429)]` (32 accepted, the 33rd refused); bad key -> `close 4401 key`; hello protocol 2 -> `close 4426 protocol`; no hello -> `close 4408 no hello after 5.0s`; 17th unwelcomed socket (16 opened) -> `InvalidStatus ... HTTP 503`.
- 1001 on stop: NOT captured on a real process (a Windows console process cannot be signalled gracefully from here; `taskkill` without /F did not end it, so it was force-stopped by PID). Proved only by the in-process real-server test named above (passed).

## 3. HTTP binding and long-poll (fea5a03) VERIFIED
- Real process: first `POST /api/v1/poll` answered `poll first 0.03s 200` with the event; 17 polls held with the current rev, one `chantier file` made 2 s later: 16 answered `200` together after the file call returned (4.3 s, the hold is 20 s), the 17th `(429, 0.0)`.
- Tests: `test_the_long_poll_answers_at_once_then_holds_empty`, `test_a_change_during_the_hold_answers_the_long_poll_before_the_hold_ends`, `test_long_polls_held_at_once_are_capped` (passed in the run of claim 1).

## 4. Key matrix (fea5a03) VERIFIED
Real process: no key -> 401; cookie `chantier_board` with no Origin -> 200; header key with `Origin: http://evil.example` -> 200; cookie with that foreign Origin -> 401; response header `access-control-allow-origin: *` and no `allow-credentials`; OPTIONS with no key -> 204 with `access-control-allow-origin: *`.
`curl -si "http://127.0.0.1:<port>/?k=<key>&x=1"` -> `HTTP/1.1 303 See Other`, `location: ./?x=1`, `set-cookie: chantier_board=...; HttpOnly; SameSite=Strict`. Tests: `test_the_key_and_the_origin`, `test_a_write_from_each_cell_of_the_key_matrix`, `test_the_key_in_the_url_goes_to_a_relative_location`.

## 5. Old routes gone, probe reduced (fea5a03) VERIFIED
Real process (real-process-1.log): GET and POST of `/api/projects`, `/api/state`, `/api/projects/x/state`, `/api/seats`, `/api/costs` -> `404 not found`. `GET /api/board` -> fields `['board','pid','protocols','served','surface','version']` only. Test `test_an_old_route_answers_404_even_for_a_post_a_cookie_carries`.

## 6. The web client uses only published ops and topics (fea5a03) VERIFIED
`test_server_protocol.py` (3 passed, in the 39), incl. `test_the_web_client_names_only_published_ops_and_topics_and_opens_no_socket_but_its_link`. `board/web/DESIGN.md` line 42, "One transport", says the page uses `core/transport.js` only and a view names a published op or topic.

## 7. docs/server-api.md matches the behaviour (daed507) VERIFIED
`sed -n 55,66p docs/server-api.md` and `sed -n 165,169p` at daed507: line 61 "1013 the server is busy (a 65th welcomed socket)"; lines 63-64 "A 17th socket still waiting for `hello` gets no close code: the upgrade itself is refused, HTTP 503 `too many clients`"; line 168 "| WebSockets before `hello` | 16 | HTTP 503 at the upgrade |"; line 167 "WebSockets past `welcome` | 64 | close 1013".
Code: `ws.py:149-150` (welcomed >= MAX_CLIENTS -> TRY_AGAIN 1013), `ws.py:304-305` (not welcomed >= MAX_WAITING -> `send_denial_response(... 503)`).
`uv run --no-sync --project . pytest -q -k "waiting_sockets_to_16 or 65th"` -> `2 passed, 1405 deselected in 2.40s`. The real-process 503 for the 17th socket (claim 2) is carried from fea5a03: ws.py is untouched.

## 8. PR description (as posted, carried from fea5a03: only docs changed) VERIFIED
`gh pr view 383` body equals work/pr-body.md (one trailing blank line). Sections render (Summary, Deliverables with mermaid and text sketch, Blast radius, Details fold); no image attached. Summary, Deliverables and Changes match the diff (65 files, `git diff --stat origin/main...HEAD`). Known gaps lists the pictures, the browser/phone/other-origin UNVERIFIED items and the `just test` time. Its wire sketch ("503 over 16 unwelcomed sockets") is right; the docs page is now fixed. The test plan's "Verified" and "CI green" boxes are still open for the Driver to tick. Review box (cites fea5a03; the docs commit daed507 moved the head): `$CHANTIER log` has `r4 approved at 9841318..., committed as fea5a03b (rebased clean on origin/main daec1986)`, which covers `Review: approved at fea5a03`.

## UNVERIFIED (not provable here)
A real browser run of the page, a phone on the LAN, a UI from another origin, the pictures (docs_screenshots not run), `just test` time at base vs head, 1001 on a real process. The first four are in Known gaps already; add 1001-on-a-real-process only if wanted (it is covered by the in-process real-server test).

## 8. Description pass at daed507 (posted body, `gh pr view 383 --json body`) NOT VERIFIED
- Checked and fine: CI `gh pr checks 383` 5 of 5 pass at daed507; `1394 passed, 13 skipped` and `18 of 18` are in work/gates-check.log and gates-evaldry.log (stated at fea5a03); local gate pass at daed507 in the gate log; Review note `r4 approved at 9841318..., committed as fea5a03b`; Known gaps hold the 1001-on-stop gap and `work/coder/release-notes-draft.md` (file exists).
- Failed: the Test plan item "New or changed tests (they fail on the previous code)" is unchecked, names no SHA and no result, and "fail on the previous code" has no proof in verify.md (the 39 passed run is at head, no run at the base).

## 9. Description pass 2 at daed507 (posted body, `gh pr view 383 --json body`) VERIFIED
Head re-checked: `git rev-parse HEAD` -> daed507b4ff2ec749b016fb6a87db3519a77eb09; `git diff --stat fea5a03 daed507` -> docs/server-api.md only.
Test plan "New or changed tests": `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_server_api.py test_server_api_calls.py test_server_api_ws.py test_server_protocol.py -q` -> `39 passed in 10.75s`, as the body states; the body now says the tests were not run against the base code, with its reason, instead of claiming they fail there.
Rest unchanged from claim 8: CI 5 of 5 at daed507, gates, Review note (`r4 approved at 9841318..., committed as fea5a03b`), Known gaps (1001 on stop, pictures, release-notes draft), no image, no role name outside product terms.
