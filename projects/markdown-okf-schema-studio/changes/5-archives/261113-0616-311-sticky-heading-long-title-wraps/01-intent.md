# Backlog (P3): a long heading in the sticky section header wraps and covers the section start

Found while recording CR 170 short video S1 take 2 (2026-10-29), real VS Code window, Cream theme.

- Observation: with `markdownOkfSchemaStudio.preview.stickyHeadingDepth` = 1, a long H1 wraps to two lines
  in the sticky band at 130-160 % zoom. The taller band then covers the first line of the section below it.
- Code: `src/page/features/stickyHeadings.ts` builds the band label.
- Open question for the plan: keep the band to one line (ellipsis, full title on hover), or let the scroll
  offset follow the band height. Add a visual test either way.
- Out of scope: the `#` level markers in the band are intended. Requirement work on them goes under
  StRS-MDOKFSTUDIO-TOOLBAR-004 in the CR 170 plan.
- Acceptance: scroll `perf-analysis.md` (demo-video/s1-v2/workspace/ on branch
  `change-requests/170-demo-video-s-assets`) at 160 % zoom: the first line of each section stays visible.
