# P9 B2b, round 1 (assertion-only conversion, step pruning, content fixes)

Gate `gate.sh P9-B2b "B"`: green on the first run (unit 1660/0, contracts 2/0, security 25/0, visual 241 scenarios, 137 with a PNG, 167 PNG = 137 primary + 30 step, 0 duplicates, 0 failures). ps clean, nothing left running, nothing committed, `images/`, README, CHANGELOG untouched.

## Changes
- B2a review LOW 1: `--scenario syntax-light-shell|preview-toolbar-dark|edit-mode-dark|edit-table-cell-dark` runs the scenario each one mirrored and prints a note (`REMOVED_ALIAS_CANONICAL` in capture.py). LOW 2: comment above `def capture_scenarios` saying `e2eGroups.test.ts` slices the file there.
- `test/visual/scenarioIds.ts`: `ASSERTION_ONLY_IDS` (the 104 A rows) and `STEPS_BY_ID` (explicit step lists of migration.md: 30 kept, 46 dropped in this batch; the other dropped ones went in B1). `scenarios.ts` applies them in the list builder (`capture: false`, `steps`); the four inline `steps` of B1 were removed (now in the table).
- Content fixes (each small, separate):
  1. `check_orphan_box`: after the last assertion the short box is added again in the same `evaluate`, so the PNG shows the box in the bottom padding (no assertion touched).
  2. `fixtures/30-toc.md`: a 10-column table right after the intro paragraph. The fixture already had one at the very end, never visible in the top-of-page shots, which is why Auto equalled Margin. `tocChecks` unchanged and all 8 TOC scenarios pass (they run the table-overlap and "auto: centred on the area left of the TOC" checks on both tables).
  3. width-modes-* and diff-*-edit: all A rows, so no PNG and no content fix needed (the key image per mode stays the existing width-mode-break PNGs; the diff edit frames are covered by the preview PNGs).
  No product code touched, no `knownIssue` needed.
- `p9-e2e/migration.md` and `inventory.md`: ids/groups refreshed to the post-D32 numbers from `tools/old_to_new.json` (textual id mapping; header notes added; counts/per-group tables of the pre-audit inventory not recomputed, said in the header; real-window rows unchanged: T1 moves the frontmatter real rows).
- STATE.md ticked.

## Proof (vs the B2a run, snapshot `p9-baseline/run-manifest-b2a.json`, `png-sha256-b2a.txt`)
- Scenarios 241 = 241, same ids. Executed (scenario, check) pairs 1308 -> 1308, 0 lost, 0 gained; per-check interaction counts: 0 differences (even the orphan and TOC scenarios: the changes add no Playwright calls; skipped captures still count).
- PNGs 316 -> 167: 103 primary PNGs of A rows removed (104 A rows, one is the `okf-schema-narrow` alias that never had a PNG) + 46 step PNGs removed = 149; 30 steps kept; 0 added; nothing else removed.
- Kept PNGs byte-identical to B2a except: orphan box (`review-annotations/v01-orphan-box-end-padding-dark-900`, intentional: box visible), the 4 TOC PNGs on 30-toc (`toolbar-navigation/v22-toc-margin-light-900`, `v23-toc-auto-light-900` (now differs from Margin), `v24-toc-full-light-900`, `v27-toc-full-dark-1600`) plus `v28-toc-hidden-narrow-light-460` (intentional: new table at the top; new baselines, none is a README source), and `frontmatter-schema/v03-links-loading-dark-900` (the known timing flake; hash equals the B0 run-2 variant).
- `generate-readme-images.py --check`: 9 identical, 0 differences; `git status images/`: clean.

## Notes
- Step sidecars and scenario descriptions that still mention dropped step PNGs (e.g. "-palette PNG") are for B2c to reword with `locks`.
- `old_to_new.json` `stepsKept` is incomplete for steps (B2a review INFO 4); the step lists that count are in `scenarioIds.ts`.
