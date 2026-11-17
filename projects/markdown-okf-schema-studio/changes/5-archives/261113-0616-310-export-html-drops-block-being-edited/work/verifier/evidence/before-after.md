# Before / after, CR 310 (head 055efc8a, base cb968299)

Pair 1, page-level tests. before: `base-tests.txt`, after: `head-tests.txt`. Shows: on the base, the cell, front matter value and front matter key cases fail (24 pass, 3 fail); at the head all 30 pass (paragraph, card, list-table cases pass on both).
Reproduce: `npm run compile && node --test --import ./scripts/register-myst-patches.mjs out/test/page/exportWhileEditing.test.js out/test/core/export/htmlExport.test.js` (base: test files copied from the head).

Pair 2, visual v44. before: `before-export.png`, `before-export.html`, `base-visual.txt` (fails: edited cell text hidden, hidden wrapper left); after: `after-export.png`, `after-export.html`, `head-visual.txt` (passed).
Reproduce: `npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --scenario toolbar-navigation/v44-export-html-edited-cell-light-900` (base: test/visual files copied from the head).
Not captured: the real VS Code window manual steps (need a window; covered by CI integration, green).
