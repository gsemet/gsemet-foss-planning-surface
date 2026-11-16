# Investigation: CR-226 board edits the backlog (read-only map of the worktree)

Worktree: `C:\Users\gaeta\Projets\chantier.worktrees\batch-17-CR-226`. `SRC` below is
`skills/chantier/scripts/cli/src/chantier`, `WEB` is `SRC/board/web`.

## Reality vs the spec's layout (read first)

The spec writes `commands/intake.py`, `lifecycle/backlog.py`, `board/journal.py`, `core/files.py`,
`static/...`. Real tree: those Python paths exist, but the board is a flat package
(`SRC/board/*.py`, no `static/` folder: the frame is `WEB = SRC/board/web/`, served by
`board/static.py`). JS lives in `WEB/js/{core,model,panel,ui,views,i18n}`, CSS in `WEB/css/` and
`WEB/css/views/`. The spec's `static/triage/`, `static/api/backlog.js`, `static/ui/toast.js` etc. map
to `WEB/js/...` (see section 5).

## (1) cr-summaries: label and group setters and read fields

PRESENT in the CLI, NOT usable in-process as they stand, and NOT in the read API.

- Storage and model: `SRC/core/records.py:249` `CrSummary` has `labels: list[str]`, `group: str|None`;
  `LABEL_PATTERN`, `GROUP_MAX`, `SUMMARY_FILE` at lines 20-25. Read/write: `SRC/summaries/store.py`
  (`read_or_new`, `write`, `UnreadableSummary`).
- Setters: `SRC/commands/summary.py` `label(args)` (`--add/--remove`, comma list) and `group(args)`
  (`--name`/`--clear`), both through `_edit_all(items, edit, show)`. Parser in
  `SRC/declare/summary.py`. Problem: they take an `argparse.Namespace`, call `open_repo()` themselves,
  and `_cr_folder` accepts a path, not a slug. They cannot be called by the server with a `Repo`.
  The Driver must refactor them (e.g. `lifecycle/backlog.py` `set_labels(repo, folders, add)` and
  `set_group(repo, folders, name|None)`, or lift `_edit_all`/`_labels`/`_one_line` out) and keep the
  command output identical. Validation to reuse: `_labels` (lowercase, regex, 24 chars, usage error),
  `_one_line(name, "group", GROUP_MAX)`. The setters never touch `sources`/`summarized`, so labels and
  group do not make a summary late (good: matches spec).
- Read side: `SRC/summaries/view.py` `summary_view(folder) -> SummaryView(title, summary, origin,
  labels, group, late)` EXISTS but is used by nothing (grep: no caller). `SRC/board/backlog.py`
  `backlog_items()` does not call it, so `GET /api/projects/{id}/state` items carry only
  `item, title, folder, files, depends, description, grill`: NO `labels`, `group`, `origin`, `late`.
  Needed (round 1): add those four keys to `backlog_items` from `summary_view` (None-safe, unreadable
  summary = late with empty fields, as the helper does). `board/fingerprint.py` must also notice a
  `summary.json` change (check what it hashes; an edit of labels/group must change the ETag).
- Status of the CR: `223-cr-summaries` is in `3-done`, and its CLI commits are in this stack
  (summary label/group exist), so the Driver does NOT have to stop on (1). The only gap is the
  in-process form and the read fields above. `depends.json` of CR-226 should list cr-summaries
  (open point 1); not checked here.

## (2) Board server code

Python, all in `SRC/board/`:
- `routes.py`: `ROUTES` list of `(verb, regex, handler)`; handlers `(ctx, req, *groups) -> Reply`.
  Current: `GET /api/board`, `GET /api/projects/{id}/state|tree|file|costs`,
  `POST /api/projects/{id}/costs/recompute`, `POST /api/seats`. `_judged()` = key check, method
  check (`guard.ALLOWED`), `guard.refusal(req)` only `if req.method == "POST"`, then `_dispatch`;
  exceptions `OSError|ValueError|KeyError|ChantierError` all become `500 UNREADABLE` (the write
  routes need their own mapping: 400 usage / 409 precondition+conflict, so `write_api.py` must catch
  `ChantierError` itself before `_judged`'s catch). Project found via `_found(ctx, id)`; `project.repo`
  is a `Repo` opened with `readonly=True` (`projects.py`; skips `.gitignore` but `changes_lock`
  calls `ensure_gitignore` itself, so a write works).
- `guard.py`: key from header `X-Chantier-Board-Key` or cookie (`key.py`); `ALLOWED = (GET, HEAD, POST)`:
  PUT is currently 405 (scenario line ~1342 asserts "`PUT` answers 405" on `/api/board`). Spec wants
  `PUT backlog/file`: either allow PUT (and change that scenario step to e.g. PATCH/DELETE) or make the
  route POST. `refusal()` already does same-origin: `Sec-Fetch-Site` same-origin/absent, `Origin ==
  http://<host>`, and a non-empty body must be `application/json` -> but it answers `403` for a bad
  content type, spec says `415`. It also lets an EMPTY body through with any type. Decide: keep 403
  (existing scenario/behaviour) or add 415 for writes only. It runs only for POST: extend to PUT.
- `reply.py`: `Reply`, `as_json`, `text`. CSP in `HTML_POLICY` has `form-action 'self'` (the spec says
  "keeps `form-action 'none'`": it is `'self'` today; either change the spec text or the policy; a
  native `<dialog>` with `method=dialog` needs no form submit, so `'none'` is safe, but changing it
  is a scenario-visible change).
- Read API for files: `files.py` `read(root, rel)` returns plain bytes, text decoded `utf-8-sig`
  (BOM stripped!) and re-encoded, cut at `TEXT_LIMIT = 1_000_000`, header `X-Chantier-Cut`. NO sha256
  anywhere. Add a header (e.g. `X-Chantier-Sha256`) of the exact bytes on disk (hash raw file bytes
  before BOM strip/cut; for a file over 1 MB the editor is refused anyway). `files.inside(root, rel)`
  is the confinement (spec calls it `board._inside`): rejects abs/drive/NUL/locks, symlink out, needs
  to exist. `is_lock`, `TEXT`, `kind_of` also there.
  Caveat for CRLF/BOM: `edit_markdown` must compare against the sha256 of the raw bytes and write via
  an atomic path that keeps line endings. `core/files.write_file` forces `newline="\n"`, so CRLF is NOT
  preserved: the Driver needs a bytes write (tmp + `retry(os.replace)`) or `write_file` with a
  `newline` option. A BOM on disk: spec says "UTF-8 with no byte-order mark" (it will be dropped on
  write; read_text already strips it). The text area's JS value has normalised newlines? No: a
  `textarea.value` keeps CR only as LF (HTML normalises CRLF to LF in `.value`), so the server must
  re-apply the file's dominant line ending (detect CRLF in the old bytes, convert).
- `static.py`: serves `WEB` with `ETag`, allowed types `.html .js .css .svg .json .ico .png .woff2`;
  no build, no bundler. New JS/CSS files need only be dropped in `WEB/js/...` and linked.
- `state.py` `project_state()`: the `backlog` key from `backlog.backlog_items(changes, dash["backlog"])`
  (`SRC/board/backlog.py`, buckets `STAGES = inbox,P1..P4,3-ready`; `grill_of()` returns raw / grill /
  specifying / specified / automatable, JS folds `specifying` into grill: `WEB/js/model/grill.js`
  already does it, answering open point 6).
- `fingerprint.py`, `costs.py` (Live), `seats.py`, `context.py` (`Context`, `Request` dataclasses),
  `command.py` (server start; `board.json` key in the git dir).
- Tests of structure: `SRC/../tests/test_board.py` has a hard-coded `MODULES` list of board modules
  (must add `write_api`, `journal`) and a list of required web files.

Frontend conventions (`WEB`):
- ES modules, no build; `index.html` `<script type="module" src="js/main.js">`, CSS `<link>`s listed
  in `index.html` (add `css/views/triage.css`, `journal.css`, `editor.css`, `dialog.css` there).
- `js/core/dom.js`: `html` tagged template (escapes), `raw`, `setHtml` (the one innerHTML), `$`, `$$`,
  `delegate(root, type, selector, handler)`, `vars()`/`data-vars` instead of inline `style`.
  `js/core/api.js`: the only module calling `fetch`; `get`, `AskError(status)`, relative URLs
  (`api/projects/{id}/...`), a `recompute()` POST showing the JSON POST pattern
  (`Content-Type: application/json`, `credentials: 'same-origin'`). New write functions belong here or
  in a new `js/core/api.js`-using `js/api/backlog.js` (it must still go through one fetch helper:
  export a `send(method, path, body)` from api.js and have backlog.js use it, to keep "only module
  that calls fetch").
- `js/core/store.js`: one `data` object, `update(patch)` notifies subscribers (main.js `draw`).
  `js/core/refresh.js`: polls every 5 s with ETag; after a write, call the same read (export `ask`).
- `js/core/router.js`: `?p=&v=`, `configure(views, overviewIds)`, `knows(view)`, `settle()` sends a
  view not in overview ids to the last real project on All projects (so a Triage view with no
  `overview` is hidden there automatically; `shown()` in `ui/sidebar.js` and `ui/bottombar.js` do the
  same for the menu).
- `js/views/registry.js`: `VIEWS` array `{id, icon, word, module{render, mount}, overview?, count?}`;
  Triage = a new entry after `home` (`knows('triage')` is already used by `views/home-backlog.js` for
  the "sort" link, which will then appear). Icons in `js/ui/icons.js` (add a triage icon).
  View contract: `render(state) -> markup`, `mount(root, state) -> cleanup` (see `views/kanban.js`).
- i18n: `js/i18n/en.js`, `js/i18n/fr.js` (flat dotted keys, `{name}` holes, `.one` plural suffix,
  `tn(key, n)`), registered in `js/model/words.js`. Spec decision: English + French. Add every new
  key to both files (they are ~225 lines each; will cross 300 lines, which is the Biome per-file
  cap `maxLines: 300`: split into `i18n/en-triage.js` + spread, or the cap fails. Same risk
  for `components.css`/`widgets.css`; check their lengths).
- File panel: `js/panel/panel.js` (`openPanel`, `closePanel`, `panelMarkup`, `syncPanel`, `bindPanel`),
  `file-view.js` (`fileView`, `bodyOf`; markdown rendered via `markdown.js`), `load.js` (`loadFile`
  fetches text via `fileText`; stores `panelFile {path, kind, text, cut, loading, failed}`), `files.js`
  (`viewKind`), `tree.js`, `head.js`. The Edit button goes in `file-view.js`; the sha256 must be
  captured in `load.js`/`api.fileText` (`res.headers.get(...)`) and kept in `panelFile`. The edit state
  (`panelEdit`) needs a `store.js` field. Backlog check for "Edit" visible: `panel.kind === 'item'` and
  `bucket` in the six backlog buckets (`model/targets.js` `ofItem` already sets `bucket`); file
  `.md`, not `STATUS.md`.
- Home tile slot: `js/views/home.js` has `export const TILES = [reviewTile, waitingTile, nextTile]`
  ("a later change adds a tile by adding a function to it"). Add `writtenTile` (uses `kpi()` from
  `ui/parts.js`, `go: 'triage'`). `kpi` tone `calm|go|hot`. CSS `css/views/home.css`.
- Kanban Intake column: `js/views/kanban.js` `column(col)` draws `<div class="colh">...<span
  class="place"></span></div>`; there is NO New button yet. Add the "+ New: a new idea" button only on
  the `intake` column (the `place` span of the header, or a first child of `.cards`). `kanban-cards.js`
  `itemCard` has two empty `<span class="place">` for "labels / origin badge" (fill them with
  `labels/tags.js`; mount via `bindOpen`).
- Header: `js/ui/header.js` exports `stats`, `title`, `notice`; `index.html` header is
  `<div>project-phone / h1#title / .stats / .notice</div>`; there is no button area. "+ New" needs a
  new slot in `index.html` header (right side, hidden on All projects: `state.project === ALL`) and on
  the phone beside `#project-phone`. Wire in `main.js` `listenToFrame` (delegate on `[data-new]`).
- Project picker: `js/ui/picker.js` `trigger(state, cls)` + `menu(state)`; no change needed except
  placing "+ New" next to `#project-phone`.
- Toast/dialog: nothing exists. New `js/ui/toast.js` and `js/ui/dialog.js` (+ `<div id="toast">` or
  appended to body, + CSS). `ui/host.js` mounts views; check it for the mount/cleanup lifecycle
  (a redraw replaces `#view`'s markup; drag state and dialogs must survive `draw()` by living in
  the store or in `<dialog>`s appended outside `#view`).
- Biome limits (`biome.json` at repo root, applies to all of `WEB/**`): max 300 lines/file, 50 lines
  and cognitive complexity 10 per function, max 5 params, `noImportantStyles` in CSS, single quotes,
  100 columns, no unused vars/imports. `just lint` runs
  `uvx --from nodejs-wheel==24.19.0 npx --yes @biomejs/biome@2.6.7 check WEB`. The prototype's JS
  style (long, dense) will not pass: write small modules.

## (3) Commands and where things live

- `SRC/commands/intake.py`: `file_cr(args)` (reads `@path` or text, BOM-strip decode, title from first
  non-blank line (`lstrip("# ")`), slug = `args.slug or slugify(title)`, `^[a-z0-9][a-z0-9-]{0,80}$`,
  `with changes_lock(repo): new_request(repo, slug, raw); write_dashboard(repo, paths)`; returns
  `["filed <shown path>; write the intent and grill the CR here"]`). `triage(args)` (changes_lock,
  `move_backlog_item(repo, item, priority, paths, ready=)`, `write_dashboard`). `abandon`, `restore`,
  `init`. Parsers: `SRC/declare/intake.py` (`triage` has a required mutually exclusive group
  `--priority P1..P4` / `--ready`; add `--inbox` there, `required=True` stays).
- `new_request` is in `SRC/commands/crs.py` (also `shown`, `slugify`): raises `ChantierError("CR folder
  already exists: ...", EXIT_PRECONDITION)` => 409 (matches spec). `commands.crs` imports
  `lifecycle.stages`, so a `lifecycle/backlog.py` that imports `commands.crs` would be a layer
  inversion/cycle risk (`tests/test_code_targets.py` checks no import cycle). Options for the Driver:
  move `new_request`, `slugify`, `shown` to `lifecycle` (or `core`) and re-export from `commands.crs`,
  or put `backlog.py` in `commands/` (not "layer 2"). Check with the test.
- `move_backlog_item(repo, item, priority, paths, ready=False)` is in `SRC/lifecycle/stages.py:264`
  (file is 254+ lines; limit 400 per file). It takes a PATH (`repo.planning_path(item, "CR folder")`),
  not a slug; source must be inbox, `2-backlog/P<n>/`, or `3-ready`. Usage message at line ~268:
  "triage takes --priority P<n> or --ready, one of them" (spec changes it to include `--inbox`).
  No inbox target today: add an `inbox=` flag (or a `to` string). `paths` = `stage_layout(repo)` dict
  with keys `inbox, ready, backlog, pending, actives, done, archives, trash, batches`; `PRIORITIES`
  also in stages.py; `cr_stage(paths, folder)`, `changes_lock(repo)` (file lock `.lifecycle.lock`,
  30 s), `cr_folders(paths)`.
- Dashboard: `SRC/status/write.py` `write_dashboard(repo, paths)`.
- `state.IGNORED`: in this tree it is `SRC/core/files.py:87` `IGNORED` (a tuple; `ensure_gitignore(changes)`
  writes missing entries to the planning folder's `.gitignore`; `Repo.ensure_gitignore` at
  `core/repo.py:206` calls it). There is also `SRC/board/state.py` (project state, unrelated: that is
  not `state.IGNORED`). Add `"board-journal.jsonl"` to the tuple. NOTE: `next-batch.json` is meant to
  be committed, so it is NOT added.
- Exit codes: `SRC/core/errors.py:5` `EXIT_USAGE=1, EXIT_PRECONDITION=2, EXIT_CONFLICT=3, EXIT_EXTERNAL=4,
  EXIT_BUDGET=5`. (Spec said "`state.py`"; it is `core/errors.py` now.) `ChantierError(msg, code)`.
- Atomic write helpers: `core/files.py` `write_file(path, text)` (tmp + `os.replace`, `newline="\n"`),
  `write_json`, `retry`, `read_text` (strips BOM), `try_lock/unlock`. An atomic JSONL append: open
  `"a"` + one `write` of a full line under `changes_lock` (no helper yet).
- Where `next-batch.json` and `board-journal.jsonl` live: `repo.changes` (planning folder root; in a
  surface each project's own `changes/` via `project.repo.changes`).

## (4) Checks and scenario

`just check` = `lint test release-notes` (justfile):
- Python: `uvx ruff@0.17.5 format --check skills`, `ruff check skills` (rules in `pyproject.toml`:
  E,W,F,I,B,UP,SIM,C90,PL,RUF,PGH004, line 100, max complexity 10, args 5, branches 12, returns 6,
  statements 50, nested blocks 3), `mypy --strict` (`uv run --locked --group dev --with mypy==1.20.0
  --with types-psutil mypy`), `uv lock --check`.
- JS/CSS: `uvx --from nodejs-wheel==24.19.0 npx --yes @biomejs/biome@2.6.7 check
  skills/chantier/scripts/cli/src/chantier/board/web` (`biome.json`; formatter + linter + css linter).
  So the spec's "ESLint/Stylelint/Prettier" answer is already realised as Biome (open point 9 resolved:
  the earlier board CRs shipped it; this CR adds none).
- Tests: `uv run --locked --group dev pytest -q` over `SRC/../tests/`: `test_code_targets.py` (every
  `*.py` under the CLI: max 400 lines/file, 50/function, no import cycle), `test_board.py`
  (hard-coded `MODULES` list and required web files), `test_cli_runs.py`, `test_cli_units.py`,
  `test_costs.py`, `test_plugin_files.py` (agents/cards identity, etc.). The spec's optional extra test
  (every module under the web folder reachable from `main.js`, no inline handler) does not exist.
  `just mod` is NOT needed (no `hooks/` or `types/`).
- Scenario: `scenario/run_scenario.py` (6233 lines, `just scenario` runs `--forge github` then
  `--forge gitlab`). Board section = `remote_board(w)` at line ~1146 ("## 16c. The remote board"),
  called from line 1042. Helpers: `BoardProc` (1045), `free_port`, `Link` (key/cookie), `fetch(port,
  path, method, headers, body)` (1100), `jget(port, link, path, headers)` (1113), `folder_state(root)`
  (1122), `exits`, `prepare_cr(w, title, priority)`, and `check(label, ok, detail)`. The section
  numbers its blocks (1. start ... 7. "nothing written": asserts the planning folder and
  `git status --porcelain` unchanged; 8 second board; 9 seat; 10 wider/clock; 11 chantier.yaml).
  The new write steps must go AFTER step 7 (otherwise "nothing was written" fails) and the existing
  `PUT answers 405` check (line ~1342) must change if PUT is allowed. The world has `board-inbox-item`,
  `board-backlog-item` (P2, BOM), `board-ready-item` (3-ready). The section already fetches
  `spec_dir` of CR `one` for file reads.
  Also add `triage --inbox` steps in the CLI part near line ~676 (existing `triage` step "the board
  shows ... what `triage` just moved"). S4 (last commit) lists top-level `chantier.yaml` keys; not
  affected.

## (5) Proposed split: two coder rounds

### Round 1: Python backend, cards/docs, scenario

Files (all under `SRC` unless noted):
1. `lifecycle/stages.py` (or new `lifecycle/backlog.py`): `move_backlog_item` gets the inbox target
   (`--inbox`, exclusivity, "is already in 1-inbox", "1-inbox already holds"), new usage message.
   `declare/intake.py`: add `--inbox` to the exclusive group; `commands/intake.py`: triage output
   `triaged 1-inbox/<name>`; help text. Keep stages.py under 400 lines.
2. `lifecycle/backlog.py` (new): `file_idea`, `move_item`, `edit_markdown`, `declare_next_batch`,
   `next_batch`, plus `set_labels`, `set_group` extracted from `commands/summary.py` (keep the CLI
   output/behaviour). Resolve the `commands.crs` import (move `new_request`/`slugify`/`shown` or keep
   backlog in a layer that may import them). `commands/intake.py:file_cr/triage` become thin callers.
   `edit_markdown`: item lookup among inbox/P1..P4/3-ready by slug, `.md`, not `STATUS.md`,
   `files.inside` confinement, sha256 compare on raw bytes, 1 MB cap, CRLF preserved, no BOM, atomic.
3. `core/files.py`: add `board-journal.jsonl` to `IGNORED`; maybe a bytes-atomic write helper.
4. `board/journal.py` (new): read since last rescan, append one JSON line, rescan.
   `board/write_api.py` (new): the 8 write/journal routes, JSON body parse, slug lookup in the 6
   backlog folders, per-item results, error mapping (400/409/415/403/500), journal line per write.
   `board/routes.py`: register routes (`PUT` or POST for the file), `guard.py`: PUT + 415 decision,
   `files.py`: sha256 header on `read`. `board/backlog.py`: `labels`, `group`, `origin`, `late` from
   `summaries.view.summary_view`; also expose `next_batch` and the journal count somewhere the page can
   read (either in the `state` payload, or `GET journal` + the marker through a small `GET
   backlog/next-batch`; the spec has the page compute the indicator from the marker, so the marker
   must be readable: add it to the state payload `project_state()` or a GET route), and make the
   fingerprint cover `summary.json`, `next-batch.json`, `board-journal.jsonl`.
5. `tests/test_board.py`: add `journal`, `write_api` to `MODULES`.
6. Cards/docs: `skills/chantier/references/chief-of-staff.md` (one row after the "board on my phone"
   row at line 41; mind the 1238-line file, and the Copilot twin rule: cards are shared, agent files
   are not touched), `skills/chantier/references/concepts.md` (Lifecycle ~line 85 and `3-ready` ~line
   91), `docs/boards.md` (web board section, line 68).
7. `scenario/run_scenario.py`: `triage --inbox` steps in the CLI section; new numbered block in
   `remote_board` after step 7: move chain with folder + journal checks, `backlog/new` byte equality +
   409 duplicate, file edit with hash + CRLF, stale hash 409, refusals (STATUS.md, `..`, non-md,
   `4-batch` slug, `5-archives` slug), `next-batch.json`, `journal/rescan`, no token / foreign Origin /
   `text/plain` refused, `git check-ignore board-journal.jsonl`, labels/group/move-out-clears-group;
   fix the `PUT` 405 check. Gate: `just check`, `just scenario` (both forges).

Round 1 is testable alone with `curl`/`fetch` against `chantier board` and needs no JS.

### Round 2: JS/CSS front

`WEB/js/api/backlog.js` (one function per route, `BoardWriteError`), `js/core/api.js` (export a `send`),
`js/ui/toast.js`, `js/ui/dialog.js`, `js/model/triage.js` (pure columns/groups/counts/indicator; the
spec's `triage/model.js`), `js/triage/{postit,drag,selection,groups,ready}.js`,
`js/labels/{filter,tags}.js`, `js/journal/journal.js`, `js/edit/{new-idea,markdown-editor}.js`,
`js/views/triage.js` (+ registry entry, icon, bottom bar), Home `writtenTile`, Kanban Intake button
and label tags in `kanban-cards.js`, header "+ New" slot (`index.html`, `ui/header.js`, `main.js`),
panel Edit button (`file-view.js`, `load.js`, store fields), words in `i18n/en.js`/`fr.js` (split to
stay under 300 lines), CSS `css/views/triage.css`, `journal.css`, `editor.css`, `dialog.css` and the
`index.html` links. Must pass the Biome caps. Gate: `just check`; the scenario only if round 1
changes or `index.html` structure assertions in it change (the scenario fetches `/js/main.js`).

### Evidence plan (E1-E7)

- E1/E2: `just check` locally (Windows) and CI; `just scenario` after round 1 and again after round 2.
- E3/E6: Playwright (or the in-session browser) against `chantier board` started on a COPY of the
  planning folder (never the live one), 1400x860 and 375x812, beside the prototype
  (`.agents/changes/2-backlog/P2/visualization-backend/prototype/index.html`, `?v=triage`/`?v=home`;
  the prototype's `evidence/prototype/v6-*.png`). Console-error capture across every action. Note
  that this repo's folder may have moved: find `visualization-backend` by slug (it is now
  `4-batch/2-actives/222-visualization-backend/`).
- E4: Playwright `drag_to` in Chromium and Firefox, or Known gap "drag and drop not verified by
  automation".
- E5: two browser contexts on one board.
- E7: needs `surface-autosync` merged and a scratch surface; otherwise `git status` shows only the
  uncommitted board writes (and the ignored journal).
- No AGENTS.md pane screenshot rule (no `hooks/register.tsx` or `STATUS.json` change).

### Risks / decisions to raise for the Driver

1. Setters are argparse-bound (section 1): refactor needed, keep CLI output byte-identical.
2. State payload lacks labels/group/origin/late and the marker/journal: the read API change is in
   round 1, not round 2.
3. `PUT` is 405 today, and a scenario step asserts it; pick PUT-with-guard-change or POST.
4. 415 vs the guard's current 403, and CSP `form-action 'self'` vs the spec's `'none'`.
5. CRLF and BOM: `write_file` forces LF; `textarea.value` normalises to LF; the server must restore
   the file's CRLF. sha256 is of raw bytes, but the file read endpoint strips the BOM: header must hash
   the bytes on disk.
6. `commands.crs` -> `lifecycle` import direction (cycle test) for `lifecycle/backlog.py`.
7. Biome 300-line file cap: `i18n/en.js`/`fr.js` (about 225 lines now) will overflow; plan a split.
8. The board's `Repo` is `readonly=True`; `changes_lock` still writes `.gitignore`, which is fine, but
   note it makes the board write `.gitignore` in the planning folder on its first write.
9. In surface mode each project has its own `repo.changes`; the journal and `next-batch.json` must be
   per project (use `project.repo.changes`), and the page's project id selects it.
