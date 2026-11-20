# Verify CR-340 marker-gate

Head: 10c92335922923f749209f2f888dc9224803cdc4

All claims judged at 10c92335922923f749209f2f888dc9224803cdc4 (worktree clean before and after).

1. Unit test (`node node_modules/typescript/bin/tsc -p .` then `node --test out/test/build/checkMarkers.test.js`): 6 pass, 0 fail
   (rule 1; rule 2; rule 3; rule 3 + 2 named companion escapes cap / one unnamed line brings it back; ratchet blocks; ratchet unnamed lines).
   Not made by the old script: with `scripts/check-marker-companions.mjs` replaced by the origin/main version, the same run gave `pass 0, fail 6`
   (restored with `git checkout`). Caveat: the old script lacks `--root`, so part of that failure is the option, not the rules.
2. `just check-markers` at head: `check-markers: 5 companion file(s), 468 in-force SwRS marked, 60 files on the marker baseline`, exit 0.
   Added `src/core/probeScratch.ts` with 4 markers above a declaration: `src/core/probeScratch.ts:1-4: a marker block names 4 requirement IDs (at most 3) ...`, exit 1; file removed.
   Removed the name of the last line of `requirementsViewer.markers.ts` (CORE-085): 2 problems (`:5-11 names 7 IDs`, `:11 a companion marker names its scenario or code point after " — "`), exit 1; reverted with `git checkout`; check passes again.
3. `just requirements-update`: 0 indexes / 0 projections updated, worktree stays clean (committed update is current). `just requirements-lint`: `0 files would change`, main paths valid.
   DIAG-128 `implemented_in_files`: exportContent.ts, exportSnapshot.ts. TRUST-074 still lists `src/page/modules/plantumlBundle.markers.ts`.
   `okfreq trace requirements --json`: 0 occurrences of LAYOUT-021, `"missing_ids": []`.
4. Other facts (`git diff origin/main..HEAD`): four companions in rule-3 form (patchTightness, seven names in requirementsViewer, SITE_CSS, `out/bundle/plantumlPreview.js`);
   plantumlBundle host line is `// Companion of: esbuild.mjs`; DIAG-128 markers in whenDiagramsSettled, its call and embedImages (blocks of <=3 IDs); LAYOUT-021 marker removed;
   marker block definition word for word in `.agents/glossary/common.md` (plus a trailing "Checked by `just check-markers`.") and in `project.guidelines.md` "Marker placement"; "Companion marker file" in glossary;
   CONTRIBUTING bullet and justfile comment updated; log.md entry present; baseline `scripts/marker-baseline.json` has `limit` 3, `blocks`, `unnamedCompanionLines`.
   Minor note: glossary entry "Marker block" sits between "Sticky heading band" and "Table bar", not in alphabetical position (inspector already noted it).
5. PR 410 description (draft, head 10c92335...): renders, sections consistent with the diff, no images, Known gaps "None" and no UNVERIFIED claims. Review box unchecked (draft); the Driver's log notes `r1 approved at dedbdb2a, committed as 10c92335`.
6. Gate: `driver gate result=pass head=10c92335922923f749209f2f888dc9224803cdc4 command=just preflight` in `$CHANTIER log`; CI green per the log.

No before/after images (no UI). VERIFIED
