# Conflicts: rebase of CR-441 onto chantier/batch-07/cr-440-requirements-viewer-shows-table-scenario

Result: fddbb49b rebased to 13cb386b on top of 8d99cd1e. Base branch untouched, nothing pushed.

## Hunks

- `requirements/tiers/log.md` (2026-11-21): both entries kept, CR-440 first, then CR-441. No marker left.
- `requirements/tiers/swrs/rendering-core/SwRS-MDOKFSTUDIO-CORE-082.md` (Verification notes): one merged Method
  (CR-441's "a full ID is the text of every link to a requirement" test added to CR-440's tests and its table
  and mixed scenarios tests and bundle guard) and CR-440's Criteria (no card of the bundle is empty). The
  rest of the file auto-merged.
- `test/site/requirementsViewer/pages.test.ts`: both sides appended tests at the same spot. Kept CR-440's
  table-scenario test, then CR-441's two tests ("the line above the map ...", "a full ID is the text ..."),
  closing braces fixed.
- `pages.ts`, `viewer.css` auto-merged; their tests pass (gates below).

Files stay LF; no BOM added. `just requirements-update`: 0 indexes and 0 projections updated, tree clean after.

## Gates

- `just check`: exit 0 (existing W2 broken cross-link warnings only).
- `just requirements-report`: exit 0.
- `STUDIO_REQUIRE_CHROMIUM=1 STUDIO_REQUIRE_REQUIREMENTS_REPORT=1 npm run test:viewer-graph`: 4 pass, 0 fail.
