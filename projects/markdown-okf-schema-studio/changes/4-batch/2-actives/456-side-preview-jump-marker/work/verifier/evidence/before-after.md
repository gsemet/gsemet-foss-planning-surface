# Before and after, CR-456

Head (after): 7517dfd17699de1c122287a97082b04e756fed14. Base (before): origin/main 5a84db8b.

| Pair | Shows | How to reproduce | Status |
| --- | --- | --- | --- |
| `after-v13-jump-if-off-screen-light-900.png` | The side preview page (anchor button on) after `previewRevealLine` with `scroll: "if-off-screen"` for line 5: arrow in the left margin and light band on the wrapped paragraph, page still at the top. Made-up fixture only, no path on screen. | `npm run visual:render` then `uv run --no-sync --group docs python test/visual/capture.py --scenario lifecycle-sync/v13-line-marker-jump-if-off-screen-light-900` at 7517dfd | captured (looked at: arrow and band visible, no path or username) |
| before of the same scenario | not captured | The scenario and the `scroll` field do not exist at the base; at 1.11.0 the side preview marked nothing on a jump (CR-445 evidence `ta-defaults-06-t12-side-preview-jump.png`, not re-captured) | not captured: the scenario has no counterpart at the base |
| real search click, before and after in a real VS Code window | not captured | the real-window trial `test/integration/sidePreviewJump.test.ts` runs only in heavy CI (Linux); no screenshot of it is published and no real window is driven here | not captured |
