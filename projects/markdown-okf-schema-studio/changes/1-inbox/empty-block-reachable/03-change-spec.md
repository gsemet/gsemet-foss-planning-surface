# Reach and delete extra blank lines, and a Delete block button

In edit mode, a run of extra blank lines shows as a small block you can select and edit, and
every body block gets a "Delete block" button.

Origin: verbal (owner, 2026-11-20, testing 1.10.0). No issue.

## Goal

The owner adds a block in the editor, leaves it empty, and it disappears from the page. It
stays in the file as blank lines that the page cannot reach: he can neither type in it again nor
delete it. After this change, an empty block never leaves something the writer cannot reach or
remove:

- Done on a new block left empty writes nothing. Done on an existing block whose text was erased
  deletes the block.
- Blank lines already in the file beyond the one that separates two blocks show in edit mode as
  a small **blank-lines block**. The writer can reach it from the keyboard, click it, type in it
  or delete it.
- Every body block has a **Delete block** button. Delete (and Backspace) on a selected block do
  the same thing.

Reading mode does not change.

Project rules: this change follows the project's constitution
(`.agents/constitution.md` in markdown-okf-schema-studio), its `AGENTS.md` (requirements,
completion gate `just preflight`) and the requirements guidelines named there. This
specification restates none of them.

## Words

- **Separator**: the one blank line between two blocks that Markdown needs.
- **Blank line**: a line holding only whitespace (`text.trim() === ""`, the `isBlank` test of
  `src/core/mapping/blockRange.ts`). The empty pseudo-line after a final line break (BLOCK-234)
  is not a blank line.
- **Blank run**: a maximal sequence of two or more blank lines in the body (after the
  frontmatter), outside the content of every top-level block (see "Where a run shows").
- **Blank-lines block**: the page element that shows one blank run in edit mode. Add this term to
  `.agents/glossary/common.md`. Do not call it a "gap": "First-element gap" already names
  something else there.

## What changes

### 1. Done on an empty block (empty-block-Q2)

**New block left empty.** `insertionText` (`src/core/mapping/insertion.ts`) already writes
nothing for an empty or whitespace-only text (SwRS-MDOKFSTUDIO-BLOCK-094). The change: it also
drops the whole blank lines at the start of the raw text, the way it already drops the trailing
ones. So a new block that starts with Enters writes no extra blank lines. Indentation on the
first non-blank line is kept: only whole blank lines are dropped.

**Existing block emptied.** The block's text is erased and Done (or Ctrl/Cmd+Enter, or a blur
that commits, BLOCK-047) posts a final `previewEditSave` whose `editedText` is whitespace-only.
On that save the host deletes the block instead of writing `"\n"`:

- The deletion follows the separator rules of `planCut` (SwRS-MDOKFSTUDIO-BLOCK-169): the
  block's lines and one separator go, so its neighbours stay one blank line apart. A first
  block leaves no blank line at the start of the body. A last block keeps the document's final
  line break, or its absence.
- The lines are those of the held edit (`ActiveBlockEdit.line`..`endLine`, applied to the
  document as it was before any autosave). It is one `TextEdit`, through `applyWrittenEdits`,
  that replaces the region from the block's start, autosaved text included, through the
  separator. Earlier autosaves are separate edits already (BLOCK-042). This final one is a single
  undo step that removes the block.
- Where: in `drainActiveBlockEdit` / `handleEditSave` of `src/session/features/blockEdits.ts`,
  for a held edit that is not an insertion, when `finalRequested` and the pending text is
  whitespace-only. The plan is a pure core function, for example `planEmptiedBlockRemoval(text,
  sourceStartOffset, lastSavedText, originalText, line, endLine)` in
  `src/core/edits/sourceEdits.ts`, reusing `planCut` on the text with the original block put
  back.
- Autosaves (`final: false`) of an empty text keep today's behaviour (the `"\n"` placeholder).
  Escape and Cancel keep BLOCK-053: they write the original text back.
- An included block never opens an editor today, so it is not concerned. A block of the
  frontmatter is not a body block: the properties table keeps its own editors.
- After the deletion, the render follows the way it does after a final save. The keyboard
  selection goes to the block that took the deleted block's place (see 3, "After a delete").

### 2. The blank-lines block (empty-block-Q3)

**Where a run shows.** The host finds the blank runs and the page places them.

- Core: a pure function `blankRuns(text): { line: number; endLine: number }[]` in a new file
  `src/core/mapping/blankRuns.ts`. It returns every maximal run of two or more blank lines after
  the frontmatter, as 1-based document lines, in document order, and leaves out the pseudo-line
  after a final line break. It works for LF, CR LF and lone CR (use `splitLines` /
  `sourceLines`).
- Render: the render of the main document adds one element at the end of the content
  container, `<div hidden data-okf-blank-runs="L-E L-E …"></div>` (an empty attribute when there
  is no run), computed from the rendered text. It is in the content, so both the full page and a
  content patch (`src/core/preview/contentPatch.ts`) carry it with the blocks it belongs to: no
  separate message and no race. Add the attribute to the sanitizer's allowlist
  (`src/core/security/html-sanitizer.ts`), or append the element after sanitizing (the value is
  host-made: digits, `-` and spaces only). Name the exact place in `renderPreviewSource`
  (`src/core/render/renderPipeline.ts`) or `renderMyst` when implementing it.
- HTML export: `src/core/export/exportContent.ts` removes the element
  (`REMOVED_BY_ATTRIBUTE`). The page-made blank-lines blocks are editing chrome and are removed
  there too.
- Page: a new feature file `src/page/features/blankLines.ts` (`installBlankLines`) is refreshed
  together with the insert points (`refreshInsertPoints` in
  `src/page/features/insertPoints.ts`). In edit mode only, it reads the runs and places one
  blank-lines block per run:
  - A run inside a top-level block is skipped. A top-level block `B` holds a run when
    `B.line < run.line && run.endLine < B.endLine`, for example blank lines inside a code fence,
    a directive or a list-table. A list whose range ends on its blank separator (BLOCK-256) does
    not hold the run that starts on that line, so that run shows.
  - The block is placed after the last top-level element whose line is before `run.line` (after
    its insert point), or first in the body when there is none. A run between the frontmatter
    and the first block goes after the properties section's insert point.
  - It carries `data-okf-blank-lines`, `data-okf-blank-line="<line>"` and
    `data-okf-blank-end-line="<endLine>"`. It never carries `data-sphinx-source-line`, so it is
    never a mapped block: scroll sync, comments, incoming-change marks and the move logic do not
    see it.
  - A refresh keeps an element whose run is unchanged, as the insert points do. It removes them
    all when edit mode ends, so reading mode is unchanged.
- One blank-lines block per run of two or more blank lines between two blocks, at the end of the
  body (after the last block) and at the start of the body (after the frontmatter, or at the top
  of a file without frontmatter). A single blank line is a separator and shows nothing, at the
  start and at the end of the body too.

**How it looks.** It is about one line high (`min-height` of one line of body text), as wide as
the content column, with a faint dashed outline and, in small muted text, "`N` blank lines". It
shows only in edit mode (CSS in `src/core/preview/styles/editModeStyles.ts`, hidden like
`.sphinx-preview-insert-point` when edit mode is off). It takes the block selection look
(`data-sphinx-preview-block-selected`) when selected. Its accessible name is "`N` blank lines".
It is focusable (`tabindex="0"`, `role="button"`).

**Keyboard and pointer.**

- Plain Up and Down (BLOCK-004, `stepSelection` in `src/page/features/blockSelectionView.ts`)
  stop on a blank-lines block between the blocks around it, in document order.
- Enter on a selected or focused blank-lines block, or a click on it, opens an insertion editor
  at its place (see "Typing in it").
- Delete or Backspace on it, or its Delete block button, removes the extra blank lines (see
  "Removing it").
- A block selection is a run of real blocks. Shift+Up/Down and Shift+click never start or end on
  a blank-lines block. A range of real blocks whose lines span a run includes those lines, as
  today. Ctrl/Cmd+C and +X with only a blank-lines block selected do nothing. Ctrl/Cmd+V with a
  blank-lines block selected pastes after the block above it, as the "+" of that block does.
  Alt+Up/Down does nothing on a blank-lines block, and block moves never treat it as a
  neighbour.
- Escape clears its selection like any block selection.

**Typing in it.** Enter or a click opens an insertion editor (`openBlockEditor` with
`insertAfterLine` = `run.line - 1`) that also names the run it replaces: a new optional field,
for example `replaceBlankRun: { line, endLine }`, on the page messages `previewEditOpen`,
`previewEditSave` and `previewEditCancel`. Add it to the validators of
`src/core/protocol/pageToHost.ts` and `pageToHostMessages.ts`. The host checks the run against
the document: every line from `line` to `endLine` blank, `line - 1` not blank (or the end of the
frontmatter, or the start of the file), `endLine + 1` not blank (or the end of the file). If the
check fails, the host answers with the existing stale reason ("The preview is stale. Reopen the
block before saving.") and changes nothing. The held insertion:

- Holds as its original text the line breaks from the end of line `run.line - 1` to the start of
  line `run.endLine + 1` (to the end of the text for a run at the end).
- Writes a non-empty text in place of that region with exactly one separator before and one after
  (none after at the end of the body, where the document's final line break is kept or kept
  absent). The extra blank lines are gone once the new block is written.
- Writes back the original region for an empty or whitespace-only text, or on Cancel / Escape
  after an autosave (BLOCK-053), so the run is unchanged. On Done with an empty text this is no
  edit at all (BLOCK-263).
- Keeps the document's line endings (BLOCK-234, BLOCK-094).

Plan it in `src/core/mapping/insertion.ts` (an `InsertionPlan` that also replaces a range).
`blockEdits.ts` uses `originalText` / `lastSavedText` as it already does for block edits.
BLOCK-256 is unchanged: no block-edit range ever starts on a blank line, because this is an
insertion.

**Removing it.** Delete, Backspace or the block's button posts a new page message
`previewBlankRunDelete { line, endLine }` (message registry in `pageToHost.ts`, gate `render` in
`src/session/pageMessages.ts`, handler in `src/session/features/sourceEdits.ts`). The host
re-checks the run as above and refuses a stale one with the existing out-of-date reason ("The
preview is out of date. Refresh it and try again."). Otherwise it removes, in one `TextEdit`:

- between two blocks (the frontmatter counts as the block above): lines `line + 1`..`endLine`,
  so one separator stays;
- at the start of a file without frontmatter: all the lines of the run;
- at the end of the body: all the lines of the run, keeping the document's final line break or
  its absence.

The plan is a pure core function, for example `planBlankRunRemoval(text, line, endLine)` in
`src/core/mapping/blockRange.ts`. The result comes back as `previewBlocksResult` with a new
`op: "delete-blank-lines"`, and a refusal shows next to the element the way a cut refusal does.
After the render, the keyboard selection goes to the block that followed the run, or to the block
above it at the end of the body.

### 3. The Delete block button and the Delete key (empty-block-Q4)

**Button.** `addMoveButtons` (`src/page/features/blockMoves.ts`) builds the bar of every body
block (the insert point after it, BLOCK-087/109). It gets one more button:

- class `sphinx-preview-delete`, `type="button"`, `aria-label` and `title` "Delete block",
  text `×`;
- placed right after the down arrow, touching it so the pointer never loses the bar
  (`.sphinx-preview-insert-point button.sphinx-preview-delete { left: 2.6em; }` beside the
  move button rules of `editModeStyles.ts`);
- shown and hidden like the move buttons: on hover of the block, on focus, by the keyboard
  owner rule of BLOCK-109 (`data-sphinx-actions-shown`), and hidden while a block editor is open
  (`data-sphinx-preview-block-editing`);
- not made for an included block (BLOCK-127). The properties section's bar has no move buttons
  and gets no delete button. The "Start writing" entry gets none.

A blank-lines block has the same button (same class, label and glyph) on its left, shown on
hover, focus or selection. It removes the run (section 2).

**What a delete does.** A click on a block's button deletes that block. If a block selection ends
at that block (`selectionEndsAt`), it deletes the whole selection, the way the move buttons act
on a selection. Delete or Backspace with focus on the page (`plainKeyTarget`, never in a text
box, an input, the properties table or an open editor) deletes the block selection if there is
one, or else the focused top-level body block. A blank-lines block is handled as in section 2.
These keys are added in the clipboard key listener's region of `blockSelectionView.ts`. Its guards
also apply: edit mode on, no active block or frontmatter edit, one blocks request in flight at a
time (`blocksFlight`).

The page posts a new message `previewBlocksDelete { line, endLine, pinViewportTop? }`, like
`previewBlocksCut` but with no clipboard write. The host (`handleBlocksCopyCut`'s sibling in
`src/session/features/sourceEdits.ts`, with a core `planBlocksDelete` beside `planBlocksCopyCut`
in `src/core/edits/sourceEdits.ts`):

- checks the span with `checkSpan` (out of date, frontmatter refusals) and refuses a span that
  opens an `{include}` with "A block that comes from an included file cannot be deleted.". This
  message joins the BLOCK-127 family;
- applies `planCut`'s edit: one `TextEdit`, one VS Code undo step, the separator rules and line
  endings of BLOCK-169 and BLOCK-234, and the viewport pin of a cut (`pinViewportTop`, the
  following line);
- answers `previewBlocksResult` with a new `op: "delete"` (extend the `op` union of
  `PreviewBlocksResultMessage` in `src/core/protocol/hostToPage.ts` and of the gate in
  `pageMessages.ts`).

**After a delete.** The block selection goes to the block that took the deleted block's place
(`followingLine`), or to the block above when the last block went. When the body becomes empty,
it goes to the "Start writing" button (BLOCK-102). So pressing Delete repeatedly keeps deleting
from the keyboard, and the screen does not jump (the cut pin).

### 4. Line endings (empty-block-Q5)

Every edit of this change keeps the document's line endings and its final line break, or its
absence: the emptied-block deletion, the blank-lines removal, the blank-lines insertion and Delete
block (BLOCK-234, BLOCK-094, BLOCK-169). The unit tests run each new plan on LF, CR LF and
lone-CR texts.

### 5. Requirements

Per the project's requirements guidelines (IDs come from `okfreq new`, never hand-allocated;
markers move with the code; `just requirements-update`; a dated entry in
`requirements/tiers/log.md`). All of these are in scope `block-editing`:

- Update **SwRS-MDOKFSTUDIO-BLOCK-094**: the leading blank lines of a new block are dropped (new
  boundary row).
- New SwRS: **an existing block emptied and committed is deleted with its separator** (none
  covers this today, per the investigation). Derives from StRS BLOCK-025 and BLOCK-011.
- New SwRS: **edit mode shows each blank run as a blank-lines block** (where it shows, where it
  does not: inside a fence, a single separator, reading mode, export).
- New SwRS: **a blank-lines block takes the keyboard selection and a click** (Up/Down stops,
  Enter and click open the insertion editor, Shift-selection and clipboard rules).
- New SwRS: **typing in a blank-lines block writes the block in place of the run** (one
  separator on each side, an empty Done writes nothing, Cancel restores, stale run refused).
- New SwRS: **removing a blank-lines block keeps one separator** (middle, start, end, line
  endings, stale refusal).
- New SwRS: **Delete block deletes a block with one separator in one undo step** (button
  placement and visibility, Delete / Backspace, selection, included-block refusal, the selection
  afterwards).
- Update **SwRS-MDOKFSTUDIO-BLOCK-127** (the delete refusal), **BLOCK-004** (Up/Down stop on a
  blank-lines block; Delete/Backspace) and **BLOCK-109** (the bar's delete button follows the
  same owner rule), each with a scenario row.
- **StRS-MDOKFSTUDIO-BLOCK-011** and **BLOCK-025**: add the new SwRS to their derivations; touch
  their main paths only if a path now goes through them. BLOCK-025 is `approved`: a new SwRS
  deriving from it (`derives_from` on the SwRS side) leaves its text alone; if its authored text
  must change, its re-approval goes to the owner through the Chief of Staff.

### 6. Shared vocabulary and docs

- `.agents/glossary/common.md`: add "Blank-lines block" and "Delete block button".
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes.
- The release notes of the next version (`docs/releases-notes/`) name the change when the release
  is prepared, not in this PR.

## Out of scope

- Collapsing blank runs by itself (on save, on render, on any edit other than the writer's own
  delete or typing in the run). The file's format is kept: Studio only removes blank lines the
  writer asked to remove (empty-block-Q2).
- Trimming the trailing blank lines of an existing block's edit. The runs they leave are now
  reachable and removable through the blank-lines block.
- Blank lines inside a block (code fence, directive, list-table, HTML block): they are the
  block's content and edited with it (BLOCK-256 unchanged).
- Blank runs in an included file, in the frontmatter, or in a cell of the properties table.
- Moving a blank-lines block, or dragging blocks across it.
- The investigation's option 2 (a "Remove extra blank lines" action on the insert point) and
  option 3 (collapse on save). The owner's direction replaces them (empty-block-Q1).

## Evidence

The checks read the shipped files at the head under test (the real stylesheet module, the real
page bundle, the real core functions), never a prepared copy. Each check below fails on the code
before the change (constitution, section 3).

**Unit (core), `test/core/mapping/`:**

- `blankRuns.test.ts`: runs of 2 and 3 blank lines between blocks; a single separator gives
  nothing; whitespace-only lines count as blank; the pseudo-line after a final break is not
  counted; frontmatter lines and runs inside the frontmatter excluded; a run at the start and at
  the end of the body; LF, CR LF, lone CR.
- `insertion.test.ts`: leading blank lines of a new block dropped (LF, CR LF, CR); an indented
  first line keeps its indentation; the replace-a-run plan writes one separator on each side,
  none after at the end, and writes back the original region for an empty text.
- `blockRange.test.ts`: `planBlankRunRemoval` in the middle, after the frontmatter, at the top of
  a file without frontmatter and at the end (with and without a final line break), with no bare
  LF added in CR LF and no CR in LF. A stale run (a non-blank line inside it, or one more blank
  line next to it) is refused.

**Unit (core edits), `test/core/edits/`:** `planBlocksDelete`: same separator outcomes as the cut
table of BLOCK-169, included-block refusal with its message, frontmatter refusal.
`planEmptiedBlockRemoval`: the owner's case `"# Title\n\nFirst.\n\nSecond paragraph.\n"`,
"First." emptied with an autosave already written gives `"# Title\n\nSecond paragraph.\n"`. Also
the first and the last block, and CR LF.

**Session, `test/session/`:**

- A held block edit with a whitespace-only final save writes one edit that deletes the block,
  and the document matches.
- A blank-lines insertion: autosave, then Cancel, restores the run. An empty Done writes nothing
  and gets `done: true` (BLOCK-263). A stale run is refused with the stale reason.
- `previewBlocksDelete` and `previewBlankRunDelete`: one `applyWrittenEdits` call each,
  `previewBlocksResult` with the new ops, refusal paths.
- The render's content carries `data-okf-blank-runs`, and a content patch updates it.
  `exportContent` removes it (and a page-made blank-lines block).

**Page, `test/page/`** (with the runtime bundle, as `runtimeBlockSelection.test.ts` and
`runtimeBlockMoves.test.ts` do):

- Edit mode places one blank-lines block for a run between blocks, none for a run inside a code
  fence or for a single separator, and one after a list that ends on its separator. Leaving edit
  mode removes them.
- Up/Down stops on it, Enter and click open the insertion editor with `replaceBlankRun`, and
  Delete/Backspace post `previewBlankRunDelete`.
- Every body block's bar has the "Delete block" button, after the down arrow. An included block
  and the properties bar have none. A click posts `previewBlocksDelete` for the block, or for the
  selection that ends there. Delete/Backspace on a selection post it too, and do nothing inside a
  text box or an open editor.
- After a delete result and render, the selection is on the following block.

**Visual (`just ci-visual`):** one capture of edit mode with a blank-lines block between two
paragraphs, one with it selected, and one with the bar of a hovered block showing "+ ↑ ↓ ×".
Captured from the shipped stylesheet, attached to the PR as the pull-request guideline asks.

**Integration (real VS Code, `just ci-integration`, heavy run on the branch):** the owner's
scenario on a real file, in LF and CR LF:

1. Open a file with two paragraphs, turn edit mode on, click "+" after the first, press Enter
   twice and Done: the file is unchanged.
2. Open the first paragraph, erase its text, Done: the paragraph and one separator are gone. One
   Ctrl+Z in the text editor brings the paragraph back.
3. Write three blank lines between the paragraphs in the text editor: the preview shows a
   blank-lines block. Select it with the arrows, press Delete: one blank line is left.
4. Write three blank lines again, click the blank-lines block, type "Middle", Done: the file
   reads `First.`, blank, `Middle`, blank, `Second.` and keeps its line endings.
5. Hover the second paragraph, click "Delete block": it is gone and one Ctrl+Z restores it.

**Requirements:** `just requirements-lint` and `just requirements-update` pass, and the new and
updated SwRS carry `@implements_req` / `@tests_req` markers at the code and tests above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

These points are open in `02-answers.md` or left to the specification. Each is decided here, as
the option most consistent with the product and the answers, for the Chief of Staff to check:

1. **Leading blank lines of a new block are dropped** (BLOCK-094 updated). Q2 says a new block
   "writes nothing (no extra blank lines)". A new block that starts with Enters was one of the
   ways the investigation found to produce the runs.
2. **The trailing blank lines of an existing block's edit are not trimmed.** That is a change to
   BLOCK-234's text round-trip that the answers did not ask for, and the blank-lines block now
   makes those lines reachable.
3. **An emptied existing block is deleted with `planCut`'s separator rules** (BLOCK-169), on
   the final save only. Autosaves keep the `"\n"` placeholder (investigation option 1). The
   final deletion is one undo step; earlier autosaves stay their own steps, as today.
4. **Delete block on a block follows `planCut`'s rules exactly**, so a run right after the
   deleted block goes with it (cut does the same), and a run before it stays. This keeps one
   rule for cut and delete, and never leaves a run created by the delete itself.
5. **Backspace deletes as well as Delete.** On macOS the key labelled "delete" sends Backspace.
   Both are undoable with VS Code's undo, and both act only outside text boxes and editors.
6. **The button glyph is `×`**, placed right after the down arrow. "Delete block" is its
   `aria-label` and `title`, as Q4 asks. It sits in the bar of the block, with the other actions
   of that block ("beside the existing handles"). The left side of a block holds no other bar
   today: list-item and table-row handles belong to items and rows, not to blocks.
7. **The blank-lines block has the same Delete block button**, so the mouse can remove it, as
   the owner asked ("clicable", "Supprimer le block").
8. **A click on a blank-lines block opens the insertion editor**, as a click on any block opens
   its editor in edit mode. Keyboard selection uses the arrows.
9. **Typing in a blank-lines block replaces the run**: one separator stays on each side of the
   new block, and Cancel or an empty Done leaves the run as it was. Q3 says Enter "opens an
   editor on those lines to type text". It is an insertion, not a block edit, so BLOCK-256 holds.
10. **Runs at the start of the body show too** (after the frontmatter, or at the top of the
    file), with the same two-line threshold as elsewhere. At the start of a file without
    frontmatter and at the end of the body, removal takes all the run's lines, because no
    separator is needed there. A single blank line at the start or the end is not shown.
11. **Runs are found by the host and placed by the page**, through one attribute in the rendered
    content. The page has no source text. Carrying the runs in the content keeps them in step
    with the blocks across a content patch.
12. **A block selection never starts or ends on a blank-lines block**, and copy or cut of a lone
    blank-lines block does nothing. A cut must still never start or end on a blank line
    (`checkSpan`), and nothing worth copying is lost.
13. **The selection after a delete goes to the block that took its place** (or the block above,
    or "Start writing"), so the keyboard can go on deleting.
14. **The new SwRS derive from StRS BLOCK-011 and BLOCK-025.** No new StRS: the use case "a
    writer adds and removes blocks; edits land in one undo step" already holds them.
15. **Spec critic**: yes, on Fable (empty-block-Q6, owner's rule). The Chief of Staff runs it.
