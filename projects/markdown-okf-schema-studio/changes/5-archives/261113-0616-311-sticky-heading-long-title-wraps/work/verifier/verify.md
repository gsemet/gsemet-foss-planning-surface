# Verify CR-311

Head: 352077df62fcf329358c8db3e9e3487c23ce3a91 (worktree batch-02-CR-311, clean)

1. `just check` -> exit 0 (all unit/contract/Python tests passed).
2. `just requirements-lint` -> exit 0 (only pre-existing W2 broken cross-link warnings in PALETTE SwRS).
3. `fnm exec -- npm run visual:render` -> exit 0; `capture.py --group toolbar-navigation` -> exit 0,
   `{"status": "passed", "scenario_count": 44}`; `passed: toolbar-navigation/v05-sticky-long-path-ellipsis-dark-460`,
   `passed: toolbar-navigation/v44-sticky-long-title-zoom-160-cream-900` (these scenarios assert one rendered line
   per level, ellipsis, cut text, section start not covered).
4. Screenshots: v44 after shows a one-line band ending in "verificati..." with the heading continuing under it;
   v05 base wrapped (before) vs ellipsis (after). See evidence/before-after.md.

Note: at base origin/main, the same group run had v31-mark-editor-selection-light-900 fail (unrelated, not in the
CR head run, where it passed).

VERIFIED
