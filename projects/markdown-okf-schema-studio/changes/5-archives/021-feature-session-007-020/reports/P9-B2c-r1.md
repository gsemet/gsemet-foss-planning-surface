# P9 B2c, round 1 (locks, invariants test, orphan box, wording)

Gate `gate.sh P9-B2c "B"`: green first run (unit 1667/0 = 1660 + 7 new, contracts 2/0, security 25/0, visual 241 scenarios, 137 with a PNG, 167 PNG = 137 + 30 steps, 0 duplicates, 0 failures). ps clean before and after, nothing left running, nothing committed, `images/`, README, CHANGELOG untouched.

## Files
- `test/visual/scenarioIds.ts`: `LOCKS_BY_ID` (241 lines, one per permanent id, incl. the 104 assertion-only ones).
- `test/visual/scenarios.ts`: `locks: string` is now required on `Scenario`, filled by the list builder (throws on a missing or blank line); descriptions reworded; `ScrollMode` bottom gets `extra?`; orphan scenario uses `{ kind: "bottom", extra: 120 }`.
- `test/visual/capture.py`: `apply_scroll` bottom honours `extra` (extra px after the usual last block + 40 px).
- NEW `test/site/scenarioInvariants.test.ts` (7 tests).
- `p9-e2e/STATE.md` ticked, reviewed: pending.

## Locks
Each line is one present-tense sentence derived from the check functions in capture.py (page checks, theme/frontmatter/schema checks, toolbar, TOC, width, first-gap, palette, slash, table, frontmatter editors, sticky, final frame), not from the old descriptions; behaviour only seen in a PNG is not claimed (examples dropped: shadow on the table overflow edge, the + button in the hover step, "set-as-null leaves the editor disabled", orphan box visibility). Every scenario also runs the global checks (toolbar rows/collapse/zoom, tooltip contrast, page overflow); the lines name them only where they are the scenario's point (toolbar family). TOC v22-v29 lines mention the 10-column table placed right after the intro paragraph (review LOW 2). The lines are raw material for P10; D32 asks a Sonnet critic pass per group over this text.

## Description and step wording (review INFO 4)
Reworded where a dropped step PNG or a missing capture was named: edit affordances, edit-palette (light/tall/tall-dark/tall-narrow), palette-mode (6), slash-menu (4), insert-point hover, table End/cell wrapped family (generator now names `arrowdown`, `cell-bar`, `cell-emoji`, `open` only for the scenario that keeps them), TOC ("final frame"), comment chips, link details, context-tag/scroll-stress "capture" wording, and the interface doc comments for `editPalette`, `editPaletteTall`, `paletteModeShot`, `slashMenuShot`. Step sidecars take their note from the description (`... Step: <name>.`), so they follow. The edit-insert-point-hover description no longer claims the insertion-point behaviour that no check asserts.

## Invariants test (all pass)
ids unique, `<group>/vNN-slug` pattern, number unique per group, group in `e2eGroups`; non-empty one-sentence `locks` on every scenario, none for an unknown id, TOC v22-v28 mention the table; `ASSERTION_ONLY_IDS` size 104, all real ids, equal to the `capture:false` set, no kept step on them; every `STEPS_BY_ID` key is a scenario and every step name (also in `scenario.steps`) is in `STEP_NAMES` (parsed from capture.py); `readme` scenarios and every `VISUAL / "<id>.png"` source in `generate-readme-images.py` are real, capturing, non-alias scenarios; orphan scenario scrolls on (`extra >= 80`). New tests were not run on the old code (the locks assertions fail trivially there; the registry/readme ones are pure invariants).

## Orphan box
The box sits in the bottom padding, below where the usual "bottom" scroll stops (last block + 40 px), so only its divider showed. Raising the height does not help (the stop is relative to the last block). The scenario now scrolls 120 px further; the box is re-added after all assertions as before. New PNG shows the divider, the title "Orphaned comments" and the entry fully inside the 400 px frame; the final-frame bottom check still passes.

## Proof (vs the B2b gate run, snapshot `p9-baseline/run-manifest-b2b.json`, `png-sha256-b2b.txt`)
- Scenarios 241 = 241, same ids; executed (scenario, check) pairs 1308 -> 1308, 0 lost, 0 gained; per-check interaction counts: 0 differences (apply_scroll is outside the trace).
- PNGs 167 = 167; 165 byte-identical; changed: `review-annotations/v01-orphan-box-end-padding-dark-900` (intended) and `frontmatter-schema/v03-links-loading-dark-900` (the known timing flake).
- `generate-readme-images.py --check <p9-baseline/readme-outputs>`: 9 identical, 0 differences; `git status images/` empty.

## Open points
- Sidecar JSON of every captured PNG now carries `locks` (no PNG change).
- The Sonnet critic review of the locks text (D32) is pending; B3 gallery should show `locks` in its rows.
