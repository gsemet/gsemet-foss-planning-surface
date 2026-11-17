Verdict: APPROVE

Reviewer re-derived everything from the B0 baseline (scratchpad p9-baseline) and the current `out/reports/e2e/screenshots`. No gate re-run, nothing committed, nothing left running (the only matching process is VS Code's own).

## Verified
- PNG identity: 316 current PNGs under `visual/<group>/`; mapped back through `old_to_new.json` (new id -> legacy id, step `id--step` -> `legacy-step`), all 316 hashes equal the B0 hashes, 0 unmapped, 0 diffs. The 19 baseline files without counterpart are exactly the B1 duplicates. No flat PNG left in `screenshots/`.
- Check pairs: 241 scenarios = the 245 minus the 4 aliases; manifest `partial=false`, passed, 0 failures, `duplicateImages` empty. Interaction counts per (scenario, check), mapped new->old: 0 differences; 1308 executed pairs after = 1308 before minus the 22 of the aliases.
- Removed aliases: for each of syntax-light-shell, preview-toolbar-dark, edit-mode-dark, edit-table-cell-dark, the baseline trace equals its canonical scenario's trace for all 43 checks (no alias-only check, all counts equal), and their definitions are `screenshotOf` of the canonical one. No unique check lost.
- `legacyId`: kept on every renamed scenario, `--scenario` maps it to the new id before validation, `screenshotOf` is remapped, unknown id/group throws at import; test asserts id format, prefix = group, aliases gone.
- Purge (full run only): rglob over `screenshots/visual/` plus flat `*.png/*.txt/*.json` directly in `screenshots/` (non-recursive, so `checkbox-e2e-*`, `real-input-*` etc. directories are untouched) and `*.json` under the first-gap / width-margins report dirs. All inside `out/`. Partial runs only delete the requested scenarios' own `<id>.*` and `<id>--<known step>` files.
- README `--check`: 9 identical, 0 differences against `readme-outputs`; `git status images/` is empty. Crop sources point at the new ids with unchanged boxes.
- Consumers: gallery (`test/site/buildSite.ts`) walks the screenshot root recursively and finds sidecars next to PNGs; review-index/reviewEvidence only read the manifest status/duplicate fields; INDEX links use `visual/`. CONTRIBUTING.md line 45 is accurate (line 82 "recursively" still true).
- Guard scope: the slice ends at `def capture_scenarios`; everything before it (checks, save_step, trace, page-run helpers) is covered, the campaign driver/`main` (legitimate id selection) is excluded. If the marker were renamed, `indexOf` = -1 makes the slice cover almost the whole file and the test fails loudly (and `length > 1000` guards the empty case), so the boundary fails safe.

## Findings (none blocking)
1. LOW, `test/visual/capture.py` `--scenario`: the four removed alias ids (old ids) are now "unknown id" errors, not redirected to their canonical scenario. Acceptable (they never ran separately), but say so in the README/CONTRIBUTING or map them to the canonical id in `legacy_to_id` for B2a-B2b convenience.
2. LOW, guard string anchor: add a comment next to `def capture_scenarios` ("e2eGroups.test.ts slices the file here") so a refactor keeps the marker; failure is loud but the cause is not obvious.
3. INFO: `migration.md`/`inventory.md` still carry pre-D32 numbers for frontmatter groups; `old_to_new.json` is authoritative (regenerate at the end of the batch series as planned).
4. INFO: `stepsKept` in `old_to_new.json` is incomplete for step PNGs (I mapped steps by the `id--step` pattern); fix if the file is reused as a proof tool in B2b/B2c.
