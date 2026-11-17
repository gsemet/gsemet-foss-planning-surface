# 235-drop-files-test-bar-tie

Priority: P1 (the heavy `integration` job of every release fails on it). Ships in 1.2.1.
Owner decision, 2026-11-01: release 1.2.0 as it is, fix this in 1.2.1.

## Today

The 1.2.0 release run (41300222825) failed `integration` twice with the same message, and the
failure reproduces locally with
`STUDIO_REAL_INPUT_SCENARIO=drop-files just integration -- --trusted-only`:

```text
source after the image drop: got "…[Getting started](The%20Guide.md)\n\n![logo](../img/logo.png) [plain](plain.md)\n\nSecond paragraph…"
wanted "…Second paragraph of the page.\n\n![logo](../img/logo.png) [plain](plain.md)\n"
```

The test of CR 146 (`test/integration/dropFiles.test.ts`) drops at 80% of the height of the last
paragraph ("Second paragraph of the page."). Measured in the page: the paragraph is 22.4 px high and
two paragraphs are 36.4 px apart, so:

| Insertion bar | Top (px) | Distance to the pointer (px) |
| --- | --- | --- |
| After the link paragraph (before "Second") | 112.8 | 17.9 |
| After "Second" (end of the page, below its margin) | 149.2 | 18.5 |

The pointer is at 130.7: 0.3 px from the midpoint (131.0), on the side of the bar *before* the paragraph. The extension is
right (the nearest bar wins); the test is too sensitive. Heavy jobs do not run on pushes to `main`
that do not change the version, so nothing caught it when it landed.

## After

1. `test/integration/dropFiles.test.ts`: `lowerHalf` returns a point one pixel above the bottom edge
   of the paragraph, so the bar below it is clearly the nearest, with a comment saying why.
2. No product change, no requirement change.

## Decisions

- Not a product bug: dropping on the lower half of the last paragraph of a page inserts before it
  only when the pointer is within a pixel of the midpoint between the two bars. Left as is.
