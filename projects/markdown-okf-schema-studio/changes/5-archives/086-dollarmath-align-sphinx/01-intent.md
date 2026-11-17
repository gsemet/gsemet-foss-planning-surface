# Align the preview's dollar maths with Sphinx's dollarmath rules

The preview typesets prices as maths: `$5 and $6` becomes the maths `5 and ` between two dollar
signs removed, `$19 base ... ($200)` and `$100–$380` likewise. Sphinx (markdown-it dollarmath)
leaves them as text: the opening `$` must not be followed by whitespace, the closing `$` must not
follow whitespace or precede a digit.

Specified as-is (Known issue) in SwRS-MDOKFSTUDIO-MYST-024; pinned by visual scenarios
`myst/v35-dollar-prices-full-light-900` and `myst/v36-dollar-prices-full-dark-900` (fixture
`55-dollar-prices`). The warning detector already applies Sphinx's rules
(`inlineDollarLine` in `src/core/render/mystSyntaxDetect.ts`).

## Expected

1. A price such as `$5 and $6` renders as text; a real `$x$` span stays maths.
2. Apply the same delimiter rules as the detector in the render path (parser option or a
   pre-pass that escapes the amounts), without changing `$$` blocks or `\(...\)`.
3. Update the two scenarios' assertions, remove the Known issue line of MYST-024 and add a unit
   test that fails on the previous code.
