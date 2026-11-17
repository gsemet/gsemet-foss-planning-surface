# Editing a MyST tab item shows only that item's source

Found after CR 148 (MyST cards, tabs and version directives, PR #156) merged. The real-window
scenario `mystBlocksWindow` fails on heavy CI run
https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40666806719 at the step
"editor holds the source of the tab item only". The scenario never ran locally (screen locked
overnight). Reproduce in a real window, then fix the block-to-source mapping for `{tab-item}` inside
`{tab-set}` (or the scenario, if its expectation is wrong).

## Status

Covered by PR https://github.com/gsemet/markdown-okf-schema-studio/pull/166 (branch `fix/tab-item-edit-source`, opened 2026-10-28 outside the CR factory). Archive this item when #166 merges.
