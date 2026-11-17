# Requirements gardening: audit synthesis (2026-11-17)

Read-only audit of the Studio okfreq bundle at main dedbdb2a, by seven sub-agents. Detailed reports, one per group of scopes, sit next to this file:

| Report | StRS | SwRS | High | Medium | Low |
| --- | ---: | ---: | ---: | ---: | ---: |
| audit-block-table.md | 14 | 86 | 11 | 44 | 16 |
| audit-review-frontmatter.md | 14 | 87 | 4 | ~30 | 9 |
| audit-palette-theme-layout.md | 13 | 106 | 3 | 27 | 13 |
| audit-toolbar-lifecycle.md | 16 | 93 | 4 | 60 | 45 |
| audit-core-diagrams-trust.md | 13 | 92 | 9 | 49 | 10 |
| audit-myst-code-gfm.md | 10 | 52 | 8 | ~30 | ~16 |
| **Total** | **80** | ~475 (overlaps) | **39** | **~240** | **~109** |

audit-crosscutting.md covers missing StRS, diagrams on the site, and deleting retired requirements.

## Systemic findings

1. **Markers are links but often not in the right place.**
   - Implementation markers are piled on file headers, big CSS constants and shared functions. Examples: `editPalette.ts:23-39` (17 IDs), `contentBlockStyles.ts:6-16`, `pageChromeStyles.ts:146-151`, `contentLayoutStyles.ts:82-90`, and module installers.
   - Test markers sit in header blocks rather than on the test. Examples: `editActions.test.ts:9-48` (40 IDs), `okfFrontmatter.test.ts:29-43` (15 IDs for 63 tests), and the companion file `test/integration/realInput/markers.ts:4-65` (39 IDs, attached to no scenario).
   - Many real tests cited in "Verification notes" carry no marker.
   - A few markers sit on the wrong test: TABLE-013, PALETTE-264, MYST-081, and four in myst/code/gfm.
2. **Wrong parents.**
   - Shared rules are derived by many StRS instead of cited with `depends_on`. LIFE-169 and LIFE-170 are derived by 9 and 10 StRS; LIFE-026, LIFE-049, LIFE-069, TRUST-005, TRUST-065, BLOCK-041 and BLOCK-058 do the same.
   - SwRS hang under an unrelated StRS: 34 in core/diagrams/trust alone. Examples: BLOCK-257/258 under BLOCK-001, LIFE-172 under LIFE-014, TRUST-001 under TOOLBAR-001, MYST-019/097 under MYST-005.
3. **StRS text contradicts its SwRS or the code.** Six of these StRS are approved, so they need the owner's re-approval:
   - CODE-001 (theme, line numbers);
   - GFM-002 (approved, colours);
   - DIAG-007 (one JAR process per diagram; the cap is 2);
   - TABLE-008 (five buttons; there are seven);
   - REVIEW-012 (approved, TODO shortcut);
   - BLOCK-025 (approved, CRLF issue already fixed);
   - PALETTE-001 (TODO shortcut, Full mode);
   - CORE-002 (editing from an include location has no SwRS);
   - GFM-029 versus CORE-071 (two raw HTML subsets);
   - TOOLBAR-011 (outside-link setting).
4. **Granularity.**
   - Message-validation SwRS that no user can observe should be folded into the behaviour they guard: BLOCK-236..245, 8 in REVIEW, and TOOLBAR-056/058/083/113/122/126.
   - Scenarios written as separate SwRS should be merged: TABLE-003..005 into TABLE-055, and TABLE-070/073/074/076/080.
   - Some SwRS should be split: TABLE-035, GFM-039, MYST-024, and 7 in core.
   - Proposed mappings take the in-force SwRS from about 475 to about 400. Each mapping is in its report.
5. **Use cases with no StRS of their own (6):**
   - Vega charts and SVG (DIAG-121..127, today under the Mermaid StRS);
   - radio choices in plans (GFM-039);
   - the writing skill and agent plugin (CORE-073..075);
   - the published site and requirements viewer (CORE-069, CORE-080..086, today under TRUST-014);
   - the release gate (CORE-076, CORE-078);
   - the side-by-side diff (REVIEW-005..010).

   Umbrella StRS should be split: PALETTE-001 (53 SwRS, into formatting, GFM and MyST), CORE-001, DIAG-001 and MYST-001.
6. **StRS validation tests.**
   - About 12 StRS have none: for example LIFE-021, TOOLBAR-002, TOOLBAR-003, TOOLBAR-014, MYST-006, and five in core/diagrams/trust.
   - About 10 rely only on the companion file. TABLE-011 and TABLE-012 have no real-window scenario at all.
   - The reports name the integration scenarios that can carry these markers.
7. **Scenarios not checked by any test.**
   - About 17 in toolbar/lifecycle alone: LIFE-038, LIFE-039, LIFE-044, LIFE-069, LIFE-119, LIFE-127, LIFE-169, TOOLBAR-058, TOOLBAR-077, TOOLBAR-094, and others.
   - GFM-021's host refusal paths.
   - MYST-024's refusals: the tests exist but carry no marker.
8. **Defects found on the way.**
   - DIAG-128 has no implementation marker: its code, `exportSnapshot.ts:84`, carries TOOLBAR-137, and no gate requires a source marker on a non-exempt SwRS.
   - The PlantUML JAR test (`diagReq.jar.requirements.test.ts:104`) passes only through the 30-second timeout.
   - A stale `@tests_req LAYOUT-021` remains at `diagReq.viewState.requirements.test.ts:107`.
9. **Lifecycle.** StRS TOOLBAR-002 and TOOLBAR-003 and 10 TOOLBAR SwRS are `draft` but implemented and tested. They are candidates for `proposed`.
10. **Verbosity.** 4 StRS are over 1000 words (core/diagrams/trust).

## Diagrams on the GitHub Pages site

- A use-case page renders only the title, `user_need`, the map from `### Main paths` and the behaviour list (`test/site/requirementsViewer/pages.ts:92-97`).
- Recommendation: an authored `### Use case diagram` section holding a Mermaid fence, placed before Main paths.
  - GitHub renders the fence natively, and plain OKF readers see text.
  - okfreq validates it with 0 errors.
  - The site pre-renders it to inline SVG at build time, with the Chromium and mermaid already in the repo (the pattern of `socialCard.ts:130`). That is about 80-120 lines plus a test.
- PlantUML is ruled out: GitHub does not render it.

## Deleting retired requirements

- 569 files: 61 deprecated and 508 superseded.
- In-force files cite them only in generated fields. One stale marker remains.
- Simulated deletion on a copy, after `update-coverage` and `lint`:
  - deprecated only: 0 errors, 1063 requirements remain;
  - all retired: 0 errors, 555 requirements remain;
  - both `--check` runs are clean.
- `okfreq retire` refuses non-draft requirements. The procedure is:
  1. a project-guideline exception to the shared "never delete a published requirement" rule;
  2. `git rm`;
  3. append the IDs to `retired_ids`;
  4. one `log.md` entry with the old-to-new mapping;
  5. `just requirements-update`, then preflight.
- Costs:
  - the viewer's retired rows and History view go empty, so they should be removed or adapted;
  - open PRs touching requirements may conflict on rebase.
- ISO/IEC/IEEE 29148 asks for unique, never-reused IDs, a consistent set and baselines under configuration management. `retired_ids`, git tags and the log satisfy those without keeping the files.

## Proposed change requests (order)

1. **Delete retired requirements.** Guideline exception, `retired_ids`, log mapping, stale marker, viewer retired rows.
2. **Use-case diagrams on the site.** Section rule in `project.guidelines.md`, Mermaid pre-rendering in the viewer.
3. **Marker gate.** Fail when a non-exempt SwRS has no implementation marker, and limit marker blocks (no header or companion lists).
4. **Six restructure CRs, one per audit group.** They depend on 1-3 and each covers:
   - StRS text fixes (with re-approval where approved);
   - new and split StRS;
   - reparenting with `depends_on`;
   - SwRS merges and splits by `okfreq supersede`, then deleted under the new rule;
   - markers moved onto the code and tests;
   - StRS validation tests;
   - the missing scenario tests;
   - one diagram per StRS.
