# K4 — Caution alert style (split from backlog P1/known-issues-k1-k3-k4, 2026-10-22)

Found by the P9 visual campaign. GFM `[!CAUTION]` renders with the Warning amber and triangle icon;
GitHub uses red and an octagon. Add a dedicated caution style/icon.

## Decisions (user, 2026-10-22)

- Q1 (a): every `.caution` turns red — GFM `[!CAUTION]` and MyST `{caution}` (same class).
- Q2: same red as danger/error (`--vscode-charts-red`); only the icon differs.
- Q3: octagon with an exclamation mark (GitHub stop-sign style), mask icon like the others.
- Q4: branch `fix/caution-alert-style` from `origin/main`; one task = one PR (doc, e2e, screenshot).
