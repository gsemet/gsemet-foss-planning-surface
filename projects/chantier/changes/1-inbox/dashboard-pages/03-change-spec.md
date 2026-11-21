# Web board Dashboard page: productivity and spending by closed batch

A read-only Dashboard view on the web board, for one project, with two tabs. Productivity: per
closed batch, the CRs held and merged, the mean rounds per merged CR, the batch's duration and the
model calls by part. Spending: the cost per merged CR, the spend per batch stacked by part or by
model, the cost outside the batches as one line, and the ten most expensive CRs. One point per
closed batch. The figures are computed on the server by a new `board/dashboard_page.py` from the closed
batch records the server already reads, and served by one read-only op, `dashboard.get` (an
addition to protocol 1): nothing new is recorded, no new file is read. Charts are drawn by the web
client itself (a new chart component: lines, and stacked bars for the stacked tiles; no library). One CR, both tabs. Joins batch-30.

Spec v2 (2026-11-21): carries dashboard-Q20 to Q27 (v1's five open questions, all decided; Q23
moves the figures to the server, tested in pytest) and the spec critic's fixes 5 to 8 on v1.

All paths below are relative to `skills/chantier/scripts/cli/src/chantier/` unless they start with
`clients/web/` (written out in full where it matters, shortened to `js/` and `css/` in the client's
sections, which are relative to `clients/web/`), `tests/` (which is
`skills/chantier/scripts/cli/tests/`), `docs/` or the repository root. Read
`clients/web/DESIGN.md` first and keep it true (AGENTS.md). Find places by their text: line numbers
move under the other batch-30 CRs.

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
| ui-night act | the board edits no batch and messages no agent; this page and its op write nothing | 1, 2 |
| Q1 | a view of the web board, "Dashboard" / "Tableau de bord"; not an artifact, a status report or a TUI page | 3 |
| Q2, Q20 | in the sidebar after Costs, before Configuration, no count; History's place is board-history's (PRs, History, Costs, Dashboard, Configuration), Q2's "Costs, History, Dashboard" superseded on that point only | 3 |
| Q3 | one project at a time; on "All projects" it opens on the last real project (no `overview`); no chart across projects | 3 |
| Q4 | two tabs, Productivity (first, default) and Spending; no Scorers tab | 4 |
| Q5, Q23 | source: only the closed batch records, the ones `board/state.py:_history` already reads; no archived CR folder, journal, transcript or forge; one read-only op computed from the records the server already reads; no new file read, nothing recorded, nothing added to the project state; AGENTS.md unchanged | 1, 2 |
| Q6 | one point per closed batch, oldest to newest, labelled with its number; its closing day shown with its value | 1, 5 |
| Q7 | range: last 10 closed batches (default), last 20, all; no date picker, period selector or arrows; headlines follow the range | 1, 4 |
| Q8 | Productivity: (a) CRs held and merged, totals; (b) rounds per merged CR, mean; (c) batch duration, median; (d) model calls by part, stacked, total | 1, 4 |
| Q9 | Spending: (a) cost per merged CR with total, merged CRs, ratio; (b) spend per batch stacked by part or by model (the Costs card's switch), "not split" segment, total, outside-the-batches line not added; (c) top 10 CRs by cost, PR opened in a new tab | 1, 4 |
| Q10, Q25 | a missing figure: no point, never a zero or a guess; "n of N batches" under each headline; back-filled batches in the CRs and rounds tiles and in the ranking of CRs, in no tile that needs a batch cost, a date or a split; unpriced marked as Costs marks it | 1, 4, 5 |
| Q11 | closed batches only; the running or paused batch has no point, one line says so and links to Costs; a record that is not closed is left out; a dropped CR counts as held, its cost stays, not merged | 1, 4 |
| Q12 | title, headline, legend in words; a point's value on hover, focus and tap; never colour alone; money and numbers as on Costs; no click-through, zoom, export or legend toggles | 5 |
| Q13 | the board's own look, tokens and tile frame; parts coloured as on Costs, models by Q21; a new colour would be a token listed in DESIGN.md (none is needed); a chart component with its own sheet and builder in DESIGN.md's Components table; no chart library, no build step; Costs and its protected features unchanged | 5, 6 |
| Q14 | Dashboard: charts by batch and one ranking; no list by date, no period totals; no link to or from History; no `depends.json` | 3, Overlaps |
| Q15 | tab and range in the address; redraws on state change; empty, few-points and narrow states | 3, 4 |
| Q16 | every word in English and French, through the language button; chantier's names kept as the board writes them | 4 |
| Q17 | out of scope as listed | Out of scope |
| Q18 | risks: "batch" on the axis and coverage on each tile; figures computed apart from the drawing and tested on prepared records (now on the server, in pytest, Q23); risk 3 reads "one read-only op computed from the records the server already reads; no new file read, nothing recorded, nothing added to the project state"; a changed record shape shows less, never a wrong number | 1, 2, 5, Evidence |
| Q19 | proof: sidebar place, real records, controls, keyboard, narrow layout, missing figures, both languages, DESIGN.md, a screenshot of each tab in each language; `docs/web-board.md` is docs-gardening's | Evidence |
| Q21 | models ranked by their summed cost over all the closed records of the project, not the range: up to eight models get `--m1` to `--m8`; with more than eight, the first seven keep theirs and the rest fold into "other models" in `--m8`; Known gap: may differ from one batch's Costs card | 1, 5, Known gaps |
| Q22 | the switch is the store's existing `spendBy`, one choice for Costs and Dashboard, default by model, not in the address | 3, 4 |
| Q23 | figures on the server: `board/dashboard_page.py`, op `dashboard.get {project, range}`, both splits in the answer, points carry `closed`, the client writes the day with `history.js:dayOf`; no `js/model/dashboard.js`; a `js/views/dashboard-feed.js`; views compute no figure; `tests/test_board_dashboard.py` in-process, plus a bad `range` refused; no Node-run test | 1, 2, 4, Evidence |
| Q24 | the stacked tiles (model calls by part, spend per batch) are stacked bars, one per closed batch, an empty slot where a record lacks the figure; no stacked area; the line tiles of Q8 and Q9 stay lines | 5 |
| Q25 | the ranking takes every CR of the range's closed records whose own `cost_usd` is a number, back-filled included; its coverage counts the records with at least one costed CR | 1 |
| Q26 | a numeric `rounds`, 0 included, counts in the batch's mean and the pooled mean; only a non-number is missing; Known gap named | 1, Known gaps |
| Q27 | one CR, both tabs; rounds ordered: op and test, then page, address, chart and Productivity, then Spending; screenshots of both tabs | Rounds |

## What changes

### 1. The figures: `board/dashboard_page.py` (new, pure) (Q5, Q6, Q8 to Q11, Q18, Q21, Q23, Q25, Q26)

A new module of pure functions over a list of batch records (the list `board/state.py:_history`
returns, newest first, as the project state's `history` holds it). It reads no file, no forge, no
journal, no transcript, and writes nothing; it imports no web client file and nothing of `board/`
but what it needs for types. It returns numbers, keys and record ids; the client adds the words.
One entry point, `answer(history: list[Any], range_: str) -> dict[str, Any]`; the helpers below are
its parts (split the module if it nears the size limit of
`tests/test_code_targets.py:test_files_and_functions_are_small_and_the_imports_have_no_cycle`).

A record whose shape changes later (a key missing, a value of the wrong type) gives no point where
the value is needed, never a raised error or a zero (Q18 risk 4): every read checks the type
(a number is an `int` or `float` and not a `bool`; a list is a list; a dict is a dict).

**The records.** `closed` = the records that are dicts with `state == "closed"` (the running or
paused batch's own record is out, and so is a stale record that never closed, such as today's
`batch-20.json`: `state: "running"`, a `number`, `closed: null`; Q11). Sorted by `number` when it
is an `int`, else the digits of `batch`, ascending. The range (`"10"`, `"20"` or `"all"`) keeps the
last 10, the last 20 or all of them: these are the range's records, and each is one point of every
chart, `{batch, n, closed, unpriced}`: `closed` the record's own `closed` string (the client writes
its day with `clients/web/js/model/history.js:dayOf`), `unpriced` true when the record's
`cost_unpriced` is a non-empty dict (the rule of `history.js:hasUnpriced`).

Every tile carries `values` aligned with `points` (`null` where the record lacks the figure),
`covered` (how many of the range's records give a value) and the tile's headline figures; `total`
is `len(points)` once, at the top.

**Productivity** (`productivity(records)`):

- **CRs** (Q8a): per record, `held` = the length of `crs`, `merged` = the CRs with `result ==
  "merged"`; a `dropped` or `cancelled` CR is held, not merged (Q11). Every closed record covers
  it, the back-filled ones (batch-01 to batch-16) included. Headline: the range's `held` and
  `merged` totals.
- **Rounds per merged CR** (Q8b, Q26): per record, the mean `rounds` of its merged CRs whose
  `rounds` is a number, 0 included; `null` for a record with none. Headline `mean`: the pooled mean
  over the range (the sum of those rounds over their count), rounded to one decimal by the client.
  A `rounds` that is not a number (missing, `null`, a string) is a missing figure, left out of both
  means. Back-filled records cover it when their CRs hold `rounds`.
- **Batch duration** (Q8c): per record, the minutes from `opened` to `closed` when both parse as
  ISO instants; `null` otherwise (batch-01 to batch-16 today). Headline `median`: the median of the
  covered values (the mean of the two middle ones for an even count).
- **Model calls by part** (Q8d): per record, `cost_receipt.split`'s `calls` per part, only when
  every part of the split holds a number `calls` (batch-23's split has none: `null`). The parts are
  `steering`, `drivers`, `workers`, or `agents` standing in place of `drivers` and `workers` when
  the split has an `agents` part: the rule of `clients/web/js/model/spend-by.js:parts`, written in
  Python with a comment naming the JS original (the Costs files do not change). Each value is a dict
  `{part: calls}`; the tile's `parts` lists the parts drawn in the range, in that fixed order.
  Headline `total`: the summed calls of the covered records.

**Spending** (`spending(records, rank)`):

- **Cost per merged CR** (Q9a): per record with a number `cost_usd` and at least one merged CR,
  `cost_usd / merged`; `null` otherwise (no division by zero, no guess). Headline: `cost` (the
  covered records' summed cost), `merged` (their merged CRs), `ratio` (`cost / merged`, `null`
  when no record covers it), and `unpriced` true when one covered record is.
- **Spend per batch** (Q9b), both splits in the answer (Q23), `spend.role` and `spend.model`, each
  `{series, values}`, plus `total` (the range's summed number `cost_usd`), `covered` (records with a
  number `cost_usd`) and `unpriced` (true when one covered record is). Per record with a number
  `cost_usd`, a dict of segments `{series_key: usd}`:
  - `role`: the split's parts' `usd` (same `agents` rule), when `cost_receipt.split` is a dict;
  - `model`: one segment per series key (below), summing `cost_receipt.models[].usd` of the models
    in that series (a model whose `usd` is not a number gives nothing), when `cost_receipt.models` is
    a non-empty list;
  - a record without that split (today batch-17 to batch-22 by part, batch-17 to batch-23 by model)
    is one segment `unsplit` of its `cost_usd`;
  - when the segments sum to less than `cost_usd` by at least half a cent, the rest is an `unsplit`
    segment; the bar's height, which the client takes as the segments' sum, is then the larger of
    `cost_usd` and the segments' sum (the Costs card's `Math.max` rule);
  - a record without a number `cost_usd` has `null` (no bar).
  `role.series` lists the part keys drawn in the range in the fixed order `steering`, `drivers`,
  `workers`, `agents`, then `unsplit` when drawn. `model.series` lists, in rank order, one entry per
  series drawn in the range, `{key, models}`: `key` is `m1` to `m8` or `other`, `models` the model
  ids it holds (one for `m1`...`m8`, the folded ones for `other`), then `{key: "unsplit", models: []}`
  when drawn.
- **The model rank** (Q21): `rank(closed)` sums each model id's `usd` over every closed record of
  the project (all of them, not the range), and sorts by that sum descending, then by id. With at
  most eight models, the i-th gets `m{i}`; with more than eight, the first seven get `m1` to `m7`
  and every other model folds into `other` (drawn in `--m8`). So a model keeps its colour when the
  range changes.
- **The outside line** (Q9b): the sum of `cost_receipt.outside.grill.usd` and
  `cost_receipt.outside.steering.usd` over the range's records where `outside` is a dict and every
  present part's `usd` is a number (as `clients/web/js/model/receipt.js:outsideOf` reads it), as
  `outside: {usd, covered, unpriced}`; `usd` is `null` when no record holds it. Never added to
  `spend.total`.
- **The most expensive CRs** (Q9c, Q25): every CR of the range's closed records whose own
  `cost_usd` is a number, back-filled records included, sorted by cost descending, then by batch
  number descending, then by CR id; the first ten, each `{cr, title, batch, rounds, cost_usd,
  unpriced, pr}` (`unpriced` true when the CR's `cost_unpriced` is non-empty, `pr` the recorded
  value or `null`). A CR with `cost_usd: null` (as CR-295 and CR-366) is left out. `top.covered`
  counts the range's records with at least one costed CR.

**The answer** (`answer(history, range_)`), the same dict the op returns (plus the op's `now`):

```
{
  "range": "10", "closed_total": <closed records of the project>, "total": <len(points)>,
  "points": [{"batch", "n", "closed", "unpriced"}, ...],          # oldest first
  "productivity": {
    "crs":      {"values": [{"held", "merged"} | null], "covered", "held", "merged"},
    "rounds":   {"values": [number | null], "covered", "mean"},
    "duration": {"values": [minutes | null], "covered", "median"},
    "calls":    {"parts": [...], "values": [{part: calls} | null], "covered", "total"}
  },
  "spending": {
    "per_cr":  {"values": [number | null], "covered", "cost", "merged", "ratio", "unpriced"},
    "spend":   {"role": {"series", "values"}, "model": {"series", "values"},
                "total", "covered", "unpriced"},
    "outside": {"usd", "covered", "unpriced"},
    "top":     {"rows": [...], "covered"}
  }
}
```

The client writes `mean` with one decimal, `median` through `views/costs-receipt.js:lasted`; a
headline with no covered record is `null`.

### 2. The op: `dashboard.get` (Q5, Q18 risk 3, Q23)

An addition to protocol 1, nothing changed (the protocol stays `1`, `board.get`'s `protocols`
stays `[1]`):

- `board/api/protocol.py`: a `DashboardArgs(_Model)` with `project: str` and
  `range: Literal["10", "20", "all"] = "10"` beside `PrsArgs`, and `"dashboard.get": DashboardArgs`
  in `OP_ARGS` (sorted into `OPS` as the others). No topic: the client asks again when the state it
  already receives changes (section 4).
- `board/api/protocol.json`: regenerated with `just protocol-schema` and committed (the existing
  test in `tests/test_server_protocol.py` that compares it with the models then passes).
- `board/api/ops.py`: `def _dashboard(ctx, project, a)`, which takes the project state the server
  already holds, `reads.state_of(ctx, project, ask=False)` (as `_prs` does: the cached state,
  rebuilt only when its fingerprint changed, so no new file read), and returns
  `Result(200, {**dashboard.answer(data["history"], a.range), "now": clock.now()})`;
  `"dashboard.get": _on_project(_dashboard)` in `HANDLERS`. An unknown project is 404 and a `range`
  not in the list 400, by the existing `_on_project` and `checked`.
- `docs/server-api.md`, the ops table, one row after `prs.get`:
  `| dashboard.get | project, range? | the Dashboard's figures over the project's closed batch records (range "10", "20" or "all", default "10"): points, productivity, spending, closed_total, now; read-only, computed from the records the server already reads |`.
- `project.state` gains nothing; `board/state.py` does not change.

### 3. The view's place and address (Q1 to Q3, Q14, Q15, Q20, Q22)

- **`js/views/registry.js`**: `import * as dashboard from './dashboard.js'` and one entry
  `{ id: 'dashboard', icon: 'dashboard', word: 'nav.dashboard', module: dashboard }`, placed right
  after the `costs` entry and right before `config`. No `count`, no `overview` (Q3: the router's
  existing rule opens it on the last real project). History's own place (after PRs, before Costs)
  is board-history's (Q20).
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
- **`js/core/store.js`**: `dashTab: 'productivity', // Dashboard: the open tab (the address's dt=)`,
  `dashRange: '10', // Dashboard: the range of closed batches (the address's dr=)` and
  `dashboard: null, // Dashboard: the last dashboard.get answer, kept across a failed read`.
- The Spending tab's switch is the store's existing `spendBy` (`'model'` or `'role'`, default
  `'model'`), the very switch of the Costs card: one choice for both pages, not in the address
  (Q22). No new store field for it.
- **`js/core/api.js`**: `export const dashboard = (project, range) => read('dashboard.get', {
  project, range });`, beside `prs`.
- No link to or from the History page, no shared module with it (Q14).

### 4. The page: `js/views/dashboard.js`, `dashboard-tiles.js`, `dashboard-feed.js` (new) (Q4, Q7 to Q12, Q15, Q16, Q23)

**The feed**, `js/views/dashboard-feed.js` (like `prs-feed.js`): `startFeed()` calls
`api.dashboard(project, state.dashRange)` and writes the answer to the store's `dashboard` with the
project it was asked for; it calls again when the project, `dashRange`, or the closed batches change
(a key of `history.js:closedBatches(state.data)`'s `batch` and `closed` values, so a batch closing
asks again and an unrelated push does not), through the store's `subscribe`, as `prs.js`'s `mount`
watches its batch. A failed read keeps the last answer on screen with the error beside it (as
`prs-feed.js:failed`); an answer for another project or range than the current ones is not drawn (the
view shows the board's loading line, `stats.loading`, as `prs.js` does). It returns the function that
stops it; `dashboard.js:mount` starts it and stops it in its cleanup. The views compute no figure:
they draw the answer (Q23).

`render(state)` returns the markup from `state.dashboard` and `state.data`; `mount(root)` starts the
feed, binds the controls and the charts (`bindCharts`, section 5) and returns the cleanup, like
`costs.js`. Top to bottom:

- **The head row**: the two tabs, the existing chip in its toggle form as the Batch view draws
  its tabs (`tag tab`, `off` when not selected, `role="tablist"` / `role="tab"`,
  `aria-selected`, Left and Right arrows between them); and the range selector, drawn with the
  segmented control `.seg` of `css/views/costs-models.css`, reused unchanged (`aria-pressed`
  buttons, as `views/costs-models.js`'s switch draws it): `.seg` is not a component in DESIGN.md's
  sense, and moving it to a component sheet is a separate CR. Words: `dashboard.range_10` "Last 10
  batches", `dashboard.range_20` "Last 20 batches", `dashboard.range_all` "All batches".
- **The live line** (Q11), when `state.data.batch` exists (running or paused): one quiet line,
  `dashboard.live` ("{batch} is not closed: its figures so far are on the Costs page"), its link a
  button that goes to Costs (`go({ view: 'costs' })`, which opens on the live batch).
- **No closed batch** (Q15, `closed_total` is 0): the tabs and the range stay, and the board's empty
  line (`ui/parts.js:empty`) with `dashboard.none` ("The charts come with the first closed batch"),
  no tile.
- **The tiles**, each the existing figure card (`ui/parts.js:kpi`): its title as `label`, its
  headline as `value`, the chart and its legend as `extra`, and under them the coverage
  `dashboard.covers` ("{n} of {total} batches", from the tile's `covered` and the answer's `total`)
  as `sub`, plus "not all priced" (the existing `costs.unpriced` badge, `tag('waits', …, { badge:
  true })`, as the Costs table marks it) when `unpriced`. A tile whose covered points are fewer than
  two shows its headline, its coverage and `dashboard.few` ("The chart starts with two batches that
  hold this figure") in place of the chart; a tile with no covered point shows `—` as its headline.
  - Productivity: `dashboard.crs` (headline `dashboard.crs_value`, "{merged} merged of {held}",
    two lines, legend `dashboard.held`, `dashboard.merged`), `dashboard.rounds` (headline the mean, one decimal, legend `dashboard.rounds_mean`),
    `dashboard.duration` (headline the median through `views/costs-receipt.js:lasted`, its sub-word
    `dashboard.median`), `dashboard.calls` (`dashboard.calls_title` "Model calls by part": the word
    is "model calls", never "runs", Q8d; headline the total; legend the parts' words, the existing
    `costs.receipt_part_*` keys).
  - Spending: `dashboard.per_cr` (headline the ratio through `model/receipt.js:money`, and a line
    `dashboard.per_cr_sub` "{cost} for {merged} merged CRs"), `dashboard.spend` (headline the total,
    the switch with the existing words `costs.money_by_model` / `costs.money_by_role` and
    `costs.money_switch`, drawing `spend.model` or `spend.role` after `spendBy`; legend: the parts'
    `costs.receipt_part_*` words, or each model series through `model/models.js:parseModel` (name
    and version), `dashboard.other_models` "other models" for `other`, `dashboard.unsplit` "not
    split"; then the outside line `dashboard.outside` "Outside the batches (grill, Chief of Staff):
    {x}, not in the total" with its own coverage, or `dashboard.outside_none` when `outside.usd` is
    `null`), and `dashboard.top` "Most expensive CRs": a table in the board's table frame (`.tbl`),
    columns `costs.th_cr`, `costs.th_title`, `costs.th_batch`, `costs.th_rounds`, `costs.th_cost`,
    the title on one line with an ellipsis and its full text in `title` (DESIGN.md "One-line
    titles", `core/format.js:title`), the cost through `money` with the CR's `unpriced`, the
    ranking's coverage under its title. A row with a PR: its CR number is an `<a target="_blank"
    rel="noopener">` to `core/format.js:safeUrl(pr)`, and a click anywhere on the row opens the same
    address in a new tab; a row with no PR is plain. With no row: `dashboard.top_none`.
- Money is written by `money` / `core/format.js:usd`, counts by `toLocaleString('en-US')`, as the
  Costs page writes them (Q12); a duration by `lasted`; a point's day by `history.js:dayOf(closed)`.
- **Words**: new `js/i18n/en-dashboard.js` and `fr-dashboard.js` (head comment like
  `en-costs.js`), every `dashboard.*` key above plus `dashboard.tab_productivity`
  ("Productivity" / "Productivité"), `dashboard.tab_spending` ("Spending" / "Dépenses"),
  `dashboard.tabs`, `dashboard.range`, `dashboard.axis` ("batch"), `dashboard.read_hint` (section 5).
  French uses "tu" and writes chantier's names (batch, CR, Driver, steering, Chief of Staff) as the
  other French files do (Q16). Data (CR ids, titles, model ids) is shown as it is.
- **The sheet**: `css/views/dashboard.css`, linked in `index.html` after the Costs sheets (after
  `css/views/costs-stamp.css`, before `css/views/config.css`): layout only (the head row, a grid of
  tiles, two columns on a wide screen, Spending's stacked tile and the ranking spanning both), tokens
  only, never restyling a component (the chip, the chart, the figure card) nor `.seg`. Below the
  phone width (`@media (max-width: 760px)`, the value `css/views/costs.css` uses for `--phone-max`)
  the tiles stack in one column at full width (Q15), and the ranking hides its title column with the
  same `hide-phone` pattern as the Costs table.
- Split into the three files (and more if needed) to keep each script under the 300 lines of
  `tests/test_code_targets.py`.

### 5. The chart component: `js/ui/chart.js` and `css/components/chart.css` (new) (Q6, Q10, Q12, Q13, Q24)

A component in DESIGN.md's sense, built by `js/ui/chart.js` only and styled in its own sheet only,
classes `chart` and `chart-*`. `css/components/chart.css` is linked in `index.html` right after
`css/components/column.css`. Inline SVG written by the client: no chart library, no build step, no
other origin (the page's CSP stays `style-src 'self'`: no `style` attribute; colours reach the sheet
through `data-vars`, `core/dom.js:vars`, as `views/costs-models.js` and `ui/parts.js:meter` do).

- `lineChart({ label, points, series, values, format })` and `stackChart({ label, points, series,
  values, format })` return markup. `points` are the answer's (`batch`, `n`, `closed`, `unpriced`);
  `values` the tile's, aligned with `points` (`null`, a number for a one-series tile, or a dict keyed
  by series); `series` are `{ key, word, color, dash }` with `color` a token (`var(--…)`);
  `format(value)` writes a value.
- **Lines** (the tiles Q8 and Q9 name as lines: CRs, rounds, duration, cost per merged CR): one
  polyline per series, cut at each `null` (a run of one point is drawn as its mark only); a round
  mark on every point; a series may be dashed (`dash: true`), so two lines are told apart without
  colour (the CRs tile: `held` dashed in `var(--accent-light)`, `merged` solid in
  `var(--state-merged)`); a one-series tile uses `var(--accent)`.
- **Stacks** (Q24, the stacked tiles: model calls by part, spend per batch): stacked bars, one bar
  per point, its segments in the series' order, bottom first; a point whose value is `null` has no
  bar, its slot left empty (the gap of Q10, never a zero); no stacked area. Parts: `steering` `var(--accent-dark)`, `drivers` `var(--accent)`, `workers` and
  `agents` `var(--accent-light)`, the Costs card's shades (`model/spend-by.js`'s `SHADE`); model
  series `m1`...`m8` in `var(--m1)` to `var(--m8)`, `other` in `var(--m8)` (Q21); `unsplit`
  `var(--queued-bar)`, a neutral grey token that exists. No new colour token is needed.
- **Geometry**: the plot fills the tile's width at a fixed height (a new size token
  `--chart-height`, section 6); the y axis starts at zero; one hairline baseline and one top line
  in `var(--line)`. Lines and marks keep their thickness and roundness at any width, and bars their
  gap (for instance a `viewBox` with `preserveAspectRatio="none"`, `vector-effect:
  non-scaling-stroke`, marks as zero-length round-capped strokes). The labels are
  HTML under and beside the SVG, in `var(--text-small)` and `var(--ink3)`: the axis word
  `dashboard.axis` ("batch"), each point's batch number when the range shows at most 12 points, else
  the first, the last and every fifth (Q18 risk 1); the top value and 0 on the left.
- **Reading a value** (Q12): each point has a transparent hit area over its whole column, focusable,
  with an `aria-label` that says the batch, its closing day and each series' value (`format`, and
  "not all priced" when `unpriced`; "no figure" for a `null` value). Hover, keyboard focus and a tap
  (a tap focuses it) light the column (`var(--accent-tint)`) and write the same text in the chart's
  readout line above the plot (`aria-live="polite"`); with nothing pointed, the readout shows
  `dashboard.read_hint` ("Point at a batch to read it"). One tab stop per chart: the focused column
  has `tabindex="0"`, the others `-1`; Left, Right, Home and End move between columns.
  `bindCharts(root)` binds this by delegation and writes only the readout's text (no store write, so
  a push repaints nothing it holds). No click action, zoom, export or legend toggle.
- **Legend**: under the plot, one entry per series drawn: a swatch (a short line, dashed when the
  series is, or a square for a stack) and its word. Never a series told by colour alone: word in the
  legend, dash for lines, order of the stack as in the legend, every value in the readout.
- `css/components/chart.css`: tokens only, no literal length, no side border (DESIGN.md "Tokens",
  "No side accent border"; `tests/test_board_design.py`).

### 6. DESIGN.md (`clients/web/DESIGN.md`) (Q13)

- **Components table**: one row, `chart | css/components/chart.css | js/ui/chart.js | chart, chart-*`
  (the format `tests/test_board_design.py:components` reads; its `test_components` then checks no
  other sheet styles `chart*`).
- **Tokens**: `css/tokens.css` gains `--chart-height: 160px` (kind `size`, use "a chart's plot
  height"), placed after `--phone-max`, and the table its row in the same place
  (`test_token_table`). No colour token is added.
- **A section after "Waits on a card"** (or after the batch-30 sections already there, at the end),
  **"Dashboard"**: a read-only view whose figures come from the server's `dashboard.get` op
  (`board/dashboard_page.py`), computed from the closed batch records, apart from the drawing; the views
  compute no figure; one point per closed batch, never per day; a figure a record lacks is no
  point (a cut line, an empty bar slot), never a zero, and each tile says how many batches it covers;
  charts drawn by the `chart` component as inline SVG (lines, and stacked bars for the stacked
  tiles), no chart library; colours from existing tokens (the Costs
  card's part shades, `--m1`…`--m8` by the project's all-time model cost order, `--m8` the "other
  models" when there are more than eight, `--queued-bar` for "not split", `--accent-light` dashed
  and `--state-merged` for held and merged); never a series by colour alone (words, dash, stack
  order, readout); a value on hover, focus and tap; the tile is the figure card; the range selector reuses
  `.seg` of `css/views/costs-models.css` unchanged (not a component; moving it is a separate CR);
  every word an i18n key of `en-dashboard.js` / `fr-dashboard.js`. No protected feature is added;
  the Costs page and its protected features are untouched.

### 7. What does not change

The Costs page and its files (`views/costs*.js`, `css/views/costs*.css` including `.seg` in
`costs-models.css`, `model/receipt.js`, `model/spend-by.js`, `model/history.js`, `model/models.js`:
read or imported, never edited); `board/state.py` and what `project.state` holds; the batch record,
`cost`, `close`; AGENTS.md (as board-history: a read-only op of the surface server over the records
it already reads is within its stated scope); the CR board pane (`hooks/`, `STATUS.json`), the
cards, the agents. `docs/web-board.md` is left to docs-gardening (Q19). The server gains one module
and one op (sections 1 and 2) and nothing else.

## Rounds (Q27)

One CR, both tabs. The Driver orders the rounds: (1) `board/dashboard_page.py`, the op and
`tests/test_board_dashboard.py`; (2) the page, its address, the feed, the chart component and the
Productivity tab; (3) the Spending tab. The PR's screenshots cover both tabs.

## Out of scope

Per-day, per-week or per-month charts; human interactions per PR; cycle times (kickoff to PR, to
first review, to merge); PRs opened per day; runs by agent type; cost split into compute, platform
and inference; a Scorers tab; charts across projects ("All projects"); the running batch's live
point; budgets against costs; any change to the batch record, to `cost` or to what `close` writes
(Q17). A list of CRs or PRs by date and period totals (the History page's, Q14); a link to or from
History; a click-through from a point, zoom, export, legend toggles (Q12); a `dashboard` topic;
moving `.seg` into a component; the user docs (docs-gardening, Q19).

## Known gaps

- Batch-01 to batch-16 hold no dates and no batch cost: they show in the CRs and rounds tiles and in
  the ranking of CRs (their per-CR costs) only (Q10, Q25).
- Batch-17 to batch-22 hold no split: one "not split" bar by part and by model; batch-23 holds a
  split without calls and no models: no bar in the calls tile, "not split" by model.
- A release CR records 0 rounds and lowers its batch's mean (batch-19, a release alone, shows 0.0)
  (Q26).
- A model's colour on the Dashboard follows the project's all-time cost order, the Costs card's
  follows the one batch's: they may differ (Q21).

## Overlaps in batch-30 and the UI night

No `depends.json` (Q14); the stack settles each shared edit, whichever lands second rebases.

- **`js/views/registry.js`, `js/i18n/en.js` / `fr.js` (`nav.*`, one import and spread),
  `js/ui/icons.js`, `index.html` (two sheets: `css/components/chart.css` after
  `css/components/column.css`, `css/views/dashboard.css` after the Costs sheets)**: also edited by
  CR-439 (Help, after Home and the Inbox), `board-user-inbox` (Inbox, right after Home) and
  `board-history` (History, after PRs, before Costs). Each adds its own line. The order once all
  have landed: Home, Inbox, Help, Triage, Kanban, Batch, PRs, History, Costs, Dashboard,
  Configuration (Q20).
- **`js/core/router.js`, `js/core/store.js`, `js/core/api.js`**: CR-434 (`TABS`, `tabOf`, `settle`,
  the store's `batchTab`), CR-439 (`topicOf`, `helpTopic`), CR-440 (`triageFolded`),
  `board-user-inbox` (`inboxMarks`), `board-history` (`historyOf`, `hp=` / `hd=`, `historyPeriod` /
  `historyDate`, and its own read in `api.js`). This CR adds `dashOf`, `dt=` / `dr=`, three store
  fields and one read in `api.js`; the address keys do not clash (`t` is the Batch view's, `h`
  Help's, `hp` / `hd` History's).
- **`board/api/protocol.py`, `board/api/protocol.json`, `board/api/ops.py`, `docs/server-api.md`**:
  `board-history` (`2-backlog/P3/board-history`) adds its `history.get` op and `history` topic;
  CR-427 (`4-batch/`) edits `docs/server-api.md` (`backlog.move`); CR-429 (`4-batch/`) its "The
  topics" paragraph and how the server watches. This CR adds one args model, one op, one handler and
  one ops-table row. Whoever lands second regenerates `protocol.json` with `just protocol-schema`.
- **`tests/test_server_api_calls.py`**: its every-op test asserts `good.seen == set(protocol.OPS)`,
  so each CR adding an op adds its call there (`board-history` its `history.get`, this CR its
  `dashboard.get`); whoever lands second keeps both.
- **`DESIGN.md`**: CR-427, CR-433, CR-434, CR-440 edit the "One card, one column, one chip" rule;
  CR-435 and CR-441 the Batch title row; CR-439, CR-440, `board-user-inbox` and `board-history` add
  sections. This CR adds one Components row, one token row and its own section; it touches no rule
  another CR edits. **`css/tokens.css`**: no other batch-30 spec adds a token, as their specs stand.
- **`tests/test_board_design.py`**: CR-439, `board-user-inbox` and `board-history` add tests there
  that assert their own entries' places; this CR's (Evidence 3) asserts only Dashboard's neighbours.
- **CR-429** (the server's watch and cache): changes how the project state is pushed and cached, not
  what it holds; `history` stays in it and `reads.state_of` stays the way to read it, so the op works
  on either side (if CR-429 renames `state_of`, the second lander follows the rename).
- **CR-441, CR-433, CR-435, board-griller**: no shared file expected.
- **docs-gardening** (`2-backlog/P1`, last in batch-30): adds the page to `docs/web-board.md` with
  its picture (Q19); this PR's screenshots are its input.

## Evidence

**Checks in `just check`**, each reading the shipped files at the head under test, never a copy:

1. **The figures** (Q18 risk 2, Q23), new `tests/test_board_dashboard.py`, in-process, calling the
   shipped `board/dashboard_page.py:answer` on prepared records (a prepared input: the real records change
   and cannot hold every edge case; the shipped module is what runs), parametrized and fast, no Node.
   The records cover:
   - a back-filled record (CRs with `rounds` and per-CR `cost_usd`, no `opened`, `closed` time,
     batch `cost_usd` or `cost_receipt`): a point in CRs and rounds, none in duration, calls, cost
     per merged CR or spend; its CRs in the ranking (Q25); the coverage counts say so;
   - a record with `cost_usd` and no `cost_receipt` (batch-17-like): one `unsplit` segment equal to
     its cost, by part and by model;
   - a split without `calls` and no `models` (batch-23-like): no calls value; split by part,
     `unsplit` by model;
   - two records with split, calls and models (one with an `agents` part: `drivers` and `workers`
     not drawn), segments summing below `cost_usd` (an `unsplit` rest) and one above it (the bar is
     the sum);
   - a dropped CR (held, not merged; its cost in its batch's cost and in the ranking);
   - a merged CR with `rounds: 0` (counted in the batch's and the pooled mean) and a merged CR with
     no `rounds` (left out of both) (Q26);
   - a merged CR with `cost_usd: null` (out of the ranking) (Q25);
   - a record with `cost_unpriced` non-empty (`unpriced` on its point and on the headlines);
   - a record with no merged CR (no cost-per-merged-CR value, no rounds value);
   - nine models over all the closed records, one of them costly only in a record outside the
     `"10"` range: the rank is the all-time one (seven own series and `other`), and the same model
     has the same key under `"10"` and `"all"` (Q21); a second case with eight models: `m1` to `m8`,
     no `other`;
   - the live batch's own `running` record, and a stale record shaped as `batch-20.json`
     (`state: "running"`, a `number`, `closed: null`) beside it: both out of every figure and of
     `closed_total`;
   - 25 closed records for the range: `"10"` and `"20"` keep the newest by number, `"all"` keeps all,
     oldest first;
   - a record with a wrong-typed value (a string `cost_usd`, a `crs` that is not a list): no value
     where it is needed, no exception;
   - expected numbers: held and merged totals, the pooled rounds mean, the duration median (odd and
     even counts), the call total, the cost-per-merged-CR ratio, the spend total, the outside sum and
     its coverage, the top ten's order (ties by batch then CR) and its coverage.
   And through the op (`board/api/ops.py:call` on a prepared board, as `tests/test_server_api_calls.py`
   does): `dashboard.get` with `range: "15"` is 400 naming `range`, and with an unknown project 404.
2. **The protocol**: `tests/test_server_api_calls.py`'s every-op test gains
   `good("dashboard.get", {**good.args, "range": "10"})` and checks its `now` and `range` (it asserts
   every op of `protocol.OPS` is called); `tests/test_server_protocol.py`'s existing check of
   `protocol.json` against the models passes on the regenerated file.
3. **The shipped client files**, a new test in `tests/test_board_design.py`: `js/views/registry.js`
   has an entry `id: 'dashboard'` with no `overview` and no `count`, the entry before it is `costs`
   and the one after it `config`; `index.html` links `css/components/chart.css` right after
   `css/components/column.css`. The existing self-contained check,
   `test_the_web_frame_is_self_contained_and_follows_the_style_rules` in
   `tests/test_code_targets.py`, keeps covering the new files (no other origin, the style rules).
4. Existing checks that now cover the new files: `test_the_web_frame_has_small_scripts_and_both_word_files_share_their_keys`
   (`en-dashboard.js` / `fr-dashboard.js`, the 300-line limit),
   `test_files_and_functions_are_small_and_the_imports_have_no_cycle` (`board/dashboard_page.py`),
   `test_board_design.py`'s `test_token_table` (`--chart-height`), `test_sheets` and
   `test_components` (`chart.css`, `dashboard.css`, the new Components row), `test_one_card`,
   `test_a_card_title_is_one_line_with_its_full_text_on_hover`; Biome and Ruff (`just lint`).

**Before the push** (AGENTS.md: a change under the CLI's `src/`): `just check` and
`just eval-dry-run` in the worktree at the rebased head; the pipeline's `just scenario
(ubuntu-latest)` green at the PR's head before the PR. The pane screenshot rule does not apply
(neither `hooks/register.tsx` nor `STATUS.json` changes). `just mod` is not owed (no `hooks/` or
`types/` change).

**By hand, in the PR's Deliverables** (DESIGN.md: screenshots are the visual record), `chantier
board` served from the PR's head on the real planning surface (`gsemet-foss-planning-surface`,
project `chantier`), captioned with the head's seven-character SHA:

1. Productivity, English, last 20 batches (back-filled batches in the CRs and rounds tiles only, the
   coverage lines, the live line for batch-30).
2. Spending, English, by role, with a value read on hover.
3. Productivity, French.
4. Spending, French, by model (the ranking shows back-filled CRs when the range is "all").
5. The narrow layout (375 px), one tab.

And a short written check: Dashboard sits between Costs and Configuration; a tab and a range survive
a reload and a copied address, and Back returns to the previous one; Tab reaches a chart and the
arrows walk its batches with the readout following; a tap reads a point on the phone; the switch is
the same choice on Costs; a model keeps its colour between "last 10" and "all"; a CR row opens its
PR in a new tab; on "All projects" the view opens on the last real project; `dashboard.get` answers
with `curl` on `api/v1/call/dashboard.get` (as `docs/server-api.md` shows for `costs.get`); the
figures of one batch (for instance batch-29: 36 CRs, $243.54, its split and models) match its Costs
receipt.

Host and default matrix: none (the page depends on neither the host nor a configured value).

## Open questions

None. v1's five open questions are decided: 1 by dashboard-Q20 (A), 2 by Q21 (A, ranked over all
closed records), 3 by Q22 (A), 4 by Q23 (B: server and pytest), 5 by Q24 (A: stacked bars).
