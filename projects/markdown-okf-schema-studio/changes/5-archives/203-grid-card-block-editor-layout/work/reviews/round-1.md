# CR 203 — Inspector review, round 1/3

Verdict: **APPROVED** (no blocking code finding; finding 1 is a required delivery action for the
driver, not a code change).

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-203` (uncommitted).

## What I checked

- Full diff and the 5 untracked files (CSS part, SwRS-BLOCK-257, unit test, visual scenarios,
  fixture 73).
- The 8 screenshots in `/private/tmp/claude-502/cr203-driver/shots/` (before/after, body/title,
  cream/dark).
- `just check`: exit 0. Unit 3262/3262 pass, contracts 71/71, `okfreq lint --check
  --check-links` and `update-coverage --check` clean (only the old W2 cross-link warnings), check-limits,
  check-markers, check-exports pass. The worktree is unchanged after the run.
- I did not re-run the 4 visual scenarios: the after shots and the assertions agree (see below).

## Owner decision vs result

| Owner decision | Result |
|---|---|
| Card gets a minimum width and pushes neighbours, like the table-cell editor | Met. Card 2 goes from about 241 to 337 CSS px; cards 1 and 3 shrink to about 194 px. They are not overlapped. |
| Palette above the text box, may be wider than the card | Met. The palette is in the flow (`position: relative`), the text box sits under it, and the palette spills about 24 px past the card. |
| Palette max height + vertical scroll | Met by the CSS (`max-height: min(9em, 30vh)`, `overflow-y: auto` unless a popover is open). At 900 px the 4 rows fit, so the scroll does not show in the shots. |
| Text box min width so a title editor is readable | The layout part is met: the title editor shows a 1-line source at full card width, readable in both themes. **The source it shows is the wrong one** (finding 1). |

Before shots: the 7-row palette covers the text box. In the body shots only the Done and Cancel
buttons and a clipped hint show. In the title shots no text is visible. After shots: the text box is
fully visible under a 4-row palette, in cream and dark, for both body and title. The shots really
show the layout fix.

Consistency with the table-cell editor: the table cell gets its width from a `min-width` on the
edited cell, and the table layout grows the column (SwRS-TABLE-006, 300 px). The grid change does
the same: `min-width: 24em` on the edited item. `--myst-grid-track-min: auto` turns the fixed tracks
into `minmax(auto, 1fr)`, so the track takes the item's minimum into account. It is CSS only, needs
no runtime state and is reset when the editor leaves the DOM. That is consistent and minimal.

Scope of the selectors: the new rules carry an ID, so they override the sticky-palette rules
(`data-sphinx-palette-top`, first-block, short-pane). They only apply inside `.myst-grid-card`
(palette and text box) or `.myst-grid-item:has(.sphinx-preview-block-editor)` (width). The table-cell
editor uses `.sphinx-preview-table-cell-editor` and does not match. Editors outside cards keep the
sticky palette. All palette popovers use `.sphinx-preview-edit-palette-menu`, so the
`:not(:has(> menu))` guard keeps popovers from being clipped by `overflow-y: auto`. `100cqw`
resolves against `.myst-grid` (`container-type: inline-size`).

## Findings

### 1. Card title editor opens the wrong source (required delivery action, not a code fix)

Clicking "2. Status projection" opens the editor on line 1 of the document. In the fixture that is
`# Grid card editing` ("Line 1" in `after-title-*.png`). The cause is in `buildCard`
(`src/core/render/mystGridToctree.ts`, around lines 236-241): the title is rendered through
`parse(title)`. "2. Status projection" parses as an ordered list, so the title is rendered as a
list item with a bullet (the "2." is lost, as all 8 shots show), and that list item carries a
`data-line` relative to the title snippet. In the issue's own document (no H1), line 1 is the
`::::{grid} 1 2 3 3` opener; I inferred this and did not run it. If the writer edits and presses
Done, the edit lands on a line that is not the title.

- **Not a direct consequence of this CR.** It predates the change. Before, the text box was hidden
  under the palette, so nobody could see it; this CR makes it visible. I do not ask for a fix here.
- **It does weaken "closes #226".** #226 expects "the title source is readable while editing". The
  layout half is fixed, but what is readable is not the title source.
- **Required before the PR is opened:**
  - file a follow-up issue/backlog item: card title rendered via `parse()` turns "N. Title" into a
    list, loses the number and opens the editor on a wrong line;
  - add a "Known issue" line to the PR body with the link;
  - either keep #226 open (use "Refs #226") or close it with a comment that points to the
    follow-up. The owner or driver decides; the PR body must not imply that title editing is
    correct.
- The v25/v26 scenarios assert only the layout and would still pass after a future fix. Good: they
  do not lock in the wrong source.

### 2. A 24em minimum in an `auto` grid can overlap a neighbour (non-blocking)

The `auto` column count keeps `repeat(auto-fit, minmax(14em, 1fr))`. Its track minimum is fixed, so
it ignores the item's `min-width: 24em`. An item edited in a narrow `auto` grid then overflows its
track into the next card instead of pushing it. I reasoned this from the grid sizing rules and did
not run it. SwRS-257's boundary scenario says the auto grid "keeps its column rules", which is true,
but the item min-width still applies there. Suggestion, in this CR or a follow-up: limit the item
`min-width` to fixed-count rows (`.myst-grid-row:not(.myst-grid-*-auto)`), or cap it with
`min(24em, 100cqw)`. The same `min()` cap would also avoid horizontal overflow in a 1-column grid on
a pane narrower than about 24em plus the card padding.

### 3. The custom property inherits into nested grids (non-blocking, nit)

`--myst-grid-track-min: auto` is set on the outer row and inherited by every nested
`.myst-grid-row` inside it. The nested grids of the edited row then also use `minmax(auto, 1fr)`.
That is harmless in practice (min-content of normal cards is small), but `@property` with
`inherits: false`, or setting `--myst-grid-track-min: 0px` on `.myst-grid-row` by default, would
keep the effect local. Optional.

### 4. The palette covers the start of the neighbour card's text (observation, non-blocking)

In `after-body-*.png` the palette is wider than the card and covers the first characters of card
3's body ("Approval becomes a" shows as "pproval…"). This is what the owner allowed ("may be wider
than the card"), and the palette is a transient bar. I mention it so the PR's screenshots are not a
surprise.

### 5. SwRS-BLOCK-257 wording (nit)

"is at most 9em high (or 30% of the viewport)": the CSS is `min(9em, 30vh)`, so the limit is the
smaller of the two. Suggest "at most 9em high and at most 30% of the viewport height". The boundary
clause "when the editor closes the cards return to their column widths" has no test. It is true by
construction (`:has`), so this is fine, but the Verification notes could say so.

## Rule checks

- Locked StRS: none of CORE-001, GFM-002, MYST-001, DIAG-001/006, REVIEW-001/003/012/015,
  BLOCK-003/025, PALETTE-015, TABLE-001/012, LAYOUT-001/003 is touched. The only StRS edit is the
  generated `derived_by` and links lines in StRS-BLOCK-001 (`req_lifecycle: proposed`, not locked).
  `update-coverage --check` and lint report 0 changes, so the edit is the generated output.
- The new SwRS is `req_lifecycle: proposed`. `status: stable` matches other proposed SwRS. It
  derives from BLOCK-001, relates to PALETTE-021 and TABLE-006, and its implemented/tested files
  match the markers (`@implements_req` in `gridCardEditStyles.ts` and on `gridColumnCss`,
  `@tests_req` in the unit test and visual scenarios).
- Tests fail on the old code: the unit tests look for rules and a `minmax(var(--myst-grid-track-min…`
  track that do not exist before the change. The visual assertions (card ≥ 320 px, palette bottom ≤
  text box top) fail on the before layout: the card is about 241 px and the palette is over the text
  box, as the before shots show. No existing assertion was changed or weakened. No existing test
  asserted `minmax(0, 1fr)`.
- e2eGroups 404 → 408: legitimate. There are exactly 4 new scenario ids (v23-v26), all with lock
  sentences in `scenarioIds.ts`, and the message follows the established pattern.
- File sizes: the new files are small (51 and 42 lines) and check-limits passes.
  `scenarioDefinitions1.ts` only gains an import and a spread.
- CHANGELOG and log entries are present and in English.
