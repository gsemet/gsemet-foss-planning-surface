# Empty blocks leave no blank lines, and a Delete block button

Done on an empty block writes no stray blank lines, an insertion after a list writes one
separator, and every body block gets a "Delete block" button with Delete and Backspace on a block
selection.

Origin: verbal (owner, 2026-11-20, testing 1.10.0). No issue.

## Goal

The owner reported that a block he added in the editor and left empty disappears from the page
but stays in the file: he can neither reach it again nor delete it. The page does not show blank
lines, so a run of extra blank lines in the file cannot be reached.

The investigation (`work/investigation.md`) found these sources of such runs:

- **An existing block emptied**: its text erased, then Done. The host writes `"\n"`, which leaves
  three blank lines between the neighbours.
- **Leading Enters in a new block**: `insertionText` keeps the blank lines typed at the start of
  the text.
- **An insertion after a list**: the list's range ends on its blank separator, so a new block
  inserted after it gets two blank lines before it.
- **Hand edits** (and merges) in the text editor.

The owner's exact path, "+" then Done with nothing typed, was **not reproduced**: that path
already writes nothing (SwRS-MDOKFSTUDIO-BLOCK-094).

This CR removes the first three sources and gives the writer a way to delete any block:

- **A**: Done on an empty block leaves no extra blank lines. A new block left empty writes
  nothing, and its leading blank lines are dropped. A top-level block or list item whose text was
  erased is deleted. An insertion anchored on a blank line writes one separator.
- **C**: every body block has a **Delete block** button. Delete and Backspace on a block
  selection do the same thing.

Runs already in the file (hand edits) become reachable in the follow-up CR
`1-inbox/empty-block-blank-lines-block` (B, the blank-lines block in edit mode). It builds on
this CR's button and keys and follows it in the stack (empty-block-Q12).

Project rules: this change follows the project's constitution (`.agents/constitution.md` in
markdown-okf-schema-studio), its `AGENTS.md` (requirements, completion gate `just preflight`) and
the requirements guidelines named there. This specification restates none of them.

## Words

- **Separator**: the one blank line between two blocks that Markdown needs.
- **Blank line**: a line holding only whitespace. This is the `isBlank` test of
  `src/core/mapping/blockRange.ts` and `src/core/mapping/blockMove.ts`, and the follow-up CR
  shares it. The empty pseudo-line after a final line break (BLOCK-234) is not a blank line.
- **Block selection**: the explicit top-level selection of `blockSelectionView.ts`
  (`blockSelection.isActive()`, `data-sphinx-preview-block-selected`). Plain Up/Down, Shift+Up/Down
  and Shift+click make it. A focused block or control is not a block selection.
- **Delete block button**: the new button of section 2. Add both terms to
  `.agents/glossary/common.md` ("Delete block button"; "Block selection" already exists: add that
  Delete and Backspace act on it).

## What changes

### 1. A: Done on an empty block

**1a. A new block's leading blank lines (empty-block-Q2).** `insertionText`
(`src/core/mapping/insertion.ts`) already writes nothing for an empty or whitespace-only text
(BLOCK-094). It also drops the whole blank lines at the start of the raw text, the way it already
drops the trailing ones. Indentation on the first non-blank line is kept: only whole blank lines
are dropped.

**1b. An insertion anchored on a blank line (empty-block-Q8).** `planInsertion` puts two line
endings (`prefix`) at the end of the anchor line. When the anchor line `afterLine` is a blank
line (a list or list item whose range ends on its blank separator, BLOCK-256), that line is
already the separator. The prefix is then one line ending, so exactly one blank line comes before
the new block. The suffix rule is unchanged. Example: `"- a\n\nPara\n"`, a block inserted after
line 2, gives `"- a\n\nNew\n\nPara\n"`. In LF, CR LF and lone CR, the inserted text uses the
document's line ending, as today.

**1c. An emptied block deleted on Done (empty-block-Q2, Q9).** An existing block's text is erased
and Done (or Ctrl/Cmd+Enter, or a blur that commits, BLOCK-047) posts the final
`previewEditSave` with a whitespace-only `editedText`. The host then deletes the block instead of
writing `"\n"`, when:

- **The editor is a top-level body block or a list item.** The page decides this, because the host
  sees only lines. The final `previewEditSave` carries a new optional field `deleteWhenEmpty: true`
  when the editor's block is one of `rt.blocks.topLevelMappedBlocks()` (the properties section
  excluded) or a mapped `li`. Add the field to the message type and validator in
  `src/core/protocol/pageToHostMessages.ts` and `pageToHost.ts`. A block inside a list item, an
  alert, a quote, an admonition or another container gets no field and keeps today's behaviour.
  Autosaves (`final: false`) never carry the field.
- **What goes.** The trailing blank lines of the held range (`ActiveBlockEdit.line`..`endLine`)
  are dropped first, with `withoutTrailingBlankLines` of `src/core/edits/sourceEdits.ts`, as a
  move does. Then the lines go by the separator rules of `planCut` (BLOCK-169), applied to the
  document with the original block text put back. In the middle, the neighbours stay one blank
  line apart. A first block leaves no blank line at the start of the body. A last block keeps the
  document's final line break, or its absence. In a tight list, the item's lines go and the items
  around it stay together. In a loose list, one blank line stays between the items around it.
  Only an editor text that is whitespace-only deletes: an item left as `- ` writes `- `, as today.
- **One edit.** It is one `TextEdit` through `applyWrittenEdits`. It replaces the region from the
  block's start (autosaved text included) through what `planCut` removes. It is a pure core
  function, for example `planEmptiedBlockRemoval(text, sourceStartOffset, lastSavedText,
  originalText, line, endLine)` in `src/core/edits/sourceEdits.ts`. It is used in
  `handleEditSave` / `drainActiveBlockEdit` of `src/session/features/blockEdits.ts`, for a held
  edit that is not an insertion, with `finalRequested`, `deleteWhenEmpty` and a whitespace-only
  pending text.
- **Undo (fix 11).** If Done comes within the autosave delay (400 ms, BLOCK-042) and no autosave
  has reached the document, the deletion is the only edit: one VS Code undo brings the block back.
  If an autosave already wrote the `"\n"` placeholder, there are two edits, the autosave and the
  deletion: two undos bring the block back. Each further autosave of earlier typing stays its own
  step, as today.
- **Unchanged.** Autosaves of an empty text keep writing the `"\n"` placeholder. Escape and Cancel
  keep BLOCK-053: they write the original text back. An included block opens no editor. The
  properties table keeps its own editors.
- **After the deletion.** The render follows as after any final save. The block selection goes to
  the block that took the deleted block's place (section 2, "After a delete").

### 2. C: the Delete block button and keys (empty-block-Q4, Q7, Q10, Q11)

**The button.** `addMoveButtons` (`src/page/features/blockMoves.ts`) builds the bar of every body
block (the insert point after it, BLOCK-087/109). It gets one more button:

- class `sphinx-preview-delete`, `type="button"`, `aria-label` and `title` "Delete block",
  text `×`.
- **Placement (fix 7).** It comes right after the down arrow and touches it, so the pointer never
  loses the bar. The spec fixes no offset in em. The move status (`.sphinx-preview-move-status`,
  today `left: 2.8em` in `src/core/preview/styles/editModeStyles.ts`) moves right of the delete
  button so the two never overlap. A geometry check (section "Evidence") holds both.
- It is shown and hidden like the move buttons: on hover of the block, on focus, by the keyboard
  owner rule of BLOCK-109 (`data-sphinx-actions-shown`). It is hidden while a block editor is open
  (`data-sphinx-preview-block-editing`).
- No button for an included block (BLOCK-127), for the properties section's bar (which has no move
  buttons) or for the "Start writing" entry.
- **Reusable.** Build the button with one exported helper, for example
  `createDeleteBlockButton(document, onDelete)` in a page module (`src/page/modules/`), with its
  CSS in one named block of `editModeStyles.ts`. The follow-up CR puts the same button on the
  blank-lines block without copying it. The key handler below dispatches through one function,
  for example `deleteSelection()`, that the follow-up CR can extend for a selected blank-lines
  block.

**What the button and keys do.**

- A click on a block's button deletes that block. If a block selection ends at that block
  (`selectionEndsAt`), it deletes the whole selection, the way the move buttons act on a
  selection.
- **Delete and Backspace act only on a block selection (Q10).** With a block selection and the
  key target on the page itself (`plainKeyTarget`), Delete or Backspace deletes the selected
  blocks. Without a block selection they do nothing: never on a merely focused block, on a focused
  control (a button of a bar, the toolbar), in a text box or input, in the properties table or in
  an open editor.
- **One level down (Q11).** When the structural navigation (BLOCK-254,
  `structuralNavigationView.ts`) holds a cell, a list item or an inner block below the top level,
  Delete and Backspace do nothing. Add an accessor to `StructuralNavigationView`, for example
  `isBelowTopLevel()`, true when the cursor path is longer than one or names a cell.
- The keys are added in the region of the clipboard key listener in `blockSelectionView.ts`, under
  the same guards: edit mode on, no active block or frontmatter edit, one blocks request in flight
  at a time (`blocksFlight`).

**The host.** The page posts a new message `previewBlocksDelete { line, endLine, pinViewportTop?
}`, like `previewBlocksCut` but with no clipboard write. Register it in the message registry
(`src/core/protocol/pageToHost.ts`, `pageToHostMessages.ts`) with gate `render`
(`src/session/pageMessages.ts`). The handler sits beside `handleBlocksCopyCut` in
`src/session/features/sourceEdits.ts`, and the plan is a core `planBlocksDelete` beside
`planBlocksCopyCut` in `src/core/edits/sourceEdits.ts`. The host:

- **drops the span's trailing blank lines first (Q7)**, with `withoutTrailingBlankLines`, as a
  move does. A selection that ends on a list whose range ends on its blank separator is then
  deleted instead of being refused by `checkSpan`. Cut and copy stay as they are: their case is
  filed as `1-inbox/cut-copy-list-trailing-blank`.
- checks the span with `checkSpan` (the out-of-date and frontmatter refusals). It refuses a span
  that opens an `{include}` with "A block that comes from an included file cannot be deleted.":
  this message joins the BLOCK-127 family.
- applies `planCut`'s edit: one `TextEdit`, one VS Code undo step, with the separator rules and
  line endings of BLOCK-169 and BLOCK-234 and the viewport pin of a cut (`pinViewportTop`, the
  following line).
- answers `previewBlocksResult` with a new `op: "delete"`. Extend the `op` union of
  `PreviewBlocksResultMessage` in `src/core/protocol/hostToPage.ts` and of the gate in
  `pageMessages.ts`. A refusal shows next to the bar or selection, as a cut refusal does.

**After a delete.** The block selection goes to the block that took the deleted block's place
(`followingLine`), or to the block above when the last block went. When the body becomes empty, it
goes to the "Start writing" button (BLOCK-102). Pressing Delete again keeps deleting from the
keyboard, and the screen does not jump (the cut pin).

### 3. Line endings (empty-block-Q5)

Every edit of this change keeps the document's line endings and its final line break, or its
absence: the leading-blank-line drop, the insertion on a blank anchor, the emptied-block deletion
and Delete block (BLOCK-234, BLOCK-094, BLOCK-169). The unit tests run each new plan on LF, CR LF
and lone-CR texts.

### 4. Requirements

Follow the project's requirements guidelines: IDs come from `okfreq new` and are never
hand-allocated; markers move with the code; run `just requirements-update`; add a dated entry in
`requirements/tiers/log.md`. All of these are in scope `block-editing`:

- Update **SwRS-MDOKFSTUDIO-BLOCK-094** with two new rows: the leading blank lines of a new block
  are dropped, and an insertion anchored on a blank line writes one separator.
- New SwRS: **a top-level block or list item emptied and committed is deleted with its separator**
  (none covers this today, per the investigation). It covers the trailing blank lines dropped,
  tight and loose lists, inner blocks unchanged, and undo with and without an autosave. It derives
  from StRS BLOCK-025 and BLOCK-011.
- New SwRS: **Delete block deletes the blocks of a selection with one separator in one undo
  step**. It covers the button's placement and visibility, Delete and Backspace on a block
  selection only, nothing one level down, the trailing blank lines dropped, the included-block
  refusal and the selection afterwards.
- Update **SwRS-MDOKFSTUDIO-BLOCK-127** (the delete refusal), **BLOCK-004** (Delete and Backspace
  on a block selection) and **BLOCK-109** (the bar's delete button follows the same owner rule),
  each with a scenario row.
- **StRS-MDOKFSTUDIO-BLOCK-011** (`proposed`) and **BLOCK-025** (`approved`): the new SwRS name
  them in `derives_from`. That leaves their authored text alone. If BLOCK-025's text must change,
  its re-approval goes to the owner through the Chief of Staff.

### 5. Shared vocabulary and docs

- `.agents/glossary/common.md`: see "Words".
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes.
- The release notes are written when the release is prepared, not in this PR.

## Out of scope

- **B, the blank-lines block in edit mode** (the former section 2 of this spec): showing runs of
  blank lines, reaching them with the arrows, typing in them and removing them. Split to
  `1-inbox/empty-block-blank-lines-block` (empty-block-Q12). The critic's points 8 and 9 (one
  shared `isBlank`; nothing shown inside folded sections) belong to that item. It reuses this CR's
  button helper and key dispatch.
- Cut and copy of a span that ends on a list's blank separator:
  `1-inbox/cut-copy-list-trailing-blank` (empty-block-Q7).
- Collapsing blank runs by itself (on save, on render, on any edit other than the writer's own
  delete). The file's format is kept (empty-block-Q2).
- Trimming the trailing blank lines of a non-empty block's edit.
- Emptied blocks inside a list item or a container (empty-block-Q9), blocks of an included file,
  and the frontmatter.

## Evidence

The checks read the shipped files at the head under test (the real stylesheet module, the real
page bundle, the real core functions), never a prepared copy. Each check fails on the code before
the change (constitution, section 3).

**Unit (core), `test/core/mapping/insertion.test.ts`:**

- Leading blank lines of a new block are dropped (LF, CR LF, CR), and an indented first line keeps
  its indentation.
- An insertion after a list that ends on its blank separator gives exactly one blank line before
  and one after the new block. A non-blank anchor keeps today's two line endings.

**Unit (core edits), `test/core/edits/`:**

- `planBlocksDelete` gives the same separator outcomes as the cut table of BLOCK-169. A span that
  ends on a list's blank separator is deleted with its trailing blank lines dropped. The
  included-block and frontmatter refusals carry their messages.
- `planEmptiedBlockRemoval` on `"# Title\n\nFirst.\n\nSecond paragraph.\n"`, with "First." emptied
  and an autosave already written, gives `"# Title\n\nSecond paragraph.\n"`. Also: the first and
  the last block, a list item in a tight and in a loose list, a range ending on a blank line, and
  CR LF.

**Session, `test/session/`:**

- A held edit's final save with whitespace-only text and `deleteWhenEmpty`:
  - before any autosave, one `applyWrittenEdits` call deletes the block (one undo step);
  - after an autosave, the autosave edit and the deletion are two calls.
- The same final save without `deleteWhenEmpty` (an inner block) writes the `"\n"` placeholder,
  as today.
- `previewBlocksDelete`: one `applyWrittenEdits` call, `previewBlocksResult` with `op: "delete"`,
  and the refusal paths.

**Page, `test/page/`** (with the runtime bundle, as `runtimeBlockSelection.test.ts`,
`runtimeBlockMoves.test.ts` and `runtimeBlockEditor.test.ts` do):

- The final save carries `deleteWhenEmpty` for a top-level paragraph and for a list item, not for
  a paragraph inside an admonition or a list item, and never on an autosave.
- Every body block's bar has the "Delete block" button after the down arrow. An included block and
  the properties bar have none. A click posts `previewBlocksDelete` for the block, or for the
  selection that ends there.
- Delete and Backspace with a block selection post `previewBlocksDelete`. They post nothing:
  - with only a focused block;
  - with a focused bar button;
  - in a text box or an open editor;
  - with the structural cursor on a cell, a list item or an inner block.
- After a delete result and render, the selection is on the following block.
- Geometry (`test/page/geometryChecks.test.ts` or the visual checks): the delete button touches
  the down arrow, and a move status never overlaps it.

**Visual (`just ci-visual`):** one capture of a hovered block's bar showing "+ ↑ ↓ ×", and one
with a move status shown beside it. Both come from the shipped stylesheet and are attached to the
PR as the pull-request guideline asks.

**Integration (real VS Code, `just ci-integration`, heavy run on the branch).** The scenario runs
on a real file, once in LF and once in CR LF:

1. **(fix 10)** Open a file with two paragraphs and turn edit mode on. Click "+" after the first,
   press Enter twice, type a word and press Done. The file has exactly one blank line before and
   one after the new block.
2. Open the first paragraph, erase its text and press Done at once: the paragraph and one
   separator are gone, and one Ctrl+Z in the text editor brings it back. Repeat, waiting past the
   autosave before Done: two Ctrl+Z bring it back.
3. Insert a block after a list: one blank line before it.
4. Select the second paragraph with the arrows and press Delete: it is gone, and one Ctrl+Z
   restores it. Hover a block and click "Delete block": the same.
5. Focus a block without selecting it and press Delete: nothing changes.

**Requirements:** `just requirements-lint` and `just requirements-update` pass. The new and
updated SwRS carry `@implements_req` / `@tests_req` markers at the code and tests above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

The answers leave these points to the specification. Each is decided here, as the option most
consistent with the product and the answers, for the Chief of Staff to check:

1. **The page marks which editors delete on Done** (`deleteWhenEmpty` on the final save). The host
   sees only lines and cannot tell a top-level paragraph from one inside a list item (Q9).
2. **Only a whitespace-only editor text deletes.** An item left as `- ` is written as it is.
3. **An emptied block is deleted with `planCut`'s separator rules**, after its trailing blank
   lines are dropped. This is the same rule as Delete block, so emptying and deleting give the
   same file.
4. **The trailing blank lines of a non-empty block's edit are not trimmed.** That would change
   BLOCK-234's text round-trip, which the answers did not ask for.
5. **The delete button's glyph is `×`.** "Delete block" is its `aria-label` and `title` (Q4). It
   sits in the block's bar beside the move buttons, which is where the block's actions are. The
   list-item and table-row handles on the left belong to items and rows.
6. **The button is one exported helper**, and the keys dispatch through one function. The
   follow-up CR reuses both without copying them (Q12).
7. **The selection after a delete goes to the block that took its place** (or the block above, or
   "Start writing"), so the keyboard can keep deleting.
8. **The new SwRS derive from StRS BLOCK-011 and BLOCK-025.** No new StRS.

The critic's fixes are carried in: 7 (no fixed offset; the move status sits right of the
button), 10 (integration step 1), 11 (undo with and without an autosave) and 12 (the Goal names
the sources and marks the owner's path as not reproduced). Points 8 and 9 are pointed to the
follow-up CR.
