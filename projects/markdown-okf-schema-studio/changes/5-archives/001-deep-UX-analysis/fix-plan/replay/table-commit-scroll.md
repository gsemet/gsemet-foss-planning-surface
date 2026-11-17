# Table cell commit: does the table jump?

Measured on 2026-10-13 at HEAD `50cd143` (extension tree clean), session `r4` on clone `ws-r2`.
VS Code window 1440×900; the side preview is 393×801 px, with a sticky band of about 38 px at the
top. Edit mode was turned on with the toolbar button. Every action was a real mouse or keyboard
event sent through CDP.

## Answer

When the user clicks a cell, types, and commits with Enter, Tab or a click outside the cell, the
table does not move: it stays within 1 px of where it was before the click (8 runs, 2 documents).

The jump in the r2 shot and in test note 33 comes from the **End** key, pressed after the click
and before typing. When the caret is already at the end of the cell, which is where the editor
places it, End scrolls the whole preview to the bottom of the document. The first typed character
then scrolls the caret back into view at the top edge of the viewport, so the edited row ends up
under the sticky band. The commit and the save render keep the table at that displaced position.

## Method

`output/qa/markdown-studio-claude/runs/r4/work/measure.mjs` does the following steps.

1. Scrolls with the mouse wheel until the table's top is at about 40 % of the viewport.
2. Installs a sampler that runs on every animation frame in the webview host. It records the
   table's `getBoundingClientRect().top` and `scrollY`, and survives the swap of the content
   iframe.
3. Wraps `scrollTo`, `scrollBy`, `scroll`, `scrollIntoView`, the `scrollTop` setter and `focus`
   to record a call stack for each programmatic scroll.
4. Clicks a body cell (row 2), types `xyz` one key at a time, then commits.

Each run checked that the buffer change was a single line (`spy --diff`). The fixture was
reverted between runs.

- Case A: `fixtures-visual/05-long-chapter.md` (scroll height about 6000 px), with a narrow
  4-column table. The clicked cell is `planner decisions`.
- Case B: `fixtures-visual/04-code-and-tables.md`, with the wide 16-column table from the r2 shot.
  The clicked cell is `North` in row `nw-02`.

## Measurements

Each cell gives the table's `top` in px, with `scrollY` in parentheses. Step (1) is taken 580 ms
after the click, (2) after the third character, (3) 80 ms after the commit and (4) 2.5 s after the
commit.

| Case | Commit | (0) before click | (1) after click | (2) after typing | (3) at commit | (4) settled | Drift (4)−(0) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A narrow | Enter, run 1 | 320 (2475) | 320.3 (2565) | 320.3 (2565) | 320.3 (2497) | 320 (2475) | 0 |
| A narrow | Enter, run 2 | 320 (2475) | 320.3 (2565) | 320.3 (2565) | **−1406.7 (4224)**, transient | 320 (2475) | 0 |
| A narrow | Enter, run 3 | 321 (2474) | 321.3 (2564) | 321.3 (2564) | 321 (2474) | 321 (2474) | 0 |
| A narrow | Enter, run 4 | 321 (2474) | 321.3 (2564) | 321.3 (2564) | 321.3 (2496) | 321 (2474) | 0 |
| A narrow | Tab | 320 (2475) | 320.3 (2565) | 320.3 (2565) | 320.3 (2565) | 320.8 (2460) | +0.8 |
| A narrow | blur (click in left margin) | 321 (2474) | 321.3 (2564) | 321.3 (2564) | 320.3 (2497) | 321 (2474) | 0 |
| **A narrow** | **End, type, Enter** | 321 (2474) | 321.3 (2564) | **−121.7 (3007)**, after End: −2406.7 (5292) | −122 (2917) | **−122 (2917)** | **−443** |
| B wide | Enter | 319.9 (856) | 319.9 (945) | 319.9 (945) | 319.9 (856) | 319.9 (856) | 0 |
| B wide | Tab | 319.9 (856) | 319.9 (945) | 319.9 (945) | 319.9 (945) | 319.9 (945) | 0 |
| B wide | blur (click in left margin) | 319.9 (856) | 319.9 (945) | 319.9 (945) | 319.9 (856) | 319.9 (856) | 0 |
| **B wide** | **End, type, Enter** | 319.9 (856) | 319.9 (945) | **−100.1 (1365)**, after End: −1806.1 (3071) | −100.1 (1276) | **−100.1 (1276)** | **−420** |

The sampler also recorded short movements between the sampled steps.

- **At every click:** for 2 frames (about 33 ms) the table moves 68 px down while the table
  toolbar is inserted above it. `applyAnchor` then moves `scrollY` by 90 px and puts the table
  back. This happens in all runs and is not visible as a jump in the screenshots.
- **End key:** a smooth scroll of about 130 ms (8 frames) to the bottom of the document. The page
  calls no scroll API during it; the only calls recorded in these runs are the 2 `scrollTo`
  calls and the `focus({preventScroll:true})` call at the click.
- **First typed character after End:** a single jump that brings the caret back into view at the
  top edge of the viewport. The page calls no scroll API here either.
- **Transient jumps during the commit render, each seen once.** Each commit swaps the content
  iframe 2–3 times. In some of the new frames the scroll position is briefly wrong, then
  corrected:
  - A, Enter, run 2: −1727 px for 50–100 ms;
  - A, Tab: −104 px for 26 ms;
  - B, Enter: `scrollTo({top: 0})` from `applyAnchor`, on the source-line anchor path, in a new
    frame, for 64 ms.

  These come from DOM samples only; no screenshot confirms them.

## Screenshots

Case B, End then type then Enter, before the commit. The toolbar is above the table and the `nw-02`
cell is selected, with the table at 320 px:

![Case B after click](table-commit-scroll/caseB-End-1-after-click.jpg)

Case B, the same run, 2.5 s after Enter. The table is pushed up under the sticky band and the
edited row is hidden. This matches the r2 shot `UX-12-wide-table.jpg`:

![Case B settled after End](table-commit-scroll/caseB-End-4-settled.jpg)

Case A, Enter without End, settled. The table and the edited cell (`planner decisionsxyz`) are at
their original place:

![Case A settled](table-commit-scroll/caseA-enter-4-settled.jpg)

## Cause

The cause is the browser's default handling of the End key, which the page does not intercept.

- `src/webview/scrollSync.ts:2231–2246`: the `keydown` listener of
  the table cell `<textarea rows=1>` in `renderTableCellEditor` handles undo, Tab, block
  navigation (`navigateBlockEdit`), Escape and Enter. It does not handle End or Home, and nothing
  in `src/webview/*.ts` refers to `"End"` or `"Home"`.
- `focusTextControlAtLastContent` already places the caret at the end of the cell. End therefore
  cannot move the caret, and Chromium passes the key to the document as a "scroll to end", which
  is a smooth scroll to the bottom of the page.
- The first typed character makes Chromium scroll the caret back into view. The scroll is the
  smallest possible, so the cell ends up at the top edge of the viewport, under the sticky band.
- `scrollSync.ts:324` (`applyAnchor`) and `scrollSync.ts:318` (`programmaticScroll`) then work as
  designed: they keep the edited cell where it was when the commit started, which is the displaced
  position.
- No `scrollIntoView`, `scrollTo` or `scrollBy` in the webview code causes the jump. Neither
  `revealTableToolbar` (`scrollSync.ts:2115`) nor `scrollIntoView` (lines 2788 and 3012) was called
  in any run.

## Introduced by the plan or not

The cause predates the plan. At `aeb9c03`, the cell editor is the same `<textarea rows=1>`, and its
`keydown` listener (old `scrollSync.ts:1648–1657`) also handles only block navigation, Escape and
Enter, with no End or Home. No plan commit added the End scroll. Neither T17 `fa73a7f` (Tab and
focus loss), T18 `b2c5476` (toolbar above the table), T19 `21106e0` (one-line cells) nor T32
`d596de8` scrolls on End.

T32 `d596de8` (UX-11) only keeps the table at the displaced position through the commit and the
save render, which is its purpose. How the commit behaved before the plan after an End scroll was
not measured, because that would need a rebuild of `aeb9c03`.

Two places pressed End before typing, and so produced the evidence:
- the product test `test/integration/realInput.test.ts:884`, which records test note 33;
- the skill scenario `SK/scenarios/table-cell-edit.json`, which the r2 replay probably used.

The test's comment at lines 886–888 says that "typing in a cell of a long document pages it by up
to ~1700 px". The paging comes from the End key, not from typing.

## User impact

An author who clicks a table cell and types, then commits with Enter, Tab or a click elsewhere,
sees the table stay where it was clicked. In 8 runs, on a narrow and a wide table, the table
stayed within 1 px. The only exception is a possible flash of a few frames while the save render
swaps the iframe, seen once per commit key in DOM samples. An author who presses End first, out
of habit to reach the end of the text, sees the whole preview scroll to the bottom of the
document. The table comes back on the first keystroke, but with the edited row hidden under the
sticky header (420–443 px higher than before), and it stays there after the commit. Home at the
start of a cell probably does the same towards the top of the document; this was not tested.
