# Requirements baseline: remaining test and marker quality work

Triage (2026-10-26, autonomous): P3. Remainder of `requirements-test-quality` after CR 103
(page tests for the Mermaid entry point, a visual scenario for the PlantUML bundled theme and
sprite, `just check-markers`, narrower markers for LAYOUT-007 and THEME-025).

- About 40 tests approximate their requirement (CSS text instead of computed layout, fake host
  events, source scans): replace with behavioural tests over time.
- Coarse markers that remain: `run()` of `test/integration/previewEditing.test.ts` carries about
  ten requirements (FMSCHEMA-063, -067, -073, TOOLBAR-120, ...); move each marker to the narrowest
  step once the run is split into one test per behaviour. The ids GFM-022, LAYOUT-008, BLOCK-251,
  THEME-037 and TOOLBAR-034 of the audit no longer exist (superseded or renumbered): re-audit
  other style modules (`pageChromeStyles.ts` still carries THEME-031, TOOLBAR-001 at file top)
  by splitting the CSS into one constant per requirement, as done for LAYOUT-007.
- 92 StRS have no end-to-end test.
- Remove each `*.markers.ts` when its host file is split (`realInput.test.ts` first); the
  `check-markers` script already reports a companion whose host is gone.
- The guards for a late Mermaid result (`drawnKeys` check in `mermaidPreview.ts`) are unreachable
  behind the serial draw queue; decide whether to keep or remove them.
