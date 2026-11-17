# T22 implementation — round 1

STATUS: DONE

## Summary
List fields whose schema (property or `items`) declares `x-okf-link: filename-stem` now get a
`datalist` of up to 500 sorted Markdown stems in the list editor, and an unknown typed value sets
`aria-invalid` plus a non-blocking warning in the editor status. Suggestions are computed once per
analysis, only when `inspectLinks === true`, from the resolver's own filename roots (resolution code
untouched, UX-22 intact).

## Files changed (all under )
- src/frontmatter/stemIndex.ts — `MarkdownStemIndex.stems(limit)`
- src/frontmatter/fileLinks.ts — exported `filenameStemSuggestions(options, limit = 500)`
- src/frontmatter/okfFrontmatter.ts — `FieldEntry.linkSuggestions?`, filled once per analysis for filename-stem fields when `inspectLinks === true`
- src/frontmatter/propertiesTable.ts — row attribute `data-okf-link-suggestions` (escaped JSON)
- src/webview/scrollSync.ts — list editor: parse attribute, datalist, `list` attr on every item input, input-time warning (recomputed across all items)
- src/preview/previewStyles.ts — `[data-state="warning"]` rule (warning colour)
- tests: test/frontmatter/{stemIndex,okfFrontmatter,propertiesTable}.test.ts, test/webview/scrollSync.test.ts, test/integration/realInput.test.ts (RI-T22)

## Tests written first (failing before the fix)
- Unit (run against HEAD sources; log in scratchpad prefail.full): `TypeError: index.stems is not a function`; linkSuggestions test `assert.ok(...) actual: undefined, expected: true`; propertiesTable attribute regex did not match; scrollSync T22 datalist `assert.ok(datalist)` falsy; warning test `null !== 'true'` (aria-invalid). ("saving an unknown value still posts" passes before and after by design.)
- RI-T22 with the old webview runtime (log logs/T22-impl-pre-trusted.log): `AssertionError: the datalist offers StRS-B: []`

## Tests added or changed
- stemIndex: stems sorted/limited. okfFrontmatter: suggestions only for filename-stem fields (property-level and items-level), absent with `inspectLinks:false`, absent on bundle-relative/plain fields. propertiesTable: attribute escaped, only when present. scrollSync (4 tests): datalist + `list` on existing/new inputs; invalid/absent attribute ignored; warn/clear; unknown value still saves.
- RI-T22: real input; known `StRS-B` offered and no warning; `X` -> warning; Enter, Enter -> buffer contains `- StRS-BX`.
- `openListEditor` test helper gained an optional `suggestions` argument.

## Existing assertions changed
- none

## Verification
- `scripts/gate.sh T22-impl unit types trusted visual` -> unit PASS, types PASS, trusted PASS (incl. RI-T22), visual PASS vs baseline (0 new failure lines, 4 baseline lines now passing). Logs: logs/T22-impl-*.log, screenshots logs/visual-T22-impl.

## Evidence for reviewers
- RI-T22 frame `29-list-link-warning` in the trusted run's real-input evidence folder.

## Open points
- Chose `inspectLinks === true` (not `!== false`) so callers that omit the option see unchanged output.
- Wikilink-syntax values (`[[x]]`) are compared literally and would warn; the task specifies a plain stem comparison.
- An earlier helper script briefly reverted source files to HEAD to capture failures; all files were restored (diff verified: 6 source files, +99/-1).
