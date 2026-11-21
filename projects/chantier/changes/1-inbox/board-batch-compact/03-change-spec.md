# Batch page: the mode and the legend move into the title row

The board's Batch page loses its two full-width rows above the views. The mode band and the
"States and arrows" line move up into the page's title row, beside `Batch ‹ batch-30 ›`. The
four figures, the view switch and the graph start about 90 px higher. Nothing shown today is
removed, at desktop and at phone widths. This is a layout change of one page of the web client
only. No server, protocol, CLI or card changes.

## Goal, in the user's terms

"il faut reduire la perte de place verticalement" (2026-11-21, `intake/screenshot-2026-11-21.png`).
On batch-30's page, between the four figures and the graph, two rows hold little and take a lot:

- the mode band: "Stack · Foreman", its one-sentence explanation, and the Stack / Series /
  Parallel switch on the right;
- the legend line: the "States and arrows" pill and its "hover for the legend" hint.

The red arrows take both up into the top rows. The left arrow carries the band's label and
sentence and the legend line. The right arrow carries the switch to the right end of the title row.

## Decisions carried (02-answers.md)

| Answer | Decision | Where |
| --- | --- | --- |
| 1 (compact) | The mode band (mode and steering, its sentence, the Stack / Series / Parallel switch) and the legend line go up into the page's top rows. The figures, the view switch and the graph move up. This is the Chief of Staff's reading of the arrows, and the user may correct it. | What changes, 1 to 3 |
| 1 (restatement) | The explanation sentence is kept, as a tooltip or as a short form when it does not fit. Nothing is removed. | What changes, 2 |
| 1 (restatement) | The board-batch-kanban CR's toggle joins the existing Graph / Gantt / Time cards switch. This CR keeps that one switch as the first line above the views. | What changes, 3; Overlaps |
| 2 | Destination batch-30, queued last. | Overlaps |

**Reading of "top rows".** Both arrows end at the title row's height (`Batch ‹ batch-30 ›`, the
`.titlerow` of `index.html`). The breadcrumb row above it is the sticky bar shared by every page,
and it holds the "+ New" button. It does not change. Everything moves into the title row. The
user may correct this reading.

**The sentence.** It becomes the tooltip of the mode label. The tooltip uses the same pattern as
the legend: a focusable pill, a tip shown on hover and on focus, so a tap opens it on a phone. A
short form would need three new sentences in two languages, and the restatement allows the
tooltip. See the open question.

## What changes

All paths are under `skills/chantier/scripts/cli/src/chantier/clients/web/` unless named in
full. Read `DESIGN.md` first and keep it true (AGENTS.md).

### 1. The title row gets a batch slot

- **`index.html`**: in `.titlerow`, after `#stats`, add one element:
  `<div class="bmode" id="batch-mode" hidden></div>`.
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
- The order in the slot: the mode label, the legend pill with its hint, then the mode switch
  pushed to the right end of the row.

### 2. The mode label and its sentence

- The mode label keeps its words, `<mode> · <steering>` (`modeWords`, `steeringFactoryWord`). It
  becomes a pill with the colours of today's band: the `--accent-tint` fill and the `--accent`
  text, weight 500. No new token.
- The sentence (`words.text`, the `mode.<mode>.text` keys) moves into a tooltip on that pill:
  - the pill gets `tabindex="0"` and `aria-describedby="mtip"`;
  - the tip is `<span class="tip" id="mtip" role="tooltip">`;
  - it shows on hover and on focus, as the legend's `#lgtip` does.
- The Stack / Series / Parallel switch (`.ms`, the current mode `on`) keeps its look. It sits at
  the right end of the title row (`margin-left: auto` inside a `flex: 1` slot). On a phone it stays
  hidden, as `@media (max-width: 760px) .batch .ms { display: none; }` hides it today.
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
- The view switch (`tabBar`, "Graph / Gantt / Time cards", and the Kanban once board-batch-kanban
  has landed) is now the first line of `.gcol`, right under the figures.
- The file's head comment and the legend's comment ("It stays on top of every tab") follow. The
  legend now sits in the title row, so it stays visible on every tab.

### 4. Style

- **`css/views/batch.css`**: these rules move to the new slot's scope (`.bmode`) and keep their
  declarations, except for the changes listed after them:
  - `.batch .mode`, `.mb`, `.ms`, `.ms span`, `.ms span.on`;
  - `.lgrow`, `.lgpill`, `.lghint`, `.tip`, `.tip .k`, `.tip .an`, and the hover and focus rules.

  The changes:
  - `.bmode`: `display: flex; flex: 1; align-items: center; flex-wrap: wrap;` with a `space` token
    gap. It has no band fill, no padding and no bottom margin.
  - the mode pill: the legend pill's padding and radius (`--space-off-3` `--space-off-10`,
    `--radius-pill`), filled with `--accent-tint`, `--accent` text, and `position: relative` for
    its tip;
  - `.lgrow` loses its `margin-bottom`;
  - the phone rule that hides `.ms` follows to `.bmode .ms`. The phone rule `.batch .mode
    { flex-wrap: wrap; }` goes, because `.bmode` always wraps.
- The title row's baseline alignment (`css/shell.css`, `.titlerow { align-items: baseline; }`)
  stays. The slot's pills sit on the title's line. `css/shell.css` changes only if the slot needs
  `align-self` to centre on the title. Any such change is placement only.
- Every value is a token (DESIGN.md "Tokens"). No new token, colour or class outside `.bmode` and
  its children.

### 5. Desktop and phone

| Width | Title row after the change |
| --- | --- |
| Desktop (above `--phone-max`, 760 px) | `Batch ‹ batch-30 ›` · mode pill · legend pill and hint · … · switch at the right. On a narrow desktop the row wraps (`.titlerow` already has `flex-wrap: wrap`), the slot going to a second line whole. |
| Phone (760 px and below) | The breadcrumb is hidden, as today. `Batch`, then the navigator on its own line (`.batchnav { flex-basis: 100%; }`, as today), then a line with the mode pill and the legend pill and hint. The switch stays hidden, as today. The page has no horizontal scroll at 375 px. A tip opens on tap (focus) and stays within the screen's width (its `max-width: 300px`, anchored at the pill's left). |

### 6. DESIGN.md

- "A batch with no CR yet": "its four figures, the mode strip and the page's empty state" becomes
  "its four figures, the mode in the title row and the page's empty state".
- Add a short section, `## The Batch page's title row`. It says:
  - the mode (`<mode> · <steering>`, its sentence in a tooltip), the "States and arrows" legend and
    the Stack / Series / Parallel switch sit in the title row, built by `js/views/batch-head.js`;
  - no full-width band or legend line sits between the figures and the view switch;
  - the switch is hidden on a phone;
  - no new colour, size or token.

### 7. Docs

- **`docs/web-board.md`**, "Batch":
  - name the mode, the legend pill and the mode switch in the title row, beside the batch's name;
  - replace "The legend pill stays above the tabs." with "The legend pill sits in the title row,
    on every tab.";
  - change the tab sentence, if needed, to say that the tabs are the first line above the central
    view.
- **Screenshots**: retake them with `just docs-screenshots`. Commit only the Batch pictures it
  changes: `docs/web-board/batch-pc.png`, `batch-phone.png`, `batch-gantt-pc.png`,
  `batch-cards-pc.png`, and the Kanban tab's picture once board-batch-kanban ships one. With the
  fixed clock and the fictional demo, the other pictures should not change. If one does, the PR
  names it.

## Overlaps (batch-30, this CR last)

This CR is built on the following as landed, and it rebases onto them:

- **board-batch-kanban** (1-inbox, being specified). It adds the Kanban as a tab of the same switch
  (its restatement, and this CR's answer 1). It touches `js/views/batch.js` (`render`, `LOADERS`,
  the panel), `js/core/router.js` (`TABS`, the default), the `batch.tab_*` keys,
  `css/views/batch.css`, `docs/web-board.md` "Batch" and the Batch screenshots.
  - Text conflicts are likely in `batch.js`'s `render` and in `batch.css`.
  - This CR keeps that switch whole and only moves it up.
  - The legend in the title row covers the Kanban tab too.
  - If the Kanban view fills the page's height (as `css/shell.css`'s `.main:has(.kanban)` does for
    the backlog Kanban), the space saved goes to it.
- **board-batch-chip-stale** (1-inbox, being specified). It removes the priority chip from a batch
  CR's card (`js/views/batch-graph.js` line 68, `js/ui/card.js`), and maybe DESIGN.md's "One card,
  one column, one chip" rule and `docs/web-board.md` "Batch", line 36: "A CR's top row begins with
  ... a priority chip".
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
- **CR-429** (board-fingerprint-cache, `4-batch/1-pending`). Its spec says "The web client
  (`clients/web/`): no change". There is no overlap.
- **CR-425 to CR-428, CR-430 to CR-432**: none touches the Batch page's layout.
  - CR-425 (factory-redefine) may change `steeringFactoryWord` or the factory words of the mode
    label. This CR moves that call as it is, whatever it returns once CR-425 has landed.

## Out of scope

- Any change to the breadcrumb row, the "+ New" button, the figures' content, the graph, the
  Gantt, the time cards, the PR column, the Kanban view itself, or other pages.
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
- `js/views/batch-head.js` builds the mode pill with `role="tooltip"` holding the mode's sentence,
  the legend pill (`lgpill`, `lgtip`) and the switch (`class="ms"`);
- `js/views/batch.js` no longer contains `class="mode"`, `lgrow` or `legend(`;
- `css/views/batch.css` has no `.batch .mode` rule.

`test_sheets` and `test_components` pass unchanged on the edited sheet (tokens only, no component
restyled). `test_token_table` passes: no token is added.

**Pictures** (in the PR's Deliverables, captioned with the head's seven-character SHA):

- the Batch page before and after, at 1400 × 860 and at 375 × 812, from `just docs-screenshots` on
  the demo;
- on the after picture at 1400 × 860, the tab bar's top is higher by the two rows (about 90 px).
  The PR states the `.tabs` element's top in both runs (Playwright `bounding_box`, one-off, not
  shipped);
- at 375 × 812: no horizontal scroll (`document.documentElement.scrollWidth <= innerWidth`), and
  the mode pill's tip, opened by focus, inside the viewport. The PR states both, from the same
  one-off run;
- a closed batch (`?b=` an older batch of the demo) and a batch with no CR yet, at desktop width.
  The first shows the mode and the legend in the title row. The second shows the mode only.

**Gates.** `just check`, `just eval-dry-run` (a change under the CLI's `src/`), and the pipeline's
`just scenario` green at the PR's head (AGENTS.md). No scenario step is added: the scenario drives
no browser.

## Open questions

1. The mode's sentence is a tooltip on the "Stack · Foreman" pill at every width. It is not shown
   inline on a wide screen, and no short form is written. Does the user accept the tooltip alone,
   or want the sentence inline when the row has room?
2. Everything moves into the title row, and the breadcrumb row is untouched (the reading of the
   arrows above). Does the user confirm this, or want any part in the breadcrumb row?
