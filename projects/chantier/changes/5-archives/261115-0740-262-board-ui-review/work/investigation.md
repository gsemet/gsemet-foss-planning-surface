# CR-262 investigation: code map and the base's Home (Investigator, 2026-11-15)

Base: worktree `batch-18-CR-262` at origin/main (HEAD 9a63cf2). Paths below are under
`skills/chantier/scripts/cli/src/chantier/board/` (`web/` = `board/web/`). Line counts are the base's.
Limits (test_code_targets.py): 300 lines a file (scripts and styles), 50 a function, cognitive
complexity 10. The two word files' keys are compared on `en.js` / `fr.js` only; `en-write.js` /
`fr-write.js` are spread into them (`...write`) and are not compared.

## 1. Code map

### Part A (Kanban, header, titles)

| file | lines | what it holds | change |
| --- | --- | --- | --- |
| `web/js/views/kanban.js` | 55 | `columns(state)` (lines 22-45, 24 lines), `column()` (the `key === 'intake'` test for the + New button, line 50), `render`, `mount` | seven columns; `columns()` will pass 50 lines with the Done column and the filters, so the column rules move to the model; the file stays under 300 |
| `web/js/views/kanban-cards.js` | 43 | `itemCard(state,item,bucket)`, `crCard`, `bars` | add a Done card (`doneCard`: CR id, title, batch, merge date, opens `path`); `itemCard` moves to the shared `ui/item-card.js` (Part C) |
| `web/js/model/grill.js` | 26 | `stageOf`, `stageWord`, `isSpecified`, `tally`, `BUCKETS`, `itemsOf`, `toGrill` (every not-specified item: this is what the header counts today) | keep; the per-column rules go in a new `model/columns.js` (a function per column: inbox, backlog, grill, ready, progress, handed, done) used by `kanban.js`, `header.js`, and Home's In grill tile |
| `web/js/ui/header.js` | 51 | `of(data)` (lines 35-48): inbox = `backlog.inbox.length`, grill = `toGrill(P1..P4)`, `working` only | call the column functions; keys `stats.working` becomes `stats.progress` |
| `web/js/ui/picker.js` | 45 | line 20 uses `stats.intake` | follow the rename to `stats.inbox` (not named by the spec) |
| `web/js/labels/filter.js` | 36 | `filterRow`, `bindFilter` (filter changes also prune `selection`) | untouched; a sibling `labels/priority.js` holds the five toggles and its binding |
| `web/js/core/store.js` | 39 | the one state; `labelFilter` at line 23 | add `priorityFilter` (default Inbox,P1..P4 all on) |
| `web/js/core/router.js` | 88 | `reset` (lines 43-56) clears `labelFilter` on a project change | add `priorityFilter` to `reset` (else a filter leaks across projects) |
| `web/js/model/triage.js` | 69 | `passes(item, filter)`, `labelsOf`, `itemsIn` | the priority pass is a new function beside it (or in `model/columns.js`) |
| `web/js/i18n/en.js` / `fr.js` | 254 / 255 | `kanban.*` (lines 130-143), `stats.*`, `priority.inbox` | the new words (7 column names and subs, `stats.inbox`, `stats.progress`, `priority.title`, "{n} more", plus Part B's) exceed 300: add sibling files (`en-board.js` / `fr-board.js`, spread like `write`) |
| `backlog.py` | 100 | `backlog_items()` (lines 102-119, `"title": subject(row["title"])`), `summary_fields()` (90-99, already calls `summary_view`) | A4: title from `summary_view(folder).title` when it has one. `summary_fields` returns no title now: add one key there, `backlog_items` uses `fields["title"] or subject(...)`. 100 lines, room to 300 |

Facts that bear on the spec:

- Item grill words come from `grill_of()` (backlog.py 78-87): `specifying`/`specified` from
  `spec_state(folder)`; a `3-ready` item is `automatable`; else `grill` if `02-answers.md`, else `raw`.
  `stageOf` folds them to `raw|grill|spec|auto`. So the Grill column = `stageOf in {grill, spec}` in
  inbox and P1..P4; a 3-ready item is never in it.
- Done column: `state.data.merged` is the server's `dash["merged"]` (50 rows at the base, `merged_total`
  145). Rows carry `cr, title, batch, when` (seen) and the title still has the "Change Specification:"
  lead (seen in Home's Last merged). `path` for "opens its folder": not seen on the rows, only `cr,
  title, batch, when` were printed; the Driver checks `merged[].path` in `status/views.py` /
  `dashboard_view`; the spec says "its `path` from the record". If absent, the spec's rule "never touch
  status/views.py" stops here: the board's `state.py` would have to add it from the record.
- The old `.card.sel` (widgets.css:135) is the Kanban "open panel" mark, a different thing from `.pi.sel`.
- No test or doc names `col-intake` outside `kanban.js`; `stats.intake` is used in `header.js` and
  `picker.js` only.

### Part B (Home, Costs)

| file | lines | what | change |
| --- | --- | --- | --- |
| `web/js/views/home.js` | 69 | `TILES = [reviewTile, waitingTile, nextTile, writtenTile]`; `waitingTile` adds `asks_unread` to blocked | add `grillTile` (B3); `waitingTile` from `waitingForYou()` (B4); stays near 80 lines |
| `web/js/model/semantics.js` | 186 | `waitingForYou(batch)` (line 182: blocked + `asks_unread`); `counts()` | B4 decision (Q3 default: blocked only). Used by whom: grep before editing (home.js does not call it today, it recomputes) |
| `web/js/views/home-feed.js` | 16 | `activityBlock`: `events` empty gives `home.none` | B2: no batch, name `history[0]` (see the hazard below) |
| `web/js/views/home-backlog.js` | 40 | `LAST_MERGED = 4`; `mergedRow` shows cr, title, `when` | add `m.batch`; 40 lines, fine |
| `web/js/views/home-batch.js`, `home-prs.js` | 46, 22 | other Home blocks | untouched |
| new `web/js/views/home-history.js` | - | Earlier batches block (5 newest closed) | new; `home.js`'s `render` adds the block (check `home.css` grid: 223 lines) |
| `web/js/views/costs.js` | 42 | `render`: `if (!batch) return empty(...)` (line 37) | no batch: the line, then the history table and `lastMerged`; recompute line and figures stay for a batch |
| `web/js/views/costs-tables.js` | 43 | `perCr`, `lastMerged` | add `costs-history.js` (rows, unfold) rather than growing this one |
| `web/js/core/store.js` | 39 | | new state field for open history rows (`historyOpen: []`), also in `router.js` `reset` |
| `board/state.py` | 169 | `_history()` (line 94) sends every `5-archives/batches/batch-*.json` newest first; `project_state` sends `history` | no change needed for the fields; see hazards |
| `web/js/ui/host.js`, `web/js/core/refresh.js` | 39, 73 | first paint / reads | B5: see section 3 |

Hazards found in the live `history` (state read at 2026-11-15, board served from this repo's planning
folder; 18 records):

1. `history[0]` is `batch-18`, the RUNNING batch: `state`, `closed: ""`, `cost_usd` empty, `crs`
   length 0. "The last closed batch" (B2) and "batch-17 to batch-01" (Evidence) mean the records with
   a non-empty `closed`; the views must filter `closed` (or the server must). Without the filter
   the Costs table gets a "batch-18" row with no CRs and the Home feed names batch-18 as closed.
2. Only batch-17 has `opened`, `closed`, `mode`, `cost_usd`, `budget_usd` (229.22 / 300). batch-16 to
   batch-01 are back-filled records (`backfill` key): `opened/closed/mode/cost/budget` are empty and
   only `crs` (1 to 19 each) is filled. The Costs row, the Home line ("id, closing date, merged / total,
   cost") and the Evidence ("batch-17 to batch-01") need a rule for an empty date, mode and cost
   (a dash). The spec does not say; a Driver's call, to be put in the PR. Note the keys of a record:
   `schema, batch, number, state, opened, closed, mode, steering, host, budget_usd, cost_usd,
   cost_unpriced, crs, report, backfill`; of a record's CR: `cr, title, result, archive, pr, rounds,
   cost_usd, cost_unpriced`.
3. A record's CR titles carry "Change Specification:" ("CR-221 | merged | Change Specification: the
   CLI takes ..."): strip once, as the spec says (`subject()` exists server-side in `backlog.py`; a
   JS `model/` function is the lighter option, `merged[].title` needs the same strip for Home and
   Done).
4. `merged / total CRs` for a record: `result === 'merged'` over `crs.length`.

### Part C (Triage cards)

| file | lines | what | change |
| --- | --- | --- | --- |
| `web/js/triage/postit.js` | 33 | `postit(item, ctx)`: `<div class="pi {stage} sel chg pend">`, `.row` (mark, `.sl`, late, origin), `.pt`, labels, `.pm` (stage, files, open button); exports `mark` | becomes the shared card plus extras. `mark` is still imported by `triage/bar.js` (legend) and `triage/columns.js` (`.sc` counts): keep the `gs` mark for the legend, or the legend/counters change too |
| `web/js/views/kanban-cards.js` | 43 | `itemCard` | moves to new `web/js/ui/item-card.js`, with a way to add the extras and the attributes (draggable, tabindex, role, aria, data-slug, data-key) |
| `web/css/views/postit.css` | 202 | `.pi` (3-16), `.pi:hover` (18-21: tilt and lift), per-stage fills 23-34 (`.pi.specified`, `.pi.automatable` dead), `.pi.sel` outline (36-39), `.pi.drag` (41), `.pi.pend`, `.pi.chg::after`, `.pi .row/.sl/.late/.pt/.pm/.open` | keep `.pi` shell, hover, drag, pend, chg, open; drop the fills, `.sl/.pt/.pm` (the card's own `.ttl/.meta/.row-tags` apply); replace `.sel` by the Q4 mark |
| `web/css/widgets.css` | 177 | `.card` family (131-185: `.card[data-open]:hover`, `.card.sel`, `.row-tags`, `.ttl`, `.desc`, `.meta`) and the `.tag.pri-*` | the shared card styles; room for 120 lines |
| `web/css/views/triage.css` | 196 | `.gs`, `.gs.specified` (dead), `.gs.automatable` (dead) | the `.gs` marks stay only if the legend keeps them |
| `web/js/triage/selection.js` | 86 | click/keydown delegates on `.pi` | the selector stays; the click on a card must not swallow the open button or the labels |
| `web/js/triage/drag.js` | 75 | `closest('.pi')`, `classList.contains('pi')`, `dragstart` on `.pi` | needs the shared card to keep `class="pi"`, `data-slug` |
| `web/css/base.css` | 52 | `:focus-visible` ring | stays (C3) |

Dead selectors confirmed: `.pi.specified`, `.pi.automatable`, `.gs.specified`, `.gs.automatable` never
match since `stageOf` returns `spec`/`auto` (and `.pi.specifying` never, folded to `grill`).

Where the files could pass 300: only `en.js` / `fr.js` (254/255 now, the added words are about 40) must
split. No other file is near 300; functions at risk of the 50-line limit: `columns()` in `kanban.js`,
the `postit()` template (a single return, long line, short function), `of()` in `header.js`.

## 2. What the live board showed at the base (point by point)

Method. I started the CR's code on this repository's planning folder: `uv run --locked --project
<worktree> chantier board --host 127.0.0.1 --port 0` (a board of the main checkout, process 1276,
already held port 8765 and the same key, so `--port 0` was needed: 127.0.0.1:60296, the same key). I
read `/api/projects/chantier/state` with curl and loaded the page in headless Google Chrome
(`--headless --dump-dom --virtual-time-budget=1500..8000`) and read the rendered text. I could
drive no clicks (dump-dom only: no hover, no drag, no screenshot taken, nothing unfolded). All figures
are of the state at 2026-11-15 00:45 UTC, not of 2026-11-14 when the user toured: the backlog moved
(see "different state").

Running batch: `batch-18`, running, 15 CRs: 7 working, 4 queued, 3 merged (CR-256, 258, 260), 1
blocked (CR-261, blocked later during the run; at first read working=8). `asks_unread` = 0.

| Home point | What the base showed | Verdict |
| --- | --- | --- |
| In grill tile | There is NO In grill tile at the base. `TILES` = To review (0), Waiting for you (1), Next batch (0), Written by the board (5). The only "grill" figure is the header's "15 in grill" (every not-specified P1..P4 item, raw included: 2+2+10+1 = 15, minus none specified). The pipeline block shows `Inbox 0, P1 2, P2 2, P3 10, P4 1, 3-ready 0` with a legend (specified, in grill, raw, automatable). So the user's "tout est 0" is the four tiles (0, 1, 0, 5 at read time); "grill en cours" had no tile | confirms B3: the tile is new, not a bug in an existing one |
| "Waiting for you" | value 1 with sub "1 blocked, 0 questions" at 00:45 (blocked CR-261, asks 0). With `asks_unread` = 0 now, the "44 questions" the user saw cannot be reproduced (they were the Foreman's unread asks to the Chief of Staff on 2026-11-14; the batch has none now). Code confirms the sum: `waitingTile` = blocked + `batch.asks_unread` (home.js 27-38) | the mixing is real in code; the 44 not reproducible now |
| Recent-activity block | NOT empty while a batch runs: 25 rows (newest `00:45 CR-261 order rounds`) under "batch-18". It is empty only with no batch (`events` is `[]` when no batch folder: state.py `events = []`; home-feed.js then draws "none" and an empty sub). I could not run a no-batch state on this folder (batch-18 is running) | user's "recent activity vide" matches a no-batch state; not reproduced here, read from code |
| Last merged CRs | 4 rows, newest first, "145 in total": CR-256, CR-258, CR-260 (batch-18) and CR-228 (batch-17), each `id`, a title that STILL starts with "Change Specification:", and `MM-DD` (11-14). No batch id shown; the data has `batch` (CR-228 = batch-17). The earlier-batches info the user missed: no block reads `history` | confirms B2 |
| B5, the first-load "Loading..." | NOT reproduced (see section 3) | not reproduced |

Different state from the spec's: `1-inbox` is empty (0), `3-ready` is empty, and the items the spec names
as "being grilled" (fast-scenario, baseline-and-legacy, board-cr-step, worker-reply-length) have left
the backlog (they were taken into batches). At the base the 15 backlog items are: P1 board-history
[raw], surface-transition-audit [raw]; P2 docs-sphinx-rtd [grill], surface-agentless-launch [raw];
P3: landing-page [grill], planning-server [grill], eight raw; P4 tracker-import [raw]. None is at
stage `spec`. So with A1's rule the Grill column holds 3 items (docs-sphinx-rtd, landing-page,
planning-server), the Backlog column 12, the Inbox 0. The Evidence line "the Grill column holds
fast-scenario, baseline-and-legacy and the other items with `02-answers.md` or `03-change-spec.md`"
cannot be met on this folder at the PR's head; the screenshots will show the 3 above (the Driver
should say so in the PR, or use a demo planning folder / `--clock`).
`cr-folder-self-contained` is no longer in the backlog (CR-257 is in the batch), so A4's "no longer
reads Intent" is verified on another item (a backlog item with a `summary.json` title) or on
`docs/demo`.

Also seen: the sidebar shows `Triage 15` and `Kanban 27` (Kanban count = the items + CRs); the header
shows "0 intake" (inbox), "15 in grill", "7 working", "0 handed back"; no blocked in "working", as the
spec says. Language: French header at the same state reads "0 en intake, 15 au grill, 7 en cours, 0
rendus": "intake" is still English in French (the spec renames it).

## 3. B5, Home's first load: reproduced or not

Not reproduced. Steps tried, each with headless Chrome against a freshly started server of the CR's
code, page text read after the virtual-time budget:

1. Empty profile, first visit with `?k=<key>` (cookie not yet set), budget 8000 ms: Home drawn, no
   "Loading".
2. Same profile, no key (cookie set), budget 1500 ms: Home drawn.
3. Same, `?p=chantier&v=home&lang=fr`, 3000 ms: Home drawn.
4. Another empty profile, `?k=..&v=kanban`, 3000 ms: Kanban drawn.
Timing: `/api/board` 0.03 s, `/api/projects/chantier/state` 0.13 s warm.

I did not try: a tab left open across a server restart (the board I could stop is my own, but a live
user tab does not exist here), a restart while the page retries (`main.js` `boot()` retries every 5 s
on a failed first read), or a real-time (not virtual) clock. From the code, the first paint path is
sound: `boot()` reads the board, `go(..., {replace:true})`, `start()` asks at once; `show()` draws
"Loading..." only while `state.data` is null and redraws on every `update`. Reading `api.js` gives
two real candidates for a stuck state: (a) `fetch` has no timeout, so a read hung on a dead socket
(server just restarted) keeps `busy === project` in `refresh.js` for as long as the socket hangs, and
no further read starts; (b) `refresh.js` `readProject` applies a 304 (`changed: false`) as a clock-only
patch, so if an `etag` survives while `data` is null the page never fills. (b) cannot arise today
(`router.js` `reset` clears `etag` with `data`, `cache: 'no-store'` is set) but nothing enforces it.
These are hypotheses, not observed. The spec's rule: it did not reproduce, so the PR says so under
Known gaps with the steps above, unless the user can say what they did.

## 4. Evidence plan

Gate runs, in the worktree at the PR's head: `just check` (Biome on `board/web`, `test_code_targets.py`,
`test_board.py`), `just scenario` (the CLI changes; `backlog.py` is CLI code), then `just
docs-screenshots`.

Per part, what to read and capture (EN and FR, captions with the head's 7-char SHA):

- Part A: Kanban at the head: 7 columns named as A1, in French no English name (`In progress`
  becomes `En cours`). Folder at the PR's head has Inbox 0, Backlog 12, Grill 3, Ready 0: the Inbox and
  Grill shots will not match the spec's description (see section 2): either state this in the PR or
  take them on a copy of `docs/demo` (mobile-app has 3 inbox, a `02-answers.md` item, a `3-ready`
  item). P3 and P4 toggled off: P3 10 raw+grill items disappear from Backlog and Grill, `3-ready`,
  CRs, Done untouched. Header figures against the column counts, equal. A card's `summary.json`
  title (a backlog item whose title differs from its first line). Done column: 20 cards, foot "{n}
  more" with `merged_total` 145 (so "125 more" at the base's count).
- Part B: Costs with no batch running needs a no-batch project: the real folder has a running batch,
  so shoot Costs on a demo folder with the new `batch-01.json` (`mobile-app`) or on this repository
  after batch-18 closes. Home: In grill tile (3 at the base), Earlier batches block, activity block
  naming the last CLOSED batch (batch-17; `history[0]` is batch-18, filter on `closed`), last merged
  with batch, Waiting for you per Q3. Fold/unfold click on a Costs row needs a real browser session
  (the headless dump-dom cannot click).
- Part C: Triage card vs Kanban card side by side; hover tilt/lift (a GIF or a before/after pair), drag
  (the board's journal gains the line), a selected card with the Q4 mark and no blue outline;
  keyboard focus ring still shown on Tab. Dragging needs a real browser; do it on a copy of
  `docs/demo` or a throwaway planning folder, never on this repository's backlog (the move would be a
  real write to the user's planning folder; a drag writes there).
- Base record for the PR (the caveat): section 2 of this file, point by point; the B5 result, section 3.

How to drive a browser: headless Chrome exists at `C:\Program Files\Google\Chrome\Application\chrome.exe`
(`--headless --dump-dom` worked; `--screenshot` was not tried). `scripts/docs_screenshots.py` is the
repository's own retake command (it serves a fixed demo folder; not read in depth). The same board
process of the main checkout (pid 1276) still runs and is not mine.

## 5. Cleanup

The board I started (uv 9676, chantier 2076, python 2828 and 22356) is stopped by id; the worktree is
clean (`git status` empty; `uv run` created an ignored `.venv` in it). Temporary files are in the
user temp folder (`b262out*.txt`, `st262.json`, `dom262*.html`, Chrome profiles `chr262*`).
