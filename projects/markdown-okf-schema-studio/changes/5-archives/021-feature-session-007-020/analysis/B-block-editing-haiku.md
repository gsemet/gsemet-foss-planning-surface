Read-only analysis of the four P2 backlog items (repo: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio, branch dev/gsemet, HEAD 9df67aa). Nothing was modified or run.

Cross-cutting facts

- scrollSync.ts is the webview script generator: the browser code lives inside a template literal (it interpolates `${installLinkNavigation.toString()}` at ~line 80). Escapes are doubled (`"\\n"`), so mind that when editing.
- Block identity: the renderer stamps `data-line`/`data-end-line` on BLOCK_TYPES only (src/render/mystRenderer.ts:90-100: paragraph, heading, blockquote, list, listItem, code, table, math, thematicBreak, definitionList), plus figure containers (:1048) and admonitions. html-sanitizer.ts:327-345 (`injectSourceMappings`) turns them into `data-sphinx-source-file/-line/-end-line/-preview-block`. Raw `html` nodes are NOT in BLOCK_TYPES (only raw tables, :1040), so a raw `<img>` block is unmapped.
- Webview "top-level blocks": `topLevelMappedBlocks()` (scrollSync.ts:1242) = mapped elements of the active file with no mapped ancestor, sorted by line. Lists are edited as a whole via `editingElementFor`/`sourceRangeForList` (:3143-3170), so a list is one block.
- Source range of a block: `sourceRangeForLines` (src/mapping/sourceMapping.ts) returns start of `line` to start of `endLine+1` (includes the trailing line break; blank lines between blocks are NOT in any range).
- Edit protocol: webview `previewEditOpen` {documentId, documentVersion, requestId, editId, line, endLine, insertAfterLine?} → host `handlePreviewEditOpen` (extension.ts:1640) answers `previewEditSource` with the raw text. Autosave `previewEditSave` (400 ms, scrollSync.ts:2252-2300) with originalText/editedText/final → host `handlePreviewEditSave` (:1809) → `drainActiveBlockEdit` (~:1740s) computes `minimalReplacement` (src/mapping/textDiff.ts) and applies a `WorkspaceEdit.replace` on the block range. Insertion (`insertAfterLine`) uses `planInsertion`/`insertionText` (src/mapping/insertion.ts): prefix "\n\n", suffix "\n" only if a non-blank line follows.
- Undo: the textarea uses native undo (execCommand in `applyTextEdit`, scrollSync.ts ~1300-1320); document undo is the WorkspaceEdit undo. Checkbox toggle is the one place using `sourceEditor.edit(..., {undoStopBefore, undoStopAfter})` (extension.ts:1621-1626), the cleanest precedent for atomic undo.
- Edit lock: `EditLock` (src/state/editLock.ts) is held from open until release; a render waits (`shouldDeferReload`). Host-side non-editor edits (checkbox, file write) refuse while `preview.activeBlockEdit` is set (extension.ts:1603-1606).
- Untrusted/readOnly: all edit messages are refused with "Editing requires a trusted workspace." (extension.ts:2367-2382). `isDocumentEligible` (:363) = .md + file scheme; `sourceAvailable` (:398) = inside workspace root.
- Message plumbing for a new type: add to `PreviewSyncMessage.type` union (extension.ts ~112), `validType` / `editRequest` checks in `isPreviewSyncMessage` (~420-490), dispatch in `handlePreviewSyncMessage` (:2316-2400, `matchesCurrentPreview` gate first).
- Refresh: any `onDidChangeTextDocument` with changes triggers `refreshPreview` (extension.ts:3263-3268); the webview then rebuilds insert points (`applyEditMode` → `refreshInsertPoints`).

1) move-block-up-down (intent: "+" button right of the horizontal bar, with up and down)

(a) Current state
- The "+" is the insert point: zero-height `div.sphinx-preview-insert-point` placed after each body block (`refreshInsertPoints`, scrollSync.ts:2942-2990; `createInsertPoint` :2923; CSS previewStyles.ts:462-520, button absolute at left -1.6em). Ambiguity: "horizontal bar" most likely = this zero-height insert line; the other candidate is the block editor's action row (`.sphinx-preview-block-editor-actions`, createEditorButtons :2667, Done/Cancel). Confirm with the user.
- Properties section (`data-okf-properties`, `data-line="1"`, src/frontmatter/propertiesTable.ts:266) is in `topLevelMappedBlocks()` → must be excluded from move targets (refreshInsertPoints already does via `isProperties`).

(b) Approach
- Webview: in `createInsertPoint` (or a sibling in refreshInsertPoints) add two small buttons (up/down) on the right of the insert point, shown only for body blocks; disabled at the first/last body block and when `activeBlockEdit` is open. Click → post new `previewBlockMove` {documentId, documentVersion, requestId, editId?, direction, line, endLine, neighborLine, neighborEndLine}. Neighbour = adjacent element of the body list (not properties).
- Host: new handler in extension.ts: validate both ranges (neighbour strictly before/after, only blank lines between them, matching documentVersion); build one `WorkspaceEdit.replace` over [neighbour.start, block.end) with `block + gap + neighbour`, gap = the original blank-line text between them (keeps CRLF and spacing). Use `sourceEditor.edit` with undo stops if the editor is visible (precedent :1621).
- Last block without trailing newline: when moving the final block up, its text gains/loses the trailing line break; normalise by appending the line ending for the block that becomes non-final.

(c) Files: src/webview/scrollSync.ts (refreshInsertPoints, createInsertPoint, click wiring), src/preview/previewStyles.ts (buttons), src/extension.ts (type union, validation, dispatch, new handler), new pure helper, e.g. src/mapping/blockMove.ts (+ test).

(d) Risks: properties as neighbour (moving the first body block "up" must not swap with frontmatter); blocks in included files (`{include}` children carry the include directive's line, see mystRenderer.ts:645-652, :752 — moving them would rewrite the include line); a list is one block; duplicate-line blocks from includes; edit lock/open editor (refuse or save first, as checkbox does); stale preview (documentVersion check).

(e) Tests: test/webview/scrollSync.test.ts (harness `createRuntimeHarness`, pattern of "arrow boundaries transfer block editing" :1842), new pure test test/mapping/blockMove.test.ts modelled on test/mapping/insertion.test.ts, host flow in test/integration/previewEditing.test.ts (pattern: sendPreviewMessageForTests, the block-insertion section ~1177-1245).

(f) Ambiguities: move granularity (top-level block vs list item / nested); which bar; wrap-around at ends (disable vs. nothing); keyboard shortcut too?

(g) Size: M.

2) edit-inline-image

(a) State after commit 2af0afa (src/render/mystRenderer.ts:1249-1266 `wrapBareBlockImages`, called at :1353): a lone `![..](..)` paragraph (MyST → bare `image`) and `{image}` directives are wrapped into a `paragraph` with the source position → get `data-line/data-end-line`. Consequences, verified by reading code:
  - Click on the image: the click handler (scrollSync.ts ~3514-3530) takes `closest(mappingsSelector)` = that paragraph → opens the raw Markdown editor for it. Works.
  - ArrowUp/Down from the text below: `adjacentMappedBlock` (:1265) now sees the image paragraph → works.
  - "+" after the image: insert point now exists (refreshInsertPoints). Works.
  - Test coverage: test/rendering/mystFeatures.test.ts:1094-1140 ("figures and plain images are mapped blocks…", "image directives are mapped blocks…"); test/mapping/insertion.test.ts:68 (plain image shape); test/integration/realInput.test.ts (2af0afa added a visual scenario in test/visual/scenarios.ts).
  - Remaining gaps: (1) raw HTML `<img>` / `<p><img></p>` lines are `html` nodes → unmapped → click does nothing, arrows skip them, no "+" after them. (2) Existing likely bug: because the frontmatter section is a mapped top-level block at line 1, ArrowUp from the first body block targets it (`adjacentMappedBlock` does not exclude `data-okf-properties`); `openMappedEditor` (:3223) returns early for it, so the editor just closes. Not verified at runtime; check with a test.

(b) Approach: (1) in mystRenderer give `html` nodes that are a single image element (or any top-level html block) a `paragraph`-style data-line (extend `wrapBareBlockImages` to html nodes whose fragment is only `<img>`/`<p>` with img); (2) exclude properties from `adjacentMappedBlock` (or from `topLevelMappedBlocks`, which is already filtered in refreshInsertPoints).

(c) Files: src/render/mystRenderer.ts, src/webview/scrollSync.ts (:1265-1270), tests.

(d) Risks: html nodes can contain arbitrary markup — only tag-level wrap; linked images `[![a](b)](c)` (the `a` ancestor check at :2846 and click handler at ~3514 both use `closest("a")` on the mapped element — the paragraph is not inside `a`, so fine); image inside tables (cell editing path).

(e) Tests: test/rendering/mystFeatures.test.ts (raw `<img>` block gets data-line), test/webview/scrollSync.test.ts (ArrowUp from text under an image; ArrowUp from first body block with frontmatter does not lose editor), test/visual scenario in test/visual/scenarios.ts.

(f) Ambiguity: whether raw HTML images should be editable at all (they are HTML, not Markdown) — user decision.

(g) Size: XS if only raw-html is wanted; S with the frontmatter-adjacency fix.

3) multibloc-selection

(a) State: no selection model exists. Plain click in edit mode opens the editor (click handler ~3514; `openMappedEditor` :3222). Drag-select in edit mode yields a click on a common ancestor, which is ignored (`!target` branch). No `copy`, `cut`, `paste` listeners anywhere in src/webview (grep empty). Preview (non-edit) copy is native browser copy (no `user-select: none` on content, only code line numbers, previewStyles.ts:1552). Host has no clipboard writing (only `vscode.env` not used).
  - Block ranges are available: `topLevelMappedBlocks` gives ordered blocks with data-sphinx-source-line/-end-line; raw text can be obtained via `previewEditOpen`-style request, or host can read `document.getText(range)` directly.

(b) Approach
- Selection: Shift+click extends from an anchor block to the clicked block (range = consecutive top-level blocks); Shift+Arrow optional. Store `selectedBlocks` in scrollSync and mark with a data attribute (CSS). Plain click clears it (and still opens editor).
- Copy (Ctrl/Cmd+C with selection and no textarea focus): `copy` event → `clipboardData.setData('text/plain', raw)` where raw is requested from host (`previewBlockRaw` {line, endLine} → host returns `document.getText(range)`), or host writes `vscode.env.clipboard` directly. Keep an internal host-side clipboard (so move works even if the OS clipboard changes).
- Cut: host reads the range, writes clipboard, applies one WorkspaceEdit deleting [first.start, last.end) plus one adjoining blank line (single undo step).
- Paste at insertion point: `paste` event → text/plain → host `insertAfterLine` path, reusing `planInsertion`/`insertionText`; the raw block set keeps internal blank lines. Paste with the internal clipboard match = "move".
- Preview copy: native copy already gives text/html + text/plain across blocks; likely only the insert-point buttons (display:none in view mode) could interfere — verify, the intent may be already met.

(c) Files: scrollSync.ts (selection state, click/shift handling, copy/cut/paste listeners, CSS class), previewStyles.ts, extension.ts (new message types, raw-read and cut/paste handlers), src/mapping/insertion.ts (reuse), possibly new src/mapping/blockClipboard.ts.

(d) Risks: keyboard focus — paste/copy events fire only when the webview has focus; VS Code webview keybinding forwarding for Ctrl+C/X/V must be verified; CRLF: the textarea normalises CRLF to LF (HTML textarea API value; not verified in code, and save at scrollSync.ts:2266 writes `textarea.value` raw), so pasted/cut blocks in CRLF documents may get mixed endings — `insertionText` already converts line endings for paste, cut/copy must too; included blocks share one line (mystRenderer.ts:752) so selecting them would cut the `{include}` line; last block without trailing newline; edit lock while a block editor is open (must save or refuse); undo across several host edits (use one WorkspaceEdit).

(e) Tests: test/webview/scrollSync.test.ts (copy/cut/paste events via RuntimeElement dispatch, pattern of :1467 and :1622), test/mapping/insertion.test.ts (multi-block raw insertion), new test/mapping/blockClipboard.test.ts for range computation/cut with blank lines, integration in test/integration/previewEditing.test.ts (pattern: section at ~1177-1245 "Block insertion protocol").

(f) Ambiguities: selection gesture (Shift+click vs Ctrl+click vs Escape); whether copy in preview must carry raw Markdown or HTML (intent says HTML in preview, raw in edit); whether selection is in preview mode too; OS clipboard vs internal clipboard for paste/move.

(g) Size: L.

4) paste-image-in-edit-mode

(a) State: no paste handling anywhere; a textarea paste of an image does nothing (no preventDefault / no listener). The host has no file writes for user content (only `vscode.workspace.fs.readFile` at extension.ts:2187; build/snapshotWorkspace.ts writes elsewhere). CSP img-src allows the webview resource and data: (src/security/csp.ts:12).

(b) Approach
- Webview: attach `paste` listener on the textarea in `receiveBlockEditSource` (scrollSync.ts ~2776-2800; the keydown listener there is the precedent). If `clipboardData.items` has `image/*`: `preventDefault`, read as base64 (FileReader/`arrayBuffer`), post `previewPasteImage` {documentId, documentVersion, requestId, editId, mime, dataBase64}. Cap size (e.g. 10 MB; the existing precedent is MAX_PATCH_CONTENT_LENGTH 20 MB, src/preview/contentPatch.ts:25). Webview postMessage is JSON; base64 inflates ~33%.
- Host: `handlePreviewPasteImage` in extension.ts: validate editId/active block edit, trust (readOnly refusal), eligibility; dir = path.dirname(document.uri.fsPath), must be inside workspace root (`isPathWithin`, as `sourceAvailable` does); name = `image.png`, conflicts → `image-2.png`, `image-3.png` (use `vscode.workspace.fs.stat` loop); ext from mime (png/jpeg/gif/webp); write with `vscode.workspace.fs.writeFile` (not undoable — note); respond `previewPasteImageResult` {fileName} or {error}.
- Webview on success: insert `![image.png](image.png)` at caret in textarea via applyTextEdit (scrollSync.ts ~1300-1320, native undo), then `setSelectionRange` over the first `image.png` alt-text occurrence (the intent wants the first image.png highlighted). The existing autosave (:1802-1820) then persists the Markdown through the normal edit path.
- Alternative: if no block editor is open in edit mode, paste does nothing (no focus); asking the user whether to open an insertion point is a decision.

(c) Files: scrollSync.ts (paste listener, result handler), extension.ts (type union, validation: new type needs editId; dispatch; handler), a pure helper for name conflict + mime → ext, e.g. src/preview/pastedImage.ts (+ test/preview/... or test/mapping/...), tests.

(d) Risks: orphan file if the Markdown edit later fails or is cancelled (Escape restores text but not the file); file created outside Ctrl+Z; relative path must be relative to the .md file (subfolder documents); untitled/unsaved document (scheme check); CSP and image caching after overwriting; `image.png` already referenced by other content (conflict vs reuse — decide); size and base64 memory; the new image is not a document change so the render relies on the text edit; Windows path separators (`path.posix` in the Markdown ref).

(e) Tests: pure naming helper unit test (node:test, pattern of test/mapping/insertion.test.ts), webview paste dispatch in test/webview/scrollSync.test.ts (pattern of the textarea keydown tests ~1467), host flow in test/integration/previewEditing.test.ts (create file in the fixture dir, check `fs.existsSync`, check document text, cleanup).

(f) Ambiguities: conflict policy (`image-2.png` vs timestamp vs ask); folder (same dir as .md vs `assets/`); reuse existing identical file; behaviour when no editor is open; alt text default (the intent says `image.png`, so alt is "image.png" as written); Markdown vs `{figure}`.

(g) Size: M.

Overall sizes: move-block-up-down M; edit-inline-image XS to S; multibloc-selection L; paste-image-in-edit-mode M.

Notes on existing code: progress note in .agents/changes/backlog/P2/progress.md:46 lists paste-image and block moving as out of scope for the earlier bug run, so these are new work, not regressions.