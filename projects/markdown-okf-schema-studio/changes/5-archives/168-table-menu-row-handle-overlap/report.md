# Report — table-menu-row-handle-overlap

Status: **done** (2026-10-28, branch `change-requests/168-table-menu-row-handle-overlap`, PR [#181](https://github.com/gsemet/markdown-okf-schema-studio/pull/181), head
`3e148886`, merged as `78a625a9` + `eca17c42`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 r1–r2 | The table menu is painted above the row and column handles (position relative, z-index 3), so "Delete selected column" receives the press instead of the row-1 drag handle | `78a625a9` |
| T1 r3 | Real-input `scenarioTableToolbar` r06 tightened (Chief of Staff review): position exactly `relative`, top/left/bottom/right `auto` or `0px`, z-index `3` (had become `static || relative`) | `eca17c42` |

## Proof of completion

- 3 rounds of 3 (FIX-REQUIRED, APPROVE, APPROVE); reviewer Opus. Cause: the menu was static while
  the handle layer is absolutely positioned at z-index 2, so a handle over a menu button won the hit
  test (a real user hits it too). Tests failing on the old code: a unit test and a headless hit-test
  (`test/visual/capture_table_menu.py`). `just check` (3132 unit); okfreq 1064 / 0 errors; 75
  headless scenarios. TABLE-064 (proposed) extended.
- Before/after: `change-requests/168-table-menu-row-handle-overlap-assets` (`shots/table-menu-*.png`).
- CI: normal [40741405896](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40741405896) pass on 3e148886; branch heavy 40743330796 cancelled at
  merge. Real-window proof: the 1.0.0 heavy gate on main
  [40743462032](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40743462032).

## Open items

- Heavy proof: run 40743462032. The exact overlap rects at 1400x900 are unproven; if "Delete selected
  column" still fails there, the interceptor is not z-order.
- `test/visual/capture_edit_checks.py:1115` (headless) still accepts `static` or `relative`: backlog
  [P2/tighten-headless-table-menu-position-check](../../2-backlog/P2/tighten-headless-table-menu-position-check/01-intent.md); the
  reviewer recommends `relative` only (same tightening as r06).
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-168` and its branch.
