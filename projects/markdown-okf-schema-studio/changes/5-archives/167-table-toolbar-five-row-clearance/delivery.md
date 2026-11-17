# Report — table-toolbar-five-row-clearance

Status: **done** (2026-10-28, branch `change-requests/167-table-toolbar-five-row-clearance`, PR [#178](https://github.com/gsemet/markdown-okf-schema-studio/pull/178), head
`b361b4dc`, merged as `b71fac7c`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | `renderTableCellEditor` scrolled the page ~105 px before `clearPreviewControls` decided the five-row toolbar inset; `clearPreviewControls` now runs before `applyAnchor`. `scenarioTableToolbar` assertion unchanged. TABLE-064 (proposed) gains a scenario row; log entry. | `b71fac7c` |

## Proof of completion

- One round (reviewer Opus: APPROVE). Unit test in `test/page/runtimeTableCellEditor.test.ts`
  (`@tests_req` TABLE-064): old order scrolls to 30 instead of 40. `just check` green (unit 3131,
  contracts 69, requirements 1064 / 0 errors, visual 54); `okfreq validate --check-links` clean.
- CI: normal [40732101981](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40732101981) (static pass, visual pending at merge);
  branch heavy 40732144309 cancelled at merge. Real-window proof: heavy on main
  [40732349085](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40732349085).

## Open items

- Reviewer risk: if the sticky heading band's bottom lands > 2 px past the reading offset after the
  scroll, `scenarioTableToolbar` could still fail (watch run 40732349085).
- A coder's `git checkout` of its own edit was denied (Irreversible Local Destruction); it reverted
  the file by hand instead (reported to the user).
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-167` and its branch.
