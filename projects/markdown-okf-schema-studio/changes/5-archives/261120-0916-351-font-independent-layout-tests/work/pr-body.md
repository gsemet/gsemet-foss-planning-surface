## Summary

The table breakout unit tests open a real Chromium page and measure tables drawn in whatever font
the machine has (Segoe UI on Windows, DejaVu Sans or Liberation on Linux, SF on macOS), so their
verdicts moved with the platform: the resize test was red on Windows until its pane was narrowed.
The test page now loads the KaTeX sans and typewriter fonts (KaTeX is already a runtime
dependency) and draws every table in them, so the widths and verdicts no longer depend on the
machine's font.

## Deliverables

A new test helper loads three font files from the installed `katex` package into the page and
points the theme's font variables at them; `openPage` calls it before any measure.

```ts
// test/page/pinnedFont.ts
export const PINNED_SANS_FAMILY = "Studio Test Sans";
export const PINNED_MONO_FAMILY = "Studio Test Mono";
export async function pinTestFonts(page: Page): Promise<void> {
  // reads KaTeX_SansSerif-Regular/-Bold and KaTeX_Typewriter-Regular .woff2 from node_modules,
  // adds them with new FontFace(...) + document.fonts.add, awaits load(), throws with the file
  // name when a face does not load, then sets --vscode-font-family,
  // --vscode-markdown-font-family and --vscode-editor-font-family on the root element and body
}
```

Measured widths on Windows 11 (headless Chromium, light and dark identical); `W` breaks out of the
688 px column, `s` stays in it:

| Case | Expected | Pinned KaTeX fonts | Machine font (Segoe UI, Consolas) |
| --- | --- | --- | --- |
| 1 two columns: short name, long prose | stays | 688 s | 688 s |
| 2 two columns: prose in both | stays | 688 s | 688 s |
| 3 three columns: short, short, prose | stays | 688 s | 688 s |
| 4 four columns: one prose, three short | stays | 688 s | 688 s |
| 5 four columns: prose in every column | breaks out | 1068 W | 1068 W |
| 6 two columns: long code paths | breaks out | 735 W | 775 W |
| 7 three columns with a long URL | breaks out | 748 W | 773 W |
| 8 five columns: short numbers | stays | 338 s | 341 s |
| 9 eight columns: numbers | stays | 537 s | 537 s |
| 10 ten columns: tick matrix | breaks out | 719 W | 705 W |
| 11 six columns: mixed, medium text (text lengthened) | breaks out | 894 W | 932 W |
| 12 three columns: inline code identifiers | breaks out | 824 W | 863 W |

- The tick matrix's natural width with the editor open (the resize test) is 719 px with the pinned
  fonts and 705 px with Segoe UI; the 600 px pane stays below both.
- With its previous text, case 11 measured 688 px (stays) in the pinned fonts against 861 px with
  Segoe UI. Its inline code names are now longer: its minimum width in the pinned fonts is 734 px,
  46 px over the column.
- Linux: **UNVERIFIED.** No CI job runs these tests in a browser: the Linux and Windows `static`
  jobs skip them ("no Chromium can start here"), so the Linux widths and verdicts are not proven
  (see Known gaps).

## Changes

- `test/page/pinnedFont.ts` (new): loads the fonts from bytes passed from Node (no fetch, so the
  page's Content Security Policy is not involved) and throws with the file name when a face does
  not load (see Known gaps for how the run ends then).
- `test/page/tableBreakout.test.ts`: `openPage` pins the fonts after setting the theme variables;
  test 1 asserts the pin holds (a cell's computed `font-family` starts with the sans family, an
  inline code span's with the mono family, and `document.fonts.check` is true); the header comment,
  the comment above cases 6 and 12 and the resize test's comment now describe the pinned fonts;
  case 11's inline code names are longer. No other case, verdict, threshold, column or pane
  changes; the requirement markers stay.
- `test/visual/themes.ts`, the visual captures and `src/` are not touched.

## Impacts

No visual change: test-only change; the product's fonts and the visual baselines are unchanged.
The on-demand review pictures of the breakout test (`STUDIO_TABLE_SHOTS`) now show the pinned
fonts.

## Blast radius

Grade: 1. Two test files; a `git revert` restores the machine-font tests.

## Human decisions

- Case 11 stayed in the column with the pinned fonts while its reviewed verdict is "breaks out".
  The owner chose to keep the pinned fonts and revise only that case's text so it still breaks out,
  keeping its six mixed columns and its verdict.

## Autonomous decisions

- The font variables are set on the root element as well as on the body: the preview's prose font
  is resolved on the root element, so a body-only value reached code spans but not prose.

## Known gaps

- Linux widths and verdicts are UNVERIFIED. The widths above were measured on Windows only; no CI
  job runs the breakout tests in a browser (the Linux and Windows `static` jobs skip them: "no
  Chromium can start here"), and no Linux machine was available for a local run. A follow-up is
  filed to run them in a Linux browser.
- A pinned font that fails to load hangs the test run instead of ending it. `pinTestFonts` throws
  with the file name, but `openPage` does not close Chromium then, so the node test process does
  not exit unless it runs with `--test-force-exit`.

## Test plan

- [x] New or changed tests (they fail on the previous code), at 80940a3 (carried from 3d1c337: clean rebase onto main, same patch):
      the pin assertion fails without the pin (cell font starts with `-apple-system`); case 11
      with its old text fails with the pin.
- [x] Requirements: no behaviour change (test-only); markers unchanged.
- [x] Changelog: no user-facing change.
- [x] Local gates (Windows) at 80940a3 (carried from 3d1c337: clean rebase onto main, same patch): `just preflight` (static stage, which runs `just check`)
      pass (unit: 4059 pass, 0 fail, 15 skipped).
- [x] Review: approved at 80940a3 (carried from 3d1c337: clean rebase onto main, same patch)
- [x] CI green at 80940a3 ([44707160557](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44707160557)):
      `checks`, `report`, `static`, `static-windows`, `visual` pass; the real VS Code jobs are
      skipped on a pull request (a heavy dispatch at the same patch, carried from d4a0089, passed
      on its one re-run). The `static` jobs skip the breakout tests (see Known gaps).

## Internal references

- Planning surface CR-351 (font-independent layout tests), follow-up of CR-339.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
