# Report — show-incoming-diff

Status: **done** (feature session, 2026-10-16, branch `dev/gsemet`), pending the idle e2e re-run.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T16 | Blocks changed since the last commit (unsaved edits included) get a green left bar, through VS Code's built-in Git extension (optional, no git spawn); untracked files and folders without Git show nothing; content from `{include}` is not marked; setting `preview.showIncomingChanges` | `7481493` |
| T17 | Diff button at the end of toolbar row 2 shows or hides the marks, remembered per workspace, survives a reload, hidden when the setting is off | `93f6a81` |

## Proof of completion

- T16: line-diff, Git-baseline (fake API), webview, message, package-contract and integration tests;
  review APPROVE in round 2 (included blocks no longer marked).
- T17: webview, shell-key, visual and reload tests; review APPROVE.
- Phase 3 e2e (2026-10-16, `4c5c869`, clean tree): unit 952, contract 2, security 23, visual 154
  checks / 149 images green; integration **not green**: one scroll scenario (solo-block-independent,
  no scroll feedback). A control run of the same e2e on `5406410` (before T19) also failed
  (checkbox undo timeout). All failures this day were timeouts in different suites while the machine
  was in active use; direct runs passed. **Pending: re-run the e2e on an idle machine** (tracked in
  followups.md; also covered by the final `just preflight`).

## Open items

- The positive diff path is unit-tested with a fake Git API only (no real-repository integration test).
- Deleted lines are not shown (D19, v1).
- With the setting off, the Diff button shows until the first host message.

## Addendum (2026-10-21)

The pending e2e re-run is done: the phase 5 e2e on `5eae169` (later tree, unlocked idle machine)
passed in full, including every integration host, the keyboard suites (75 real-input screenshots)
and checkboxToggle; visual 162 scenarios / 157 screenshots. Status is now **done** without
reservation.

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
