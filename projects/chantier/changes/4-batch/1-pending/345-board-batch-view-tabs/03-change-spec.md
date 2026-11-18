# Change Specification: the Batch page's central view gets tabs (graph, Gantt, time cards)

## Goal

On the board's Batch page, the user wants more than one way to see the same batch. The central
view goes under three tabs, placed under the "States and arrows, hover for the legend" line:

- **Graph** (the default): today's dependency graph. A CR that has just changed state carries a
  small burst for 10 minutes.
- **Gantt**: one line per CR on a real time scale, from the batch's start to now, with a "now"
  line. A CR's bar is split into coloured segments, one per period the CR spent in a state, each in
  that state's colour. The open segment of a CR that is not finished runs to the "now" line and is
  hatched. A CR that has not started is a cross at the right edge. The graph's arrows are drawn as
  vertical arrows between the lines.
- **Time cards**: one paper time card per CR, as in the prototype's view 1
  (`intake/prototypes.html`, `intake/1-carte-de-pointage.jpg`). Each round is one stamped line,
  then the verifier line, the PR and the cost. A merged CR gets the red MERGED stamp. A CR at round 3
  or more gets an orange REWORKED ×N stamp.

Every CR of a live batch shows the Triage priority chip of the stage it came from (Inbox, P1...P4,
3-ready) on its card in every tab, derived by the board from the CR's `add` event.

The whole page stays uniform with the `board-design-system` redesign, on the user's word ("Keep the
Gantt uniform with the redesign in this CR"): tokens only, no side accent border, the one card, the
one chip, no new one-off style.

In this document, `<cli>` is `skills/chantier/scripts/cli/src/chantier` and `<web>` is
`<cli>/board/web`. The pieces this CR uses from `board-design-system` (not merged yet) are named
as that CR's specification names them: `<web>/DESIGN.md`, `<web>/js/ui/card.js` `card(parts)`,
`<web>/js/ui/parts.js` `priorityChip(bucket)`, the sheets `<web>/css/components/card.css` and
`chip.css`, and its blocking test `tests/test_board_design.py`.

## Decisions carried from `02-answers.md`

| Source | Decision | Where it lands |
|---|---|---|
| tabs-Q1 (A) | The Gantt uses real time, from the batch's start to now, with a "now" line. A CR that has not started is a cross stuck to the right edge. | §3 |
| tabs-Q2 (B) | The burst stays for 10 minutes after the state change, whatever the user does (reload, tab change, hover). | §2, §5 |
| tabs-Q3 (A), read by the CoS | Both tabs draw the declared dependencies only (`after`), as today's graph does. The option text the user picked wrongly named the stack base; its point, "the same arrows as the graph", holds. | §3, §6 |
| tabs-Q4 (A) | An orange "REWORKED ×N" stamp (French "RETOUCHÉ ×N"; N is the CR's rounds) on a CR at round 3 or more. It is distinct from the red MERGED stamp, and both may show together. | §4 |
| tabs-Q5 (the user) | A CR's bar is split into segments, one per period in a state (working, blocked, ready, merged...), each in that state's colour from the tokens. The current, open segment runs to the "now" line and stays hatched. | §3, §5 |
| CoS | The open tab is kept in the URL. The graph is the default tab. | §1 |
| CoS | Each non-default tab's module is imported on its first opening, with dynamic `import()`. | §1 |
| CoS | Start, end and per-round times come from the batch's `events.jsonl` as the board already reads it. No new CLI command. | §5 |
| CoS | Every label goes through the i18n keys, in every language. | §8 |
| CoS | The time card follows the prototype's view 1: one card per CR, one stamped line per round (coder, inspector), the verifier line, the PR and the cost, the MERGED stamp in red. | §4 |
| CoS | The priority chip comes from the `add` event's `origin`, with no CLI change: `1-inbox/…` Inbox, `2-backlog/P<n>/…` P<n>, `3-ready/…` 3-ready. Closed records show no chip. | §7 |
| CoS | Closed batches keep no events: their Gantt and time-card tabs show a "no times kept" note. | §1, §5 |
| CoS | This CR depends on `board-design-system` (it uses its card, chip and tokens): `depends.json`. | §9 |
| CoS, after the critic | `costs-stamp.css` stays untouched (protected). The time card's stamps are a variant inside `card.css`'s `paper` variant, on the same tokens. | §4, §9 |
| CoS, after the critic | The graph's levels keep today's look, on tokens only; they do not become `column()`. | §2 |
| CoS, after the critic | It stays one CR; the time cards build on the Gantt's `times.py`. | §4, §5 |
| The user, after the grill | Every new view uses `board-design-system`'s rules and shared pieces: tokens only, the one card and chip components (the priority chip as in Triage), no side border, no new one-off style. | §2, §3, §4, §9 |

## What changes

### 1. The tabs (`<web>/js/views/batch.js`, `<web>/js/core/router.js`, `<web>/js/core/store.js`)

- **Where the tabs sit.** The legend line (`legend()` in `views/batch-graph.js`: the "States and
  arrows" pill and `batch.legend_hint`) moves out of `graphBlock` into `batch.js`. It stays on top
  for every tab, because the Gantt segments use the same state colours. Right under it comes a tab
  bar with three tabs, in this order: Graph (`graph`), Gantt (`gantt`), Time cards (`cards`). The
  selected tab's panel comes under the bar. The figures and the mode strip above, and the PR column
  on the right of a live batch, stay as they are for every tab.
- **Markup.** `role="tablist"` (labelled `batch.tabs`) holds
  `<button role="tab" aria-selected aria-controls>`. The panel is `role="tabpanel"`. The left and
  right arrow keys move between tabs. The tabs are the one chip of `css/components/chip.css`, in its
  toggle form (filled when on, outlined grey when off, as Kanban's priority filters in
  `board-design-system`'s `target-columns.html`). The bar has no style of its own beyond layout
  (flex, gap) in `css/views/batch.css`.
- **The URL.** The router is the only module that writes the address, so it gains a `t=` parameter
  that it reads and writes only on the Batch view:
  - `resolve()` reads `t` and keeps it when it is `gantt` or `cards`. Any other value, or no value,
    means `graph`.
  - `href()` writes `t` only when the tab is not `graph`.
  - `go()` accepts `tab` in the place it is given, as it accepts `batch`.
  - The tab is kept while the user moves between batches with the navigator on the Batch view. Any
    other view clears it.
  - A tab click calls `go({ tab })` the way the batch navigator moves, so back and forward walk the
    tabs.
  - The store gains `batchTab`, set by `apply()`.
- **Lazy modules.** The two new views are `<web>/js/views/batch-gantt.js` and
  `<web>/js/views/batch-timecards.js`. `batch.js` imports neither statically. On the first render
  that needs one, it calls `import('./batch-gantt.js')` (or `'./batch-timecards.js'`), keeps the
  promise, and paints a short loading line (`batch.tab_loading`). When the import resolves, it
  triggers a repaint at once, without waiting for the 5 s poll. If the import fails, the panel shows
  `batch.tab_failed`, and the next opening of the tab tries again. The graph stays a static import,
  because it is the default tab.
- **`mount` and `after`.** These keep their duties for the graph: arrows, resize, light. They call
  the open tab's own `after` and `mount` when it has them. A tab change cleans up the previous
  tab's listeners. `drawEdges` runs only when the graph tab is shown.
- **Closed batches.** The tab bar shows on a closed record too. The graph tab draws as today. The
  Gantt and time-card tabs each show only the note `batch.times_none` ("This batch's record keeps
  no times"), because a closed record keeps no events (§5). Their module is not imported for a
  closed record.

### 2. The graph tab (`<web>/js/views/batch-graph.js`)

- **Levels.** The graph's levels (`level()`: `.lvl` and its head `.lvlh`) keep today's look and
  markup, on tokens only (as `board-design-system` makes every sheet). They do not become
  `column()`.
- **The one card.** The nodes are built by `card()` (`board-design-system` moves `node` and
  `recordedNode` there); this CR adds the priority chip at the live node's top left (§7).
- **The "just changed state" burst.**
  - The burst shows on a live batch's node (`node()`, not `recordedNode`) when the row's
    `times.state_at` (§5) is less than 10 minutes before `state.now`.
  - The node then carries a small icon (a new `spark` entry in `<web>/js/ui/icons.js`) in the
    card's top row, after the priority chip and the CR chip, before the state badge. Its `title` is
    `batch.changed_ago` ("Changed state {age} ago", with `age()` from `core/format.js`).
  - The icon plays its burst animation once when it appears. Under `prefers-reduced-motion: reduce`
    it is static. Its colour is the CR's state token, `--state-<vstate>` (`vstate(c)` from
    `model/semantics.js`), and `--state-queued` for a cancelled CR (no `--state-cancelled` token
    exists). Its class (`spark`) is styled in `css/views/batch-graph.css`; it is not a card
    variant, and the card gets no border, ring, shadow or side change.
  - The burst ends at the first repaint after the 10 minutes. The poll refreshes `state.now` every
    5 s even when the record has not changed (`core/refresh.js`, `clock`), so no timer of its own
    is needed. Because it is computed from the record's timestamp, a reload, a tab change or a
    hover neither restarts nor clears it (tabs-Q2 B).
  - The burst shows on the graph tab only.

### 3. The Gantt tab (`<web>/js/views/batch-gantt.js`, `<web>/css/views/batch-gantt.css`)

- **Scale.** The axis runs from the batch's start to `state.now` (tabs-Q1 A). The start is the
  batch payload's `created`, or the first event's `t` when `created` is absent. A thin vertical
  "now" line sits at the right end, labelled `batch.gantt_now`. Ticks fall on whole hours, or on
  whole days when the batch spans more than 48 h. They are labelled in the browser's local time
  (HH:MM, or the short date for day ticks).
- **Rows.** There is one row per CR, in the graph's row order (the record's `order`). The left
  label cell is the one card in its compact variant (the graph node's), built by `card()`: the
  priority chip (§7), the CR chip, the title (clamped as in the graph), the state badge (the same
  `stateIcon` and word as the graph). No phase line and no meta band in the Gantt's label. The card
  opens the CR's folder (`opener(crKey(c))`), as a graph node does on a live batch.
- **Bars: segments by state (tabs-Q5).**
  - A started CR's bar is the sequence of its `times.segments` (§5), each drawn from its `from` to
    its `to`, filled with its state's token `--state-<state>` (`--state-working`,
    `--state-blocked`, `--state-draft`, `--state-ready`, `--state-local`, ...), the colours of the
    graph's badges and the legend.
  - The open segment (`to: null`, present only while the CR is not finished) runs to the "now"
    line and is hatched: diagonal stripes in its state's token over the panel's background. Its
    state is the row's current visible state (`vstate(c)`), so the open segment always matches the
    card's badge.
  - A finished CR (merged or cancelled: `times.ended_at` set) has only solid segments. Its bar ends
    at `ended_at` with a small round end mark: `--state-merged` for a merged CR, `--state-queued`
    for a cancelled one. A CR handed back ready that waits for its merge is not finished: its open
    segment (ready, draft or local) stays hatched up to now.
  - Each segment has a `<title>`: the state's word (`state.<s>`) and its interval
    (`batch.gantt_span`, "{from} – {to}", HH:MM, "now" for the open one). The bar's start time is
    written at its left end as HH:MM, and its end time at its right end once finished.
  - A CR with no `started_at` has no bar: a cross (×) stuck to the right edge of its row, in
    `--state-queued`, with the `<title>` `batch.gantt_not_started`.
- **Vertical arrows.** These are the graph's arrows: the pairs from the shared `edges(rows)` (§6),
  the declared dependencies only, nothing more and nothing less.
  - Each arrow is a vertical segment at the x of the waiting CR's start (or at the right edge for a
    CR that has not started). It runs from the row of the CR it waits for to the row of the waiting
    CR, with an arrow head on the waiting CR's row, in the graph arrows' stroke token.
  - Hover or focus on a row lights it and its neighbours and dims the rest, as `light()` does on the
    graph, with the same `related()` set and the card's own dimmed and highlighted variants.
    `light()` is generalised to the cards of the open panel (`[data-id]`), not only `.node`.
- **Drawing.** The time area (segments, hatch, end marks, crosses, arrows, ticks, "now" line) is one
  SVG drawn from data. x and width are percentages of the axis, as SVG attributes. The hatch is one
  `<pattern>` per state in `STATE_ORDER`, its stripes carrying a class per state whose stroke is
  that state's token in `batch-gantt.css`; no colour is written in markup. No `style=` is written
  in markup (the `test_code_targets.py` rule). Any position that has to be measured (the row
  heights, which follow the label cards) is measured after paint, as `drawEdges` does, and redrawn
  on a resize.
- **Narrow screens.** On a narrow screen the Gantt scrolls horizontally inside its panel, as
  `.gscroll` does for the graph, and the label column stays visible.
- **Style.** `css/views/batch-gantt.css` only lays the view out (grid of label and time area,
  gaps, the label column's width) and gives the SVG's classes their fill and stroke through tokens.
  The cards and chips come from the component sheets. No side border, no raw value.

### 4. The time-cards tab (`<web>/js/views/batch-timecards.js`, `<web>/css/views/batch-timecards.css`)

There is one card per CR, in the graph's row order, in a grid that fills the width
(`repeat(auto-fill, minmax(...))`, the minimum from a size token). Its times come from the same
`times` field as the Gantt (§5). Each time card is the one card, built by `card()`, in a new
`paper` variant defined in `css/components/card.css` (paper fill, ruled lines, mono type, the
ticket shadow: the receipt's tokens `--paper`, `--paper-line`, `--paper-ink`, `--paper-grain`,
`--shadow-ticket`, `--mono`). Its parts follow the card's one anatomy and the prototype's view 1:

- **Top row.** The priority chip (§7) at the top left, then the CR chip, then `timecard.number`
  ("No. {n}" / "N° {n}", n the CR's number) at the right.
- **Title.** The CR's title, under a centred caption `timecard.title` ("TIME CARD" / "CARTE DE
  POINTAGE").
- **Body (the card's free block): one stamped line per round.** These come from `times.rounds`, in
  order. Each line shows the round (`R{n}`), the coder stamp (`{HH:MM} ▣ coder`) and the inspector
  stamp (`{HH:MM} ▣ insp`), or `…` when that round has no inspector time yet. Stamp text is in the
  stamp ink, slightly tilted, as in the prototype. Labels: `timecard.coder`, `timecard.insp`.
- **The verifier line.** When `times.verifier_at` or `times.verdict_at` is set, the line shows
  `{HH:MM} ▣ verifier` (`timecard.verifier`) and the verdict word (`timecard.verified` "VERIFIED",
  or `timecard.unverified` for any other result).
- **Times.** Times are local HH:MM. When a stamp falls on another day than the card's previous
  stamp, the short date is prefixed.
- **Meta band.** The PR (`PR #{n}` with `prNumber()`, or `timecard.no_pr` "no PR" / "pas de PR")
  on the left, then the rounds (`timecard.rounds`, "{n} rd") and the cost (`usd(c.cost_usd)`) at the
  right end.
- **Stamps.**
  - **State stamp, as in the prototype.** Merged: `timecard.merged` "MERGED" / "MERGÉ", red
    (`--bad-ink`). Ready (the ready-to-merge, PR-in-draft and ready-locally visible states):
    `timecard.ready`, accent. Working: `timecard.working`, stamp ink, dashed. Queued, waits,
    blocked and cancelled cards carry no state stamp: the badge already says it, and the prototype
    stamps only these three.
  - **Rework stamp.** At `c.round >= 3`: `timecard.reworked` "REWORKED ×{n}" / "RETOUCHÉ ×{n}",
    n = `c.round`. Orange, at its own place (top right, under the number, so it never covers the
    state stamp), with its own tilt. Both stamps may show together (tabs-Q4 A).
- **Where the stamps are styled.** The stamps are a variant inside `card.css`'s `paper` variant
  (`card-stamp` parts with their `merged`, `ready`, `working` and `rework` variants), built on the
  same tokens as the receipt's stamp. `css/views/costs-stamp.css`, `css/views/costs-receipt.css`
  and `js/views/costs-image.js` are not touched: the receipt and its stamp are protected features
  of `DESIGN.md`. Tilts and opacities are custom properties declared in `card.css` with the variant.
- **Colours.** All tokens. If `tokens.css` has no orange meant for a stamp, add one semantic token
  `--stamp-rework` (the value of the prototype's orange) and list it in `DESIGN.md`'s token table;
  the round lines' ink is an existing ink token or one new `--stamp-ink`, listed the same way.
- **Interaction.** A card opens the CR's folder on a live batch, as a graph node does.
- **Target look.** `intake/1-carte-de-pointage.jpg`, with the board's tokens, not the prototype's
  own values.
- **Layout sheet.** `css/views/batch-timecards.css` holds only the grid and its gaps.

### 5. The data: times and segments per CR from `events.jsonl` (`<cli>/board/times.py`, `<cli>/board/crs.py`)

The page today gets only the last 40 events (`EVENTS_SHOWN` in `board/state.py`), and without the
`phase` kind. The server already reads the whole file once per state (`read_events(folders[0])` in
`project_state`) and hands it to `crs.cr_rows`. This CR derives the times there, from that same
list: no new CLI command, no new endpoint, no new read, no write. `EVENTS_SHOWN`, `EVENT_KINDS` and
the `events` field stay as they are.

A new module, `<cli>/board/times.py`, has `cr_times(events, c) -> dict` (with small helpers) and
`priority_of(events, c) -> str | None` (§7). `crs._row` adds their results to each row as
`"times"` and `"priority"`. From the CR's own events (`e.cr == c.id`), in file order:

| Field | Value |
|---|---|
| `started_at` | `t` of the first `take`, else `null`. A retake (`take` with `restart`) does not move it. |
| `ended_at` | Merged (`c.status == "merged"`): the entry's `merged_at` if set, else `t` of the last `handback` with `result: merged` or `order` with `order_kind: merged`. Cancelled: `t` of the last `cancel`, else of the last `order` with `order_kind: drop`. Any other state: `null`. |
| `state_at` | `t` of the last event that moves the CR's shown state: `take`, `round`, `handback`, `pr-draft`, `cancel`, and `order` with `order_kind` `merged` or `drop`. For a merged CR, its `merged_at` if later. Else `null`. A CR's `add`, `phase` or `verdict` is not a state change. |
| `segments` | The periods from `started_at`, each `{"state", "from", "to"}`, by the rules below. `[]` when not started. |
| `rounds` | One entry per round, in order: `{"n", "coder_at", "inspector_at"}`. A `round` event opens round `n` (its `round` field; one without it opens the previous n + 1), `coder_at` its `t`. Only the first event for a given n counts. `inspector_at` is the `t` of the first `phase` event with `phase: inspector` after it and before the CR's next `round` event, else `null`. |
| `verifier_at` | `t` of the last `phase` event with `phase: verifier`, else `null`. |
| `verdict`, `verdict_at` | `result` and `t` of the last `verdict` event, else `null`. |

**Segments.** Walking the CR's events from its first `take`, each event sets the state that holds
from its `t`:

| Event | State from then |
|---|---|
| `take`, `round` | `working` |
| `handback` `result: blocked` | `blocked` |
| `handback` `result: ready` | `draft` (a handed-back CR with no other word, as `vstate` reads it) |
| `pr-draft` `draft: false` / `draft: true` | `ready` / `draft` |
| `handback` `result: merged`, `order` `merged`, `cancel`, `order` `drop` | none: the bar ends |

A new segment opens only when the state differs from the open one; the previous segment's `to` is
the new one's `from`. When `ended_at` is set, the last segment closes at `ended_at` (so a
`merged_at` later than the last event closes it there); otherwise the last segment has
`"to": null` (open, drawn hatched to now with the row's current visible state, §3). The states are
the board's visible-state words, so each maps to its `--state-*` token.

- **Order and timestamps.** Times are the events' ISO `t` strings, passed as they are. File order is
  time order (`orders_reorder.py` relies on it too), so no sort is needed.
- **Closed batches.** A closed record (`5-archives/batches/batch-NN.json`) keeps no events: its rows
  (`recordRows`) carry no `times` and no `priority`, and the Gantt and time cards show
  `batch.times_none` (§1).
- **Size limits.** `times.py` stays under `MAX_FILE_LINES` (400) and each function under
  `MAX_FUNCTION_LINES` (50). `crs.py` only gains the two calls.

### 6. One list of arrows for both tabs (`<web>/js/model/semantics.js`, `views/batch-graph.js`)

- Add `edges(rows)` to `model/semantics.js`. It returns the `[from, to]` pairs `drawEdges` draws
  today: for each row `c`, each `d` of `c.after` whose row is present, the pair `[d, c.cr]`.
- `drawEdges` and the Gantt both use it; neither builds its own list. Only declared dependencies
  are drawn; the stack base is not an arrow in either tab.

### 7. A batch CR's priority chip, from its `add` event (`<cli>/board/times.py`, `<cli>/board/crs.py`, the card builders)

No CLI change: nothing new is recorded. `add_cr` already logs `add` with `origin`, the CR's folder
before it entered the batch, relative to the repository (`commands/opening.py:52`, `:75`).

- **`priority_of(events, c)`** reads the `origin` of the CR's `add` event and matches its path
  segments (whatever planning-folder prefix precedes them): a `1-inbox` segment gives `inbox`;
  `2-backlog` followed by `P1`...`P4` gives that `P<n>`; a `3-ready` segment gives `3-ready`; no
  `add` event, no `origin` or no match gives `null`.
- **`crs._row`** adds `"priority"` with that value. `recordRows` (closed records) adds none: closed
  records show no chip.
- **The chip.** Every card of a live batch CR with a priority (graph node, Gantt label, time card,
  and the PR card of the same CR in the PR column, built by `batch-pr-card.js`) shows
  `priorityChip(c.priority)` at its top left, exactly as `board-design-system` draws it on backlog
  cards (Inbox neutral, P1...P4 filled in the ramp, 3-ready on the accent tint). A CR with no
  priority shows no chip. This replaces `board-design-system`'s note that a batch CR's cards get no
  chip.

### 8. Words (`<web>/js/i18n/`)

- `en.js` and `fr.js` are near the 300-line script limit, so the new keys go into new files merged
  as `en-board.js` is: `en-batch.js` and `fr-batch.js`, imported and spread in `en.js` and `fr.js`.
- New keys:
  - Tabs: `batch.tab_graph`, `batch.tab_gantt`, `batch.tab_cards`, `batch.tabs`,
    `batch.tab_loading`, `batch.tab_failed`, `batch.times_none`.
  - Burst: `batch.changed_ago`.
  - Gantt: `batch.gantt_now`, `batch.gantt_not_started`, `batch.gantt_span`.
  - Time cards: `timecard.title`, `timecard.number`, `timecard.coder`, `timecard.insp`,
    `timecard.verifier`, `timecard.verified`, `timecard.unverified`, `timecard.no_pr`,
    `timecard.rounds`, `timecard.merged`, `timecard.ready`, `timecard.working`,
    `timecard.reworked`.
- The English and French files hold the same keys (the existing test checks it). No label is
  written in the code. The state words reuse `state.<s>`; the chip's words are
  `board-design-system`'s.

### 9. Design rules (`board-design-system`)

This CR lands after `board-design-system` and builds on it: its `DESIGN.md` rules, its one card
builder, its priority chip and its component sheets; it passes that CR's blocking test (no side
border, no raw value outside `tokens.css`, no component class styled in two sheets, no card built
outside `card()`). The CR's `depends.json` names `board-design-system`: a real need, since it uses
that CR's builder and chip, not just a shared file.

- **New sheets.** `css/views/batch-gantt.css` and `css/views/batch-timecards.css` lay out only, as
  `DESIGN.md` allows a page sheet. The `paper` card variant and its stamps live in
  `css/components/card.css`. Every new sheet is linked in `<web>/index.html`, after
  `batch-graph.css`. Each sheet stays under `MAX_STYLE_LINES` (300), with no id selector and
  nesting of 3 at most.
- **`DESIGN.md`.** It gains the time card (the card's `paper` variant and its stamps) as a
  protected paper object, next to the receipt and its stamp, the variant in the card's row of the
  component table, and any new token in its token table.

### 10. Docs

`docs/web-board.md`, section "Batch": describe the tabs and the `t=` address, the burst and its 10
minutes, the Gantt (scale, segments by state, the hatched open segment, the cross, arrows identical
to the graph's), the time cards (lines, stamps), the priority chip on a live batch's CRs (from the
stage the CR came from), and the "no times kept" note of a closed batch. Add one screenshot of each
new tab, made like the section's existing one.

## Out of scope

- The prototype's other three views (departure board, building, telex) and any other page.
- A burst on the Gantt, the time cards, Home or Kanban.
- A stack-base arrow (the graph does not draw one today).
- Any change to the CLI's lifecycle or records: `events.jsonl`, `batch.json`, `summary.json`, the
  closed record, `STATUS.json`, or the Claude Code pane (the pane's screenshot rule does not apply).
- The Costs receipt and its stamp (`costs-stamp.css`, `costs-receipt.css`, `costs-image.js`).
- A new look for the graph's levels.
- New CLI commands, endpoints or event kinds; times or chips for closed records.
- The rest of `board-design-system`'s scope.

## Evidence

- **Tests (pytest, in-process, few and parametrized),** in a new `tests/test_board_times.py`:
  - One parametrized test of `board/times.cr_times` on prepared event lists. Cases: a CR taken,
    rounds 1 to 3 with inspector phases, a verifier phase and a verdict, then merged with
    `merged_at` (segments working, draft, ready, working..., all closed at `merged_at`); merged with
    only an `order merged`; merged by `handback merged`; cancelled by `cancel`; cancelled by
    `order drop`; never taken (all null, `segments: []`, `rounds: []`); a retake that leaves
    `started_at` at the first take; a round with no inspector phase yet; a blocked then retaken CR
    (working, blocked, working, open); a CR handed back ready still open (last segment `draft` with
    `to: null`); `state_at` following the last `handback` or `pr-draft`, not a `phase`.
  - One parametrized test of `board/times.priority_of`: an `add` origin under `1-inbox`,
    `2-backlog/P2`, `3-ready`, under a planning prefix (`.agents/changes/3-ready/...`), and no
    `add` event, giving `inbox`, `P2`, `3-ready`, `3-ready`, `null`.
  - The `just test` budget holds.
- **`tests/test_code_targets.py` passes**: sizes, no `style=` or `on…=` in JS markup, no colour
  outside `tokens.css`, both word files sharing their keys, and the dynamic
  `import('./batch-gantt.js')` and `import('./batch-timecards.js')` resolving inside the web folder.
- **`board-design-system`'s blocking test passes** on the new and changed sheets and views.
- **`just check`** and **`just eval-dry-run`** (a change under the CLI's `src/`), in the worktree at
  the pushed head. **`just scenario (ubuntu-latest)`** green at the PR's head.
- **Manual check, recorded in the PR**, on a project with a running batch (the scenario's
  surface-board project):
  1. `v=batch` opens on the graph, the address has no `t=`; the levels look as before.
  2. Clicking Gantt sets `t=gantt`; the network panel shows `batch-gantt.js` fetched only then;
     Back returns to the graph.
  3. A reload with `t=cards` opens the time cards.
  4. A CR whose state changed less than 10 minutes ago carries the burst; it survives a reload and
     is gone after the 10 minutes.
  5. In the Gantt, each bar shows coloured segments in the legend's colours; a working or ready CR's
     last segment is hatched up to the "now" line in its badge's colour; a merged CR's bar is solid
     with its end mark; a queued CR is a cross at the right edge; the vertical arrows match the
     graph's arrows one for one.
  6. A time card of a CR at round 3 or more shows the orange REWORKED ×N stamp, and the merged ones
     also the red MERGED stamp.
  7. On a batch opened at the PR's head with one CR added from `3-ready`, one from
     `2-backlog/P<n>` and one from `1-inbox` (the scenario's surface-board project), each CR shows
     its chip (3-ready, P<n>, Inbox) on its node, Gantt label, time card and PR card; no card has a
     side accent border.
  8. The FR language shows every label in French.
  9. A closed batch shows its graph with no chips, and the "no times kept" note in the Gantt and
     time-card tabs.
  10. The Costs receipt and its stamp, and its image copy, look unchanged.

  Attach screenshots of the three tabs at the PR's head (SHA in the caption).

## Working choices (settled by the Spec-writer; no open question left)

1. Finished bar: a CR is finished when merged or cancelled; a CR handed back ready keeps a hatched
   open segment (ready, draft or local) until it merges.
2. Past ready periods are `draft` unless a `pr-draft draft: false` made them `ready`; the open
   segment takes the row's current visible state, so it always matches the badge.
3. The Gantt label and the time card are the one card (compact and `paper` variants); the tabs are
   the one chip in its toggle form.
4. Queued, waits, blocked and cancelled time cards carry no state stamp, as in the prototype.
5. The tab bar shows on a closed record; its Gantt and time-card tabs show only the note.
