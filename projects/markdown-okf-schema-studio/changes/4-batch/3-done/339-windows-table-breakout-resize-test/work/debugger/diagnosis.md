# Diagnosis CR-339: tableBreakout "measures again on a real resize" red on Windows

Reproduce: `node scripts/node-test.mjs unit "out/test/page/tableBreakout.test.js"` (after `npm ci`, `npx tsc -p .`).

## Cause: a test assumption that depends on the font, not a product bug, not timing

The test opens the ten-column tick matrix at a 1100 px pane, opens the editor of cell 0, shrinks the viewport to 760 and asserts
`narrower.width < open.width`. It silently needs the table's width at 1100 to be larger than the room at 760 (760 - gutters = 727.4 px).
That width is the table's min-content, which depends on the font:

- Windows (Segoe UI, from `--sphinx-preview-font`): 705 px at 1100. At 760 with the editor open the table is 727 px, the room cap. 705 < 727: red.
- Probe with other fonts set on the page: Verdana 797, Tahoma 739 (both > 727, would pass), Arial 722, Consolas 720 (both red like Segoe).
  Linux has no Segoe UI and falls back to a wider system-ui font (not run here; no Linux), so it very probably passes there.

Not timing: 4 consecutive layout passes with 300 ms waits after the resize give the same 727 (probe log values in this session).
Not viewport/scrollbar: iw = clientWidth = 760 in both states.

Why 727 and not 705 at 760 (product side, worth knowing, not a bug fix target):
without an editor the table stays 705 at 760 (probe: edit false, 1100: 705, 760: 705). With the cell editor open its
min width (the 300 px minimum of the selected cell) makes the re-measured natural width reach the room cap, so the table
fills the pane (727 <= 760). `widthMode.ts` measureWide releases the held verdict on a geometry change and measures again
(correct and intended: the test title). The re-measure does happen; the result is just not smaller than 705 on this font.

## Fix (test only): test/page/tableBreakout.test.ts, test "Auto measures a table again on a real resize while a cell is edited" (~line 404)

Shrink to a pane narrower than the table's min-content on every font: change `setViewportSize({ width: 760, ...})` to
`{ width: 600, ... }` and the second assertion `narrower.width <= 760` to `<= 600`. Probed (open -> after, wide stays true):

    viewport 600 : Segoe 705->568, Verdana 797->568, Arial 722->568, Consolas 720->568
    (640: ->608 and 700: ->668 also pass on all four)

Why the old test was wrong: it chose 760 as "a narrower pane" while the real condition is "narrower than the table's natural
width", which varies with font (705 to 797 px here). 600 is below every measured natural width, so it proves the breakout
follows the pane without depending on the font. Optionally pass the intended invariant by also asserting `narrower.width === 568`-like
value? No: keep `<` and `<= 600`.

Probe script: generated from out/test/page/tableBreakout.test.js (copy edited, deleted after use; out/ is git-ignored). No worktree
source file changed.
