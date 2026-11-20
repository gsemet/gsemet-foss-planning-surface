# Show blank-line runs as a reachable blank-lines block in edit mode

In edit mode, every run of two or more blank lines between top-level blocks shows as a small
blank-lines block. The writer reaches it with the arrows, clicks it to type a block in its place,
and removes it with Delete, Backspace or its Delete block button, keeping one separator.

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

**Stack (blank-runs-Q3).** This CR lands after **CR-439**
(`4-batch/2-actives/439-empty-block-reachable` in the planning folder, branch
`chantier/batch-07/cr-439-empty-blocks-leave-no-blank-lines-and-a-`) in the same stack, and
builds on it. It reuses CR-439's pieces:

- the `createDeleteBlockButton` helper (`src/page/modules/`);
- the key dispatch `deleteSelection()` in `src/page/features/blockSelectionView.ts`;
- `handleBlocksDelete` in `src/session/features/sourceEdits.ts`;
- the `previewBlocksResult` `op` union extension;
- the "Delete block button" glossary entry.

Branch from CR-439's branch while the stack is open, or from its merged head. Its spec is
`03-change-spec.md` in that folder.

Project rules: this change follows the project's constitution (`.agents/constitution.md` in
markdown-okf-schema-studio), its `AGENTS.md` (requirements, completion gate `just preflight`) and
the requirements guidelines named there. This specification restates none of them.

## Words

- **Separator**: the one blank line between two blocks that Markdown needs.
- **CommonMark blank line**: a line holding only spaces (U+0020) and tabs. It is tested by the new
  exported function of section 1, never by a restated regex (blank-runs-Q4, Q9). A line of U+00A0
  is not blank: it renders as a paragraph. The empty pseudo-line after a final line break
  (BLOCK-234) is not a line (`splitLines` of `src/core/mapping/blockMove.ts` does not return it).
- **Blank run**: a maximal sequence of two or more CommonMark blank lines in the body, between
  top-level blocks, at the start of the body or at its end (section 2, "Where a run shows").
- **Blank-lines block**: the page element that shows one blank run in edit mode. Add this term to
  `.agents/glossary/common.md` ("Blank-lines block"; "Blank run"). Do not call it a "gap":
  "First-element gap" already names something else there.

## What changes

### 1. The CommonMark blank test (blank-runs-Q4, Q9)

- Add one exported function to `src/core/mapping/blockRange.ts`, for example
  `isCommonMarkBlank(text: string): boolean`, true for a line of only spaces and tabs
  (`/^[ \t]*$/u`). JavaScript's `trim` also strips U+00A0, and markdown-it renders
  `"a\n\n \n\nb"` as three paragraphs, so a `trim()` test would count a real block as blank.
- It has two callers, and no other: `blankRuns` (section 2) and the run checks of the host (the
  insertion, paste and removal checks of section 2, all through one helper, for example
  `checkBlankRun(text, line, endLine)` in `blockRange.ts`).
- The existing `isBlank` of `blockRange.ts` and `blockMove.ts`, and their callers (`checkSpan`,
  `planCut`, the BLOCK-256 check, `planBlockMove`), keep `trim()` unchanged. Moving them to the
  new function is backlog `blank-line-check-unicode-spaces`, which names it.

### 2. The blank-lines block (blank-runs-Q2)

**Where a run shows.** The host finds the blank runs and the page places them. The page has no
source text.

- **Core.** A pure function `blankRuns(text): { line: number; endLine: number }[]` goes in a new
  file `src/core/mapping/blankRuns.ts`. It returns every maximal run of two or more CommonMark
  blank lines after the frontmatter, as 1-based document lines, in document order. It uses
  `splitLines`, so the pseudo-line after a final line break is never counted. It works the same in
  LF, CR LF and lone CR. The frontmatter's lines come from `matchFrontmatterBlock`, as
  `frontmatterLineCount` in `blockRange.ts` reads them.
- **Render.** `renderPreviewSource` (`src/core/render/renderPipeline.ts`) appends one element at
  the very end of the rendered HTML: `<div hidden data-okf-blank-runs="L-E L-E ..."></div>`. It is
  computed with `blankRuns(input.text)`, and the attribute is empty when there is no run. Because
  it is in the content, the full page and a content patch (`src/page/features/contentPatch.ts`,
  `src/core/preview/contentPatch.ts`) both carry it with the blocks it belongs to. That means no
  separate message and no race. The value is host-made: digits, `-` and spaces only.
- **The page trusts only the host's element (fix 6).** The sanitizer keeps every `data-okf-*`
  attribute (`ALLOWED_ATTRIBUTE_PREFIXES` in `src/core/security/html-sanitizer.ts`). An author can
  therefore write `<div data-okf-blank-runs="1-9">` in the Markdown, and it reaches the page.
  - The page reads the runs only from the **last element child of the content container**
    (`#sphinx-myst-preview-content`), and only when that element carries `data-okf-blank-runs`.
  - Any other element with that attribute is ignored. The page parses the value strictly and
    ignores a malformed pair or a pair with `line >= endLine`.
  - The page builds every blank-lines block itself (`document.createElement`). It never makes an
    element of the content into one, and it never reads `data-okf-blank-lines`,
    `data-okf-blank-line` or `data-okf-blank-end-line` from authored content: it keeps its own
    elements in a `Set`, as `insertPoints.ts` does with `made`.
  - If the content patch keeps the run list somewhere other than the end, the Driver names where
    the host appends it and the page reads it from that one place.
- **Export.** `src/core/export/exportContent.ts` adds `data-okf-blank-runs` and
  `data-okf-blank-lines` to `REMOVED_BY_ATTRIBUTE`. The HTML export then carries neither the run
  list nor a page-made blank-lines block, and it is unchanged.
- **Page.** A new feature file `src/page/features/blankLines.ts` (`installBlankLines(rt)`,
  exposed on the page runtime like `rt.insertPoints`) has a `refresh()`. In edit mode, `refresh()`
  places one blank-lines block per run. Out of edit mode, it removes them all, so reading mode is
  unchanged. It runs:
  - right after `refreshInsertPoints` (in `applyEditMode`, `src/page/features/editMode.ts`, and
    `frontmatterEditor.ts` line 70);
  - after `parts.headingFold.apply()` in `initializeContent` (`contentPatch.ts`);
  - after every fold change. Add the call to the `onLayoutChange` hook that `src/page/runtime.ts`
    passes to `installHeadingFold`, or give `HeadingFold` a hook named for it.
- **Placement rules.** They use the body's top-level mapped blocks
  (`rt.blocks.topLevelMappedBlocks()`, without the properties section):
  - **Inside a block (blank-runs-Q11).** A top-level block `B` holds a run when
    `B.line < run.line && run.endLine < B.endLine`. Such a run shows nothing. Examples: blank lines
    inside a code fence, a directive, a list-table or an HTML block, between the items of a list,
    and inside a quote, an admonition or a list item. Runs inside lists and containers are out of
    scope, filed as `1-inbox/blank-runs-inside-lists`. A list whose range ends on its blank
    separator (BLOCK-256) does not hold the run that starts on that line, so that run shows.
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
- **The open editor's host (fix 7).** While an insertion editor opened from a blank-lines block
  is open (`state.activeBlockEdit` with `replaceBlankRun`), a refresh never removes or moves that
  blank-lines block. An autosave writes the typed text in place of the run, so the next render no
  longer has that run, and the refresh keeps the block anyway:
  - it keeps its element, its place and its `replaceBlankRun` lines;
  - it hides the dashed look and the label while the editor is inside it.

  The block goes, or comes back as a run, at the first refresh after the editor closes (Done,
  Cancel, Escape, blur).

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

**Keyboard and pointer (blank-runs-Q2, Q6, Q10, Q12).**

- **Arrows.** Plain Up and Down (`stepSelection` in `blockSelectionView.ts`, BLOCK-004) stop on a
  visible blank-lines block between the blocks around it, in document order. The view keeps it as
  a "selected blank-lines block", one at a time, beside the block selection. It never enters the
  block selection's range.
- **Enter or click.** Enter on a selected or focused blank-lines block, or a click on it (not on
  its Delete block button), opens an insertion editor in its place ("Typing in it").
- **Delete and Backspace (Q10).** On a **selected** blank-lines block, with the key target on the
  page (`plainKeyTarget`), Delete and Backspace remove it ("Removing it"). They go through
  CR-439's `deleteSelection()`, which this CR extends. They do nothing on a blank-lines block that
  is only focused (Tab) and not selected, as on a focused real block (empty-block-Q10). The Delete
  block button removes it on click, selected or not. CR-439's guards hold: edit mode on, no
  active block or frontmatter edit, one blocks request in flight (`blocksFlight`).
- **The block selection (Q6).** A block selection never starts or ends on a blank-lines block.
  - Shift+Down from a selected blank-lines block starts the block selection on the next block.
    Shift+Up starts it on the previous block.
  - Shift+Up/Down that extends a range of blocks steps over blank-lines blocks.
  - Shift+click on a blank-lines block does nothing: the selection is unchanged.
  - A range of blocks whose lines span a run includes those lines, as today.
- **Clipboard.**
  - Ctrl/Cmd+C and Ctrl/Cmd+X with only a blank-lines block selected do nothing.
  - **Ctrl/Cmd+V (Q12)** with a blank-lines block selected pastes in place of the run, like
    typing in it, with one separator on each side. The page posts `previewBlocksPaste` with a new
    optional field `replaceBlankRun: { line, endLine }` and `insertAfterLine: run.line - 1`. Add
    the field to `PreviewBlocksPasteMessage` (`pageToHostMessages.ts`) and its validator
    (`pageToHost.ts`).
  - The host checks the run (`checkBlankRun`), and refuses a stale run with the out-of-date
    reason. Otherwise it writes, in one `TextEdit`, the pasted block in place of the region
    defined in "Typing in it". `planPaste` gains an optional replaced range: for example
    `planBlankRunPaste(text, line, endLine, raw)` returning `PastePlan` with an `end` offset.
  - The selection afterwards follows a paste.
- **Other keys.**
  - Alt+Up/Down does nothing on a selected blank-lines block: no message, no move. Block moves
    never treat it as a neighbour.
  - Escape clears its selection like any block selection.
  - The structural navigation (BLOCK-254) never enters a blank-lines block.

**Typing in it.** Enter or a click opens an insertion editor:
`rt.blockEditor.openBlockEditor(element, undefined, { line, endLine, insertAfterLine:
run.line - 1, replaceBlankRun: { line: run.line, endLine: run.endLine } }, "end")`.

- **Messages.** `replaceBlankRun: { line, endLine }` is a new optional field on
  `previewEditOpen`, `previewEditSave` and `previewEditCancel`. Add it to
  `src/core/protocol/pageToHostMessages.ts` and to `hasValidStateFields` in
  `src/core/protocol/pageToHost.ts`. It is valid only on `BLOCK_EDIT_TYPES`, only with
  `insertAfterLine`, with both lines `isSourceLine` and `line < endLine`.
- **The run check** (`checkBlankRun`, one helper for open, save, paste and removal). These must
  hold:
  - every line from `line` to `endLine` is a CommonMark blank line;
  - line `line - 1` is not blank, or is the last line of the frontmatter, or `line` is 1;
  - line `endLine + 1` is not blank, or `endLine` is the last line.
- **The region.** The run's region runs from the end of line `run.line - 1` to the start of line
  `run.endLine + 1`. It starts at the start of the text when `run.line` is 1, and ends at the end
  of the text for a run at the end.
- **Open (`handleEditOpen`, `src/session/features/blockEdits.ts`, the `insertAfterLine` branch,
  around line 168).** The host runs `checkBlankRun` beside today's `planInsertion` check. A
  failed check gets today's open error ("The preview is stale. Refresh it before editing this
  block.") and nothing changes.
- **The page-facing original text stays `""` (fix 5).** As for every insertion today:
  - `previewEditSource` carries `originalText: ""` (around line 186);
  - the page's saves carry `originalText: ""`;
  - the stale comparison `message.originalText !== edit.originalText` (around line 478) keeps
    comparing `""`.

  The run's region is held in a separate host-only field of `ActiveBlockEdit`, for example
  `blankRunRegion: { line, endLine, text }`. It is never sent to the page, and it is used only
  to restore the run.
- **Save without a held edit (fix 5).** `handleEditSave` re-creates the edit when none is held
  (the `!edit && message.insertAfterLine !== undefined` path, around lines 408-430). There it runs
  `checkBlankRun` on `message.replaceBlankRun` against the current document before it builds the
  plan and the host-only region. A failed check gets that path's stale reason ("The preview is
  stale. Reopen the block before saving."). A save or cancel whose `replaceBlankRun` differs from
  the held edit's is refused with the held-edit stale reason, as a different `insertAfterLine`
  is today.
- **What is written.**
  - **A non-empty text** replaces the region. Exactly one separator goes before it: none at the
    start of a file without frontmatter. Exactly one separator goes after it: none at the end of
    the body, where the document's final line break is kept, or kept absent. The extra blank
    lines are gone once the block is written. Leading blank lines of the typed text are dropped
    (`insertionText`, BLOCK-094 as CR-439 changes it).
  - **An empty or whitespace-only text, or Cancel or Escape after an autosave (BLOCK-053),**
    writes the held region's `text` back in place of what the autosaves wrote. Either way the run
    is unchanged.
  - **Done with an empty text before any autosave** makes no edit at all, and the editor closes
    (BLOCK-263).
  - The document's line endings are kept (BLOCK-234, BLOCK-094).
- **Where the plan goes.** In `src/core/mapping/insertion.ts`, an `InsertionPlan` with an
  optional replaced range (for example `replace?: { start: number; end: number }`), built by a new
  `planBlankRunInsertion(text, line, endLine)`. It is used by `blockEdits.ts` the way
  `planInsertion` is today. BLOCK-256 is unchanged: no block-edit range starts on a blank line,
  because this is an insertion.

**Removing it.** The trigger is Delete or Backspace on a selected blank-lines block, or its
Delete block button.

- **The message.** The page posts a new message `previewBlankRunDelete { line, endLine }`.
  Register it in the message registry (`src/core/protocol/pageToHost.ts`,
  `pageToHostMessages.ts`) with gate `render` (`src/session/pageMessages.ts`). Its handler goes
  beside CR-439's `handleBlocksDelete` in `src/session/features/sourceEdits.ts`.
- **The check.** The host re-checks the run with `checkBlankRun`. It refuses a stale one with the
  existing out-of-date reason ("The preview is out of date. Refresh it and try again.").
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
absence: the blank-lines removal, the blank-lines insertion and the paste in place of a run
(BLOCK-234, BLOCK-094, BLOCK-169). The unit tests run each new plan on LF, CR LF and lone-CR
texts.

### 4. Requirements

Follow the project's requirements guidelines: IDs come from `okfreq new` and are never
hand-allocated; markers move with the code; run `just requirements-update`; add a dated entry in
`requirements/tiers/log.md`. All of these are in scope `block-editing`:

- New SwRS: **edit mode shows each blank run between top-level blocks as a blank-lines block**.
  - Where a run shows and where it does not: inside a fence, a single separator, a folded
    section, reading mode, the export.
  - Its out of scope: runs inside a list or a container show nothing (Q11).
  - Only the host's run list is read (fix 6).
- New SwRS: **a blank-lines block takes the arrows, Enter and a click**. It covers:
  - Up/Down stops and the insertion editor;
  - Delete and Backspace on a selected block only (Q10);
  - the block selection, Shift+click, Alt+Up/Down, Escape and clipboard rules (Q6, Q12).
- New SwRS: **typing or pasting in a blank-lines block writes the block in place of the run**.
  It covers:
  - one separator on each side;
  - an empty Done writing nothing, and Cancel restoring the run;
  - the editor kept across an autosave's re-render;
  - a stale run refused, on open and on a re-created save.
- New SwRS: **removing a blank-lines block keeps one separator**. It covers the middle, after
  the frontmatter, the start, the end, line endings, one undo step, the stale refusal shown next
  to the block, and the selection afterwards.
- Update with a scenario row:
  - **SwRS-MDOKFSTUDIO-BLOCK-004** (Up/Down stop on a blank-lines block);
  - the Delete block SwRS added by CR-439 (its Delete, Backspace and button also remove a
    selected blank-lines block).
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

- Everything CR-439 delivers: Done on an empty block, the insertion fix, and the Delete block
  button and keys on blocks.
- Runs between the items of a list, or inside a quote, an admonition, a list item or another
  container (blank-runs-Q11): `1-inbox/blank-runs-inside-lists`.
- Moving the existing `isBlank` callers to the CommonMark test (blank-runs-Q9): backlog
  `blank-line-check-unicode-spaces`.
- Collapsing blank runs by itself: on save, on render, or on any edit other than the writer's own
  removal of, typing in or paste on a run. The file's format is kept.
- Blank lines inside a block (code fence, directive, list-table, HTML block): they are the
  block's content and are edited with it (BLOCK-256 unchanged).
- Blank runs in an included file, in the frontmatter or in a cell of the properties table.
- Moving a blank-lines block, or dragging blocks across it.
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
  - `isCommonMarkBlank` on `""`, spaces, tabs, U+00A0 and U+3000;
  - `checkBlankRun` refuses a run with a non-blank line inside it, with one more blank line next
    to it, or with a U+00A0 line;
  - `planBlankRunRemoval` in the middle, after the frontmatter, at the top of a file without
    frontmatter, at the end with and without a final line break, and in a text of only blank
    lines, with no bare LF added in CR LF and no CR added in LF;
  - `planBlankRunPaste` writes one separator on each side.
  - The existing `checkSpan` / `planCut` tests are unchanged, which shows the old callers keep
    `trim()`.
- `insertion.test.ts`: `planBlankRunInsertion` writes one separator on each side, none before at
  the top of a file without frontmatter, and none after at the end. LF, CR LF and CR.

**Render and export:**

- `renderPreviewSource` output ends with the `data-okf-blank-runs` element, with the right pairs,
  and with an empty value for a text with no run.
- A content patch updates it.
- `exportContent` removes it and a page-made `data-okf-blank-lines` element.

**Session, `test/session/`:**

- A blank-lines insertion:
  - `previewEditSource` carries `originalText: ""`, and nothing of the region;
  - a save with text writes one separator on each side;
  - an autosave then Cancel restores the run byte for byte;
  - an empty Done writes nothing and gets `done: true` (BLOCK-263);
  - a stale run is refused on open;
  - with no held edit, the re-created edit's save re-checks `replaceBlankRun` and refuses a run
    that is no longer blank (lines 408-430 path).
- `previewBlankRunDelete`: one `applyWrittenEdits` call, `previewBlocksResult` with
  `op: "delete-blank-lines"`, and the refusal path.
- `previewBlocksPaste` with `replaceBlankRun`: one edit in place of the run, and a stale-run
  refusal.
- The validators reject `replaceBlankRun` without `insertAfterLine`, on another message type, or
  with `line >= endLine`.

**Page, `test/page/`.** These run with the runtime bundle, as `runtimeBlockSelection.test.ts` and
`runtimeBlockMoves.test.ts` do, with one check per rule.

Placement:

- Edit mode places one blank-lines block for a run between blocks.
- It places none for a run inside a code fence, between two items of a list, or for a single
  separator.
- It places one after a list that ends on its separator, and one before "Start writing" in an
  empty body.
- Leaving edit mode removes them.
- A run after a folded block shows nothing. A run right after the heading of a folded section
  shows nothing; unfolding shows it.
- **Authored attribute (fix 6):** content holding an authored `<div data-okf-blank-runs="1-9">`
  among the blocks makes no blank-lines block, while the host's last-child element still does.

Selection and keys:

- Up/Down stops on it.
- Enter and a click open the insertion editor and post `previewEditOpen` with `replaceBlankRun`.
- Delete and Backspace on a selected block post `previewBlankRunDelete`. On a block only focused
  with Tab they post nothing. Its Delete block button posts it.
- Shift+Up/Down never starts or ends a block selection on it.
- Shift+click on it leaves the selection unchanged.
- Alt+Up/Down with it selected posts nothing.
- Escape clears its selection.
- Ctrl/Cmd+C and +X post nothing with only it selected.
- Ctrl/Cmd+V with it selected posts `previewBlocksPaste` with `replaceBlankRun`.

Editor kept and results:

- **The editor is kept (fix 7).** Open the editor from a blank-lines block, type, and let the
  autosave post. Apply a content patch whose run list no longer has that run. The editor is still
  open in the same element, and Cancel posts `previewEditCancel` with the same `replaceBlankRun`.
  The host side of that path restores the run (session check above).
- A `previewBlocksResult` refusal for `op: "delete-blank-lines"` shows next to the blank-lines
  block.
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
3. Write three blank lines again, click the blank-lines block, type a word, wait past the
   autosave and press Cancel: the file is back to its three blank lines.
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

1. **Runs are found by the host and placed by the page**, through one element the host appends
   at the end of the rendered content. The page reads only that element (fix 6). The page has no
   source text, and carrying the runs in the content keeps them in step with the blocks across a
   content patch.
2. **One helper checks a run** (`checkBlankRun`) for open, save, paste and removal. These are the
   "run checks" of Q9.
3. **A run is hidden when the block after it is folded too**, not only the block before it
   (Q5). A run right after a folded section's heading is inside that section.
4. **A run in an empty body shows before "Start writing"**, so no top-level run is ever out of
   reach.
5. **The label is drawn by CSS from an attribute**, so the find bar and copy never see the text
   "blank lines".
6. **The Delete block button sits at the left edge of the blank-lines block**, from
   `createDeleteBlockButton`, shown on hover, focus or selection. Q1 says "a gauche", and the
   blank-lines block has no bar of its own.
7. **Shift+arrow from a selected blank-lines block starts the block selection on the neighbour**
   in that direction (Q6: never on the blank-lines block itself).
8. **The blank-lines block hosting an open editor stays in place** until the editor closes, even
   when an autosave's re-render no longer has its run (fix 7).
9. **Removal returns the selection to the following block** (or the block above, or "Start
   writing") with the cut's viewport pin, as Delete block does in CR-439.
10. **The new SwRS derive from StRS BLOCK-011 and BLOCK-025.** No new StRS.
11. **Spec critic**: yes, on Fable (blank-runs-Q8, owner's rule). The Chief of Staff runs it.

### Second run: the critic's results

- **Answers carried.**
  - Q9: a new CommonMark test, with the old callers unchanged. This replaces the first run's
    change of the shared `isBlank`.
  - Q10: Delete and Backspace act on a selected block only. A focused one takes Enter and its
    button. This replaces the first run's decision 7.
  - Q11: runs inside lists and containers are out of scope, filed as
    `1-inbox/blank-runs-inside-lists`.
  - Q12: Ctrl/Cmd+V pastes in place of the run. This replaces the first run's "after the block
    above".
- **Fixes applied.**
  - 5: the page-facing `originalText` stays `""`, the host holds the region in a separate field,
    and the re-created save re-checks the run.
  - 6: the page reads only the host's last-child element and builds the blocks itself, with a
    check on an authored attribute.
  - 7: the editor's block survives a refresh, with a page check.
  - 8: one page check per rule.
  - 9: CR-439 and its branch are named here and in `01-intent.md`.
