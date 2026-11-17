# Report — 046-light-animations

Status: **done** (2026-10-23, branch `feat/light-animations`,
[PR #41](https://github.com/gsemet/markdown-okf-schema-studio/pull/41), merge commit 9da2c26).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Light preview animations (update glow 600 ms, editor-close fade), reduced-motion respected, visual suite runs with reduced motion, real-window test | 7b8dd7b (9da2c26 on main) |

## Proof of completion

- 2/3 rounds, reviewer APPROVE in both.
- Local: tsc clean, unit 1940/1940, `just check`, `just visual` 303/303, trusted real-window suite once under the lock.
- CI: PR [run 39976750605](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/39976750605) — the user merged
  before visual finished; it then passed (static, visual, report, `checks` success). Main
  [run 39976939711](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/39976939711) success.
- Screenshots light/dark/cream before/after on `pr-assets/41` (cd9e994).
- Autonomous decisions (in the PR body): 600 ms glow; no glow while typing in the active editor (undo/redo always glow); close fade may be cut by the next update; reduced-motion rule `0s`.

## Open items

- Two stale comments saying the final frame shows the glow: `test/visual/capture.py:2769`,
  `test/visual/scenarios.ts:197-199` (low severity, unfixed; backlog candidate).
