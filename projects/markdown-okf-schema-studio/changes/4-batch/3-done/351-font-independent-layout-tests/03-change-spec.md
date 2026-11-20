# Change specification: layout tests that do not depend on the page font

Origin: batch-05 retro point, kept by the owner on 2026-11-17 (`intake/request.md`);
`02-answers.md` here. Follow-up of CR-339 (`win-breakout-test`, main commit 02fd3b1c).

## Goal

A unit test that measures the preview in a real browser gives the same result on Linux, Windows
and macOS. Today `test/page/tableBreakout.test.ts` measures tables drawn in whatever font the
machine has for `-apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif` (Segoe UI
on Windows, DejaVu Sans or Liberation on Linux, SF on macOS). Its verdicts move with the font: the
resize test was red on Windows on `main` (a 705 px natural width with Segoe UI, against 727 px
needed by the 760 px pane) and failed `just preflight` for every change until CR-339 lowered the
pane to 600 px. After this CR the test draws its tables in one font, the same on every machine.

## Survey: which unit tests depend on the page font

The unit tests (`npm run test:unit`, run by `just check` and by `just ci-static` on Linux and
Windows) that open a real Chromium:

| Test | Measures | Font-dependent |
| --- | --- | --- |
| `test/page/tableBreakout.test.ts` | table widths against a 688 px column, breakout verdicts | yes, all six tests (below) |
| `test/page/svgBreakout.test.ts` | an SVG picture's declared width (900, 300 px, 90 %) | no: no text in the measure |
| `test/page/chartCsp.test.ts` (with `test/page/chartPage.ts`) | render states, SVG text, policy violations | no: no size asserted |
| `test/page/mermaidLabelFit.test.ts` | each label's text against its own box | no: relative by design; it must keep the page's own fonts, since it checks a mismatch between page and image fonts |
| `test/site/socialCard.test.ts`, `test/site/requirementsViewer/cards.test.ts`, `useCaseDiagram.test.ts` | PNG size 1200 x 630, SVG content | no: a fixed canvas, no text measure |

The other `test/page/**` tests run on the fake DOM of `test/page/runtimeHarness.ts` or hand-made
objects, with sizes set by the test: no font. The Python visual checks (`test/visual/capture*.py`,
`just ci-visual`) run only on the Linux CI image, never in `just check` nor on Windows; they are
out of scope.

In `tableBreakout.test.ts`, every test asserts a verdict or a width that comes from the natural
width of text:

1. "Auto keeps a table in the column when its minimum widths fit and breaks it out when they do
   not" (LAYOUT-044): the twelve owner-reviewed verdicts (`CASES`) depend on text widths against
   the 688 px column (the comment above cases 6 and 12 already works around Consolas against DejaVu
   Sans Mono).
2. "Auto breaks a table out when a cell holds content that cannot shrink" (LAYOUT-044): the
   110-character line and the command line break out only if their width passes 688 px.
3. "Auto keeps the breakout of a table while a cell is edited, in every cell it moves to"
   (LAYOUT-023): needs the tick matrix wide before the edit.
4. "Auto keeps a table that fits the column in the column while a cell is edited" (LAYOUT-023):
   needs the eight-column table in the column.
5. "Auto measures a table again on a real resize while a cell is edited" (LAYOUT-023): the CR-339
   test; the pane must be narrower than the tick matrix's natural width.
6. "Auto gives the column width to a table edited as source, or holding another editor field"
   (LAYOUT-023): needs the long-code-paths table wide before the edit.

## Decision: pin a bundled font in the test page

The test page loads one font for prose and one for code, from files every machine has, and the
theme's font variables point to them. Reason: the twelve verdicts of test 1 are the LAYOUT-044 rule
itself (text widths against a column), so no relative rewrite can keep them without computing the
table's minimum widths again in the test, which would test the page against a copy of itself.
Pinning the font fixes every width at once, keeps each assertion's intent unchanged (constitution,
section 3) and serves any later layout test.

The font: KaTeX's `KaTeX_SansSerif-Regular.woff2` and `KaTeX_SansSerif-Bold.woff2` (prose,
table headers in bold) and `KaTeX_Typewriter-Regular.woff2` (inline code), from
`node_modules/katex/dist/fonts/`. KaTeX is already a runtime dependency (`package.json`,
`"katex": "^0.19.1"`), installed by `npm ci` on every machine and CI job, under the MIT license:
no new dependency, no font file added to the repository (constitution, section 5).

Glyphs these fonts lack fall back to the platform's font: `✓` (U+2713, the tick matrix's cells) and,
in code, `–` (U+2013, not used in code cells). A tick sits in columns whose header (`GFM`,
`Mermaid`, `PlantUML`, ...) is wider than it, so the fallback does not move a column. KaTeX's sans
also lacks `< > | { } \` and the backtick, none of which appears in the prose of the cases.

## What changes

### New helper: `test/page/pinnedFont.ts`

- Exports the family names (for example `Studio Test Sans`, `Studio Test Mono`) and one function,
  for example `pinTestFonts(page: Page): Promise<void>`, that:
  - reads the three woff2 files in Node, from the `katex` package's `dist/fonts/` folder found
    from the extension root (as `test/page/chartPage.ts` finds it: `path.resolve(__dirname,
    "../../..")`, then `node_modules/katex/dist/fonts/`);
  - in the page, adds them with `new FontFace(family, bytes, { weight })` and `document.fonts.add`
    (bytes passed from Node: no fetch, so the page's Content Security Policy is not involved),
    and awaits each face's `load()`;
  - sets `--vscode-font-family` and `--vscode-markdown-font-family` to the sans family and
    `--vscode-editor-font-family` to the mono family on `document.body`, the way `openPage` sets
    the theme variables (CSSOM, which the policy allows);
  - throws when a face does not reach `status === "loaded"`, with the file name: a missing font is
    an error, never a silent fallback to the platform's font.
- `test/visual/themes.ts` is not changed: the visual captures keep their fonts.

### `test/page/tableBreakout.test.ts`

- `openPage` calls the helper right after it sets the theme variables, before the
  `data-sphinx-preview-width` wait; tests 1 to 6 all go through `openPage`.
- One assertion that the pin holds, in test 1: the computed `font-family` of a table cell starts
  with the sans family and of an inline code span with the mono family, and
  `document.fonts.check("14px \"<sans family>\"")` is true.
- The header comment states that the page draws its text in the pinned KaTeX fonts, so widths and
  verdicts are the same on every machine. The comment above cases 6 and 12 (Consolas against DejaVu
  Sans Mono) and the comment of test 5 (705 to 797 px across platforms) are rewritten for the
  pinned font: test 5's comment gives the tick matrix's natural width measured with it.
- The 600 px pane of test 5 stays (below the natural width with the pinned font as with every font
  probed by CR-339). No other number, threshold or verdict changes; `@tests_req` markers stay.
- The review pictures (`STUDIO_TABLE_SHOTS`) now show the pinned font; they are on-demand pictures,
  not baselines.

### Stop rule

If, with the pinned font, one of the twelve verdicts of `CASES` (or a precondition of tests 2 to 6)
no longer holds, the Driver does not change the verdict, the case or the column: the verdicts are
the owner's review. It records the measured widths in the PR body and stops for the Chief of
Staff.

## Out of scope

- Visual baselines (screenshots of `just ci-visual`, the gallery): unchanged, since
  `test/visual/themes.ts` and the capture scripts are not touched.
- The product's fonts and styles (`src/`): no change. No SwRS changes; no `requirements/` edit and
  no `requirements/tiers/log.md` entry (no behaviour change).
- The other browser tests of the survey, and the integration and e2e tests (real VS Code windows).
- A new dependency or a committed font file.

## Evidence

- `just check` passes on Windows (the machine where test 5 was red), including
  `out/test/page/tableBreakout.test.js`.
- The pull request's `ci-static` job passes on Linux and Windows.
- In the PR body: the tick matrix's natural width (test 5's `open.width`) and the twelve case widths,
  measured on Windows and read from the Linux CI log or a Linux run; equal within 1 px on both. To
  read them, the Driver may print them in a local run; the committed test does not log them.
- Proof the pin works: on Windows, with the pin temporarily removed, the widths are those of Segoe
  UI (the tick matrix about 705 px), and with it, the pinned font's width; stated in the PR body.
- `just preflight` passes (on Windows, its static stage).

Commit type: `test:` (no scope, per `.agents/guidelines/git-commit-allowed-scopes.md`).
