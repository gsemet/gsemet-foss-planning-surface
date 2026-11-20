## Summary

The requirements of the command palette and slash menu, of the theme and zoom controls and of the layout and
content width were a mix of overlapping, duplicated and stale items. This change gardens them: one umbrella
user need is split into three readable ones, near-duplicate software requirements are merged, requirements are
attached to the user need they serve, each user need gets a use case diagram, and the validation markers and
unit tests follow the new structure. No product behaviour changes. Published requirements are never deleted: a
merged requirement is superseded by `okfreq supersede` and stays readable.

## Deliverables

The user need "A writer inserts and formats Markdown from the palette" (palette-001) is replaced by three needs, and
the software requirements that repeated one rule in many places are folded into one each:

| Before | After |
| --- | --- |
| StRS PALETTE-001 (umbrella) | StRS PALETTE-019 (formatting buttons and shortcuts), 020 (GitHub Flavored Markdown constructs), 021 (MyST constructs); 001 is superseded |
| SwRS PALETTE-045, 048, 135, 138, 126 | SwRS PALETTE-276, inline marker buttons toggle their markers |
| SwRS PALETTE-049, 052, 053, 123, 267 | SwRS PALETTE-277, line-prefix buttons toggle their prefix |
| SwRS PALETTE-265, 273, 274 | SwRS PALETTE-278 (starter blocks) and PALETTE-001 (mode membership) |
| SwRS PALETTE-130, 137; 268 | SwRS PALETTE-127; PALETTE-238 |
| SwRS PALETTE-010, THEME-013 | SwRS LIFE-169 (shared lifecycle rule, cited through `depends_on`) |
| SwRS LAYOUT-018 | SwRS LAYOUT-011 |
| rule icon in PALETTE-002; scroll-follow row of PALETTE-021 | new SwRS PALETTE-280 and PALETTE-279 |

Each of the 15 in-force user needs of the three areas now has a `### Use case diagram` (one Mermaid fence before
Main paths); the requirements viewer already draws them.

## Blast radius

Grade: **1**. Requirement text, markers and tests only; `git revert` restores the previous state. The one risk is a
marker moved to the wrong requirement, which `just check-markers` and the requirements lint check.

## Autonomous decisions

- The three-way split of the palette need (formatting, GFM, MyST) and the new IDs follow the specification; the
  placement of shared rules between the sibling gardening changes was settled here (the foreign-ID marker blocks in
  `webview.ts`, `blockSourceEditor.ts` and the `editActions.test.ts` header are left to them).
- StRS THEME-004 carries its validation marker inline on one assertion, because a block marker would push the test
  file over its size baseline.
- The width scenarios that need a layout engine (rendered column at `maxContentWidth` 0) are covered by visuals, not
  unit tests; the SwRS verification notes say so.

## Known gaps

- SwRS PALETTE-114's parent moved to StRS REVIEW-015 (only generated `derived_by` links change; no re-approval). Owner
  to confirm.
- Open point for the owner: superseding PALETTE-001 dropped the "write a link" path from the old need's Main paths; it
  stays covered by StRS PALETTE-007, which already had two paths.
- The rendered column at `maxContentWidth` 0 and the content-patch, image-load and TOC-toggle triggers of the
  LAYOUT-023 re-measure are by inspection or visual only (resize and toolbar collapse are unit tested).
- The site build was not run in CI: the gallery job was skipped in the on-demand heavy run although requested, so
  the requirements site's drawing of the new use case diagrams was not checked there.
- `requirements/tiers/log.md` says SwRS PALETTE-039 and 052 keep StRS PALETTE-015 as a parent; 052 is superseded by
  this change, so only 039 is in force. A wording slip in the changelog, no requirement is affected.

<details>
<summary>Details</summary>

## Changes

- Added (proposed): StRS PALETTE-019, 020, 021; SwRS PALETTE-276, 277, 278, 279, 280.
- Superseded, none deleted: StRS PALETTE-001; SwRS PALETTE-045, 048, 135, 138, 126, 049, 052, 053, 123, 267, 265,
  273, 274, 130, 137, 268, 010; THEME-013; LAYOUT-018 (targets in the table above).
- Approved needs changed with the owner's agreement: StRS LAYOUT-001 (maintainer half of the need and tooling bullets
  dropped), LAYOUT-003 (rationale trimmed to 7 reader-level bullets), PALETTE-015 (diagram). Their `approved_by` and
  `approved_at` are set again, recording the owner's agreement. Each correction is its own commit, for the owner's
  review: LAYOUT-001 in c145e649, LAYOUT-003 in 0240436a, PALETTE-015 in 9e210e0a.
- The use case diagrams of StRS PALETTE-007, 013, 018, 019, 020 and 021 name their text box participant `Field`,
  not `Box`: Mermaid 12 reserves the `box` keyword, so those diagrams did not parse.
- Text changed in place: StRS PALETTE-002, 005, 018, LAYOUT-004, THEME-002; SwRS PALETTE-001, 002, 021, 127, 238, 275,
  LAYOUT-001, 011, 022, 023, 044, THEME-001, 034, LIFE-169; verification notes of LAYOUT-002, THEME-016, THEME-043.
- Reparented: the SwRS derived from PALETTE-001 now derive from 019, 020, 021 or the need they belong to; PALETTE-114
  to REVIEW-015; PALETTE-275 to PALETTE-015. Other software requirements only drop a palette or theme parent and keep
  their other parents: TABLE-085 (PALETTE-015), TABLE-111 (PALETTE-001), CORE-028 (THEME-002), TRUST-001
  (PALETTE-002), TRUST-005 and TRUST-065 (PALETTE-007 and 013), TRUST-006 (THEME-011), PALETTE-192, 196 and 203
  (PALETTE-013). LIFE-169 and LIFE-170 are cited by StRS LAYOUT-003, PALETTE-002, THEME-004, THEME-011.
- Sources with markers: `inlineEditActions.ts` (276), `blockEditActions.ts` (277, 278), `scrollSync.ts` and
  `blockEdits.ts` (279), `paletteIcons.ts` (280), plus the `*.markers.ts` companions in `src/core/preview/styles/`.
- Tests: new `test/core/preview/layoutThemeStyles.test.ts` and `test/page/widthModeScenarios.test.ts`; added cases in
  `previewConfiguration.test.ts`, `firstClearance.test.ts`, `runtimePageControls.test.ts`; StRS validation markers
  placed in `editToolbarCover.test.ts`, `lifecycle.test.ts`, `realInput/textEditing.ts`, `realInput/markers.ts`,
  `reload-suite.ts`, `scenarioDefinitions2.ts`. Existing tests for LAYOUT-032, PALETTE-256 and LIFE-169 are kept.
- `requirements/tiers/log.md` lists every ID added, superseded and changed.

## Human decisions

- Published requirements are never deleted; merges and splits use supersede or archive.
- Approved needs whose text changes (LAYOUT-001, LAYOUT-003) and the diagram added to PALETTE-015 were agreed in
  advance, to be reviewed on this PR; generated links and an added diagram need no new approval.
- A main path may cite a shared software requirement that the need lists in `depends_on`.

## Impacts

No visual change; requirements pages read better (shorter needs, one use case diagram each).

## Test plan

- [x] No behaviour change: the new unit tests listed above pin today's behaviour to its requirements
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: No user-facing change
- [x] Local gates at `c3b9802`: `just check` and `just preflight` pass (on Windows, its static stage)
- [x] Review: approved at `c3b9802` (the changelog correction on top of the patch approved before)
- [x] Verified at `c3b9802`; the requirements site's drawing of the diagrams is UNVERIFIED (see Known gaps)
- [x] CI green at `c3b9802`, with the real VS Code integration and stress jobs in an on-demand run

## Internal references

CR-345 req-garden-palette-theme-layout, batch-06; sibling gardening changes req-garden-*.

</details>
