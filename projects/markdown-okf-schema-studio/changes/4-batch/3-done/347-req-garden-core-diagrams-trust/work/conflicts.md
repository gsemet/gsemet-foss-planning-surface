# CR-347 rebase conflicts

Rebase: `git rebase --onto origin/chantier/batch-06/cr-345-... 9d284eca`. Old head 46ef6780, new head 3766a40e. No commit skipped; the last three commits stay one per StRS (CORE-001, DIAG-001, DIAG-006), each touching one file.

## Stop 1: c2772e4a (use cases and reparenting)

- StRS DIAG-001 and DIAG-006, generated Links (Derived by): CR-347 removes the reparented SwRS (DIAG-121..127, REVIEW-017/038, TRUST-074/075) from the list; CR-345 had only grown it. Took the CR-347 side (empty), then `just requirements-update`.
- SwRS LIFE-026, `derives_from` and Links: CR-345 dropped LIFE-001 and LIFE-010, CR-347 drops TRUST-001. Result: LIFE-003 only.
- SwRS TRUST-065, `derives_from` and Links: CR-345 dropped FMEDIT-008 and REVIEW-015, CR-347 drops DIAG-009. Result: all three gone.

## Stop 2: 0040286 (merge, split and rewrite)

- StRS BLOCK-016, BLOCK-025, GFM-003, FMEDIT-008 and SwRS TOOLBAR-058/083/113/126 (generated Links): took the CR-345 side, then `just requirements-update` regenerated them from the frontmatter (TRUST-005 title is CR-347's "page messages", BLOCK-254 / FMSCHEMA-083 links come back where the frontmatter still holds them).
- SwRS LIFE-169, `depends_on`: CR-345 has TRUST-006 + 052 + 065, CR-347 replaces TRUST-006 by TRUST-005. Result: TRUST-005, 052, 065; Links regenerated.
- StRS TOOLBAR-001, `derived_by`: CR-345 removed TRUST-001, CR-347 adds TRUST-005. Result: TRUST-005 (TRUST-006 kept), no TRUST-001; Links regenerated.
- scripts/marker-baseline.json: CR-345 lowered pageStateMessages 9 to 5 and keeps hostToPage 5; CR-347 removes hostToPage. Result: hostToPage removed, pageStateMessages 5.

## Stop 3: acd1b16 (move markers onto code and tests)

- src/core/preview/styles commentStyles, contentBlockStyles, contentLayoutStyles, editModeStyles: CR-345 had re-sectioned the files and moved the markers; CR-347 had edited the old file head. Took the CR-345 structure, then applied CR-347's intent: removed from the source the marker lines now carried by the `.markers.ts` companions (CORE-008 in comment styles; CORE-028, 034, 022, 008, DIAG-001, 023, 032 in content block styles; CORE-028, 034 in content layout styles; DIAG-001 in edit mode styles).
- test/page/modules/editActions.test.ts: DIAG-017 marker moved from the file head into the mermaid test (CR-347), on top of CR-345's file head.
- test/integration/realInput/markers.ts: CR-345 left only DIAG-009 and StRS DIAG-001; CR-347 removes both. The companion would hold no marker, so it is deleted (`check-markers` asked for it; nothing imports it).
- scripts/marker-baseline.json: took the CR-345 side, then `node scripts/check-marker-companions.mjs --update` (3 entries lowered or removed: contentBlockStyles 5, html-sanitizer and realInput/markers removed, unnamedCompanionLines empty).

CRLF from okfreq converted back to LF in every resolved file; no BOM added.

## Gates (fast gate)

- `just requirements-lint`: 1156 requirements, 0 errors (26 warnings, as before), 0 files would change: pass.
- `just check-markers`: 9 companion files, 406 in-force SwRS marked, 30 baseline files: pass.
- `just check`: exit 0 (log: work/gates/rebase-check.log).
