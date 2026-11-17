# The toolbar-float `:has()` rule slows the load of very large pages

Type: perf · Priority: P3 · Filed 2026-10-31 from the v20 hang investigation (stack -v5)

## Today

The narrow-toolbar fix (d5c3de33) added document-wide `:has()` selectors: `#sphinx-myst-preview-content:has(...)`,
and a clear rule written as `:not(:has(...)) > :not(...)`, in `src/core/preview/styles/contentLayoutStyles.ts` and
`contentBlockStyles.ts`. On the 2.3 MB visual fixture, they lengthen the parse and style pass:
- load goes from about 0.34 s to 0.47 s;
- main-thread busy time goes from about 220 ms to 320 ms (headless, local).

This also widened the Playwright networkidle race behind the v20 hang (now removed from the harness). Evidence:
`/private/tmp/claude-502/v20-debug/NOTES.txt` (scratch, may be gone).

## Expected

Replace the document-wide `:has()` test with a flag or class set at render time (or by firstClearance), so that
style matching stays local. The layout is the same as today, and the huge-document load returns to its pre-fix cost.

Proof: same layout in the narrow-toolbar visual scenarios; a load-time measure on the huge fixture before and after.
