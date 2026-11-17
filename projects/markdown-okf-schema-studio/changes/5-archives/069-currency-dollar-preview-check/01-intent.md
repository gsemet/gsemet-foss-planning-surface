# Check that prices with "$" render as text in the preview, like Sphinx

User decision (2026-10-24): verify first.

Sphinx's dollarmath leaves prices as text: `$19 base subscription … ($200)`, `$5 and $6`,
`$100–$380`. The preview renders with myst-parser rules, and a comment in
`src/core/render/mystSyntaxDetect.ts` (`inlineDollarLine`) suggests myst-parser can typeset such
text as maths. Only the warning detector is tested (it does not flag prices, F-MYST-027); the
rendered output is not tested anywhere.

## Expected

1. Add a visual scenario (myst group) with the three price sentences from the white paper, light
   and dark, plus one real `$x$` span as a control.
2. If the preview typesets a price as maths: specify it as-is in the myst SwRS ("Known issue"),
   and file a P2 fix to align the preview with Sphinx's dollarmath rules.
3. If it renders as text: the scenario pins it; update the SwRS verification.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
