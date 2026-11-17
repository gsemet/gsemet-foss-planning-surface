# Block range checks treat no-break / ideographic spaces as blank

From the host guard PR #187: `isBlank` uses `trim()`, which also strips U+00A0 and U+3000. The
renderer treats a line holding only those as paragraph text, so the guard refuses to open such a
paragraph (refresh does not help); copy, cut and move already behave the same. Fix: blank = only
spaces and tabs (`/^[ \t]*$/`) in `src/core/mapping/blockRange.ts` and `blockMove.ts`, with tests.
Also optional: the page sends the block tag so the host can check kind consistency.
