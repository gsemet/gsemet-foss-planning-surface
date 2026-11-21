# Batch page: the mode and the legend move into the title row

The board's Batch page loses its two full-width rows above the views. The mode band and the
"States and arrows" line move up into the page's title row, beside `Batch ‹ batch-30 ›`. The
four figures, the view switch and the central view start about 90 px higher. Nothing shown today
is removed, at desktop and at phone widths, except the legend's "hover for the legend" hint on a
phone (760 px and below), where the two pills alone stay. This is a layout change of one page of
the web client only. No server, protocol, CLI or card changes.

## Goal, in the user's terms

"il faut reduire la perte de place verticalement" (2026-11-21, `intake/screenshot-2026-11-21.png`).
On batch-30's page, between the four figures and the graph, two rows hold little and take a lot:

- the mode band: "Stack · Foreman", its one-sentence explanation, and the Stack / Series /
  Parallel switch on the right;
- the legend line: the "States and arrows" pill and its "hover for the legend" hint.

Both arrows end in the title row: one mid-row, one at its right end. The circles hold the band's
label and sentence and the legend line; the switch is not circled and follows its band.

## Decisions carried (02-answers.md)

| Answer | Decision | Where |
| --- | --- | --- |
| 1 (compact) | The mode band (mode and steering, its sentence, the Stack / Series / Parallel switch) and the legend line go up into the page's top rows. The figures, the view switch and the views move up. This is the Chief of Staff's reading of the arrows, and the user may correct it. | What changes, 1 to 3 |
| 1 (restatement) | The explanation sentence is kept. Nothing is removed (compact-Q5 excepts the legend's hint on a phone). | What changes, 2 and 4 |
| 1 (restatement) | The board-batch-kanban CR's toggle joins the existing view switch. This CR keeps that one switch as the first line above the views. | What changes, 3; Overlaps |
| 2 | Destination batch-30, queued last. | Overlaps |
| 3 | The spec's open questions go to a Fable advisor in the user's place; its answers are 4 and 5. A new open question is stated with options, A recommended, and A is built. | Open questions |
| 4 (compact-Q4) | Everything goes into the title row. The breadcrumb row (sticky, shared by every page, hidden on a phone) and "+ New" stay untouched. Both arrows end in the title row; the switch follows its band, at the row's right end as today. | What changes, 1; Out of scope |
| 5 (compact-Q5) | The mode's sentence is a tooltip alone, at every width, no short form, on the legend pill's pattern (shown on hover, focus and focus-within). Every moved tip rule is rescoped under `.bmode`; the mode pill has its own show rule for `#mtip`. At 760 px and below `.bmode .lghint` is hidden and the pills stay. The mode pill gets `cursor: help`, as the legend pill. | What changes, 2, 4, 5; Evidence; Open questions |

**Reading of "top rows".** Both arrows end at the title row's height (`Batch ‹ batch-30 ›`, the
`.titlerow` of `index.html`, lines 68-72). The breadcrumb row above it is the sticky bar shared by
every page, and it holds the "+ New" button. It does not change (compact-Q4). The order inside
the row is the spec's choice, not the user's; the user may correct it on the after picture.

## What changes

All paths are under `skills/chantier/scripts/cli/src/chantier/clients/web/` unless named in
full. Read `DESIGN.md` first and keep it true (AGENTS.md).

### 1. The title row gets a batch slot

- **`index.html`**: in `.titlerow`, after `#stats`, add one element:
  `<div class="bmode" id="batch-mode" hidden></div>`. The title row sits outside `#view` and so
  outside `.batch` (`index.html` lines 68-74): no rule scoped `.batch …` reaches the slot.
- **`js/main.js`**: `drawFrame` paints `#batch-mode` with `batchMode(state)` and hides it when the
  markup is empty, as `paintNav` does for `#batch-nav`.
- **`js/views/batch-head.js`** (new): it exports `batchMode(state)`. The code it holds moves out of
  `js/views/batch.js`: `MODES`, `modeBand` and `legend`, with their comments. It returns:
  - `''` unless the project is not `ALL` and the view is `batch`;
  - for a closed record (`shownRecord(state.data, state.batchId)`): the mode, when the record has
    one (as `recorded` does today), then the legend;
  - for the live batch with no CR yet (`noCrYet`): the mode only, as today (no legend, no views);
  - for the live batch: the mode, then the legend;
  - with no batch: `''`.
- The order in the slot (the spec's choice, compact-Q4): the mode pill, the legend pill with its
  hint, then the mode switch pushed to the right end of the row.

### 2. The mode pill and its sentence

- The mode label keeps its words, `<mode> · <steering>` (`modeWords`, `steeringFactoryWord`). It
  becomes a pill, class `mpill`, with the colours of today's band: the `--accent-tint` fill and the
  `--accent` text, weight 500. No new token.
- The sentence (`words.text`, the `mode.<mode>.text` keys) moves into a tooltip on that pill, at
  every width, with no short form and no inline copy (compact-Q5):
  - the pill gets `tabindex="0"` and `aria-describedby="mtip"`;
  - the tip is `<span class="tip" id="mtip" role="tooltip">`, inside the pill, as `#lgtip` is
    inside `.lgpill`;
  - it shows on hover, focus and focus-within, by its own rule (section 4), so a tap opens it on a
    phone.
- Both pills get `cursor: help` (compact-Q6, A: the shipped legend pill is `cursor: default`).
- The Stack / Series / Parallel switch (`.ms`, the current mode `on`) keeps its look. It sits at
  the right end of the title row (`margin-left: auto` inside the `flex: 1` slot). On a phone it
  stays hidden, as `@media (max-width: 760px) .batch .ms { display: none; }` hides it today.
- The legend pill (`.lgpill`, `#lgtip`) and its hint (`.lghint`) keep their markup, words and
  tooltip.
- No i18n key is added or removed: `batch.legend`, `batch.legend_hint`, `batch.arrow`, `mode.*`
  and `state.*` are reused.

### 3. The Batch view loses the two rows

- **`js/views/batch.js`**: `render` and `recorded` no longer draw `modeBand(...)` or `legend()`:
  - the live page becomes figures, then `.bwrap` (`.gcol`: `tabBar`, the panel; then `prsBlock`);
  - the closed page becomes figures, then `.bwrap.one` (`.gcol`: the deps note, `tabBar`, the
    panel);
  - the no-CR page becomes figures, then the empty state.
- The view switch (`tabBar`: Kanban, Graph, Gantt, Time cards once CR-434 has landed) is now the
  first line of `.gcol`, right under the figures.
- The file's head comment and the legend's comment ("It stays on top of every tab") follow. The
  legend now sits in the title row, so it stays visible on every tab.

### 4. Style

- **`css/views/batch.css`**: these rules leave the `.batch` scope for `.bmode` and keep their
  declarations, except for the changes listed after them:
  - `.batch .mode`, `.mb`, `.ms`, `.ms span`, `.ms span.on`;
  - `.lgrow`, `.lgpill`, `.lghint`;
  - every tip rule: `.batch .tip`, `.batch .tip .k` and `.batch .tip .an` become `.bmode .tip`,
    `.bmode .tip .k` and `.bmode .tip .an`;
  - the legend's show rule: `.batch .lgpill:hover .tip`, `.batch .lgpill:focus .tip` and
    `.batch .lgpill:focus-within .tip` become `.bmode .lgpill:hover .tip`,
    `.bmode .lgpill:focus .tip` and `.bmode .lgpill:focus-within .tip`.

  No `.batch .tip`, `.batch .lg*`, `.batch .mode`, `.batch .mb` or `.batch .ms` rule remains.

  The changes:
  - `.bmode`: `display: flex; flex: 1; align-items: center; flex-wrap: wrap;` with a `space` token
    gap. It has no band fill, no padding and no bottom margin.
  - `.bmode .mpill`: the legend pill's padding and radius (`--space-off-3` `--space-off-10`,
    `--radius-pill`), `--text-small`, weight 500, filled with `--accent-tint`, `--accent` text,
    `position: relative` for its tip, `cursor: help`;
  - the mode pill's own show rule for `#mtip`: `.bmode .mpill:hover .tip`,
    `.bmode .mpill:focus .tip`, `.bmode .mpill:focus-within .tip { display: flex; }`;
  - `.bmode .lgpill`: `cursor: default` becomes `cursor: help` (compact-Q6, A);
  - `.lgrow` loses its `margin-bottom`;
  - the tip keeps `position: absolute` under its pill and `z-index: 4`. It must draw above the
    figures' tiles below the title row, whole, not clipped. If a tile or the view's layer covers
    it, the fix is placement only, under `.bmode` or on `.titlerow` (`position: relative` with a
    `z-index` below `.head`'s 5);
  - the phone block (`@media (max-width: 760px)`): `.bmode .ms { display: none; }` (moved) and a
    new `.bmode .lghint { display: none; }`; the pills stay. The phone rule `.batch .mode
    { flex-wrap: wrap; }` goes, because `.bmode` always wraps.
- The title row's baseline alignment (`css/shell.css`, `.titlerow { align-items: baseline; }`)
  stays. The slot's pills sit on the title's line. `css/shell.css` changes only if the slot needs
  `align-self` to centre on the title, or for the tip's stacking above; any such change is
  placement only.
- Every value is a token (DESIGN.md "Tokens"). No new token, colour or class outside `.bmode` and
  its children.

### 5. Desktop and phone

| Width | Title row after the change |
| --- | --- |
| Desktop (above `--phone-max`, 760 px) | `Batch ‹ batch-30 ›` · mode pill · legend pill and hint · … · switch at the right. On a narrow desktop the row wraps (`.titlerow` already has `flex-wrap: wrap`), the slot going to a second line whole. |
| Phone (760 px and below) | The breadcrumb is hidden, as today. `Batch`, then the navigator on its own line (`.batchnav { flex-basis: 100%; }`, as today), then one line with the mode pill and the legend pill; the hint and the switch are hidden. The page has no horizontal scroll at 375 px. A tip opens on tap (focus) and stays within the screen's width (its `max-width: 300px`, anchored at the pill's left). |

### 6. DESIGN.md

- "A batch with no CR yet": "its four figures, the mode strip and the page's empty state" becomes
  "its four figures, the mode in the title row and the page's empty state".
- Add a short section, `## The Batch page's title row`. It says:
  - the mode (`<mode> · <steering>`, its sentence in a tooltip at every width), the "States and
    arrows" legend and the Stack / Series / Parallel switch sit in the title row, built by
    `js/views/batch-head.js` and styled under `.bmode` (the title row is outside `.batch`);
  - no full-width band or legend line sits between the figures and the view switch;
  - on a phone the switch and the legend's hint are hidden; the two pills stay;
  - both pills show `cursor: help`;
  - no new colour, size or token.

### 7. Docs

- **`docs/web-board.md`**, "Batch" (line 36, the paragraph CR-434 rewrites; this CR edits it as
  CR-434 leaves it):
  - name the mode, the legend pill and the mode switch in the title row, beside the batch's name;
  - replace "The legend pill stays above the tabs." with "The legend pill sits in the title row,
    on every tab.";
  - change the tab sentence, if needed, to say that the tabs are the first line above the central
    view.
- **Screenshots**: retake them with `just docs-screenshots`. Commit only the Batch pictures it
  changes: `docs/web-board/batch-pc.png`, `batch-phone.png`, `batch-gantt-pc.png`,
  `batch-cards-pc.png`. CR-434 retakes none and makes the Kanban the default tab, so the script's
  `batch` shot (no `t=`) then shows the Kanban: `batch-pc.png` and `batch-phone.png` carry
  CR-434's change too, and the PR says so. With the fixed clock and the fictional demo, the other
  pictures should not change. If one does, the PR names it.

## Overlaps (batch-30, this CR last)

This CR is built on the following as landed, and it rebases onto them:

- **CR-434** (board-batch-kanban, `4-batch/1-pending/434-board-batch-kanban`). This CR rebases on
  it: both edit `js/views/batch.js`, `css/views/batch.css` and `docs/web-board.md`'s "Batch"
  paragraph (line 36).
  - CR-434 adds the Kanban as the first tab of the same switch and its default (`TABS` in
    `js/core/router.js`, the initial `batchTab` in `js/core/store.js`), a
    `js/views/batch-kanban.js` panel, layout rules scoped `.batch .bkanban` in `batch.css`, and
    narrows `css/shell.css`'s `.main:has(.kanban)` to `.main:has(.view > .kanban)` so the batch
    page keeps scrolling.
  - Text conflicts are likely in `batch.js`'s `render` (its panel branch) and in `batch.css`.
    Resolve them by keeping CR-434's panel and rules whole and removing only the band and legend
    calls and rules this CR moves.
  - CR-434 keeps "The legend pill stays above the tabs"; this CR replaces it (section 7), on top of
    CR-434's rewrite of the tab and address sentences.
  - This CR keeps the switch whole and only moves it up. The legend in the title row covers the
    Kanban tab too.
  - If this CR touches `css/shell.css` (section 4, placement only), it leaves CR-434's
    `.main:has(.view > .kanban)` rule as it is.
- **CR-433** (board-batch-chip-stale, `4-batch/1-pending`). It changes the chip a batch CR's card
  shows (`js/views/batch-graph.js`, `js/ui/card.js`), DESIGN.md's "One card, one column, one chip"
  rule and line 36's priority-chip sentence in `docs/web-board.md` "Batch".
  - The code does not overlap.
  - The text overlaps in `docs/web-board.md`'s same paragraph and in DESIGN.md (another section).
  - The screenshots overlap.
- **CR-427** (board-running-batch-lane, `4-batch/1-pending`). It changes the Triage page
  (`js/triage/*`, `js/ui/column.js`, `css/components/column.css`, `css/views/triage.css`, the
  `triage.*` keys).
  - It also edits DESIGN.md (the "One card, one column, one chip" rule) and `docs/web-board.md`
    ("Triage" and line 163).
  - It retakes the Triage screenshots.
  - The overlap is text only, in other sections of the same two files, plus the screenshot run.
    This CR's `just docs-screenshots` runs on top of it.
- **CR-429** (board-fingerprint-cache, `4-batch/2-actives`). Its spec says "The web client
  (`clients/web/`): no change". There is no overlap.
- **CR-425, CR-426, CR-428, CR-430 to CR-432**: none touches the Batch page's layout.
  - CR-425 (factory-redefine) may change `steeringFactoryWord` or the factory words of the mode
    label. This CR moves that call as it is, whatever it returns once CR-425 has landed.

## Out of scope

- Any change to the breadcrumb row, the "+ New" button, the figures' content, the graph, the
  Gantt, the time cards, the PR column, the Kanban view itself, or other pages.
- A short form or an inline copy of the mode's sentence (compact-Q5: the tooltip alone).
- Making the mode switch active. It shows the mode and changes nothing, as today.
- New words, tokens, colours or components.
- The CR board pane (`hooks/`). Its screenshot rule does not apply.

## Evidence

Every check reads the shipped files from the repository at the head under test. No prepared text
stands in for a shipped file.

**Tests** (`skills/chantier/scripts/cli/tests/`, in-process, few; `just test` within its limit).

Add one parametrized test to `tests/test_board_design.py`, beside
`test_a_card_title_is_one_line_with_its_full_text_on_hover`. It reads the shipped files:

- `index.html`'s `.titlerow` holds `id="batch-mode"`;
- `js/views/batch-head.js` builds the mode pill (`mpill`, `aria-describedby="mtip"`, `id="mtip"`
  with `role="tooltip"` holding the mode's sentence), the legend pill (`lgpill`, `lgtip`) and the
  switch (`class="ms"`);
- `js/views/batch.js` no longer contains `class="mode"`, `lgrow` or `legend(`;
- `css/views/batch.css` has no `.batch .mode`, `.batch .ms`, `.batch .lg` or `.batch .tip` rule; it
  has the three show rules (`:hover`, `:focus`, `:focus-within`) for `.bmode .mpill .tip` and for
  `.bmode .lgpill .tip`; `.bmode .mpill` and `.bmode .lgpill` both declare `cursor: help`; its
  `max-width: 760px` block hides `.bmode .lghint` and `.bmode .ms`.

`test_sheets` and `test_components` pass unchanged on the edited sheet (tokens only, no component
restyled). `test_token_table` passes: no token is added.

**Pictures** (in the PR's Deliverables, captioned with the head's seven-character SHA):

- the Batch page before and after, at 1400 × 860 and at 375 × 812, from `just docs-screenshots` on
  the demo;
- on the after picture at 1400 × 860, the tab bar's top is higher by the two rows (about 90 px).
  The PR states the `.tabs` element's top in both runs (Playwright `bounding_box`, one-off, not
  shipped);
- at 1400 × 860, one picture with the mode pill's tip open: `#mtip` drawn above the figures'
  tiles, whole, not clipped; and the same for `#lgtip` (one picture each, or one with both open by
  hover and focus). The PR states, from the same one-off run, that each tip's box lies inside the
  viewport and that `document.elementFromPoint` at the centre of the tip's part over a tile
  returns the tip or a child of it;
- at 375 × 812: no horizontal scroll (`document.documentElement.scrollWidth <= innerWidth`); the
  mode pill and the legend pill on one line (their `bounding_box` tops equal); the hint and the
  switch not displayed; and the mode pill's tip, opened by focus, inside the viewport. The PR
  states each, from the same one-off run;
- a closed batch (`?b=` an older batch of the demo) and a batch with no CR yet, at desktop width.
  The first shows the mode and the legend in the title row. The second shows the mode only.

**Gates.** `just check`, `just eval-dry-run` (a change under the CLI's `src/`), and the pipeline's
`just scenario` green at the PR's head (AGENTS.md). No scenario step is added: the scenario drives
no browser.

## Open questions

None for the user (answer 3). Spec v1's two questions are settled: compact-Q4 and compact-Q5,
carried above. One point compact-Q5 leaves open is stated here with its options; A is built.

- **compact-Q6: the pills' cursor.** compact-Q5 gives the mode pill `cursor: help` "as the legend
  pill", but the shipped `.batch .lgpill` declares `cursor: default`.
  - **A (recommended, built):** both pills `cursor: help`, the legend pill's one declaration
    changing from `default`. Both open a tooltip, and the advisor meant one cursor for both.
  - B: both pills `cursor: default`, as the legend pill today.
  - C: the mode pill `cursor: help`, the legend pill left at `default`.
