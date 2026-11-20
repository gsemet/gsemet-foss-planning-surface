# Show blank-line runs as a reachable blank-lines block in edit mode

In edit mode, every run of two or more blank lines in the body shows as a small blank-lines block.
The writer reaches it with the arrows, clicks it to type a block in its place, and removes it with
Delete, Backspace or its Delete block button, keeping one separator.

Origin: verbal (owner, 2026-11-20, testing 1.10.0). No issue.

## Goal

The owner asked for this in edit mode. "en mode edition il faudrait que les ligne vide au dela
que 1 (qui sert de delimiter en md) soit representé par un petit block vide, selectable par le
clavier et clicable. et il faut rajouter un bouton a gauche Supprimer le block." (blank-runs-Q1).

The page shows no blank lines: markdown-okf makes no token, no DOM node and no source-map entry
for them. Extra blank lines already in a file therefore cannot be reached from Studio. They come
from hand edits, merges and older Studio versions (`empty-block-reachable/work/investigation.md`).
`empty-block-reachable` stops Studio from writing new runs and adds the Delete block button and
keys. This CR makes the runs already in a file visible and removable.

**Stack.** This CR lands after `3-ready/empty-block-reachable` in the same stack and builds on it
(blank-runs-Q3). It reuses that CR's `createDeleteBlockButton` helper (`src/page/modules/`), its
key dispatch `deleteSelection()` in `src/page/features/blockSelectionView.ts`, its
`previewBlocksResult` `op` union extension and its "Delete block button" glossary entry. Start
from that CR's merged head, or from its branch while the stack is open.

Project rules: this change follows the project's constitution (`.agents/constitution.md` in
markdown-okf-schema-studio), its `AGENTS.md` (requirements, completion gate `just preflight`) and
the requirements guidelines named there. This specification restates none of them.

## Words

- **Separator**: the one blank line between two blocks that Markdown needs.
- **Blank line**: the shared `isBlank` of `src/core/mapping/blockRange.ts`, exported and used
  everywhere this CR tests for blank lines; no other module restates it (blank-runs-Q4). See
  section 1 for its new definition. The empty pseudo-line after a final line break (BLOCK-234) is
  not a line (`splitLines` of `src/core/mapping/blockMove.ts` does not return it).
- **Blank run**: a maximal sequence of two or more blank lines in the body, outside the content of
  every top-level block (section 2, "Where a run shows").
- **Blank-lines block**: the page element that shows one blank run in edit mode. Add this term to
  `.agents/glossary/common.md` ("Blank-lines block"; "Blank run"). Do not call it a "gap":
  "First-element gap" already names something else there.

## What changes

### 1. One shared blank-line test (blank-runs-Q4)

`isBlank` in `src/core/mapping/blockRange.ts` today is `text.trim() === ""`. JavaScript's `trim`
also strips U+00A0 and other Unicode spaces. A line of U+00A0 renders as a paragraph
(markdown-it renders `"a\n\n \n\nb"` as three paragraphs), so `trim` would count a real
block as blank.

- `isBlank` becomes CommonMark's blank line: a line holding only spaces (U+0020) and tabs, for
  example `/^[ \t]*$/u.test(text)`. It is exported from `blockRange.ts`.
- `blockMove.ts` drops its own copy (`const isBlank = (line: SourceLine) => ...`) and calls the
  exported one on `line.text`. `blockRange.ts` already imports `splitLines` from `blockMove.ts`,
  so this makes an import cycle of two function modules. `.dependency-cruiser.cjs` has no
  circular-import rule, and both functions are only called at run time, so the cycle is safe. If
  the Driver prefers no cycle, move `splitLines`, `SourceLine` and `isBlank` together into a new
  `src/core/mapping/sourceLines.ts` and re-export them from their current modules. That keeps one
  definition.
- **Effect on existing checks.** `checkSpan`, `planCut`, the BLOCK-256 edit-range check and
  `planBlockMove` now treat a U+00A0-only line as a block line, not as a blank line. Such a
  paragraph can then be cut, copied, moved and edited like any other, where it was refused as out
  of date before. Every other `trim() === ""` test in `src/` keeps its behaviour (out of scope).

### 2. The blank-lines block (blank-runs-Q2)

**Where a run shows.** The host finds the blank runs and the page places them. The page has no
source text.

- **Core.** A pure function `blankRuns(text): { line: number; endLine: number }[]` goes in a new
  file `src/core/mapping/blankRuns.ts`. It returns every maximal run of two or more blank lines
  (`isBlank`) after the frontmatter, as 1-based document lines, in document order. It uses
  `splitLines`, so the pseudo-line after a final line break is never counted. It works the same in
  LF, CR LF and lone CR. The frontmatter's lines come from `matchFrontmatterBlock`, as
  `frontmatterLineCount` in `blockRange.ts` reads them.
- **Render.** `renderPreviewSource` (`src/core/render/renderPipeline.ts`) appends one element to
  the rendered HTML: `<div hidden data-okf-blank-runs="L-E L-E ..."></div>`. It is computed with
  `blankRuns(input.text)`, and the attribute is empty when there is no run. Because it is in the
  content, the full page and a content patch (`src/page/features/contentPatch.ts`,
  `src/core/preview/contentPatch.ts`) both carry it with the blocks it belongs to. That means no
  separate message and no race. The sanitizer already keeps `data-okf-*` attributes
  (`ALLOWED_ATTRIBUTE_PREFIXES` in `src/core/security/html-sanitizer.ts`). The value is host-made:
  digits, `-` and spaces only. The page parses it strictly and ignores a malformed pair.
- **Export.** `src/core/export/exportContent.ts` adds `data-okf-blank-runs` and
  `data-okf-blank-lines` to `REMOVED_BY_ATTRIBUTE`. The HTML export then carries neither the run
  list nor a page-made blank-lines block, and it is unchanged.
- **Page.** A new feature file `src/page/features/blankLines.ts` (`installBlankLines(rt)`,
  exposed on the page runtime like `rt.insertPoints`) has a `refresh()`. In edit mode, `refresh()`
  reads the runs and places one blank-lines block per run. Out of edit mode, it removes them all,
  so reading mode is unchanged. It runs:
  - right after `refreshInsertPoints` (in `applyEditMode`, `src/page/features/editMode.ts`, and
    `frontmatterEditor.ts` line 70);
  - after `parts.headingFold.apply()` in `initializeContent` (`contentPatch.ts`);
  - after every fold change. Add the call to the `onLayoutChange` hook that `src/page/runtime.ts`
    passes to `installHeadingFold`, or give `HeadingFold` a hook named for it.
- **Placement rules.** They use the body's top-level mapped blocks
  (`rt.blocks.topLevelMappedBlocks()`, without the properties section):
  - **Inside a block.** A top-level block `B` holds a run when
    `B.line < run.line && run.endLine < B.endLine`. Examples: blank lines inside a code fence, a
    directive, a list-table or an HTML block. Such a run shows nothing. A list whose range ends
    on its blank separator (BLOCK-256) does not hold the run that starts on that line, so that
    run shows.
  - **Position.** The block goes after the last top-level block whose `line` is before
    `run.line`, after that block's insert point. With none, it goes first in the body: after the
    properties section's insert point when there is frontmatter, or first in the content
    container.
  - **Folded sections (blank-runs-Q5).** A run whose preceding top-level block carries
    `data-okf-folded` shows nothing. The same holds when its following block carries it: the run
    then lies inside a folded section, right after its heading. Unfolding shows it again.
  - **Empty body.** When the body has no block but the text has a run (a file of only
    frontmatter and blank lines, or only blank lines), the run shows before the "Start writing"
    entry (BLOCK-102). That way it stays reachable.
  - **Thresholds.** A single blank line is a separator and shows nothing, at the start and at the
    end of the body too.
- **Attributes.** The element carries `data-okf-blank-lines`, `data-okf-blank-line="<line>"` and
  `data-okf-blank-end-line="<endLine>"`. It never carries `data-sphinx-source-line`, so it is
  never a mapped block: scroll sync, comments, incoming-change marks, the structural navigation
  and the move logic do not see it.
- **Refresh.** A refresh keeps the element of an unchanged run (same line, same end line, same
  anchor), as the insert points do (`reusablePoint`), so focus and selection survive a re-render.

**How it looks.** CSS goes in one named block of `src/core/preview/styles/editModeStyles.ts`.

- About one line of body text high (`min-height`), as wide as the content column, with a faint
  dashed outline.
- Its label, in small muted text: "`N` blank lines". It is drawn with CSS generated content from
  an attribute (for example `data-okf-blank-label`), so the find bar, copy and text extraction
  never see it.
- Its accessible name is the same text (`aria-label`). It has `role="button"` and `tabindex="0"`.
- It is hidden out of edit mode, like `.sphinx-preview-insert-point`.
- When selected, it takes the block selection look (`data-sphinx-preview-block-selected`).
- It holds one Delete block button from `createDeleteBlockButton(document, onDelete)`, at its
  left edge, with no copied markup or CSS. The button shows on hover or focus of the blank-lines
  block or while it is selected, and hides while a block editor is open
  (`data-sphinx-preview-block-editing`), as on the block bars.

**Keyboard and pointer (blank-runs-Q2, Q6).**

- **Arrows.** Plain Up and Down (`stepSelection` in `blockSelectionView.ts`, BLOCK-004) stop on a
  blank-lines block between the blocks around it, in document order. The view keeps it as a
  "selected blank-lines block", one at a time, beside the block selection. It never enters the
  block selection's range. A visible blank-lines block is one that is placed and not hidden: the
  folded rules above already left out the hidden ones.
- **Enter or click.** Enter on a selected or focused blank-lines block, or a click on it (not on
  its Delete block button), opens an insertion editor in its place ("Typing in it").
- **Delete and Backspace.** On a selected blank-lines block, with the key target on the page
  (`plainKeyTarget`), Delete and Backspace remove it ("Removing it"). The key goes through the
  same `deleteSelection()` as a block selection; this CR extends that function. They do the same
  on a focused blank-lines block. Its Delete block button does the same on click. The guards of
  `empty-block-reachable` hold: edit mode on, no active block or frontmatter edit, one blocks
  request in flight (`blocksFlight`).
- **The block selection (Q6).** A block selection never starts or ends on a blank-lines block.
  - Shift+Down from a selected blank-lines block starts the block selection on the next block.
    Shift+Up starts it on the previous block.
  - Shift+Up/Down that extends a range of blocks steps over blank-lines blocks.
  - Shift+click on a blank-lines block does nothing.
  - A range of blocks whose lines span a run includes those lines, as today.
- **Clipboard.** Ctrl/Cmd+C and Ctrl/Cmd+X with only a blank-lines block selected do nothing.
  Ctrl/Cmd+V with a blank-lines block selected pastes after the block above it, as that block's
  "+" would (at the start of the body: at `afterLine` 0).
- **Other keys.** Alt+Up/Down does nothing on a blank-lines block, and block moves never treat it
  as a neighbour. Escape clears its selection like any block selection.
- **Structural navigation** (BLOCK-254) never enters a blank-lines block.

**Typing in it.** Enter or a click opens an insertion editor:
`rt.blockEditor.openBlockEditor(element, undefined, { line, endLine, insertAfterLine:
run.line - 1, replaceBlankRun: { line: run.line, endLine: run.endLine } }, "end")`.

- **Messages.** `replaceBlankRun: { line, endLine }` is a new optional field on
  `previewEditOpen`, `previewEditSave` and `previewEditCancel`. Add it to
  `src/core/protocol/pageToHostMessages.ts` and to `hasValidStateFields` in
  `src/core/protocol/pageToHost.ts`. It is valid only on `BLOCK_EDIT_TYPES`, only with
  `insertAfterLine`, with both lines `isSourceLine` and `line < endLine`.
- **The host checks the run** on open (`src/session/features/blockEdits.ts`, where
  `insertAfterLine` is handled today). These must hold:
  - every line from `line` to `endLine` is blank;
  - line `line - 1` is not blank, or is the last line of the frontmatter, or `line` is 1;
  - line `endLine + 1` is not blank, or `endLine` is the last line.

  On a failed check, the host answers with the existing stale reason ("The preview is stale.
  Reopen the block before saving.") and changes nothing. A save or cancel whose `replaceBlankRun`
  differs from the held edit's is refused the same way, as a different `insertAfterLine` is
  today.
- **The held insertion.**
  - **Original text.** The region from the end of line `run.line - 1` to the start of line
    `run.endLine + 1`: the start of the text when `run.line` is 1, the end of the text for a run
    at the end. Its `originalText` is that region. `lastSavedText` follows autosaves as for block
    edits.
  - **A non-empty text** replaces that region. Exactly one separator goes before it: none at the
    start of a file without frontmatter. Exactly one separator goes after it: none at the end of
    the body, where the document's final line break is kept, or kept absent. The extra blank
    lines are gone once the block is written. Leading blank lines of the typed text are dropped
    (`insertionText`, BLOCK-094 as `empty-block-reachable` changes it).
  - **Empty text.** An empty or whitespace-only text writes the original region back. So does
    Cancel or Escape after an autosave (BLOCK-053). Either way the run is unchanged. On Done with
    an empty text before any autosave there is no edit at all, and the editor closes (BLOCK-263).
  - **Line endings.** The document's line endings are kept (BLOCK-234, BLOCK-094).
- **Where the plan goes.** In `src/core/mapping/insertion.ts`, an `InsertionPlan` with an
  optional replaced range (for example `replace?: { start: number; end: number }`), built by a new
  `planBlankRunInsertion(text, line, endLine)`. It is used by `blockEdits.ts` the way
  `planInsertion` is today. BLOCK-256 is unchanged: no block-edit range starts on a blank line,
  because this is an insertion.

**Removing it.** The trigger is Delete or Backspace on a selected or focused blank-lines block,
or its Delete block button.

- **The message.** The page posts a new message `previewBlankRunDelete { line, endLine }`.
  Register it in the message registry (`src/core/protocol/pageToHost.ts`,
  `pageToHostMessages.ts`) with gate `render` (`src/session/pageMessages.ts`). Its handler goes
  beside `handleBlocksDelete` of `empty-block-reachable` in `src/session/features/sourceEdits.ts`.
- **The check.** The host re-checks the run as above. It refuses a stale one with the existing
  out-of-date reason ("The preview is out of date. Refresh it and try again.").
- **What goes.** One `TextEdit` through `applyWrittenEdits`, one VS Code undo step, removes:
  - between two blocks, the frontmatter counting as the block above: lines
    `line + 1`..`endLine`, so one separator stays;
  - at the start of a file without frontmatter, before a block: all the lines of the run;
  - at the end of the body, after a block or the frontmatter, or in a text of only blank lines:
    all the lines of the run. The text then ends where line `line - 1` ends, with its line break
    when the document had a final line break and without it when it had none. A text of only
    blank lines becomes empty.
- **The plan** is a pure core function `planBlankRunRemoval(text, line, endLine)` in
  `src/core/mapping/blockRange.ts`, returning `{ start, end, followingLine }` or a refusal.
- **The answer.** `previewBlocksResult` with a new `op: "delete-blank-lines"`. Extend the `op`
  union of `PreviewBlocksResultMessage` in `src/core/protocol/hostToPage.ts`, and the gate in
  `pageMessages.ts`. A refusal shows next to the blank-lines block, as a cut refusal shows next to
  its bar.
- **After the render**, the keyboard selection goes to the block that followed the run, or to the
  block above it at the end of the body, or to "Start writing" when the body is empty. The screen
  does not jump: use the cut's viewport pin (`pinViewportTop` on the following line).

### 3. Line endings (blank-runs-Q7)

Every edit of this change keeps the document's line endings and its final line break, or its
absence: the blank-lines removal and the blank-lines insertion (BLOCK-234, BLOCK-094, BLOCK-169).
The unit tests run each new plan on LF, CR LF and lone-CR texts.

### 4. Requirements

Follow the project's requirements guidelines: IDs come from `okfreq new` and are never
hand-allocated; markers move with the code; run `just requirements-update`; add a dated entry in
`requirements/tiers/log.md`. All of these are in scope `block-editing`:

- New SwRS: **edit mode shows each blank run as a blank-lines block**. It covers where a run shows
  and where it does not: inside a fence, a single separator, a folded section, reading mode and
  the export.
- New SwRS: **a blank-lines block takes the arrows, Enter and a click**. It covers Up/Down
  stops, the insertion editor, and the block selection and clipboard rules of Q6.
- New SwRS: **typing in a blank-lines block writes the block in place of the run**. It covers one
  separator on each side, an empty Done writing nothing, Cancel restoring the run, and a stale run
  refused.
- New SwRS: **removing a blank-lines block keeps one separator**. It covers the middle, after the
  frontmatter, the start, the end, line endings, one undo step, the stale refusal and the
  selection afterwards.
- Update **SwRS-MDOKFSTUDIO-BLOCK-004** (Up/Down stop on a blank-lines block) with a scenario
  row. Update the Delete block SwRS added by `empty-block-reachable` (its Delete, Backspace and
  button also remove a selected blank-lines block) with a scenario row.
- Update **SwRS-MDOKFSTUDIO-BLOCK-124** (a span's first and last line are not blank) with a row: a
  U+00A0-only paragraph is a block line, not a blank line (section 1).
- The new SwRS derive from **StRS-MDOKFSTUDIO-BLOCK-011** (`proposed`) and **BLOCK-025**
  (`approved`) through `derives_from`, which leaves their authored text alone. If BLOCK-025's text
  must change, its re-approval goes to the owner through the Chief of Staff.

### 5. Shared vocabulary and docs

- `.agents/glossary/common.md`: "Blank-lines block" and "Blank run" (see "Words").
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes. The blank-lines block is edit-mode chrome, absent from reading mode and the
  export.
- The release notes are written when the release is prepared, not in this PR.

## Out of scope

- Everything `empty-block-reachable` delivers: Done on an empty block, the insertion fix, and the
  Delete block button and keys on blocks.
- Collapsing blank runs by itself: on save, on render, or on any edit other than the writer's own
  removal of, or typing in, a run. The file's format is kept.
- Blank lines inside a block (code fence, directive, list-table, HTML block): they are the
  block's content and are edited with it (BLOCK-256 unchanged).
- Blank runs in an included file, in the frontmatter or in a cell of the properties table.
- Moving a blank-lines block, or dragging blocks across it.
- The other `trim() === ""` tests of `src/` (insertion separators, `withoutTrailingBlankLines`,
  comments, renderer helpers): unchanged.
- Cut and copy of a span that ends on a list's blank separator:
  `1-inbox/cut-copy-list-trailing-blank`.

## Evidence

The checks read the shipped files at the head under test: the real stylesheet module, the real
page bundle, the real core and render functions, never a prepared copy. Each check below fails on
the code before the change (constitution, section 3).

**Unit (core), `test/core/mapping/`:**

- `blankRuns.test.ts`:
  - runs of 2 and 3 blank lines between blocks;
  - a single separator gives nothing;
  - space-only and tab-only lines count as blank;
  - a U+00A0-only line is never part of a run (it breaks `"a\n\n\n \n\n\nb"` into two runs);
  - the pseudo-line after a final break is not counted;
  - frontmatter lines are excluded;
  - runs at the start and at the end of the body;
  - LF, CR LF and lone CR.
- `blockRange.test.ts`:
  - `planBlankRunRemoval` in the middle, after the frontmatter, at the top of a file without
    frontmatter, at the end with and without a final line break, and in a text of only blank
    lines;
  - no bare LF added in CR LF and no CR added in LF;
  - a stale run refused: a non-blank line inside it, or one more blank line next to it.
- `blockRange.test.ts` and `blockMove.test.ts`: a U+00A0-only paragraph is cut and moved like
  another block (section 1).
- `insertion.test.ts`: `planBlankRunInsertion` writes one separator on each side, none before at
  the top of a file without frontmatter, none after at the end, and writes back the original
  region for an empty text. LF, CR LF and CR.

**Render and export:**

- `renderPreviewSource` output carries `data-okf-blank-runs` with the right pairs, and an empty
  value for a text with no run.
- A content patch updates it.
- `exportContent` removes it and a page-made `data-okf-blank-lines` element.

**Session, `test/session/`:**

- A blank-lines insertion:
  - with text, it writes one separator on each side;
  - an autosave then Cancel restores the run;
  - an empty Done writes nothing and gets `done: true` (BLOCK-263);
  - a stale run is refused with the stale reason.
- `previewBlankRunDelete`: one `applyWrittenEdits` call, `previewBlocksResult` with
  `op: "delete-blank-lines"`, and the refusal path.
- The validator rejects `replaceBlankRun` without `insertAfterLine`, on another message type, or
  with `line >= endLine`.

**Page, `test/page/`** (with the runtime bundle, as `runtimeBlockSelection.test.ts` and
`runtimeBlockMoves.test.ts` do):

- Edit mode places one blank-lines block for a run between blocks. It places none for a run
  inside a code fence, for a single separator, or after a folded block. It places one after a
  list that ends on its separator, and one before "Start writing" in an empty body. Leaving edit
  mode removes them. Folding and unfolding a section hides and shows them.
- Up/Down stops on it. Enter and a click open the insertion editor and post `previewEditOpen`
  with `replaceBlankRun`.
- Delete and Backspace post `previewBlankRunDelete`, and so does its Delete block button.
- Shift+Up/Down never starts or ends a block selection on it. Ctrl/Cmd+C and +X post nothing with
  only it selected.
- The label is not in the element's text content (the find bar does not match "blank lines").
- After a removal result and render, the selection is on the following block.

**Visual (`just ci-visual`):** three captures from the shipped stylesheet, attached to the PR as
the pull-request guideline asks:

- edit mode with a blank-lines block between two paragraphs;
- the same block selected, with its Delete block button shown;
- reading mode of the same file, with no blank-lines block.

**Integration (real VS Code, `just ci-integration`, heavy run on the branch).** The scenario runs
on a real file, once in LF and once in CR LF:

1. Write three blank lines between two paragraphs in the text editor. Turn edit mode on: the
   preview shows one blank-lines block. Select it with the arrows and press Delete: one blank
   line is left. One Ctrl+Z in the text editor brings the three back.
2. Write three blank lines again, click the blank-lines block, type "Middle" and press Done. The
   file reads `First.`, blank, `Middle`, blank, `Second.` and keeps its line endings.
3. Write three blank lines again, click the blank-lines block and press Cancel: the file is
   unchanged.
4. Write three blank lines at the end of the file and click the Delete block button of the
   blank-lines block: the file ends with `Second.` and its final line break.
5. Turn edit mode off: no blank-lines block shows.

**Requirements:** `just requirements-lint` and `just requirements-update` pass. The new and
updated SwRS carry `@implements_req` / `@tests_req` markers at the code and tests above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

The answers leave these points to the specification. The owner is away and gave the Chief of
Staff autonomy, so each is decided here, as the option most consistent with the product and the
answers, for the Chief of Staff to check:

1. **The shared `isBlank` becomes CommonMark's blank line** (spaces and tabs only). Q4 asks for
   the shared test and for a U+00A0 line never to be part of a run. Today's `trim()` test counts
   such a line as blank, so the one shared definition changes. `blockMove.ts` uses it too. Cut,
   copy, move and edit of a U+00A0 paragraph therefore stop being refused (BLOCK-124 row). The
   other `trim()` tests of `src/` are left alone.
2. **Runs are found by the host and placed by the page**, through one attribute in the rendered
   content. The page has no source text, and carrying the runs in the content keeps them in step
   with the blocks across a content patch.
3. **A run is hidden when the block after it is folded too**, not only the block before it
   (Q5). A run right after a folded section's heading is inside that section.
4. **A run in an empty body shows before "Start writing"**, so no run is ever out of reach.
5. **The label is drawn by CSS from an attribute**, so the find bar and copy never see the text
   "blank lines".
6. **The Delete block button sits at the left edge of the blank-lines block**, from
   `createDeleteBlockButton`, shown on hover, focus or selection. Q1 says "a gauche", and the
   blank-lines block has no bar of its own.
7. **A focused blank-lines block takes Delete and Backspace like a selected one.** Arrows select
   it and Tab focuses it. Either way the writer has picked that single element, unlike a merely
   focused real block (empty-block-Q10).
8. **Shift+arrow from a selected blank-lines block starts the block selection on the neighbour**
   in that direction (Q6: never on the blank-lines block itself).
9. **Ctrl/Cmd+V on a selected blank-lines block pastes after the block above**, as that block's
   "+" would. Cut and copy of it alone do nothing (Q6).
10. **Removal returns the selection to the following block** (or the block above, or "Start
    writing") with the cut's viewport pin, as Delete block does in `empty-block-reachable`.
11. **The new SwRS derive from StRS BLOCK-011 and BLOCK-025.** No new StRS.
12. **Spec critic**: yes, on Fable (blank-runs-Q8, owner's rule). The Chief of Staff runs it.
