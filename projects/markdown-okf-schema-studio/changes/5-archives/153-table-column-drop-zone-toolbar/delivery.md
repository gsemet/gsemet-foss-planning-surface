# Report — table-column-drop-zone-toolbar

Status: **done** (2026-10-28, branch `change-requests/153-table-column-drop-zone-toolbar`,
PR [#167](https://github.com/gsemet/markdown-okf-schema-studio/pull/167), head `ff9f9c1e`, merged
as `d48739d7`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 (scope 1) | Root cause of the tableMoves column drop zone failure: the sixth toolbar button widened the floating toolbar over the table handle strip | folded into `ff9f9c1e` |
| T1 (scope 2) | Floating toolbar in five rows (Refresh/Edit/collapse · Anchor/Back/Next · Theme/Zoom · Width/TOC · Fold/Diff/Comments), 102 x 166 px; palette reserve re-measured for tall frames (`syncTallPaletteTop`) and uncapped at scroll 0 (`reservePaletteClearance`); StRS/SwRS toolbar requirements, docs, CHANGELOG, README image | `ff9f9c1e` |

## Proof of completion

- Scope 2: 2 rounds of 3 (round 1 FIX-REQUIRED, round 2 APPROVE). Local: `just check` exit 0
  (unit 3098, contracts 69); `just requirements-update` 0 changes; `okfreq validate --check-links`
  0 errors (1059 requirements); `npm run test:visual` 400 passed.
- CI: normal [40714661274](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40714661274)
  pass (both 360 px visual checks green). Heavy
  [40716533723](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40716533723):
  integration FAILED in `editToolbarCover` (figure "Edit figure" button covered by the row-5 Fold
  button), found after the merge; previous heavy on the four-row head passed integration.
- Screenshots: before/after, light and dark, on `change-requests/153-table-column-drop-zone-toolbar-assets` (tip `8ffd2331`).
- Owner approval of the toolbar requirement change logged in `requirements/tiers/log.md`.

## Open items

- Heavy integration regression on main: hotfix [CR 161](../161-edit-toolbar-cover-figure-button/intake/request.md)
  (move the link to `04-archives/` once it lands).
- Side-by-side button of the parked CR 147 moves into row 5:
  [02-backlog/P3/147-rich-diff-side-by-side](../../2-backlog/P3/147-rich-diff-side-by-side/intake/request.md).
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-153`, its branch, and the temporary
  worktree `/private/tmp/claude-502/cr153-driver/main-wt` (user's permission needed to delete).
