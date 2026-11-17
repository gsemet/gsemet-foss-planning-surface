# 149 — Vega-Lite and Vega charts, and a new "Full" palette mode

Type: feat · Priority: P1 · From the user, 2026-10-27 (overnight run)

## Intent (user)

See [01-intent.md](../01-intent.md).

## Autonomous decisions

- Decided by the main session on 2026-10-27; list these in the PR body under "Autonomous decisions".
- Placed on the stack above CR 148.
- Vega is supported together with Vega-Lite: same runtime, no extra size.
- Charts render in every palette mode; only the insert commands belong to Full.
- Full's other extensions are left for a later grill with the user; this CR adds the mode and its
  first extension (charts) only.
