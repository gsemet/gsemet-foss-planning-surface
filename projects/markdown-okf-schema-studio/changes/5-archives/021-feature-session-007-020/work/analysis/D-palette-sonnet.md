# D - Edition palette: technical analysis (Sonnet)

Read-only analysis of `.agents/changes/backlog/P1/block-edition-palette/01-intent.md`.
Line numbers refer to the tree on branch `dev/gsemet`; scrollSync.ts line numbers are approximate (+-5)
because the file is 3668 lines and was read in ranges. Items marked UNVERIFIED are reasoning, not observed.

## 1. Current editing infrastructure

### 1.1 Block editor lifecycle (src/webview/scrollSync.ts)
- `openBlockEditor(target, selectedCell, sourceRange, initialCaretPosition)` ~2179. Guard: one editor at a
  time (`if (activeBlockEdit) return`). Creates `div.sphinx-preview-block-editor` (or
  `.sphinx-preview-table-cell-editor`), `role=region`, `data-sphinx-preview-block-editor`, inserted
  `afterend` the rendered target (`renderedTarget.insertAdjacentElement("afterend", element)`), or appended
  INTO the selected `td/th` for cells. Creates `status` `<p role=status data-sphinx-preview-edit-status>`.
  Stores everything in `activeBlockEdit` (target, element, status, editId, line, endLine,
  insertAfterLine, selectedCell, ...). Posts `previewEditOpen` to host. Disables refresh button.
- The textarea does NOT exist yet at open: host answers with `previewEditSource`-type message handled by
  `receiveBlockEditSource` (~2700-2830) which creates `<textarea aria-label="Raw Markdown block"
  spellcheck=false autocorrect/autocapitalize/autocomplete off>` (~2737), sets `textarea.value =
  displayText` (trailing line ending stripped, remembered in `edit.trailingLineEnding`), auto-grows via
  `resizeTextarea` (height=auto then scrollHeight). DOM order inside `edit.element`: textarea, then
  `div.sphinx-preview-block-editor-actions` = [status hint, `div.sphinx-preview-block-editor-buttons` (Done, Cancel)].
  Status hint text from `blockEditHint` (~2650): "Line N - Enter: new line - Tab: indent - Esc: cancel - Cmd+Enter: done".
- IMPORTANT: a palette must be created AFTER the textarea exists (inside `receiveBlockEditSource`), not in
  `openBlockEditor`, and must be removed in `closeBlockEdit`. For the table path the order is
  `renderTableCellEditor(edit)` instead (cell textarea).
- Commit: `saveBlockEdit()` = `postBlockEditSave(true)` (~2240): serialises `textarea.value +
  trailingLineEnding`, posts `previewEditSave` {editId, line, endLine, originalText, editedText, final,
  insertAfterLine, anchor...}; if unchanged and no autosave happened it just `closeBlockEdit()`.
  Autosave: `input` event -> `autosaveBlockEdit()` debounce `AUTOSAVE_DELAY_MS` -> `postBlockEditSave(false)`.
  Flush on `pagehide` / `visibilitychange hidden`.
- Cancel: `cancelBlockEdit()` -> `closeBlockEdit(edit.hasAutosavedChange === true)` (restores original block via
  host if autosave already wrote). Bound to Esc, Cancel button.
- FOCUS TRAP (critical for the palette): `textarea.addEventListener("blur", saveBlockEdit)` (~2765). Any
  focus loss from the block textarea = FINAL SAVE AND CLOSE. Existing Done/Cancel buttons avoid it with
  `mousedown -> preventDefault` (`createEditorButtons` ~2670, comment "keep the focus in the field").
  Every palette button, select, popover item and swatch MUST do the same; popovers with text inputs
  (link panel: text+URL fields, image alt, figure caption) cannot do that (they need focus) -> they need an
  "editor-owned focus" rule: blur handler must ignore focus moving to a node inside the palette/popover
  (use `relatedTarget` + `edit.palette.contains`), the same trick the cell editor already uses.
- Table cell editor uses a softer rule: `commitCellEditorOnFocusLoss` (~2425) defers with `setTimeout(0)`,
  ignores if a pointerdown happened <500 ms ago (`lastPointerDownAt`), and ignores focus inside
  `edit.element` or `edit.tableMenu`. This is the model to generalise to the palette.

### 1.2 How text is changed
- `applyTextEdit(control, edit, onFallbackInput)` ~1448: `control.focus()`, `setSelectionRange(start,end)`,
  `document.execCommand("insertText", false, text)` (or `"delete"` when text empty and range non-empty); falls
  back to manual `control.value = splice` + callback (which calls resize+autosave) when execCommand is
  missing/throws. Then restores `setSelectionRange(selectionStart, selectionEnd)`.
  Consequence: edits via execCommand are in the native undo stack (Cmd+Z undoes one palette action);
  the fallback path is not undoable. A native `input` event fires on the execCommand path, so autosave
  and resize run automatically (the callback is only for the fallback).
  Direct `.value =` assignments elsewhere (e.g. 1077-1990) are frontmatter controls, not the block editor.
- Pure helpers in src/webview/textEditing.ts (stringified into the webview, so bodies must stay
  self-contained, no imports): `TextEdit {start,end,text,selectionStart,selectionEnd}`; `continueOnEnter`,
  `indentSelection`, `wrapSelection` (only `*_\`~`, non-empty selection, marker both sides, selection kept),
  `mapRenderedCaret`. This is exactly the shape the palette `apply()` should return.
- Undo: `keepUndoInControl` ~1398 does `stopPropagation()` for Cmd/Ctrl+Z/Y so the host/workbench does not
  also undo the document (precedent: key events inside the webview DO reach the workbench unless stopped).
- Caveat: execCommand("insertText") with multi-line text works in Chromium textarea; selection after
  insertion is collapsed at end and then overridden by `setSelectionRange`, fine. Collapsed-undo
  granularity: Chromium merges consecutive insertText into one undo step only if typed; programmatic calls
  each create a step (UNVERIFIED, plausible, add a real-input test).

### 1.3 Keyboard handling already bound in the block textarea (keydown ~2776, order matters)
1. `keepUndoInControl` (Cmd/Ctrl+Z/Y -> stopPropagation, native undo)
2. `wrapSelectionInControl` (`*` `_` backtick `~` over a selection; skips isComposing/metaKey, AltGr aware)
3. `navigateBlockEdit` (ArrowUp/Down/Left/Right at boundary -> save and open adjacent block)
4. `homeEndInControl` (Home/End to text start/end)
5. Enter (no modifiers, not composing) -> `continueOnEnter` list/quote/indent continuation
6. Tab/Shift+Tab (no ctrl/meta/alt) -> `indentSelection`; never leaves the editor
7. Escape -> cancel; Cmd/Ctrl+Enter -> done
Not bound: Cmd/Ctrl+B, I, K, `/`, Shift+S, etc. -> free for the palette. Note `wrapSelectionInControl` already
gives `*`/`_`/`~`/backtick wrapping, so italic/bold/strike/code buttons can reuse `wrapSelection`
(bold = two applications of `*` or a dedicated `**` variant; strikethrough needs `~~` = two applications).
Cell input (~2620): same list minus Enter-continuation/indent, plus Tab through cells, arrows between cells,
Enter = save (single-line semantics).
Document-level keydown listeners: Escape for frontmatter (2441) and for cell editors when focus is outside
the editor (2452), Enter on empty doc (2908), Enter/Space activation (3588). A palette with its own
focusable popovers must not collide with the 2452 handler (it already treats focus inside `edit.element` as
inside; the palette lives elsewhere -> extend `inside()` to include `edit.palette`).

### 1.4 Table-cell bar (the thing to merge/shift)
- Built in `renderTableCellEditor` ~2495-2640. `div.sphinx-preview-table-menu` (`role=toolbar`,
  `data-sphinx-table-menu`), created once per cell edit (`edit.tableMenu`), inserted in document flow
  directly BEFORE the `<table>` (or its single-child wrapper div without source-line attribute), fallback
  `document.body`. Contains 4 buttons (Row +, Row -, Col +, Col -, groups `row`/`column`, each icon + text
  label, `data-sphinx-table-operation`) then `edit.status` ("Header - column 2 of 4" / "Row 1 of 3 - ..."). CSS
  `.sphinx-preview-table-menu` previewStyles.ts:682: static, flex-wrap, pill radius 18px, `editorWidget-background`,
  border `--vscode-widget-border`, shadow `0 2px 9px`, `width:max-content; max-width:100%`.
- Its buttons do NOT `preventDefault` on mousedown; they rely on `commitCellEditorOnFocusLoss` tolerance.
- `revealTableToolbar`/`toolbarUsableTop` (2466-2500) keep the bar visible under the sticky heading band and
  the fixed floating toolbar by scrolling; the palette needs the same logic (generalise to "edit bar").
- Cell content is ONE logical Markdown table cell (`|` and newlines are significant). Only inline actions are
  valid in a cell editor (bold/italic/strike/code/link/image/emoji/sub/sup/color). Block actions
  (headings, quote, hr, table, fences, admonitions, lists, checkbox) must be disabled via the `modes`/`scopes`
  field of the registry. In a pipe table a literal `|` in inserted text must be escaped (`\|`) - the registry
  `apply` needs a `scope: "cell"` post-processor.

### 1.5 Host side (src/extension.ts)
- Messages validated in `isPreviewSyncMessage` ~400-590 with a hard whitelist of `message.type` (line 412-425).
  Any new message type (image pick, history, zoom, margin) must be added there AND in the handler chain
  starting ~2340-2450 (`handlePreviewSyncMessage`). Edits go through the edit lock (`preview.editLock`,
  `activeBlockEdit`) and a WorkspaceEdit; `previewReady` releases the lock when the page reports no editor.
- State persistence precedents: theme mode = session variable + `workspaceState` (`readPreviewThemeMode`/
  `writePreviewThemeMode`, 337-345, 3237-3244); edit mode = `workspaceState` key
  `markdownOkfSchemaStudio.editMode` (283, 917 `initialEditMode`, 2361); per-document description collapse =
  bounded map in workspaceState (280); anchor mode = webview `vscode.setState` + settings; webview-local state
  via `vscode.getState/setState` (scrollSync ~93, 166, 756). Webview created with
  `retainContextWhenHidden: true` (3252, 2992), so webview state survives tab switches but not reloads.
- No existing `showOpenDialog`, no image-insertion code (grep: none). Backlog items `paste-image-in-edit-mode`
  and `edit-inline-image` are neighbours and should share the host helper.

### 1.6 Does VS Code swallow Ctrl/Cmd+K, +/, +B, +I in a webview textarea?
- package.json contributes ONE keybinding: `ctrl+k shift+v` / `cmd+k shift+v` for openPreview with
  `when: editorTextFocus && resourceExtname == .md` (package.json:80-87). `editorTextFocus` is false while a
  webview has focus, so it does not fire there and does not interfere. No other contributed keybindings.
- Reasoning about the platform (UNVERIFIED in this repo, from knowledge of VS Code's webview host): the
  webview iframe forwards keydown events to the workbench keybinding service (`did-keydown`), so workbench
  keybindings whose `when` clause is satisfied with a webview focused DO run. Evidence inside this repo that
  forwarding is real: `keepUndoInControl` calls `stopPropagation` for Cmd+Z/Y precisely to stop it.
  Consequences: Cmd/Ctrl+K is the workbench chord prefix (global, no `when`), so pressing it in the webview
  will likely open the "waiting for second key" chord state UNLESS the textarea handler calls
  `preventDefault()` + `stopPropagation()` (and keydown reaches the textarea first, which it does as the
  target). Cmd+B (toggle sidebar), Cmd+I (differs by version: chat/inline chat/italic-like), Cmd+/ (commentLine:
  needs editorTextFocus, so not triggered in a webview) are global-or-editor-scoped; stopPropagation should
  suffice for the global ones. Cmd+Shift+K/others avoid problems but diverge from the intent text.
  `Ctrl+/` on non-US layouts: use `event.code === "Slash"` OR `event.key === "/"`; AZERTY needs Shift.
- Required action: manual check in a real VS Code (integration tests use Playwright/Chromium via
  `page.keyboard` in test/integration/realInput.test.ts, which cannot reproduce workbench forwarding). Add a
  checklist item to the manual QA skill, and implement defensively: preventDefault + stopPropagation for every
  palette shortcut, and expose all shortcuts as editable only through the palette (no package.json keybinding
  needed because they are webview-local).

## 2. Syntax supported by the renderer today (evidence)

Renderer: src/render/mystRenderer.ts, engine `myst-parser` `mystParse` + `myst-to-html` `mystToHtml`
(line 1466), plus alert pre-pass `expandGithubAlerts` (397-445), checkbox pre-pass
(`prepareCheckboxMarkers`, src/render/checkboxMarkers.ts), math via KaTeX (src/render/mathRenderer.ts),
sanitiser src/security/html-sanitizer.ts.

| Feature | Supported | Evidence |
|---|---|---|
| Admonitions, MyST `:::{note}` ... all named types (attention caution danger error hint important note seealso tip warning) | yes | titles map mystRenderer.ts ~105-114; test mystFeatures.test.ts:496 "all named MyST admonitions" |
| Generic `{admonition}` + custom title + `:class:` | yes | tests :310, :530 |
| Sphinx versionadded/versionchanged/deprecated | yes | :272, VERSION_ADMONITION_TITLES 117 |
| Dropdown admonitions (`:class: dropdown`) -> details | yes | :580 |
| Quarto callout classes | yes | :559 |
| GitHub alerts `> [!NOTE]` NOTE TIP IMPORTANT WARNING CAUTION, optional title | yes | GITHUB_ALERT_TYPES 122-128, ALERT_MARKER 130, tests :396,:417; CRLF crlfAlerts.test.ts |
| `> **Note**` bold markers (Note/Important/Warning only) | yes | GITHUB_BOLD_ALERT_MARKER 131, test :437 |
| Colon fences `:::` and nesting with backtick fences | yes | test :333 |
| Footnotes `[^a]` / `[^a]: text` | yes | test :463 (id `user-content-fn-hr`) |
| Definition lists `Term\n: Def` | yes | test :463 (`dl`) |
| `{sub}` / `{sup}` / `{abbr}` roles | yes | test :463. NOT supported: `~sub~` / `^sup^` shorthand (no evidence anywhere; treat as unsupported) |
| Math `$..$`, `$$..$$` (dollarmath), `{math}` | yes | contract test :65 (math-inline/math-display), mathRenderer.ts, fixtures 01/05 `$$` |
| amsmath `\begin{align}` | NOT PROVEN | no test or fixture found; myst-parser supports it when enabled but must be verified before a palette button ships |
| Figures `:::{figure} img` with `:alt:`, `:name:`, caption, and `{image}` | yes | tests :111,:1094,:1120; mapped block ranges |
| Figure `:width:` / `:align:` options | NOT PROVEN | parser supports them; no repo test; CSS handling unknown. Needed for the "Figure (size...)" editor |
| Task lists `- [ ]` / `- [x]` + click toggle | yes | checkboxMarkers.ts, checkboxRendering.test.ts, `previewCheckboxToggle` message |
| GFM tables, MyST `{table}` captions/alignment | yes | :610 |
| Raw HTML tables (colspan/rowspan), safe `style` subset | yes | :681, :709, sanitizeTableStyle html-sanitizer.ts:70 |
| `<details><summary>` raw HTML | yes | :1007 |
| Labels / anchors `(name)=` | NOT PROVEN | renderer only mentions `mystTarget` as a literal-markup guard (1323-1326); no test; no anchor icon in preview. The intent's "anchors edition" is a NEW rendering feature (rendered marker + click-to-edit), not just an insert |
| Heading ids `{#id}` | partially | only in navigation (markdownFragmentRange, previewNavigation.ts) |
| Strikethrough `~~x~~` | NOT PROVEN | no test mentions `<del>`/`~~` (only crlfAlerts fence usage). myst-parser GFM strikethrough support must be verified |
| Emoji shortcodes `:smile:` | NO | no emoji handling in src/render. Emoji picker should insert the Unicode character, not a shortcode |
| Inline colour `<span style="color:..">` | NO | sanitiser strips `style` on everything except tables: html-sanitizer.ts:233 (`name === "style"` removed, diagnostic `blocked-inline-style`) |
| `<kbd>`, `<mark>` | not proven | not in tests; sanitiser allow-list not located |
| Code fences with language, highlight | yes | src/render/highlight.ts, tests :163 |
| Mermaid / PlantUML fences | yes | :222,:245 |
| Wikilinks `[[note]]` | yes | :49 |
| Hex colour swatch preview in text | no | the "html color picker (self-activated when a colour code is detected)" requires a new inline renderer feature or a palette-only overlay |

Flags (palette would insert something that does not render today -> per the intent, each becomes a feature):
colour (text/background), emoji shortcode (avoid), strikethrough (verify), `~sub~/^sup^` (avoid; use `{sub}`),
amsmath (verify), figure width/align (verify), label anchors `(name)=` (needs rendering + icon), hex swatch,
TODO indicator (no definition exists; see ambiguity 10).

## 3. Proposed architecture

### 3.1 Module layout (keep the "stringified factory" constraint)
- `src/webview/editActions.ts`: pure registry + `apply` functions, exported as
  `createEditActions()` factory (self-contained, like `createTextEditingTools`). Unit-testable under
  test/webview without DOM.
- `src/webview/editPalette.ts`: DOM builder `createEditPalette(deps)` (also stringified; deps injected:
  `document`, `applyTextEdit`, `getControl`, `postHost`, `keepFocus`). scrollSync.ts only wires: create on
  textarea creation, destroy in `closeBlockEdit`, call from the keydown chain.
- `src/preview/editPaletteStyles.ts` or a section in previewStyles.ts (the file is 2198 lines; a new const
  appended to the same CSS list is lower-risk than a new bundle pipeline).

### 3.2 Action registry
```
interface EditAction {
  id: string;                         // "bold", "link", "admonition-gfm", ...
  label: string; icon: string;        // inline svg string, same style as toolbar icons
  shortcut?: { key: string; code?: string; mod: true; shift?: boolean };  // Cmd on mac, Ctrl else
  syntaxes: ("strict"|"gfm"|"myst")[]; // modes in which the button is shown; gfm implies strict, myst implies gfm
  scopes: ("block"|"cell")[];          // cell = inline only
  group: "text"|"insert"|"block"|"extra";
  popover?: "heading"|"language"|"grid"|"alert"|"link"|"emoji"|"color"|"figure";
  apply(ctx: {value, selectionStart, selectionEnd, scope, arg?}): TextEdit | undefined;
  hostRequest?: "pickImage";           // async path
  available?(ctx): boolean;            // e.g. disabled for multi-line selection
}
```
`apply` returns the existing `TextEdit` so everything goes through `applyTextEdit` (one native undo step,
autosave via `input`). Extensibility = `registry.register(action)` and a data-driven palette render
(`groups -> buttons`), so "every unsupported edition => new feature" means adding an action + a renderer test.
Action behaviours worth specifying: toggle semantics (bold on already-bold text unwraps; reuse the
`wrapSelection` marker logic generalised to marker strings), line-prefix actions (heading, quote, list,
checkbox) operate on the line range touched by the selection (copy the line-walk from `indentSelection`),
heading replaces an existing `#+ ` prefix, fenced code wraps selection or inserts a fence pair with caret
inside, link: selection -> `[sel](|)` caret in URL, empty -> `[|]()` (matches "caret placed at link location").
Respect surrounding context: the block under edit is the whole block source, so "blockquote" on a list item
etc. must compose prefixes (`> ` before list markers, like the `quote` regex in `continueOnEnter`).
Block-level inserts on a multi-block context: the editor holds ONE block, so inserting a table or HR in it makes
the block multi-block; the next render splits it fine (the "New block" insert-point editor already does that).

### 3.3 Mode select (strict / GFM / MyST)
- Show/hide button groups by `syntaxes`. Add `data-syntax` on the palette root for CSS.
- Persistence: recommend a global preference in `workspaceState` like edit mode (key
  `markdownOkfSchemaStudio.editSyntax`), seeded into the page as `context.initialEditSyntax` exactly like
  `initialEditMode` (extension.ts:917) and mirrored in `vscode.setState`. Add a message
  `previewEditSyntaxChanged` (whitelist in isPreviewSyncMessage). Plus an optional contributed setting
  `markdownOkfSchemaStudio.editing.defaultSyntax` ("strict"|"gfm"|"myst", default "myst") used when nothing is
  stored. Not per-document by default (a project is almost always one flavour), but allow later per-document
  override from frontmatter or `.okf` config (out of scope).
- Auto-default heuristic (optional): if the document contains `:::{` or `{role}` choose myst.

### 3.4 Placement and the table bar
- Block editor: palette is a sibling inserted BEFORE the editor frame (in flow, like the table menu), i.e.
  `edit.element.insertAdjacentElement("beforebegin", palette)`. In-flow keeps layout predictable and avoids
  position:fixed + sticky heading overlap problems; scroll anchoring already handles an inserted element via
  `beginEditAnchor`/`applyAnchor`, but the palette creation must happen before `applyAnchor()` runs (or be
  followed by one) so the text line does not jump. Reuse the pill style of `.sphinx-preview-table-menu`
  (radius 18px, editorWidget bg) for harmony, 2 rows allowed (`flex-wrap`).
- Table cell: RECOMMEND MERGE, not stack: one bar above the table = `[row/col ops group] | [inline palette
  group (scope=cell)] | status`. Reasons: the table menu already sits in flow above the table; a second bar
  would double the height shift above an edited cell, and the cell's own textarea is tiny. Implementation:
  render the palette inline group into `edit.tableMenu` in `renderTableCellEditor` (the menu is cleared and
  rebuilt there on every op, so the palette group is rebuilt too). Fall back to shift/wrap (flex-wrap) at
  narrow width, as the menu already wraps. Keep the existing `data-sphinx-table-operation` buttons untouched
  (tests at scrollSync.test.ts:1894, :2011 assert them).
- Palette buttons: `mousedown preventDefault` always. Selection preservation: since the textarea keeps focus
  and selection (mousedown prevented), `selectionStart/End` are still valid at click time.
- Popovers (heading level h1-h5, language list, 9x9 table grid, alert type, emoji, colour, link panel,
  figure editor): absolutely positioned child of the palette, `role=menu/dialog`, closed on Esc (the Esc must
  close the popover first and only then cancel the edit: intercept in the textarea keydown BEFORE the
  existing Escape branch), outside pointerdown, and on edit close. Heading/language/alert/grid popovers are
  pointer-only lists (mousedown prevented, keep focus). Link and figure panels have inputs and need real
  focus -> rely on the relaxed blur rule from 1.1 (ignore focus moving into `edit.palette`), and on commit
  re-focus the textarea and restore the saved selection (save selection on open since a blurred textarea keeps
  `selectionStart` anyway).
- 9x9 table grid: 81 buttons or one canvas-like `div` grid with hover highlight via CSS `:has`/JS; output a
  GFM pipe table skeleton (header row + separator + N rows) using the same table serialiser as
  src/webview/markdownTable.ts (`serialize`) so alignment/escaping is uniform. Use hover through
  `mouseover` on the grid container (event delegation), selection on `click`.
- Image: webview -> host `previewPickImage {editId}`; host `vscode.window.showOpenDialog({defaultUri:
  dirname(document), filters images})`, computes a POSIX relative path (`path.relative` of document dir,
  `split(path.sep).join("/")`, encode spaces as `%20` or wrap in `<>`), validates against the workspace root /
  resource policy (src/security/resource-policy), posts back `previewPickedImage {editId, relativePath, alt}`
  which the webview turns into `![alt](path)` (strict/gfm) or `:::{figure} path` (myst, per ambiguity 6).
  Must go through the whitelist in isPreviewSyncMessage, check `matchesCurrentPreview` and that the edit is
  still active (same editId) before applying. Cancelled dialog = no-op. Note that the picker steals focus from
  the webview -> the blur handler fires `saveBlockEdit` (final save, editor closes). The picker call is made by
  the HOST, so the webview blur happens when the native dialog opens: set `edit.suspendBlurCommit = true` before
  posting the request, clear it on the reply or on 30 s timeout. The same flag serves the emoji picker if it
  uses a native input.
- Emoji picker: webview-only grid of curated Unicode emoji (no network, CSP safe), inserting the character.
- Colour picker: since inline style is stripped by the sanitiser, the feature needs a renderer decision
  (ambiguity 7) before UI work.

### 3.5 Shortcuts
Cmd/Ctrl+B bold, +I italic, +K link, +Shift+X strikethrough (GitHub uses Cmd+Shift+X), +E inline code (avoid
Cmd+`), +/ -> TODO (see ambiguity 10; handle `event.code === "Slash" || event.key === "/"`). All via a
single `paletteShortcut(event)` placed after `keepUndoInControl` and BEFORE `wrapSelectionInControl`, guarded
by `!event.isComposing`, `event.preventDefault(); event.stopPropagation()`. In cell scope only inline actions
respond. Do not touch Cmd+Enter / Esc / Tab.

## 4. Toolbar additions (src/preview/previewToolbar.ts, scrollSync.ts)

Current toolbar: 4 round 30px buttons in `div[data-sphinx-preview-toolbar]` `position:fixed; top:12px;
right:14px; z-index:1100; display:flex; gap:2px; padding:3px; radius 18px` (previewStyles.ts:271-330), built
by `renderPreviewToolbar(editingEnabled)` (15 lines) = refresh, anchor, edit (only if editable), theme. Width
feeds `--sphinx-preview-toolbar-width` for the sticky headings (scrollSync.ts ~423) and `toolbarUsableTop`.
Wired by `querySelector` at scrollSync.ts:88-91. Tooltip is CSS `data-tooltip` (353-405).

### 4.1 Two rows
Convert to `flex-wrap: wrap` with a fixed `max-width: calc(2*30px+...)`? Simpler: two child rows
(`div[data-row=nav]`: back, next, zoom out, zoom in(+reset on click of the percent), margin; and
`div[data-row=view]`: refresh, anchor, theme, edit) so the pill becomes a rounded rectangle (radius ~14px) with
column layout. Row 2 (edit palette entry points) stays free. Checks: sticky-headings width variable (height
changes too: `toolbarUsableTop` uses `controls.bottom`, so automatically handled), pending overlay at
`top:58px` (previewStyles.ts ~300) will overlap a 2-row toolbar -> move to ~`96px`; table menu
`toolbarUsableTop` logic ok; narrow widths (<640 px, descriptionsCollapsed default) - row 1 must wrap itself.
Keep existing button `data-*` hooks untouched; tests in previewStyles.test.ts (33 KB) and
creamTheme.test.ts assert toolbar CSS/DOM and will need updates.

### 4.2 Back / Next
- Findings: clicking a link posts `previewLink {request}` (linkNavigation.ts:`activate`, ~50-60) -> host
  `handlePreviewLink` (extension.ts:2227). Three outcomes: (a) `anchor` -> posts `navigateAnchor` back to the
  webview which scrolls (scrollSync ~3382); (b) `external` -> `vscode.env.openExternal` (no history entry);
  (c) local file -> `vscode.commands.executeCommand("vscode.open", uri, {viewColumn, preview:false,
  selection})`, i.e. it opens a TEXT editor tab; the side preview then switches via
  `onDidChangeActiveTextEditor -> followActiveEditor -> switchPreviewDocument` (extension.ts:3220, 2514).
  A custom-editor preview (`markdown-okf-schema-studio.editor`, priority "option") would instead be a
  separate tab. So there is no history today and "document switch in the same panel" is a host-side event.
- Design: host-owned history per `ActivePreview` ( `{back: Entry[], forward: Entry[]}`, `Entry =
  {documentUri, anchorLine, scrollFraction}` ), pushed in `handlePreviewLink` immediately BEFORE navigating
  (for both anchor and local-file kinds; use the webview's reported anchor line `preview.anchor.line`), and
  cleared of forward entries on a new push. Back/Next buttons post `previewHistoryBack/Forward`; host pops,
  opens the document (`vscode.open` with `selection` or, if same document, posts `navigateAnchor`/a new
  `restoreAnchor` with the saved line). Guard against re-push loops: a `navigatingFromHistory` flag so
  `followActiveEditor`/`switchPreviewDocument` do not record. Host posts `previewHistoryState
  {canBack, canForward}` so the buttons can be `disabled` (like `refreshButton.disabled`).
- Webview-only alternative for in-page anchors (cheap): history of `{scrollY/line}` pushed on `navigateAnchor`
  and on in-page `a[href^="#"]` clicks, stored in `vscode.setState` -> survives context loss with
  `retainContextWhenHidden`. Recommend the host-owned unified stack (one source of truth) rather than two.
- Edge cases: blocked/failed navigation must not push; unsaved block edit must be committed before leaving
  (existing `switchPreviewDocument` handles active edit via edit lock? verify); history size cap (e.g. 50);
  persistence across reload is not needed (in-memory).
- Not to be confused with VS Code `workbench.action.navigateBack`: it navigates editor location history of
  the text editor, which would work partially for file switches but not for in-page anchors. Not recommended.

### 4.3 Zoom
- Only font-size variable exists: `--sphinx-preview-font-size: var(--vscode-markdown-font-size, 14px)`
  (previewStyles.ts:114). Recommend a multiplier variable `--sphinx-preview-zoom` applied as
  `font-size: calc(var(--vscode-markdown-font-size, 14px) * var(--sphinx-preview-zoom, 1))` rather than CSS
  `zoom` (non-standard; it changes `getBoundingClientRect` semantics, which would break the line/scroll
  anchor maps in anchorPolicy.ts and the layout cache in scrollSync). With the font-size route, all `em`/`rem`
  derived sizes scale, but px-sized pieces (images' natural size, code `12px` toolbars at lines 301/372,
  max content width px, gutters) do not: decide whether zoom scales the column width too (recommend: scale
  `max-width` by the same factor, i.e. use `em`-based width or multiply the var).
- Steps 80/90/100/110/125/150/200 %, persisted like theme mode: `workspaceState` key
  (`markdownOkfSchemaStudio.previewZoom`) + `previewZoomChanged` message + `initialZoom` in the page context +
  `vscode.setState`. Global (not per document). Reset by clicking the percentage label or Cmd+0 when
  preview focused. After change: call the existing layout stabilisation (`stabilizeLayout`) and re-restore the
  scroll anchor, as in resize. Also Cmd/Ctrl+wheel optional (out of scope).
- Do NOT use the workbench `window.zoomLevel`; unrelated.

### 4.4 Margin toggle
- Today: setting `markdownOkfSchemaStudio.preview.maxContentWidth` (default 960, 0 = full width, max 2400)
  -> `:root{--sphinx-preview-content-max-width: ...}` via `previewContentWidthCss`
  (previewStyles.ts:2194; used at lines 423-424 sticky band and 1229 content). The intent "switch left/right
  margin on/off" = a runtime override of that variable; recommended semantic: toggle between "configured width"
  and "full width" (variable `none`), state stored like zoom (`workspaceState`), overriding the setting
  until reset. It overlaps the backlog item `clever-margin-break` which wants THREE states: margin /
  auto-margin (wide tables and figures break out of the column) / full width. Recommend implementing the
  toggle as a 3-state cycle from the start (`data-margin-mode="margin|auto|full"` on `<html>`, CSS selects
  `table`, `figure`, `.myst-*-figure` with `margin-inline: calc(50% - 50vw)`-style breakout in auto mode),
  but ship P-phase 1 with 2 states (margin/full) and the attribute contract so clever-margin-break only adds
  CSS. The sticky-heading band padding and `--sphinx-preview-toolbar-width` use the same variable, so
  they follow for free (lines 423-424).
- Note "left/right margin" in the intent: the content is centred (`max-width` with auto margins); the toggle
  removes both. A one-sided toggle is not supported by the current CSS and is not recommended.

## 5. Phased plan

P1 - Registry core + inline shortcuts (size S). Scope: `editActions.ts` with bold/italic/strike/inline-code/
link actions (generalised `wrapSelection` with marker strings + toggle), keyboard path `paletteShortcut`
(Cmd/Ctrl+B/I/K/Shift+X), no UI yet. Files: src/webview/editActions.ts (new), textEditing.ts (generalise
wrap, keep signature), scrollSync.ts (keydown chain, 3 lines + factory injection like `textEditing`). Tests:
new test/webview/editActions.test.ts mimicking textEditing.test.ts; keydown behaviour tests in
test/webview/scrollSync.test.ts next to "Tab and Shift+Tab indent..." (:1529); a realInput.test.ts case
(Cmd+B on selection, then Cmd+Z). Risks: IME (guard `isComposing`), VS Code swallowing (manual check),
undo granularity (execCommand), AltGr (`event.ctrlKey && altKey`).

P2 - Palette bar for block editor, single row, inline + line-prefix actions (size M). Scope: DOM builder,
CSS, mousedown guard, blur relaxation (`edit.palette`), lifecycle (create on textarea creation, destroy on
close), actions: heading dropdown, quote, hr, list/ordered, checkbox, code fence (language popover), link
button (inserts `[sel](|)` only, panel later). Files: editPalette.ts, previewStyles.ts, scrollSync.ts
(receiveBlockEditSource ~2737, closeBlockEdit, Escape handler for popover-first), extension.ts none. Tests:
scrollSync.test.ts (palette present only in edit mode, buttons keep focus and don't close editor,
popover Esc closes popover not edit, cell editor shows inline group only), previewStyles.test.ts (CSS
tokens for dark/light/cream via creamTheme.test.ts pattern), visual scenario in test/visual/scenarios.ts
(new `editPalette` flag next to `editAffordances` + a fixture). Risks: focus/blur final-save (biggest),
scroll anchor jump when the palette is inserted (use `beginEditAnchor`), sticky heading overlap, narrow
width wrapping, edit lock/content patch (palette lives inside page DOM: confirm src/preview/contentPatch.ts
leaves nodes with `data-sphinx-preview-block-editor`; the palette must either live inside that node
or carry an equivalent marker or the incremental patch may remove it), dark/light/cream tokens.

P3 - Table cell merge (size S). Scope: render inline group into `edit.tableMenu` for `scope=cell`, escape `|`,
disable block actions. Files: scrollSync.ts `renderTableCellEditor`. Tests: extend scrollSync.test.ts
:1894/:2011 style (operations still present, palette group present, Enter still saves). Risks: bar width at
narrow widths (already wraps), `commitCellEditorOnFocusLoss` 500 ms heuristic, cell content containing `|`.

P4 - Mode select (strict/GFM/MyST) + persistence (size S-M). Files: palette, extension.ts (message whitelist
~412, handler ~2361, `initialEditSyntax` ~917), package.json setting, src/preview/webview.ts context.
Tests: new cases in test/webview, extension-level test mimicking edit mode persistence
(test/integration/previewEditing.test.ts, lifecycle.test.ts), config schema test in test/configuration.
Risks: message whitelist forgotten (silently dropped), page reload keeps old value.

P5 - Table grid, image picker, emoji, GFM admonition, html-table conversion (size M-L). Image requires host
round trip + blur suspend flag; admonition inserts `> [!NOTE]` (GFM) with dropdown at caret; "markdown table
-> html table" converter reusing `markdownTable.ts` parse. Files: editActions.ts, palette, extension.ts
(`previewPickImage`), markdownTable.ts (+ `toHtml`). Tests: markdownTable.test.ts (`toHtml`), mystFeatures
render check that every inserted snippet renders (a contract test: for each registry action, apply to a
sample and render with `renderPreviewDocument`; fails if output contains the literal syntax) - this
operationalises "every non-supported edition => new feature". Risks: relative path computing on Windows
(path separators, spaces, `..` outside workspace -> resource policy), native dialog stealing focus, image
alt escaping, IME.

P6 - MyST group (size M). admonitions all types + custom, footnote (insert ref at caret + definition at
block end: block-scoped; definition must live at doc level - decide, see ambiguity 8), deflist, math
inline/block, `{sub}/{sup}`, figure with caption, anchor `(name)=`. Requires renderer work for the NOT PROVEN
rows in section 2 (anchor icon, amsmath verification, figure width). Tests: mystFeatures.test.ts additions.

P7 - Toolbar: two rows + back/next + zoom + margin (size L overall; can be split: 7a two rows + zoom +
margin XS-S; 7b history M). Files: previewToolbar.ts, previewStyles.ts, scrollSync.ts, extension.ts
(history stack, 3 new message types, whitelist), package.json (none for first cut). Tests:
test/webview/linkNavigation.test.ts (history push on anchor/link), previewStyles.test.ts (2-row layout,
variables), extension integration (history after two link navigations, back restores doc and line),
visual scenarios at 360/640/1200 px, three themes. Risks: sticky heading toolbar width variable, pending
overlay offset, scroll anchor after zoom, forward-stack cleared properly, history entries for deleted files.
NOTE: P7a is independent of P1-P6 and can run in parallel or first (it touches different regions).

P8 - Custom editors (size L): figure editor panel, colour picker (blocked by sanitiser decision), link
panel (text+URL, double field), anchor edit icon (needs renderer). Tests as above.

Regression-risk checklist for every phase: IME composition (never act on keydown/paste while
`isComposing`; for palette click while composing, ignore), undo (always `applyTextEdit`), incremental
content patch + edit lock (contentPatch.ts must not clobber the palette), narrow widths and wrapping,
dark/light/cream (use `--vscode-*` tokens + cream overrides as in creamTheme.test.ts), sticky headings
(`toolbarUsableTop`), selection scroll anchoring (`beginEditAnchor`/`applyAnchor`), `Esc` ordering, blur =
final-save trap, `previewReady` lock release when the editor has no textarea yet.

## 6. Ambiguities needing decisions (recommended default)

1. Mode semantics: is GFM a superset of strict and MyST a superset of GFM (intent: "MyST incl. GFM")?
   Default: yes, additive groups, strict buttons always visible.
2. Persistence scope for mode: global (workspaceState) vs per document. Default: global workspaceState +
   `editing.defaultSyntax` setting, default value myst.
3. Table-cell bar: merge or shift. Default: merge (one bar, row/col ops + inline palette), wrapping on
   narrow widths.
4. Palette placement: in flow above the block (default) vs floating `position:fixed` under the main toolbar
   ("floating palette below the existing one" in the intent's first sentence). Default: in flow above the edited
   block (matches "Placement: on top of the block under edition"), and drop the "below the toolbar"
   sentence as superseded.
5. Shortcuts conflicts: Cmd/Ctrl+K may open the workbench chord. Default: preventDefault+stopPropagation,
   verify manually; if swallowed, fall back to Cmd+Shift+K and document it.
6. Image in MyST mode: plain `![alt](path)` or `:::{figure}` with caption. Default: `![alt](path)` for the
   image button; separate Figure button for the directive.
7. Colour picker: needs inline style, which the sanitiser strips (html-sanitizer.ts:233). Options: allow a
   restricted `color`/`background-color` on `span` (hex only) or MyST role/class. Default: allow a restricted
   `span style` (hex/rgb only, same pattern as `sanitizeTableStyle`) and emit `<span style="color:#rrggbb">`;
   defer to P8.
8. Footnote insertion in a single-block editor: definition `[^n]: ...` must be at document level. Default:
   insert the reference at the caret and append the definition at the end of the current block (renders fine
   in MyST), numbered by scanning the host-provided document, else `[^1]` collision risk; confirm.
9. Emoji: Unicode character vs shortcode. Default: Unicode (shortcodes do not render).
10. "TODO indicator ... self activate on Ctrl+/": what text does it insert (`<!-- TODO -->`, `TODO:`,
    `- [ ]`) and how is it rendered? Backlog `todo-comments` exists. Default: toggle a `<!-- TODO: -->`
    comment at line start; render marker is out of scope until that backlog item is specified.
11. "html color picker self-activated when a colour code is detected": default = show a swatch button in the
    palette when the caret/selection is inside `#rgb|#rrggbb|rgb(...)`, clicking opens the picker and replaces
    the code; no inline rendered swatch.
12. Back/Next scope: documents only, or also in-page anchors? Default: both, one host-owned stack; external
    links never recorded.
13. Zoom: scope (global vs per document) and whether it scales the content column. Default: global,
    scales text and column width (multiplier), range 70-200 %, step 10 %.
14. Margin toggle states: 2 (margin/full) now or 3 with clever-margin-break. Default: ship 2 with the
    `data-margin-mode` contract and add `auto` in the clever-margin-break item.
15. Which highlight languages in the code dropdown. Default: the list actually supported by
    src/render/highlight.ts (read it before building; do not offer languages that do not highlight) plus
    "plain text".
16. Strikethrough and amsmath: verify support before shipping the buttons; if unsupported, either add
    rendering or hide the button. Default: verify in P1/P6 with a render test; hide until proven.
17. Anchors edition (`(name)=` icon, click to edit): requires new preview rendering; separate backlog
    item or P8? Default: P8, after label rendering exists.
18. Palette in the frontmatter editor, properties cells and the "Start writing" insert-point editor: out of
    scope except the insert-point editor, which uses the same textarea path (default: yes, palette shows
    there as well; frontmatter: no).
19. Edit mode only: palette visible only while a block editor is open (default) vs always visible in edit
    mode (disabled when no editor). Default: only with an open editor, to avoid layout noise.
