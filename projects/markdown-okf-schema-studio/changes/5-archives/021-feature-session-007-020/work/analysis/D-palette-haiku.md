Read-only analysis of the edition palette request (repo: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio). Nothing was modified and no build or test was run.

Note: the intent file says "inspect the book/ folder". No book/ folder exists. The Sphinx/MyST docs are in docs/ (known-limitations.md, feasibility-*.md) and test/visual/fixtures/.

## (a) Current editing infrastructure

**Block editor (raw Markdown textarea)**
- `openBlockEditor` is at src/webview/scrollSync.ts:2179. It creates a `div.sphinx-preview-block-editor` (or `...-table-cell-editor`) and inserts it after the rendered target (`insertAdjacentElement("afterend")`, ~2220). It posts `previewEditOpen` to the host.
- The textarea is created in `receiveBlockEditSource` (~2692-2800, textarea at 2737). The status line and buttons go in `div.sphinx-preview-block-editor-actions` (~2750). The status is the hint from `blockEditHint` (2646): "Lines N · Enter: new line · Tab: indent · Esc: cancel · ⌘↩/Ctrl+Enter: done".
- Textarea events: `input` triggers resize plus `autosaveBlockEdit` (AUTOSAVE_DELAY_MS = 400 at line 70). `blur` calls `saveBlockEdit`.
- Keydown order (~2776-2832): `keepUndoInControl` (1398) → `wrapSelectionInControl` (1411) → `navigateBlockEdit` (1429) → `homeEndInControl` (1380) → Enter continuation (`textEditing.continueOnEnter`) → Tab indent (`textEditing.indentSelection`) → Escape cancel / Ctrl+Enter save.
- Buttons come from `createEditorButtons` (2667). Done and Cancel use a `mousedown` preventDefault so focus stays in the field. This is the pattern the palette must copy.
- Close and cleanup: `closeBlockEdit` at 828. Post-save and patch handling: `postBlockEditSave` (2252).

**Text insertion**
- `applyTextEdit` (1448) focuses the control, sets the selection, then uses `document.execCommand("delete")` or `execCommand("insertText", false, text)`. This keeps the native undo stack. If execCommand is unavailable or throws, it falls back to `control.value = …` and calls `onFallbackInput`, which bypasses undo.
- `keepUndoInControl` calls `stopPropagation` on Cmd/Ctrl+Z/Y. This is the existing precedent for keeping shortcuts away from VS Code.

**Pure helpers (stringified into the webview)**
- src/webview/textEditing.ts: `continueOnEnter` (18), `indentSelection` (89), `wrapSelection` (175; `*_\`~` only, emphasis wrapping that keeps the selection), `mapRenderedCaret` (199). The file is injected at scrollSync.ts:57 via `createTextEditingTools.toString()`, so its body must be self-contained.
- The factory pattern is the one to mirror for a palette registry.

**Table cell editor and its controls bar**
- `renderTableCellEditor` (2506). The bar `div.sphinx-preview-table-menu` (`role=toolbar`) is inserted before the table or its single-child wrapper (~2535-2550), not above the block. It has Row+/Row−/Col+/Col− buttons, `data-sphinx-table-operation` attributes, and a status label.
- Cell textarea keydown is at ~2617-2650 (Tab, arrows, Esc, Enter). Blur uses `commitCellEditorOnFocusLoss` (2425), which ignores blur if a pointerdown happened in the last 500 ms (`lastPointerDownAt`, 2420).
- Bar positioning: `toolbarUsableTop` (2466) and `revealTableToolbar` (2490) keep the bar below the sticky band and the fixed preview controls.
- Model: src/webview/markdownTable.ts (`createMarkdownTableTools`; `parse`, `serialize`, `insertRowAfter`, etc.).

**Styles**
- src/preview/previewStyles.ts: `.sphinx-preview-block-editor` (524, focus-border frame, z-index 1), `--first` (540), textarea (545), actions (571), buttons (580-613), table cell editor (634-680), table menu (682-730). The fixed preview toolbar sits at 12px top, 38px tall, per the comment near 540.

**Keyboard and VS Code**
- package.json:80-88 contributes one keybinding only: `markdown-okf-schema-studio.openPreview` on `ctrl+k shift+v` / `cmd+k shift+v`, with `when: editorTextFocus && resourceExtname == .md`. Nothing binds Ctrl+K or Ctrl+/ alone.
- The webview has no Ctrl+K or Ctrl+/ handler. Shortcuts typed inside the textarea are not `editorTextFocus`, so the contributed binding should not fire. Whether an unhandled Ctrl+K chord prefix or Ctrl+/ still reaches the VS Code workbench from a webview is a VS Code runtime behaviour I could not verify from the repo. Calling `preventDefault` and `stopPropagation` in the textarea handler, as keepUndoInControl does, is the safe default.
- Global document keydown listeners (2441, 2452, 2908, 3039, 3588) skip inputs and textareas, so the palette's own shortcuts should not be swallowed by them.

**Images and resource roots**
- extension.ts:920-923: `localResourceRoots = [workspaceRoot]` (plus `out/bundle` when Mermaid is present). The preview resolves images through `webview.asWebviewUri` (src/preview/webview.ts:213).
- CSP: src/security/csp.ts:12 sets `img-src ${cspSource} data:`.
- A webview cannot open a native file dialog. The picker needs a new host message. Existing edit messages are validated at extension.ts:412-490, and `previewEditOpen`/`previewEditSave` are handled around 2368-2400. The new handler would call `vscode.window.showOpenDialog({ defaultUri: dirname(document) })`, then return a path relative to the document. Files outside `workspaceRoot` will not render because they are not in localResourceRoots.

**Mode storage precedent**
- The edit toggle is stored in `context.workspaceState` under `markdownOkfSchemaStudio.editMode` (extension.ts:283, 3243). The webview reports changes with `previewEditModeChanged` (validated near 430; handled ~2360).
- An edition-mode select can copy this exact path: a new message type added to the union at extension.ts:112 and to `validType` at ~412-430, plus a new workspaceState key. The webview's own `vscode.setState` is per-panel and not persisted across reloads.

## (b) Proposed architecture

- **Pure module** `src/webview/editionPalette.ts`, factory `createEditionPalette()`, stringified like textEditing. It holds a registry of `{ id, mode, group, label, icon, shortcut?, run(ctx) }` entries. `run` returns a `TextEdit` (the same shape as textEditing.ts), so every button reuses `applyTextEdit`, which keeps undo, and the existing autosave path.
- **Modes**: `strict | gfm | myst`. `myst` includes gfm, and gfm includes strict. Mode-specific buttons are filtered through the registry. The mode is stored in the host workspaceState (preferred), or as a setting if the user wants it. A `previewEditionModeChanged` message mirrors `previewEditModeChanged`.
- **Dropdowns and grids** are generic `kind: "menu" | "grid" | "picker" | "panel"` entries rendered by a shared function. Heading, code language, and admonition types are menus. Table is a 9x9 grid. Emoji and color are pickers. The link mini-panel and figure editor are panels.
- **Placement**: a `div.sphinx-preview-edition-palette` (role=toolbar) inside `element` before the textarea, so it lies between the frame top and the text. It is positioned in the same flow as the existing `sphinx-preview-table-menu`, which is the simplest pattern. Table cell editing either hosts the palette above the table menu (stacked, sharing the `toolbarUsableTop` logic) or merges the table operations into the palette as a group. This is a user decision.
- **Buttons**: `mousedown` preventDefault on every button, `click` runs the entry, and focus returns to the textarea. The palette is hidden or refreshed on each `receiveBlockEditSource`.
- **Styles**: reuse the `--vscode-*` variables already used for `.sphinx-preview-block-editor` and the table menu, so light, dark, and forced themes follow the existing approach.

## (c) Phases

- **Phase 1 (S-M)**: registry, mode select (strict only, others wired but empty), palette shell, inline toggles (bold, italic, strikethrough), heading menu, code fence with no language, blockquote, horizontal rule. Files: new src/webview/editionPalette.ts; src/webview/textEditing.ts (new pure transforms, or in the new file); src/webview/scrollSync.ts (~2740 insertion, `createEditorButtons` neighbour, renderTableCellEditor 2506); src/preview/previewStyles.ts; src/extension.ts (only if mode is persisted in this phase).
- **Phase 2 (M)**: code-language dropdown, table 9x9 grid (uses markdownTable.ts `serialize`), link with Ctrl+K (`preventDefault` and `stopPropagation`), TODO with Ctrl+/, native `<input type=color>` for color (verify it works in the VS Code webview), emoji picker (static bundled list, no dependency). Files: editionPalette.ts, scrollSync.ts, previewStyles.ts, markdownTable.ts. GFM items (alert menu, checkbox, markdown-table to HTML conversion) are also M.
- **Phase 3 (M-L)**: image file picker (new host message and validation in extension.ts, plus path checks), MyST insertions: admonition types including custom, footnote, definition list, `{math}`/`$…$`, sub/sup roles, figure with caption, label or anchor edit. Files: extension.ts, editionPalette.ts, scrollSync.ts, and possibly a new host-side module for insertion helpers.
- **Phase 4 (L)**: custom editors (figure editor panel, color picker overlay, link mini-panel with two fields and default focus, anchor icon overlay with click-to-edit). The preview-level back/next/zoom/margin buttons are excluded per the user's note.

## (d) Risks

- **IME**: all handlers already skip `isComposing`. Palette insertions must do the same and never run during composition.
- **Undo**: use `execCommand` through `applyTextEdit`. The fallback path (manual splice, 1456-1460) loses undo and must be avoided for palette actions. Multi-step insertions (for example a table) should be one `insertText` call.
- **Focus loss**: textarea `blur` calls `saveBlockEdit`, so any button needs `mousedown` preventDefault. Pickers that open a grid or input must not steal focus at open time. Table cell blur is protected by the 500 ms pointer window (2420), but a palette button inside the cell must still be excluded from `focusInside` (2433) or it will commit early.
- **Shortcut conflicts**: Ctrl+K is a VS Code chord prefix. Ctrl+/ is VS Code's line comment. Both need `preventDefault` and `stopPropagation` in the textarea handler. The contributed `ctrl+k shift+v` binding (package.json:83) is `editorTextFocus`-scoped, so it should not fire from the webview. Verify in the extension host.
- **Content patch**: `planContentPatch` (contentPatch.ts:122) is used at extension.ts:985 and 1114. The palette lives inside the edited block's element, so a patch of the content region could remove it. The existing `activeBlockEdit` handling at scrollSync ~3068 and ~2864 must be checked before adding DOM inside the editor.
- **Narrow widths**: the palette needs to wrap or collapse (the table menu and the fixed toolbar set the precedent). Existing `toolbarUsableTop` (2466) must account for a second bar, and `revealTableToolbar` (2490) must be reused.
- **Themes**: use `--vscode-*` tokens, and check light, dark, and forced cream (the existing visual scenarios cover these).
- **Sanitizer**: color `<span style>` and HTML tables are subject to src/security/html-sanitizer.ts. Table cell styles are preserved as "safe preview metadata" (test/rendering/mystFeatures.test.ts:709), so a span style may be stripped.
- **Image paths**: `localResourceRoots` is the workspace root only (extension.ts:920). Images outside it will not render.

## (e) Tests

- Pure logic: `test/webview/editionPalette.test.ts` (new), mirroring `test/webview/textEditing.test.ts` (the `|` caret and `[ ]` selection notation, `node:test`, `assert/strict`). Cover each transform: bold, italic, strikethrough, heading level, fence with language, blockquote, hr, table serialize, link text and caret, TODO, emoji, mode filtering.
- Renderer for inserted syntax: `test/rendering/mystFeatures.test.ts` (footnotes, definition list, math, sub/sup, figure captions, admonitions, GFM alerts, task lists, HTML tables). Note there is no emoji test or handling in the renderer.
- DOM: extend `test/webview/previewStyles.test.ts` for palette CSS, and `test/webview/markdownTable.test.ts` for the grid output. `test/webview/scrollSync.test.ts` (297 KB) is the place for DOM-level palette behaviour, if a jsdom-style helper exists there.
- Visual: add fixtures under `test/visual/fixtures/` (for example `19-edition-palette.md`) and scenarios in `test/visual/scenarios.ts`, using the existing `editor-keyboard-wrapped-narrow` (line 303) as a template for narrow and forced-theme runs.
- Integration: `test/integration/realInput.test.ts` already drives real input (`scenarioParagraphBlurCommit` 154, `scenarioCtrlEnterCommit` 185). Add a scenario for palette click and blur, Ctrl+K, and undo after a palette insertion.
- Host: `test/integration/previewEditing.test.ts` for the new mode message and the image picker message validation.

## (f) Ambiguities for the user

1. Mode scope: is it per workspace (workspaceState), per document, or a VS Code setting?
2. Does the mode change rendering or only the palette buttons?
3. Table cell editing: merge the palette with the table bar, or stack it above?
4. Color syntax: raw `<span style="color:…">` (sanitizer risk), or a MyST role?
5. TODO syntax: plain `TODO:` text, or a MyST `{todo}` directive?
6. Emoji: which dataset (static bundled list, size), and what output (Unicode or `:shortcode:`)?
7. Image picker: insert relative paths only, and what to do for files outside the workspace?
8. HTML table conversion: raw HTML table, or a MyST `{list-table}`?
9. Math: `$…$` / `$$…$$` or `{math}`? Confirm the renderer's math path works through mathRenderer.ts (not read in full here).
10. Anchor syntax for creating or editing labels: `(label)=`?
11. Ctrl+K and Ctrl+/: accept overriding VS Code shortcuts while the textarea is focused?
12. Admonition custom types: MyST only, with GFM limited to the five GitHub types?
13. Figure editing: `{figure}` directive only, or also `{image}`?

Feature support in src/render/mystRenderer.ts (per source and test/rendering/mystFeatures.test.ts):
- Admonitions: `:::{note}`-style directives with the ADMONITION_TITLES list (note, tip, warning, etc., line 103), version admonitions (versionadded/changed/deprecated, 116), dropdown admonitions (test 580), Quarto callouts (test 559), custom titles (test 310), and hyphenated context tags (tests 860-967).
- GitHub alerts: `> [!NOTE]`-style and bold Note/Important/Warning markers (lines 122-131, `expandGithubAlerts` 398; tests 396-463).
- Footnotes, definition lists, abbreviations, sub/sup: test 463 ("typography renders definitions, abbreviations, scripts, and footnotes"), and `definitionList` in BLOCK_TYPES (line 100).
- Math: `math` and `inlineMath` node types, plus src/render/mathRenderer.ts (94 lines, not read in full).
- Figures: figure directive with caption normalization (785), figure references (test 111, 137), image directive (test 1120).
- Task lists: src/render/checkboxMarkers.ts, `markTaskList` (1417), test/rendering/checkboxRendering.test.ts.
- HTML tables: SAFE_HTML_TABLE_TAGS (140), `sanitizeTableStyle`, tests 681-758.
- Anchors and labels: `label` in directive nodes (44), target collection (806-810), src/webview/anchorPolicy.ts.
- Colon fences: `:::` directives and nested backtick/colon delimiters (test 333).
- Also present: Mermaid, PlantUML, code-cell, and include directives. Emoji shortcodes and Unicode emoji handling: no support found in the renderer.

Key files: src/webview/scrollSync.ts, src/webview/textEditing.ts, src/webview/markdownTable.ts, src/preview/previewStyles.ts, src/extension.ts, src/security/csp.ts, src/preview/webview.ts, src/render/mystRenderer.ts, package.json.