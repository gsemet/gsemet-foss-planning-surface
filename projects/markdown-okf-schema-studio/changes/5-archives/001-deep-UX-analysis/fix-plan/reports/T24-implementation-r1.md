# T24 implementation — round 1

STATUS: DONE

## Summary
Resolved after the orchestrator amendment (capture.py allowed). All T24 steps are implemented and the unit, types, contracts and trusted gates pass (RI-T24 included).
The earlier visual STOP was resolved by updating the Add-field block in capture.py as the amendment specifies.

## Files changed
- src/frontmatter/okfFrontmatter.ts — `FieldEntry.required?`, set for schema-required fields (also for the synthetic "missing required" rows).
- src/frontmatter/propertiesTable.ts — row attribute `data-okf-required="true"`.
- src/webview/scrollSync.ts — `createFrontmatterMenu`: Remove disabled plus tooltip/aria-label/data-tooltip on required rows (row found with `anchor.closest("tr[data-okf-field]")`, so it covers value and key editors); select `change` adds immediately with `afterField = edit.fieldName`; confirm button hidden for the select variant (`hidden` plus `style.display = "none"`, because the menu CSS gives buttons an explicit `display` that overrides `[hidden]`); text variant keeps the confirm button and adds Enter. `postFrontmatterAction(..., afterField)` sends `afterField` only for a non-empty string on `add`.
- src/extension.ts — `PreviewSyncMessage.afterField`; `isPreviewSyncMessage` validation (only `previewFrontmatterSave` + `add`, string 1–1024 chars, no CR/LF); `handleFrontmatterSave` passes `{ afterField }` to `createFrontmatterFieldPatch` when that field exists in `preview.frontmatter.fields`.
- tests: test/frontmatter/okfFrontmatter.test.ts, test/frontmatter/propertiesTable.test.ts, test/webview/scrollSync.test.ts, test/integration/previewEditing.test.ts, test/integration/realInput.test.ts (RI-T24, registered in `run()`).

## Tests written first (failing before the fix)
- T24: analyzeFrontmatter flags schema-required fields only — `required` was undefined, expected true (the types were added first so the tests compile).
- T24: required fields render data-okf-required — no attribute in the markup.
- T24: Remove field is disabled with a tooltip on a required row — `removeButton.disabled` not true.
- T24: choosing a field in the picker adds it right after the open row — `actual: undefined, expected: 'add'` (no message posted on change).
- T24: the text-input picker adds on Enter with afterField — no message posted on Enter.
- RI-T24 against the unmodified code (`logs/T24-impl-pre-trusted.log`) — `Real-input integration failed: AssertionError: Remove field is disabled on the required scope field  false !== true`.
- previewEditing host checks (bad `afterField`, add after `status`) were added with the same change; the run order puts real-input first, so they were not observed failing separately. They pass now.

## Tests added or changed
- Unit tests above (required flag, table attribute, webview remove disabled/enabled, select change posts add with afterField and hides confirm, text Enter posts add).
- previewEditing.test.ts: an `afterField` containing a line break leaves the document unchanged; an add with `afterField: "status"` inserts `summary:` directly after the `status:` line; then the field is removed again (additions only).
- RI-T24: opens the `scope` value, asserts Remove is disabled with the tooltip, clicks Add field, `selectOption("depends_on")` (the one allowed exception, documented in the code comment), and asserts the buffer equals the original with exactly one new `depends_on: []` line directly after `scope: Core`.

## Existing assertions changed
- test/visual/capture.py:check_preview_edit_mode (Add-field block only) — old: enabled confirm-add button required and clicked, then add message checked → new: `wait_for_function` (2000 ms) for an add message with `fieldName === values[0]` and `afterField === 'status'`, plus the confirm-add button is not visible — required by: select choice adds immediately (D-08). Nothing else in capture.py changed.
- Unit tests: None. The existing "frontmatter field toolbar adds and removes fields" unit test still passes: the change already posts the add, and the later confirm click is ignored while saving.

## Verification
- `gate.sh T24-impl unit types contracts trusted` → PASS (logs/T24-impl-*.log)
- `gate.sh T24-impl unit types contracts trusted visual` → all PASS; visual: 0 new failure lines (logs/T24-impl-*.log). `afterField` was `'status'` as expected.

## Evidence for reviewers
- Screenshot "32-required-remove-disabled" from RI-T24 (real-input evidence folder).

## Feedback addressed (rounds 2–3)
- n/a

## Open points / STOP reason
- None.
