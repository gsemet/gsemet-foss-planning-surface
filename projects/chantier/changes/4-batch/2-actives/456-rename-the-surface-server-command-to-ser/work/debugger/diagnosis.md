# CR-456 surface-board scenario red: diagnosis

Repro: `just scenario --unit surface-board` in the worktree (needs port 8765 free for the serve_and_webui part).
Local transcript with the exceptions: scenario/results/20261122-140741-42208/surface-board-github.md
(CI prints only check names, not the exceptions).

## Cause (proven)
CR-456 (11975a1f) changed the server's cookie to a per-server name: board/key.py
`COOKIE_PREFIX = "chantier_board_"`, `cookie_name(served)` = prefix + 12 hex of sha256(served.as_posix());
guard.py:40 reads the cookie under `ctx.cookie` (board/context.py:67). It updated scenario/run_scenario.py
call sites to use `link.cookie_name` (lines 2721, 3301) but NOT the `Link` class (scenario/run_scenario.py:1657-1672):
- no `cookie_name` attribute -> `AttributeError: 'Link' object has no attribute 'cookie_name'` (line 3301 = first
  failure, "remote_board ran to the end"; line 2721 in serve_and_webui)
- `Link.cookie` (line 1672) still sends `chantier_board=<key>`, a name the server no longer reads -> every
  cookie-authenticated request of the scenario is 401 / WS close 4401 ("surface_server ran to the end:
  ConnectionClosedError 4401"); forge_hub, external_surface and the "board write" checks cascade from it
  (unpack of empty results, missing forge-journal.jsonl because the board write was refused).
The server side is fine: test_serve_webui.py:137 already proves old cookie -> 401, new -> 200.

## Fix (scenario only, one place)
In `class Link` (scenario/run_scenario.py ~1657): add
    @property
    def cookie_name(self): return cookie_name(Path(self.over))   # from chantier.board.key; Path(...).as_posix() matters on Windows
    @property
    def cookie(self): return {"Cookie": f"{self.cookie_name}={self.key}"}
`over` is the `served` folder the start line prints (command.py:262 `over {served}`). Caveat: surface_link()
(line ~2293) falls back to the literal "the surface" when server.json has no `server.served`; it should then
give a real path (it reads `data["server"]["served"]`, so check that key exists in server.json).

## serve_and_webui specifics (partly unproven)
The `webui` failures ("exits 0", "already running") occur when `first` (serve --port 8765) gave no start line
(port 8765 held; locally by another program; on CI likely a server left by an earlier failed case of the
same unit, which crashed on the cookie bug before cleaning up). Then `webui` cold-starts `uvx --from ... serve`
and exceeds START_S (20 s) -> exit 4. Once the cookie bug is fixed and earlier cases clean up, expect it to pass;
if it still fails on CI, run the unit alone and read `first.line()`; consider having the scenario pass a free
port instead of DEFAULT_PORT, or not depend on a cold uvx within 20 s. Not reproduced here (8765 is busy on this machine).
