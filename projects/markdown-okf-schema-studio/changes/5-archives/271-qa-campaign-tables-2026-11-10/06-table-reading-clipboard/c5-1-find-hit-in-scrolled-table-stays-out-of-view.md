# Find does not scroll a table sideways to its hit

Severity Medium · Reproduced · Verdict Gap · Requirements: none found (SwRS-MDOKFSTUDIO-TOOLBAR-010 paints and walks matches, says nothing on horizontal reveal) · Area Tables · Find · Side preview · c5-1 · Replay `scenarios/271-c5-1-find-hit-in-scrolled-table-stays-out-of-view.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../evidence/c5-1-currently.jpg) | ![expected](../evidence/c5-1-expected.jpg) |
| Find reports "1 of 1" for `needle`, but the table stays scrolled to the Owner column (scrollLeft 864); the hit text is at x -665..-622 in a 393 px pane, nothing is highlighted on screen. | Same search with the table at scrollLeft 0: the hit is highlighted in view. Expected: Enter on a hit brings it into view in both directions (source: the find bar already scrolls vertically to the current hit; browser and editor find do the same). |

## Why this is wrong

The author scrolled a wide table to the right, pressed Meta+f, typed a word that exists only in an earlier column and pressed Enter. The bar says "1 of 1" and the page appears not to react: the hit is out of sight to the left, so they cannot tell whether the search worked. The find bar already scrolls vertically to centre the hit, so horizontal reveal inside a table that scrolls sideways is the same promise left half done. Edit mode keeps whole words, so tables with a long cell scroll sideways often there.

## Steps to reproduce

1. Fixture `synth/c5-reading.md`, side preview, edit mode on.
2. Click the `carol` cell (table scrolls to the Owner column), Escape.
3. Meta+f, type `needle`, Enter.
4. The match is counted but the cell is off screen to the left.

## Impact

Find inside wide tables looks broken; the author scrolls by hand to look for the hit.

## Where it comes from

`src/page/modules/findBar.ts` `scrollToCurrent` (around line 247) tests only `rect.top`/`rect.bottom` against the viewport height; it never checks `rect.left`/`rect.right`, so a hit that is vertically visible is not scrolled into view.

## Suggested direction

Also call `scrollIntoView({ inline: "nearest" })` (or scroll the table wrapper) when the range is outside the horizontal viewport.

Uncheck to disagree: [x]

## Test to add

Page test of `scrollToCurrent`: a range with rect.left < 0 triggers a scroll; or promote the replay.

Uncheck to disagree: [x]

## Requirement to write or change

Amend TOOLBAR-010: "the current match is brought into view horizontally as well as vertically".

Uncheck to disagree: [x]

## Done when

- [ ] After Enter on a hit inside a sideways-scrolled table, the hit text lies inside the preview.
- [ ] The replay scenario passes.
