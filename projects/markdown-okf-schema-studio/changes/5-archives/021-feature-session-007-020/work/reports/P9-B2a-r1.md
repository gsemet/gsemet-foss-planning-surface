# P9 B2a, round 1 (pure rename and move)

Gate `gate.sh P9-B2a "B"`: green (unit 1660/0, contracts 2/0, security 25/0, visual 241 scenarios, 240 primary PNG + 76 step PNG = 316, 0 duplicates, 0 failures). ps clean before/after, nothing left running, nothing committed, `images/` untouched (0 changes), README/CHANGELOG untouched.

## Changes
- NEW `test/visual/scenarioIds.ts` (replaces `scenarioGroups.ts`): `SCENARIO_ID_BY_LEGACY_ID` (241 entries, `<group>/vNN-<slug>-<theme>-<width>`) and `REMOVED_ALIASES` (syntax-light-shell, preview-toolbar-dark, edit-mode-dark, edit-table-cell-dark).
- `test/visual/scenarios.ts`: `SCENARIOS` is built from the unchanged definitions: aliases filtered out, id replaced by the permanent id, `group` = id prefix, `legacyId` kept, `screenshotOf` remapped. A definition not in the table must already carry a `<group>/vNN-...` id, otherwise the import throws.
- `test/visual/capture.py`: PNG/sidecar in `screenshots/visual/<group>/vNN-....png|json`, step PNGs `…--<step>.png` (+ json); `captures[].file` and `capture` are paths relative to `screenshots/` (INDEX links `visual/...`); first-gap and width-margin reports in `out/reports/visual/{first-gap,width-margins}/<group>/` (parents created); a full run purges the whole `visual/` tree, the legacy flat files (png/txt/json) and the old first-gap/width-margin JSON; partial-run cleanup follows the new layout; `--scenario` also accepts the legacy id (through `legacyId`).
- `scripts/generate-readme-images.py`: the 9 visual sources point to `screenshots/visual/<new id>.png`; `--check` filter now "source under `visual/`".
- `test/site/e2eGroups.test.ts`: B1 review LOW 1 (guard now rejects `scenario["id"]` with `==`, `!=`, `in`, `not in`, `.startswith/.endswith`, and `scenario.get("id"`; applied to the check code, i.e. the part of capture.py before `capture_scenarios`, because the campaign driver legitimately selects by id) and LOW 2 (no hard-coded id: exactly one flagged scenario, fixture matches `/mermaid/`); new assertions: 241 scenarios, id format `<group>/vNN-slug` with the group prefix, aliases gone.
- `CONTRIBUTING.md`: layout of the screenshot folder (the lines 76-81 about the gallery needed no change: it still lists every PNG recursively).
- `p9-e2e/tools/old_to_new.json` (outside git): old id -> new id, action, group, aliasOf. STATE.md ticked.

## Proof (against the B0 baseline in scratchpad p9-baseline)
- PNG bytes: all 316 produced PNGs (240 primary, 76 step) are byte-identical to their B0 counterparts through `old_to_new.json` (step `old-step.png` -> `new--step.png`); frontmatter-links-loading was identical this time (the known flake did not trigger). The 19 B0 files without counterpart are exactly the B1 duplicates (incl. the alias steps).
- Check-pair trace vs `run-manifest-traced.json`: 1330 executed pairs before; 22 belong to the 4 removed aliases; the remaining 1308 pairs match 1308 after, lost 0, gained 0, and all interaction counts are equal (0 differences) modulo the rename.
- Scenarios 245 -> 241 (only the 4 aliases), `duplicateImages` empty, no flat PNG left in `screenshots/`.
- `generate-readme-images.py --check`: 9 identical, 0 differences.

## Deviations / notes
- Ids are applied by a table in `scenarioIds.ts` instead of editing every id literal in `scenarios.ts`: most ids are produced by template/`.map` generators, so the definitions stay untouched (smallest diff). New scenarios (B4/B5) are written directly with their final id.
- Numbering for the D32 split: `frontmatter-schema` renumbered v01-v19, `frontmatter-editing` v01-v06 (migration.md still has the pre-D32 numbers for these; `old_to_new.json` is authoritative; `migration.md`/`inventory.md` not regenerated).
- Bug found and fixed during the gate: my first `save_step` refactor referenced a removed variable; it surfaced as 2 check failures plus duplicate-PNG failures and was fixed before the green run.
- Open: real-window renames, `locks`, step pruning are later batches; the README real-input sources are unchanged.
