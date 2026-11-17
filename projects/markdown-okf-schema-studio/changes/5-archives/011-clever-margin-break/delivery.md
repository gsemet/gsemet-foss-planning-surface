# Report — clever-margin-break

Status: **done** (feature session, 2026-10-16, branch `dev/gsemet`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T10 | One toolbar button cycles Margin → Auto (tables and figures wider than the column break out to the pane width) → Full width; remembered per workspace | `570bcee` |

The toolbar row hosting the button comes from T08 (`201b2d6`, tracked in block-edition-palette).

## Proof of completion

- T10: unit tests for the mode cycle and preference, visual checks for the three modes; review
  APPROVE.
- Phase 2 e2e (2026-10-16, `9afb00f`, clean tree): unit 863, contract 2, security 23; visual 151
  checks / 146 images; integration scroll, untrusted, trusted (incl. realInput, checkboxToggle),
  standalone and reload suites green, 0 failures.

## Open items

- Pre-existing quirk: `maxContentWidth` 0 makes the sticky band padding calc invalid in
  Margin/Auto (fix: emit a large px value for 0).
- The Full width visual assertion is weak.

## Amendment (user request U22, 2026-10-16)

| Task | Change | Commit |
| --- | --- | --- |
| T10b | Narrow tables and figures centred in every width mode (captions too); in Auto a wide table or figure takes min(max-content, free pane width) and is centred on the free area, also with the TOC open; README screenshot in the cream theme (`images/readme/margin-break-cream.png`); page-script injection no longer corrupted by `$&` | `a48535a` |

Proof: 5 new unit tests (4 failed before), visual centring and no-wrapped-cell checks in light, dark
and cream; review APPROVE. Gate B+S+T green (958 unit, visual 155).

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
