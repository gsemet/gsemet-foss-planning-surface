# Report — bug-one-line-top-margin-missing

Status: **done** (feature session, 2026-10-16, branch `dev/gsemet`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T09 | The same 40 px gap above the first element of every page (text, heading, table, properties table, empty document); interactive first elements (properties table, first block editor, Start writing) also clear the toolbar when it would overlap them | `3bf2624` |

## Proof of completion

- T09: visual checks measure the gap for each first-element kind, including the properties table
  at 460 px; the RI-T31 jump seen in T08 was traced to a test click target and fixed; review
  APPROVE.
- Phase 2 e2e (2026-10-16, `9afb00f`, clean tree): unit 863, contract 2, security 23; visual 151
  checks / 146 images; integration scroll, untrusted, trusted (incl. realInput, checkboxToggle),
  standalone and reload suites green, 0 failures.

## Open items

- RI-T31 does not assert that the typed "x" landed.
- firstClearance has an extra MutationObserver callback and a layout read on every ResizeObserver
  tick (performance nit).

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
