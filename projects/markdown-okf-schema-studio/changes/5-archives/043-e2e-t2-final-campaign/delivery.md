# Report — 043-e2e-t2-final-campaign

Status: **done** (2026-10-23, branch `test/real-window-t2-final`, PR #36, merge commit 98195d9).
Re-scoped by the user (decisions 7–9): reduced T2, heavy real-VS Code tests on demand, F from CI.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T2 | Real-window captures for incoming changes, image paste, Restricted Mode (untrusted window), review comment threads | PR #36, 98195d9 |
| CI | Required path keeps the simulated tests; integration and stress move to an optional manual job (`workflow_dispatch` input `heavy`), outside `checks` | PR #36, 98195d9 |
| F | Gallery from the heavy run, README image check, `inventory.md` regenerated (old kept as `inventory-b0.md`, 110/110 real PNGs) | PR #36, 98195d9 |

## Proof of completion

- CI stress run 39963915074 (bc414d4): all 16 scenarios 20/20.
- PR run 39965946197: required `checks` success. Heavy run 39966448771 (20a2d43): 9 trusted +
  untrusted 20/20, gallery success.
- Local: full real-input suite stops at the pre-existing undo step (17 captures passed before it);
  the 4 new scenarios in stress mode 5/5 each; untrusted capture passed in the full run.
- README images: committed = B0; CI Linux differs (fonts); local macOS 12/15 match, 3 changed by
  the new toolbar review-comments button (main). `images/` not committed.

## Open items

Details in `followups.md`:

- Six real-window captures removed by the re-scope (standalone read-only, conf.py MyST warning,
  label rename, Back/Next, Refresh Preview + keybinding, doubleClickToSwitchToEditor); code in
  bc414d4.
- Local macOS undo never restores the buffer (VS Code 1.143.0): CR 048.
- Product observations: conf.py warning not visible in the preview; image pasted at paragraph end
  renders above the text.
- README images refresh from a macOS run in a docs PR.
