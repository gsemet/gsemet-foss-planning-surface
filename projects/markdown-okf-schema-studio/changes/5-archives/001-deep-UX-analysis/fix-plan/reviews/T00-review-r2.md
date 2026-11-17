# T00 review — round 2

Base: 1a5f8d875162b6d428ec51f99eef5a6e82141890 · Reviewed diff: 2 files, +12/-8
(`test/integration/previewEditing.test.ts` +10/-6, `test/integration/reload-suite.ts` +2/-2;
no untracked files; no product source touched)

## Gates

- compile: PASS (`logs/T00-compile.log`); re-run by reviewer: PASS (`logs/T00-review-compile.log`, 2 s)
- unit: PASS, 315/315 (`logs/T00-unit.log`); re-run by reviewer: PASS (`logs/T00-review-unit.log`)
- types: PASS (`logs/T00-types.log`); re-run by reviewer: PASS (`logs/T00-review-types.log`)
- contracts: PASS, 2/2 (`logs/T00-contracts.log`)
- full: PASS, 149 s (`logs/T00-full.log`). All hosts exit 0: 12 scroll E2E + block keyboard E2E,
  untrusted, trusted (4 checkbox + 16 description captures + links), standalone, reload campaign
  (`.artifacts/reload-e2e-ZTpo1I/manifest.json` → `suiteResult: passed`).
  Independent re-run by reviewer: PASS, 150 s (`logs/T00-review-full.log`; reload campaign
  `.artifacts/reload-e2e-tpFkYX/manifest.json` → `passed`; `integration-manifest.json` → `passed`).
- visual: PASS vs baseline (`logs/T00-visual.log`): 0 new lines, 0 baseline lines now passing,
  37 failed / 58 passed, capture exit 1 as on HEAD. `T00-visual-failures.txt`,
  `T00-impl-r2-visual-failures.txt` and `visual-baseline-failures.txt` are byte-identical, and the
  r1 and r1-rerun logs produce the same signature. The baseline was recorded after the journal's
  15:02 "Restaurer HEAD" step, so it reflects HEAD product code (T00 changes only integration tests,
  which the visual capture does not run).
- Flakiness: the implementer's first r2 `full` run failed in the scroll campaign (see finding 1).
  It is outside the diff, and 4 later `full` runs passed with no change (r2b, r2c, orchestrator
  T00, reviewer T00-review). Checklist item 12's "two clean reruns" rule is met.
- Tree after the reviewer's gates: `git status --porcelain -- src/markdown-okf-schema-studio` lists
  only the two allowed test files.

## Done-when

- [x] `trusted` passes, or fails only for documented reasons other than the stale header. Evidence:
  the trusted suite runs inside `full` (`run-tests.ts` `main()`: scroll → untrusted → trusted →
  standalone → reload), and `full` passed in `logs/T00-full.log` and `logs/T00-review-full.log`.
  The preview-editing test reaches and passes all 16 `PASS frontmatter screenshot: description-*`
  captures (wide + narrow, white + dark, expanded / collapsed / collapsed-after-refresh /
  expanded-again).
- [x] The report contains a "Baseline" section ready for `STATE.md`. Checked against evidence:
  VS Code 1.141.0 (re-read by reviewer with `code --version`), Node v24.21.0 (re-read with
  `fnm exec -- node --version`), durations per level, and known failures with classification. The
  visual message counts (36 / 5 / 5 / 5 / 1) match a tally of `logs/T00-visual.log` exactly.
- [x] Step 2 (stale header): the two assertions are exactly the ones the task prescribes
  (`previewEditing.test.ts` lines 485–492).
- [x] Step 2b (toggle locators): every occurrence the task lists is changed, and nothing else.
  The task's line numbers 506/507/510/518 are post-round-1 numbers; at base they are 502/503/506/514.
  `git grep` confirms no bare `[data-okf-description-toggle]` locator remains in
  `test/integration` except `reload-suite.ts:65` (`.count() === 0`, intentionally unchanged).
- [x] Pre-fix failure shown: `logs/T00-impl-full.log:915` and `logs/T00-impl-rerun-full.log`
  (`strict mode violation: locator('[data-okf-description-toggle]') resolved to 2 elements`). The
  old header regex cannot match HEAD markup: it requires `<th scope="col">Value</th>` while
  `renderPropertiesTable` emits `<th scope="col"><span class="okf-column-heading">Value…`, which
  `test/frontmatter/propertiesTable.test.ts:577` pins.

## Protected features checked

- P-R7 (properties table, description column collapse persisted per document): no product change.
  Still covered by `captureDescriptionState` in `previewEditing.test.ts`. With `:visible` it now
  asserts that exactly one toggle is displayed in each state: strict mode fails on two, and the
  locator times out on zero. It then checks that this toggle's `aria-expanded`, `aria-label`,
  bounds and fit are correct. Also covered by `propertiesTable.test.ts:74-76` (two toggles by
  design), `previewStyles.test.ts:118-121` (restore toggle `display: none` unless collapsed) and the
  `scrollSync.test.ts` collapsed-attribute tests. Screenshots
  `.artifacts/frontmatter-e2e-xWIo32/description-white-collapsed.png` (single ▶ in the Value
  heading, Description column hidden) and `description-dark-expanded-narrow.png` (single ◀ in the
  Description heading) confirm one visible toggle per state.
- P-L3 (reload restores the side preview and its state): the reload campaign passed in both the
  orchestrator and reviewer runs. `.artifacts/reload-e2e-tpFkYX/02-after-window-reload.png` shows
  the collapsed state restored after a real Reload Window, with ▶ in the Value heading.
- P-L7 (theme modes): the white/dark loop in the preview-editing test is unchanged and passed.
- P-R6 / UX-34, P-N6 / UX-22, UX-24: not touched (no product file in the diff).
- P-S1–P-S4, P-E1–P-E8, P-N1–P-N5, P-P1–P-P3: not touched. Checklist items 14–17 do not apply
  (no runtime, message, read-only or accessibility change).

## Findings

1. [MINOR] Scroll campaign flake (pre-existing, outside the diff). `logs/T00-impl-r2-full.log:311`:
   `locator.inputValue: Timeout 30000ms exceeded … waiting for locator('[data-sphinx-preview-block-editor] textarea')`
   at compiled `out/test/integration/scroll-sync-suite.js:459`. This is the `mode === "block"`
   assertion in scenario **`solo-block-independent`** (the scenario after the last PASS,
   `solo-block-anchored`). It occurred once in 7 `full` runs at this base, and the 6 others passed.
   The block editor textarea disappeared after a scroll, which could be a real intermittent product
   bug (block editor closed by a re-render) rather than pure timing. Action for the orchestrator:
   record it in the `STATE.md` baseline as "known flake: scroll E2E `solo-block-independent`,
   block-editor textarea missing, 1/7 runs". Add a `followups.md` entry so that reviewers of T09,
   T29–T34 (autosave, re-render churn, in-place patch) treat any recurrence in their gates as a
   possible regression and rerun twice before accepting it. No change is needed in T00.
2. [MINOR] Stale visual check outside Allowed files. The `test/visual/capture.py` narrow-schema
   header check reports `narrow schema headers are ['Name', 'Value◀▶'], expected Name/Value`
   against the intended toggle-in-header markup (commit e1b4ad0). Action for the orchestrator: add
   a `followups.md` entry, or fold it into T03 (machine-checked screenshots). The check should read
   the header text without the toggle glyphs, for example the text of
   `.okf-column-heading` minus its `button` descendants, and still expect exactly `Name`/`Value`.
   That line then leaves the visual baseline. No change is needed in T00.
3. [NIT] The `STATE.md` baseline line has slots for `trusted`, `scroll` and `reload` durations.
   The report records them as "inside `full`, not split". When copying, the orchestrator can write
   "trusted/scroll/reload: inside full (149–150 s)" so those slots are not left as `?`.

## Existing assertions changed

- `previewEditing.test.ts` header assertion (base line 487). Old:
  `/<thead><tr><th scope="col">Name<\/th><th scope="col">Value<\/th><th scope="col">Description<\/th><\/tr><\/thead>/u`.
  New:
  `/<thead><tr><th scope="col">Name<\/th><th scope="col"><span class="okf-column-heading">Value/u`
  and `/<th scope="col"><span class="okf-column-heading">Description/u`.
  **OK**: these are the exact replacements in the task's Expected changes, required by the
  intended e1b4ad0 markup. The full three-column `<thead>` structure stays pinned at unit level by
  `propertiesTable.test.ts:577`.
- `previewEditing.test.ts` `captureDescriptionState` `const toggle` (line 98), and the run loop at
  lines 506, 507, 510 and 518 (base 502, 503, 506, 514): `[data-okf-description-toggle]` →
  `[data-okf-description-toggle]:visible`. **OK**: listed in Expected changes. This is not a
  weakening: the locator still targets the toggle the user sees, and strict mode now also fails if
  both toggles are ever displayed together.
- `reload-suite.ts` line 79 (`capture`) and line 90 (×2): same change. **OK**: listed in Expected
  changes. Line 65 is unchanged as required.

VERDICT: PASS
