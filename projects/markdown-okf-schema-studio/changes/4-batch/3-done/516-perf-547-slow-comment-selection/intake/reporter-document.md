# The reporter's document, measured without a window (2026-11-26)

The gist of issue 547 (14 files, about 234 KB), downloaded on the owner's word into a folder outside
the repository and copied, with its charts under `svg/`, for the measure. Same harness as
`request.md` (headless Chromium, main 5f0746d), three runs, the reporter's document alternated with
the generated "full" and "small" ones. No error, no network request from the page, 9 of 9 comment
threads anchored. The machine was loaded by other work, so the throttled figures are noisy.

Page main thread, milliseconds per step, medians: reporter / full / small.

| scenario | normal | CPU four times slower (quietest run in brackets) |
|---|---|---|
| drag over text | 1.44 / 1.28 / 1.09 | 13 (10) / 27 (10) / 9 (8) |
| drag over cells | 1.55 / 1.32 / 1.01 | 25 (12) / 28 (10) / 8 (8) |
| release | 5.3 / 4.1 / 2.8 | 29 (27) / 45 (20) / 14 (12) |
| drag while scrolling | 4.8 / 4.1 / 2.2 | 58 (55) / 84 (30) / 18 (17) |
| extend a large selection | 6.2 / 3.1 / 0.86 | 42 (34) / 39 (18) / 10 (5) |
| scroll with a large selection | 11.1 / 5.2 / 1.14 | 96 (66) / 108 (30) / 7.5 (6.5) |
| comment, save to the DOM (n=9) | 69 / 58 / 44 | 478 (193) / 281 (146) / 68 (60) |

- Normal speed: no stall. In the selection scenarios the median longest task is at most 8.8 ms (worst
  run 12 ms).
- The reporter's document is heavier than "full": 3160 elements in the page against 1873 (856 `code`
  against 22, 864 `strong` against 197, 21 blockquotes against 0), with fewer table cells (620 against
  879). Both are 464 lines; 61 against 53 KB. The charts do not differ (11 external images).
- A comment save restyles 3222 elements against 1892 (the root `:has()` rule), style 11.2 against
  7.4 ms.
- Large selections cost about twice "full", about half of it script; the element count is the likely
  cause, not isolated.
- Not measured: a real VS Code window, its messages and GPU; the reporter's machine.
