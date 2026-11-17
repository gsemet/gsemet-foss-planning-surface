# CR 226, round 1, Inspector review

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-226` (uncommitted diff on
HEAD `0b4ede78`). I read the constitution, `AGENTS.md` and `rules.md` first.

## Verdict: CHANGES REQUESTED

The approved case works: at 393 px no heading or first-paragraph line runs under the toolbar. The
heading keeps its 40 px gap. The unit and visual tests fail on the old code. But the full visual
campaign shows 7 regressions that pass at HEAD, so `just preflight` would fail. The heading-clear
change also has a user-visible side effect outside the brief.

## Findings

### 1. Blocker: 7 visual scenarios fail with the change and pass at HEAD

How I checked: I ran the visual groups with the CR applied (411 scenarios: 404 pass, 7 fail).
Then I put the 3 `src/` files back to their HEAD version, rendered again, and ran the 7 failing
scenarios plus v88. All 7 passed and v88 failed. I then restored the files.

- `layout-width/v66`–`v71` width-cycle (light, dark and cream, at 900 and 1600 px) fail with
  "the narrow table is not centred in the column". At 900 px this happens in margin, auto and full
  modes; at 1600 px in full mode only.
  - At 900 px, HEAD centres the small table at 356..544 (offset 0). With the CR it sits at 330..518
    (offset −26 px, half of the 52 px float).
  - Cause: a table, a centred figure, a `pre` with overflow, a flex or grid editor frame, and any
    other block that forms its own block formatting context cannot run under a float. Beside the
    float it is narrowed or re-centred **as a whole box, over its full height**. This is more than
    "the first lines wrap", and it is not the accepted "border or background may run under the
    toolbar".
- `palette-slash/v28-palette-clears-text-rule-cream-900` fails. In edit mode, opening the editor of
  the paragraph under the title (fixture `64-rule-edit`) gives "the palette's bottom edge 260 is
  below the top of the textarea 246" and "the palette covers the top of the frame". The palette
  spans 190–260 and the frame 239–306. The frame of a block that starts beside the float is now
  laid out next to it.

The coder's gates (`just check` plus the single v88 scenario) do not include the visual campaign,
which is why these were missed.

Fix direction: this needs an owner decision, because each option is visible. For example:

- **Block editors:** have `measureFloat()` (`src/page/modules/firstClearance.ts:139`) return 0
  while any `.sphinx-preview-block-editor` is open in the column, the same way it does for the
  first-block editor.
- **Tables, figures, `pre`, admonitions:** either let them clear the float
  (`clear: inline-end` on those top-level blocks: they move below the toolbar and leave a blank
  band), or accept the narrowing and off-centring and update v66–v71 after an owner gate.
  Assertions must not be changed silently.

After the fix, run at least the `layout-width`, `palette-slash`, `block-editing` and `myst` groups.

### 2. Major: headings no longer clear raw-HTML `align` floats

File: `src/core/preview/styles/contentBlockStyles.ts:39`

The new selector only treats `img` and `figure` elements with the class `.align-left` or
`.align-right` as floats. But the sanitizer keeps the HTML `align` attribute
(`src/core/security/html-sanitizer.ts:74`). So `<img align="right" src="logo.png">`, the usual
README logo pattern, and `<table align="right">` still float, and the headings after them no
longer clear them.

Probe at 1300 px, adding `<p><img align="right" height=400></p><p>short</p><h2>`:

| Case | Heading `clear` | Result |
| --- | --- | --- |
| Raw `<img align="right">`, with the CR | `none` | Heading top 401, image bottom 745: the heading wraps beside the logo |
| Same input at HEAD | `both` | Old rule matched every top-level heading |
| MyST `img.align-right`, with the CR | `both` | Heading top 761, below the image: still correct |

What still works:
- MyST `:align:` figures keep their behaviour (myst v17–v19 pass).
- Floats nested in a list, a directive or an admonition are still found by the `:has()` branch.
- Headings later in the document still clear, through `~`.
- The rule is still direct-child only, as before.
- Every heading that does not come after an aligned element had no float above it before, except
  now the toolbar float. So for MyST content the change is equivalent to before.

Smallest fix: extend both float lists in the selector to the attribute form as well, for example
`:is(img, figure, table):is(.align-left, .align-right, [align="left" i], [align="right" i])`, in
the direct form and inside the `:has()`.

The alternative, keeping `clear: both` and exempting only `:first-child` headings, is worse: a
second heading inside the toolbar's reach would jump below 186 px.

`:has()` is safe: the `engines` range is `vscode ^1.95.0` (Electron 32, Chromium 128), and `:has()`
is supported since Chromium 105. `float: inline-end` is supported since Chromium 118.

Also needed: a test for the heading-clear rule (raw `align` and MyST `.align-*`), and one line in
SwRS-MDOKFSTUDIO-LAYOUT-043 saying that top-level headings clear aligned images and figures before
them but never the toolbar float. SwRS-MDOKFSTUDIO-MYST-031 line 95 ("top-level headings clear
the float") stays true.

### 3. Minor: the SwRS-MDOKFSTUDIO-LAYOUT-043 nominal scenario mixes two geometries

File: `requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-043.md` (nominal scenario)

The scenario uses the unit-test geometry (content box 16..377, float width 108 px) but labels it
"a 393 px column", which is also the visual check. The real 393 px page has a content box of
31..362 and publishes 93 px.

Fix: word the scenario as an abstract column ("a column whose content box ends at 377 px…"), or use
the real numbers.

Also state the behaviour that finding 1 settles: what happens to blocks with their own formatting
context beside the float, and that in Full width mode the float exists at every pane width.

### 4. Minor: `measureFloat()` assumes the toolbar is on the physical right

File: `src/page/modules/firstClearance.ts:157`

The width is computed as `right - bar.left`, while the CSS uses `float: inline-end`
(`contentLayoutStyles.ts:48`) and the toolbar uses `inset-inline-end`. With a right-to-left root,
both would sit on the left, but the width would come out as almost the whole column (capped). The
first 186 px would then hold no text. This cannot happen today: no right-to-left root direction is
set, and the existing `measure()` makes the same assumption.

Fix: use `float: right` to match the measurement, or measure the overlap on both sides:
`min(right, bar.right + m) - max(left, bar.left - m)`.

### 5. Nit: duplicated geometry code

File: `src/page/modules/firstClearance.ts:139-158`

`measureFloat()` repeats the lookup, padding and overlap code of `measure()` (lines 70–79). A
shared `geometry()` helper would keep the two in step.

## Review focus, answered

1. **`measureFloat()` correctness:**
   - Document coordinates are correct: the height is measured from the toolbar bottom to
     `column.top + scrollY`, and the unit test covers a scrolled page.
   - It does not depend on its own result. The probe confirmed `#sphinx-myst-preview-content` is
     `display: flow-root` with no top padding, so the float spans 0–186 px from the column top. The
     last narrowed line is at 183 px and the first full line at 205 px.
   - No loop: `setProperty` on the root fires the "root attribute" observer once, and the next
     `apply()` finds nothing changed. `settle()` is unchanged.
   - A hidden or zero-size toolbar gives 0.
   - The table of contents column, the width modes and zoom (which works through font size, so
     pixel values are unaffected) are all measured from live rectangles; the `theme-zoom` group
     passes.
   - Width cap: correct.
   - Right-to-left: finding 4.
2. **Heading-clear change:** finding 2. MyST cases are equivalent, raw-HTML `align` regresses, and
   `:has()` is supported.
3. **Non-zero float at 900 px:** consistent with the approved scope ("any width where the toolbar
   overlaps"). On the CR fixture at 900 px, HEAD had no text under the toolbar, because the lines
   happen to end before 784 px. A full-length first line would run 44 px under it, so the toolbar
   can cover text at 900 px too.
   - With the CR, the first ~186 px lose 52 px of width. That is mild for text, but it causes the
     table off-centring in finding 1.
   - In Full width mode the float exists at every pane width (v67, v69 and v71 at 1600 px).
   - The float becomes 0 from about 1100 px in auto mode.
4. **Edit mode:**
   - The first-block editor, the Start writing button (which only appears in empty documents) and
     a leading properties table give a float of 0, so the existing inset and clearance logic is
     untouched. The unit tests and the frontmatter groups pass.
   - When the first-block editor opens, the float drops to 0 and the text below reflows. That is
     expected.
   - The editor of a non-first block inside the float's reach regresses (finding 1, v28).
   - Blocks with their own formatting context regress too (finding 1).
5. **Tests:**
   - The unit tests fail before the fix. I swapped in `git show HEAD:src/page/modules/firstClearance.ts`,
     compiled and ran them: the 3 "CR 226" tests fail with `actual: undefined` and 16 pass. Then I
     restored the file.
   - The visual scenario v88 fails at HEAD with the reported rectangles
     (`31,138,324,155 | 31,161,359,178` under `277,12,379,178`).
   - No assertion was weakened, and the e2eGroups count change 410→411 matches the one new
     scenario.
   - The `@implements_req` and `@tests_req` markers point to SwRS-MDOKFSTUDIO-LAYOUT-043 and are
     correct.
   - Every touched requirement is `req_lifecycle: proposed`: LAYOUT-011, StRS-LAYOUT-004 and the new
     LAYOUT-043. The index and links blocks were regenerated. No approved requirement was edited.
   - Missing tests: the heading-clear rule (finding 2), and the effect on blocks with their own
     formatting context and on editors (finding 1).

## User-visible changes the owner did not approve

1. Tables, centred figures, code blocks and other blocks that form their own formatting context,
   when they start within the toolbar's reach, are narrowed or shifted off-centre over their full
   height. This applies at 393 to ~1100 px in auto and margin modes, and at every width in Full
   mode.
2. In edit mode, the editor frame of a non-first block within the toolbar's reach lays out beside
   the float, and its palette covers the top of the frame (v28 at 900 px).
3. Headings no longer clear raw-HTML `align="left|right"` images and tables, such as README logos.
   They wrap beside them.
4. In Full width mode the text float is present at every pane width. This is arguably covered by
   "any width where the toolbar overlaps", but the owner should know.
5. A right-aligned MyST figure within the first ~186 px now sits left of or below the toolbar float
   instead of under the toolbar. This is an improvement, but it is a visible change.

## Commands run

- `npm run compile` then `node --test out/test/page/modules/firstClearance.test.js`: 19/19 pass.
- The same with `firstClearance.ts` swapped back to HEAD: 3 fail (`actual: undefined`), 16 pass.
  File restored and recompiled.
- `just check` (foreground): exit 0. Unit 3323/3323, security 71/71, pytest 153 passed,
  requirements lint green.
- Visual (I held the machine lock `226`; it was found already gone at my first release, and I took
  and released it again for one probe):
  - `capture.py --scenario layout-width/v88-toolbar-float-first-lines-cream-393`: passed.
  - Groups `layout-width`, `myst`, `palette-slash`: 155 passed, 7 failed (finding 1).
  - Groups `block-editing`, `rendering-core`, `gfm`, `toolbar-navigation`, `table-editing`,
    `code-blocks`, `theme-zoom`: 164/164 pass.
  - Groups `review-annotations`, `frontmatter-schema`, `frontmatter-editing`, `diagrams`,
    `lifecycle-sync`, `trust-security`: 85/85 pass.
  - With the HEAD versions of the 3 `src/` files: v66–v71 and palette-slash v28 pass, and v88
    fails.
- Playwright probes (scratchpad `insp226/probe*.py`) for the float size at 393, 600, 900, 1100,
  1200 and 1400 px, the table offset, raw `align` heading clear, and where the float ends.
- At the end, the worktree's `git status --porcelain` and `git diff` hash are identical to the
  start (`3c7255fb…`). `out/` was rendered again from the worktree sources. Nothing is left running.
