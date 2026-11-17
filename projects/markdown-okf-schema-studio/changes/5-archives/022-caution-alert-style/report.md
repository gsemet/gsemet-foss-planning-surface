# Report — caution-alert-style (K4)

Status: **done** (2026-10-22, branch `fix/caution-alert-style`, PR #12, merged as `7d2d92e`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | GitHub `[!CAUTION]` and MyST `caution` callouts use the danger red and a new octagon ("stop sign") icon instead of the Warning amber triangle; Warning, Attention, Danger, Error unchanged; CHANGELOG bullet | `e596a6b` → `7d2d92e` |

## Proof of completion

- Unit: new test "caution callouts are red with the octagon icon" (fails on the old stylesheet);
  the warning-group assertion updated with the same intent; unit 1703/0.
- Visual e2e: `37-gfm-gallery` asserts the Caution title colour equals computed
  `--vscode-charts-red` and differs from Warning; `just check` + `just visual` (255) green locally.
- Review: Sonnet reviewer APPROVE r1 (reviews/T1-r1.md); vacuous-regex note fixed by the orchestrator.
- CI: run 39779674653 attempt 1 failed only on unrelated flakes (F1 visual toolbar, F2 linked
  metadata) → CR 023; the user merged PR #12 on 2026-10-22.
- Screenshots: PR body, branch `pr-assets/12` @6b984e3 (keep: the PR body links to it).

## Open items

- Flaky tests F1–F3 → `requests/023-ci-flaky-tests`.
- No MyST `{caution}` fixture assertion (same class and rule as GFM; reviewer note, low risk).
