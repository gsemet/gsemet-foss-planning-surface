# Verify CR-457 (two board keys)

Head: 53a134e6e2804387be6ae43ae24b06bab5c836c6

All claims judged at 53a134e (worktree head = pushed head). Method: a real `chantier serve --port 8799
--host 127.0.0.1` started from a scratch git repo (`work/scratch/p`, `chantier init`ed, two inbox items,
no `--seat`, no `--project`), driven over HTTP and WebSocket by a script (`work/scratch/drive.py`,
`two.py`, removed at the end). Keys masked below.

- Start line: output `board on http://127.0.0.1:8799/?k=<KEY> over <scratch>/.agents/changes` then
  `read-only: http://127.0.0.1:8799/?k=<READKEY> (it shows the board and acts on nothing; it can be shared)`.
  A second start printed `board already running at ...?k=<KEY>` then the same `read-only:` line. PASS.
- server.json: `key` and `read_key` both 43 chars, different. PASS.
- Read key: `board.get` 200 `X-Chantier-Access: read`, no private key in the body; `project.state` 200 read;
  `config.get` 200; `project.file` 200; `GET /api/v1/projects/p/file?path=...` 200 read; WebSocket `sub project`
  answers result 200 then an event, `sub board` answers. PASS.
- Read key refusals: `backlog.move` 403 `refused: the read-only key acts on nothing: use the private link`
  (HTTP and WebSocket `result`), `config.put` 403 (both), `backlog.file` 403; `git status --porcelain` in the
  scratch repo stayed empty after them. PASS.
- Private key writes: `backlog.move` to P2 with the private key 200 `X-Chantier-Access: write`;
  git status then showed alpha moved from 1-inbox to 2-backlog/P2. PASS.
- Both keys accepted in header, cookie and `hello`: WS welcome `access: read` / `write` for read key and
  private key, each via hello and via header; HTTP header both; cookie: read cookie -> `read`, private cookie
  -> write. Bad hello -> `error` code `key`; no key / bad key HTTP 401. Static page `/` 200 with either header,
  401 with none. PASS.
- Cookies: exchange of the read link sets `chantier_board_d831a446df4d_read=<READKEY>`; of the private link
  `chantier_board_d831a446df4d=<KEY>` (separate names, each only its own); request with both cookies ->
  `write`, read cookie only -> `read` (and `backlog.move` 403 with it); header read key + private cookie ->
  `write`. PASS.
- CORS: `Access-Control-Expose-Headers: X-Chantier-Access` on an answer to an `Origin: http://other` request. PASS.
- `live --once --url http://127.0.0.1:8799/?k=<READKEY>`: exit 0, printed the screen (`chantier live ...`,
  Projects box with `p  no batch / inbox 2 ...`). PASS.
- Tests at head: `pytest -q` on test_board_exposure, test_server_api, test_server_api_calls,
  test_server_api_ws: `58 passed in 13.18s`. PASS.
- Code reads: `BEYOND` says "the private link acts: give it to the user only, plain HTTP"; `--new-key` help says
  it replaces both keys; `reads.for_read_key` is applied in ops.py:277 and push.py:120 (autonomous decision
  claimed in PR body). `webui` imports `read_only_lines` and prints it (webui.py:58). The `webui` printed
  output itself was not run (it needs the browser step); the line comes from the same `read_only_lines` the
  serve start lines use, which I ran.
- PR body (work/pr-body.md): sections render, Summary/Deliverables/Changes match the diff (35 files, keys,
  auth, ops/topics allow-lists, protocol, command/webui, AGENTS.md, docs, cards, tests); Known gaps names the
  skipped first-server step, the page's controls and Windows scenario; no images. Test-plan boxes unticked
  placeholders as the template has them (Review box to be filled by the Driver). PASS, not a failure.
  Not run by me: `just scenario`, `just check`; CI green is reported by the Driver (not proof).
- Evidence before/after: no screenshots in this CR; the before is the base's single-key server, not captured
  (see verifier/evidence/before-after.md).

VERIFIED

Description pass at 53a134e6e2804387be6ae43ae24b06bab5c836c6: posted body read against verify.md and diff; Summary/Deliverables/Changes match; Known gaps present; Review box matches log (r2 approved at 13e79ac, committed as 53a134e); CI green at 53a134e (gh pr checks: check x3, eval-dry-run, scenario pass); no images. VERIFIED
