no new captures by the Verifier; the pairs are those posted in the PR #364 Impacts section (4 images, all HTTP 200).

| Pair | Shows | Reproduce |
| --- | --- | --- |
| v33-before-light / v33-after-light | click on `qa` in the quoted table, light 900: raw block editor before, cell editor and table bar after | `npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --group table-editing` (scenario table-editing/v33-cell-editor-in-quote-light-900; before: same on a detached worktree of 0dc8aa5f with the scenario files copied in) |
| v34-before-dark / v34-after-dark | click in the GFM Note table, dark 900, same contrast | same command, scenario v34-cell-editor-in-note-dark-900 |

The after scenarios passed locally at 9c550983 (their checks assert the cell editor and the table bar).
