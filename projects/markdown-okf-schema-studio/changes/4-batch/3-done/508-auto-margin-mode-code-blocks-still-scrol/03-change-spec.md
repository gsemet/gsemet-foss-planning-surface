# Auto width: a code block widens until its longest line fits

Short name: `code-auto-width`. No tracker issue: a verbal report of the owner, relayed by the Chief
of Staff on 2026-11-25. Destination: the running batch batch-09 (stack). Spec critic: yes (round 1
applied, `work/critic-r1.md`).

## Goal

The owner sees it on many pages: with the Width button on Auto, a code block whose longest line is
a little wider than the text column still shows a horizontal scroll bar, although a slightly wider
block would have been enough. In Auto, a code block must behave as a wide table does: it widens up
to the available width (the pane minus the open table of contents and the two 16 px gutters),
centred, so that its longest line fits whenever that width is enough, and it scrolls sideways only
when the line is wider than the available width. Margin and Full width do not change.

## Cause (measured)

The Auto pass is `measureWide()` in `src/page/modules/widthMode.ts`. For every top-level block that
may break out it takes `Math.ceil(Math.max(wrapper.scrollWidth, declared, intrinsic, box))` as the
width the block needs, and sets `--sphinx-preview-breakout` to that width minus the column; a gain
of 1 px or less (`extra <= 1`) is not marked. The CSS rule of
`src/core/preview/styles/contentLayoutStyles.ts` (`html[data-sphinx-preview-width="auto"]
#sphinx-myst-preview-content > [data-sphinx-preview-wide]…`) then gives the block
`box-sizing: border-box; width: calc(100% + var(--sphinx-preview-breakout))`. Two faults follow for
code blocks:

1. **The border is not counted.** A code block is a `pre` with `overflow-x: auto` and a 1 px border
   on each side (`#sphinx-myst-preview-content pre` in
   `src/core/preview/styles/contentBlockStyles.ts`; on the dark background a diff block gets the
   same border from `src/core/preview/styles/codeBlockStyles.ts`). `scrollWidth` measures its
   padding box only (content plus padding, borders excluded), but the breakout sets its border box.
   The widened block is always exactly 2 px too narrow for its own content, so every code block
   that breaks out keeps a scroll bar, for a 2 px overflow: the "slightly wider area" of the
   report. Worse, a code block whose content overflows by up to 3 px is not widened at all: its
   `scrollWidth` is then at most 1 px above the column (an overflow of k px gives a breakout of
   k − 2 px), a "gain of 1 px or less", and it keeps its scroll bar.
2. **A captioned code block never breaks out.** A MyST `code-block` with `:caption:` renders as a
   top-level `figure` holding the `pre` and its `figcaption` (the title bar of
   `figure:has(> pre)`). The pass measures the `figure`, whose `scrollWidth` is its own width,
   because the long line overflows inside the `pre`, not inside the figure. The figure is never
   marked wide and its code always scrolls.

Measured on 2026-11-25 by the spec-writer in Chromium (Playwright, the page built by
`buildPreviewWebviewHtml` with the shipped stylesheet and the page runtime built from `src/` by
`test/page/runtimeHarness.ts`; hand-written renderer markup, a 688 px column in a 1100 px pane, Auto,
the default settings). The figures are `clientWidth/scrollWidth` of the `pre` after the Auto pass:

| Block | Line length | After the Auto pass |
| --- | --- | --- |
| Top-level fence, numbered (Python) | 90 characters | breakout 19 px, `pre` 707 px wide, 705/707: scrolls by 2 px |
| Top-level diff, dark background | 90 characters | `pre` 696 px wide, 694/696: scrolls by 2 px |
| Top-level plain fence | 100 characters | breakout 33 px, 719/721: scrolls by 2 px |
| Captioned `code-block` (top-level `figure`) | 100 characters | figure 688 px, not marked; inner `pre` 686/749: scrolls by 63 px |
| Fence inside an ordered list item | 100 characters | not eligible, 658/756: scrolls (Known issue, D5) |
| Fence of 200 characters (wider than the pane) | 200 characters | capped at 380 px, scrolls (expected) |

In Margin at 100 characters every block scrolls inside the column, as `SwRS-MDOKFSTUDIO-LAYOUT-022`
requires. The same page with the rule of "What changes" (below) simulated in the page (needed width =
the wrapper's box width minus the `pre`'s `clientWidth` plus its `scrollWidth`), checked at 86, 89,
91, 93, 97, 101, 107, 113, 119 and 127 characters: every top-level fence, numbered fence, diff and
captioned block either stays in the column without overflow or breaks out with
`scrollWidth == clientWidth` (no scroll bar). The 200-character block stays capped and scrolls, and
the fence in a list item keeps scrolling.

## Decisions

Each decision of `02-answers.md` is carried; the routine gaps are decided here (the owner asked for
no questions) and named.

| Id | Decision | Source |
| --- | --- | --- |
| code-auto-width-Q1 | Scope: Auto mode only; code blocks are sized like the wide table, up to the available width, and scroll beyond it; Margin and Full width are unchanged; the spec-writer finds the cause (the measured width of the code block versus the Auto container) and updates the SwRS, the tests and `docs/user/wide-tables.md`. | `02-answers.md` Q1 |
| code-auto-width-D1 | The width a code block needs is its whole box: `wrapper box width − code.clientWidth + code.scrollWidth`, rounded up. This counts the `pre`'s two borders, a vertical scroll bar if one ever shows, and, for a captioned block, the frame of its figure, without naming any CSS value. | Cause 1 and 2 |
| code-auto-width-D2 | A captioned code block (a top-level `figure` whose direct child is a `pre`) is measured through that inner `pre`, as a table inside a figure is measured through its inner table. It breaks out as a whole: the caption bar keeps the width of the block. A figure whose `pre` is not a direct child (a Mermaid figure, whose `pre` sits in a `details`) is not a code block. | Cause 2 |
| code-auto-width-D3 | A code block is marked wide when its code really overflows (`code.clientWidth > 0 && code.scrollWidth > code.clientWidth`) and the breakout is at least 1 px (`extra >= 1`): a 1 px overflow shows a whole scroll bar, so no tolerance then. A code block that does not overflow keeps the rule "`extra <= 1` is not marked", as every other block does: fractional box widths (Windows display scaling of 125 % or 150 %, zoom, a non-integer column) round up to 1 px and would otherwise mark and shift every code block that fits. | Routine gap, critic r1 point 1 |
| code-auto-width-D4 | Only code blocks change. Tables, images, figures of images, SVG pictures and Mermaid diagrams keep the measure they have today, so the widths and verdicts the owner reviewed (`test/page/tableBreakout.test.ts`, `WINDOWS_CASES`) do not move. | Routine gap |
| code-auto-width-D5 | A code block nested in a list item, an admonition, a block quote, a tab set or a card keeps the column of its container and scrolls, in every mode, as a nested table does today (Known issue of `SwRS-MDOKFSTUDIO-LAYOUT-023`: only top-level blocks break out). The intent asks for "as a very wide table does"; widening a nested block is a design of its own, left to the inbox follow-up "Nested code blocks do not widen in Auto" (filed by the Chief of Staff, see "Out of scope"). Fence lines at column 0 versus indented, in the owner's Markdown: gsemet-foss-planning-surface 3548/399, chantier 5622/242, okf-schema 1128/150 (a fence inside an admonition directive sits at column 0 and is not counted as indented). | Routine gap, critic r1 point 4 |
| code-auto-width-D6 | The cap is unchanged: a code block whose line is wider than the available width gets the available width (`floor(room − column)`) and scrolls inside it; with row handles nothing changes (code blocks have none). | Q1 |
| code-auto-width-D7 | Margin and Full width are unchanged. The measurement shows no bug there: Margin keeps every block in the column and scrolls it by design (`SwRS-MDOKFSTUDIO-LAYOUT-022`); Full width has no column limit and no breakout, a `pre` is as wide as the pane minus its gutters and scrolls only beyond it. | Q1, measured |
| code-auto-width-D8 | Requirements: `SwRS-MDOKFSTUDIO-LAYOUT-023` (Auto breakout, `req_lifecycle: proposed`) gains the code-block rule. No new SwRS (a new derived SwRS would touch the main paths of the approved `StRS-MDOKFSTUDIO-LAYOUT-003`); no StRS changes: `StRS-MDOKFSTUDIO-LAYOUT-003` already says "a table, figure, image, code block or Mermaid diagram wider than the column uses the available width". | Routine gap, batch rule on approved StRS |
| code-auto-width-D9 | The real measurement test is a new real-browser test, `test/page/codeBlockBreakout.test.ts`, run by the unit stage (skipped when no Chromium starts) and by the `visual` CI job through `npm run test:breakout` with `STUDIO_REQUIRE_CHROMIUM=1`. Its assertions are relations measured in the page (overflow or not, against the widths the page itself reports), so they hold on Windows and on Linux alike: asserted on every platform, no reference widths. | Routine gap |
| code-auto-width-D10 | Docs: `docs/user/wide-tables.md` keeps its file name and title (links and the site navigation), and gains one paragraph about code blocks, in line with D5, placed so that it does not touch the lines CR-498 changes. | Q1 |
| code-auto-width-D11 | A user-facing `fix`: a `## Unreleased` line in `CHANGELOG.md`; the commit type and scope `fix(render)` (preview rendering, `.agents/guidelines/git-commit-allowed-scopes.md`). The writing skill is not touched: no rendered syntax changes. | Routine gap |

## What changes

### 1. The Auto measure (`src/page/modules/widthMode.ts`)

In `installWidthMode`, inside `measureWide()`:

- Add a helper next to `sizedElement` and `tableOf`, for example `codeOf(wrapper)`, that returns the
  code box of a wrapper: the wrapper itself when it is a `PRE`, the direct child `PRE` of a `FIGURE`
  (a captioned code block; walk `wrapper.children`, the test fake has no `:scope` selector), else
  `null`. A figure that holds an image, a table, or a `pre` deeper than a direct child (a Mermaid
  figure) is not a code block.
- In the `widths` map, for a wrapper whose `codeOf` is not `null` and whose `code.clientWidth > 0`,
  the needed width becomes `Math.ceil(Math.max(<today's value>, box − code.clientWidth +
  code.scrollWidth))` where `box` is the wrapper's `getBoundingClientRect().width` (already read).
  When `code.clientWidth` is 0 (a block that is not laid out: hidden, folded, or a fake element in a
  unit test), the term is skipped, so the old value holds. Comment the reason in the code:
  `scrollWidth` excludes the borders and the breakout sets the border box (2 px short), and a
  captioned block's overflow is inside its `pre`.
- Record per wrapper whether its code overflows (`code.clientWidth > 0 && code.scrollWidth >
  code.clientWidth`). In the `measured.forEach` that marks the wrappers, the "no gain" test
  (`if (extra <= 1) return;`) becomes `extra < 1` only for a code block whose code overflows (D3);
  it stays `extra <= 1` for a code block that does not overflow and for every other block (D3, D4).
- Add a `// @implements_req SwRS-MDOKFSTUDIO-LAYOUT-023` marker at the new helper (the function
  already carries the marker; one more block of at most 3 IDs is fine).
- Update the JSDoc of `installWidthMode` ("code blocks stay in the list and are not centred when
  narrow" stays true) with one clause: a code block is measured with its border, a captioned one
  through its inner `pre`, and an overflowing code block has no 1 px tolerance.
- Nothing else changes: `eligibleWrappers` and `wrapperOf`, the held tables of an open cell editor,
  the sideways scroll that `scrolledBoxes` and `restoreScroll` keep (they already cover a `pre`
  inside a wrapper), the shift, the cap, the export of the frozen breakout
  (`src/core/export/exportContent.ts` copies `data-sphinx-preview-wide` and the custom properties
  and needs no change).
- The re-measure is stable: `clear()` releases every breakout before the measure, so the block is
  always measured at the column width, and the second pass gives the same breakout as the first.

No stylesheet change is needed: the existing wide rule already sets `width` and the margins on any
top-level wrapper, the `figure:has(> pre)` is a flex column so its `pre` and caption bar follow the
figure's width (the simulation above confirmed it). If the Driver finds otherwise in the real test,
the fix stays in `contentLayoutStyles.ts`, named in the PR.

### 2. Requirements (`requirements/`)

Read `requirements/guidelines/requirements.guidelines.md` and
`requirements/guidelines/project.guidelines.md` ("During a change") first.

`requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-023.md`:

- Normative behavior: add to the sentence that a code block is widened until its longest line fits,
  its border and a caption bar included, and scrolls only beyond the available area. Keep the
  frontmatter `description` in sync with the normative sentence.
- New scenario, "Scenario (nominal): A code block fits its longest line", as a table:
  | Input | Outcome |
  | --- | --- |
  | Auto, 700 px column, 1000 px pane, a top-level code block with a 1 px border whose `pre` is 698 px inside and 760 px of content | Breakout 62 px (762 − 700): after the pass `scrollWidth` equals `clientWidth`, no scroll bar |
  | The same block captioned (a figure with the `pre` and its caption bar), 800 px of content | The figure breaks out by 102 px and the caption bar has the block's width |
  | A code block whose content overflows by 1 px | Marked wide with a breakout of 1 px (an overflowing code block has no 1 px tolerance) |
  | A code block that fits, with a fractional box width (700.4 px in a 700 px column) | Not marked wide, not shifted |
  | A code block of 1600 px of content | Capped at the available area (breakout 268 px) and scrolls inside it |
  | A code block inside a list item, wider than the item | Not marked; scrolls inside the item (Known issue) |
- "Scenario (boundary): Author pixel width and a gain of 1 px", the two rows to amend:
  - Line 78, "Element 701 px wide in a 700 px column | Not marked wide": the outcome becomes "Not
    marked wide (a table, image or diagram, or a code block whose code does not overflow; an
    overflowing code block, see the code block scenario)".
  - Line 79, "Element as wide as the column, or 1 px wider, measured after a resize | Not marked
    wide": the outcome becomes "Not marked wide; for a code block, not marked unless its code
    overflows".
- Criteria, line 111 (the `Criteria:` line of the Verification notes), two sentences to amend:
  - "the breakout is the ceiling of the largest of scroll width, declared width, intrinsic width and
    box width, minus the column" gains "; for a code block (a top-level `pre`, or a `figure` whose
    direct child is a `pre`) the largest also includes the wrapper's box width minus the code
    box's client width plus its scroll width".
  - "no mark for a gain of 1 px or less (breakout 100 px for the declared case)" gains ", except a
    code block whose code overflows, marked from a gain of 1 px".
  - Add: "after the pass a code block that fits the available area has `scrollWidth <=
    clientWidth`".
- Known issues: "Only top-level blocks, or the paragraph holding only an image, break out" gains
  "; a code block in a list item, admonition, block quote, tab set or card scrolls inside it".
- Verification notes: a new `Method:` line naming the new unit tests (section 3, in
  `test/page/runtimePageControls.test.ts`) and the real-browser test
  `test/page/codeBlockBreakout.test.ts`.
- `implemented_in_files` already lists `src/page/modules/widthMode.ts`; `tested_in_files` gains
  `test/page/codeBlockBreakout.test.ts` if absent (through `just requirements-update`, never by hand
  when the tool writes it).

`SwRS-MDOKFSTUDIO-CODE-007` and `SwRS-MDOKFSTUDIO-CODE-013` already say "outside Auto width mode"
and are not changed. No StRS changes (D8).

After the change: `just requirements-update` (generated files committed) and a dated entry
`## 2026-11-25` (or the day of the change) in `requirements/tiers/log.md`, at its usual place, that
names LAYOUT-023, the cause and the tests.

### 3. Unit tests (fake DOM)

In `test/page/runtimePageControls.test.ts`, next to "T10b" (the file where `widthModeFixture`
lives), with `// @tests_req SwRS-MDOKFSTUDIO-LAYOUT-023` at each test, in a 700 px column and a
1000 px pane (the `widthModeFixture` geometry). Every code-block fake gets its box width through a
`rectProvider` (the measure reads `getBoundingClientRect().width`), and an explicit `clientWidth`
and `scrollWidth`:

1. "a code block that breaks out is widened by its border too": a top-level `pre` with box width
   700, `clientWidth` 698, `scrollWidth` 760 → breakout `62px` (today `60px`: fails before the fix).
2. "a captioned code block breaks out through its inner code": a top-level `figure` (box 700,
   `scrollWidth` 700) holding a `pre` (box 700, `clientWidth` 698, `scrollWidth` 800) and a
   `figcaption` → the figure is marked wide with breakout `102px` (today not marked: fails before
   the fix).
3. "a code block that overflows by 1 px still breaks out": `pre` box 700, `clientWidth` 698,
   `scrollWidth` 699 → breakout `1px` (today not marked: fails before the fix); and a `table` whose
   `scrollWidth` is 701 is still not marked (D4).
4. "a code block that fits is not marked at a fractional width": `pre` box 700.4, `clientWidth` 698,
   `scrollWidth` 698 → not marked, no breakout and no shift property (D3; guards the fix against
   marking every code block under display scaling).
5. "a code block wider than the available area is capped": `scrollWidth` 1600 → `268px`
   (unchanged; the existing T10 `huge` case may carry it instead).
6. "a code block inside a list item is not measured": an `ol > li > pre` wider than the column →
   no `data-sphinx-preview-wide` anywhere.
7. Optional: "a Mermaid figure is not a code block": a top-level `figure` holding a `details` with a
   `pre` inside (`clientWidth` 698, `scrollWidth` 900), figure box 700 and `scrollWidth` 700 → not
   marked, as today (D2).

The `RuntimeElement` fake (`test/page/runtimeHarness.ts`) has `clientWidth`, `scrollWidth` and a
`rectProvider`; extend it only if a needed property is missing. The existing `widthModeFixture`
`huge` element is a `pre` whose `clientWidth` is 0: the guard of section 1 keeps its 268 px.

### 4. The real measurement test (`test/page/codeBlockBreakout.test.ts`)

A new real-browser test modelled on `test/page/svgBreakout.test.ts` and `test/page/tableBreakout.test.ts`:

- The page is the real preview: Markdown rendered by `renderPreviewDocument`
  (`src/core/render/renderPipeline.ts`), the page built by `buildPreviewWebviewHtml`
  (`src/session/webview.ts`, the shipped stylesheet), the runtime from `pageRuntimeScript()`
  (`test/page/runtimeHarness.ts`, built from `src/page/main.ts` at the head under test). No
  hand-written HTML and no copy of the stylesheet: the shipped files are read as they ship.
- The text in the pinned fonts (`pinTestFonts`, `PINNED_MONO_FAMILY` from `test/page/pinnedFont.ts`),
  so the widths do not depend on the machine's fonts. The generated code lines are ASCII only
  (letters, digits, spaces and the `+`/`-` of the diff), so no glyph falls back to another font.
- Chromium launch: the same `chromium.launch()` call and `chromiumUnavailable` pattern as
  `tableBreakout.test.ts` (skip with a message, or fail with the launch error when
  `STUDIO_REQUIRE_CHROMIUM=1`).
- Geometry: a column of 688 px (`maxContentWidth` 688 + 2 × 78 gutters, as the other breakout
  tests) in a 1100 px viewport, the TOC closed; a second pass with the TOC open
  (`toc: true`, the 256 px reserve) for the cap.
- Fractional pass (D3): the same page with `deviceScaleFactor: 1.25` in `browser.newPage` (and, if
  the setting accepts it, a non-integer `maxContentWidth` such as 688.5). Assert that every block
  that fits the column is not marked wide, has no `--sphinx-preview-breakout` and no
  `--sphinx-preview-breakout-shift`, and that its left edge is the column's left edge within 0.5 px
  (no shift); the overflowing blocks still pass the assertions below.
- Document: for a range of line lengths that crosses the column and the available width (for
  example every 3 characters from 70 to 160), each of: a plain fence, a `python` fence of two lines
  (numbered by default), a `diff` fence, a captioned MyST `code-block`, a fence inside a list item.
  Plus one fence of 300 characters.
- Assertions, per block, all measured in the page (D9):
  - In Margin first: read the `pre`'s needed width (its box width minus `clientWidth` plus
    `scrollWidth`) and the available width (pane minus the TOC reserve minus 32).
  - Then switch to Auto (the Width button, or `widthMode: "auto"` at start; wait two animation
    frames after a `resize`, as `svgBreakout.test.ts` does).
  - A top-level block (plain, numbered, diff, captioned) whose Margin needed width is at most the
    column: not marked wide and no overflow.
  - One whose needed width is above the column and at most the available width: marked wide, and
    `pre.scrollWidth <= pre.clientWidth` (no horizontal scroll bar). This is the assertion that
    fails today (by 2 px, or by the whole overflow for a captioned block, or the whole block for an
    overflow of up to 3 px).
  - One whose needed width is above the available width: marked wide, its box width equals the
    available width within 1 px, and it scrolls.
  - The block is centred on the available area within 2 px; the page has no horizontal overflow
    (`documentElement.scrollWidth - clientWidth <= 1`).
  - The fence inside a list item: never marked, still scrolls when wider than the item (D5).
  - Back to Margin: no block is marked and every overflowing block scrolls in the column (D7); in
    Full width no block is marked.
  - Each case writes its numbers with `t.diagnostic` (as `tableBreakout.test.ts` does), so a CI run
    logs them.
- Settings cells (see "Host and default matrix"): each cell boots its own page with the code block
  settings in the runtime context, the way the host sends them (`applyCodeBlockSettings` in
  `src/page/pageSettings.ts` reads `codeBlocks.darkBackground` and `codeBlocks.lineNumbers` through
  `readPreviewBootSettings` once at boot, `src/page/runtime.ts:281`). If the Driver flips the root
  attributes (`data-okf-code-dark-background`, `data-okf-code-line-numbers`) on a running page
  instead, it forces a re-measure (a `resize` event, then two animation frames) before measuring.
  Each cell first asserts that it took effect: the diff `pre`'s computed `border-left-width` is
  `1px` with the dark background on and `0px` with it off; with line numbers off the numbered
  fence's `.myst-code-line` has no `padding-inline-start` of 4ch.
- Markers: `// @tests_req SwRS-MDOKFSTUDIO-LAYOUT-023` on each test.
- `package.json`: the script `test:breakout` runs both files:
  `node scripts/node-test.mjs breakout out/test/page/tableBreakout.test.js out/test/page/codeBlockBreakout.test.js`
  (check that `scripts/node-test.mjs` takes several paths; if not, a glob of the two). The `ci-visual`
  target of the `justfile` and `.github/workflows/ci.yml` are not changed: the job already runs
  `STUDIO_REQUIRE_CHROMIUM=1 npm run test:breakout` after `just dev-ci visual` (Chromium installed on
  Linux). The test also runs in the unit stage (`out/test/page/**/*.test.js`), where it is skipped
  when no Chromium starts.

### 5. Docs (`docs/user/wide-tables.md`)

Insert a new paragraph between the sentence that ends "…and can still break out." and the sentence
"The capture uses the cream theme." (a blank line before and after, so the latter starts its own
paragraph just above the image it introduces). Do not touch the image line nor the lines after it
(CR-498 adds its clip GIF after the image). Text, in the style of the page and in line with D5:

> In Auto width a code block whose longest line does not fit the column widens too, up to the space
> left of the table of contents, centred, so that the line fits without a scroll bar; a captioned
> code block widens with its caption bar. A line wider than that space still scrolls sideways
> inside the block. A code block inside a container (a list, an admonition, a quote, a tab or a
> card) keeps the width of its container and scrolls. Margin and Full width are unchanged.

### 6. CHANGELOG

One line under `## Unreleased` in `CHANGELOG.md`, per "CHANGELOG line" in
`.agents/guidelines/pull-request.guidelines.md`, for example: "In Auto width, a code block whose
longest line is a little wider than the column now widens until the line fits, instead of keeping
a scroll bar; a captioned code block widens too (CR-<number> code-auto-width, PR #<n>)".

### 7. Commits and the pull request

- Commits (`.agents/guidelines/git-commit-message.guidelines.md`):
  `fix(render): fit a code block's longest line in Auto width` (widthMode.ts, the unit tests, the
  real test, `package.json`, LAYOUT-023 and the files `just requirements-update` writes, the log
  entry, the CHANGELOG line), and `docs: explain code blocks in Auto width` (wide-tables.md), or one
  commit if the Driver prefers.
- The PR follows `.agents/guidelines/pull-request.guidelines.md` and the template; it names
  `SwRS-MDOKFSTUDIO-LAYOUT-023` with its source and test files in the Tests section; Impacts holds
  the before/after screenshots ("Screenshots in the PR").
- Stack: in batch-09 this CR has no code dependency on the other CRs. It shares one file with
  CR-498 (`docs/user/wide-tables.md`, different lines, see section 5): if both are in the same
  stack, put this CR above CR-498 or rebase on it; the edit must keep CR-498's GIF line.

## Out of scope

- Code blocks nested in a list item, admonition, block quote, tab set or card (D5). They go to the
  inbox follow-up "Nested code blocks do not widen in Auto" (filed by the Chief of Staff), whose
  design points are:
  - `eligibleWrappers` and `wrapperOf` in `widthMode.ts` accept top-level blocks only;
  - the CSS rule is `#sphinx-myst-preview-content > [data-sphinx-preview-wide]` (direct children);
  - a nested block can grow to the right only (its left edge stays at the container's indent);
  - `.myst-grid-card` clips its content;
  - tab panels, dropdowns and admonitions are to be checked one by one;
  - the export (frozen breakout) and the overlays (edit handles, comments) are to be re-checked.
- Any change to the measure of tables, images, figures of images, SVG pictures and Mermaid
  diagrams (D4), and to Margin and Full width (D7).
- The setting `markdownOkfSchemaStudio.preview.maxContentWidth`, the Width button, its order and
  its stored preference.
- The code block's look (border, padding, line numbers, dark background), the copy button and the
  writing skill.

## Host and default matrix

The change is page code (the webview runtime and the shipped stylesheet); the host does not take
part in it. What it depends on is a shipped default versus a configured value of the code block
settings, which change the `pre`'s border and padding. One line per cell, all covered by the real
test in Chromium (section 4), each cell booted with its settings in the runtime context and checked
to have taken effect, unless marked:

| Cell | `preview.codeBlocks.darkBackground` | `preview.codeBlocks.lineNumbers` | Evidence |
| --- | --- | --- | --- |
| Shipped defaults | on (diff block gets a 1 px border) | on (a block of two lines or more is numbered, 4ch inset) | Real test, every block kind; the diff `pre` border is 1px |
| Dark background off | off (a diff block has no border and no padding) | on | Real test, the diff and the numbered fence; the diff `pre` border is 0px |
| Line numbers off | on | off | Real test, the numbered fence; no 4ch inset |
| Both off | off | off | Real test, the diff fence; border 0px, no inset |
| Display scaling 125 % | defaults | defaults | Real test, fractional pass: fitting blocks unmarked and unshifted |
| VS Code webview, real window | defaults | defaults | Real VS Code preview: the before/after shot of evidence 6 (no automated test in a real window) |

## Evidence

1. The unit tests of section 3: 1, 2 and 3 fail before the fix and pass after (shown in the PR's
   Test plan with the failing run before the fix); 4, 5, 6 (and 7) pass before and after.
2. `test/page/codeBlockBreakout.test.ts` fails before the fix (the "fits the available area" cases,
   by 2 px for a top-level block and by the whole overflow for a captioned block) and passes after,
   on Windows, with its fractional pass; `STUDIO_REQUIRE_CHROMIUM=1 npm run test:breakout` passes
   locally (both files), and the `visual` CI job at the PR's head passes and logs the numbers.
3. `test/page/tableBreakout.test.ts` is unchanged and passes: the table widths and verdicts the owner
   reviewed do not move (D4).
4. `just check` passes; `uv run --no-sync --group requirements okfreq validate --check-links
   --project-root .` and the coverage check as CI runs them pass; `just requirements-update` leaves
   no diff after the commit.
5. Before/after screenshots in Auto, 1100 px pane, cream theme, from the visual harness: a page with
   a numbered fence of about 95 characters and the same block captioned. Before: both scroll (the
   fence by 2 px). After: neither scrolls and both are centred, wider than the column. Plus one
   shot in Margin, unchanged.
6. One before/after shot of a real page of the planning surface (gsemet-foss-planning-surface, a
   page with a top-level code block a little wider than the column) in the real VS Code preview, in
   Auto: before, the block scrolls; after, it fits.
7. `just preflight` passes (on Windows the static stage; CI runs the others).

## Notes for the Driver

- In a new worktree run `just dev` first (`.agents/guidelines/local-worktree.guidelines.md`). The
  spec-writer's own measurement used hand-written markup because the base checkout's dependencies
  were not installed for the render pipeline; the real test must use the render pipeline.
- Read `.agents/constitution.md` before any change.
