# Batch graph: one arrowhead per CR, lit arrows on top, a mode tooltip

On the board's Batch page, the graph of connected cards shows which CR waits for which, and this
change makes it read right. A CR that waits for several others gets one arrowhead at one point of
its left edge. On hover or focus, the lit arrows are drawn above the cards. Each word of the
Stack / Series / Parallel switch also gets a tooltip that says how to change a batch's mode. Web
client only, in English and French. No server, protocol, CLI, card or record change.

## Goal, in the user's terms

The user, 2026-11-15 (`intake/request.md`, translated):

- "The design of the connected cards is not very functional; it shows the interdependencies (keep
  that purpose, make it work)."
- "The arrowheads are wrong when a card has several sources" (batch-18's CR-275, which waits for
  CR-268 to CR-274).
- "A tooltip on 'Stack', 'Series', 'Parallel' saying: to switch, ask the Chief of Staff to
  'change the batch to stack' (with the mode named)."

The other four points filed are delivered elsewhere (batch-view-Q1). The goal of the UI night
(2026-11-21) is a working UI with the least scope.

## Decisions carried (02-answers.md)

| Answer | Decision | Where |
| --- | --- | --- |
| Scope notes (2026-11-17), batch-view-Q1 | Only two points are left: the graph's arrows when a CR waits for several others (and following a CR's dependencies), and the tooltip on the three modes. The navigator, the removed Merged column, one place per CR with a badge, and "Level N" are done (checked at `3b3eba06`). | Out of scope |
| batch-view-Q2 | A repair, not a redesign. The levels stay columns, each CR keeps one place, the cards stay white and the arrows grey, and the hover light stays. No new layout, view or library. | 1, 2 |
| batch-view-Q3 | All the arrows of a CR that waits for several others arrive at one point: the middle of its card's left edge, arriving level. One arrowhead shows there, whole and touching the card. The same holds for two sources and for seven. | 1 |
| batch-view-Q4 | Hover or focus lights a CR, what it waits for and what waits for it, as today. The lit arrows are then drawn whole, above the cards they cross. Unlit arrows stay behind the cards. Nothing else is added: no list on the card, no click to pin. | 2 |
| batch-view-Q5 | The Gantt's arrows do not change. | 1, Out of scope |
| batch-view-Q6 | The tooltip sits on each of the three words of the switch, in the title row as CR-435 leaves it. It uses the page's own tooltip pattern (the legend pill's: shown on hover and keyboard focus), not a browser `title`. The mode pill's tooltip (CR-435) does not change. | 3 |
| batch-view-Q7 | On a mode the batch is not in: `To switch, ask the Chief of Staff to "change the batch to <mode>"`. On the batch's own mode: "This batch's mode." Both texts exist in English and French. | 3, 4 |
| batch-view-Q8 | Clicking a mode does nothing: the board edits no batch and messages no agent. | 3 |
| batch-view-Q9 | A closed batch: its mode words have no switch tooltip. Its graph gets the same arrows and light as a live one. | 1 to 3 |
| batch-view-Q10 | On a phone, the switch is hidden (as today and in CR-435), so its tooltips are too. The arrows follow the same rules at every width. | 3, Evidence |
| batch-view-Q11 | The proof is pictures of a Batch graph that has a CR waiting for at least three others in different rows, plus one arrow that skips a level. They are taken on the board's demo, extended for this (it has no such CR), before and after, with the tooltip in both languages. | 6, Evidence |
| batch-view-Q12 | Queued in batch-30 after CR-435; CR-433 and CR-434 are taken as landed. Web client only, with `DESIGN.md` and `docs/web-board.md` kept true. | Overlaps |
| batch-view-Q13 | Out of scope: the Kanban, the Gantt, the Time cards, the PR column, the figures, a clickable switch, routing arrows around cards, the CR board pane, and Q1's points. | Out of scope |

**What the code shows today** (read at `3b3eba06`, `js/views/batch-graph.js`):

- `path()` already ends every arrow level, at the middle of the waiting card's left edge, after a
  12 px straight tail.
- Each graph arrow carries its own `marker-end="url(#ar)"`. A card with n sources therefore gets
  n heads drawn on top of each other.
- With a light on, the dimmed arrows (`path.dim`, opacity 0.15) pass their opacity to their own
  heads. Seven stacked heads at 0.15 add up to a nearly opaque grey head under faint lines.
- The lit arrow (`path.hl`, `--accent`) keeps a grey head (`.head`, `--edge-arrow`). The head does
  not follow the light.
- The SVG layer is under the levels (`svg.edges` `z-index: 0`, `.lvl` `z-index: 1`). An arrow
  that skips a level crosses behind the cards of the level it skips, even when lit.

So Q3 costs code: one head per waiting card, drawn once (Q11's "no code" case does not hold). Q4
needs a second layer above the cards.

## What changes

All paths are under `skills/chantier/scripts/cli/src/chantier/clients/web/` unless named in full.
Read `DESIGN.md` first and keep it true (AGENTS.md). Find places by their text: line numbers move
with CR-433, CR-434 and CR-435.

### 1. One arrowhead per waiting CR (`js/views/batch-graph.js`, `css/views/batch-graph.css`)

- `path(graph, from, to)` keeps its geometry: the curve, the level tail of `TAIL` (12 px), and the
  end at the middle of the target's left edge. It loses `marker-end="url(#ar)"`. A graph arrow is
  a line only.
- `drawEdges(root, rows)` draws, after the arrows, **one head per CR that has at least one arrow
  into it**:
  - `<path class="head" data-to="<cr>" d="…">`, a filled triangle the size of today's marker (8 px
    long, 8 px tall);
  - its tip is the end point of that CR's arrows (the middle of its card's left edge), and its
    base is 8 px to the left, centred on the same line;
  - one head per waiting CR, whatever its number of sources (2 or 7); never one per arrow.
- The tail (12 px) stays longer than the head (8 px). The head therefore lies on the straight,
  level stretch that all of the CR's arrows share: whole, touching the card, pointing at it, and
  never under a card or across another.
- `marker()` stays exported and unchanged: the Gantt (`js/views/batch-gantt.js`) still uses it and
  its `marker-end` (Q5). The graph no longer puts the marker in its SVG.
- `light(root, rows, id)`: on top of today's path loop (`svg.edges path[data-from]`, which a head
  does not match: it has no `data-from`), a loop over `svg.edges path.head[data-to]`:
  - a head is `hl` when one of the lit arrows ends at it, that is when its `data-to` is `id` and
    `id` has an arrow into it, or when its `data-to` is the `to` of an arrow from `id`;
  - with a light on, every other head is `dim`;
  - with no light, a head is neither.
- Style, in `css/views/batch-graph.css` (tokens only):
  - `.batch svg.edges .head` keeps `fill: var(--edge-arrow)` and `stroke: none`;
  - `.batch svg.edges .head.hl { fill: var(--accent); stroke: none; }`. The `stroke: none` is
    needed here: a lit head is a `path.hl`, and `.batch svg.edges path.hl` (stroke `--accent`,
    width 2) outranks `.batch svg.edges .head`, so without it the lit head would get a 2 px
    outline and grow past the card's edge;
  - `.batch svg.edges .head.dim { opacity: 0.15; }`, the same opacity as `path.dim`;
  - the head gets the paths' `transition` on `fill` and `opacity`.

### 2. Lit arrows above the cards

- `graphBlock(...)` draws a second SVG layer after the levels, inside `.graph`:
  `<svg class="edges top" aria-hidden="true"></svg>`. The first one, `svg.edges`, stays before the
  levels, and both closed and live graphs get the second one.
- `drawEdges` gives the top layer the same `width` and `height` as the base layer and leaves it
  empty. It then calls `light` (as today) when a light is in force.
- `light(root, rows, id)`, when the root holds a `svg.edges.top`:
  - it fills that layer with copies (`cloneNode`) of the lit arrows (`path.hl[data-from]`) and of
    the lit heads (`path.head.hl`), taken from the base layer only (`svg.edges:not(.top)`);
  - its class loops (arrows and heads) run on `svg.edges:not(.top)` too, so they never match the
    top layer's copies; the copies carry the `hl` class they were cloned with;
  - with `id` null it empties the layer.

  The base layer keeps every arrow, lit or not: the copy only draws the lit ones a second time, on
  top. The Gantt has no `svg.edges.top`, so it skips this step and stays as it is (Q5).
- Style:
  - `.batch svg.edges.top { z-index: 2; }`: above `.lvl` (`z-index: 1`) and below the page's tips
    (`z-index: 4`). It keeps `pointer-events: none` and `overflow: visible` from `svg.edges`, so a
    hover still reaches the cards under it;
  - the rule sits right after `.batch svg.edges` in `batch-graph.css`.
- Unlit, the picture is today's: grey arrows behind white cards. Lit, the CR's arrows show in
  `--accent`, whole, end to end, with their heads, over the cards they cross. The dimmed cards and
  arrows keep today's dimming.
- Nothing else is added: no list of dependencies on the card, no click to pin a light, no routing
  of the arrows around cards (Q4, Q13).
- The file's head comment says it: one head per waiting CR, and the lit arrows drawn again above
  the cards. `batch.js`'s graph comment needs no change.

### 3. The mode switch's tooltips (`js/views/batch-head.js`, from CR-435)

CR-435 moves the switch (`MODES`, the `.ms` span with one span per mode, the current one `on`)
into `js/views/batch-head.js`, under `.bmode` in the title row. This CR changes only how each mode
word is built there:

- **Live batch** (the running batch, whose `batchMode` branch draws the mode and the legend):
  - each mode word becomes
    `<span class="[on]" tabindex="0" aria-describedby="mstip-<mode>"><word><span class="tip" id="mstip-<mode>" role="tooltip"><sentence></span></span>`,
    where `<word>` is today's `t('mode.<mode>')`;
  - `<sentence>` is `t('mode.current')` for the batch's own mode, and
    `t('mode.switch_to', { mode: t('mode.<mode>').toLowerCase() })` for each of the two others.
  - A batch with no CR yet is a live batch: it shows the switch (CR-435 draws the mode for it)
    and gets the same tooltips.
- **Closed batch** (`shownRecord`): the mode words stay as today: plain spans, no `tabindex`, no
  tip (Q9). A closed record with no mode shows no switch, as today.
- No click handler. A click or Enter on a mode word does nothing (Q8): the board edits no batch,
  and the Chief of Staff changes the mode on the user's word (`order mode`).
- The mode pill (`.mpill`, `#mtip`, the mode's sentence) and the legend pill do not change (Q6).

Style, in `css/views/batch.css` (tokens only):

- **Child selectors.** CR-435's `.bmode .ms span` and `.bmode .ms span.on` become
  `.bmode .ms > span` and `.bmode .ms > span.on`. Otherwise their padding, radius, colour and
  weight would reach the tip, which is a span inside a mode word.
- `.bmode .ms > span[tabindex] { position: relative; cursor: help; }`: the word anchors its tip
  and shows it has one, like the two pills (CR-435's `cursor: help`).
- The show rule, on the legend pill's pattern: `.bmode .ms > span:hover .tip`,
  `.bmode .ms > span:focus .tip` and `.bmode .ms > span:focus-within .tip` get `{ display: flex; }`.
- `.bmode .ms .tip { left: auto; right: 0; color: var(--ink2); font-weight: 400; }`:
  - the tip anchors at the word's right edge, because the switch sits at the title row's right end
    and a tip anchored on the left would run past the screen, where `.main`'s
    `overflow-x: hidden` would cut it;
  - its colour and weight are the legend tip's, whatever the word's state (`on` is `--ink` 500,
    off is `--ink3`).
- The tip keeps CR-435's `.bmode .tip` rule: `position: absolute`, `top: calc(100% + 6px)`,
  `z-index: 4`, `max-width: 300px`, `white-space: normal`.
- Phone (`@media (max-width: 760px)`): nothing new. `.bmode .ms { display: none; }` (CR-435) hides
  the words and their tips (Q10).

### 4. Words (`js/i18n/en.js`, `js/i18n/fr.js`, beside the `mode.*` keys)

| Key | en | fr |
| --- | --- | --- |
| `mode.switch_to` | `To switch, ask the Chief of Staff to "change the batch to {mode}"` | `Pour changer, demande au Chief of Staff : « passe le batch en {mode} »` |
| `mode.current` | `This batch's mode.` | `Le mode de ce batch.` |

`{mode}` is the board's mode word in lower case, in the board's language:

- English: stack, series, parallel;
- French: stack, série, parallèle.

The French uses the familiar "tu" form, as `notice.key` and `writer.box.conflict` do in `fr.js`
(open question 1). No other key is added or removed.

### 5. DESIGN.md

- In the section `## The Batch page's title row` (added by CR-435), one bullet: on a live batch,
  each word of the Stack / Series / Parallel switch carries a tooltip on the legend pill's pattern
  (hover, focus, focus-within; `cursor: help`). The tooltip is anchored at the word's right edge,
  so it stays within the screen. It says how to ask the Chief of Staff to switch (`mode.switch_to`),
  or "This batch's mode." (`mode.current`). There is none on a closed batch. A click does nothing.
- A new short section, `## The Batch graph's arrows`:
  - an arrow goes from the right edge of a CR to the middle of the left edge of the CR that waits
    for it, and arrives level;
  - all of a CR's arrows share that point, under one arrowhead drawn once per CR
    (`path.head[data-to]`), never one per arrow;
  - unlit arrows are drawn behind the cards;
  - on hover or focus, the lit arrows and their heads are drawn again in `--accent` in a layer
    above the cards (`svg.edges.top`, `z-index` 2, no pointer events), so an arrow that skips a
    level can be followed end to end;
  - no routing around cards, and no new colour, size or token;
  - the Gantt keeps its own markers.

### 6. The demo and the docs

- **Demo** (`docs/demo/projects/shop-api/changes/4-batch/`). CR-148 (localised-receipts, queued
  in `1-pending`) is made to wait for three CRs:
  - in `batch.json`, the CR-148 entry's `after` becomes `["CR-141", "CR-145", "CR-146"]`;
  - add `1-pending/148-localised-receipts/depends.json` with the same `after`, in the form of the
    demo's other `depends.json` files.

  CR-141 and CR-146 are in level 0, in different rows, and CR-145 is in level 2 (CR-142, then
  CR-143, then CR-145). CR-148 therefore lands in level 3, with three sources in three rows, and
  two of its arrows skip levels 1 and 2: Q11's case. No test reads `docs/demo/`. The board reads
  `after` from `batch.json` (`board/crs.py`, `"after": list(c.after)`).
- **`docs/web-board.md`**, "Batch":
  - In the graph paragraph (the one with "an arrow goes from a CR to the one that waits for it"),
    add: "A CR that waits for several others takes all its arrows at one point of its left edge,
    under one arrowhead. When you hover or focus a CR, its arrows are drawn above the cards, so an
    arrow that skips a level can be followed from end to end."
  - Where the paragraph names the mode switch in the title row (CR-435's text), add: "On a running
    batch, hover a mode of the switch to see how to change it: ask the Chief of Staff to 'change
    the batch to series' (the board changes nothing itself)."
- **Screenshots** (`scripts/docs_screenshots.py`, `just docs-screenshots`). After CR-434 the
  Batch page opens on the Kanban, so no shipped picture shows the graph (open question 2):
  - in `views()`, the desktop tab loop becomes `("graph", "gantt", "cards")`, and its
    `wait_for_selector` also waits for `.graph svg.edges path.head`;
  - this gives `docs/web-board/batch-graph-pc.png`, shown in `docs/web-board.md` under the graph
    paragraph: `![The batch's graph: levels and the arrows between CRs](web-board/batch-graph-pc.png)`.

  Commit the pictures the run changes. The demo's new dependency also shows in the Kanban cards,
  the project Kanban and the Gantt, so expect `batch-pc.png`, `batch-phone.png`,
  `batch-gantt-pc.png`, `kanban-pc.png`, `kanban-phone.png`, `panel-pc.png` and
  `panel-phone.png`. The PR names each picture that changed.

  The demo also loses its next CR to start: CR-148 is today the one ready to start, so its "next"
  tag and the "queued, next CR-148" line go away once it waits for CR-145 and CR-146 (both
  active). Any picture that shows that tag or that line changes too, beyond the list above; the
  PR names those as well.

## Overlaps

batch-30, this CR after CR-435, built on the following as landed:

- **CR-435** (board-batch-compact, `4-batch/1-pending/435-board-batch-compact`). This CR edits
  CR-435's files:
  - `js/views/batch-head.js`: the switch's mode words;
  - `css/views/batch.css`: the `.bmode .ms` rules become child selectors, and a tip rule is added;
  - DESIGN.md's title-row section;
  - `docs/web-board.md`'s Batch paragraph.

  It keeps CR-435's `.bmode .tip` and `#mtip` rules whole.
- **CR-434** (board-batch-kanban). The Kanban is the default tab. This CR touches neither
  `router.js`, `store.js` nor `batch-kanban.js`. It writes its docs sentences on top of CR-434's
  rewrite of the same paragraph, and its screenshot change follows from CR-434's default (section
  6).
- **CR-433** (board-batch-chip-stale). It changes the chip on a graph node (`node()` in
  `batch-graph.js`, `js/ui/card.js`). This CR does not touch `node()`, `recordedNode()` or the
  card. A text conflict in `batch-graph.js` keeps CR-433's node whole.
- **CR-427** (Triage's last column) and **CR-429** (the server's watch): no shared file except the
  screenshot run and other sections of `docs/web-board.md` and DESIGN.md.
- **CR-425** (factory-redefine): nothing beyond what CR-435 already takes in.
- **CR-439** (board-help-page, `4-batch/1-pending/439-board-help-page`): `en.js` / `fr.js` keys,
  a test in `tests/test_board_design.py`, and a DESIGN.md section. Text only, no shared behaviour.
- **CR-440** (board-triage-polish, `4-batch/1-pending/440-board-triage-polish`): Triage
  screenshots and a test in `tests/test_board_design.py`. Text only, no shared behaviour.
- **docs-gardening** (`2-backlog/P1/docs-gardening`, last in batch-30): it owns the end
  correction of `docs/web-board.md` and retakes the batch screenshots that the batch-30 CRs left
  stale. This CR still writes its own sentences and commits the pictures its run changes (section
  6); docs-gardening keeps the ones that still match and corrects the rest after it.

  board-history, board-griller, board-user-inbox and dashboard-pages: none touches the Batch
  graph or the switch. Whichever lands last rebases its text.

## Out of scope

- The Kanban, Gantt (its arrows and markers included) and Time cards views, the PR column, the
  figures, the navigator, the levels' layout and the cards' content.
- A clickable mode switch, or any write from the board.
- Routing arrows around cards; a list of dependencies on a card; a click to pin a light.
- The mode pill's own tooltip and the legend.
- The CR board pane (`hooks/`): its screenshot rule does not apply.
- The points delivered elsewhere (Q1).

## Evidence

Every check reads the shipped files from the repository at the head under test. No prepared text
stands in for a shipped file.

**Test** (`skills/chantier/scripts/cli/tests/test_board_design.py`, one test, parametrized where
natural; `just test` within its limit). It reads the shipped files:

- `js/views/batch-graph.js`:
  - `path(` builds no `marker-end`;
  - `drawEdges` builds `class="head"` with `data-to`;
  - `graphBlock` holds `class="edges top"`;
  - `light` handles `path.head` and `svg.edges.top`;
- `js/views/batch-gantt.js` still has `marker-end="url(#ar)"` (the Gantt is unchanged);
- `css/views/batch-graph.css`:
  - `.batch svg.edges.top` declares a `z-index` greater than the one of `.batch .lvl`;
  - `.batch svg.edges .head.hl` fills with `var(--accent)` and declares `stroke: none`;
  - `.batch svg.edges .head.dim` has the opacity of `.batch svg.edges path.dim`;
- `js/views/batch-head.js` builds `aria-describedby="mstip-`, `id="mstip-`, `role="tooltip"`, and
  uses `mode.switch_to` and `mode.current`;
- `css/views/batch.css`:
  - has no `.bmode .ms span` rule without `>`;
  - has the three show rules for `.bmode .ms > span … .tip`;
  - its `.bmode .ms .tip` declares `right: 0`;
- `js/i18n/en.js` and `js/i18n/fr.js` both hold `mode.switch_to` (with `{mode}`) and
  `mode.current`. The English one holds `To switch, ask the Chief of Staff to "change the batch to {mode}"`.

`test_sheets`, `test_components` and `test_token_table` pass unchanged: tokens only, no new token,
no component restyled.

**Pictures and measures** (in the PR's Deliverables, captioned with the head's seven-character
SHA; on the demo, `just docs-screenshots`, plus a one-off Playwright run, not shipped):

- The graph tab of shop-api's batch at 1400 × 860, **before** (the base of the stack) and
  **after**, with the demo change in both: CR-148 in level 3 with three arrows. Each of the two
  is taken twice: unlit, and with CR-148 hovered. The defect shows mainly with a light on (the
  stacked dimmed heads, the grey head on a lit arrow, the lit arrows behind the cards), so the
  hovered pair is the one that proves the change.
- After, measured and stated in the PR:
  - exactly one `svg.edges:not(.top) path.head[data-to="CR-148"]`;
  - its tip within 1 px of the middle of CR-148's card's left edge;
  - each of the three `svg.edges:not(.top) path[data-from][data-to="CR-148"]` ends at that same
    point (the last `L` of its `d`).
- After, with CR-148 hovered:
  - the top layer holds its three arrows and one head, in `--accent`;
  - a picture shows the arrows from CR-141 and CR-146 drawn over the cards of levels 1 and 2;
  - a second picture with CR-146 focused by the keyboard (Tab) shows the same.
- A closed batch's arrows: the demo's closed records (mobile-app's) hold no `after`, so they draw
  no arrow. The arrows and the light of a closed batch therefore rest on the live graph's checks
  above and on the code path both share (`graphBlock`, `drawEdges`, `light`, which the test reads);
  the PR says so. The closed batch below (`?p=mobile-app&v=batch&b=batch-01&t=graph`) serves only
  the switch's check (no tooltip, no `tabindex`).
- The switch at 1400 × 860, on the running batch (mode `stack` in the demo):
  - one picture with the tooltip of "Series" open: `To switch, ask the Chief of Staff to "change
    the batch to series"`;
  - one with "Stack" open: "This batch's mode.";
  - the same two in French (the board's language switch): « passe le batch en série » and "Le mode
    de ce batch.";
  - measured: each tip's `bounding_box` lies inside the viewport (right ≤ `innerWidth`);
  - a click on "Series" changes nothing (the page and the record stay as they are).
- On the closed batch above: hovering a mode word shows no tooltip, and the words have no
  `tabindex`.
- At 375 × 812: the switch is not displayed, the graph shows CR-148's one head, and the page has
  no horizontal scroll.

**Gates.** `just check`, `just eval-dry-run` (a change under the CLI's `src/`), and the
pipeline's `just scenario` green at the PR's head (AGENTS.md). If this CR is the stack's top, it
also owes the local `chantier gate` at its head before the user merges. No scenario step is added:
the scenario drives no browser.

## Open questions

Each one is stated with its options. A is recommended and is the one built.

1. **The French tooltip's wording.**
   - A: `Pour changer, demande au Chief of Staff : « passe le batch en {mode} »`, with the
     familiar "tu" and the French mode word in lower case (série, parallèle). This is the form of
     `fr.js`'s other asks to the Chief of Staff.
   - B: the polite "vous" (`demandez`).
   - C: keep the English mode word (`series`) inside the French quote.
2. **A shipped picture of the graph.**
   - A: add the graph tab to `docs_screenshots.py` (`batch-graph-pc.png`) and show it in
     `docs/web-board.md`, because once CR-434 makes the Kanban the default, no shipped picture
     shows the graph this CR fixes.
   - B: keep the pictures in the PR only.
