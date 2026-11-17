# B - Block operations analysis (planning only, no implementation)

Scope: move-block-up-down, edit-inline-image, multibloc-selection, paste-image-in-edit-mode.
Line numbers are from the working tree at analysis time (branch dev/gsemet). Items marked
"UNVERIFIED" were inferred from reading, not run.

## 0. Shared current state (applies to all four)

### Message protocol webview <-> host
- Webview -> host (src/extension.ts:412-425, `isPreviewSyncMessage`, strict allowlist + per-field
  validators): `previewEditOpen`, `previewEditSave` (autosave every 400 ms, `final:true` on exit),
  `previewEditCancel`, `previewFrontmatterSave`, `previewCheckboxToggle`, plus scroll/state/link
  messages. Edit requests require `editId` plus `line` and `endLine >= line` (extension.ts:455-470).
  `insertAfterLine` is only legal on EditOpen/EditSave/EditCancel (extension.ts:471-477).
  Any new message type MUST be added to this allowlist and validators, or it is silently dropped.
- Host -> webview: `previewEditSource` (carries `originalText` = raw source of the range, or
  `originalText:""` for an insertion, or `error`), `previewFrontmatterResult`, checkbox result.
  Errors for block edits go through `postEditSourceError` (extension.ts:1565).
- Webview side: `openBlockEditor` (scrollSync.ts:2179) builds the `div.sphinx-preview-block-editor`,
  posts `previewEditOpen` (2240); `receiveBlockEditSource` (2692) creates the textarea, trims the
  trailing line ending into `edit.trailingLineEnding` (2709) and re-adds it on save (2263);
  `postBlockEditSave` (2252) posts `previewEditSave` with `originalText` + `editedText`.
- Host: `handlePreviewEditOpen` (extension.ts:1640) -> `currentSourceEdit` (1340) ->
  `sourceRangeForLines` (src/mapping/sourceMapping.ts:35). `handlePreviewEditSave` (1809) re-reads
  the range, compares with `originalText` (stale check), creates an `ActiveBlockEdit`,
  `beginActiveBlockEdit` acquires the EditLock (src/state/editLock.ts) so renders are deferred.
  `drainActiveBlockEdit` (1741) applies one `WorkspaceEdit` per autosave using `minimalReplacement`
  (src/mapping/textDiff.ts). Concurrency guard: only ONE block edit at once
  (`"Another Markdown block is already being edited."`, 1641). `completeActiveBlockEdit` releases
  the lock and refreshes.
- Staleness guard everywhere: `currentPreviewDocument` (extension.ts ~1325) requires
  `document.version === message.documentVersion`, same doc key, `isDocumentEligible`.

### How a block's source range is computed
- Renderer: mdast `position.start/end.line` -> `data-line` / `data-end-line`
  (src/render/mystRenderer.ts:483-490 `sourcePositionProperties`); sanitizer
  (src/security/html-sanitizer.ts:323-345 `injectSourceMappings`) renames to
  `data-sphinx-source-line`, `data-sphinx-source-end-line` (falls back to `line` when absent/invalid),
  adds source-file, `data-sphinx-preview-document`, `data-sphinx-preview-block`, and `tabindex=0`
  on non-focusable mapped elements. Ranges are 1-based inclusive line numbers.
- `sourceRangeForLines` converts to offsets: start = start of `startLine`, end = start of
  `endLine+1` (so the range INCLUDES the last line's line break) or `text.length` for the last line
  without newline. Handles `\r\n`, `\n`, `\r`.
- Blank lines BETWEEN blocks belong to no block: a block range never contains the blank separator
  lines. That is why the webview strips `trailingLineEnding` and the insertion planner adds
  `prefix = EOL+EOL` after the anchor line (src/mapping/insertion.ts:59-63) and `suffix = EOL` when
  non-blank text follows immediately.
- Top-level mapped block (webview): `topLevelMappedBlocks()` (scrollSync.ts:1242) = elements with
  source attrs for the ACTIVE source file/document, minus those having a mapped ancestor, sorted by
  `data-sphinx-source-line`. Frontmatter properties table is a mapped block with
  `data-okf-properties` and is excluded from the "body" set in `refreshInsertPoints` (2942).
- Nested blocks: list items, admonition/directive bodies, table rows/cells are mapped (children get
  `data-line`) but are not top-level, so click editing never edits them alone:
  `editingElementFor` (3171) widens any click inside `ul/ol` to the WHOLE list via
  `sourceRangeForList` (3143, min/max over mapped descendants); table cells open the table-cell
  editor on the whole table range (`openMappedEditor` 3222, `tableTools` model); a click inside an
  admonition opens that whole directive block (mapped outer element is the closest mapped ancestor
  of the click target, found with `target.closest(mappingsSelector)` at 3514+; UNVERIFIED for
  nested mapped children: closest() returns the INNERMOST mapped element, so a click on a
  paragraph inside an admonition may select the inner paragraph's range - check
  `editHoverTarget` 2845 and the click handler 3532-3575 before relying on "whole directive").
- ArrowUp/ArrowDown/Left/Right block-to-block navigation: `boundaryNavigation` (1280),
  `adjacentMappedBlock` (1263 = neighbour in `topLevelMappedBlocks()` order), `navigateBlockEdit`
  (1429): save final, remember `pendingBlockNavigation` (persisted in `vscode.setState`),
  re-open after re-render via `resumePendingBlockNavigation` (3254), matching by
  `data-sphinx-preview-block` id or source line.
- Insert points: `refreshInsertPoints` (2942) puts a zero-height `div.sphinx-preview-insert-point`
  with a "+" button after every body block (`afterLine = endLine`), and one after properties
  (afterLine 0). `createInsertPoint` (2923); CSS previewStyles.ts:462-520 (button absolutely
  positioned at `left:-1.6em`, `opacity:0` until `[data-sphinx-source-line]:hover +
  .insert-point button`). Rebuilt (not patched) on every `applyEditMode`/`initializeContent`.
- `{include}`: renderer expands includes (mystRenderer.ts:692-780) and re-positions the included
  AST with `setIncludedSourceLine` (645) which rewrites ONLY `position.start.line` to the include
  directive line; `position.end.line` keeps the line number from the INCLUDED file.
  Consequence (UNVERIFIED but evident from code): included blocks carry the host document's
  source-file attr and `data-sphinx-source-line = include line`, `end-line` = a line number of a
  different file (or falls back to `line` when smaller). Clicking them would open the range
  [includeLine .. foreign endLine] of the HOST document - i.e. potentially wrong lines, not the
  included file. No code path edits the included file. This is a latent bug that move/multiselect
  would amplify (swap/cut/delete of wrong lines). Recommendation: tag expanded include output
  (e.g. wrap in container carrying only the directive's own range and `data-sphinx-readonly`) or
  clamp end-line to the directive's `position.end.line`, and make every new operation refuse
  blocks flagged as included. Needs a quick repro test first.
- readOnly / untrusted: `readOnly = workspaceFolder === undefined || !vscode.workspace.isTrusted`
  (extension.ts:2519, 2782). `initialEditMode: !preview.readOnly && ...` (extension.ts:917) so edit
  mode (and so every feature below) is not offered in a read-only preview. Host edit handlers rely
  on `isDocumentEligible` + `sourceAvailable` (extension.ts:397); NEW handlers must also check
  `preview.readOnly` explicitly (defence in depth; I did not see it checked in the edit handlers
  I read).
- Webview options: `localResourceRoots = [workspaceRoot]` (+ extension bundle for mermaid)
  (extension.ts:920-949); CSP `img-src ${cspSource} data:`, `connect-src 'none'`
  (src/security/csp.ts) - so a newly written workspace image displays after re-render with no CSP
  or roots change, but clipboard/network from the webview go through postMessage only.
- No `copy`, `cut`, `paste`, `clipboardData` or `user-select` handling exists in scrollSync.ts or
  previewStyles.ts (grepped). So: native browser copy/paste everywhere, nothing intercepts.

## 1. move-block-up-down (intent: add up/down buttons right of the "+" bar)

### Current state
No move concept exists. Building blocks present: insert point bar (above), `topLevelMappedBlocks`,
`sourceRangeForLines`, `insertion.ts` EOL detection, `storePendingPin`/`pinFields` pin mechanism
(extension.ts:2011, scrollSync.ts:538) that keeps a given source line at a given viewport top
after the next render (single use, 5 s expiry, applies to renders >= the saved version).

### Algorithm (new pure module `src/mapping/blockMove.ts`, `planBlockMove(text, a, b)`)
Inputs: `a` = block to move, `b` = its neighbour (up: b above a; down: b below a). Normalise so
`first`/`second` are the upper/lower ranges (line pairs from webview, re-validated on host with
`sourceRangeForLines`).
1. Offsets: `F = sourceRangeForLines(first)`, `S2 = sourceRangeForLines(second)`; require
   `F.end <= S2.start` and non-overlap.
2. Strip the trailing line break of each block text (`\r?\n|\r`): `Ft`, `St`. Record the
   break that terminated `second` (`tail`, may be "" for last line without newline) - it must stay
   where it is so the document keeps/loses its final newline exactly as before.
3. Separator `sep = text.slice(F.end, S2.start)` (the blank lines) plus the break that ended
   `first` (`firstBreak`). Semantics: `[first][firstBreak][sep][second][tail]` becomes
   `[second][firstBreak][sep][first][tail]`. i.e. keep separators in place, swap contents. Each
   block's internal EOLs are untouched (CRLF preserved); `firstBreak`/`sep` are the document's own.
4. If `sep` and `firstBreak` together contain NO blank line (blocks glued, e.g. heading directly
   above paragraph) keep as is: swap preserves the same adjacency. Exception: when `sep` contains
   non-blank text (a comment, link reference definition, footnote definition, `<!-- -->` etc. that
   is not a mapped block) -> REFUSE (return undefined; UI shows "Cannot move across unmapped
   content"). This is the safe default; see ambiguity 3.
5. Result is ONE `WorkspaceEdit.replace` over `[F.start, S2.end - tail.length]` with
   `Second + firstBreak + sep + First`; wrap through `minimalReplacement` only if desired (not
   needed). One applyEdit = one undo step. Do NOT use the EditLock/ActiveBlockEdit machinery: moving is
   atomic. Reject when `preview.activeBlockEdit` exists, or have the webview first
   `postBlockEditSave(true)` and then send the move on the next macrotask after the save ack
   (simpler: disable the move buttons while an editor is open - recommended).
6. Frontmatter boundary: the first body block must not move up (its upper neighbour is the
   properties block / frontmatter, excluded). The `body` filter in `refreshInsertPoints` already
   excludes properties, so up is disabled for `body[0]`; host must ALSO re-check by comparing
   `first.line` with the end of the frontmatter (`matchFrontmatterBlock`, as insertion.ts:24 does)
   because a stale/hostile message could target it.
7. Lists: v1 moves the WHOLE top-level list as one block (that is what `topLevelMappedBlocks`
   yields). Moving an item inside a list is a separate feature (needs per-item ranges incl. nested
   sublists and renumbering of ordered lists) - out of scope; ambiguity 2.
8. Adjacent-list hazard: swapping a list with a following list separated only by blank lines can
   merge or split lists (CommonMark: same marker => one loose list). Not detectable at mapped
   level; accept, documented. Blocks inside `{include}` expansion: refuse (see section 0).
9. Second hazard: A = indented code / paragraph continuation semantics when `sep` has no blank line
   (lazy continuation). If either block is a paragraph and `sep+firstBreak` has no blank line,
   insert one blank line (`EOL+EOL`) as separator to avoid fusing paragraphs; rule: if swap would
   make `first` end directly followed by a paragraph line without blank, use
   `firstBreak + firstBreak`. Cover with unit tests.

### UI placement
Extend `createInsertPoint(afterLine, label, standalone)` (2923) to take the block the point follows
(or compute from `insertPoints` index). Inside the same `div.sphinx-preview-insert-point` add two
`button`s ("up arrow", "down arrow", aria-label "Move block up/down", `type=button`) positioned to
the right of "+" (CSS at previewStyles.ts:474+: same absolute scheme, `left:-1.6em` for "+", the
arrows at `left: calc(-1.6em + 1.6em)`... or in the gutter above/below). Revealed by the same
`:hover + .insert-point button` rule (extend selector to `.sphinx-preview-insert-point button`).
No arrows on the point after properties (afterLine 0) nor on `--start` standalone. First body block:
up disabled; last: down disabled. Disabled and hidden while `activeBlockEdit` exists. Note the "+"
bar is drawn AFTER the block (below it), so the arrows act on the block ABOVE the bar; make the
aria-label/tooltip explicit ("Move the block above up/down"). Click handlers must
`stopPropagation` (the global click handler at ~3532 already ignores `.sphinx-preview-insert-point`).

### Messages
New webview->host `previewBlockMove`: `{documentId, documentVersion, requestId, editId (reuse for
validator), line, endLine, direction: "up"|"down", neighbourLine, neighbourEndLine, pinLine,
pinViewportTop}`. Add to allowlist (extension.ts:412), include in `editRequest` set (455), add a
`validDirection`; `pinLine/pinViewportTop` currently legal only for FrontmatterSave and final
EditSave (434-440) - extend. Host handler `handlePreviewBlockMove`: readOnly check, no
`activeBlockEdit`, `currentPreviewDocument`, recompute offsets, `planBlockMove`, one `applyEdit`,
on success `storePendingPin(preview, {pinLine: newStartLine, pinViewportTop}, document.version)`,
on failure/refusal post an error (reuse `previewEditSource` error shape or add `previewMoveResult`).
`newStartLine`: moving down: `first.line + (lines in second) + (lines in sep/firstBreak)`;
moving up: the moved block ends at `second` position -> new line = `first.line`. Simpler: compute from
the replacement text (count line breaks).

### Keyboard
VS Code convention is Alt+Up/Down (move line). Inside the textarea that chord is bound by nothing
in the editor today (`navigateBlockEdit` ignores Alt: boundaryNavigation returns undefined when
`altKey`), so Alt+Up/Down in the textarea can be wired to "save final then move the block"
(natural, mirrors VS Code), and on a focused non-editing mapped block (`tabindex=0`) to move
directly. Caveat: macOS Option+Arrow is word/paragraph navigation in a textarea; so on macOS the
chord would shadow it. Recommended default: Alt+Shift+Up/Down? VS Code uses Alt+Shift for COPY
line up/down, so avoid. Decision needed (ambiguity 4); default: Alt+Up/Down only when the focus is
on the block or bar (not in the textarea); in the textarea use Ctrl/Cmd+Alt+Up/Down.

### Caret/scroll following
Use the existing pin: the webview records `pinFields(movedLine, blockElement, ...)` (which line + its
viewport top) so after the re-render (in-place patch via contentPatch.ts, or full reload) the moved
block sits at the same viewport position as before... For "down" this means the block jumps away
from the cursor by the neighbour height, so pin the NEW line at the SAME viewport top: the moved
block stays under the mouse, and a second click on the same arrow continues moving it. Also re-focus:
set `pendingBlockNavigation = {blockId?, sourceLine: newStartLine}` with a new mode "focus" (no
editor open) or reuse `resumePendingBlockNavigation` (3254) which opens the editor - not desired;
add a variant that only focuses the block and shows a brief highlight. If the user moved with the
editor open (Alt+arrows in textarea), reopen the editor on the new line with the caret restored via
the existing `initialCaretPosition`.

### Files touched / size
src/mapping/blockMove.ts (new, pure), src/extension.ts (validator, handler), src/webview/scrollSync.ts
(createInsertPoint buttons, click/keydown, pin), src/preview/previewStyles.ts (buttons CSS),
test files below, CHANGELOG. Size: M (S for the pure algorithm, M for UI + pin + validators).

### Tests
- test/mapping/blockMove.test.ts (mimic test/mapping/insertion.test.ts): LF, CRLF, last block with
  and without trailing newline, glued blocks (no blank), several blank lines, frontmatter edge,
  non-blank separator refusal, overlapping/unordered ranges refused, round trip (move down then up
  == identity), unicode.
- test/webview/scrollSync.test.ts (the 296 KB harness): arrows rendered per body block, disabled at
  ends, hidden while editing, click posts `previewBlockMove` with the right ranges, pin fields.
- test/integration/previewEditing.test.ts: apply move via host, assert document text, single undo
  step restores (call `vscode.commands.executeCommand("undo")`), stale-version rejection, readOnly
  rejection.
- test/integration/realInput.test.ts (real-input pattern from commit 2af0afa) for up/down on a
  figure and on the last block; test/visual/scenarios.ts for the button geometry.
### Regression risks
Insert-point CSS (hover reveal, z-index, left gutter clipping at narrow widths); `isPreviewSyncMessage`
allowlist drift; included blocks; edit lock being not held during a move so an in-flight render may
race (the refresh after the doc change handles it, but pin `minVersion` must be the post-edit
version); table-of-contents / sticky headings anchors referencing lines; scroll-sync layout cache
(`measure()`).

## 2. edit-inline-image

### What 2af0afa fixed
`wrapBareBlockImages` (mystRenderer.ts:1169-1187, call at ~1353) wraps (a) top-level `image` nodes
(MyST lifts a paragraph holding only an image) and (b) the position-less image inside an `{image}`
directive into a `paragraph` with the node/directive position. Before this the `<img>` had no
`data-line`, so: no mapped block => (1) click on the image did nothing in edit mode, (2) no "+"
bar after it (insert points are created only for mapped blocks), (3) ArrowUp/Down navigation
(`adjacentMappedBlock` = `topLevelMappedBlocks()`) skipped it, because it simply is not in the
list. That is exactly the three symptoms in the intent (the "skips to the text above it" one is
the navigation case). The commit added insertion tests (test/mapping/insertion.test.ts),
renderer tests (test/rendering/mystFeatures.test.ts), realInput, visual fixtures
18-figure-at-end.md / 19-image-at-end.md. So the intent is probably FULLY or mostly covered at
HEAD for standalone `![]()` and `{image}`; it should be re-verified in the real UI, because the
backlog item may predate the commit.

### What still might fail (verify first; UNVERIFIED unless noted)
- Click on `<img>` today: the document click handler (scrollSync.ts ~3532) takes
  `event.target.closest(mappingsSelector)`; with the wrapper `<p data-line>` the click on the img
  resolves to the `<p>`, `openMappedEditor` opens a textarea for its range. OK for plain images.
  It does NOT open when the image is inside a link (`target.closest("a")` returns early, 3537):
  `[![alt](img)](url)`, which is common (badges). Decide: edit-mode click on an image inside a link
  should open the editor (link navigation remains Cmd+click, like frontmatter links at line ~74).
- `{figure}` (colon fence or backtick): the container `figure` is mapped by mystRenderer.ts:1048-1053
  (`mergeProperties(figure, sourcePositionProperties(node, line))`), so click + navigation work;
  covered by the commit's tests for insertion after figures.
- Image inside a paragraph with text: paragraph is mapped, works (the wrapper only handles pure
  image paragraphs).
- Images in lists/tables/admonitions: handled via the whole-list / table / directive editor.
- Image with attribute syntax `![a](b){width=50%}` or a title: depends on mdast; lifted by MyST as
  image only if the paragraph has no other inline; if MyST yields a `paragraph` containing image +
  text node for the `{...}` it is mapped already.
- Reference images `![a][ref]` -> `imageReference` is not in `wrapBareBlockImages` (type is
  `imageReference`, not `image`): a paragraph holding only `![a][ref]` is NOT lifted by MyST either
  (it stays a paragraph), probably fine.
- Edit mode "hover outline" (`editHoverTarget` 2845) works from mapped.
- CSS: images may have `pointer-events`/lightbox? None seen (only a `load` listener at 3283).
- ArrowUp from the block BELOW an image: `adjacentMappedBlock` now includes the wrapper p, so caret
  goes into the image's raw `![..](..)` textarea. Verify the `start/end` caret choice is sensible.
- Wrapper side effect: an extra `<p>` around a lifted image might alter the layout of images
  (margins; `display:block` selectors like `main > img`). Check previewStyles for `> img`
  selectors (UNVERIFIED).

### Fix approach (if anything is still broken after a manual check)
1. Add a realInput scenario (click the `<img>` in edit mode; ArrowUp from the paragraph below;
   "+" after it, including as last block) - if all three pass the item is "done by 2af0afa" and the
   remaining work is only the linked-image case.
2. Linked image: in the click handler change the early return for `closest("a")` so that, in edit
   mode, when the click target is an `<img>` (or the anchor contains only an img) and no
   Cmd/Ctrl, it opens the editor and `preventDefault`s. `editHoverTarget` (2845) has the same
   `mapped.closest("a")` exclusion; align it.
3. Pure `{image}` directive in an include: refuse (section 0).
### Files / size
src/webview/scrollSync.ts (2 small conditions), tests; maybe src/render/mystRenderer.ts. Size: XS
(verification + linked image) .. S.
### Tests
test/webview/scrollSync.test.ts (click on img opens editor; click on img inside `<a>` in edit mode;
arrow navigation up from a paragraph below an image opens the image's block editor),
test/integration/realInput.test.ts (mimic the 2af0afa addition), test/rendering/mystFeatures.test.ts
(image-in-link mapping), test/visual/scenarios.ts.
### Risks
Link navigation regression (badges); shift-click/ctrl-click conventions; hover outline on images.

## 3. multibloc-selection

### Current state
Edit mode is strictly single-block: one `activeBlockEdit` in the webview and one `ActiveBlockEdit`
on the host. There is no selection model, no clipboard handling. Preview mode: no `copy`/`cut`
listeners, so the browser/VS Code webview copies the DOM selection as `text/html` + `text/plain`
natively across blocks; `postReveal` on click only. A drag-selection that ends on a different
element fires `click` on the common ancestor (not mapped => ignored), but a selection inside one
block ends with a `click` on that block => `postReveal` (reveals the source in the editor; does not
clear the selection by itself - UNVERIFIED whether the reveal steals focus and drops the selection;
guard with `window.getSelection()?.isCollapsed` if so). In edit mode a mouse-down in a block starts
a native text selection while the click opens the textarea - a drag to select across blocks opens an
editor on mouse-up when both ends are in the same block.

### Design (recommended)
Selection model = a CONTIGUOUS range of top-level BODY blocks (never properties, never included
blocks). Non-contiguous selections make "exact raw copy" ill-defined (what about the gaps?).
- Gestures: (1) Shift+click on a block (outside an open editor; if an editor is open, save it first
  via the `rememberPending...` path, then select) selects from the anchor block (last opened/clicked
  block) to the clicked one; (2) with a block selected (not editing), Shift+ArrowUp/Down extends;
  (3) Escape or a plain click clears; (4) optional later: drag on the left gutter. A gutter checkbox
  is rejected: clutters; the "+" bar already uses the gutter.
- Visual: `data-sphinx-preview-block-selected="true"` on each block + outline (new CSS next to
  the hover rule at previewStyles.ts:456). Blocks keep `tabindex=0`; use a hidden live region for
  "N blocks selected" (a11y).
- State: `blockSelection = {startIndex, endIndex}` over `topLevelMappedBlocks()` order, rebuilt on
  `contentReplaced`/`initializeContent` by block id/line (selection should survive an in-place patch
  or be cleared; clearing is simplest and safe).
- Lines: range = `first.line` .. `last.endLine`; this includes the blank separators between selected
  blocks, so the raw copy is byte-exact for the span.

### Operations
- Copy (Cmd/Ctrl+C, only when blockSelection non-empty and focus is not in a textarea/input):
  `keydown`/`copy` listener on document, `preventDefault`, post `previewBlocksCopy {line, endLine}`;
  host re-derives with `currentPreviewDocument` + `sourceRangeForLines`, takes `document.getText(range)`
  and writes `vscode.env.clipboard.writeText(text)`. Host-side write is required: the webview CSP and
  focus rules make `navigator.clipboard.writeText` unreliable (needs permission/gesture, works in
  VS Code webviews only for user-initiated copy). Alternative: set `event.clipboardData` in the `copy`
  event synchronously - but the raw text lives on the host, so the webview must either already hold
  it (cache the span text from a prefetch on selection change: host answers `previewBlocksSource`)
  or round-trip. Round trip with `vscode.env.clipboard` is simplest.
  Keep trailing line break? Strip the final EOL of the range, keep inner text exactly (CRLF kept).
- Cut (Cmd/Ctrl+X): copy as above then delete. Deletion range: from start of `first` through the
  start of the next block (consumes the blank separator that FOLLOWED the span) so no double blank
  remains; if the span is the last block, delete from the end of the previous block's last line
  (consume the separator that PRECEDED) - symmetric to `planInsertion` conventions. If it is the
  only body block, leave the body empty (so the "Start writing" entry appears). One WorkspaceEdit.
- Paste (Cmd/Ctrl+V): target = the selection's last block (insert after) or the keyboard-focused
  insert point; webview posts `previewBlocksPaste {insertAfterLine}`; host reads
  `vscode.env.clipboard.readText()`, rejects empty, builds `planInsertion(text, afterLine)` +
  `insertionText(plan, raw)` (src/mapping/insertion.ts: already normalises EOL to the document's and
  adds separators) and applies in one WorkspaceEdit. This gives "move several blocks": Cut then paste
  elsewhere (two undo steps; ambiguity 6). Paste INSIDE an open block editor stays native text paste
  (works for multi-block text since it is just text; the saved block then contains several blocks -
  acceptable, parsed on re-render).
- Delete/Backspace on a selection: optional, same deletion path as cut without clipboard (ambiguity
  recommended to include only behind explicit key; default: Delete removes selected blocks).
- Preview mode (non-edit): the request "selection copy the HTML code across blocks" is satisfied by
  the native browser behaviour (HTML + text flavours already include several blocks). If the intent
  is "copy the raw Markdown source" in preview mode, that needs the same host round trip using the
  mapped blocks intersecting `window.getSelection()` (use `Range.intersectsNode` on top-level
  blocks) - ambiguity 5; default: leave native behaviour, only fix the click-reveal-vs-selection
  clash if it exists.

### Interaction with single-block editor and the lock
- Selection and an open textarea are mutually exclusive: starting a selection finalizes the editor
  first (`postBlockEditSave(true)` then act on the save result, like the table switch path in
  `openMappedEditor`), because the host allows only one `activeBlockEdit` and the lock defers renders
  (the selected DOM would otherwise be replaced under the user).
- Cut/paste/delete are atomic host edits (like move): reject while `preview.activeBlockEdit`
  exists; they do NOT acquire the EditLock; the refresh after the document change re-renders and
  clears the selection (pin: keep the viewport via `pinFields` of the first selected block).
- readOnly preview: no edit mode so no selection; host handler must also check `preview.readOnly`.
### Files / size
src/webview/scrollSync.ts (selection state, listeners, CSS attr), src/preview/previewStyles.ts
(selected style), src/extension.ts (3 message types + validators + handlers), possibly new pure
module `src/mapping/blockRange.ts` (cut-range planning), CHANGELOG. Size: L (selection UX, 3
host operations, a11y, keyboard focus rules).
### Tests
test/mapping/blockRange.test.ts (new; mimic insertion.test.ts: cut range middle/last/only block,
CRLF, no final newline); test/webview/scrollSync.test.ts (shift+click range, Shift+Arrow extend,
Escape clears, copy posts message with right lines, copy ignored in textarea/input, selection
cleared on content replace, finalizing an open editor before selecting); test/integration/
previewEditing.test.ts (clipboard stub: `vscode.env.clipboard` round trip, cut then paste, single undo
per operation, stale version); realInput.test.ts for real key chords; visual scenarios for outline.
### Risks
Native selection vs click-to-edit conflicts (drag selection opening an editor); Cmd+C inside
textarea/frontmatter inputs must remain native; accessibility focus handling; clipboard permission
differences between desktop/web VS Code; large selections (host reads whole text; fine); included
blocks (refuse); the selection spanning a `{include}`-expanded group would produce wrong lines.

## 4. paste-image-in-edit-mode

### Current state
No paste handling at all (no `paste` listener, no `clipboardData`, no `workspace.fs` writes in the
extension apart from a read at extension.ts:2187). The block textarea gets native paste (text only;
images are ignored by a textarea). Table-cell editor uses an `<input>` (`edit.tableInput`) - out of
scope. Image display: `localResourceRoots=[workspaceRoot]` and CSP `img-src ${cspSource}` already
permit images in the workspace; an image next to the md file is within the root as long as the file
is inside the workspace folder.

### Design
Webview (in `receiveBlockEditSource`, scrollSync.ts:~2745, next to the `input`/`keydown` listeners):
`textarea.addEventListener("paste", (event) => {...})`:
1. `const items = Array.from(event.clipboardData?.items ?? [])`; take the first with
   `kind === "file"` and `type` in `image/png|jpeg|gif|webp` (exclude `image/svg+xml`, `image/bmp`
   v1: svg can carry script; our sanitizer handles `<img>` so it would be safe, but keep an
   allowlist). If the clipboard ALSO has non-empty `text/plain` (copying from a spreadsheet/Word
   gives both), let the native text paste run (default: text wins; ambiguity 8).
2. `event.preventDefault()`; capture `selectionStart/End` and `edit` identity; `file.size` cap
   (recommend 10 MB raw; reject over with status "Image too large (max 10 MB)"); read via
   `FileReader.readAsDataURL` or `arrayBuffer` + chunked `btoa` (avoid
   `String.fromCharCode(...bigArray)` stack overflow); set `edit.status.textContent = "Saving image..."`.
3. `vscode.postMessage({type:"previewImagePaste", documentId, documentVersion, requestId, editId,
   mime, dataBase64, line, endLine})`. Message size: postMessage handles several MB but structured
   cloning a 13 MB string is heavy and JSON-serialised on the host side - cap it; add the same cap in
   the host validator (`typeof dataBase64 === "string" && length <= 14_000_000 &&
   /^[A-Za-z0-9+/]*={0,2}$/`), and verify the magic bytes (PNG `89 50 4E 47`, JPEG `FF D8 FF`, GIF
   `47 49 46`, WEBP `RIFF....WEBP`) against the declared mime. Mime -> extension from the verified
   magic, never from the client.
4. Host `handlePreviewImagePaste`: reject if `preview.readOnly`, `!vscode.workspace.isTrusted`,
   document not `file:` scheme (untitled / `vscode-vfs` etc -> error "Save the document before
   pasting an image"), stale version, no `activeBlockEdit` for that editId (an editor must be open:
   paste only makes sense inside it). Directory = `path.dirname(document.uri.fsPath)`; require
   `isPathWithin(canonicalPath(workspaceRoot), canonicalPath(dir))` (symlink escape). A standalone
   file outside any workspace folder is already `readOnly` (extension.ts:2519 => edit mode
   unavailable) - nothing extra to do, but keep the check. Name: `image.png`; if exists
   (`await vscode.workspace.fs.stat(uri)` resolves) try `image-1.png`, `image-2.png`... up to e.g.
   1000, then error. TOCTOU between stat and write is negligible but use a `writeFile` only after a
   fresh stat; there is no exclusive-create flag in `workspace.fs`; accept.
   `await vscode.workspace.fs.writeFile(uri, bytes)`. Reply `previewImagePasted {editId, fileName,
   relativeUrl}` (URL-encode with `encodeURI` only if the name could contain spaces; generated
   names never do) or `{editId, error}`.
5. Webview on reply (still the same `activeBlockEdit`/editId, else drop and tell nothing):
   restore the saved selection, `applyTextEdit(textarea, {start, end, text: "![image.png](image.png)",
   selectionStart: start + 2, selectionEnd: start + 2 + alt.length}, ...)` - uses the native
   `execCommand("insertText")` path so the textarea undo stack keeps one step (the helper at
   scrollSync.ts:1448); then `resizeTextarea(); autosaveBlockEdit()`. The alt is the file's stem
   or literally the first `image.png` as in the intent: the intent says the text highlighted is the
   first `image.png`, i.e. the alt text; the alt equals the filename (`image.png`), so selecting
   `[2, 2+len)` gives exactly that. After the alt is selected the user can type to replace.
   The existing autosave posts the text; the rendered image only appears after the final save
   (lock defers render while the editor is open; editor is open so no re-render until Done) - fine.
6. If the editor was closed/blurred before the reply (blur => `saveBlockEdit` final), the image file
   exists but the reference is not inserted. Mitigation: keep the textarea focus during pasting; if
   `activeBlockEdit` changed, drop (orphan file, rare). Document it. Do not auto-delete.
7. When pasting at an insertion editor (insertAfterLine), same flow; the dir is still the md's dir.
8. Pasting in edit mode but NOT in a textarea (no editor open): not handled v1 (could open an
   insertion editor after the focused block) - ambiguity 9.

### Files / size
src/webview/scrollSync.ts (paste listener, reply handler in the message switch),
src/extension.ts (allowlist type `previewImagePaste`, validators incl. size/base64, handler,
`vscode.workspace.fs` write, reply), maybe new pure helper `src/mapping/imageName.ts`
(`nextImageName(existing: Set<string>, ext)`) and `src/mapping/imageBytes.ts` (magic sniffing) so
they are unit-testable without VS Code. Size: M.
### Tests
test/mapping/imageName.test.ts + imageBytes.test.ts (new, pure; mimic textDiff.test.ts);
test/webview/scrollSync.test.ts (fake `ClipboardEvent` with image item posts message, with text+image
prefers text, oversize rejected, reply inserts reference and selects alt, editor changed => ignored,
undo step); test/integration/previewEditing.test.ts (host handler: writes file next to md, conflict
=> image-1.png, untitled rejected, readOnly/untrusted rejected, path escape rejected, bad magic
bytes rejected, stale version) - clean created files; test/security/ for the validator limits (look at
existing test/security/* for the pattern); realInput for real paste if feasible (clipboard images
are hard in headless: use the synthetic DataTransfer in the webview test only).
### Risks
Message size/perf; security (MIME spoof, SVG, path traversal -> we generate the name only);
workspace.fs on remote/virtual workspaces (use the document's own `Uri` scheme/authority, not
`Uri.file(fsPath)`: build with `vscode.Uri.joinPath(vscode.Uri.joinPath(document.uri, ".."), name)`);
file watcher triggering a dependency re-render while the editor is open (the lock defers it - good,
but confirm that a changed dependency does not release the lock: `needsRefresh` isDependencyChange
=> re-render is deferred by `shouldDeferReload`); the image appears via the existing
img-src; git status noise.

## 5. Numbered ambiguities (decision needed, with recommended default)

1. Move semantics for blocks coming from `{include}` expansions (and the include end-line anomaly
   in section 0): default = refuse move/cut/paste-adjacent/multiselect on included blocks and fix the
   end-line clamp as a prerequisite bug fix.
2. Lists: move whole list only, or list items? Default = whole top-level block only (v1); item moves
   a follow-up.
3. Non-blank unmapped content between two blocks (comments, link reference definitions, footnote
   definitions, HTML comments): refuse vs move the block across it. Default = refuse with a status
   message.
4. Keyboard shortcut: Alt+Up/Down (VS Code convention, but Option+Arrow is word navigation on macOS
   in a textarea) vs Ctrl/Cmd+Alt+Up/Down. Default = Alt+Up/Down on focused block / bar, and
   Ctrl/Cmd+Alt+Up/Down inside the textarea.
5. Preview-mode copy: keep native HTML/rich-text copy (default), or intercept to put raw Markdown on
   the clipboard? Default = native (the intent says "copy the HTML code").
6. Cut + paste = two undo steps vs a dedicated "move blocks" drag. Default = two steps; drag-drop
   out of scope.
7. Selection gesture: Shift+click + Shift+Arrows (default) vs gutter drag vs checkboxes; contiguous
   only (default) vs arbitrary (Ctrl+click).
8. Paste: when the clipboard has both text and an image (spreadsheet, Word). Default = text wins
   unless text is empty.
9. Paste an image while edit mode is on but no editor open: ignore (default) vs open an insertion
   editor after the focused/last block.
10. Image destination: next to the markdown file (default per the intent) vs honouring
    `markdown.copyFiles.destination` / an `assets/` setting; and naming `image.png`, `image-1.png`
    (default) vs timestamped. Max size default 10 MB; formats png/jpeg/gif/webp; SVG excluded.
11. Edit-mode click on an image inside a link: edit (default, Cmd/Ctrl+click still navigates) vs
    keep navigating.
12. edit-inline-image may already be fully fixed by 2af0afa for plain images; default = add the
    realInput scenario first and only then change code (close the item as "done" if green).
13. Where Alt+Up/Down moves when a multi-selection exists: move the whole selection (default,
    shares `planBlockMove` generalised to a span) or ignore. Recommend implementing move for N blocks
    by treating the selected span as `a`.
