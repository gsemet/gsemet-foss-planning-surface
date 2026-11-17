# CR 226, round 3, Inspector review

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-226` (uncommitted diff on
`origin/main` `0b4ede78`). Scope: the three round-3 edits that answer round-2 findings 1, 4 and 5,
the coherence of SwRS-MDOKFSTUDIO-LAYOUT-043 as a whole, and a check that nothing else moved.

## Verdict: APPROVE

The round-3 edits are accurate and complete. LAYOUT-043 reads as one coherent requirement. The CSS
is the one round 2 reviewed. Every gate is green.

## Round-3 edits

### Finding 1: the opened comment panel is a known issue

`SwRS-MDOKFSTUDIO-LAYOUT-043.md`, Known issues, item 5. It is accurate:

- `div.okf-comment` is still in the "never moves" list
  (`src/core/preview/styles/contentLayoutStyles.ts`, the `clear: right` selector).
- The opened `.okf-comment-body` is an inline panel, not a block formatting context
  (`commentStyles.ts:78`). Its text therefore wraps while its border and tint run under the toolbar,
  which matches the round-2 probe.
- It agrees with the normative bullet ("comment chips ... never move") and with known issue 1 (the
  h1 rule under the toolbar).
- The rationale, "opening a comment never moves the page", is a sound reason to document the issue
  rather than change the CSS.

### Finding 4: the image-align known issue is reworded

Known issues, item 6. Verified:

- `src/core/render/mystRawHtml.ts:40` has `ALIGN_TAGS = div, p, center, hr, h1–h6`.
- `:144` keeps `align` only for those tags, so `<img align>` in raw Markdown HTML loses it before
  the sanitizer runs.
- Tables keep `align` through the table path (`mystTables.ts` / `applyTableAlignments`). v90, which
  uses raw `align` tables, passed in round 2.
- The claim and the consequence ("covered by the CSS only, not by a visual test") are both correct.

### Finding 5: the comment on the column's top padding

`src/page/modules/firstClearance.ts`, in `geometry()`: "The column's top padding is 0
(contentLayoutStyles.ts), so its top is the content top." Verified: the column padding is
`0 var(--sphinx-preview-content-gutter) …` (`contentLayoutStyles.ts:298`). The comment is accurate.

## LAYOUT-043 as a whole

- **Lifecycle:** `req_lifecycle: proposed`, and `derives_from: StRS-MDOKFSTUDIO-LAYOUT-004`.
- **Normative text:** the description and the body match. The text, box and never-moves lists match
  the CSS selector. One small asymmetry: the CSS also leaves `[data-okf-folded]` blocks in place,
  and the SwRS covers them as "folded blocks".
- **Scenarios:**
  - The nominal 393 px numbers (93 x 186) and the document-coordinate table are consistent with
    `measureFloat`: width = right − bar.left + 8, height = bar.bottom + 8 − contentTop.
  - The boundary "No float" table covers both owner-accepted cases: a first block that is a box, and
    any aligned image, figure or table.
- **Known issues:**
  1. The h1 rule runs under the toolbar.
  2. A blank band appears above a box.
  3. A first block that is a box gets no float (owner-accepted).
  4. Any aligned image, figure or table means no float on the whole page (owner-accepted). It names
     the backlog follow-up.
  5. The opened comment panel (new).
  6. The image `align` attribute (reworded).

  None contradicts the normative text or another issue.
- **Verification notes:** the unit tests and v88, v89 and v90 are still named correctly.

## Touched requirements

| File | Change | Lifecycle |
| --- | --- | --- |
| `swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-043.md` | new | proposed |
| `swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-011.md` | one known-issue sentence | proposed |
| `strs/layout-width/StRS-MDOKFSTUDIO-LAYOUT-004.md` | generated `derived_by` and link | proposed |
| `swrs/layout-width/index.md`, `log.md` | additions only | n/a |

No approved requirement is touched.

## Nothing else changed since round 2

- The file list is the one round 2 reviewed: 11 modified files and 4 untracked ones. The diffstat is
  230 insertions and 17 deletions.
- The CSS in `contentLayoutStyles.ts` and `contentBlockStyles.ts` is identical to what round 2
  describes:
  - the `ALIGNED_FLOAT` selector, with `[align=left|right i]`
  - the `::before` float, with `pointer-events: none`
  - the `clear: right` exclusion list, including `div.okf-comment` and `[data-okf-folded]`
  - the `:has(ALIGNED)::before { display: none }`
  - the gated heading `clear: both`
- `firstClearance.ts` differs from the round-2 reading only by the new comment line.

## Findings

None blocking. Round-2 findings 2 (blockquote and `hr` treated as boxes) and 3 (the aligned detector
over-matching, now in the P3 backlog item) stay open for the owner and the backlog, as decided.

## Commands run

- `npm run compile`: exit 0.
- `node --import ./scripts/register-myst-patches.mjs --test out/test/page/modules/firstClearance.test.js`:
  22/22 pass.
- `UV_NO_CONFIG=1 just check` (foreground): exit 0.
  - unit 3326/3326
  - security 71/71
  - pytest 153 passed
  - requirements: 1073, 0 errors, 21 warnings (existing)
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`: exit 0.
  - 1073 requirements, 0 errors, 21 warnings.
  - The warnings are existing ones, for example the `url` placeholders in PALETTE-264. None concerns
    LAYOUT.
- The worktree state hash (`git diff` plus untracked contents) is identical before and after:
  `2bf54184…`. Nothing is left running, and no visual run was made.
