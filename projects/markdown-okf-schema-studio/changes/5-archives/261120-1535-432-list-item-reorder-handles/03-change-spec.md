# Change Specification: CR-432 list-reorder, reorder handles on list items in edit mode

No tracker issue (verbal request, owner, 2026-11-20).

## Goal

In edit mode, the writer reorders the items of a list exactly the way they reorder the body rows
of a table. Each item has a handle on its left. Dragging the handle to a place among the item's
sibling items moves the item there, and so does Alt+Up or Alt+Down on the focused handle. The item
moves with everything inside it (its sub-items and blocks), and the document gets one edit, so one
undo reverts it. An ordered list keeps its numbers in order. This holds for every list, including
the lists inside GitHub alerts and MyST admonitions. Owner's words: "il faut mettre des ancre de
reordonnement de la liste sur la gauche comme les ligne d une table", then "je veux le meme
comportement pour les listes et les poignee" and "alors on met partout, tu peux decaler les poignee
en dehors de l admonition ou des n niveaux d admonition".

## Base

This CR builds on CR-424 (external PR 404, item-level list editing: a click on a list item edits
that item only). CR-424's commit must be in this CR's base; it is not merged at the time of
writing. CR-424's branch is `chantier/batch-06/cr-424-take-ownership-of-external-pr-404-list-i`,
in the worktree `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-424`.
The names below (`sourceRangeForList`, `spanOf`, the item editor) are those at CR-424's head. If
CR-424's later rounds rename them, use its final names.

## Decisions carried from `02-answers.md`

First series:

1. List items get reorder handles on the left, like table rows. Cmd/Ctrl+Alt+Up/Down in a list
   item editor keeps moving the whole list (CR-424's behaviour). This CR does not change it.
2. Nesting: an item moves with its sub-items and blocks, and only among its siblings in the same
   list. It never moves into another list, and never up or down a level.
3. Where: every list in edit mode: bullet, ordered and task lists, at every level. An ordered list
   keeps its numbers in order after a move.
4. Depends on CR-424 being in the base (section "Base").

Second series (these replace the first series' "menu" and "hover" answers):

5. Style: the list item handles behave exactly like the table row handles. They show at all times
   in edit mode, they drag the same way, and there is no menu. The table handles do not change.
6. Keyboard: Alt+Up/Down on a focused list item handle moves the item, as on a table row handle
   (SwRS-MDOKFSTUDIO-TABLE-002).
7. Lists inside a GitHub alert or a MyST admonition, at any nesting depth, get handles too. Their
   handles may sit outside the container's box, shifted left past the n nested container levels.

## The model: the table row handles

The pattern to follow is `src/page/features/tableRowMove.ts` (SwRS-MDOKFSTUDIO-TABLE-002). The
list feature copies its behaviour and its shape, not its code:

- **The handle.** A `<button>` with the class `okf-list-editor-handle`: the six-dot mark of the
  frontmatter list editor, styled in `src/core/preview/styles/frontmatterEditorStyles.ts`. It
  carries `contenteditable="false"`, `draggable="true"`, an `aria-label` and a `title`. It shows at
  all times in edit mode.
- **The layer.** The handles live in a layer of their own appended to `document.body`
  (`data-okf-row-handle-layer` for tables). They are placed from the rectangles of what they move.
  - They are placed again in the next animation frame on render, on resize (a `ResizeObserver` on
    `#sphinx-myst-preview-content`, and the `window` resize), and on width-mode changes
    (`reposition`, called from `src/page/runtime.ts` next to `rt.tableRowMove?.reposition()`).
  - Every box is read before any handle is written (issue 420), and the placement waits for the
    next frame (issue 423).
  - A block that leaves less than a handle's room on its left is pushed right (`data-okf-row-shift`,
    `margin-inline-start: 2.2em`).
- **The keyboard.** Alt+Up and Alt+Down on the focused handle move the row
  (`rt.blockMoves.moveChordDirection(event, false)`). `preventDefault` and `stopPropagation` keep
  the chord from also moving the whole block. A repeat is ignored while a move is pending.
- **The move.** The page asks the host for the source with `previewEditOpen`, moves the row on the
  source text in the page, and saves the whole range in one `previewEditSave` (`final: true`, with
  `rt.scroll.anchorField()`). It then posts the edit closed (`rt.blockEditor.postEditClosed`).
  - The source has 5 s to arrive. A settle timer holds further moves until the render arrives.
  - A move is refused while the page is busy.
  - After the render, the focus goes back to the moved row's handle.
- **The drag.** The dragged row is dimmed, and a drop line shows before or after the row under the
  pointer. The drop zone also covers the handle strip, and the marker follows the nearest gap. A
  drop that would leave the row in place requests nothing.
- **The wiring:**
  - `src/page/features/blockSourceEditor.ts` hands each `previewEditSource` to
    `rt.tableRowMove.receiveSource(message)` first (line 47).
  - `src/page/features/pageInput.ts` skips the click-to-edit for a click on a handle (line 262).
  - `src/page/features/editMode.ts` `applyEditMode` calls `rt.tableRowMove.refresh()` (line 77),
    so the handles are rebuilt on every edit-mode switch and render.
- **Containers.** A table inside a quote or an admonition is moved on its own lines, and every line
  keeps its container prefix (`containedTable` in `src/page/modules/tableInContainer.ts`,
  SwRS-MDOKFSTUDIO-TABLE-121).

## What changes

### A. A pure module that moves an item on the list source

Add a new file `src/page/modules/listItemMove.ts`. Like `src/page/modules/listTableMove.ts`, it
works on text only, with no DOM. It exports one function:

```ts
/**
 * Moves the item at index `from` of the list `source` (the text of one whole list, the lines the
 * page opened, container prefix included) to index `to`, or undefined when the source cannot be
 * read as `itemCount` items.
 */
export function moveListItem(source: string, itemCount: number, from: number, to: number): string | undefined;
```

Rules:

1. **Line endings.** Split the lines with their line endings kept, as `readListTable` does. Keep
   the source's line endings as they are.
2. **Container prefix (Decision 7).**
   - Every line of a list inside a quote or a GitHub alert carries the same quote prefix (`> `,
     `> > `, with up to three spaces before each `>`, as `QUOTE_PREFIX` of `tableInContainer.ts`
     reads it). A blank quote line (`>` or `> >` alone) counts as carrying that prefix.
   - Strip the prefix before rules 3 to 10, then write it back on every line, byte for byte as it
     was.
   - Refuse a source whose lines carry different prefixes (`undefined`).
   - A list inside a MyST admonition has no prefix. Its lines may be indented, which rule 3 reads.
   - Share the prefix reader with `tableInContainer.ts`: export it from there, or move it to a
     small module both files import. Do not copy it.
3. **Items.** The list's items are the lines that start with a list marker at the indentation of
   the first non-blank line.
   - A marker is a bullet (`-`, `*`, `+`) or an ordered marker (digits followed by `.` or `)`). It
     is followed by a space, a tab or the end of the line.
   - An item runs from its marker line to the line before the next marker line at the same
     indentation, or to the end of the source.
4. **Gaps.** The blank lines between two items belong to the list, not to the item (the "gaps", as
   in `ListTableSource.gaps`).
   - An item moves without its trailing blank lines, and every gap stays where it is. So a loose
     list stays loose and a tight list stays tight.
   - A blank line inside an item belongs to the item when a line of the same item follows it (an
     indented continuation, a nested list, a fenced block).
5. **Refusals.** Refuse the move (`undefined`) when the source holds anything other than items at
   that indentation: a non-blank line with less indentation, or text before the first item.
6. **Count check.** Refuse the move when the number of items found differs from `itemCount` (the
   number of `li` children of the rendered list): the page and the source disagree.
7. **Indexes.** Return `undefined` when `from` or `to` is outside `0..itemCount-1`, or when
   `from === to`.
8. **Ordered lists.**
   - After the move, number the items in order from the number of the first item of the source
     (`3.` `4.` `5.` stays `3.` `4.` `5.`). Each item keeps its own delimiter (`.` or `)`).
   - A list whose items all carry the same number (`1.` `1.` `1.`, which CommonMark renders in
     order) keeps that number on every item.
9. **Content column.**
   - When a renumbered marker gets longer (`9.` to `10.`), indent the item's continuation lines
     (every non-blank line of the item after its marker line) by the difference. Its paragraphs,
     sub-lists and blocks then stay inside the item.
   - When a marker gets shorter and the item was written with one space after its marker, widen
     that space by the difference, so the content column does not move. Leave the continuation
     lines as written.
10. **Task items.** Task items (`- [ ] text`, `- [x] text`) are bullet items. Their checkbox text
    moves with them, unchanged.

### B. The page feature: handles, drag, keys, move

Add a new file `src/page/features/listItemMove.ts` with `installListItemMove(rt: PageRuntime):
ListItemMove`.

- Add a `ListItemMove` interface in `src/page/features/pageRuntime.ts`, next to `TableRowMove`:
  `refresh(): void`, `reposition(): void`,
  `receiveSource(message: PreviewEditSourceMessage): boolean`.
- Add a `listItemMove: ListItemMove` member to the runtime, and install it in `src/page/runtime.ts`
  after `installTableRowMove`.

Wire it the way the table feature is wired:

- `editMode.ts` `applyEditMode`: call `rt.listItemMove.refresh()` after
  `rt.tableRowMove.refresh()`.
- `runtime.ts`: call `rt.listItemMove?.reposition()` next to `rt.tableRowMove?.reposition()`.
- `blockSourceEditor.ts`: add `if (rt.listItemMove.receiveSource(message)) return;` next to the
  table line.
- `pageInput.ts`: make the click skip also cover `[data-okf-list-item-handle]`.

Mark the module and the feature with `@implements_req` for the new SwRS (section D).

**Which items get a handle (Decisions 3 and 7).** In edit mode, every `li` child of a `ul` or `ol`
in `#sphinx-myst-preview-content` whose list has a source range gets a handle:

- bullet, ordered and task lists, at every level;
- lists inside a GitHub alert, a quote or a MyST admonition, at any nesting depth.

These get none:

- a list with a single item (nothing to reorder, like a table with one body row);
- the items of an included file (`rt.blocks.isIncludedBlock` on the list's top-level block);
- the properties table (`[data-okf-properties]`).

What a click on an item edits does not change: CR-424's rule still applies, so a click on an item
inside an alert or an admonition edits the whole container. The handle only moves the item.

**The handle (Decision 5).**

- A `<button type="button">` with the classes `okf-list-editor-handle okf-list-item-handle`.
- Attributes:
  - `data-okf-list-item-handle="true"`, `contenteditable="false"`, `draggable="true"`;
  - `aria-label="Move list item"`;
  - `title="Drag to move item (Alt+Up, Alt+Down)"`, the wording of the table row handle;
  - `data-okf-list-item-line`, holding the item's `data-sphinx-source-line`.
- It shows at all times in edit mode, like the table row handle. There is no hover rule and no
  menu.
- Every handle lives in one layer, `<div data-okf-list-handle-layer="true">`, appended to
  `document.body`. `refresh()` rebuilds the layer, with no handles when edit mode is off. A
  `position()` pass places the handles in the next frame, as in `tableRowMove.ts`.

**Placement.**

- **Vertically**, the handle is centred on the item's first line, not on the whole item, so an
  item with sub-items keeps its handle beside its marker. Read the first line from a `Range` over
  the item's first text, or from the item's top plus half its computed line height.
- **Horizontally**, the handle's right edge sits 4 px left of the left edge of the item's own list
  box (the `ul` or `ol` that holds the item). The handles of sibling items then line up in one
  column, left of their markers.
- **In containers (Decision 7)**, when the list sits inside one or more GitHub alerts, quotes or
  MyST admonitions, the right edge sits 4 px left of the outermost container's left edge. The
  handle is then outside the box of every container level, n levels included.
  - The handles of nested lists inside the same container share that column. They differ only by
    their height.
- **Push right.** As for tables, a top-level block (the list, or the outermost container) that
  leaves less than a handle's room on its left is pushed right with
  `data-okf-list-shift="true"`. The stylesheet reads it with the same rule as
  `table[data-okf-row-shift]`: `margin-inline-start: 2.2em`, and a width reduced to match. The
  handle then never leaves the pane.
  - The shift is removed when edit mode goes off, or when the block has room again.
- **Hidden items.** A hidden item (height 0, for example while its list or container is edited as
  raw Markdown) hides its handle.
- **Edit outline.** While the pointer is over a handle, `rt.editMode.setEditHover(item)` puts
  CR-424's edit outline on the item the handle moves.

**Drag (the table pattern, siblings only, Decision 2).**

- **Start.** `dragstart` on a handle is refused when the page is busy (below). Otherwise it:
  - marks the item `data-okf-list-item-dragging="true"` (dimmed, opacity 0.45, as
    `tr[data-okf-row-dragging]`);
  - sets `text/plain` to `list-item`, the drag image to the item, and `effectAllowed = "move"`.
- **Drop zone.** It covers the dragged item's list (its siblings and anything inside them), plus
  the handle strip at their height. In a container, that strip runs from the handle column to the
  list.
- **Drop target.** The target is the sibling whose vertical extent holds the pointer.
  - On its upper half the drop line shows above it (`data-okf-list-item-drop="before"`); on its
    lower half it shows below it (`"after"`).
  - The line is an inset line in `var(--studio-focusBorder, Highlight)`, like the table drop line.
  - Over a nested item of a sibling, the target is that sibling (the ancestor at the dragged item's
    level).
- **No drop.** Outside the zone, and over another list, no line shows and a drop requests nothing.
  A drop that would leave the item in place requests nothing.
- **Index.** Compute the index after the drop as `commitDrop` of `tableRowMove.ts` does.

**Keys (Decision 6).**

- A `keydown` on the handle reads `rt.blockMoves.moveChordDirection(event, false)`. Alt+Up moves
  the item from `index` to `index - 1`, and Alt+Down to `index + 1`.
- `preventDefault` and `stopPropagation` keep the chord from also moving the block.
- Alt+Up on the first item, and Alt+Down on the last, do nothing.
- A repeat while a move is pending, or until its render arrives, is ignored.
- The index is read from the item at the time of the key: the item may have been replaced by a
  render since the handle was made.
- A click on the handle opens no editor.

**Move.** It works like `requestMove` and `receiveSource` of `tableRowMove.ts`:

1. **The range.** The range is the item's own list, given by CR-424's `sourceRangeForList` in
   `mappedBlocks.ts`, exposed through `MappedBlocks` (for example `listRange(list: Element)`).
   - It is the range of the list itself, not of the container, even inside an alert or an
     admonition (Decision 7). Only the list's lines are opened and saved; the container's other
     lines are not touched.
   - Inside a quote or an alert, the opened lines carry the quote prefix, which rule A.2 strips
     and writes back.
   - A range that is not two safe integers with `line <= endLine` refuses the move.
2. **The request.** Post `previewEditOpen` for that range with a new `editId`
   (`context.requestId + "-" + (++state.editSequence)`). Keep the pending move (editId, line,
   endLine, the item count, from, to) and arm the 5 s timeout, which posts the edit closed.
3. **The answer.** On a `previewEditSource` with that `editId`:
   - On an error or no `originalText`, post the edit closed.
   - Otherwise call `moveListItem(originalText, itemCount, from, to)`. When it returns `undefined`
     or an unchanged text, post the edit closed.
   - Otherwise post one `previewEditSave` (`final: true`, the opened range, `originalText`,
     `editedText`, `rt.scroll.anchorField()`), then post the edit closed. Remember to focus the
     moved item's handle after the render (by the list's first line and the new index), and arm
     the settle timer.
4. **Busy.** No move happens (the drag is cancelled, the key does nothing) in these cases:
   - edit mode is off;
   - a frontmatter editor or any block editor is open, CR-424's item editor included;
   - a move waits for its source;
   - the render of the last move has not arrived yet.

The page sends nothing new to the host. `previewEditOpen` and `previewEditSave` are existing
messages, and the host's checks on them apply unchanged. Nothing changes in `src/session/` or in
`src/core/protocol/`.

**Precondition to check first.** The move relies on the `li` elements, and the mapped blocks
inside them, carrying their `data-sphinx-source-line` inside a GitHub alert, a quote and a MyST
admonition, so that `sourceRangeForList` gives the list's own lines there.

- Make that the first runtime test, rendered with the real renderer.
- If it does not hold for one of these containers, stop and report it to the Foreman as a blocker
  with the rendered markup. Do not invent a range.

### C. Styles

Add a `LIST_ITEM_HANDLES_CSS` block to `src/core/preview/styles/editModeStyles.ts`, next to
`TABLE_HANDLES_CSS`, scoped to `html[data-sphinx-preview-edit-mode="on"]`. It holds these rules:

- the list handle layer;
- the handle's placement transform (`translate(-100%, -50%)`, and the dot lift of
  `.okf-table-row-handle::before`);
- the push (`[data-okf-list-shift="true"]`);
- the dragged item;
- the drop lines.

If the file would then pass 800 lines, put the block in a new styles file in the same folder,
joined where `TABLE_HANDLES_CSS` is joined. The light, dark and cream themes read the existing
theme variables. Add no colour literal beyond the existing fallbacks.

### D. Requirements

First read `requirements/guidelines/requirements.guidelines.md` and
`requirements/guidelines/project.guidelines.md` ("During a change").

1. **StRS-MDOKFSTUDIO-BLOCK-014** ("A writer reorders blocks with arrows, keys and selections").
   It is `req_lifecycle: proposed`, so it can change without re-approval.
   - Add the list items to its intent and its constraints: an item of any list, inside alerts and
     admonitions too, moves among its sibling items by a handle on its left, shown in edit mode,
     by a drag or Alt+Up/Down, with its sub-items and blocks, as one edit. An ordered list keeps
     its numbers in order.
   - Add a main path "Move a list item" that cites the new SwRS.
   - Do not touch the approved StRS-MDOKFSTUDIO-BLOCK-003 or BLOCK-025.
2. **A new SwRS** in the `block-editing` scope, created with `okfreq new` (never a hand-allocated
   ID).
   - It derives from StRS-MDOKFSTUDIO-BLOCK-014. Title: "List item handle reorders an item among
     its siblings in edit mode".
   - Its scenarios mirror SwRS-MDOKFSTUDIO-TABLE-002:
     - drag: before and after, the marker in the handle strip, a drop in place;
     - keyboard: Alt+Up and Alt+Down, the ends, a repeat before the render, the focus back on the
       handle;
     - the handle beside its item, shown at all times in edit mode;
     - the push of a block with no room on its left;
     - nesting: the item moves with its children, only among its siblings, with no drop into
       another list;
     - containers: a list in a quote, a GitHub alert, a MyST admonition and two nested admonitions.
       The handles sit outside the outermost box, only the list's lines are saved, the quote
       prefix is kept, and a click on the item still edits the whole container;
     - ordered numbering and the content column (rules A.8 and A.9), and task items;
     - one edit and one undo;
     - refusals: the busy states, a single item, an included file, the properties table, a source
       that does not read as the rendered items or carries mixed prefixes, and a refused source.
   - Write no Known issue for containers: they are covered.
   - Put `@implements_req` on the module and on the feature, and `@tests_req` on every test of the
     evidence.
   - Name CR-424's item SwRS (BLOCK-014 at CR-424's head) under "Related requirements", or in
     `depends_on` when it is a shared rule.
3. **SwRS-MDOKFSTUDIO-BLOCK-130** (the move chord in a block editor's text box): check that it
   says what Decision 1 keeps (in a list item editor, the chord moves the whole list). CR-424 is
   the CR that writes that row, so only read it here, and report any mismatch.
4. **Update and log.** Run `just requirements-update`, then `just check-markers` and
   `just requirements-lint` (0 changes, main paths valid). Add a dated entry in
   `requirements/tiers/log.md`, under its date heading, in a `### List item handles` sub-heading,
   with the commands run and their results.

### E. Docs, glossary, changelog

- **`docs/user/editing.md`.** Add a short paragraph next to CR-424's item-editing paragraph:
  - in edit mode, each list item has a handle on its left, as table rows do;
  - drag it among its sibling items, or focus it and press Alt+Up or Alt+Down;
  - the item moves with its sub-items, and an ordered list keeps its numbers;
  - inside an alert or an admonition, the handles sit left of the box.
- **`.agents/glossary/common.md`.** Add a "List item handle" entry, in alphabetical order.
- **`CHANGELOG.md`.** Add one line under `## Unreleased`.
- **The writing skill** (`skills/writing-for-markdown-okf-schema-studio/`) needs no change: no
  rendered syntax changes (`writing-skill-maintenance.guideline.md`).

## Design choices of this spec

The answers do not fix these points. This spec takes them from the table model. The Chief of Staff
may take any of them to the owner:

- **Placement.** The handle sits left of the item's own list box, centred on the item's first line
  rather than on the whole item. A block with no room on its left is pushed right, as a table is.
- **Containers.** Inside containers, every handle goes to one column left of the outermost
  container, whatever the list's depth inside it.
- **The edited range.** A move opens and saves the range of the item's own list (one edit), not
  the range of the outermost list or of the container.
- **Numbering.** Renumbering starts at the first item's number. A list whose items all carry the
  same number keeps it.
- **Open editors.** No move happens while any block editor is open. A table allows a move while one
  of its own cells is being edited, but a list item editor has no item model to move.

## Out of scope

- The whole-list move chord in a list item editor (Decision 1: unchanged).
- What a click on an item inside an alert or an admonition edits (CR-424's rule: the whole
  container).
- Moving an item into another list, or changing its level (indent or outdent).
- Lists inside a `{list-table}` cell, when the `{list-table}` renders them inside a table cell: they
  get handles like any list, but the table keeps its own row and column handles unchanged.
- Any change to the table handles.
- Any host or protocol change.

## Evidence

All the evidence comes from the CR's worktree, at the head under test. The check that guards a
shipped file (the stylesheet block of section C) reads the shipped stylesheet, as
`previewStyles.test.ts` already does, not a copy.

### Unit and contract (`just check`, on Windows locally and on Linux in CI)

- **`test/page/modules/listItemMove.test.ts` (new):**
  - markers: `-`, `*` and `+` bullets, ordered items with `.` and `)`, and task items;
  - moves: first to last, last to first, a swap in the middle;
  - an item with a nested list, a fenced code block and a blank line inside moves whole;
  - tight and loose lists keep their gaps in place;
  - numbering: an ordered list starting at 3 renumbers 3, 4, 5, and an all-`1.` list stays all
    `1.`;
  - content column: `9.` to `10.` indents the moved item's continuation lines by one, and a nested
    list stays nested (the renderer, parsing the result, gives the same nesting);
  - a list in `> ` and in `> > ` keeps its prefix on every line, blank quote lines included;
  - CRLF line endings are kept;
  - refusals: a count mismatch, text before the first item, a line with less indentation, mixed
    prefixes, `from === to`, an index out of range.
- **`test/page/runtimeListItemMove.test.ts` (new)**, on `test/page/runtimeHarness.ts` like
  `runtimeTableRowMove.test.ts`:
  - First, the precondition: with the real renderer, the items of a list in a quote, a GitHub
    alert, a MyST admonition and two nested admonitions carry their source lines, and the list
    range covers only the list's lines.
  - Which items get handles:
    - every item of a bullet, ordered, task and nested list in edit mode, shown without hover;
    - none in reading mode, none on a one-item list, none on an included list;
    - lists in containers get handles placed left of the outermost container's box.
  - Moves:
    - a drag posts one `previewEditOpen`, then one `previewEditSave` (final), and opens no editor;
    - in a GitHub alert, the save holds only the list's lines, with the `> ` prefix kept;
    - a drop in place, or outside the list, requests nothing;
    - a drop over a nested item of a sibling lands before or after that sibling;
    - Alt+Up and Alt+Down move the item, nothing happens at the ends, a repeat is ignored, and the
      chord is not read as a block move;
    - after the render, the moved item's handle has the focus.
  - Refusals: a block editor or a frontmatter editor is open, a move is waiting, the source is an
    error or cannot be read.
  - Other cases:
    - a click on the handle opens no editor;
    - a block with no room on its left is pushed right, and edit mode off removes the push;
    - placing the handles reads each box once per pass (issue 420), and in the next frame
      (issue 423).
- **`test/core/preview/previewStyles.test.ts`:** the shipped `LIST_ITEM_HANDLES_CSS` scopes every
  rule to edit mode, holds the push rule, and uses the theme variables.
- Each new behaviour test fails on CR-424's head (constitution, section 3).

### Visual (`just ci-visual`, heavy CI)

Add new scenarios in the `block-editing` group, in `test/visual/scenarioIds.ts` and
`scenarioDefinitions2.ts` (or the file the group uses).

- **Fixture:** `test/visual/fixtures/<next number>-list-item-handles.md`. It holds a bullet list,
  an ordered list starting at 3 with a nested list, a task list, a GitHub alert holding a list, and
  two nested MyST admonitions holding a list.
- **Themes and widths:** light, dark and cream, at 900 px, and at 360 px for the push.
- **What the captures show:**
  - the handles left of their markers, centred on each item's first line;
  - the handles of the container lists, outside the outermost box;
  - a pushed list in the narrow pane;
  - a real mouse drag held down (dimmed item, drop line), as `capture_table_move.py` does for rows.
- **Assertion:** each handle rectangle lies left of its list (or of its outermost container),
  inside the pane, and centred on the item's first line within 2 px.

### Real window (heavy CI)

Run it with `gh workflow run ci.yml --ref <branch> -f heavy=true`: Linux, and macOS for the Alt
chord. Add a new scenario next to `test/integration/tableMoves.ts`, registered in
`test/integration/realInput/run.ts`. It checks:

- a real drag of the second item of an ordered list after the third moves it and renumbers the
  list, and one undo (`Ctrl+Z` / `Cmd+Z` in the editor) restores the text;
- a drag of an item with a sub-list moves both;
- a drag of an item of a list inside a GitHub alert moves it and keeps the alert's other lines;
- a drag over another list leaves the document as it was;
- Alt+Down on a focused handle moves the item down, and the focus is back on its handle;
- Cmd/Ctrl+Alt+Down in an open item editor still moves the whole list (Decision 1).

### Before and after for the PR

Screenshots, in light and dark:

- a list in edit mode with its handles;
- a list in an admonition with its handles outside the box;
- the drag line;
- an ordered list before and after a move.

### Gates

Run `just check` and `just requirements-lint`, then `just preflight` (its static stage on
Windows), then the heavy CI dispatch above, since the change touches edit mode.
