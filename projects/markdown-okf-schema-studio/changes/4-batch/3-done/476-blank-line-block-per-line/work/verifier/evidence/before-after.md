# Before and after, CR-476

Before: base origin/main dcc84def8b331e323fb3b91ef89941f9ca7dbb13 (detached worktree, removed at the end).
After: head 58c9f1e679e8b89e2c0da54a16edfefb1ea3c23b.
Reproduce: `npm run visual:render`, then `uv run --no-sync --group docs python test/visual/capture.py --scenario <id>` (ids below); PNGs land in out/reports/e2e/screenshots/visual/.

| Pair | Scenario | Shows |
| --- | --- | --- |
| before-v44 / after-v44 | block-editing/v44-blank-lines-block-light-900 (bar) | text, three blank lines, text: before one "Blank lines (3)" block; after two "Blank line" blocks (first line is the hidden separator) |
| before-v45 / after-v45 | block-editing/v45-blank-lines-block-selected-dark-900 (selected) | the selected block, dark |
| before-six / after-v54 | v54-blank-lines-six-light-900 (bar); the before runs fixture 96-blank-lines-six.md on the base through the base's own v44 scenario, with the base harness patched only to save the screenshot first (patch in the throwaway worktree, not kept) | "Text." then six blank lines: before one "Blank lines (6)" block, after six stacked "Blank line" blocks |
| before-v86 / after-v86, after-v87 | layout-width/v86-empty-start-writing-hint-light-700 (v87 is dark) | one-newline document: before only Start writing; after one "Blank line" block at the top then Start writing 40 px below |

Every capture shows made-up content only (fixtures); no path, username or home folder appears (looked at each image opened).
The toolbar overlaps the right end of the single top block in the one-newline captures (toolbar floats over content; the block is empty).
