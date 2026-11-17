# T41 implementation — round 1

STATUS: DONE

## Summary
- Position (D-21 a): the host computes the insertion point from the table's own ordering rule (schema order for present schema fields, then non-schema keys in source order) with a new pure function `frontmatterAddPlacement`. The key goes after its table predecessor, or before its table successor when it comes first. `minimalAddPatch` gained `beforeField`. Without a schema the table follows the source, so the clicked-row `afterField` is kept.
- One-line custom keys (D-21 b): a just-added custom key opens as a one-line text field (Enter saves, Shift+Enter adds a line, Cmd/Ctrl+Enter saves). It saves with the new message field `fieldValueStyle: "plain"`; the host honours it only when the current value is the empty string. `isPlainSafeScalar` decides plain vs quoted (also quotes `yes/no/on/off/y/n`).
- Escape (D-21 c): one document-level keydown listener cancels the open frontmatter edit when the target is inside `[data-okf-properties]`. It sets the editor's `cancelled` flag through a new `edit.cancel()` hook, so a later blur writes nothing.

## Files changed
- `src/frontmatter/okfFrontmatter.ts` — `frontmatterAddPlacement`, `isPlainSafeScalar`, `beforeField` and `plainScalar` options.
- `src/extension.ts` — import; `fieldValueStyle` in `PreviewSyncMessage` and `isPreviewSyncMessage`; placement and plain-scalar wiring in `handleFrontmatterSave`.
- `src/webview/scrollSync.ts` — new custom key editor mode, `fieldValueStyle` in the save message, `edit.cancel`, Escape listener.
- `test/frontmatter/okfFrontmatter.test.ts` — unit tests.
- `test/webview/scrollSync.test.ts` — harness option `frontmatterRowAttributes` (additive) and webview tests.
- `test/integration/realInput.test.ts` — RI-T41 and the two changed expectations below.

## Tests written first (failing before the fix)
- All new tests in `okfFrontmatter.test.ts` — the project did not compile: `error TS2305: Module ... has no exported member 'frontmatterAddPlacement'` and `'beforeField' does not exist in type` (log `logs/T41-pre-types.log`, `T41-pre-compile.log`). The webview tests were written in the same state; the runtime had no `fieldValueStyle`, no `cancel` and no section-level Escape, so they could not pass. I did not run them separately against the old runtime because the whole test build failed to compile.

## Tests added or changed
- `T41: a schema field goes between its schema neighbours...`, `...skips absent schema neighbours...`, `...custom key goes after the last row...` — placement rules, including the first-in-table case (`beforeField`).
- `T41: beforeField inserts above the named field with a one-line diff` — start, middle, CRLF.
- `T41: plain scalar safety` and `T41: plainScalar writes ... unquoted only when safe` — `Ann`/`two words` plain; `yes`, `null`, `123`, `a: b`, `#x`, ` lead` quoted.
- `T41: without plainScalar an edited quoted value keeps its quotes` — existing writing unchanged.
- Webview: new custom key opens a one-line text editor; Enter saves with `fieldValueStyle: "plain"` and no yaml format; Shift+Enter does not save; an existing field's save has no style; Escape on the picker cancels and a later blur saves nothing; Escape outside the properties section leaves the edit open.
- RI-T41 (`scenarioAddFieldPositionAndEscape`): schema field added from a non-neighbour row lands after `owner` as a one-line diff and its row follows `owner`; custom `approver` + `Ann` + Enter gives the single added line `approver: Ann`; Escape on the picker closes editor and picker, buffer unchanged.

## Existing assertions changed
- `test/integration/realInput.test.ts` RI-T24 (`scenarioRequiredAndPositionedAdd`) — old: `depends_on: []` right after `scope: Core` → new: after `owner: platform` — required by: D-21 a (table position).
- `test/integration/realInput.test.ts` RI-T25 (`scenarioCustomKeyAndOpenNewField`) — old: `reviewer: ""` after `scope: Core`, saved with Cmd/Ctrl+Enter as `reviewer: "Ana"` → new: `reviewer: ""` after `owner: platform` (last table row), saved with plain Enter as `reviewer: Ana` — required by: D-21 a and b.

## Verification
- `PLAN/scripts/gate.sh T41-impl unit types trusted full` → PASS (unit 605 tests; logs in `PLAN/logs/T41-impl-*.log`).
- Screen was unlocked before the run. Visual level not run (orchestrator).

## Evidence for reviewers
- Evidence captures `t41-add-field-position`, `t41-custom-key-plain`, `t41-escape-on-picker` from the real-input suite.

## Open points / STOP reason
- Insertion at the very start (field first in the table and in the source) goes at text offset 0, above any leading comment block.
- With a schema but no source key to anchor on, the key is appended at the end of the YAML.
- A schema key whose declared type is unknown and whose value is `""` is not treated as a new custom key (only rows with class `okf-unknown`).
