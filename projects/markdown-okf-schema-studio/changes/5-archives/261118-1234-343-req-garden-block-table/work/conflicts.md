# Conflicts: CR-343 rebased onto CR-346 (batch-06)

Rebase of `chantier/batch-06/cr-343-change-specification-garden-the-requirem` (abb5cd82, bcb958e7,
225e73b9, from origin/main ee592ea3) onto CR-346's branch at 69913b57. Result: 5cced9e4, 29ada256,
f9c37f6d (HEAD). Rule applied (spec, Coordination): each CR removes only its own scopes' lines; keep
both sides' removals and both sides' additions. No BOM added (the three resolved files start with
`{`, `//` and `#`, as before). Nothing committed by hand, nothing pushed.

## Commit 2 (bcb958e7, markers placed on the code)

### `test/integration/realInput/markers.ts`

- HEAD (CR-346) kept `// @tests_req StRS-MDOKFSTUDIO-BLOCK-001` and had removed
  `// @tests_req SwRS-MDOKFSTUDIO-TOOLBAR-077`; CR-343 removed the BLOCK-001 line and still had
  TOOLBAR-077.
- Choice: both removals, the hunk resolves to no line. The auto-merged removals (CR-343's
  StRS-TABLE-001/006/008/012/011, CR-346's StRS-TOOLBAR-013) stay.

### `scripts/marker-baseline.json`

- `blocks`, styles hunk: HEAD had contentBlockStyles 14, contentLayoutStyles 6, editModeStyles 12,
  pageChromeStyles 4 (propertiesStyles removed); CR-343 had contentBlockStyles 13, contentLayoutStyles
  11, pageChromeStyles 7, propertiesStyles 4 (editModeStyles removed). Choice: the lower value or the
  removal of each: contentBlockStyles 13, contentLayoutStyles 6, pageChromeStyles 4; editModeStyles and
  propertiesStyles removed.
- `blocks`, `test/integration/realInput/markers.ts`: HEAD 60, CR-343 28; and `unnamedCompanionLines`
  for the same file: HEAD 60, CR-343 28. Choice: 28, then `--update` lowered both to 24 (both sides'
  removals now apply to that file).
- `blocks`, editActions hunk: HEAD editActions.test.ts 43 (package-contract.test.ts removed); CR-343 36
  and package-contract 7. Choice: editActions 36, package-contract removed.
- Check: `node scripts/check-marker-companions.mjs --update` on the merged tree changed only the two
  `markers.ts` entries (28 to 24, "2 entries lowered or removed"); `node scripts/check-marker-companions.mjs`
  then passed: "5 companion file(s), 434 in-force SwRS marked, 46 files on the marker baseline".

## Commit 3 (225e73b9, use case diagrams and scenarios)

### `requirements/tiers/log.md`

- Both sides added a `###` entry at the top of `## 2026-11-17`: CR-346's "Garden the requirements of
  toolbar-navigation and lifecycle-sync (CR 346, round 1)" and CR-343's "Garden block-editing and
  table-editing".
- Choice: keep both, CR-346's first (it is already on the base), then CR-343's, one blank line between.
- After this commit, `check-marker-companions.mjs --update` reported 0 entries lowered or removed.

## Fast gates (run in the worktree after the rebase)

- `just requirements-lint`: exit 0; "1136 requirements, 0 errors, 27 warnings" (W2 broken
  cross-links in example text of GFM/PALETTE SwRS, outside this CR's scopes); 0 indexes and 0 OKF
  projections would change; coverage `--check` 0 files would change; main paths: 80 StRS checked,
  542 SwRS citations, all valid. Log: `work/gates/conflict-resolver-requirements-lint.log`.
- `just check`: exit 0 (tsc, min-vscode tsc, check-boundaries passed, check-limits passed,
  check-exports clean, check-markers passed with 46 baseline files, check-settings passed, unit tests,
  requirements lint). Log: `work/gates/conflict-resolver-check.log`.
