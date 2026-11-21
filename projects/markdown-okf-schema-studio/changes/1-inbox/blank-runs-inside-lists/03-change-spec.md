# Show blank-line runs inside lists as blank-lines blocks

In edit mode, a run of two or more blank lines between two items of a list, or inside a list
item, shows as the same blank-lines block CR-444 shows between top-level blocks, placed inside the
list where the run is. The writer reaches it, types in it or removes it as with any blank-lines
block; removing it keeps one blank line, so the list stays one list and nothing else in the file
changes.

Origin: verbal (found by the spec critic of CR-444 empty-block-blank-lines-block, 2026-11-21;
owner's goal, 2026-11-20). No issue.

## Goal

The owner's goal (2026-11-20): blank lines beyond the one separator are always reachable in edit
mode. CR-444 (merged, PR #453) made the runs between top-level blocks reachable. A run that lies
inside a list's lines is still unreachable: the page skips every run that a top-level block holds,
so a writer cannot see or remove the extra blank lines between two items of a list or between two
paragraphs of a list item.

This CR shows those runs. It reuses everything CR-444 built and changes the host in no way except
the requirements and tests. CR-444's specification is
`4-batch/3-done/444-empty-block-blank-lines-block/03-change-spec.md` in the planning folder; this
file restates what a Driver needs from it.

Base: `main` of markdown-okf-schema-studio, at or after `5a84db8b` (version 1.11.0), which holds
CR-444. The references below are read from that commit.

Project rules: this change follows the project's constitution (`.agents/constitution.md`), its
`AGENTS.md` (requirements, completion gate `just preflight`) and the requirements guidelines named
there. This specification restates none of them.

## Words

- **Blank run**, **Blank-lines block**, **Separator**, **CommonMark blank line**: as in CR-444 and
  `.agents/glossary/common.md`. A blank run is found by `blankRuns` (`src/core/mapping/blankRuns.ts`)
  and tested line by line by `isCommonMarkBlank` (`src/core/mapping/blockRange.ts`).
- **Run inside a list**: a blank run that a top-level `ul` or `ol` holds strictly (the list's first
  line is before the run, its last line after it), in one of two places:
  - **between items**: the line after the run starts the next item of the same list (at any
    nesting depth);
  - **inside an item**: the line after the run is more content of the same item (a paragraph, a
    nested list, a fence...).
- **Holder** of a run: a mapped element of the active document whose range holds the run strictly:
  `line < run.line && run.endLine < endLine` (`rt.blocks.blockRange`).
- **Host item** of a run inside a list: the list item (`li`) the blank-lines block goes into (rule
  below).

## What CR-444 already gives, unchanged

- **The host lists every run.** `blankRuns(text)` returns every run after the frontmatter,
  wherever it is, runs inside lists and inside fences included. `renderPreviewSource`
  (`src/core/render/renderPipeline.ts`, `blankRunsMarker`) appends them as the last element of the
  content, `<div hidden data-okf-blank-runs="L-E ...">`. No change there.
- **The page reads only that element** (`readRuns` in `src/page/features/blankLines.ts`) and builds
  every blank-lines block itself (`create`). No change there; the authored-attribute guard of CR-444
  holds for runs inside lists too.
- **The host's write paths are position-free.** `checkBlankRun`, `planBlankRunRemoval`,
  `planBlankRunPaste` (`blockRange.ts`), `planBlankRunInsertion` (`src/core/mapping/insertion.ts`),
  `handleEditOpen` / `handleEditSave` (`src/session/features/blockEdits.ts`) and
  `handleBlankRunDelete` (`src/session/features/sourceEdits.ts`) check and write a run by its lines
  only. They need no change: a run inside a list passes the same checks, and its removal deletes
  lines `line + 1`..`endLine` and keeps line `line` byte for byte (br-Q3, br-Q4). The session tests
  of this CR prove it on list texts.
- **The block's look, label, keys and messages**: the dashed bar, the CSS label "Blank lines (N)",
  `role="button"`, `tabindex="0"`, the Delete block button at its left edge, Enter or a click opening
  the insertion editor (`open`), Delete and Backspace on a selected block (`deleteSelection`),
  `previewBlankRunDelete`, `previewEditOpen`/`Save`/`Cancel` and `previewBlocksPaste` with
  `replaceBlankRun`, the editor kept across an autosave's re-render (br-Q2).

## What changes

### 1. Scope (br-Q1)

- **In scope:** runs between two items of the same list, and runs inside a list item, at any
  nesting depth of lists, in a top-level list of the body.
- **Quotes and admonitions are split out**, because the same mechanism does not serve them:
  - Inside a quote, and inside a GitHub alert (`> [!NOTE]`, a quote), the empty lines of the block
    are `>` lines. They are not CommonMark blank lines, so `blankRuns` never lists them: the host
    needs a new run finder and new run checks.
  - A MyST admonition is a directive. CR-444 treats a directive's lines as the block's content, and
    telling an admonition apart from the other directives (code-block, list-table, tab-set, math,
    figure) is a new placement rule per directive kind.
  - A list held by a quote, an alert or an admonition goes with them: a run in it shows nothing in
    this CR.
  - The Chief of Staff files them as one inbox item, proposed slug
    `blank-runs-inside-quotes-admonitions` (the Driver does not file it).

### 2. Placement inside a list (br-Q2)

All in `refresh()` of `src/page/features/blankLines.ts`. Today it computes `inside` (a top-level
body block holds the run) and skips such a run. The new rule, for each run of the host's list:

1. **No holder** among the top-level body blocks: CR-444's top-level rule, unchanged (position
   after the insertion bar of the block above, folded neighbours, empty body, the list that ends on
   its blank separator, BLOCK-256).
2. **Held by a top-level block that is not a `ul` or `ol`**: nothing, as today (a fence, an HTML
   block, a directive, an admonition, a quote, a table, a list-table).
3. **Held by a top-level `ul` or `ol`**: collect every holder of the run among the mapped elements
   inside that list (`rt.blocks.mappedChildren`, recursively, or the mapped elements under it;
   same file and document, never an included block, `isIncludedBlock`). If any holder is not a
   `ul`, `ol` or `li` element, the run shows nothing: this keeps blank lines inside a fence, a
   directive, an HTML block or a table that sits in a list item out of reach, as they are the
   block's content.
4. **Folded:** a run whose top-level list carries `data-okf-folded` shows nothing (unfolding shows
   it again), as CR-444's folded rule does for its neighbours.
5. **Host item.** The deepest holder that is an `li`. When the deepest holder is a `ul` or `ol`
   (a run between items, when the renderer does not count the run in the item above), the host item
   is that list's last `li` child whose line is before `run.line`.
6. **Position.** The blank-lines block goes inside the host item, right after the item's last
   child element that starts before the run (its mapped line before `run.line`, or the last child
   when the item ends before the run). It is never a direct child of a `ul` or `ol`. So a run
   between items A and B shows at the end of item A, and a run between two paragraphs of an item
   shows between them, indented with the item's content (br-Q2: "shown inside the list where the
   run is").
7. **Refresh.** A kept run keeps its element (`existing` map, same line and end line), as for
   top-level runs. The open editor's block (`editing`) stays where it is across a refresh; when a
   content swap dropped it, `place` puts it back inside its host item with the same rule (the
   `aboveOf` fallback of today becomes the placement of rule 6 for a run inside a list).

`place(block, above)` gains a branch for a run inside a list (for example
`placeInItem(block, item, run)`), or the Driver splits the placement into a small helper of the same
file. `blankLines.ts` is 203 lines; it stays under the 800-line cap.

### 3. Keyboard and pointer (br-Q2)

The keys are CR-444's. Two places of `src/page/features/blockSelectionView.ts` change so that a
blank-lines block inside a list is reachable by the arrows like the others:

- **Up and Down: stops in order of their first line.** `neighbourStop` finds the next stop with
  `stop.line > endLine` of the current one, so Down from a selected list skips the blank-lines
  blocks inside it, while Up from the block after the list lands on them. The order becomes: Down
  goes to the first stop whose first line is after the current stop's first line; Up to the last
  stop whose first line is before it. The stops stay the top-level body blocks and all visible
  blank-lines blocks (`stops`). So: list selected, Down, the first blank-lines block inside it, Down,
  the next one inside it or the block after the list; Up walks back the same way. For top-level
  stops the order is unchanged (their ranges do not overlap). The block selection (BLOCK-004)
  without any blank-lines block keeps its index path.
- **Shift+Up/Down from a selected blank-lines block** starts the block selection on the nearest
  body block in that direction, skipping blank-lines blocks (today `next.blank` ends the key with
  nothing done; with two runs in one list, Shift+Down from the first would do nothing). For a block
  inside a list, Shift+Up starts it on the list, Shift+Down on the block after the list.
- **The selection after a removal (`requestDeleteBlankLines`).** Today `targetIndex` counts the body
  blocks that start before the run, which for a run inside a list selects the block after the list.
  For a run inside a list, the selection goes to the top-level list that held it; for a top-level run
  it is unchanged (the following block, else the one above, else "Start writing"). The viewport pin
  is unchanged.
- **Unchanged and to keep:** a click on a blank-lines block inside a list opens its insertion
  editor and never the list item editor (the click handler stops propagation); Shift+click does
  nothing; Delete and Backspace act only on a selected one; Alt+Up/Down on it moves nothing (the list
  item handles' Alt+Up/Down acts on a focused handle only); Escape clears it; Ctrl/Cmd+C and +X do
  nothing with it selected; Ctrl/Cmd+V pastes in place of its run; the structural navigation
  (BLOCK-254, Right into a list's items) never stops on it, because it is never mapped.

`blockSelectionView.ts` is 660 lines; it stays under 800.

### 4. Look

- Same element and CSS as CR-444 (`.sphinx-preview-blank-lines`, the named block of
  `src/core/preview/styles/editModeStyles.ts`). Inside an item it is as wide as the item's content
  box, not the content column.
- Its Delete block button stays at its left edge and must not overlap the list item handles
  (`installListItemMove`, `src/page/features/listItemMove.ts`, handles in their own layer left of
  the list). The visual captures check it.
- `editModeStyles.ts` is 792 lines, under the 800-line cap. If the change needs new CSS rules
  (for example a margin inside an `li`), the Driver moves the blank-lines block's named CSS block to
  a style module of its own, wired where `editModeStyles.ts` is, rather than raising the cap.

### 5. Typing, pasting and removing (br-Q2, br-Q3, br-Q4)

- **Typing or pasting** in a blank-lines block inside a list goes through CR-444's path unchanged:
  the typed or pasted block replaces the run's region with one separator on each side, in one text
  edit, line endings kept; an empty Done writes nothing; Cancel after an autosave restores the run
  byte for byte. The text is written as the writer typed it, with the indentation the writer gave
  it: the host adds none (see the open question).
- **Removing** it (Delete or Backspace on the selected block, or its Delete block button) removes
  lines `line + 1`..`endLine` in one text edit and one undo step. Line `line` stays as it is,
  spaces or tabs included. Between two items, the one blank line left keeps the list one loose list,
  as a single blank line between items does today (br-Q3). No other line of the list or the file
  changes (br-Q4).
- A stale run is refused as today, with today's messages.

### 6. Requirements

Follow the project's requirements guidelines: markers move with the code; run
`just requirements-update`; add a dated entry in `requirements/tiers/log.md`. All in scope
`block-editing`. Update the four SwRS of CR-444 (all `proposed`), with the reason in the log entry:
they said runs inside lists show nothing.

- **SwRS-MDOKFSTUDIO-BLOCK-266** (where a run shows): title and normative text cover a run between
  two items of a list or inside a list item, shown inside the item that holds it. The "Nothing is
  shown" scenario drops "or a list" and adds: a run inside a fence, directive, HTML block or table
  in a list item, and a run inside a quote, an alert, an admonition or a list they hold. Add a
  scenario "Runs inside a list are shown".
- **SwRS-MDOKFSTUDIO-BLOCK-267** (arrows, Enter, click): add a scenario: Down from a selected list
  stops on each blank-lines block inside it in line order, then the block after the list; Up walks
  back; Shift+Up/Down from one starts the block selection on the list or the block after it; a click
  on it opens its insertion editor, not the list item editor.
- **SwRS-MDOKFSTUDIO-BLOCK-268** (typing or pasting): add a scenario row for a run inside a list:
  the block replaces the run with one separator on each side, written as typed.
- **SwRS-MDOKFSTUDIO-BLOCK-269** (removal): add a scenario: removing a run between two items or
  inside an item keeps line `line` and leaves one list; the selection goes to the list that held it.
- No new StRS; `derives_from` stays StRS BLOCK-011 and BLOCK-025, whose text is unchanged.
- New tests carry `@tests_req` for the SwRS they check; the changed code in `blankLines.ts` and
  `blockSelectionView.ts` keeps or gains its `@implements_req` markers (at most 3 IDs per marker
  block).

### 7. Shared vocabulary and docs

- `.agents/glossary/common.md`: "Blank run" today says "between top-level blocks, at the start or at
  the end of the body". Add "between two items of a list or inside a list item". "Blank-lines block":
  add that inside a list it shows in the item that holds the run.
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes, the blank-lines block is edit-mode chrome.
- The release notes are written when the release is prepared, not in this PR.

## Out of scope

- Runs inside a quote, a GitHub alert or a MyST admonition, and in a list they hold: split to the
  inbox item `blank-runs-inside-quotes-admonitions` (section 1).
- Blank lines inside a fence, a directive, an HTML block or a table, including when it sits in a
  list item: they are the block's content (CR-444, BLOCK-256 unchanged).
- Any change to the host's run checks or plans, to `blankRuns`, or to the hidden run list.
- Collapsing runs by itself, on save, render or any other edit. Making a loose list tight. Any
  re-indentation of the list.
- How a list item move (handle drag or Alt+Up/Down on a handle) carries the blank lines of an item:
  unchanged.
- Runs in an included file, in the frontmatter or in a cell of the properties table.
- Moving a blank-lines block, or dragging blocks or list items onto it.

## Evidence

The checks read the shipped files at the head under test: the real render pipeline, the real page
bundle and the real stylesheet, never a prepared copy. Each new check fails on the code before the
change (constitution, section 3). CR-444's existing tests keep their intent: "a run inside a block
gets no blank-lines block" (a block that is not a list) still passes unchanged. A CR-444 assertion
that expected nothing for a run between list items is changed only for that reason, said in the
commit.

**Render, `test/core/render/`** (real renderer, so the placement inputs are real): for a list text
with a run between items, a run between two paragraphs of an item, a run inside a fence of an item
and a run in a list inside a MyST admonition, `renderPreviewSource` gives:

- the run list with all four runs;
- a top-level `ul` whose `data-line` / `data-end-line` hold the first two runs strictly;
- the fence's `pre` (or its mapped element) with a range that holds its run strictly;
- the admonition as the top-level holder of the fourth run.

**Page, `test/page/runtimeBlankLines.test.ts`** (runtime bundle, one check per rule; add a list
shape to the harness: a `ul` with mapped `li` children and mapped blocks inside them):

- a run between two items makes one blank-lines block, as the last child of the item above, never a
  direct child of the `ul`;
- a run between two paragraphs of an item makes one, between them inside that item;
- a run between two items of a nested list goes into the nested item above;
- a run inside a fence in an item, and a run inside a list held by an admonition, make none;
- a run inside a folded list makes none, and unfolding makes it;
- a content patch keeps the element of an unchanged run inside a list;
- an editor opened from one inside a list stays in its element across a patch without that run;
- Down from the selected list stops on each blank-lines block inside it in line order, then on the
  block after the list; Up walks back through them to the list;
- Shift+Up and Shift+Down from one start the block selection on the list and on the block after it;
- a click on one posts `previewEditOpen` with `replaceBlankRun` and opens no list item editor;
- Delete on a selected one posts `previewBlankRunDelete`; after the removal result and render, the
  list is selected.

**Session, `test/session/blankRunHost.test.ts`** (real handlers, no host change expected):

- `previewBlankRunDelete` on a run between two items of `- a` / `- b`, LF and CR LF: lines
  `line + 1`..`endLine` go, the first blank line stays byte for byte (with its spaces when it has
  some), one `applyWrittenEdits` call, the rest of the text is identical;
- the same for a run between two paragraphs of an item indented with two spaces;
- a save with text in place of a run between items writes the text as sent with one separator on
  each side; Cancel after an autosave restores the run byte for byte.

**Core, `test/core/mapping/blockRange.test.ts`**: `planBlankRunRemoval` on the two list texts above
leaves one list (re-rendering the result gives one top-level `ul`).

**Visual (`just ci-visual`)**: a new fixture (for example
`test/visual/fixtures/93-blank-lines-in-lists.md`) with a run between two items, a run inside an
item and a fence with blank lines in an item, and scenarios in
`test/visual/blankLinesBlockScenarios.ts` with checks in `test/visual/capture_blank_lines_block.py`:

- edit mode: exactly two blank-lines blocks, each inside the right `li`, as wide as the item's
  content, none in the fence;
- one selected with the arrows: its Delete block button is shown at its left edge and its box does
  not overlap any list item handle;
- reading mode: none.

The captures are attached to the PR as the pull-request guideline asks.

**Integration (real VS Code, `just ci-integration`, heavy run on the branch)**: in
`test/integration/blankLines.test.ts`, a second fixture, a list with three blank lines between two
items and three inside an item, in LF and CR LF:

1. Send `previewBlankRunDelete` for the run between items: one blank line is left, the list's other
   lines are unchanged, no bare LF in CR LF. One undo brings the run back.
2. Send `previewEditSave` with `replaceBlankRun` for the run inside the item and the text `  X`:
   the run is replaced by `  X` with one blank line on each side. One undo brings it back.

**Requirements:** `just requirements-lint` and `just requirements-update` pass; the updated SwRS
carry their markers at the code and tests above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Open questions

1. **Indentation of a block typed inside a list item.** br-Q2 says Enter or a click writes a block
   in the run's place, the same as CR-444; br-Q4 says only the removed blank lines change. This spec
   writes the typed text as typed (CR-444's path, no host change). A writer who types `More` in a
   blank-lines block shown inside an item, with no indentation, gets a paragraph at column 0, which
   ends the list there; typing `- c` between two items adds an item. The other choice is for the host
   to indent the typed lines to the host item's content column, so the block stays in the item (and
   a typed `- c` becomes a sub-item). Keep "as typed", or indent to the item?
