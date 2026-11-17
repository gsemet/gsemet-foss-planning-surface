# Report — window-switch-keys-block-selection

Status: **done** (2026-10-28, branch `change-requests/152-window-switch-keys-block-selection`, PR #164, merge commit 724841e6).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Test isolation fix for the keyboard block-selection scenario, plus a guard unit test | 724841e6 |

## Proof of completion

- Root cause: the paste-URL real-window test left edit mode on; the workspace remembers it, so the
  windowSwitchKeys scenario opened in edit mode, skipped its toggle click (the only page focus), and
  the arrow keys went to the workbench. Product code was not at fault.
- Before: heavy run 40662211644 (unchanged branch) integration failed. After: heavy run 40663643091
  integration passed; normal CI 40663636991 passed. Reviewer APPROVE in round 1.

## Open items

- A fresh preview gets no keyboard focus until clicked (Known issue SwRS BLOCK-004): backlog item
  `02-backlog/P3/preview-keyboard-focus-before-click/`.
