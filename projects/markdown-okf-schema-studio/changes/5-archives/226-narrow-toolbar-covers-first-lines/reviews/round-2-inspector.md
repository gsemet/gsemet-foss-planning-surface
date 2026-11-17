# CR 226, round 2, Inspector review

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-226` (uncommitted diff on
HEAD `0b4ede78`). I read the constitution, `AGENTS.md`, `rules.md`, the behaviour note (gates 226,
226b and 226c) and the round-1 review first.

## Verdict: APPROVE

The approved behaviour holds. Text wraps around the toolbar, and boxes within its reach start below
it, centred. A 0-size float adds no gap. Pages with aligned floats keep the main layout. Headings
clear aligned floats as on main. The gates are green, the round-1 regressions pass again, and no
approved requirement was touched. The findings below are minor or nits; none blocks the merge.

## Findings

### 1. Minor: an opened comment panel runs under the toolbar

File: `src/core/preview/styles/contentLayoutStyles.ts:67`

`div.okf-comment` is in the "never moves" list, so a closed chip doesn't push text down, which is
correct. But an opened comment shows `.okf-comment-body` as an admonition-like panel, with a border,
an accent bar and a tint (`commentStyles.ts:78`), and that panel is not a block formatting context.

- Probe at 393 px: a comment opened right after the h1 spans 31..362 px from y 136 to 238. The float
  is 93 x 186.
- The panel's border and background run under the toolbar while its text wraps.
- A note in the same place clears the float. Two blocks that look alike behave differently.

Fix: exclude only closed comments, replacing `div.okf-comment` with
`div.okf-comment:not(:has(> .okf-comment-body:not([hidden])))`. Or, if the driver prefers, add the
opened comment panel to the LAYOUT-043 known issue about borders under the toolbar.

### 2. Minor (owner awareness): blockquotes and rules count as boxes

File: `src/core/preview/styles/contentLayoutStyles.ts:67`. SwRS LAYOUT-043 lists both.

A blockquote or `hr` isn't narrowed beside a float (neither is a BFC), but the selector still makes
it clear the float.

- Probe at 393 px: a blockquote right after the h1 starts at 186 px, while the h1 ends at 119 px.
  That leaves a blank band of about 50 px that wrapping would have avoided.
- For `hr` this is arguably better: the line no longer runs under the toolbar.

This is consistent with the briefing ("every other top-level block") and with the SwRS text. The
owner's gate 226b wording, though, named "tables, figures, code, notes, grids, diagrams,
block-editor frames".

Fix: either add `blockquote` to the text list (it wraps like a paragraph, and its left border is
away from the toolbar), or leave it as is and point the owner to the SwRS list when it is shown.

### 3. Nit: the "aligned" detector also matches elements that don't float

File: `src/core/preview/styles/contentLayoutStyles.ts:39`

- `table.align-left` and `table.align-right` (for example a MyST list-table with `:align: right`)
  have no float rule in the page CSS.
- `figure > img.align-left|right` is set to `float: none` (`src/core/directives/figure.ts:61-65`).

Either one turns the toolbar float off for the whole page. This is covered by the accepted known
issue 2 ("any aligned image, figure or table") and by the P3 backlog item for a precise rule. No
action needed now; mention these two cases in the backlog item.

### 4. Nit: an unverified claim in a LAYOUT-043 known issue

File: `requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-043.md:89`

"An image aligned with the HTML `align` attribute in a Markdown file loses the attribute when
rendered." The sanitizer allows `align` on every element (`src/core/security/html-sanitizer.ts:74`),
so the loss, if real, happens earlier in the pipeline. I did not verify it.

Fix: the coder confirms it with a one-line render, and names the cause or rewords it ("is not
covered by a visual test").

### 5. Nit: `contentTop` uses the column's border-box top

File: `src/page/modules/firstClearance.ts:81` and `:153`

The float starts at the content-box top, but `contentTop` is measured from the border-box top. The
two are equal only because the column's `padding-top` is 0 (`contentLayoutStyles.ts`, the
`#sphinx-myst-preview-content` padding `0 var(--gutter) …`). If that padding ever changes, the float
height will be off by it.

Fix (optional): add `parseFloat(style.paddingTop)` to `contentTop`, or add a comment.

## Review focus answers

### 1. CSS

**Which top-level children are text and which are boxes.** I parsed all 172 rendered visual pages
for the direct children of `#sphinx-myst-preview-content`, then checked the runtime-inserted
elements.

- **Text:** `p`, `h1`–`h6`, `ul`/`ol` (including `contains-task-list` and `myst-radio-group`) and
  `dl`.
- **Boxes:**
  - `table`, `div.myst-raw-html-table` and `pre`
  - `aside.admonition.*`, including GitHub alerts, and `details.dropdown`
  - `figure.*` (mermaid, plantuml, vega and numbered), `div.math-display`, `div.myst-grid`,
    `div.myst-card` and `div.myst-tab-set`
  - `div.myst-toctree`, `div.myst-directive.myst-unresolved` and `section.footnotes`
  - `blockquote`, `hr` and `details`
  - an image-only paragraph: the runtime marks it with `data-sphinx-preview-figure`. A README
    `<p align="center"><img></p>` opening becomes a box, so it gets no float and keeps its 40 px
    gap. I probed this.
- **Never moves:**
  - `div.okf-anchor-row` and `.sphinx-preview-insert-point` (both height 0)
  - `div.okf-comment` (see finding 1)
  - `[hidden]` blocks, and `.myst-toctree-hidden` (`display: none`)
  - the edited block (`[data-sphinx-preview-editing]` is `display: none !important`)
- The properties section has its own runtime exit.
- The selection status and the row-handle layer go to `body`, not to the column.
- I found no zero-height clearing element that would move the text after it down.

**The 0-size float adds no gap.** The column is `display: flow-root`, so the first child's 40 px
margin does not collapse through it, and a 0 x 0 float at y 0 never introduces clearance. The probe
confirms it: with a box first, the box is at 40 px. So do the first-gap scenarios v21, v24, v27 and
v46–v48 in the `layout-width` run. Beyond the toolbar's reach, `clear` is a no-op.

**Aligned floats.** The clear rule and the `::before` float are both gated on
`:not(:has(ALIGNED))` / `:has(ALIGNED)`, so a box can never clear an aligned float.

**The heading rule is equivalent to main.**

- Every float source in the page CSS is `figure.ts` (`img`/`figure` `.align-*`).
- Inline `style` is removed except on `span` (colours) and on tables (width and background only).
- The UA `align` floats (`img` and `table`) are covered by `[align=left|right i]`.
- The only gaps: `<input type="image" align>`, which is exotic, and a project stylesheet linked from
  the output root. Both are acceptable.
- CORE-028 (proposed) and MYST-031 (proposed) say "headings clear the float". That stays true.

**Performance.** There are three `:has()` rules on the root with the same argument. Chrome
invalidates them only when an `img`, `figure` or `table` is inserted or removed, or when a class or
`align` changes. Typing (`characterData`) does not invalidate them. v20 (huge document) passes
here.

### 2. Runtime

- `measureFloat` reads the toolbar's and column's rectangles, the first non-empty child's `clear`
  (CSS only) and whether its height is non-zero, and the `::before` display.
- The float can change the first child's height, but not from 0 to non-zero, so there is no
  self-dependence.
- Publishing the property mutates the root `style` and triggers "root attribute". The next update
  finds no change, so it does not settle again.
- Zoom scales `font-size`, not px, so the px float stays right.
- Edit transitions: when the first-block editor opens, the float goes to 0 (observed through the
  content mutation). A non-first editor clears the float, as approved; see the driver's
  `after-editor-900-cream.png`.
- The physical-side check is correct for the right-hand toolbar.

### 3. Tests

- v88, v89 and v90 assert geometry against live rectangles, with a 0.5 px or 2 px tolerance. They
  are not pixel diffs, so they are not brittle.
- v89 also asserts that a float is published, so it fails on HEAD.
- The unit setup extends the mock without changing any existing assertion, and the 6 new tests are
  meaningful.
- The e2eGroups count of 413 is 410 plus 3, and the message is extended accordingly.
- Markers: `@implements_req LAYOUT-043` is on the CSS (both files) and on `measureFloat`;
  `@tests_req` is on the unit tests and the 3 scenarios.
- **Requirements.** The SwRS text matches the probes: 31..362, 93 x 186 and the 40 px gap. It
  states both accepted known issues and the border-under-toolbar issue. Every touched requirement
  is `proposed`: the new LAYOUT-043, LAYOUT-011 (one known-issue sentence) and StRS LAYOUT-004 (the
  generated `derived_by` and links). The `index.md` and `log.md` changes are additions only.
  LAYOUT-007 and every approved requirement are untouched.

### 4. Visible behaviour beyond the approval

Nothing is strictly outside the approval. Two items are borderline, for owner awareness:

- the opened comment panel under the toolbar (finding 1)
- blockquotes pushed below the toolbar with a blank band (finding 2)

A centred text paragraph near the top now centres within its shortened lines. That is inherent to
wrapping.

## Commands run

- `npm run compile`, then `node --test out/test/page/modules/firstClearance.test.js`: 22/22 pass.
- `UV_NO_CONFIG=1 just check` (foreground): exit 0.
  - unit 3326/3326
  - security 71/71
  - pytest 153 passed
  - requirements 1073, 0 errors (21 warnings, existing)
- Visual: I held the lock `226` and released it.
  - `npm run visual:render`, then `capture.py --workers 1` with the group `layout-width` and
    `rendering-core/v20-huge-document-bottom-dark-900`, `palette-slash/v28-palette-clears-text-rule-cream-900`,
    `myst/v17-figure-width-align-anchor-full-light-900` and `myst/v20-myst-gallery-full-dark-900`:
    94/94 passed (v88, v89 and v90, v66–v71, the first-gap scenarios, v20 and v28 included).
- Playwright probes on the rendered 75-toolbar-float page at 393 px:
  - injected README centred logo, blockquote, `hr`, opened comment, and centred paragraph
  - scripts in the session scratchpad: `probe226.py` and `probe226b.py`
- Screenshots viewed: `after-narrow-toolbar-cream`, `after-table-900-cream` and
  `after-editor-900-cream`.
- The worktree's `git diff` and `git status --porcelain` hashes are identical at the start and the
  end. Nothing is left running.
