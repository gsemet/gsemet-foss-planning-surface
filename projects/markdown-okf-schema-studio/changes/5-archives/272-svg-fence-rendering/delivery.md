# Report — 272-svg-fence-rendering

Status: **done** (2026-11-10, branch `change-requests/272-svg-fence-rendering`, PR #340, merge commit `5d2f13cf`, fixes GitHub #336).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A `svg` fence or a raw `<svg>` block is drawn as a themed picture, with a dedicated sanitizer, per-theme variables and width-mode handling; SwRS, requirements log, CHANGELOG and writing-skill examples | `5d2f13cf` |

## Proof of completion

- Three rounds, Inspector on Opus each time: r1 FIX-REQUIRED (HTML comment and `$$` breakage, id references leaving the picture, placeholder forgery), r2 FIX-REQUIRED (the fixes caused regressions in code block content and `aria-*` attributes), r3 APPROVE (coder on Opus).
- Round 3: `just check` passed (3671 unit, 93 security); the headless visual capture of diagrams and rendering-core ran 53 scenarios and passed; the 5 new tests failed against the reverted round-2 fixes.
- CI at head `ddacc7b6`: PR run 42844361852 green; heavy run 42844031952 green (integration and stress included).
- Screenshots (Cream, White, Dark, edit mode, before and after) are on branch `change-requests/272-svg-fence-rendering-assets`.

## Open items

- `fill`, `stroke`, `mask` and `clip-path` still skip the value check in the final sanitizer pass, as on main: the Inspector suggests a backlog item to tighten them (not filed by this run).
- A raw `<svg>` in a table cell stays dropped (SwRS-GFM-031); the HTML sanitizer now allows `textPath` with an inert link.
