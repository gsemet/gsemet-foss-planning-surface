# Investigation: CR-227, a planning surface stays in sync through its own autosync

Read only. Worktree `C:/Users/gaeta/Projets/chantier.worktrees/batch-17-CR-227`, head `e2212ae`
(stack top: CR-242, with CR-222's board and CR-225's reading views). Paths below are under
`skills/chantier/scripts/cli/src/chantier/` (shortened `pkg/`) unless stated.

## 1. The smallest change

Add one read-only package `pkg/autosync/` (4 small modules) used by `preflight` (P13), `status`
(one line) and the board. Add two board modules (`board/autosync_tool.py`, `board/autosync_api.py`),
one start-up call in `board/command.py`, one field in `Context`, an `autosync` key in `GET
/api/board`, a pill in the existing frame (`web/js/ui/autosync.js`, one CSS file, 4 tokens, words in
`en.js` and `fr.js`), the cards, `docs/planning-modes.md`, one clause in `AGENTS.md`, a fake tool
and new steps in the scenario. No change to `agents/`, `com.github.copilot/`, `hooks/`, `types/`,
`STATUS.json`, `ci.yml`, `pyproject.toml` (no new dependency): so no `just mod`, no pane screenshot.

## 2. What the spec names versus what exists today

| Spec name | Today |
| --- | --- |
| `autosync/` package | Absent. Packages now: `board/ commands/ core/ costs/ declare/ lifecycle/ playbook/ status/ summaries/`. `declare/` (light parser modules, loaded for `--help`) is new since the spec and must stay free of pydantic/psutil: `autosync/` is imported only by handlers (`commands/preflight.py`, `commands/batch_status.py`, `board/*`), never by `declare/` or `cli.py` (test `test_the_start_up_imports_only_the_standard_library_and_chantier` enforces it). |
| `core/` | Exists: `batch, batch_records, clock, errors, files, git, ids, records, repo, seat`. Layer rule is only enforced by `tests/test_code_targets.py` (file <= 400 lines, function <= 50, no import cycle). |
| `commands/` | Exists. `commands/preflight.py` (245 lines), `commands/batch_status.py` (236 lines; `status()` at line 171; the batch line is `lines[0]`, `last_closed_text` is `lines[1]`). |
| `procs.alive` | Exists: `procs.alive(pid) -> bool` (psutil loaded lazily, zombie = gone, AccessDenied = True). Also `alive_since`. Use `alive` as spec says; psutil is banned at module level by ruff `TID253`. |
| `plugin_files.surface_instructions(repo)` | Exists (`plugin_files.py:106`): first of `AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` in `repo.surface_root`; `None` when not external. |
| `repo.external` | Exists: property, `project_dir is not None`. Also `repo.surface_root`, `repo.git_dir` (for an external repo it is the **surface's** git common dir, `Repo._external` sets it from `rev-parse --git-common-dir` of the project folder), `repo.session_root`, `repo.changes`. So `state_dir = repo.git_dir / "ai-autosync"`. The tool itself uses `--absolute-git-dir` (per-worktree); identical in the surface's main checkout, which P7 enforces. |
| Preflight "checks up to P12" | True. Printed order is P1, P4, P5, P6, P7, P8, P12, P11, P10, then the "own checks" line and the verdict. P13 is free. `_Report.check(tag, passed, good, bad, warn=True)` is the warn-only form. `_check_allow` appends to `r.lines[-1]` (P10), so P13 must be added in `_check_project` (which runs before `_check_allow`), not after it. The report has ~12 lines with P13; the code comment says "within ten lines" (about P10 only, no test asserts a total). The spec's P13 "ok" lines fit `check`; the `missing` / `blocked` lines are `warn=True`. |
| `commands/batch_status.py` | Exists, as above. `status` fails with no running batch via `resolve_batch` (open point 4 default holds). The autosync line goes in as `lines.insert(1, ...)` (after `_batch_line`, before `last_closed_text`) or the spec's "right after the first line". |
| `seat.json` | `core/seat.py:read_seat(repo) -> SeatRecord | None`; `SeatRecord` has `session, transcript, env, title, link`. The file is `repo.changes/"seat.json"` (per project). The board already reads it (`board/seats.py`, `board/state._seat`). `seat take <id>` stores the same id the card passes to `board --seat <own session id>`, so rule 2 of the naming (seat session) works with a card that passes `--session-id <own session id>`. |
| Foreman session | `BatchRecord.foreman` (set by `foreman set <session-id>`), read with `read_batch_json(repo.batch_folders()[0]/"batch.json")`. |
| `repo.external` + `board` | `board/projects.py`: `Projects.surface` (root or None), `Projects.home` (a `Repo`, external when a surface), `Projects.all()`. A site is the surface's, so `find_site(projects.home.repo)`; for in-project `home` is not external, so `find_site` returns None as spec wants. |
| `board/static/js/views`, `board/static/css` | **Wrong path.** The frame is `board/web/` (`web/index.html`, `web/css/`, `web/js/{core,i18n,model,panel,ui,views}`). `static.py` serves `web/` with `Cache-Control: no-cache` + ETag. Views are `web/js/views/*.js` registered in `views/registry.js`; the sidebar, phone project button, bottom bar and picker are `web/js/ui/*.js`. |
| `mountAutosync({sidebarFoot, phoneBar, store, api})` | **Does not fit.** The page has no mount-with-store pattern for the frame: `main.js` `drawFrame(state)` calls `paint(element, markup)` from pure `ui/*` functions on every store update, and events are delegated on `document.body` via `delegate(body, 'click', '[data-...]', ...)`. The fitting design: `web/js/ui/autosync.js` exports pure markup functions (`pill(state)`, `dot(state)`, `panel(state)`; `label`, `subtitle`, `actions`), `main.js` paints two new slots and one delegate block, and the open/busy/error flags live in the store (`autosync: {open, busy, error}` beside `menu`). A separate small `web/js/core/api.js` function `post(path, body)` (the only `fetch` module). |
| i18n | `web/js/i18n/en.js` and `fr.js` registered in `model/words.js` (`t(key, params)`, `tn`). A test requires the **same keys** in both. This is the decision "English by default and French, one word file per language": already the page's mechanism. The prototype's French strings go to `fr.js`; English ones are new. No new mechanism. |
| "live-refresh payload" | There is **no push**. The page polls `GET /api/board` and `GET /api/projects/<id>/state` every 5 s (`core/refresh.js`), the state with `If-None-Match`. The state's ETag is a `stat` walk of the planning folder (`board/fingerprint.py`) and does **not** see `.git/ai-autosync/`. So the autosync object cannot ride on the project state (it would stay `304`). Put it in `GET /api/board` (a small object, always rebuilt; `routes.board()` already rebuilds per request) and make `refresh.js` `lines()` compare it too (today it compares `b.projects` only). Keep `GET /api/autosync` for the panel and the actions (`present:false` with no site). |
| `board/` "URL secret, write protection" | Key in the URL once, then the `chantier_board` cookie (`board/guard.py`); a POST needs the cookie/header, same-origin (`Sec-Fetch-Site`, `Origin`) and `application/json` when it has a body. POST routes today: `costs/recompute` and `seats`. Routes are a regex table `ROUTES` in `board/routes.py` (187 lines), handlers `(ctx, req, *groups) -> Reply`; `_judged` maps `OSError/ValueError/KeyError/ChantierError` to 500. `Reply`/`as_json(data, status=...)` in `board/reply.py` give 409/502. Add `autosync_api.ROUTES` and extend the table (`ROUTES += ...`); no circular import (api imports `reply`, `context` only). |
| backlog writes (CR-226) | Not in this worktree: the board has no backlog POST route yet (`board/backlog.py` is read-only). The autosync server writes are therefore the first state-changing routes beyond recompute; nothing to merge with. |

## 3. Where the board starts, routes, CSP

- Start: `board/command.py:board()`. Order: `open_projects()` -> `check_planning` -> `settings` ->
  `load_or_create` key -> `Seats` -> `_running(...)` ("board already running", returns before
  binding: **no join on a reuse**, as the spec wants) -> `_bind` -> `print("board on <link> over
  <served>")` -> optional `BEYOND` line -> `_run(...)` (uvicorn, blocks). The join goes after the
  `BEYOND` print and before `_run`; its status line is the 2nd or 3rd line. Scenario `Link.LINE`
  parses the **first** line only and an in-project start asserts "nothing else" after it
  (`first.line(1.5) is None`, scenario line ~1197), which holds because no site means no line.
  A surface start prints one more line: update that scenario step only if it is a surface one.
- Server pid: `os.getpid()` in `command.py` (the process that serves; under `uv run` it is the
  Python child, which is what the participant must follow).
- Routes now (all behind the key): `GET /api/board`, `GET /api/projects/<id>/{state,tree,file,costs}`,
  `POST /api/projects/<id>/costs/recompute`, `POST /api/seats`, static files for anything else.
- CSP (`board/reply.py`, HTML only): `default-src 'none'; script-src 'self'; style-src 'self';
  img-src 'self'; connect-src 'self'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'`.
  So: no inline style attribute (the prototype's `style="background:${col}"` is not allowed; use
  classes or `data-vars` + `setVars`, which uses the CSSOM), no inline script, same-origin fetch
  only. Tests (`test_code_targets.py`) also forbid: a hex colour outside `tokens.css`, an id
  selector in CSS, CSS files over 300 lines or nesting over 3, JS files over 300 lines, `innerHTML`
  outside `dom.js`, `style=`/`on...=` in markup, a non-relative or missing import, and `en`/`fr` key
  mismatch. Biome (`biome.json`): function <= 50 lines, cognitive complexity <= 10, <= 5 params,
  file <= 300 lines, `noUnusedImports`.

## 4. How CR-225 built the places the pill plugs into

- Sidebar foot: `web/index.html` `<div class="foot"><div id="heard"></div><button class="lang"
  id="lang" data-lang></button></div>` inside `<aside class="side">`; styled by `.side .foot`
  (`css/shell.css:148`, `margin-top:auto`, border-top). `main.js drawFrame` paints `#heard` with
  `heard(state)` (`ui/sidebar.js`) and `#lang`. The pill is a new slot **above** `#heard` in `.foot`
  (`<div id="autosync-side">`), painted from `ui/autosync.js`, hidden when `present:false`.
- Phone bar: there is no "phone bar" element; the phone header is `<div class="project phone"
  id="project-phone">` inside `.head`, which `drawFrame` fills with `[trigger(state,'pbtn'), menu(state)]`
  (`ui/picker.js`). `.project.phone` is `display:none` above 760 px and `display:block` below
  (`shell.css:221-247`); `.pbtn` is a `display:flex` button. The dot (34x33 button) goes in a new
  `<span id="autosync-phone">` **beside** it: wrap both in a flex row (prototype: `.pwrap` then
  `.aswrap.asph` inline-block). Also the bottom nav `#bottom-nav` (views) is separate and untouched.
- Project picker: `ui/picker.js` `trigger(state, cls)` / `menu(state)`; menu open flag is `state.menu`
  and closed by a document click (`main.js`). Its outside-click/Escape handlers are the pattern to
  copy: one more branch for `state.autosync.open` in the two document listeners, which must stay
  small (`main.js` is already 116 lines; keep new wiring in `ui/autosync.js`/a `bindAutosync(body)`).
- Panel placement: the prototype's panel is `position:absolute; bottom:calc(100% + 6px)` over the
  pill (PC, 300 px) and `position:fixed; left/right:12px; top:58px` on the phone. There is an
  unrelated `#panel` (file side panel, `panel/panel.js`): name the new one `autosync-pop` to avoid a clash.
- Projects: `All projects` is `state.project === '*'` (`ALL`); `drawFrame` runs the same for every
  project, so a frame slot shows on every project and on All projects with no extra work.
- Times: `core/format.js` `span`/`age(iso, nowIso)` count against the **server's** `now` (`state.now`),
  with `time.s/min/h` words. Reuse `age(last_push, state.now)` for "pushed N s ago"; the 5 s client
  tick in the spec is not needed (the page already redraws every 5 s and `minute` moves per minute).
  Caveat: `chantier board --clock` freezes `now`; `last_push` is real epoch time. Harmless, only worth knowing for scenario assertions.
- Colours: `tokens.css` holds the only colours. Existing `--green #2fa86b`, `--red #d6455d`,
  `--amber #d98a1c`, `--grey #9aa0ab`, `--tag-blocked-ink #c03552`, `--warn-ink #8a5208` do not equal
  the prototype's `#23805a / #8b909c / #c03552 / #b86e0c`. Add four tokens
  (`--autosync-active/stopped/blocked/approval`) plus the red and amber box fills (prototype `#fff4f5/#9c2a41`,
  `#fff6ec/#7a4a0c`), as the spec says "CSS custom properties"; do not reuse the near-miss ones if the
  QA wants the prototype's exact look.

## 5. The CLI side

- `autosync/site.py` `find_site(repo)`: external AND `surface_instructions(repo)` text contains
  `.agents/guidelines/autosync.guidelines.md` AND `<surface_root>/scripts/ai-autosync-git.py` exists
  (`script_missing` when only the first two). Read text with `core.files.read_text`.
- `autosync/records.py`: the repo's pydantic `Record` base is in `core/records.py` (used by `SeatRecord`);
  check its `extra` policy before choosing `extra="allow"` (the spec says allow). Reading mirrors the
  tool's `read_json` and `read_control`: `enabled = data.get("enabled", True) is not False`.
- Facts verified in the user's script (`gsemet-foss-planning-surface/scripts/ai-autosync-git.py`, v1.0.0,
  1040 lines, read only):
  - State dir `<absolute-git-dir>/ai-autosync` (`repository()`, line 200). Files in the user's checkout
    today: `control.json`, `status.json`, `watcher.json`, `attributes.json`, `sync.lock`, `participants/<pid>.json`.
    `approvals.json` only appears on `approve`. (`attributes.json` is not in the spec; chantier ignores it.)
  - `participants()` (line 809) **unlinks** dead participant files: chantier must not (the spec says so; E2 proves it).
  - `status.json` has `state, message, updated_at` plus `incident` for `approval_required` and, after a cycle, `branch, head, committed`.
    `control.json`: `enabled, local_only, reason, updated_at, updated_by_pid`.
  - `--harness` choices are `auto` plus the registered names, and `generic` is the base `Harness`
    (`HARNESSES` = copilot, claude-code, omp, generic): `--harness generic --owner-pid N --session-id X` is valid, and
    `join` refuses when `harness.alive()` is false (owner pid dead). `approve` accepts only the incident `status.json` names now.
    `start --enable-only` returns at once; `join` blocks in `participate()` (hence the detached spawn).
  - The script has a PEP 723 header with `filelock` and `watchdog`: `uv run scripts/ai-autosync-git.py` needs
    uv's cache or network the first time. The AGENTS.md "no network once uv's cache holds its packages" covers it;
    a first `uv run` offline fails and the join line must say so (`board: autosync not joined: <reason>`), no fallback.
  - The printed "participant pid <n>" in the spec's join line is the pid of the spawned process (`Popen.pid`), which under
    `uv run` is uv, not the Python child whose pid the participant file records. Print "started" with that pid labelled as the
    process, or read the participant list later; do not claim it equals the participant's `pid`.
  - The user's surface `AGENTS.md` mentions `.agents/guidelines/autosync.guidelines.md` (as a markdown link) and the phrases `start autosync` / `stop autosync`: detection by substring works on it.
- Preflight and status wording: the spec's lines are exact strings the scenario must match; keep them in one
  place (`autosync/lines.py`) as the spec says.

## 6. The scenario's external-surface setup

`scenario/run_scenario.py` (6,400+ lines, not linted by `just lint`): `class SurfaceWorld(World)` (line 6131) builds a
scratch surface with `build()`: `git init` of `root/surface`, `AGENTS.md` = "# Surface rules / Plan on the default branch.",
projects `demo` and `other` with `checkout.yml`/`project.md`, one commit; `state` = `surface/projects/demo/changes`;
`chantier(...)` adds `--project demo`. The section is `external_surface(tmp)` ("## 20", line 6193); it already starts a
board with `BoardProc(w, "board", "--project", "demo", "--host", "127.0.0.1", "--port", 0, cwd=w.surface)`, then
`Link(bp.line())`, `jget(port, link, path)`, `fetch(port, path, method, headers, body)` (cookie header `link.cookie`).
`BoardProc` runs `python -m chantier board` with `w.env`. Reuse all of this: add a `surface_autosync(w)` step after
`surface_publishes(w, "after the close")` or before the board at line 6290, and extend the surface `AGENTS.md` per
case (add the guidelines line, then the fake `scripts/ai-autosync-git.py`, a stdlib script `scenario/fake_autosync.py`
copied to the surface). State files go under `Path(w.sh("git","rev-parse","--absolute-git-dir", cwd=w.surface)) / "ai-autosync"`.
POST to the board needs JSON body, `Content-Type: application/json` and the cookie; no `Origin`/`Sec-Fetch-Site` unless same-origin.
The in-project board (`remote_board`, line 1146, `World` in `w.work`) is the "in-project folder returns `present:false`" case.
`just scenario` runs both forges (`--forge github`, then `gitlab`); `external_surface` runs for both. The scenario runs under `uv run --locked python`; check the
scenario env (`w.env`) does not set `VIRTUAL_ENV`/UV vars that make a nested `uv run scripts/...` noisy (stderr is `DEVNULL` in the spawn).
CI scenario job runs only `ubuntu-latest`; Windows is covered by `just check` only, and the Windows detached spawn is proved on this machine (E3).

## 7. Lint and gates (exact targets)

`just check` = `lint test release-notes`; `just lint` =
`uvx ruff@0.17.5 format --check skills`, `uvx ruff@0.17.5 check skills`,
`uv run --locked --group dev --with mypy==1.20.0 --with types-psutil mypy` (strict, pydantic plugin; files: `src`, `tests`, `session_usage.py`),
`uv lock --check`, and `uvx --from nodejs-wheel==24.19.0 npx --yes @biomejs/biome@2.6.7 check skills/chantier/scripts/cli/src/chantier/board/web`.
Ruff selects `E W F I B UP SIM C90 PL RUF PGH004` + `PLR1702` (nesting <= 3) + `TID253` (psutil, ruamel, starlette, uvicorn banned at module level), complexity 10, max args 5,
branches 12, returns 6, statements 50, `line-length 100`. `just test` = pytest (structure). `scenario/` is not under `skills`, so not linted. Not needed: `just mod`.

## 8. Cards and docs (current text to change)

- `AGENTS.md` (worktree), the git exception today, lines 32-34, verbatim: "The board's server is also the CLI's one git exception: while it runs it joins the planning
  surface's own autosync group, which commits and pushes its writes; it commits nothing itself.
  The rest of the CLI keeps no git write." It already carries the join and "commits nothing itself" but **not** "runs its start, stop and approve on the user's click":
  per open point 8, add that clause (one sentence); nothing else in `AGENTS.md` changes. Also line 12-17 ("chantier writes only in the planning folder ...") lists the
  git-folder key; the tool's `.git/ai-autosync/` files are the surface tool's, not chantier's, so no list change.
- `concepts.md` "Planning surface" bullet at line 67; `session-start.md` section 2 (line ~63 "The board" paragraph and the board's line list at 69-75);
  `chief-of-staff.md` "With a planning surface" paragraph at line 240 and the entry-points table (rows near line 40: add "start autosync", "stop autosync");
  `foreman.md` (uses `$CHANTIER asks "<text>"`, line 250; add the autosync ask, once per block); `griller.md` "In a planning surface" line 58 (and "In a worktree", line 66, stays);
  `docs/planning-modes.md`: the surface paragraph at lines 27-52 (the "Its own sync rules win; without any, the Chief of Staff commits and pushes after each step" sentence is line ~41-43) and "## Grillers" at line 83.
  Chief-of-staff.md is a ruled file in `rules` output with README/CONTRIBUTING; `chantier rules` lists AGENTS.md, CONTRIBUTING.md, README.md, `docs/use-cases-direct.md`, `chief-of-staff.md`, `scenario/README.md`, `evals/README.md`, `evals/SCORECARD.md`, `docs/release-process.md`; the ones touching this work are AGENTS.md, CONTRIBUTING.md (repo text in English, docs rules) and `scenario/README.md` (add the new steps to its list).

## 9. Prototype pill code (found)

`C:/Users/gaeta/Projets/chantier/.agents/changes/4-batch/2-actives/222-visualization-backend/prototype/index.html`
(the spec's `visualization-backend` folder is now `222-visualization-backend`, in `2-actives`): styles `.asy .adot .apop .aw .aa .asim .asph .asyd` at lines 118-134;
markup `#asy`/`#apop` at 400 and `#asy2`/`#apop2` at 407 (`.aswrap.ph-only.asph`, next to `.pwrap` project button); logic lines 1074-1098 (`AS`, `ASL`, `asPaint()`, click and outside-click handlers, 5 s interval).
Details to reproduce: panel at `bottom:calc(100% + 6px); width:300px; border-radius:10px; padding:12px; font-size:12.5px`; amber/red boxes `.aw.wa` (`#fff6ec/#7a4a0c`) and `.aw.ko` (`#fff4f5/#9c2a41`); dl grid `auto 1fr`; title text "Autosync <state>".
Prototype points that conflict with the board's rules: inline `style="background:..."` (CSP), ids as selectors (test), `onclick=` assignments, 12.5 px / 11 px text (the grill rule says no text under 11 px for a badge and 12 px elsewhere: 12.5 and 12 pass, `small` 11 px is a badge-class text, check), "Simuler" row (not delivered).
Reference images: `.../222-visualization-backend/evidence/prototype/v6-20-autosync-approval-pc.png` and `v6-21-autosync-blocked-phone.jpg`.
Another copy of the prototype for QA: `225-board-read-views/work/qa/proto/index.html` and `work/verifier/proto/index.html` (CR-225's QA reused it; handy for the "Simuler" row states).

## 10. Risks

1. **Fingerprint blindness** (section 2): the project state's ETag cannot see `.git/ai-autosync/`; the object must ride on `/api/board` or a separate poll. If forgotten, the pill never updates.
2. **`refresh.js` `lines()`** compares only `board.projects`; a changed `autosync` would be dropped unless the comparison is widened (one line).
3. **Read cost**: each `/api/board` (every open page, every 5 s) reads 3-5 small JSON files and runs `procs.alive` per participant; trivial, but do it once per request, not per project. `routes.board()` already loops projects with `ask=False`.
4. **Detached spawn on Windows**: `uv run` creates a child; `DETACHED_PROCESS` + `DEVNULL` stdio; the participant follows `--owner-pid`. Prove with E3 (the leave within ~2 s of server stop). The Popen pid is not the participant pid (section 5).
5. **Test "start-up imports"**: `autosync/*` and `board/autosync_*` import pydantic/psutil only inside handler paths; keep `declare/` untouched. Putting `import subprocess` is fine (stdlib).
6. **Scenario tests that count board start lines**: only surface starts with a site print the extra line; the existing surface step in `external_surface` has no site (AGENTS.md lacks the guidelines line) so it is unchanged.
7. **Synchronous POST in the thread pool**: `run_action` blocks up to 30 s inside `run_in_threadpool` (default pool 40 threads); fine. `start`/`stop` on a stuck lock return the tool's last line as 502.
8. **Approve race**: between the page's click and `approve`, `status.json` may change; the server re-reads the state just before running `approve` and 409s on a stale id (spec). Then `start --enable-only` after success; if it fails, return 502 with the line, leaving state `blocked` which the pill shows.
9. **Cards**: `session-start.md` must tell hosts how to get "own session id" and the host PID for `join --owner-pid`; the spec says follow the guidelines (`$PPID`). A PowerShell host cannot use `$PPID` the same way (spec open point 11); the card change must not claim it works there. No `agents/` change, so `AGENTS.md`'s hand-written parity rule is not engaged.
10. **Closed wording trap**: the spec says "no force push" and "never runs approve" in the cards; the Inspector should grep the cards for any "approve" instruction to an agent.

## 11. Questions only the user can answer

None blocking. The spec's open points carry defaults; the only item worth a user glance: the 12.5 px / 11 px prototype sizes against the grill's "12 px elsewhere" rule (the Coder will use 12 px and 11 px badge class and the QA table will name it as an expected difference).

## 12. Evidence plan

Kind of change: CLI + server behaviour (testable by output), a UI element (screenshots), and cards/docs (text). The project's rules (AGENTS.md, scenario/README) require `just check` and `just scenario`; they are silent on UI screenshots except the spec's own QA, so the plan below follows the spec. Items go to `work/verifier/evidence/`.

| # | Proves | Technique | Before / after |
| --- | --- | --- | --- |
| E1 | lint, types, size rules, tests, release-notes | `just check` on this Windows machine (log of ruff, mypy, biome, pytest); then CI's three-OS run | pass log; CI links in the PR |
| E2 | detection, P13 and `status` lines, read-only, board API, spawn argv, 409 rules | `just scenario` (both forges) with new steps in `external_surface` (section 20) using `scenario/fake_autosync.py` as `scripts/ai-autosync-git.py` and state files under the scratch surface's `.git/ai-autosync/`: each state (active with/without a live participant, stopped, blocked, approval, no folder), exact lines from the spec, dead participant file still there, `GET /api/autosync` per state, `POST start` 409/ok, `POST approve` 409 with stale id and `approve . <id>` then `start . --enable-only` with the current one, in-project board `present:false` and no spawn (argv file absent) | "before": the same run on `e2212ae` has no P13/autosync line (quote one `preflight` output without the line); "after": scenario output of the new checks |
| E3 | the real tool end to end | Scratch folder outside the repo and outside the user's surface: bare `origin`, a clone as surface, copy `gsemet-foss-planning-surface/scripts/ai-autosync-git.py` (read only) and its guidelines text, run `init`, add `projects/demo/`; `chantier board --project demo`, show the join line and the participant file; board-API `triage` is committed/pushed by the server's participant with no agent session (`git log` of the bare repo); blocked (second clone pushes), approval (stage a file by hand), stopped via the board's stop; approve from the board; stop the server and show the participant file gone within 2 s. Tools present here: git-lfs 3.8.1, gitleaks 8.30.1, uv 0.13.6. | transcript of commands and outputs, `git log` of origin before/after, listing of `participants/` |
| E4 | cards walked through | In the E3 scratch surface: a Chief of Staff and a Griller join (`status` lists "chief-of-staff", "session ..."); a blocked group is integrated by rebase and restarted; `git reflog` of `origin` shows no forced update | `status` output of the tool and the reflog. **Not provable:** a real Foreman (no batch); name it in Known gaps. |
| QA | the pill and its panel against the prototype, PC 1400x860 and phone 375x812 | Playwright (chromium-1248 and headless shell are already installed in `%LOCALAPPDATA%\ms-playwright`); a scratch uv script outside the repo, not committed; the board of E3 against the prototype with its "Simuler" row; the 8 pairs of the spec, plus console-error capture, tab/Escape/`aria-expanded` check, and the CSP header (no `unsafe-inline`) | Screenshots `proto-<n>.png`/`board-<n>.png`, a table pair/differences for the PR; expected differences: real data, no "Simuler" row, English words by default (French with `?lang=fr`, which is the prototype's text) |
| Cards | text changes | `git diff` of the 5 cards and `docs/planning-modes.md`; Inspector's grep for "approve" instruction to an agent; `just check` tests the references | diff |

Cannot be shown: the Linux and macOS detached spawn (only CI's scenario on `ubuntu-latest` runs it, through E2's fake; macOS is only in `check`), a real Foreman reading the autosync line, a real remote phone session, and any run on the CR board pane (unchanged, so no pane screenshot is owed).
