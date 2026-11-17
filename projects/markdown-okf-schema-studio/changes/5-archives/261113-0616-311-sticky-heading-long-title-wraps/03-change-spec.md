# Change Specification: a long heading in the sticky band stays on one line

Short specification (triage: automatable). Code read at `origin/main` `cb968299` (version 1.7.1).
Rules: [constitution](../../../../constitution.md), [AGENTS.md](../../../../../AGENTS.md) and the
requirements guidelines it links to.

## Goal

When a heading is too long for the sticky heading band, the band no longer wraps it onto a second
line. Each heading level stays on one line, cut with an ellipsis (`…`), so the band is never taller
than the configured depth and never covers the first line of the section under it (seen at 130 to
160 % zoom with `markdownOkfSchemaStudio.preview.stickyHeadingDepth` = 1).

## Decisions carried from `02-answers.md`

1. One line per heading level, cut with an ellipsis. CSS only: `white-space: pre;
   overflow: hidden; text-overflow: ellipsis;` on the band. This reverses SwRS TOOLBAR-025 "wrapping a
   long heading path onto more lines", its scenario "Long heading path wraps" and visual scenario v05;
   all three are updated (owner, USER-IMPACT answer).
2. No full title on hover. The band keeps `pointer-events: none` (TOOLBAR-025 scenario "Pointer"
   unchanged). The full title stays readable in the heading itself and in the table of contents.
3. The band stays one text node with one line per level joined by `\n`
   (`src/page/features/stickyHeadings.ts` is not changed); `text-overflow` cuts each line of a `pre`
   block, so every test that reads the band text keeps working.
4. TOOLBAR-025 changes in the same change; TOOLBAR-030 (reading offset) is unchanged: its allowance is
   already `depth` lines (`anchorPolicy.readingOffset(depth, lineHeight, 5)`), which is what the band
   now always is.
5. New visual test with its own fixture (not the demo branch file `perf-analysis.md`): depth 1, a long
   H1, 160 % zoom, Cream.
6. Every assertion that changes is named in the PR with the reason (constitution, section 3).

## What changes

### Style: `src/core/preview/styles/pageChromeStyles.ts`

In the `[data-sphinx-preview-sticky-headings]` rule (around line 561), replace
`white-space: pre-wrap; overflow-wrap: anywhere;` with
`white-space: pre; overflow: hidden; text-overflow: ellipsis;`. Keep everything else (position,
padding that ends the text before the toolbar, `pointer-events: none`, the `[data-scrolled-under]`
shadow). Update the comment above the rule if it mentions wrapping.

### Unit test: `test/core/preview/previewStyles.test.ts`

Lines 74-75 assert `white-space: pre-wrap;` and `overflow-wrap: anywhere;` on the band. Replace them
with assertions of `white-space: pre;`, `overflow: hidden;` and `text-overflow: ellipsis;` in the band
rule, and an assertion that the band rule has no `overflow-wrap: anywhere`. Keep the
`@tests_req SwRS-MDOKFSTUDIO-TOOLBAR-025` marker.

### Visual checks: `test/visual/capture_final_checks.py`, `check_sticky_headings`

- Read `textOverflow` and `overflow` from the computed style, and whether the band text is cut
  (`element.scrollWidth > element.clientWidth`).
- For every sticky scenario: the rendered line count (`textLineCount`) equals the number of heading
  levels shown, and the height check (rendered lines times line height plus padding and border,
  within 2 px) stays.
- Replace the `expectStickyGrowth` branch ("long sticky headings did not expand beyond one line per
  heading level") with an `expectStickyEllipsis` branch: white-space `pre`, text-overflow `ellipsis`,
  the text is cut, and one rendered line per level.
- New check `expectSectionStartVisible` (or a part of the ellipsis branch): the first block after the
  active heading has its top at or below the band's bottom (within 1 px), so the first line of the
  section is not covered.

### Visual scenarios: `test/visual/scenarioDefinitions2.ts`, `scenarios.ts`, `scenarioIds.ts`

- `scenarios.ts`: rename the option `expectStickyGrowth` to `expectStickyEllipsis` (and add
  `expectSectionStartVisible` if it is a separate flag), with a doc comment.
- v05 (`preview-sticky-headings-natural-growth`, fixture `10-sticky-heading-wrap`, depth 3, dark,
  460 px): keep the scenario and its permanent number v05; it now proves the ellipsis. Set
  `expectStickyEllipsis: true`, keep `expectedStickyHeadings` (the full text: the text node is not
  cut, only its drawing), update `description`. In `scenarioIds.ts` change its slug to
  `toolbar-navigation/v05-sticky-long-path-ellipsis-dark-460` and rewrite its gallery sentence (line
  423) to: at 460 px each long heading level stays on one line cut with an ellipsis, the band is three
  lines tall and the document flow does not shift. Update the fixture's sentence "The sticky heading
  band must expand to show every wrapped line without clipping its content." to say the band keeps
  one line per level.
- New scenario, final id written directly (next free number of the group at implementation time;
  `v44` on `origin/main` today, unless another CR of the stack took it):
  `toolbar-navigation/v44-sticky-long-title-zoom-160-cream-900`. Fixture: a new
  `test/visual/fixtures/NN-sticky-long-title.md` (next free fixture number; `88` on `origin/main`
  today) with a long H1 that cannot fit one line at 160 % in a 900 px pane, several sections, and a
  following H1 far enough down to scroll. Options: `previewThemeMode: "cream"`,
  `stickyHeadingDepth: 1`, `render: { zoom: 160 }`, `...WIDE`,
  `scroll: { kind: "stickyHeading", value: <the long H1's selector> }`, `expectedStickyHeadings` set
  to `# <full title>`, `expectStickyEllipsis: true`, the section-start check on. Markers:
  `@tests_req SwRS-MDOKFSTUDIO-TOOLBAR-025`. Gallery sentence: at 160 % zoom in Cream, depth 1, a
  long title stays on one line with an ellipsis and the first line of the section is visible under
  the band.
- Visual baselines are generated, not committed: regenerate with the visual target and look at v05
  and the new scenario.

### Requirements

- `requirements/tiers/swrs/toolbar-navigation/SwRS-MDOKFSTUDIO-TOOLBAR-025.md`:
  - Normative sentence and `description`: replace "wrapping a long heading path onto more lines" with
    "keeping each heading level on one line, cut with an ellipsis when it is too long".
  - Scenario "Band grows" (one to three lines) stays.
  - Replace scenario "Long heading path wraps" with "(boundary): Long heading cut with an
    ellipsis": GIVEN a 460 px pane and long headings at depth 3, WHEN the band is measured, THEN it
    shows three rendered lines, each ended by an ellipsis where the heading does not fit, its height
    equals three lines and the document flow does not shift; and GIVEN depth 1, a long H1 at 160 %
    zoom, THEN the band is one line and the first line of the section is below the band.
  - Verification notes and Criteria: `white-space pre`, `overflow hidden`, `text-overflow ellipsis`,
    rendered lines = levels shown; the visual method names v05 with its new slug and the new
    scenario; `tested_in_files` unchanged (the fixture is not a test file).
  - "Pointer" scenario unchanged.
- `requirements/tiers/strs/toolbar-navigation/StRS-MDOKFSTUDIO-TOOLBAR-004.md`, "Rationale and
  constraints": "wraps in a narrow pane" becomes "keeps each level on one line, cut with an ellipsis".
- TOOLBAR-030 unchanged.
- Run `just requirements-update` (indexes, links) and add a dated entry in
  `requirements/tiers/log.md`: TOOLBAR-025 amended (one line per level with an ellipsis instead of
  wrapping; scenario replaced; v05 reworded, new visual scenario), StRS TOOLBAR-004 rationale line.

### Changelog

One line under `## Unreleased` in `CHANGELOG.md`, user terms: a long heading in the sticky band
stays on one line, cut with an ellipsis, and no longer covers the first line of the section below.

### Commit

Type `fix(render)` (allowed scopes in `.agents/guidelines/git-commit-allowed-scopes.md`). The PR body
lists each changed assertion and why: `previewStyles.test.ts` lines 74-75, the `expectStickyGrowth`
check, v05 and TOOLBAR-025.

## Out of scope

- The `#` level markers in the band (intended; StRS TOOLBAR-004 work belongs to CR 170).
- A tooltip or any pointer interaction on the band.
- Moving the scroll offset with a taller band; any change to `stickyHeadings.ts`,
  `refreshReadingOffset` or TOOLBAR-030.
- Right-to-left headings: the ellipsis side follows the CSS `direction`; no RTL test is added.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/`: no rendered syntax changes.
- The demo branch file `perf-analysis.md` (`change-requests/170-demo-video-s-assets`).

## Evidence

- `just check` passes (unit test of the band style).
- The visual run passes with v01 to v04 unchanged, v05 showing three one-line levels with
  ellipses, and the new 160 % Cream scenario showing one line and the section's first line visible.
- `just requirements-lint` and `just requirements-update` leave no diff after the commit.
- `just preflight` passes (completion gate).
- Scenario steps (manual check, optional, real window): set the depth to 1, zoom the preview to
  160 %, open a document with a long H1, scroll into its section: the band is one line ending with
  `…`, and the first line of the section is visible under it; a click on the band reaches the text
  below.

## Open questions

None.
