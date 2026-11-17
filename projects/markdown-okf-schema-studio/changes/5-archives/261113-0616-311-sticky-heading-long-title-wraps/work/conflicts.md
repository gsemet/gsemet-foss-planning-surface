# CR-311 restack conflicts

Rebase onto chantier/batch-02/cr-310-change-specification-export-to-html-keep. Conflicts on commit 1 only.

- CHANGELOG.md: kept both entries (CR-310 line first, then CR-311).
- requirements/tiers/log.md: kept both sections (CR-310 then CR-311).
- test/visual/scenarioIds.ts: kept both new ids. The CR-311 id was renumbered from
  `toolbar-navigation/v44-sticky-long-title-zoom-160-cream-900` to `v45-...`, because CR-310 already
  uses v44 in that group (updated in stickyLongTitleScenarios.ts, scenarioIds.ts, SwRS-TOOLBAR-025, log.md).
- test/site/e2eGroups.test.ts: base text kept, count set to 475, "plus 1 sticky long title scenario (CR 311)" appended.
- Generated requirements indexes: `just requirements-update` changed nothing.

Result: `just check` passes. Not pushed.
