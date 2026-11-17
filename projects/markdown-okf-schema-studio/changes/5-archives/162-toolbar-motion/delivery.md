# Report — toolbar-motion

Status: **done** (2026-10-28, branch `change-requests/162-toolbar-motion`, PR [#175](https://github.com/gsemet/markdown-okf-schema-studio/pull/175), head
`e51957b2`, merged as `f39a0aa5`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 (3 rounds) | Shared tooltip slide-in (left + fade) for toolbar, palette and table menu; rows 2–5 expand/collapse as one block; load hint on each new preview opening when saved collapsed (cancelled by input, preference unchanged); all disabled by `prefers-reduced-motion` | `f39a0aa5` |

## Proof of completion

- 3 rounds of 3 (FIX-REQUIRED, FIX-REQUIRED, APPROVE; Coder on Opus in round 3). Local: `just check`,
  `just requirements-update` (0 changes), requirements lint clean; `npm run test:visual` 400 passed.
- CI: normal [40729041950](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40729041950)
  pass on e51957b2. Heavy runs 40728130959 and 40730931376 cancelled (superseded / merged).
- Evidence: before/after GIFs and frame sheets on `change-requests/162-toolbar-motion-assets` (`8be7755d`).
- Autonomous decisions: hint once per panel (state carried by webview snapshots); reduced motion
  disables all three; a row-button press during the hint cancels it and loses that click; the
  pending-changes overlay stays below the open rows; new SwRS TOOLBAR-129/-130 proposed, StRS
  TOOLBAR-001 extended (proposed).
- Heavy proof: run [40729778216](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40729778216) on main `f39a0aa5`.

## Open items

- `interpolate-size` and `transition-behavior: allow-discrete` (Chromium 129+) unchecked in a real
  VS Code window: heavy run above (blocked first by `scenarioTableToolbar`, hotfix CR 167).
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-162` and its branch.
