# CR-411 verify

Head: dd1f1c109079a77874abdfe4bd6189d94c923276

All claims judged at dd1f1c1 (worktree clean, `git status --short` empty; `gh pr view 384` headRefOid = dd1f1c1).
Raw output of the HTTP probes: `work/ui-probe.log` (kept; scratch removed).

## 8.3 "In a browser" (not a browser: HTTP requests)
No browser tool in this session: the browser step was NOT exercised. The same was proved with HTTP
requests (Python urllib with a cookie jar) against `uv run --no-sync --project <worktree> chantier
--project <scratch project> board --host 127.0.0.1 --port 0 [--ui ...]` after `uv sync --locked --project <worktree>`
(a scratch git project under work/scratch, not the live planning folder; every board stopped by PID, none left running).
- default: `?k=` -> 303 `./` with Set-Cookie; `/` 200 text/html + CSP (`default-src 'none'; script-src 'self'; ... connect-src 'self'`);
  `/js/main.js` 200 text/javascript; `/app.js` 404; no key -> 401. PASS.
- `--ui none`: start line printed; `?k=` 303 with cookie; `/`, `/index.html`, `/js/main.js`, `/app.js` -> 404 body
  `this server serves no UI: see docs/server-api.md`; `GET /api/board` 200; `POST /api/v1/call/board.get` 200. PASS.
- `--ui <drive-letter folder with index.html + app.js calling board.get>`: `/` 200 text/html + the same CSP; `/app.js` 200
  text/javascript; `/js/main.js` 404; `/api/board` 200; the page's own call (`POST api/v1/call/board.get`, same origin, cookie) 200.
  The CSP allows that page (script-src 'self', connect-src 'self', no inline). PASS (page rendering in a real browser not seen).
- `--ui <missing folder>`: exit 1 (EXIT_USAGE), stderr `error: --ui <path>: not a folder with an index.html: give a folder of static files, or none`, stdout empty. PASS.
- 8.2/B1 by hand, on a running board: second `board --ui none` -> exit 0, `board already running at <same link>` then
  `--ui not applied: a board already serves this surface; stop it to change what it serves`; `/js/main.js` still 200 (default board) / 404 (the none board) = still what it was started with. PASS.

## 8.1 pytest (at dd1f1c1, worktree, `python -m pytest ...`)
- `tests/test_board_ui.py tests/test_board.py tests/test_board_design.py tests/test_code_targets.py tests/test_open_empty_batch.py tests/test_server_protocol.py tests/test_scenario_coverage.py`: `74 passed, 1 skipped in 6.50s`.
- `tests/test_board_ui.py -rs -v`: `11 passed, 1 skipped in 20.57s`; the skip is the symlink case ("this OS does not let the test make a symlink"), the skip states why, as the spec allows. The test file holds the split (no `board/web`, `clients/web/index.html`+`DESIGN.md`, no `.py` under `clients/`, AST check on `board/`), serving a folder, no UI (`/`, `/index.html`, `/js/main.js`), the three refusals with no `server.json`, and the B1 cases. PASS.
- `grep -rn clients skills/chantier/scripts/cli/src/chantier/board --include=*.py`: only comments/docstrings/`"too many clients"` (no `clients/` or `clients` literal). PASS.

## Spec reading checks (diff `git diff -M origin/main HEAD`)
- 4.3: `static.py` has no `WEB`; `serve(ui, rel, if_none_match)`, `_file(ui, rel)`, `NO_UI`; `Context.ui`, `_run(..., ui)`, routes pass `ctx.ui`. PASS.
- 5: `declare/board.py` `--ui`, `SHIPPED_UI`, HELP as spec; `_ui` runs right after `--clock`, before `open_projects()`; NOT_APPLIED only when `args.ui != SHIPPED_UI`. PASS.
- 4.2: `.gitattributes`, `biome.json`, `justfile` lint paths moved; no stale `board/web` left outside old release notes (`grep -rln "board/web" .` excluding .git and release notes: none). PASS.
- 7.1: AGENTS.md has both edits (DESIGN.md path sentence; `--ui <folder>` / `--ui none` in the server sentence). PASS. 7.4: DESIGN.md path sentence names `clients/web/` (the only changed line; R099). PASS.
- 7.3/6: `docs/server-api.md` "Serving another UI" and `docs/web-board.md` bullet present, match the code. PASS.
- Cards unchanged (diff touches none). PASS.
- Release-notes line (spec 9): not added; no new-release file exists (Driver's note in r1.md and PR Known gaps). Accepted, named in Known gaps.

## 8.4 matrix, this Windows host
- absent / Windows: probe above (default 200s) plus Driver's local long gate pass (carried from the Driver's notes, not redone).
- folder / Windows (drive-letter path): probe above + test_board_ui (passes here). PASS.
- none / Windows: probe above + test_board_ui. PASS.
- bad folder / Windows: probe above + test_board_ui refusals. PASS.
- given, board running / Windows: probe above + test_board_ui B1 cases. PASS.
- Linux cells: not provable on this host; CI green (5 jobs) per the Driver, not redone.

## PR description (pr-body.md; the posted body on the forge is identical, `gh pr view 384`)
Renders (headings, mermaid block, fold); Summary, Deliverables and Changes match the diff; no image; no role name outside Internal references.
Note for the Driver, not a failure: Known gaps' first bullet says "Hand checks of the spec's 8.3 not yet run: wheel listing, eol listing, Biome file count, docs screenshots, browser check, `just test` timing", and the Test plan boxes are unchecked. The Driver reports those proven; the bullet must be rewritten before ready (the browser step stays a gap: not exercised in a real browser, HTTP only; the 8.3 listings are meant to be quoted in the PR). One small edge seen, not in the spec's tests: `args.ui != SHIPPED_UI` compares a string to a Path, so passing the shipped folder explicitly on a running board also prints the "not applied" line (harmless, arguably correct).

## Verdict
VERIFIED at dd1f1c109079a77874abdfe4bd6189d94c923276 (browser step not exercised; HTTP proofs only).

## Description pass

Head: dd1f1c109079a77874abdfe4bd6189d94c923276

Judged on the posted body of PR 384 (`gh pr view 384 --json body`), at dd1f1c1.
- Diff vs base d1a5d71 (`git diff --find-renames=100% --name-status`): 154 R100, 1 D + 1 A (DESIGN.md), 27 M of which 5 under `chantier/` (board/command, context, routes, static, declare/board); 1 other A is tests/test_board_ui.py. Matches Deliverables. PASS.
- 8.3 figures (eol 153 lf / 2 woff2, wheel 155 files, biome 151, just test 69 s/72 s, docs-screenshots bytes): recorded in the CR log note of 2026-11-20T18:50:01Z at dd1f1c1. Not rerun. PASS (from the log).
- `--ui none` 404 line, bad folder, running board, drive-letter folder, browser gap: proved above in this file at dd1f1c1. Known gaps match (browser, symlink skip, string-vs-path edge, no release-notes line). PASS.
- Test plan: gates (check, eval-dry-run, scenario) in log at dd1f1c1; Review `dc1f3ad` = "r1 approved at daed507b, committed as dc1f3ad9" in log; Verified at dd1f1c1; CI: `gh pr checks 384` 5 jobs pass, head oid dd1f1c1. PASS.
- Renders (sections, mermaid, fold); no images; no role name as internal reference. PASS.

VERIFIED at dd1f1c109079a77874abdfe4bd6189d94c923276.
