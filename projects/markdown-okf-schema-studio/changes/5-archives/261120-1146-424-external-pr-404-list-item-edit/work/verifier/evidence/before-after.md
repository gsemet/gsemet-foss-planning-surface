# Before and after: a click on a list item, list items in the TOC, ordered-list numbering

- Before: origin/main `145f195377c605581a30582dc2dbb5edcca47ca3` (detached worktree, `npm ci`, `npm run visual:render`).
- After: pushed head `a6f0de15a2dc34fcb5128b0e91df04af6bef7ff6` (the CR's worktree, `npm run visual:render`).
- Every image is a Playwright capture of a rendered fixture page; each was opened and checked: no local path, no username (the pages show made-up depot and fleet text only).

## Pairs

| Pair | Before | After | What it shows |
| --- | --- | --- | --- |
| Item click, 460 px dark | `before-list-item-click-dark-460.png` | `after-list-item-click-dark-460.png` | A click on the "Criteria" item: before, the editor replaces the whole list (lines 7-9); after, it holds that item only (lines 8-10) after the first item, which stays shown. |
| Item hover, 900 px dark | `before-item-hover-dark-900.png` | `after-item-hover-dark-900.png` | Pointer on the nested item "Weight class assignment": before, the dashed outline is on its whole nested list; after, on that item (with its sub-list). |
| Ordered list item click, 900 px light | `before-ol-item-click-light-900.png` | `after-ol-item-click-light-900.png` | Before: the whole "Shift changes" list in one editor. After: item 2 alone in the editor, and the next items read 3. and 4. as in the source. |
| TOC, `preview.listItemsInToc` on, 900 px light | `before-toc-on-light-900.png` | `after-toc-on-light-900.png` | Before: 11 heading entries (the setting does not exist on main). After: 23 entries, the 12 top-level list items one level below the heading before them, cut to their first line. |
| TOC rail, setting on, 460 px light | `before-toc-on-light-460.png` | `after-toc-on-light-460.png` | The rail has 11 ticks in both: list items get no tick. |
| TOC, setting off (default), 900 px light | (same as the before above: 11 entries) | `after-toc-off-light-900.png` | With the setting off the TOC is unchanged: the same 11 headings. |

Measured in the same runs: `after toc entries 23 ticks 11` (setting on, 900 and 460), `after toc entries 11 ticks 11` (off); `before toc entries 11 ticks 11`. Ordered list: after, the list markers Chromium draws (accessibility tree `ListMarker`) are `1. 3. 4.` while item 2 is edited, the editor holds `2. Depot reports vehicle availability.`; before, the editor holds all four lines.

## How to reproduce

- Item click and hover: `uv run --no-sync --group docs python test/visual/capture.py --scenario edit-list-narrow --scenario edit-affordances-hover-and-open --workers 2` in each worktree after `npm run visual:render`; the PNGs are under `out/reports/e2e/screenshots/visual/block-editing/` (`v12-...-dark-460.png`, `v06-hover-outline-then-editor-dark-900--hover.png`).
- TOC and ordered list: `work/verifier/shots.py <worktree> <before|after> <evidence dir> <1 if the setting exists>` (Playwright Chromium on `out/reports/visual/pages/05-long-chapter--light--sticky-3--default.html`; the page's boot context gets `"toc":true` in `initialViewPreferences` and a top-level `"listItemsInToc":true`; the ordered list is the "Shift changes" list, edit mode on, click on "Depot reports vehicle availability.").

## Not captured

- The real-window checks of the plan other than the hover: the caret, Right/Left/Enter, the arrows, task lists and the move chord ran in the jsdom page and session tests only, and nothing ran on macOS (no macOS job), so the Cmd+Alt chord in an item editor is unproved in a real macOS window.
- The TOC's cost on a document with thousands of list items: not measurable here.
- Light-theme pairs of the item click and hover: the scenarios exist in dark only; the TOC and ordered-list pairs are light.
- The ordered-list numbering in Firefox and Safari: only Chromium (the webview's engine) is checked.
