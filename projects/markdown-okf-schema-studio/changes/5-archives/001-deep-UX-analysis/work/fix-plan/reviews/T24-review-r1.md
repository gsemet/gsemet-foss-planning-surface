# T24 review — round 1

Base: 24d5ab9 · Reviewed diff: 10 files (excluding unrelated book/chapters/05-skills.md, pre-existing working-tree change not part of T24), src +62/-7, tests +225/-21 (capture.py)

## Gates
compile PASS, unit PASS, types PASS, contracts PASS, trusted PASS incl. RI-T24 (logs/T24-*.log), visual PASS: 0 new failure lines vs T00 baseline (logs/T24-visual-*).

## Done-when
- [x] unit and trusted gates pass; RI-T24 passes — logs/T24-unit.log, logs/T24-trusted.log.
- [x] `FieldEntry.required` set from effective schema (both analyzeFrontmatter synthetic missing rows and fieldsFromYaml) — "T24: analyzeFrontmatter flags schema-required fields only".
- [x] `data-okf-required="true"` row attribute (static literal, no data injection) — propertiesTable test.
- [x] Remove disabled + title/aria-label/data-tooltip on required rows; enabled on optional rows — scrollSync unit test, RI-T24.
- [x] Select `change` adds immediately with `afterField = edit.fieldName`; confirm hidden — unit test + capture.py amended block.
- [x] Text variant keeps confirm and adds on Enter — unit test.
- [x] Host inserts after `afterField`; CR/LF afterField rejected — previewEditing.test.ts; RI-T24 asserts buffer equals original plus exactly one `depends_on: []` line after `scope:`.

## Protected features checked
P-S2: `isPreviewSyncMessage` accepts `afterField` only on `previewFrontmatterSave`+`add`, string 1–1024, no CR/LF; otherwise whole message rejected. Host additionally passes it to the patch only when the name exists in `preview.frontmatter.fields`; else `undefined` → append (T06 fallback, `positioned` false). Version/requestId matching untouched. A stale name that passes the field check but not the YAML map lookup still falls back inside createFrontmatterFieldPatch. Safe.
P-S4: no new innerHTML; tooltip text is a constant.
P-E7: optional removal unchanged (button enabled when attribute absent; existing "adds and removes fields" unit test passes); required removal blocked by disabled button and host refusal at extension.ts ("Cannot remove required frontmatter field") left intact. Key rename and value editing paths untouched.
P-E8: picker/menu only built in edit mode; no new entry point.
Minimal patch: T06 insert path used unchanged; RI-T24 asserts byte-identical rest of buffer.
Double add: `postFrontmatterAction` returns early while `edit.saving`; select change is the only trigger in the select variant (confirm hidden via `hidden` + `display:none`), and a residual confirm click is a no-op while saving. No double add.
Webview template (conventions §2): no backticks/`${`, `preventDefault?.()` guarded, no global timers.

## Findings
1. [MINOR] scrollSync.ts:createFrontmatterMenu — in the select variant, `change` with keyboard arrow navigation on some platforms fires per arrow press, so a keyboard user may add the first field they move over. Fix (follow-up, not blocking): consider adding on `change` only when not triggered by arrow keys, or document. Native VS Code webview (Chromium) select on macOS fires `change` on commit only, so impact is low.
2. [NIT] Report says host previewEditing tests were not observed failing separately; acceptable since RI-T24 failed pre-fix.

## Existing assertions changed
- test/visual/capture.py check_preview_edit_mode Add-field block — OK, exactly as the orchestrator amendment; stricter (now requires afterField === 'status') and checks confirm hidden.
- No other assertion modified or removed.

VERDICT: PASS
