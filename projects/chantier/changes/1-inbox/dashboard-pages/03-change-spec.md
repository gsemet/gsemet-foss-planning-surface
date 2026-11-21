# Web board Dashboard page: productivity and spending by closed batch

A read-only Dashboard view on the web board, for one project, with two tabs. Productivity: per
closed batch, the CRs held and merged, the mean rounds per merged CR, the batch's duration and the
model calls by part. Spending: the cost per merged CR, the spend per batch stacked by part or by
model, the cost outside the batches as one line, and the ten most expensive CRs. One point per
closed batch, from the closed batch records the board already sends to the Costs page: nothing new
is recorded, read or served. Charts are drawn by the web client itself (a new chart component, no
library). Joins batch-30.

All paths below are relative to `skills/chantier/scripts/cli/src/chantier/clients/web/` unless
they start with `tests/` (which is `skills/chantier/scripts/cli/tests/`), `docs/` or the
repository root. Read `DESIGN.md` there first and keep it true (AGENTS.md). Find places by their
text: line numbers move under the other batch-30 CRs.

## Goal, in the user's words

The owner (2026-11-20, `intake/request.md`, with two screenshots of another product,
`intake/dashboard-example-productivity.png` and `intake/dashboard-example-spending.png`): dashboard
pages for chantier, charts over time of what the team produced and of what it cost, in the spirit
of the examples' "Productivity" and "Spending" tabs. The user (2026-11-21, ui-night): "le but est
d'avoir une UI fonctionnelle". Each tile of the examples is replaced by the nearest figure chantier's
records already hold; what they do not hold is out of scope.

## Decisions carried from 02-answers.md

| Answer | Decision | Section |
| --- | --- | --- |
| ui-night | batch-30 (the intake's "after the studio's batch-06" is superseded by the user's ui-night destination); questions answered by a Fable advisor; the goal is a working UI | all |
| ui-night act | the board edits no batch and messages no agent; this page writes nothing | 1 |
| Q1 | a view of the web board, "Dashboard" / "Tableau de bord"; not an artifact, a status report or a TUI page | 2 |
| Q2 | in the sidebar after Costs, before Configuration, no count (open question 1 for History's place) | 2 |
| Q3 | one project at a time; on "All projects" it opens on the last real project (no `overview`); no chart across projects | 2 |
| Q4 | two tabs, Productivity (first, default) and Spending; no Scorers tab | 3 |
| Q5 | source: only the closed batch records in `state.data.history`, as Costs gets them; no archived CR folder, journal, transcript or forge; no server change, AGENTS.md unchanged | 1 |
| Q6 | one point per closed batch, oldest to newest, labelled with its number; its closing day shown with its value | 1, 4 |
| Q7 | range: last 10 closed batches (default), last 20, all; no date picker, period selector or arrows; headlines follow the range | 3 |
| Q8 | Productivity: (a) CRs held and merged, two lines, totals; (b) rounds per merged CR, mean; (c) batch duration, median; (d) model calls by part, stacked, total | 1, 3 |
| Q9 | Spending: (a) cost per merged CR with total, merged CRs, ratio; (b) spend per batch stacked by part or by model (the Costs card's switch), "not split" segment, total, outside-the-batches line not added; (c) top 10 CRs by cost, PR opened in a new tab | 1, 3 |
| Q10 | a missing figure: no point, the line cut, never a zero or a guess; "n of N batches" under each headline; back-filled batches only in CRs and rounds; unpriced marked as Costs marks it | 1, 3, 4 |
| Q11 | closed batches only; the running or paused batch has no point, one line says so and links to Costs; an abandoned record left out; a dropped CR counts as held, its cost stays, not merged | 1, 3 |
| Q12 | title, headline, legend in words; a point's value on hover, focus and tap; never colour alone; money and numbers as on Costs; no click-through, zoom, export or legend toggles | 4 |
| Q13 | the board's own look, tokens and tile frame; parts and models coloured as on Costs (open question 2 for models); a new colour would be a token listed in DESIGN.md (none is needed); a chart component with its own sheet and builder in DESIGN.md's Components table; no chart library, no build step; Costs and its protected features unchanged | 4, 5 |
| Q14 | Dashboard: charts by batch and one ranking; no list by date, no period totals; no link to or from History; no `depends.json` | 2, Overlaps |
| Q15 | tab and range in the address; redraws on state change; empty, few-points and narrow states | 2, 3 |
| Q16 | every word in English and French, through the language button; chantier's names kept as the board writes them | 3 |
| Q17 | out of scope as listed | Out of scope |
| Q18 | risks: "batch" on the axis and coverage on each tile; figures computed apart from the drawing and tested on prepared records; nothing new asked of the server; a changed record shape shows less, never a wrong number | 1, 4, Evidence |
| Q19 | proof: sidebar place, real records, controls, keyboard, narrow layout, missing figures, both languages, DESIGN.md, a screenshot of each tab in each language; `docs/web-board.md` is docs-gardening's | Evidence |

## What changes

### 1. The figures: `js/model/dashboard.js` (new, pure) (Q5, Q6, Q8 to Q11, Q18)

A pure ES module, no DOM, no words, no store: it imports only `closedBatches` and `hasUnpriced`
from `./history.js` (itself import-free), so a test can run it under Node (Evidence). It returns
numbers and keys; the views add the words. Every figure comes from `state.data.history` (the
records `board/state.py:_history` already reads for Costs); the server, the protocol and
`project.state` do not change.

**The records** (`recordsOf(data, range)`): `closedBatches(data)` (state `closed` only: the
running batch's record and an abandoned one, such as today's `batch-20.json`, are out, Q11), sorted
by `number` (else the digits of `batch`) ascending, then the last 10, the last 20, or all
(`range` is `'10'`, `'20'` or `'all'`). Each point of every chart is one of these records:
`{ batch, n, day, unpriced }`, `day` from `history.js:dayOf(closed)` (the day Costs' table shows),
`unpriced` from `hasUnpriced(record)`.

**Productivity** (`productivity(records)`), each tile `{ points, covered, total: records.length, ... }`
where `covered` counts the records that give the tile a value:

- **CRs** (Q8a): per record, `held` = `crs.length`, `merged` = the CRs with `result` `merged`
  (`history.js:mergedOf`); a `dropped` CR is held, not merged (Q11). Every closed record covers it,
  the back-filled ones (batch-01 to batch-16) included. Headline: the range's held and merged totals.
- **Rounds per merged CR** (Q8b): per record, the mean `rounds` of its merged CRs whose `rounds` is
  a number; no point for a record with none. Headline: the pooled mean over the range (the sum of
  those rounds over their count), one decimal. Back-filled records cover it when their CRs hold
  `rounds`.
- **Batch duration** (Q8c): per record, the minutes from `opened` to `closed` when both parse; no
  point otherwise (batch-01 to batch-16 today). Headline: the median of the covered records.
- **Model calls by part** (Q8d): per record, `cost_receipt.split`'s `calls` per part, only when
  every part of the split holds a number `calls` (batch-23's split has no `calls`: no point). The
  parts are `steering`, `drivers`, `workers`, or `agents` standing in place of `drivers` and
  `workers` when the split has an `agents` part: the same rule as `model/spend-by.js:parts`, copied
  in this module with a comment naming it (the Costs files do not change, and `spend-by.js` imports
  the words, so the pure module cannot import it). Headline: the total calls of the covered records.

**Spending** (`spending(records, by)`, `by` is `'model'` or `'role'`, the Costs card's two values):

- **Cost per merged CR** (Q9a): per record with a number `cost_usd` and at least one merged CR,
  `cost_usd / merged`; no point otherwise (no division by zero, no guess). Headline: the covered
  records' total cost divided by their merged CRs, with both figures (`cost`, `merged`, `ratio`).
  `unpriced` when one covered record is.
- **Spend per batch** (Q9b): per record with a number `cost_usd`, segments in a fixed order:
  - `by: 'role'`: the split's parts (`usd`, same `agents` rule), when `cost_receipt.split` exists;
  - `by: 'model'`: one segment per series key (below) from `cost_receipt.models[].usd` (a model
    whose `usd` is not a number gives no segment), when `cost_receipt.models` is a non-empty list;
  - a record without that split (batch-17 to batch-22 by part, batch-17 to batch-23 by model) is
    one segment `unsplit` of its `cost_usd`;
  - when the segments sum to less than `cost_usd` by at least half a cent, the rest is an
    `unsplit` segment; the bar's height is the larger of `cost_usd` and the segments' sum (the
    Costs card's `Math.max` rule).
  Model series: the models of the range ranked by their summed `usd` over the range; the first
  seven are their own series (`--m1` to `--m7`), any others are folded into one `other` series
  (`--m8`) (open question 2). Headline: the range's summed `cost_usd`, `unpriced` when one record is.
  The outside line: the sum of `cost_receipt.outside.grill.usd` and `.steering.usd` over the records
  where `outside` is there and every present part's `usd` is a number (as `model/receipt.js:outsideOf`
  reads it), with its own `covered` count and `unpriced`; never added to the total.
- **The most expensive CRs** (Q9c): every CR of the range's records with a number `cost_usd`,
  sorted by cost descending, then by batch number descending, then by CR; the first ten, each
  `{ cr, title, batch, rounds, cost_usd, unpriced (its cost_unpriced is non-empty), pr }`.

A record whose shape changes later (a key missing, a value of the wrong type) gives no point where
the value is needed, never a thrown error or a zero (Q18 risk 4).

### 2. The view's place and address (Q1 to Q3, Q14, Q15)

- **`js/views/registry.js`**: `import * as dashboard from './dashboard.js'` and one entry
  `{ id: 'dashboard', icon: 'dashboard', word: 'nav.dashboard', module: dashboard }`, placed right
  after the `costs` entry and right before `config`. No `count`, no `overview` (Q3: the router's
  existing rule opens it on the last real project).
- **`js/ui/icons.js`**: a `dashboard` icon in the style of the others (strokes only, for instance
  three bars on a baseline).
- **`js/i18n/en.js` / `fr.js`**: `'nav.dashboard': 'Dashboard'` / `'Tableau de bord'` beside the
  other `nav.*` words; import `./en-dashboard.js` / `./fr-dashboard.js` and spread them as the
  other parts are.
- **`js/core/router.js`** (with the store, the only writer of the URL): `DASH_TABS =
  ['productivity', 'spending']` and `DASH_RANGES = ['10', '20', 'all']`, the first of each the
  default. The address carries `dt=<tab>` and `dr=<range>` on the Dashboard view only, each only
  when not the default (`resolve` reads them only when `view === 'dashboard'`, a value not in the
  list reads as the default; `href` writes them only on that view). A `dashOf(place, now, project,
  view)` helper beside `prsOf` and `tabOf`: the place's own values, else the current ones while on
  the same project's Dashboard, else the defaults; used in `go`, `apply` (store fields `dashTab`,
  `dashRange`) and `settle`. Update the file's head comment, which lists the address's keys. A tab
  or range change is a `go(...)`, so a reload, a shared link and Back give the same view (Q15).
- **`js/core/store.js`**: `dashTab: 'productivity', // Dashboard: the open tab (the address's dt=)`
  and `dashRange: '10', // Dashboard: the range of closed batches (the address's dr=)`.
- The Spending tab's switch is the store's existing `spendBy` (`'model'` or `'role'`), the very
  switch of the Costs card: one choice for both pages (open question 3). Not in the address.
- No link to or from the History page, no shared module with it (Q14).

### 3. The page: `js/views/dashboard.js` and `js/views/dashboard-tiles.js` (new) (Q4, Q7 to Q12, Q15, Q16)

`render(state)` returns the markup from `state.data`; `mount(root)` binds the controls and the
charts (`bindCharts`, section 4) and returns the cleanup, like `costs.js`. Top to bottom:

- **The head row**: the two tabs, the existing chip in its toggle form as the Batch view draws
  its tabs (`tag tab`, `off` when not selected, `role="tablist"` / `role="tab"`,
  `aria-selected`, Left and Right arrows between them); and the range selector, the existing
  segmented control (`.seg` with `aria-pressed` buttons, as `views/costs-models.js`'s switch):
  `dashboard.range_10` "Last 10 batches", `dashboard.range_20` "Last 20 batches",
  `dashboard.range_all` "All batches".
- **The live line** (Q11), when `state.data.batch` exists (running or paused): one quiet line,
  `dashboard.live` ("{batch} is not closed: its figures so far are on the Costs page"), its link a
  button that goes to Costs (`go({ view: 'costs' })`, which opens on the live batch).
- **No closed batch** (Q15): the tabs and the range stay, and the board's empty line (`ui/parts.js:empty`)
  with `dashboard.none` ("The charts come with the first closed batch"), no tile.
- **The tiles**, each the existing figure card (`ui/parts.js:kpi`): its title as `label`, its
  headline as `value`, the chart and its legend as `extra`, and under them the coverage
  `dashboard.covers` ("{n} of {total} batches") as `sub`, plus "not all priced" (the existing
  `costs.unpriced` badge, `tag('waits', …, { badge: true })`, as the Costs table marks it) when
  `unpriced`. A tile whose covered points are fewer than two shows its headline, its coverage and
  `dashboard.few` ("The chart starts with two batches that hold this figure") in place of the
  chart; a tile with no covered point shows `—` as its headline.
  - Productivity: `dashboard.crs` (headline `dashboard.crs_value`, "{merged} merged of {held}",
    legend `dashboard.held`, `dashboard.merged`), `dashboard.rounds` (headline the mean, legend
    `dashboard.rounds_mean`), `dashboard.duration` (headline the median through
    `views/costs-receipt.js:lasted`, its sub-word `dashboard.median`), `dashboard.calls`
    (`dashboard.calls_title` "Model calls by part": the word is "model calls", never "runs", Q8d;
    headline the total; legend the parts' words, the existing `costs.receipt_part_*` keys).
  - Spending: `dashboard.per_cr` (headline the ratio through `model/receipt.js:money`, and a line
    `dashboard.per_cr_sub` "{cost} for {merged} merged CRs"), `dashboard.spend` (headline the total,
    the switch with the existing words `costs.money_by_model` / `costs.money_by_role` and
    `costs.money_switch`, legend: the parts' `costs.receipt_part_*` words, or the models through
    `model/models.js:parseModel` (name and version), `dashboard.other_models`, `dashboard.unsplit`
    "not split"; then the outside line `dashboard.outside` "Outside the batches (grill, Chief of
    Staff): {x}, not in the total" with its own coverage, or `dashboard.outside_none` when no
    record holds it), and `dashboard.top` "Most expensive CRs": a table in the board's table frame
    (`.tbl`), columns `costs.th_cr`, `costs.th_title`, `costs.th_batch`, `costs.th_rounds`,
    `costs.th_cost`, the title on one line with an ellipsis and its full text in `title` (DESIGN.md
    "One-line titles", `core/format.js:title`), the cost through `money` with the CR's
    `cost_unpriced`. A row with a PR: its CR number is an `<a target="_blank" rel="noopener">` to
    `core/format.js:safeUrl(pr)`, and a click anywhere on the row opens the same address in a new
    tab; a row with no PR is plain. With no costed CR: `dashboard.top_none`.
- Money is written by `money` / `core/format.js:usd`, counts by `toLocaleString('en-US')`, as the
  Costs page writes them (Q12); a duration by `lasted`.
- **Words**: new `js/i18n/en-dashboard.js` and `fr-dashboard.js` (head comment like
  `en-costs.js`), every `dashboard.*` key above plus `dashboard.tab_productivity`
  ("Productivity" / "Productivité"), `dashboard.tab_spending` ("Spending" / "Dépenses"),
  `dashboard.tabs`, `dashboard.range`, `dashboard.axis` ("batch"), `dashboard.read_hint` (section 4).
  French uses "tu" and writes chantier's names (batch, CR, Driver, steering, Chief of Staff) as the
  other French files do (Q16). Data (CR ids, titles, model ids) is shown as it is.
- **The sheet**: `css/views/dashboard.css`, linked in `index.html` after the Costs sheets (before
  `config.css`): layout only (the head row, a grid of tiles, two columns on a wide screen, Spending's
  stacked tile and the ranking spanning both), tokens only, never restyling a component (the
  chip, the chart, the figure card). Below the phone width (`@media (max-width: 760px)`, the value
  `css/views/costs.css` uses for `--phone-max`) the tiles stack in one column at full width (Q15),
  and the ranking hides its title column with the same `hide-phone` pattern as the Costs table.
- Split into the two files (and more if needed) to keep each script under the 300 lines of
  `tests/test_code_targets.py`.

### 4. The chart component: `js/ui/chart.js` and `css/components/chart.css` (new) (Q6, Q10, Q12, Q13)

A component in DESIGN.md's sense, built by `js/ui/chart.js` only and styled in its own sheet only,
classes `chart` and `chart-*`. Inline SVG written by the client: no chart library, no build step,
no other origin (the page's CSP stays `style-src 'self'`: no `style` attribute; colours reach the
sheet through `data-vars`, `core/dom.js:vars`, as `views/costs-models.js` and `ui/parts.js:meter` do).

- `lineChart({ label, points, series, format })` and `stackChart({ label, points, series, format })`
  return markup. `points` are section 1's (`batch`, `n`, `day`, `unpriced`, and `values` keyed by
  series, `null` where the record lacks it); `series` are `{ key, word, color, dash }` with `color`
  a token (`var(--…)`); `format(value)` writes a value.
- **Lines**: one polyline per series, cut at each `null` (a run of one point is drawn as its mark
  only); a round mark on every point; a series may be dashed (`dash: true`), so two lines are told
  apart without colour (the CRs tile: `held` dashed in `var(--accent-light)`, `merged` solid in
  `var(--state-merged)`); a one-series tile uses `var(--accent)`.
- **Stacks**: one bar per point, its segments in the series' order, bottom first; a point with no
  value has no bar, its slot left empty. Parts: `steering` `var(--accent-dark)`, `drivers`
  `var(--accent)`, `workers` and `agents` `var(--accent-light)`, the Costs card's shades
  (`model/spend-by.js`'s `SHADE`); models `var(--m1)` to `var(--m8)` (section 1); `unsplit`
  `var(--queued-bar)`, a neutral grey token that exists. No new colour token is needed.
- **Geometry**: the plot fills the tile's width at a fixed height (a new size token
  `--chart-height`, section 5); the y axis starts at zero; one hairline baseline and one top line
  in `var(--line)`. Lines and marks keep their thickness and roundness at any width (for instance
  a `viewBox` with `preserveAspectRatio="none"`, `vector-effect: non-scaling-stroke`, marks as
  zero-length round-capped strokes). The labels are HTML under and beside the SVG, in
  `var(--text-small)` and `var(--ink3)`: the axis word `dashboard.axis` ("batch"), each point's
  batch number when the range shows at most 12 points, else the first, the last and every fifth
  (Q18 risk 1); the top value and 0 on the left.
- **Reading a value** (Q12): each point has a transparent hit area over its whole column, focusable,
  with an `aria-label` that says the batch, its closing day and each series' value (`format`, and
  "not all priced" when `unpriced`). Hover, keyboard focus and a tap (a tap focuses it) light the
  column (`var(--accent-tint)`) and write the same text in the chart's readout line above the plot
  (`aria-live="polite"`); with nothing pointed, the readout shows `dashboard.read_hint` ("Point at a
  batch to read it"). One tab stop per chart: the focused column has `tabindex="0"`, the others
  `-1`; Left, Right, Home and End move between columns. `bindCharts(root)` binds this by delegation
  and writes only the readout's text (no store write, so a push repaints nothing it holds). No click
  action, zoom, export or legend toggle.
- **Legend**: under the plot, one entry per series drawn: a swatch (a short line, dashed when the
  series is, or a square for a stack) and its word. Never a series told by colour alone: word in the
  legend, dash for lines, order of the stack as in the legend, every value in the readout.
- `css/components/chart.css`: tokens only, no literal length, no side border (DESIGN.md "Tokens",
  "No side accent border"; `tests/test_board_design.py`).

### 5. DESIGN.md (Q13)

- **Components table**: one row, `chart | css/components/chart.css | js/ui/chart.js | chart, chart-*`
  (the format `tests/test_board_design.py:components` reads; its `test_components` then checks no
  other sheet styles `chart*`).
- **Tokens**: `css/tokens.css` gains `--chart-height: 160px` (kind `size`, use "a chart's plot
  height"), placed after `--phone-max`, and the table its row in the same place
  (`test_token_table`). No colour token is added.
- **A section after "Waits on a card"** (or after the batch-30 sections already there, at the end),
  **"Dashboard"**: a read-only view fed only by the project state's closed records (no op, no topic
  of its own); its figures computed by the pure `js/model/dashboard.js`, apart from the drawing;
  one point per closed batch, never per day; a figure a record lacks is no point, never a zero, and
  each tile says how many batches it covers; charts drawn by the `chart` component as inline SVG,
  no chart library; colours from existing tokens (the Costs card's part shades, `--m1`…`--m8` by the
  range's cost order with `--m8` the "other models" when there are more than eight,
  `--queued-bar` for "not split", `--accent-light` dashed and `--state-merged` for held and merged);
  never a series by colour alone (words, dash, readout); a value on hover, focus and tap; the tile
  is the figure card; every word an i18n key of `en-dashboard.js` / `fr-dashboard.js`. No protected
  feature is added; the Costs page and its protected features are untouched.

### 6. What does not change

The Costs page and its files (`views/costs*.js`, `css/views/costs*.css`, `model/receipt.js`,
`model/spend-by.js`, `model/history.js`, `model/models.js`: read or imported, never edited); the
server (`board/`), `board/api/protocol.py` and `protocol.json`, `docs/server-api.md`; the batch
record, `cost`, `close`; AGENTS.md; the CR board pane (`hooks/`, `STATUS.json`), the cards, the
agents. `docs/web-board.md` is left to docs-gardening (Q19).

## Out of scope

Per-day, per-week or per-month charts; human interactions per PR; cycle times (kickoff to PR, to
first review, to merge); PRs opened per day; runs by agent type; cost split into compute, platform
and inference; a Scorers tab; charts across projects ("All projects"); the running batch's live
point; budgets against costs; any change to the batch record, to `cost` or to what `close` writes
(Q17). A list of CRs or PRs by date and period totals (the History page's, Q14); a link to or from
History; a click-through from a point, zoom, export, legend toggles (Q12); the user docs
(docs-gardening, Q19).

## Known gaps

- Batch-01 to batch-16 hold no dates and no cost: they show in the CRs and rounds tiles only (Q10).
- Batch-17 to batch-22 hold no split: one "not split" bar by part and by model; batch-23 holds a
  split without calls and no models: no point in the calls tile, "not split" by model.
- A model's colour on the Dashboard follows the range's cost order, the Costs card's follows the one
  batch's; they agree while one model leads every batch (today, Sonnet then Opus) (open question 2).

## Overlaps in batch-30 and the UI night

No `depends.json` (Q14); the stack settles each shared edit, whichever lands second rebases.

- **`js/views/registry.js`, `js/i18n/en.js` / `fr.js` (`nav.*`, one import and spread),
  `js/ui/icons.js`, `index.html` (one sheet)**: also edited by CR-439 (Help, after Home and the
  Inbox), `board-user-inbox` (Inbox, right after Home) and `board-history` (History, after PRs,
  before Costs). Each adds its own line. The order once all have landed: Home, Inbox, Help, Triage,
  Kanban, Batch, PRs, History, Costs, Dashboard, Configuration.
- **`js/core/router.js`, `js/core/store.js`**: CR-434 (`TABS`, `tabOf`, `settle`, the store's
  `batchTab`), CR-439 (`topicOf`, `helpTopic`), CR-440 (`triageFolded`), `board-user-inbox`
  (`inboxMarks`), `board-history` (`historyOf`, `hp=` / `hd=`, `historyPeriod` / `historyDate`).
  This CR adds `dashOf`, `dt=` / `dr=` and two store fields; the address keys do not clash (`t` is
  the Batch view's, `h` Help's, `hp` / `hd` History's).
- **`DESIGN.md`**: CR-427, CR-433, CR-434, CR-440 edit the "One card, one column, one chip" rule;
  CR-435 and CR-441 the Batch title row; CR-439, CR-440, `board-user-inbox` and `board-history` add
  sections. This CR adds one Components row, one token row and its own section; it touches no rule
  another CR edits. **`css/tokens.css`**: no other batch-30 spec adds a token, as their specs stand.
- **The Node test helper**: `board-user-inbox` also runs a shipped pure module under the lint's
  pinned Node (`tests/test_board_inbox_marks.py`). Whichever lands second moves the shared part (the
  pin read from the `justfile`'s `node :=` line, the `uvx` call, the `.mjs` written to `tmp_path`)
  into one helper module under `tests/`, used by both.
- **`tests/test_board_design.py`**: CR-439, `board-user-inbox` and `board-history` add tests there
  that assert their own entries' places; this CR's (Evidence 2) asserts only Dashboard's neighbours.
- **CR-429** (the server's watch and cache): changes how the project state is pushed, not what it
  holds; `history` stays in it, so this page works on either side.
- **CR-441, CR-433, CR-435, CR-427, board-griller**: no shared file expected.
- **docs-gardening** (`2-backlog/P1`, last in batch-30): adds the page to `docs/web-board.md` with
  its picture (Q19); this PR's screenshots are its input.

## Evidence

**Checks in `just check`**, each reading the shipped files at the head under test, never a copy:

1. **The figures** (Q18 risk 2), new `tests/test_board_dashboard.py`: the shipped
   `js/model/dashboard.js` run under the lint's pinned Node (`uvx --from nodejs-wheel==<pin> node`,
   the pin read from the `justfile`'s `node :=` line), by one short `.mjs` written to `tmp_path`
   that imports the shipped file by its `file://` URL, runs every case and prints JSON (one Node run
   for the file, to stay fast). The prepared records (a prepared input: the real ones change; they
   are the case the shipped files cannot hold) cover:
   - a back-filled record (CRs with `rounds`, no `opened`, `closed`, `cost_usd`, `cost_receipt`): a
     point in CRs and rounds, none in duration, calls, cost per merged CR or spend; the coverage
     counts say so;
   - a record with `cost_usd` and no `cost_receipt` (batch-17-like): one `unsplit` segment equal to
     its cost, by part and by model;
   - a split without `calls` and no `models` (batch-23-like): no calls point; split by part,
     `unsplit` by model;
   - two records with split, calls and models (one with an `agents` part: `drivers` and `workers`
     not drawn), segments summing below `cost_usd` (an `unsplit` rest) and one above it (the bar's
     height is the sum);
   - a dropped CR (held, not merged; its cost in its batch's cost and in the ranking);
   - a record with `cost_unpriced` non-empty (`unpriced` on its point and on the headline);
   - a record with no merged CR (no cost-per-merged-CR point, no rounds point);
   - nine models over the range (seven series and `other`, ranked by the range's cost);
   - a `running` record and an abandoned one (out of every figure), and 25 closed records for the
     range: `'10'` and `'20'` keep the newest by number, `'all'` keeps all, oldest first;
   - expected numbers: held and merged totals, the pooled rounds mean, the duration median (odd and
     even counts), the call total, the cost-per-merged-CR ratio, the spend total, the outside sum
     and its coverage, the top ten's order (ties by batch then CR) and the CRs with no cost left out.
2. **The shipped client files**, new test in `tests/test_board_design.py`: `js/views/registry.js`
   has an entry `id: 'dashboard'` with no `overview` and no `count`, the entry before it is `costs`
   and the one after it `config`; `js/model/dashboard.js` imports nothing but `./history.js`; no
   file under `clients/web/` loads a script from another origin (the existing self-contained test,
   `test_the_web_frame_is_self_contained_and_follows_the_style_rules`, keeps covering it).
3. Existing checks that now cover the new files: `test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys`
   (`en-dashboard.js` / `fr-dashboard.js`, the 300-line limit), `test_board_design.py`'s
   `test_token_table` (`--chart-height`), `test_sheets` and `test_components` (`chart.css`,
   `dashboard.css`, the new Components row), `test_one_card`,
   `test_a_card_title_is_one_line_with_its_full_text_on_hover`; Biome (`just lint`).

**Before the push** (AGENTS.md: a change under the CLI's `src/`): `just check` and
`just eval-dry-run` in the worktree at the rebased head; the pipeline's `just scenario
(ubuntu-latest)` green at the PR's head before the PR. The pane screenshot rule does not apply
(neither `hooks/register.tsx` nor `STATUS.json` changes).

**By hand, in the PR's Deliverables** (DESIGN.md: screenshots are the visual record), `chantier
board` served from the PR's head on the real planning surface (`gsemet-foss-planning-surface`,
project `chantier`), captioned with the head's seven-character SHA:

1. Productivity, English, last 20 batches (back-filled batches in the CRs and rounds tiles only, the
   coverage lines, the live line for batch-30).
2. Spending, English, by role, with a value read on hover.
3. Productivity, French.
4. Spending, French, by model.
5. The narrow layout (375 px), one tab.

And a short written check: Dashboard sits between Costs and Configuration; a tab and a range survive
a reload and a copied address, and Back returns to the previous one; Tab reaches a chart and the
arrows walk its batches with the readout following; a tap reads a point on the phone; the switch is
the same choice on Costs; a CR row opens its PR in a new tab; on "All projects" the view opens on
the last real project; the figures of one batch (for instance batch-29: 36 CRs, $243.54, its split
and models) match its Costs receipt.

Host and default matrix: none (the page depends on neither the host nor a configured value).

## Open questions (built as A; the user asks none tonight)

1. **History's place in the sidebar.** dashboard-Q2 reads "Costs, History, Dashboard,
   Configuration"; board-history's spec v1 (its Q21) puts History after PRs, before Costs. Both keep
   Dashboard right after Costs and right before Configuration, which is all this CR places.
   A (recommended, built): PRs, History, Costs, Dashboard, Configuration, as board-history builds
   it. B: Costs, History, Dashboard (board-history would move its entry).
2. **A model's colour across batches.** The Costs card colours a batch's models by their cost order
   in that batch (`--m1`…`--m8`, wrapping); a chart over many batches needs one colour per model.
   A (recommended, built): rank the range's models by summed cost, the first seven `--m1`…`--m7`,
   the rest one "other models" series in `--m8`; it matches Costs while one model leads every batch.
   B: Costs' wrapping rule over the range's order (two models may share a colour past eight).
3. **The by part / by model switch.** A (recommended, built): the store's existing `spendBy`, the
   Costs card's switch, one choice for both pages (default by model, as Costs). B: a Dashboard field
   of its own, in the address.
4. **How the figures are tested.** A (recommended, built): a pytest that runs the shipped pure
   module under the lint's pinned Node through `uvx`, the way board-user-inbox's spec tests its
   hides. B: compute the figures in Python on the server: a new read and a protocol addition,
   against Q5 and Q18 risk 3. C: no test of the figures, only the PR's written check, against Q18.
5. **Stacked bars, not stacked areas.** The examples draw stacked areas; with one point per closed
   batch and gaps where a record lacks the split, a bar per batch reads each batch apart and shows a
   gap as an empty slot. A (recommended, built): bars. B: stacked areas cut at a gap.
