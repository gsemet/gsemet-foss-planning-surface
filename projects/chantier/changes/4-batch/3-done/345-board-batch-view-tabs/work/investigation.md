# CR-345 investigation: Batch page tabs (graph, Gantt, time cards)

Read-only map, in the worktree `C:\Users\gaeta\Projets\chantier.worktrees\batch-24-CR-345`
(base: CR-344's head `6f63babc`). `<cli>` = `skills/chantier/scripts/cli/src/chantier`,
`<web>` = `<cli>/board/web`, `<tests>` = `skills/chantier/scripts/cli/tests/` (NOT a root `tests/`).

## 0. Findings that change the spec's text (read first)

1. **`board-design-system` is already in the base**: `ui/card.js` `card(parts)` (it already takes
   `priority`, `variants`, `top`, `body`, `meta`, `end`, `foot`), `ui/parts.js` `priorityChip(bucket,
   {button,on,attrs})`, `css/components/{card,chip,column}.css`, `DESIGN.md` (283 lines),
   `tests/test_board_design.py`. Nothing to wait for.
2. **`card-stamp` cannot be written outside `ui/card.js`.** `test_board_design.py::test_one_card`
   (`check_card`) refuses any class list holding `card` or `card-*` in any script but `ui/card.js`
   and `i18n/`. So the spec's "`card-stamp` parts with merged/ready/working/rework variants" needs
   either a new `stamps` part in `card()` (builds `<span class="card-stamp card-stamp-merged">`) or
   a non-`card-` class (`stamp`). Smallest: a `stamps` part in `card.js` (about 8 lines), the
   `paper` variant passed as `variants: ['paper']` (already supported, gives `card-paper`).
   Update card.js's header comment (it lists the variants) and DESIGN.md's component row.
3. **No orange in the prototype.** `intake/prototypes.html` has `--red #c8352b`, `--accent`,
   `--stamp #4b3f9e` (violet) and nothing orange; the "working" stamp is violet dashed. The spec
   line "`--stamp-rework` (the value of the prototype's orange)" has no value to take. Candidates in
   `tokens.css`: `--state-waits #d08a1f` (amber), `--autosync-approval #b86e0c`, `--warn-ink #8a5208`.
   Needs a decision (see Q1). The prototype's stamp ink is violet `#4b3f9e`; the board's
   `--state-local #8b6bd8` is the nearest violet but means "ready locally".
4. **`--stamp-ink` is already a name**: `css/views/costs-stamp.css` declares a local custom property
   `--stamp-ink: 0.8` (an opacity) on `.ticket .stamp`. A new token `--stamp-ink` (colour) in
   `tokens.css` would collide in meaning there (the local one wins inside `.ticket .stamp`, but it
   is confusing). Pick another name (`--stamp-hand`) and do not touch costs-stamp.css.
5. **`tests/test_code_targets.py` bans `https?://` in any web file**, so no `xmlns="http://www.w3.org/2000/svg"`
   and no `createElementNS`. Draw the Gantt SVG as markup through `html` + `setHtml` (inline SVG in
   HTML5 needs no xmlns), as `batch-graph.js` does for `svg.edges`.
6. **The demo has none of the data the new tabs show** (`docs/demo/projects/shop-api/changes/4-batch/events.jsonl`,
   49 lines): no `add` has `origin` (chips would be absent), no `phase` event (no inspector or
   verifier stamps), no `pr-draft`. It does have `round` 1..3 (CR-145 reaches round 3 at 10:26:15,
   clock 10:30: the REWORKED stamp and the burst show), `order merged` for CR-141 with `merged_at`
   09:12:40, `handback blocked` (CR-146), `handback ready`, `verdict`. The doc screenshots need the
   demo's events enriched (add `origin` to the 9 `add` lines, a few `phase` lines, one `pr-draft`).
   That also changes the existing `batch-pc/phone.png` (chips appear): retake them.
7. A `take` for a batch has `cr: null` (`commands/driver.py:82`, "take stack"): filter `e.cr == c.id`
   as the spec says; it already ignores it.

## 1. Files and entry points (what exists)

### Python

| File | Lines | What | Touch |
|---|---|---|---|
| `<cli>/board/crs.py` | 121 | `_row(repo, d, c, events) -> dict` builds one row (keys: phase, cr, title, folder, state, readiness, round, cost_usd, pr, after, merged_at, updated, handed_back_at, gate...). `cr_rows(repo, d, events)` is the only caller of `_row`, itself called only by `state._batch`. `handed_back_at(events, cr)` is the pattern to copy (list-comp over `events` with `e.kind`, `e.cr`, `e.result`). | add `"times": cr_times(events, c)`, `"priority": priority_of(events, c)` to the dict |
| `<cli>/board/state.py` | 244 | `project_state` reads `events = read_events(folders[0])` once, passes it to `_batch` -> `crs.cr_rows`. `_events()` keeps 40 events of `EVENT_KINDS` (no `phase`, `pr-draft`, `cancel`, `round`...is in; `phase` is not). `_batch` already puts `"created": d.created`. | none |
| `<cli>/board/times.py` | new | `cr_times`, `priority_of` | new, < 400 lines, functions < 50 |
| `<cli>/core/records.py` | | `EventRecord(t, actor, kind, cr, phase)` + extras read as attributes, `None` when absent (`e.order_kind`, `e.result`, `e.origin`, `e.round`, `e.draft`, `e.restart`). `CrEntry(id, status, merged_at, round, ...)` all defaulted: a unit test builds `CrEntry(id="CR-1", status="merged", merged_at=...)` with no repo. `read_events(folder)` skips a half line. | none |
| `<cli>/board/fingerprint.py` | | ETag from the changes folder entries (events.jsonl included): a new event changes the ETag, so the page reads fresh data. | none |

**Events that exist** (`log(kind, cr, **fields)`, `core/batch.py:183`): `add` (title, path,
**origin** = `repo.rel(prepared.directory)`, `commands/opening.py:52,75`), `take` (note, `restart: true`
on a retake of a CR already `working`), `round` (`round` = new `c.round`, round starts at 0 so the
first event is round 1, note, worktree print), `phase` (`phase` from `core/phases.py` PHASES:
investigator, coder, inspector, review, debugger, conflict-resolver, rebase, gate, pr, ci, verifier,
release; `note` detail), `pr-draft` (`draft` bool), `verdict` (`result`, `head`), `handback`
(`result`: ready, blocked, merged), `order` (`order`, `order_kind`: merged, drop, rounds, budget...,
`note`), `cancel` (killed, path), `gate`, `ship` (pr, base, head), `ask`, `note`, `cost`, `heartbeat`,
`depends` (after). Matches every kind the spec's table uses; field names in the spec are right
(`order_kind`, `result`, `draft`, `round`, `phase`).
- `merged_at` is on the batch entry (`CrEntry.merged_at`), set at merge; `order merged` carries no
  `merged_at` (the entry's wins, spec rule holds).
- A CR can be merged with `handback result: merged`? `driver.py:236` logs `handback` with the
  result arg for a released release CR; keep the spec's rule for it.
- Edge the spec leaves implicit: a `take` after `blocked` or after `handback ready` (a new Driver)
  re-opens `working`; `take` on an already-working CR has `restart: true` and changes nothing (state
  stays working: "a segment opens only when the state differs" covers it).
- `round` event of round n while state is `working` is a no-op for segments; `phase inspector`
  must be matched with `e.phase` (a declared field, not `e.get`).

### Web (`<web>`), with the limits

Limits: scripts 300 lines (`MAX_SCRIPT_LINES`, `test_the_web_frame_has_small_scripts...`), sheets 300
(`MAX_STYLE_LINES`, incl. `tokens.css`), CSS nesting 3, no id selector, no colour outside
`tokens.css`, Python files 400 / functions 50.

| File | Lines now | Role / hooks |
|---|---|---|
| `js/views/batch.js` | 97 | `render(state)`, `mount(root)` (called ONCE per `project|view` by `ui/host.js`, not per paint; cleanup returned), `after(root, state)` after every paint. `recorded(rec, state)` for a closed record; `rowsNow()` reads `snapshot()`. Imports `graphBlock`, `drawEdges`, `bindLight`, `bindGateLinks`, `prsBlock`. |
| `js/views/batch-graph.js` | 148 | `legend()` (the `.lgrow` pill + `batch.legend_hint`), `graphBlock(rows, batch, now, recorded)` = `legend()` + `.gscroll > .graph > svg.edges + levels`, `node(c, batch, now)` and `recordedNode(c)` via `card({classes:'node', variants:['compact'], attrs, top, title, body, meta, end, foot})`, `level()`, `path()`, `marker()`, `light(root, rows, id)` (module var `lit`, loops `$$('.node')`), `drawEdges(root, rows)` builds `paths` from `rows.flatMap(c => c.after...)` (the spec's `edges(rows)` extraction), `bindLight(root, rowsNow)` (delegates on `.node`). Moving `legend()` out leaves it at ~140; the burst icon + chip add ~10. |
| `js/views/batch-pr-card.js` | 84 | `prCard(c, batch, index, draft)` via `card({as, classes:'prc', variants:['clamp', draft && 'draft'], top: ...})`: add `priority: c.priority`. |
| `js/ui/card.js` | 55 | see finding 2; part `priority` already puts the chip first. |
| `js/ui/parts.js` | 82 | `priorityChip`, `stateIcon`, `stateColor`, `tag`, `empty`. |
| `js/ui/icons.js` | 57 | `PATHS` map + `icon(name)`; add `spark` (an outline in `currentColor`). |
| `js/core/router.js` | 133 | `resolve(projects, search)` returns `{project, view, batch}`; `href(place)`; `batchOf(place, now, project, view)` (exported, `BATCH_VIEWS = ['costs','batch']`); `go(place,{replace})`; `apply(place)` -> `update({project, view, batchId, ...})`; `settle`; `listen()` popstate -> `apply(settle(resolve(board.projects)))`. Add `tab` next to `batch` in all five, with a `tabOf` twin of `batchOf` (kept when `place.tab === undefined` and view is `batch`, and also when `place.batch` is set, so the batch navigator keeps it; null for any other view; `ALL` project clears it as it clears the batch in `settle`). |
| `js/core/store.js` | 54 | add `batchTab: 'graph'` to `data`. |
| `main.js` | 170 | click delegates (`[data-batch-go]` -> `go({batch})` at l.113). The tab click is the same shape: `[data-tab]` -> `go({tab})`, wrapped in `guarded(...)`, or bound inside `batch.js` `mount` with `delegate` + `go` (keeps main.js small). |
| `js/model/semantics.js` | 238 | add `edges(rows)` next to `related`, `levels`; `vstate`, `STATE_ORDER`, `related(rows,id)`, `mergedAt` exist. |
| `js/core/format.js` | 70 | `hhmm(iso)` (local time, 24 h) exists: use it; `age(iso, nowIso)`; `span`; `prNumber(url)`; `usd`; `slug`; `title`. No short-date helper: add one (`shortDate(iso)`) here (≈6 lines) for the time card and day ticks. |
| `js/ui/open.js` | 33 | `opener(key, scope)`; `bindOpen(root)`. Use scope `gantt-` and `tc-` so `data-key` (focus restore in `paint`) stays unique per tab. |
| `js/core/paint.js` | 50 | `paint` skips a redraw when the template text is unchanged and restores focus (by `data-key`) and scroll (by `data-scroll`). So: drawing measured overlays after paint (as `drawEdges`) survives polls; a tab change changes the text so it redraws and `after` must redraw the overlay. The Gantt's scroller wants `data-scroll="gantt"`. |
| `js/i18n/en.js` / `fr.js` | 260 / 261 | merged with `...board, ...prs, ...costs, ...write` (l.232-235): add `import batch from './en-batch.js'` + `...batch`. Test key-equality is over files matching `en*.js`/`fr*.js` in `i18n/` (regex `^\s*'([\w.]+)':`), so `en-batch.js`/`fr-batch.js` are picked up. Keys in the file must be single-quoted `'a.b':`. Existing: `batch.legend`, `batch.legend_hint`, `batch.hover`, `state.<s>` etc. |
| `index.html` | 78 | sheets linked l.8-41; insert the two new ones after `css/views/batch-graph.css` (l.31). |
| `css/views/batch.css` | 150 | tab bar layout goes here (flex, gap); `.lgrow`, `.lgpill`, `.note` live here. |
| `css/views/batch-graph.css` | 91 | `.batch svg.edges path` stroke `var(--edge-line)` 1.4, `.hl` accent, `.dim` opacity .15, `.head` fill `--edge-arrow`; add `.spark`. |
| `css/components/card.css` | 184 | `paper` variant + stamps (about 80 lines) fits under 300. Existing variants `card-compact` (nowrap top row, 2-line clamp), `card-dim` (opacity .28), `card-highlight` (halo ring). `.card` has `overflow: hidden` and `position: relative`: a tilted stamp placed inside must stay inside the box or it is clipped (design the stamps to sit in the card's padding area; the meta band is `margin: ... calc(-1 * ...)` flush with the bottom). |
| `css/components/chip.css` | 257 | toggle form is only the priority one: `button.tag` (border 1px `var(--edge, var(--chip-2))`) and `.tag.off`; `priorityChip(bucket,{button:true,on,attrs})` is hard-wired to `pri-<bucket>`. A tab is not a priority: a neutral tab chip needs `tag` + a new neutral "on" look (fill `--chip-2`/ink on, outlined `--line` off): either a small `tab` extra in `parts.js` (`tabChip`) + ~10 lines in chip.css, or reuse `.lbtn.on` (accent tint, a label toggle already in chip.css l.246: `class="tag lbtn on"`). The latter needs no new CSS. |
| `css/tokens.css` | 251 | `--paper #fffefb`, `--paper-line #efefe9`, `--paper-ink #2a2c31`, `--paper-grain`, `--shadow-ticket`, `--mono`, `--bad-ink #c03552`, `--edge-line`, `--edge-arrow`, `--queued-bar #c9cdd6`, `--state-*` (blocked, working, ready, draft, local, waits, queued, merged; no cancelled, no `--state-<x>` for `ready`...only those 8). `DESIGN.md`'s token table must list every new token with the exact value (`test_token_table`), kind one of colour/space/radius/type/shadow/font/size/other. |
| `DESIGN.md` | 283 | token rows format: `| \`--x\` | \`value\` | kind | use |` (padded; test collapses spaces); component table row `| card | \`css/components/card.css\` | \`js/ui/card.js\` | \`card\`, \`card-*\` |`; "Protected features" list at the end gets the time card. Rules: tokens only for margin/padding/gap (`space`/`size`), radius (`radius`), font-size (`type`); `check_raw` refuses literals (`10px`, `1.5em`, `99%`) in those properties. `LITERAL` only inspects margin, padding, gap, radius, font-size, font. `width`, `height`, `stroke-width`, `top` etc. are not checked. |

**Size / values to watch when moving things** (rule "search the old value"): `legend()` moves out
of `graphBlock`; nothing else measures from it, but `.batch .gcol` / `.lgrow` selectors in
`batch.css` stay valid. `data-key="graph"` and `.graph`/`.edges` are used by `drawEdges`/`light`;
the `.node` class is the hook of `light`, `bindLight`, `drawEdges`'s `found()`: when `light()` is
generalised to `[data-id]`, `drawEdges` stays on `.node[data-id]` (graph only). Card width: graph
`.lvl` is `300px` (250 on phones, `batch-graph.css`). The two `rowsNow()` closures are the only
data readers: pass the tab's rows the same way.

## 2. The smallest change that meets the spec

Backend (about 110 lines of Python + one test file):
1. `board/times.py`: `cr_times(events, c)`: one pass over `[e for e in events if e.cr == c.id]`
   producing started_at, segments, rounds, verifier_at, verdict(+_at), ended_at, state_at; helpers
   `_segments(own, ended)`, `_rounds(own)`, `_ended(own, c)`. `priority_of(events, c)`: take the
   first `add` event of the CR, split `origin` on `/`, find `1-inbox`, `3-ready`, or `2-backlog`
   followed by `P[1-4]`. Note an `add` may repeat after a `reopen`... only the first is used.
2. `crs._row`: two keys. `state.py` untouched. JSON size: per CR the rounds list is small; fine.

Frontend, in dependency order:
1. `core/format.js` `shortDate`; `model/semantics.js` `edges(rows)` and the `drawEdges` rewrite to use it.
2. `core/router.js` + `store.js` (`t=`), `batch.js` (tabs, lazy import, tab cleanup), `legend()` move.
3. `batch-graph.js`: `priority: c.priority` on `node`, `spark` icon and `.spark` css, `light()` on `[data-id]`.
4. `batch-gantt.js` + css, `batch-timecards.js` + css, `card.js` `stamps` part, `card.css` `paper`.
5. i18n files, `index.html` links, `DESIGN.md`, tokens, `docs/web-board.md`, demo events, screenshots.

**Lazy modules and the host contract.** `ui/host.js` mounts a view once and calls `view.after` on
every repaint; so tab-specific `mount` work (listeners, resize) must be set up and torn down by
`batch.js` itself on each tab change (keep a `tabCleanup`; compare a `shownTab` module variable in
`after`). A first-open `import()` repaint must go through `paint` again: trigger it with
`update({})` from the store (listeners repaint; markup differs from the loading line so it draws),
no new API.

**Gantt rows vs measured height.** Rows follow the label cards (variable height: 2-line title,
priority chip). Smallest robust layout: a CSS grid, one row per CR (label card | time cell) so the
row heights come from the browser; each time cell holds its bar. Vertical arrows span rows, so they
need an overlay SVG measured after paint (`after`), exactly like `drawEdges` (read each row's
`offsetTop/offsetHeight`, redraw on resize and `document.fonts.ready`). Bars could then be drawn in
the overlay too (one SVG, spec section 3) with y from the measured row boxes: that keeps the spec's
"one SVG" and `<pattern>` per state; only the percentages (x, width) come from data, y/height from
measurement (`setAttribute` values in markup are fine, `style=` is not). Per-state hatch classes
(`.hatch-working` etc.) in `batch-gantt.css` with `stroke: var(--state-<s>)`; 8 states x 2 rules
is about 20 lines. Segment fill classes the same (`fill: var(--state-<s>)`); `cancelled` maps to
`--state-queued`.

**Burst.** `times.state_at` vs `state.now` in `node()`: `Date.parse(state.now) - Date.parse(state_at) < 600000`.
`node(c, batch, now)` already receives `now`. Icon placement is in `top:`; `.card-compact .card-top`
is nowrap with `.tag, .sb {flex:none}` and `.lbl` shrinkable: the extra icon needs `flex: none`.
Animation: `@keyframes` once + `@media (prefers-reduced-motion: reduce)` none, in `batch-graph.css`
(no literal lengths in margin/padding/gap; `transform: scale()` is not checked). Note: because the
markup is compared as text, the burst plays once on first paint, then not again at a repaint
(correct), but replays after a tab change back to Graph (the DOM is rebuilt): spec (tabs-Q2 B: a
tab change must neither restart nor clear it) -> to stop a replay, add the icon's animation only
when the node first appears is not possible without state; the clean answer is a replay on remount
is acceptable animation-wise (the burst is NOT cleared) but contradicts "neither restarts": see Q3.

## 3. Risks

- **Design test** (`test_board_design.py`) on every new sheet: no `border-left/right`, no side
  separators on an element with a radius, no literal in margin/padding/gap/radius/font-size,
  `components` rule: a page sheet may only lay out (`grid*`, `flex*`, `order`, `*-self`, `width`,
  `min/max-width/height`, `overflow*`, `margin*`, `--*`) elements of `tag`, `lbl`, `lab`, `si`,
  `sb`, `card`, `card-*`, `column*`: `.batch .tabs .tag { color: ... }` would fail. So tab styling
  must live in `chip.css` (or reuse `.lbtn.on`), and the Gantt/time-card sheets may not colour
  `.tag`/`.card`.
- `card.css` `.card` is `overflow:hidden`: stamps that stick out are clipped; a rotated box's
  corner needs padding room (pick the `.card-paper` bottom padding / body min-height).
- `light()` generalisation: `[data-id]` also matches nothing else today (only `node`), safe. The
  Gantt label and the graph node share `data-id`; only one tab is in the DOM at a time.
- `paint` focus restore keys by `data-key`: tabs need `data-key="tab-<id>"`; rows `data-key` via
  `opener(..., 'gantt-')`.
- Closed records: `recordRows` has no `times`/`priority`; the Gantt/time-card branches must
  early-return `batch.times_none` before touching `c.times`; also a live batch row from an older
  server (no `times`) should not throw: guard `c.times ?? null` is a fallback-free read of an
  optional field (the board and page ship together, so a missing `times` on a live row is a bug,
  not a state; do not add a fallback, let the test show it).
- `en.js` is 260 lines: adding an import + spread is +2 lines; the new keys (about 30 per
  language) go in `en-batch.js` / `fr-batch.js` (about 40 lines each).
- A `just test` budget: `test_board_times.py` is in-process, no repo, so a few ms.
- Windows: `hhmm` and the Gantt ticks use local time: the screenshot job fixes TZ=UTC; a unit
  test can not cover the JS (no JS test runner in the project: Biome lint only, `just lint`).
- The demo surface changes shift other doc screenshots (chips on batch graph and PR cards).

## 4. Questions only the user can answer

- Q1. The prototype has no orange, only violet stamp ink `#4b3f9e` (finding 3). Which token should
  the REWORKED stamp take: `--state-waits` amber (reuse, no new token), `--autosync-approval`
  `#b86e0c`, or a new orange? Recommendation: reuse `--state-waits` through a new alias
  `--stamp-rework: var(--state-waits)` (one row in DESIGN.md), and a violet `--stamp-hand`
  for the round-line ink following the prototype.
- Q2. Time-card stamps through `card()`: new `stamps` part in `card.js`, or a plain `stamp` class
  outside the `card-*` namespace (finding 2)? Recommendation: the part in `card.js`.
- Q3. "The burst ... neither restarts" vs the DOM being rebuilt on a tab switch replays the CSS
  animation. Accept the replay on return to Graph (no clear), or keep the icon static after its
  first play (needs per-CR "already seen" memory in the store)? Recommendation: accept; the
  animation is once per mount.

## 5. Evidence plan

Kind: a web UI change (new Batch tabs, new card variant, chips), plus a data derivation
(`times.py`) and a URL parameter.

**Tests (before/after is the red-to-green of the new tests):**
- `<tests>/test_board_times.py`: one parametrized `cr_times` test and one `priority_of` test, as
  the spec lists (11 event lists, 5 origins), with in-memory `EventRecord(t=..., actor=..., kind=..., cr=..., **fields)`
  and `CrEntry(id=..., status=..., merged_at=...)`: no `repo` fixture, no CLI call.
- Run: `uv run --no-sync --project <repo> pytest skills/chantier/scripts/cli/tests/test_board_times.py test_code_targets.py test_board_design.py`,
  then `just check` and `just eval-dry-run`. `test_board_design.py`/`test_code_targets.py` are the
  structure gates for the sheets, scripts, words, dynamic imports.
- `just scenario` (ubuntu-latest, CI) and `chantier gate` locally on Windows when CR-345 is on top.
  Optional, cheap: in the scenario's surface-board unit assert one `GET /api/projects/<id>/state`
  row carries `times` and `priority` (the unit already reads that endpoint for `phase` and
  `next_to_start`, scenario README l.120).

**Screenshots (the manual check of the spec and the PR's evidence).** Technique: reuse
`just docs-screenshots` machinery (`scripts/docs_screenshots.py`: copies `docs/demo/` to a temp
git surface, runs `chantier board --host 127.0.0.1 --port 0 --clock 2026-06-18T10:30:00Z` through
`uv run --locked --project <repo>`, Playwright Chromium 1400x860 and 375x812, TZ UTC, en-US,
`animations="disabled"`; `goto(page, url, view, project)`; `shot(page, name, size)`). It needs the
CHECKOUT that holds the code (here the worktree, `.git` exists as a file: the script's check is
`(ROOT / ".git").exists()`, true for a worktree) and downloads Chromium the first time.
Add to its `views()` after the batch shot: `goto` then click or open with `&t=gantt` / `&t=cards`
(the address parameter makes it a plain URL: `?p=shop-api&v=batch&t=gantt`), shot `batch-gantt`,
`batch-cards`; and a phone one. The enriched demo events (finding 6) are part of the change.
For a free-hand check (network panel for the lazy import, back/forward, reload on `t=cards`,
FR language, closed batch `b=batch-01` on `mobile-app`), start the same board by hand on a copy
of `docs/demo` (make it a git repo, `CHANTIER_ROOT=<copy>`, `uv run --no-sync --project <worktree>
chantier board --host 127.0.0.1 --port 0 --clock 2026-06-18T10:30:00Z`, it prints `board on <url>`),
and drive it with a browser tool if the session has one; this session cannot launch a browser
from here without Playwright. Checks 7 (chips per stage) needs `origin` values in the demo
(`1-inbox/...`, `2-backlog/P2/...`, `3-ready/...`); the scenario's surface-board batch is an
alternative but has no UI run.
- Before: `docs/web-board/batch-pc.png` at the base (already in the repo) and a capture of the
  base for the Costs page (check 10, unchanged). After: the new three tabs at the head's SHA
  (seven characters) in the caption; `docs/web-board.md` "Batch" section with one picture per new
  tab (pictures live in `docs/web-board/`, named `<view>-pc.png`).
- The burst: capture is with `animations="disabled"` so it shows static; the 10-minute behaviour
  is shown by two runs with `--clock` at 10:30 and at 10:40 on the same copy (burst on CR-145 /
  CR-144 then gone), reload in between.

**What cannot be shown:** the burst animation itself (a still image), `prefers-reduced-motion`
without a browser emulation (Playwright `reduced_motion="reduce"` can show it), the live poll
(5 s) behaviour, and Windows/macOS rendering in the CI (only the local run on Windows). There is
no JS unit-test runner in the project (Biome lints JS), so `edges()`, `router` `t=` handling and
the Gantt geometry are shown by screenshots and the manual list only, not by tests, unless the PR
adds one (a Python test that reads the router file would be a structure test, not behaviour).
Nothing has to be shown for `DESIGN.md` beyond `test_token_table`, `test_components`.
