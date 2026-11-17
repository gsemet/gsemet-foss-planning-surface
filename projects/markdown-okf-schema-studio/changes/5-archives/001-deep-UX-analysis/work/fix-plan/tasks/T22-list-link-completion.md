# T22 — List fields suggest link targets and warn about unknown ones

| Field | Value |
| --- | --- |
| Fixes | [UX-19](../../03-frontmatter-editing/UX-19-list-editor-keyboard-and-completion.md) (points 3 and 4) |
| Decisions | D-07 |
| Depends on | T21 |
| Gate | `unit trusted` |
| Risk | Low–medium (must not alter link resolution: UX-22 frozen) |
| Commit message | `feat(vscode): suggest Markdown targets in frontmatter link lists` |

## Goal

- **Suggestions.** In the list editor of a field whose schema declares
  `x-okf-link: { resolution: filename-stem }`, either on the property or on its `items`, each item
  input offers a `datalist` of up to 500 known Markdown filename stems. They come from the same
  roots the resolver uses.
- **Warning.** Typing a value that is not a known stem shows a non-blocking inline warning; saving
  stays allowed.
- Link resolution and its diagnostics do not change (UX-22 frozen).

## Context to read first

- `src/frontmatter/stemIndex.ts` → `MarkdownStemIndex`: `candidatesByStem`, `get`, `lookup`;
  `getCachedMarkdownStemIndex(roots)`.
- `src/frontmatter/fileLinks.ts` → `resolveFrontmatterLinkRoots(options).filenameRoots`,
  `inspectFrontmatterLinks`.
- `src/frontmatter/okfFrontmatter.ts` → `analyzeFrontmatter`: where `inspectLinks` triggers
  `inspectFrontmatterLinks`, and how the effective schema properties are available per field.
- `src/frontmatter/propertiesTable.ts` → `renderPropertiesTable`: row attributes.
- `src/webview/scrollSync.ts` → list editor `appendItem`; the editor's `status` element.
- `src/extension.ts`: the link-enrichment render (`scheduleLinkEnrichment`) already re-renders the
  table with `inspectLinks: true`.

## Allowed files

- `src/frontmatter/stemIndex.ts` (add a read-only method)
- `src/frontmatter/fileLinks.ts` (add one exported helper; do not touch resolution)
- `src/frontmatter/okfFrontmatter.ts` (`FieldEntry.linkSuggestions?`, filled when `inspectLinks`)
- `src/frontmatter/propertiesTable.ts` (one row attribute)
- `src/webview/scrollSync.ts`
- `src/preview/previewStyles.ts` (warning-state rule only)
- `test/frontmatter/stemIndex.test.ts`, `test/frontmatter/okfFrontmatter.test.ts`,
  `test/frontmatter/propertiesTable.test.ts`, `test/webview/scrollSync.test.ts` (add tests)
- `test/integration/realInput.test.ts` (add RI-T22)

## Steps

1. `MarkdownStemIndex.stems(limit: number): string[]` returns the indexed stems, sorted, at most
   `limit`. It is read-only and touches no file system beyond the existing index.
2. `fileLinks.ts`: `export function filenameStemSuggestions(options: FileLinkInspectionOptions, limit = 500): string[]`
   returns `getCachedMarkdownStemIndex(resolveFrontmatterLinkRoots(options).filenameRoots).stems(limit)`.
3. `okfFrontmatter.ts`:
   - add `linkSuggestions?: string[]` to `FieldEntry`;
   - in `analyzeFrontmatter`, **only when `inspectLinks` is true**, for each field whose resolved
     schema property, or its `items`, has `x-okf-link.resolution === "filename-stem"`, set
     `linkSuggestions`;
   - call the helper **once** per analysis, with the same options as the link inspection.
4. `propertiesTable.ts`: when `field.linkSuggestions?.length`, add the row attribute
   `data-okf-link-suggestions="<escapeHtml(JSON.stringify(list))>"`.
5. Webview, list editor:
   - parse the attribute (`try`/`catch`; ignore it when invalid);
   - create one `datalist` with a unique id (as the key editor does) and set
     `input.setAttribute("list", id)` on every item input, new ones included;
   - on item `input`, when the value is non-empty and not in the set, set `aria-invalid="true"` on
     that input and show in the editor status, with `data-state="warning"` and
     `data-visible="true"`:

     ```text
     No Markdown file named "<value>.md" was found. It will be saved as typed.
     ```

     Clear both when the value matches or is empty.
6. If `[data-state="warning"]` is not styled yet for frontmatter status lines, add one rule in
   `previewStyles.ts`, with the warning colour
   `var(--vscode-editorWarning-foreground, #bf8803)`, next to the existing `data-state="error"`
   rule.

## Tests

**Unit:**

- `stems` is sorted and limited.
- `analyzeFrontmatter` with `inspectLinks: true` fills `linkSuggestions` only for filename-stem
  fields; with `inspectLinks: false`, it does not.
- `renderPropertiesTable` escapes the attribute.
- Webview: the list inputs get the `list` attribute and the datalist options; an unknown value
  sets `aria-invalid` and the warning status; a known value clears it; saving an unknown value
  still posts the save.

**Real-input E2E**, scenario **RI-T22** (the T21 fixture):

- Open the list editor, add an item, type `StRS-B`.
- Assert that `input.list` has an option `StRS-B` (read with `frame.evaluate`) and that no warning
  is shown.
- Type `X` → the warning is visible. `Enter`, `Enter` → saved. The buffer contains `- StRS-BX`.

## Expected changes to existing tests

None. Snapshot-like assertions of the full properties-table markup may need the new attribute
**only** on filename-stem fields **after** link enrichment. List any such change.

## Must not change

- `resolveFrontmatterLinkRoots`, `inspectFrontmatterLinks` and their messages (UX-22 frozen).
- The display of values (UX-24 frozen).
- Performance: the stem index is cached. Do not rebuild it per field or per keystroke.

## Done when

- The `unit` and `trusted` gates pass; RI-T22 passes.
