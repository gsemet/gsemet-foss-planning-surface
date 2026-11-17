# Requirements baseline: test and marker quality follow-ups

Triage (2026-10-25, autonomous, user asked to triage without technical questions): P3.

Current behaviour is specified as-is with "Known issue" in the SwRS listed below (PR #62 baseline).
The fix updates those SwRS in the same change.

From the PR #62 audit (CR folder gap-report.md and reviews/completeness.md).

- Browser tests for the Mermaid and PlantUML entry points: DIAG-012, 013, 014, 031, 116 (the only
  SwRS without a test marker).
- About 40 tests approximate their requirement (CSS text instead of computed layout, fake host
  events, source scans): replace with behavioural tests over time.
- Coarse markers on style modules and integration run() functions (e.g. GFM-022, FMSCHEMA-063,
  BLOCK-251, LAYOUT-007/008, THEME-025/037, TOOLBAR-034).
- 92 StRS have no end-to-end test; a check script for the *.markers.ts companion files; remove each
  *.markers.ts when its source file is split.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
