# CR-406 investigation (round 0)

Worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-29-CR-406`, base 98413181. Read-only. Paths
below are under `skills/chantier/scripts/cli/` (`src/chantier/board/` = `B/`, `tests/` = `T/`) unless
rooted. `$CHANTIER rules` read: AGENTS.md (CLI scope, "A change under board/web/ reads DESIGN.md first",
`just check` + `just eval-dry-run` for `src/` changes, scenario gate), CONTRIBUTING.md, scenario/README.md.

## 1. What the worktree holds (spec section 15 seams, as they stand)

- `B/routes.py` (214 lines): `ROUTES` = list of `(verb, regex, handler(ctx, req, *groups) -> Reply)`;
  `handle -> _judged` (k exchange, `guard.authorised`, `ALLOWED`, `guard.refusal` on POST/PUT, `_dispatch`,
  then `ctx.seats.gone() -> ctx.stop()` after every request, so seats are checked per request: keep that
  call in the new HTTP path and in the ws call path). `X-Chantier-Now` set in `handle`.
  `_state_of(ctx, project, ask)` is the one place for state + fingerprint + `Live.ask`; it is what
  `project`/`costs` topics must call (with `ask=True`, per spec 5.3). `board()` builds the whole payload.
- `B/write_api.py` (336): write ops are `(repo, data: dict) -> (body, status)` (`_new`, `_move`, `_labels`,
  `_group`, `_ungroup`, `_file`, `_next_batch`, `_rescan`), wrapped by `_write(ctx, req, project_id, op,
  command)`, which does project lookup (404), content-type 415, `json.loads`, `replace(project.repo,
  command=...)`, ChantierError -> status map (`STATUS`, `stale: true` on EXIT_CONFLICT), OSError -> 500.
  `_text`/`_texts` are the hand-written checks the spec replaces by pydantic models (messages: "'x' is a
  string of the JSON body", "'items' is a list of slugs..."): tests assert on some of them, keep the 400 and
  naming. `journal_of` (GET journal) lives here too. `P` prefix regex is shared with `config_api`.
- `B/config_api.py` (165): `config_of` (GET) and `_put(repo, data)` through `write_api.writer(_put, "board
  config")`. `_put` checks `base_sha256`/`dry_run` itself; `changes` is checked in `edit.edit_surface_file`.
- `B/writer_api.py` (35): `payload(ctx)` and `sync(ctx, req)`; `sync` takes `req` but never reads it;
  409 body is `{"error", "code": "off", "writer"}` (this is "C.8's text"; note it has no `ok`).
- `B/guard.py` (60): `exchange` (303 with an ABSOLUTE-path `Location`, `quote(req.path)` + query: spec 7.5
  wants it relative `./...`), `authorised` (header OR cookie, no source), `refusal` (403 site/origin, 415;
  origin compared to `http://{host}` only: needs `https` + `X-Forwarded-Host` for 7.2), `ALLOWED`, `WRITE`.
  `address.py` imports `guard.NEEDS_KEY` and `key.HEADER` (keep both names).
- `B/key.py`: `KeyFile.current()` is cheap (one stat), so the push loop can call it each pass to close
  ws sockets that used the old key (4401). `HEADER = "x-chantier-board-key"` (lower case; spec 7.1 uses
  mixed case on the wire: HTTP is case-insensitive, `Request.headers` is lower-cased).
- `B/app.py` (56): one catch-all `Route("/{rest:path}", endpoint, methods=METHODS)`; lazy starlette imports
  inside `build_app`; `make_server` passes `ws="none"`, `lifespan="off"`. The `Request` dataclass
  (`B/context.py`) has no `client`/scheme; a ws handler needs the same `headers` dict: build a `Request` for the
  upgrade (method GET, path `/api/v1/ws`) and judge it with the same auth function.
- `B/command.py` `_run`: `ctx = Context(...)`, `box.append(make_server(ctx))`, `HubThread(HubLoop(home),
  stop)`, `_start_writer`, `box[0].run(sockets=[sock])`; the `finally` stops writer, hub, closes `sock`. The
  `stop()` closure only sets `should_exit`. A PushThread goes beside `hub` with the same `(loop, on_death)` shape.
- `hub/loop.py`+`hub/times.py`: the seam to copy (`HubLoop.poll(now)`, `HubThread`, `CHANTIER_HUB_TEST_TIMES`
  parsed `a:b`, ignored when not both > 0). `board/times.py` (132) is an unrelated time-words module.
- `B/fingerprint.py`: `fingerprint(changes, extra)` already includes `forge-journal.jsonl` and
  `board-journal.jsonl` by stat (SINGLE), so a `project` rev moves on every journal line too (fine; a journal
  append moves `project`, `journal` and `events` revs together).
- `B/costs.py`: `Live.mark()`, `Live.ask(running)` (5 min rule), `Live.snapshot()`.
- `B/prs.py`: `ForgeReads.get(key, links, load)` keeps a read `TTL_S` (10 s) per key; `answer(...)` includes
  `now` and `all_done`. NOTE: `ForgeReads` re-reads after the TTL even when every PR is done, because the
  "stop when all done" rule is in the page's JS (`views/prs-feed.js`, `tick`). The push loop must carry that
  rule itself: keep per (project, batch) the last answer's `all_done` and not call `answer` again while it is
  true and the PR links (from `project.state`) are unchanged (spec 5.3 "none once every PR is merged or closed,
  until a PR joins"). A closed batch (`answer.closed`) is also read once (JS: `feed.once`): same rule.
- `hub/journal.py`: `read(changes)` returns `(entries, bad, later, unknown)`, entries with effective
  `type/source/audience`; `last_seq(entries)`; file `forge-journal.jsonl`; `append(repo, events, source)`.
  The `events` topic is a thin filter over `read` (seq > after, first 200, oldest first). An entry may have no
  `seq` (old v1 lines): filter with `type(e.get("seq")) is int`.
- `hub/schemas.json` precedent: `hub/schemas.py` models + shipped JSON + `scripts/journal_schemas.py`
  (`just journal-schemas`) + `T/test_event_types.py`. Copy the pattern for `board/api/protocol.json`
  (a recipe is not asked by the spec; a test that fails on drift is, so a tiny script or a documented
  one-liner in the test's failure text is enough; prefer the script, same as `journal_schemas.py`).

## 2. Dependency and uvicorn

- `uv.lock` has NO `websockets` (and no `wsproto`): `pyproject.toml` deps are pydantic, ruamel.yaml, psutil,
  starlette 1.10.0, uvicorn 0.54.0 (h11, click only). Add `websockets==<pin>` to `[project] dependencies`,
  run `uv lock` (network once), add `"websockets"` to ruff `banned-module-level-imports` (line 58 of
  pyproject; `T/test_board.py` `LAZY = ("starlette", "uvicorn")` gets it too, plus the new `board/api/*`
  module names in `MODULES`). uvicorn 0.54's own extra says `websockets>=13.0`: pin a version meeting it.
  The Driver's machine needs network for `uv lock`; `--locked` everywhere else.
- `uvicorn.config.WS_PROTOCOLS` keys: `auto, none, websockets, websockets-sansio, wsproto`. The `websockets`
  key is the legacy implementation (it imports `websockets.legacy`, raises `UvicornDeprecationWarning`): take
  `ws="websockets-sansio"` (not `auto`: `auto` picks by what is importable, a look-alike choice). Both
  advertise the ASGI extension `websocket.http.response`, so Starlette's `WebSocket.send_denial_response`
  gives the 401/503 refusals of spec 5.6 with no socket opened (call it before `accept`).
- uvicorn `Config` already has `ws_max_size` (set 4 MiB: gives close 1009), `ws_ping_interval=20`,
  `ws_ping_timeout=20` (defaults equal the spec): set them explicitly in `make_server`.
- RISK, shutdown: with `lifespan="off"` and sansio impl, uvicorn's `shutdown()` sends close 1012 to every
  socket (read in `websockets_sansio_impl.py` line 186). The spec wants 1001, sent by the server before
  `should_exit`. The `stop()` closure covers seats-gone and hub-death. Ctrl-C does NOT pass through `stop()`:
  uvicorn's signal handler (`Server.handle_exit`) sets `should_exit` itself, and `_run` only sees
  `KeyboardInterrupt` after the run. To get 1001 on Ctrl-C too, `make_server` should return a small
  `uvicorn.Server` subclass (defined inside the function, lazy import) whose `handle_exit` closes the
  sockets first, then calls `super()`. The test "through `_run`'s stop path" only needs `stop()`; the
  Ctrl-C case is by hand. Closing from a non-loop thread: keep the event loop in a holder on the ctx
  (set by the ws endpoint when the first socket opens) and use `asyncio.run_coroutine_threadsafe`.

## 3. Turning routes into ops with checked args

Smallest shape (all new code in `B/api/`, old route modules shrunk, not duplicated):

- `protocol.py`: pydantic models, `ConfigDict(extra="forbid", frozen=True)`, one per frame and one per op
  args (`ProjectArgs(project)`, `ProjectPathArgs`, `StateArgs(project, rev=None)`, `PrsArgs(project, batch=None)`,
  `SeatArgs(project, session)`, `NewArgs(project, text, slug=None, title=None)`, `MoveArgs` (items XOR group,
  `to` Literal over `write_api.COLUMNS`), `LabelsArgs(project, items, add: list[str]|str)`, `GroupArgs`,
  `UngroupArgs`, `FileArgs(project, item, path, text, base_sha256)`, `NextBatchArgs(project)`,
  `ConfigPutArgs(project, changes: list[dict]|Any, base_sha256: str|None, dry_run: bool=False)`, empty args for
  `board.get`/`writer.sync`). A `ValidationError` becomes 400 with the field name (`e.errors()[0]["loc"]`).
  Do not tighten `changes` beyond what `edit.edit_surface_file` already checks (the web client sends exactly today's
  body; spec 14: no payload change). `MoveArgs` XOR is a `model_validator` (today: `"group" in data` wins).
- `ops.py`: `Op = (ctx, args_model) -> Result(status, data)`, with `Result` a plain dataclass; a table
  `OPS: dict[str, (ArgsModel, handler, writes: bool)]`. Handlers become today's functions minus `Request`:
  - read routes (`routes.state/tree/file/costs_of/prs_of/board`): return `data` dicts instead of `Reply`.
    `files.tree` and `files.read` return `Reply` today: refactor them to return data / raise a small error
    (404) and keep `files.read`'s bytes path for the HTTP `GET .../file` of 6.3; `project.file` in ops needs
    `files.kind_of == "text"` else 415 "binary: read it over HTTP", cut/sha256 as `data` (the `Reply` headers
    `X-Chantier-Cut` / `X-Chantier-Sha256` become fields).
  - writes: `write_api._write` splits in two: the checking/lookup (`project = _project(...)`, 404) moves to the op
    layer; the `try/except ChantierError/OSError` and the `replace(repo, command=...)` stay in one shared function
    returning `(body, status)`. The `op(repo, data)` functions can keep taking a dict (`args.model_dump()` minus
    `project`), which keeps `write_api`'s 336 lines and every existing assertion nearly intact; do that, rather than
    rewriting each op around the model.
  - `seats.register`: `routes.seats` today defaults `project` to `ctx.projects.home_id` and returns 404 if
    unknown; keep `project` optional there (the CLI's `register_seat` always sends it).
  - `project.state` with `rev`: `rev` = fingerprint (what `_etag` hashes now, 32 chars of `print_`): use the full
    fingerprint as rev, `{"changed": false, "rev"}` when equal, else state plus `rev` and `now`. `_state_of`
    returns `(data, print_)` already.
  - `writer.sync`: 409 data keeps `{"error", "code", "writer"}`; the frame's `error` text = `data.error`.
  - the HTTP status for not-writable cases is unchanged (`STATUS`).
- `topics.py`: `TOPICS: name -> (ArgsModel, rev(ctx, args), value(ctx, args))`. `project` rev = `_state_of`
  print (call with `ask=True` as in spec 5.3); `costs` rev = `f"{live.mark()}|{print}"`; `prs` rev = sha256 of
  the answer minus `now`; `journal` rev = stat size+mtime of `board-journal.jsonl`; `board` rev = hash of
  `json.dumps([lines, seats, writer])` (project_line + project_paths, the `lines()` of `refresh.js` shows what the
  client compares: projects and writer; spec adds seats). `events` is stateful per subscription (cursor): keep the
  cursor in the subscription record, not in the topic table. `board.get`'s `now` and `local_url` must not be in the
  rev (so not in the hash).
- `push.py`: `PushLoop.poll(now)` over a registry `{(topic, frozen args): [subscriber, ...]}` with
  `subscribe/unsubscribe`, subscribers being a callback `(event dict)`; ws registers a callback that
  `loop.call_soon_threadsafe`s a queue put; a long-poll registers a one-shot waiter (`threading.Event`) and the loop
  sets it. One value computation per topic+args per pass, shared (test claim: "two clients cost one computation").
  Because the HTTP poll is stateless, `poll` requests could also compute inline: but spec 6.2 says the `prs` read
  rule counts a poll's sub as watching, so a poll should register for its hold and wait on the loop (reuses the same
  throttle). `PushThread`: copy `HubThread` (daemon, `wait(poll_s)`, `on_death`), `stop()` in `_run`'s finally.
- `times.py`: copy `hub/times.py`; env `CHANTIER_API_TEST_TIMES=<push>:<hold>:<tick>:<hello>`, four floats all > 0.
- `ws.py`: Starlette `WebSocket` endpoint; `hello` within `HELLO_S` via `asyncio.wait_for(receive_text)`;
  counters for the 64/16 limits live on the ctx (needs a lock or only touched in the loop thread: the ws code runs
  in the event loop, so a plain int is fine); calls via `run_in_threadpool(ops.run, ...)`; `tick` task per socket.
  Subscriber callback must not block the push thread.
- `http.py`: `POST /api/v1/call/<op>`, `POST /api/v1/poll`, `GET /api/v1/projects/<id>/file`, `OPTIONS`, plus
  the probe. `routes.handle` keeps the key/method gate and dispatches `/api/v1/` and `/api/board` here before the
  static files; any other `/api/` -> existing `_unknown()` 404. `poll` holds up to 20 s: run it in the thread pool
  (starlette's default pool is 40 threads: 32 subs x many pollers hold threads; an `asyncio` wait on the push loop's
  event would be cheaper, decide in round 2; with `HOLD_S` shortened by the test seam).
- `auth.py` (from `guard.py`): `authorised(req, key) -> "header"|"cookie"|None`; cookie path adds the 7.2 rule for
  `/api/v1/` and the upgrade only (`Sec-Fetch-Site`, `Origin` against `Host` or `X-Forwarded-Host`, http and
  https); `refusal` applies to the cookie only; CORS headers on every `/api/v1/` answer (via `Reply.headers`);
  `ALLOWED` gains `OPTIONS` for `/api/v1/` only. `GET /` and statics keep today's cookie check. Today `guard.refusal`
  also checks `origin` against `http://{host}` only: extend to https in the cookie branch.
- Probe: `GET /api/board` frozen at `{"board": true, "version", "pid", "served", "surface", "protocols": [1]}`.
  `address.probe` only needs `board`; `command._recorded/_answering` read `served`, `version`, `pid`. Existing
  tests that read `routes.board(...)`'s other fields (`T/test_board.py` line 150, `T/test_writer_commands.py`
  lines 203-214) move to `board.get`.
- `address.register_seat`: `_call(base, key, "POST", "/api/v1/call/seats.register", {"project", "session"})`;
  `_call` already sends the header key and `Content-Type: application/json`. Answer shape changes
  (`{"ok", "status", "data", ...}`): it only checks no exception today; with a 4xx `urlopen` raises `HTTPError`
  (an `OSError`), so it still returns False.

## 4. The web client (`B/web/js/`)

Files (lines): `core/api.js` 95, `core/refresh.js` 85, `core/store.js` 57, `core/router.js` 174, `main.js`
(boot reads `board()` itself at line 156, retry loop), `api/backlog.js` 50, `api/config.js` 13. Max 300 lines per
file, 50 per function, no global, relative addresses, no `innerHTML` outside `core/dom.js`, i18n in `en*`+`fr*`.
`DESIGN.md` is read first (no token change planned).

Who calls the server today (all through `core/api.js` except one):
- `api.js`: `get` (ETag), `board`, `projectState(id, etag)`, `costs`, `prs`, `tree`, `fileText`, `fileUrl`,
  `post`, `recompute`, `send`, `route(id, path)` (route builder, used by `api/backlog.js`, `api/config.js`).
- `api/backlog.js`: `write(method, project, path, body)` over `send(method, route(...), body)`; paths
  `backlog/new|move|labels|group|ungroup|file|next-batch`, `journal/rescan`, `journal` (GET, `get`).
  `api/config.js`: `config` GET and PUT.
- `ui/writer-events.js` line 9: `const SYNC = 'api/writer/sync'`, `post(SYNC, {})`: must become an op call.
- `views/costs-action.js`: `costs`, `projectState(project, null)` (uses `.etag`), `recompute`.
- `views/prs-feed.js`: `prs` every 10 s with its own tick/`subscribe`; becomes a `prs` subscription, but keeps the
  `failed(last, error)` keep-last-good behaviour (the `update({prs: ...})` and `.closed/.all_done` logic can stay
  server-side; the client no longer needs its 10 s timer).
- `panel/load.js`: `fileText`, `tree`; `panel/file-view.js`: `fileUrl` (stays a URL, now `api/v1/projects/<id>/file?path=`).
- `core/refresh.js`: `board`/`projectState` with etag on a 5 s timer, `reload()` after writes (used by `edit/new-idea.js`,
  `triage/actions.js`, `ui/sidebar.js` imports `unreachable`).
- `main.js` boot: `board()` call: replace by the first `board` event or one `board.get`.
- `views/costs-image.js:29`: `fetch(new URL(path, document.baseURI))` of CSS/fonts: stays (spec 8.1).
- store fields to feed: `heard` (device ms), `fails`, `denied`, `now`/`minute`, `etag` (now `rev`), `data`, `board`, `prs`.
  `ui/sidebar.js` `heard()` gains " (HTTP)": new i18n key in `en-board.js` and `fr-board.js` (also the "board was
  upgraded, reload" key, and any `foot.*` ones; the i18n test in `T/test_board.py`/`test_board_design.py` checks
  every key exists in every language file, so add to `en` and `fr` both).
- New `core/transport.js`: `call`, `subscribe`, `fileUrl`, state (`mode`, `heard`, `fails`, `denied`). Needs splitting to
  stay under 300 lines and 50 per function: suggest `transport.js` (public API, state), `ws-link.js` (socket,
  hello, reconnect backoff 1,2,4,8,16,30 s), `http-link.js` (long-poll loop). BUT spec 10.1's
  `test_server_protocol.py` says no JS file but `js/core/transport.js` may contain `WebSocket(` or an `api/` address:
  so either keep the socket and the `api/` strings in `transport.js` (tight against 300 lines) or change that
  test sentence and name the sibling files; this is a spec ambiguity to resolve in the Driver's call (it is
  testing wording, not user-visible): proposal below in section 8.
- `?transport=http`: `router.js` already keeps `lang` across navigation; add `transport` the same way (line-level
  edit; router.js is 174 lines).
- Uses `heard` fed from every frame including `tick`; the `writer-tick.js` local clock (`now` + 5 s) is separate and
  can stay, `tick`'s `now` can replace its guess.
- `CONTRIBUTING.md` ("The board's page", line ~367 area) holds the rule "only `js/core/api.js` calls fetch": update
  with the new wording of spec 11.3.

## 5. Old `/api/` callers: every one to change (file:line at this head)

Spec line numbers drifted (spec: forge_hub 1952/1979, external_surface 9204-9214, surface_config_page 8890-8916).

Tests (`T/` = `skills/chantier/scripts/cli/tests/`):
- `T/test_board.py:150` `routes.board(ctx, Request("GET","/api/board"...))` (reads full payload: use `board.get`);
  `MODULES` list lines 31-52 (add `api` modules; drop none unless removed) and `LAZY` line 53.
- `T/test_board_config.py:15,46-47` `routes.handle(... f"/api/projects/{id}/config")` PUT/GET, also `config_api._event`
  monkeypatch at 224-225 (keep `_event` name or update).
- `T/test_board_journal.py:48-49` `.../{route}` for backlog and journal routes (several cases).
- `T/test_board_prs.py:1,68`, `T/test_board_prs_batches.py:44-45`: `GET .../prs` through `routes.handle` (2 files, many cases).
- `T/test_store_command_table.py:169-170`: `.../{route}` backlog writes against a command table (the `call` helper).
- `T/test_writer_commands.py:197-214`: `GET /api/board`, `POST /api/writer/sync` (key/no key/off/409), `GET /api/autosync` (404).
- Not routes but affected: `T/test_surface_server.py`, `T/test_writer_edges.py:230` (`monkeypatch command.make_server`), `T/test_board_running.py`.
  Check each at the head of the coder round; they do not call `/api/` strings.
- Structure tests that read web files: `test_board_design.py`, `test_code_targets.py` (300-line, nesting), i18n in `test_board.py`.

Scenario (`scenario/run_scenario.py`, 10287 lines; unit `surface-board` budget is 700 at line 116-121, not 500 as the spec says):
- `settled_live` 1561-1565 (`GET .../costs`): used by `remote_board` at 2689 and 2771.
- `board_prs` 1713-1790+ (line 1717 route, 1761 `.../state`): called from `remote_board` 2793; read PRs through `prs.get`.
- `forge_hub` 2053 (`GET .../demo/prs`) and 2080 (`POST .../backlog/new`).
- `remote_board` 2557-~2900: 2620-2622 (401 on `/`, `/api/board`, static, `/api/projects/x/file`), 2646, 2681-2688 (`/api/board`,
  `/api/autosync` 404), 2690-2745 (`state`, ETag/If-None-Match 304 cases at ~2725-2733: become `rev`/`changed:false`;
  the ETag checks stay as rev checks), `tree`, `file` (text, image, 404 for escapes), costs recompute 202, 403 foreign Origin at
  2784, 405 `PUT /api/board` at 2785, 2808-2854 (seats count through `/api/board`: now `board.get`, the probe has no `seats`),
  2881 (`tapi` from `/api/board`).
- `surface_config_page` 9205, 9211, 9235 (GET/PUT config, `save` helper).
- `external_surface` 9533-9548 (`/api/board` PID, `state`, `tree`, `file` refusals).
- `surface_server`: seat registration by second `board --seat` (no literal `/api/` line; through the CLI): proves
  `register_seat` works.
- `scenario/README.md:297,298,307` name old routes (`/api/autosync`, `/api/board`, `GET /api/projects/<id>/prs`): Coverage list
  lines to reword, each new check named with its test (`test_scenario_coverage.py` reads it).
- The scenario runs through `just scenario` = `uv run --locked python scenario/run_scenario.py`: `websockets` will be importable
  once it is in the project dependencies (the runner is not a PEP 723 script). `urllib`/`http.client` already used.

Other:
- `scripts/docs_screenshots.py:183` `ctx.route("**/api/board*", fix_surface_path)` (function at 152-165). It is a PEP 723 script
  (`uv run --script`, deps `playwright>=1.49`, own env, starts the real `chantier board` as a subprocess), so it has no
  `websockets` of its own and needs none: use `ctx.route_web_socket("**/api/v1/ws", handler)` (Playwright 1.48+) to proxy
  frames (`ws.connect_to_server()`, `on_message` rewriting `board.get` results and `board` events), and `ctx.route("**/api/v1/call/board.get")`
  for HTTP. Because `route_web_socket` frames cannot be matched to an op without tracking `id`s, keep a dict of call ids
  whose op is `board.get`. The 7 fields to rewrite: `served`, `served_origin`, each project's `repo_path` and `origin`.
- Cards: `session-start.md:78`, `hosts/claude-code.md:48,54`, `hosts/copilot.md:42,46` name `GET /api/board`: stay true.
  Re-search `board/web` in cards at the head (spec 11.1).
- `evals/kit/sandbox-*/json-api` hits are an unrelated fixture project.

## 6. Risks beyond the spec

1. Shutdown close code on Ctrl-C (section 2); on Windows `should_exit` from the signal handler.
2. `prs` rule "none once all done" lives in JS today and must move to the push loop (section 1).
3. `prs.answer` appends journal lines (`merged`): running it in the push loop thread is a write from a non-request thread;
   fine (same `forge_journal.append`) but the hub also reads: tests for "no second line" (scenario `forge_hub` step 6) must hold.
4. Per-request `ctx.seats.gone() -> ctx.stop()` side effect: a pure ws client sending no HTTP request never triggers it; the
   seats' own thread (`_loop`) covers it, as spec 5.3 says. A test is not needed.
5. `Context` (`B/context.py`) gains the push registry, the ws counters and the loop holder: all tests build `Context(projects, key, seats,
   "t", lambda: None)` positionally (5 sites); give new fields defaults.
6. `requests` held in the thread pool: starlette's anyio pool is 40 threads; 32-sub long-polls hold a thread each for 20 s. Prefer an
   `asyncio` wait on a `threading.Event` set via `to_thread`... or an `asyncio.Event` set by the push thread through the loop. Decide
   at round 2; a note in `docs/server-api.md` of the limit if kept simple.
7. `HEAD`/304 handling in `app.py` (`NOT_MODIFIED`): the new HTTP replies never use 304; keep it for statics.
8. 413 and 415 statuses: body size cap on `POST /api/v1/call` (4 MiB) is not in `app.py` today: add where the body is read.
9. Hash cost: `board` rev hash and `fingerprint` run every 2 s per watched topic; `fingerprint` is a stat walk of the whole planning
   folder: with 3 clients on 3 projects that is 3 walks per pass, cached by (topic, args). Memoise `_state_of` per pass.
10. Python 3.15 in the worktree's fresh `.venv` (created by my first `uv run`, not synced; `.venv` is ignored by git, no change
    in the tree): the Driver runs `uv sync --locked` itself.
11. Spec drift: unit budget 700 s (not 500), `board.json`/seat names fine, and `GET /api/board` today also serves `seats`: the scenario's
    seat counting (2808-2854) must read `board.get` over HTTP.

## 7. Questions only the user can answer

None. Two spec ambiguities the Driver can settle itself (no user question): (a) section 10.1's "no JS file but `transport.js` names an
`api/` address" vs the 300-line cap: allow the socket, the HTTP link and the address strings in `transport.js` plus `ws-link.js`/`http-link.js`
only if the test's allow-list names exactly those three, and say so in the PR; (b) `board.get`'s `rev` hash covers seats.

## 8. Evidence plan

Kind of change: CLI server + web client behaviour (user-visible: live updates, footer text) + docs + rules. Screenshots owed? No (no `hooks/` pane).

| Claim | Proof | Technique |
| --- | --- | --- |
| Every op returns what its old route did, bad args 400, unknown 404, `{"changed": false}` | `test_server_api.py` parametrized over `OPS`; old tests' cases moved, none dropped | pytest in-process, `ops.call(ctx, name, args)` |
| Topics, one event, change = new rev, one computation for 2 clients, `events` cursor, `prs` read once per 10 s (fake reader, injected clock), none when all done | `test_server_api.py` | `PushLoop.poll(now)` with fake clock, no sleep |
| Long-poll answers at once / at HOLD_S / on change | `test_server_api.py` | `CHANTIER_API_TEST_TIMES` via monkeypatch |
| Key matrix, CORS, relative `Location`, probe fields | `test_server_api.py` + `test_server_api_ws.py` | pytest; real server port 0 for the upgrade cases |
| WS handshake, 4401/4408/4426, 429, 503 on 17th, 1001 on stop | `test_server_api_ws.py` | `websockets.sync.client`, one server per module, under 2 s |
| Schema = shipped `protocol.json`; JS uses only published ops/topics, no stray `WebSocket(`/`api/` | `test_server_protocol.py` | pytest reading repo files |
| Real board process: WS with cookie, `chantier file` triggers event within PUSH_EVERY_S + 2 s, `backlog.move` over WS writes one `board` line seen via `events`, HTTP binding, long-poll, foreign-origin 401, old route 404, probe fields, 1001 on stop | scenario unit `surface-board`, case `remote_board` (rewritten) + the 4 moved cases (forge_hub, external_surface, surface_config_page, surface_server) | `just scenario --unit surface-board` (GitHub), then full `just scenario`; Windows local `chantier gate` for the stack top; set `CHANTIER_API_TEST_TIMES=1:3:1:2` for the unit |
| `grep '/api/' scenario/run_scenario.py` has only `/api/board` left (and `/api/v1/`) | command output saved in `evidence/` | `rg` |
| Pictures unchanged | `just docs-screenshots` at base and at head on the same machine, PNG hashes compared | `scripts/docs_screenshots.py` (edited), `git status docs/web-board` empty or each diff named |
| Browser: live mode (Data line moving, second tab shows a Triage move within 3 s), `?transport=http` (" (HTTP)", same move within HOLD_S), console shows socket opened under CSP, one other-origin check | by hand | Playwright script run by the Driver (the project has Playwright via `docs_screenshots`); capture console log and 2 screenshots into `evidence/` |
| Phone on LAN | by hand | cannot be shown by the Driver unless the user is there: Known gap "no check on a phone" |
| Other-origin UI | by hand | `python -m http.server` on another port + Chromium; else Known gap "UI from another origin: unproved in a real browser" |
| `just test` time within +3 s of base | `just test` timing at base (`98413181`) and head, same machine | `time just test`, logged in `work/gates/` |
| `just check`, `just eval-dry-run`, `just scenario` | gate logs | `chantier gate` |

Not provable here: a real nginx/Caddy proxy; a TLS/https origin end to end (covered only by header unit cases).

## 9. Suggested coder rounds (3, each green on `just check`, the board works at the end of each)

**Round 1 - the protocol and the server's HTTP side, old routes kept until the client moves** (Python only; no JS yet).
`websockets` pin + `uv lock`, ruff ban, `T/test_board.py` LAZY/MODULES. `board/api/protocol.py`, `protocol.json`, `times.py`, `ops.py`,
`topics.py`, `auth.py`, `http.py` (`/api/v1/call/<op>`, `/api/v1/poll`, file GET, OPTIONS), `push.py` (loop + thread, started in `command._run`),
`routes.handle` dispatching `/api/v1/` first; the old `ROUTES` stay registered in this round only so the existing web client and scenario
still pass (an explicit, temporary, deliberate state named in the round's note; the old routes are deleted in round 3). Probe frozen at
its final shape now (add `protocols`; keep the other fields on `board.get`, and until round 3 also on `/api/board`? NO: keep
`/api/board` full in round 1 and cut in round 3 together with the client move; the probe readers only need the four identity fields).
`guard.exchange` relative `Location`. `address.register_seat` -> `/api/v1/call/seats.register`. Tests: `test_server_api.py` (all but the ws
and pages), `test_server_protocol.py` (schema half). Evidence: pytest, `just check`, `just eval-dry-run`.

**Round 2 - the WebSocket binding and the scenario** (Python + scenario). `ws.py`, `app.py` (`ws="websockets-sansio"`, route
`/api/v1/ws` before the catch-all, `make_server` subclass for 1001, size/ping config), the `_run` ordering, `Context` fields. Tests:
`test_server_api_ws.py`. Scenario: add the new `remote_board` ws/http steps against the new paths while the old routes still exist; do NOT
yet move the cases that call old routes (they stay green). Docs started: `docs/server-api.md`. Evidence: pytest, `just scenario --unit surface-board`,
`just check`.

**Round 3 - the web client, removal of the old routes, the rest of the scenario, docs and rules.** `core/transport.js` (+ siblings),
`api.js` over `call`, `refresh.js`, `prs-feed.js`, `costs-action.js`, `writer-events.js`, `sidebar.js` (" (HTTP)"), `router.js` (`transport`),
i18n en/fr, `main.js` boot; delete `routes.ROUTES`, `write_api.ROUTES`, `config_api.ROUTES`, `writer_api.ROUTES`, cut `/api/board` to the
probe; the old route tests moved to ops (`test_board*.py`, `test_store_command_table.py`, `test_writer_commands.py`);
`test_server_protocol.py` JS half; scenario: move `forge_hub`, `external_surface`, `surface_config_page`, `remote_board`'s old checks, README Coverage;
`scripts/docs_screenshots.py`; `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `docs/web-board.md`, `docs/boards.md`, release notes; by-hand
Chromium/phone checks; `just docs-screenshots` base vs head. Evidence: full `just check`, `just eval-dry-run`, `just scenario` (and Windows local),
browser logs and screenshots.

Why this split: round 1 and 2 are server-only and adding (nothing breaks, the old client keeps working), round 3 is the one switch where client,
routes, tests and docs must change together (the structure tests compare the JS to `OPS`/`TOPICS`). If round 3 is too large for one coder, the
lowest-risk cut inside it is: (3a) client + route removal + Python tests + scenario; (3b) docs, rules, release notes, screenshots and by-hand
checks (a doc-only second pass, which needs no `just scenario`).
