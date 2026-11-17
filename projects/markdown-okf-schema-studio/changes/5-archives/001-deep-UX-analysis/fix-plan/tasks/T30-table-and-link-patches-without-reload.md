# T30 — Properties-table and link updates without reloading the webview

| Field | Value |
| --- | --- |
| Fixes | [UX-28](../../06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md) (step 2 of 3) |
| Depends on | T29 |
| Gate | `unit trusted scroll` |
| Risk | Medium (P-R7 properties table; open frontmatter editors) |
| Commit message | `perf(vscode): update the properties table in place` |

## Goal

The two deferred passes that today re-assign the whole webview document after every render now
patch the properties section in place, or do nothing when it is unchanged:

- `refreshFrontmatter`: 300 ms after each edit;
- `scheduleLinkEnrichment`: 150 ms after each render, and on linked-file changes.

After this task, a settled render of a document costs **one** html assignment: the ready render
itself.

## Context to read first

- `src/extension.ts`: `refreshFrontmatter`, `scheduleLinkEnrichment`, `setPanelHtml`, and
  T29's `assignWebviewHtml` and `readyRequestId`.
- `src/frontmatter/propertiesTable.ts`: `replacePropertiesTableMarkup`, `renderPropertiesTable`.
- `src/webview/scrollSync.ts`: `setFrontmatterEditCells`, `applyDescriptionVisibility`,
  `closeLinkTooltip`, `measure`, `applyAnchor`, `closeFrontmatterEditor`, `activeFrontmatterEdit`.

## Allowed files

- `src/extension.ts`
- `src/frontmatter/propertiesTable.ts` (a small refactor so the markup can be reused)
- `src/webview/scrollSync.ts`
- `test/frontmatter/propertiesTable.test.ts`, `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T30)

## Steps

1. Write the tests first and record the failures.
2. Host helper `patchPropertiesTable(preview, result)`. It replaces both `setPanelHtml(…replacePropertiesTableMarkup…)` call sites:
   1. `markup = renderPropertiesTable(result, enabled, sourceMapping, !preview.readOnly)`;
      `html = replacePropertiesTableMarkup(preview.webview.html, …)`. Either refactor
      `replacePropertiesTableMarkup` to accept precomputed markup, or call both. The output must be
      identical.
   2. If `html === preview.webview.html`, return: nothing changed.
   3. If the webview is ready for the current stage (`preview.readyRequestId === preview.stage?.requestId`):
      set `preview.webview.html = html`, then post
      `{ type: "previewPropertiesTable", documentId, documentVersion, requestId, markup }` with the
      current stage's identifiers.
   4. Otherwise, fall back to `setPanelHtml(preview, html)`.
3. Runtime handler for `previewPropertiesTable` (`sameContext`; `markup` must be a string):
   - **A frontmatter editor is open** (`activeFrontmatterEdit`): store `deferredPropertiesMarkup =
     markup` and return. In `closeFrontmatterEditor`, apply the deferred markup if present.
   - **Otherwise, apply it:**
     1. `closeLinkTooltip()`.
     2. Find `[data-okf-properties]` in `#sphinx-myst-preview-content`.
        - With a non-empty `markup`: replace the section if it exists
          (`insertAdjacentHTML("beforebegin", markup)`, then `remove()`); otherwise insert it with
          `main.insertAdjacentHTML("afterbegin", markup)`.
        - With an empty `markup`: remove the section.
     3. Then: `setFrontmatterEditCells(editMode)`, `applyDescriptionVisibility()`, `measure()`,
        `applyAnchor()`.
   - The markup is host-generated and escaped (P-S4). Do not run it through any other path.
4. Leave PlantUML injection (`scheduleDeferredPreviewWork`) on the full-assignment path; T34
   covers it. Add a comment there.

## Tests

**Unit** (runtime):

- The message replaces the section.
- It inserts the section when absent; it removes the section on an empty markup.
- It is deferred while a frontmatter editor is open, then applied on close.
- It is ignored for another `requestId`.
- After a replacement, edit cells get `tabindex` in edit mode.

**Unit** (`propertiesTable.test.ts`): the refactor leaves the `replacePropertiesTableMarkup` output
unchanged on the existing fixtures. Existing tests cover this; add one with precomputed markup if
the signature changed.

**Real-input E2E**, scenario **RI-T30**:

- Frontmatter document with an x-okf-link to an existing target (as in RI-T21); side preview
  ready.
- Record `htmlAssignments` as `A0`.
- Type 10 characters in the **body** (source editor) with a 60 ms delay, then wait for ready
  plus 600 ms.
- Assert `htmlAssignments - A0 <= renders`, where `renders` is the number of distinct `requestId`
  values that reached `phase === "ready"`. Poll `getActivePreviewForTests()` every 25 ms while
  typing and collect the `requestId` values seen with `phase === "ready"`.
- Then modify the linked target's description on disk (`fs.writeFileSync`) → the excerpt updates
  in the **same** frame, with no new assignment (`htmlAssignments` unchanged).

## Expected changes to existing tests

None expected. `previewEditing.test.ts` checks for enrichment "without a full document render"
must still pass. If one relied on the html being re-assigned, STOP and report.

## Must not change

- Properties-table content and attributes (P-R7); description-column state; link tooltips; edit
  flows.

## Done when

- The `unit`, `trusted` and `scroll` gates pass; RI-T30 passes.

## Amendment (2026-10-14, after T43)

T29 was replaced by T43 (D-22). Read "T29's" as "T43's" everywhere above:

- `assignWebviewHtml(target, html)` in `src/extension.ts` is the only place that assigns
  `panel.webview.html`. It counts changed assignments in `htmlAssignments` and clears
  `readyRequestId` and the pending overlay.
- `preview.readyRequestId` is set when the runtime reports `previewReady`.
- The test hook `getActivePreviewForTests()` already exposes `htmlAssignments` and
  `webviewReady`; the real-input harness has `htmlAssignmentCount()`.
- In step 2.3, `preview.webview` is the **host's record** of the last page (`{ html, diagnostics }`),
  not VS Code's webview. Update it with `preview.webview = { ...preview.webview, html }` and do
  **not** call `assignWebviewHtml` or `setPanelHtml` on that path: the in-place path must not
  reload the frame.
- No installs of any kind (no network). Allowed files are unchanged.
