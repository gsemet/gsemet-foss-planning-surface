# Investigation CR-225: the board as CR-222 merged it, and what the reading views still need

Paths below are relative to the worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-17-CR-225`
unless absolute. `BOARD` = `skills/chantier/scripts/cli/src/chantier/board`. Facts read from the
code and from one run of `biome check`; nothing was changed.

## 1. Big surprise: the frame is not where or how the spec says

- The spec says `static/` (and `GET /` removing `render.py`). Reality: the frame is `BOARD/web/`,
  served by `BOARD/static.py` (module named `static`, folder named `web`). There is no `render.py`,
  `collect.py` or `server.py` (a test asserts they are gone). Decide once: keep `web/` (cheapest;
  `test_board.py`, `biome.json`, `justfile`, scenario already say `web`) and tell the Verifier
  "static/" in the spec = `web/`.
- The frame already holds a flat layout, not the spec's core/model/ui/views/panel layout:
  `web/index.html` (1.3 KB, no inline script/style, 3 stylesheets), `css/{tokens,frame,components}.css`,
  `js/{main,api,store,router,poll,frame,dom,i18n,icons,time}.js`, `js/i18n/{en,fr}.js` (the "one word
  file per language" decision is already done: it replaces the spec's `model/words.js`),
  `js/views/{home,kanban,batch,costs,triage}.js` (stubs). `frame.js` (5.6 KB) does sidebar, header,
  bottom nav, notice, foot in one file with a `put()` memo that skips unchanged markup (this is the
  "keep focus on refresh" device).
- View contract today: a view exports `title` (i18n key) and `render(state, root)` (it writes
  with `setHtml`); no `mount`, no cleanup. The spec wants `render(state)` returning markup + optional
  `mount(root, state)`. `frame.js` `paintBody` redraws the whole view whenever `state` identity
  changes (a new object only when the ETag changed, so "no redraw when unchanged" already holds).
- `router.js` `VIEWS = ['home','triage','kanban','batch','costs']` and `triage.js` stub exist,
  but Triage is `board-backlog-edit`'s: remove it from VIEWS/nav in the registry step (registry.js
  becomes the single list). The router resolves `p` against `board.projects`; no `p=*` yet.
  `LAST_KEY='chantier.project'`, `chantier.lang` in localStorage (router.js / i18n.js write them;
  spec says router/store only).
- `dom.js` already is the spec's `dom.js`: `html` tag escaping, `raw`, `esc`, `setHtml` as the one
  `innerHTML`, `$`, `$$`. `api.js`: only module with `fetch`; `get(path, etag)` returns
  `{changed, etag, now, data}`; only `board()` and `projectState(id, etag)` exist. `poll.js`:
  5 s interval while visible, `If-None-Match`, 304 -> `changed:false`, notice after 2 fails,
  drops a late answer for another project. `time.js`: `span`, `ago(iso, nowIso)`, `waited`; ages use the
  server's `now` (good for "Data: N min ago").
- Mojibake in the files as printed by PowerShell (`â€”`, `Â·`, `FranÃ§ais`) is only my console's
  CP1252 display; files are UTF-8. Not a bug, but the coder must read/write with UTF-8.
- Existing icons set `icons.js` (1.6 KB) is small: the prototype's `IC` set is to be ported.
- i18n key rule: `test_code_targets` asserts en/fr share the same keys (regex `'key':` per line).
  A multi-line value like `'notice.silent':\n 'text'` still matches.

## 2. The server (BOARD/*.py), exact shapes

CLI start/policy: `command.py` (5.2 KB, `chantier board`), `address.py` (URL), `key.py`
(`.git/chantier/board.json`), `guard.py`, `app.py` (Starlette, lazy), `context.py`, `seats.py`
(`POST /api/seats` keeps the board alive while a seat exists), `projects.py`.

Auth/policy: every route needs the key (cookie `chantier_board`, or header
`X-Chantier-Board-Key`; `/?k=` 303 to the clean URL + HttpOnly SameSite=Strict cookie). POST needs
same-origin + JSON body. Every reply: `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`,
`Referrer-Policy: no-referrer`, `X-Chantier-Now` (the server's instant). **CSP only on text/html**:
`default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; connect-src 'self';
base-uri 'none'; form-action 'self'; frame-ancestors 'none'` (`reply.py`). Static files (`static.py`):
`Cache-Control: no-cache` + size-mtime ETag, `304` on match; types from a fixed `TYPES` map (.html
.js .css .svg .json .ico .png .woff2; others 404); anything under `web/` not a mapped type is 404.

Routes (`routes.py`):

| Route | Returns |
| --- | --- |
| `GET /api/board` | `{board:true, version, surface:bool, served, seats, projects:[project_line], now}` |
| `GET /api/projects/{id}/state` | ETag = fingerprint (a `stat` walk of `1-inbox 2-backlog 3-ready 4-batch`, shallow `5-archives 6-trash`, `seat.json`, plus the live-cost mark), `304` on `If-None-Match` (weak, list, `*`). Body: state below + `now`. Asking it also triggers the 5-min cost rule (`live.ask`). |
| `GET /api/projects/{id}/tree?path=` | `{path, files:[{path,size,kind}], now}`: every file under the folder, recursive, sorted by path; `path` relative to the planning folder; `kind` = text / image / other; locks left out; 404 outside |
| `GET /api/projects/{id}/file?path=` | text -> `text/plain; charset=utf-8` (UTF-8 BOM removed; cut at 1 MB, header `X-Chantier-Cut: 1`); image (png jpg jpeg gif webp, <=5 MB) -> its own type, so an `<img src="file?path=...">` works under `img-src 'self'`; **everything else (svg, html is TEXT so text/plain; svg is "other") -> `application/octet-stream` + `Content-Disposition: attachment`** = the download link. |
| `GET /api/projects/{id}/costs` | `{recorded:{spent_usd,budget_usd,unpriced,per_cr:{cr:usd},at}, live:{at,error,spent_usd,unpriced,per_cr:{cr:{calls,usd,unpriced}},computing}|null, now}` |
| `POST /api/projects/{id}/costs/recompute` | `202 {computing:true}`; `costs.Live.start()` runs a thread, one at a time, in memory, never writes |

Live refresh form = **client polling of `/state` with ETag** (no SSE/WebSocket). Costs on demand =
exists (`recompute`); the 5-minute rule is `costs.RULE_S=300`, run when a page asks a running batch.
So "Recompute" is drawable (open point 4 resolved: yes); poll `/costs` until `live.computing`
is false (the scenario does the same, `settled_live`).

`state` body (`state.py project_state`): `project, surface, seat{title,env}|null, batch|null,
events (last 40 of 12 kinds, keys t actor kind cr result pr note order_kind reason command round),
backlog{inbox,P1..P4,3-ready: [{item,title,folder,files,depends,description,grill}]}, merged,
merged_total, trashed, trashed_total, history (batch records), live`.
`batch`: `id, state, mode, steering, spent_usd, budget_usd, unpriced, priced, heartbeat,
heartbeat_stopped, asks_unread, orders_pending, created, default_branch, max_rounds,
slots{taken,total}, cost_at, merge_order[cr...], crs[]`.
`crs[]` (`crs.py _row`): `cr, title, folder, state, label, severity, round, round_limit, cost_usd,
cost_unpriced, pr (http(s) only), blocked, waits, kind (fix|release|null), order, stacked, after,
merged_at, handed_back_at, files, description, chain_place, base{on,why: stack|dependency|planned|
series|default}, to_review`.
`merged[]` (`status/views.py _past/_done_rows`, 50 max, `PAST_LIMIT`): `cr,title,state,batch,pr,
cost_usd,when,path` (the batch's `3-done` ones first, `when`=`merged_at`; archived ones `when` is the
folder-name timestamp).
`project_line` (picker/overview): `id, batch{id,state,mode,steering}|null, running, working[{cr,title,pr}],
blocked[...], to_review[...] (in merge order), merged (count), total, spent_usd, budget_usd,
unpriced, inbox, backlog, by_priority, cost_at, heartbeat, heartbeat_stopped`.

Already provided by the server, so NOT to add: description (first paragraph, `backlog.py`: skips
headings/`issue:`/fences, strips marks, 300 chars, one read per state build, cached by fingerprint),
file counts (CRs and items), `round_limit`, `max_rounds`, `default_branch`, slots, `created`,
`heartbeat(_stopped)`, `asks_unread`, `handed_back_at`, `merged_at`, base/chain/to_review/merge_order
(Semantics largely computed server-side: the JS `semantics.js` may read these instead of
recomputing; the spec's "pure model" still holds for levels, state groups, hints), events 40,
tree/file/images/downloads, recompute, CSP.

## 3. Facts the views need that the server LACKS (where to add)

1. **Stack verified on the forge** (`crs.py _row to_review`, `state.py _batch`): nothing in the
   record carries it (only `VERIFIED` verdict events, which are a different thing). Today
   `to_review = ready and base.on == default_branch`, so a stack's PRs are drafts: exactly the
   spec's "while the server has none". Do not invent a field. Add to `_batch` only if a record
   source exists (none found); otherwise leave it out and list it in the PR's Known gaps. Needs the
   CoS to confirm. If a field is added: `to_review` in `_row` becomes
   `ready and (base.on == default or (mode=="stack" and kind!="fix" and stack_verified))`.
2. **`updated` per CR** (merged-time fallback; open point 8 fallback for parallel order):
   add `"updated": c.updated` to `crs.py _row`.
3. **`branch` per CR** (spec "What the views read"): add `"branch": c.branch` to `_row` (cheap;
   `_on()` already uses branches).
4. **Overview ("All projects") per project**, in `state.py project_line`: `asks_unread`
   (for "Waiting for you"), `last_event_at` (open point 7, "Data" = last event time:
   `events[-1].t` from `project_state`; needs the events, so compute in `project_state`/`_batch`
   and pass), `slots` (taken/total, optional), `heartbeat` kind is there. The overview card needs
   "N PRs to review", "N working", spent, intake: present.
5. **Steered here or not**: no explicit flag; "no batch" (`batch: null`) is what the spec wants shown,
   so nothing to add. `project_line.id` is the project name (no separate display name).
6. **Merged CRs "at least 8, total count"**: present (`merged` 50, `merged_total`).
   Note a merge `when` from an archive is the folder's minute-resolution timestamp; fine.
7. **Backlog item: `priority` is the bucket key** (not a field), and `has_spec` / `has_answers` are
   folded into `grill` (`raw|grill|specifying|specified|automatable`): enough for the pipeline; the
   `specifying` state counts as "in grill" in the JS (open point 13).
8. **Event kinds**: `cost` is not in `EVENT_KINDS` (right: the feed does not show it). `pause`
   is included; the prototype's `evText` has no `pause`: map it as "note"-like in `model/events.js`.
9. **Cut flag** for a long text arrives as the header `X-Chantier-Cut: 1`; `api.js` must expose it
   (`get` returns JSON only today): add a `getText(path)` that returns `{text, cut}` and an image
   URL builder (`file?path=`) relative to the page.
10. Nothing else is missing: no change to `STATUS.json` or `register.tsx`. All Python edits stay
    <=400 lines/file, <=50 lines/function (`test_code_targets`, ruff, mypy).

Edits to the Python are therefore tiny (items 1-4, plus tests/scenario checks for the fields).

## 4. The prototype (found)

In the main checkout, CR-222's folder (active, not archived):
`C:\Users\gaeta\Projets\chantier\.agents\changes\4-batch\2-actives\222-visualization-backend\`
- `prototype/index.html` 101,022 bytes (1114 lines)
- `prototype/README.md` 1,501 B; `prototype/snapshot.py` 5,083 B; `prototype/data.js` 1,550,727 B (generated)
  `prototype/compare.html` 992 B; `prototype/v1/` (older)
- `evidence/prototype/v6-01..v6-24` (jpg/png, 5-74 KB each), e.g. `v6-12-semantics-batch-pc.jpg` 47,726 B,
  `v6-13-semantics-kanban-pc.jpg` 48,687 B, `v6-14-semantics-batch-phone.jpg` 43,203 B,
  `v6-16-all-projects-home-only-pc.jpg`, `v6-17-all-projects-home-only-phone.jpg`.
The worktree does not contain `.agents/changes`; coders read the prototype by the absolute path
above (it will move to `5-archives/` when CR-222 merges; then use the slug).
`index.html` at 101 KB is too big to read whole: slice by function (`home`, `kanban`, `batch`,
`modeBar`, `prCols`, `drawEdges`, `costs`, `openPanel`, `showFile`, `md`, `allProjects`, `evText`,
`levels`, `IC`, `:root`).

## 5. Existing checks of the board and what would change

- `cli/tests/test_board.py` (3 tests): MODULES list present; no `collect/render/server`; lazy
  imports of `starlette/uvicorn`; frame shipped files exist: `index.html js/main.js css/tokens.css
  js/i18n/en.js js/i18n/fr.js`. Changes only if files are renamed/moved (they need not be). Add a new
  module name here if a Python module is added (none planned).
- `cli/tests/test_code_targets.py`: Python <=400 lines/<=50 per function, no cycle; test 4 =
  every `web/js/**/*.js` <=300 lines and en/fr key equality. **Spec says 400 lines; the repo already
  enforces 300 (JS) and Biome 300**: keep 300 (stricter), tell the CoS. Add here the spec's one
  structure test: every `<link>/<script>/import` of `web/` resolves inside `web/` (regex over
  `href`, `src`, `from '...'`), no `http(s)://`/`//` origin in any web file, `index.html` has no
  inline `<script>` body / `style=` / `<style>` / `on\w+=`, CSS <=300 (or 400) lines, no `#id`
  selector, no hex colour outside `tokens.css`, CSS nesting depth <=3, no `innerHTML =` outside
  `dom.js` (E3). These CSS checks are not in Biome (see 6).
- `scenario/run_scenario.py` step 16c `remote_board` (line 1118+, big, key/guard/cookie/state/
  files/costs/seats): checks `GET /` = HTML UTF-8 with `script-src 'self'`, no `unsafe-inline`,
  nosniff; `/js/main.js` JS type + ETag + 304; the API shapes (rows hold `label`, `round_limit`,
  `after`, `chain_place`, `base`, `to_review`; markup in a title comes back as text; BOM cleaned;
  tree/file/lock/image checks). To add for E2: (a) fetch every `.js` and `.css` the page imports
  (parse `index.html` + each module's `import ... from './x.js'` recursively) and assert 200 and
  `text/javascript`/`text/css`; (b) assert the policy has `style-src 'self'`, `img-src 'self'`,
  `connect-src 'self'` and no `*`/`http:`; (c) assert the new row fields (`updated`, `branch`,
  `last_event_at`, `asks_unread` in a project line). Keep it concise: scenario step is already long.
- `just lint` (justfile): `uvx ruff@0.17.5 format --check skills`; `ruff check skills`; mypy
  1.20.0; `uv lock --check`; and the web frame:
  `uvx --from nodejs-wheel==24.19.0 npx --yes @biomejs/biome@2.6.7 check skills/.../board/web`.
  I ran that Biome command on this Windows machine: passes ("Checked 21 files"). So Node from
  PyPI via uvx works on Windows, and CR-222 already chose Biome (the post-spec decision "ESLint,
  Stylelint, Prettier ... or Biome if simpler" is settled for Biome: no ESLint/Stylelint/Prettier
  to add).

## 6. Biome (2.6.7) against the targets

`biome.json` (repo root): root:true, vcs off, `files.includes: board/web/**`; formatter space/2/
width 100/lf, single quotes, semicolons always; linter `recommended` preset + `noVar`, `useConst`,
`style/noExcessiveLinesPerFile` error max 300, `complexity/noExcessiveLinesPerFunction` error max 50;
assist on. It lints and formats **JS and CSS** already (Biome 2 handles CSS; HTML not linted).

| Target | Biome | Verdict |
| --- | --- | --- |
| file length | `style/noExcessiveLinesPerFile` (JS; set already, 300) | covered (JS) |
| function length | `complexity/noExcessiveLinesPerFunction` (set, 50) | covered |
| complexity <=10 | `complexity/noExcessiveCognitiveComplexity` (`maxAllowedComplexity: 10`), **cognitive, not cyclomatic**: close, stricter in nesting; no cyclomatic rule in Biome | add rule, document "cognitive" in CONTRIBUTING |
| params <=5 | `complexity/useMaxParams` (since 2.2, `max: 5`) | add rule |
| nesting <=3 | **no Biome rule**; cognitive complexity penalises nesting | not exact; cover via cognitive limit, or a small AST-free brace-depth check in the structure test (JS arrow callbacks make it noisy: prefer the cognitive rule and say so) |
| eqeqeq | `suspicious/noDoubleEquals` (recommended, error) | covered |
| unused variable | `correctness/noUnusedVariables` (recommended; make `error`), `noUnusedImports` | covered (raise to error) |
| undeclared global | `correctness/noUndeclaredVariables` (error by default; browser globals known; add `javascript.globals` if a rule trips) | covered |
| format 100 cols | formatter lineWidth 100 | covered |
| CSS `!important` | `complexity/noImportantStyles` (recommended, warn: set `error`) | covered |
| CSS id selector | **no Biome rule** (`noIdSelector` unrecognised) | structure test regex `^[^{]*#[A-Za-z_-]` outside values |
| CSS nesting <=3 | **no rule** | structure test (count `{` depth) |
| CSS file length | `noExcessiveLinesPerFile` is JS-only | structure test |
| CSS colours via tokens | none | structure test (hex/rgb( outside `tokens.css`) |
| CSS formatted | Biome CSS formatter | covered |
| HTML rules | not linted | structure test |

Warnings become failures only if the rule is `error`: `biome check` exits 1 on an error-level
diagnostic, 0 on warn/info, so set each new rule to `"error"` (as `noExcessive*` already are).
Since Biome stays, no second tool; `justfile` needs no change except the path if `web/` moves.

## 7. Evidence plan (the Verifier keeps outputs in `work/verifier/evidence/`)

- **E1** `just check` (Windows now, then CI x3): includes the `lint` Biome line and
  `pytest` with the new structure test. Capture the "Checked N files ... No fixes" line.
- **E2** `just scenario` (both forges); the step 16c lines for: `GET /`, each static module 200 with
  its type, policy self-only, new row fields.
- **E3** table: `Get-ChildItem -Recurse BOARD\web -File | % { "$($_.FullName.Substring(...)) $((Get-Content $_ | Measure-Object -Line).Lines)" }`;
  `rg -n "innerHTML\s*=" BOARD/web/js` -> only `dom.js:setHtml`.
- **E4** scratch planning folder (`uv run --script chantier.py` with a temp git repo, as the
  scenario's `World`): `triage`/`file` a CR with the three markups; open the board
  (`chantier board --port 0`), open with Playwright (uv script, not committed), assert no
  `dialog` event, console clean, `evil.svg` listed and downloaded as attachment.
- **E5** board on `222-visualization-backend`'s own folder: open its panel (needs the folder under
  the served planning folder; it is under `.agents/changes/4-batch/2-actives/222-...` of the main
  checkout, serve `chantier board` from there), check the tree: top .md, `evidence/` with nested
  images, `intake/`, `prototype/` with `v1/`, `work/`; `data.js` (1.5 MB) listed as a text-kind
  file by extension (`.js` is in the server's TEXT set, so the server **will** serve it as text: the
  panel must not show `data.js` as text per the spec: either a size cap in the panel (>1 MB treated
  as "listed by size") or kind rule: decide, spec says "never shown as text"; the server cut at 1 MB
  gives a "cut" line otherwise).
- **E6** CLI `note`/`round`/`triage` against a running board: `Invoke-WebRequest` the `/state` ETag
  changes within 5 s and the page (Playwright) redraws with the panel still open.
- **E7** scratch folders made with the CLI per case (parallel, series, stack with a CR not stacked,
  `after`, fix, release, blocked with a reason, queued waiting): `chantier batch ... --mode`; one PC
  screenshot each.
- **E8** `chantier board` on the repo's planning folder (no picker) and on a scratch surface of 3
  projects (picker, overview).
- **E9** `$env:UV_CACHE_DIR`, `$env:npm_config_cache` set to new empty folders outside the repo, then
  `just lint`, with `uvx --from nodejs-wheel==24.19.0 npx --yes @biomejs/biome@2.6.7 --version`
  printed.
- **E10** throwaway uv script (Playwright + Chromium inline deps) with 1400x860 and 375x812 mobile
  shots of the prototype (`prototype/index.html` + a `data.js` from `snapshot.py`, needs a running
  batch in the folder) and the board; side-by-side `compare-<view>-<pc|phone>.png` captioned with
  the `v6-xx` and the 7-character head SHA; checklist table per view.

## 8. Proposed slices (each small enough for one coder with limited context)

**Slice A: server additions and checks (Python only, ~60 lines).**
`crs.py _row`: add `updated`, `branch`. `state.py`: `last_event_at`/`asks_unread` into the
overview line; `to_review` gate only if CoS names a stack-verified source. Scenario 16c: new field
asserts, static-modules loop, CSP asserts. `test_board.py` untouched. Confirm item 1 with the CoS
before coding it.

**Slice B: tooling and core.** Biome rules (`useMaxParams` 5, `noExcessiveCognitiveComplexity` 10,
`noUnusedVariables`/`noImportantStyles` as error, `noExcessiveLinesPerFile` stays 300); the
structure test (CSS/HTML/imports/origin/id/nesting/colours/innerHTML); `CONTRIBUTING.md` "Code
standards" JS/CSS part. JS: extend `api.js` (file text + cut, image URL, costs, recompute, tree),
`format.js` (money, size, ages, local HH:MM, PR number, slug), `store.js`/`router.js` (view `'*'`
project, overview hiding rule), `views/registry.js`, `model/{semantics,grill,events}.js` (pure),
`ui/{icons,parts}.js` port of the prototype's `IC`, tokens/base/components CSS from the prototype's
`:root`. Move frame.js into `ui/{sidebar,picker,bottombar,header}.js` (each small).

**Slice C: views.** One commit per view: `home.js` (+`home.css`), `kanban.js`, `batch.js` +
`batch-graph.js` + `batch-prs.js`, `costs.js`, `overview.js`. Each view reads the prototype's matching
function and screenshot. Order: Home, Kanban (cards shared with graph nodes via `parts.js`), Costs,
Batch (largest: split graph/prs), Overview + picker. Keep each file <=300 lines (limit in force).

**Slice D: panel.** `panel/{panel,tree,markdown}.js` + `panel.css`: tree grouping by first-level
folder, first file opened (03 spec, 01 intent, STATUS.md, first .md, first file), markdown renderer
(escape first), JSON pretty, images through `file?path=`, `X-Chantier-Cut` line, text >1 MB policy
for `data.js`. Hooks `Escape`, Tab/Enter.

**Slice E: QA tools and evidence.** Not committed: Playwright shot scripts, scratch folders for
E4/E7/E8, compare images, checklist, PR body. Includes the phone layout checks (bottom bar, 86% swipe
columns, panel fullscreen) and the "Board unreachable" foot wording.

Open flags for the CoS: (1) `web/` vs `static/` naming; (2) 300 vs 400 JS lines (keep 300);
(3) stack-verified has no source in the record (stack PRs stay drafts); (4) Biome (not ESLint) is
the lint tool and has no nesting/CSS-structure rules (structure test fills them); (5) `data.js`
is a `.js` text file the server will serve as text.
