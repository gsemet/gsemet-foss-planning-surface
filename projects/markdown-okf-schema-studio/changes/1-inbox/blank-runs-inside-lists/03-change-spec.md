# Show blank-line runs inside lists as blank-lines blocks

In edit mode, a run of two or more blank lines between two items of a list, or inside a list item,
shows as the same blank-lines block CR-444 shows between top-level blocks. It is placed inside the
list where the run is. The writer reaches it, types in it or removes it as with any blank-lines
block. A block typed there is indented to the item, so it stays in the item. Removing the run keeps
one blank line, so the list stays one list and nothing else in the file changes.

Origin: verbal (found by the spec critic of CR-444 empty-block-blank-lines-block, 2026-11-21;
owner's goal, 2026-11-20; owner's answers, 2026-11-21). No issue.

## Goal

The owner's goal (2026-11-20): blank lines beyond the one separator are always reachable in edit
mode. CR-444 (merged, PR #453) made the runs between top-level blocks reachable. A run that lies
inside a list's lines is still unreachable: the page skips every run that a top-level block holds,
so a writer cannot see or remove the extra blank lines between two items of a list or between two
paragraphs of a list item.

This CR shows those runs. It reuses everything CR-444 built. On the host, the only change is the
indentation of a block typed or pasted in place of a run inside a list item (br-Q5); the host's run
checks and its removal stay as they are. CR-444's specification is
`4-batch/3-done/444-empty-block-blank-lines-block/03-change-spec.md` in the planning folder. This
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
  line is before the run and its last line after it). It is in one of two places:
  - **between items**: the line after the run starts the next item of the same list (at any
    nesting depth);
  - **inside an item**: the line after the run is more content of the same item (a paragraph, a
    nested list, a fence...).
- **Holder** of a run: a mapped element of the active document whose range holds the run strictly:
  `line < run.line && run.endLine < endLine` (`rt.blocks.blockRange`).
- **Host item** of a run inside a list: the list item (`li`) the blank-lines block goes into (rule
  below). Its **item line** is its first source line (its `data-sphinx-source-line`): the line that
  holds its list marker.
- **Item indent**: the leading spaces and tabs of the item line, copied as they are.
- **Content indent**: the item indent, followed by one space for each character of the marker and
  of the spaces after it. The marker is `-`, `+`, `*`, or 1 to 9 digits followed by `.` or `)`.
  When five or more spaces follow the marker, or nothing follows it, only one space counts after it
  (CommonMark's rule for an item's content column). A tab after the marker counts as one space.
  Examples: `- a` gives 2 spaces, `  10. a` gives 6, `-     code` gives 2.

## What CR-444 already gives, unchanged

- **The host lists every run.** `blankRuns(text)` returns every run after the frontmatter, wherever
  it is, including runs inside lists and inside fences. `renderPreviewSource`
  (`src/core/render/renderPipeline.ts`, `blankRunsMarker`) appends them as the last element of the
  content: `<div hidden data-okf-blank-runs="L-E ...">`. No change there.
- **The page reads only that element** (`readRuns` in `src/page/features/blankLines.ts`) and builds
  every blank-lines block itself (`create`). No change there. CR-444's guard against an authored
  attribute holds for runs inside lists too.
- **The run checks and the removal work on line numbers only.** `checkBlankRun` and
  `planBlankRunRemoval` (`blockRange.ts`), and `handleBlankRunDelete`
  (`src/session/features/sourceEdits.ts`), check and remove a run by its lines alone, so a run
  inside a list passes the same checks. The removal deletes lines `line + 1`..`endLine` and keeps
  line `line` byte for byte (br-Q3, br-Q4). The session tests of this CR prove it on list texts.
- **The block's look, label, keys and messages**:
  - the dashed bar, with the CSS label "Blank lines (N)";
  - `role="button"`, `tabindex="0"`, and the Delete block button at its left edge;
  - Enter or a click opens the insertion editor (`open`); Delete and Backspace act on a selected
    block (`deleteSelection`);
  - the messages `previewBlankRunDelete`, and `previewEditOpen`/`Save`/`Cancel` and
    `previewBlocksPaste` with `replaceBlankRun`;
  - the editor stays open across an autosave's re-render (br-Q2).

## What changes

### 1. Scope (br-Q1)

- **In scope:** runs between two items of the same list, and runs inside a list item, at any
  nesting depth, in a top-level list of the body.
- **Quotes and admonitions are split out** into `1-inbox/blank-runs-inside-quotes-admonitions`
  (filed 2026-11-21), because the same mechanism does not serve them:
  - Inside a quote, and inside a GitHub alert (`> [!NOTE]`, which is a quote), the empty lines of
    the block are `>` lines. They are not CommonMark blank lines, so `blankRuns` never lists them.
    The host would need a new run finder and new run checks.
  - A MyST admonition is a directive. CR-444 treats a directive's lines as the block's content.
    Telling an admonition apart from the other directives (code-block, list-table, tab-set, math,
    figure) would need a new placement rule for each directive kind.
  - A list held by a quote, an alert or an admonition goes with them: a run in it shows nothing in
    this CR.

### 2. Placement inside a list (br-Q2)

All of it is in `refresh()` of `src/page/features/blankLines.ts`. Today `refresh()` computes
`inside` (a top-level body block holds the run) and skips such a run. The new rule, for each run of
the host's list:

1. **No holder among the top-level body blocks.** CR-444's top-level rule applies, unchanged:
   - the run goes after the insertion bar of the block above;
   - a run next to a folded block shows nothing;
   - in an empty body it goes before "Start writing";
   - a run that starts on the blank separator ending a list shows (BLOCK-256).
2. **Held by a top-level block that is not a `ul` or `ol`**: nothing, as today. Such blocks are a
   fence, an HTML block, a directive, an admonition, a quote, a table or a list-table.
3. **Held by a top-level `ul` or `ol`.** Collect every holder of the run among the mapped elements
   inside that list (`rt.blocks.mappedChildren`, recursively, or the mapped elements under it). Take
   only the same file and document, and never an included block (`isIncludedBlock`). If any holder
   is not a `ul`, `ol` or `li` element, the run shows nothing. Blank lines inside a fence, a
   directive, an HTML block or a table in a list item therefore stay out of reach: they are that
   block's content.
4. **Folded:** a run whose top-level list carries `data-okf-folded` shows nothing, and unfolding
   shows it again, as CR-444's folded rule does for its neighbours.
5. **Host item.** It is the deepest holder that is an `li`. When the deepest holder is a `ul` or
   `ol`, the host item is that list's last `li` child whose line is before `run.line`. This happens
   for a run between items when the renderer does not count the run in the item above.
6. **Position.** The blank-lines block goes inside the host item, right after the item's last child
   element that starts before the run. That is the child whose mapped line is before `run.line`, or
   the item's last child when the whole item ends before the run. The block is never a direct child
   of a `ul` or `ol`. So a run between items A and B shows at the end of item A, and a run between
   two paragraphs of an item shows between them, indented with the item's content (br-Q2: "shown
   inside the list where the run is").
7. **Item line.** The page keeps the host item's line with the run (`runs` map, for example
   `{ line, endLine, itemLine }`) and sends it as `replaceBlankRun.itemLine` (section 5). A
   top-level run has no `itemLine`.
8. **Refresh.**
   - A kept run keeps its element (the `existing` map, same line and end line), as for top-level
     runs.
   - The block of the open editor (`editing`) stays where it is across a refresh.
   - When a content swap dropped that block, `place` puts it back inside its host item by the rule
     of point 6. For a run inside a list, today's `aboveOf` fallback becomes that placement.

`place(block, above)` gains a branch for a run inside a list (for example
`placeInItem(block, item, run)`), or the Driver splits the placement into a small helper of the same
file. `blankLines.ts` is 203 lines, so it stays under the 800-line cap.

### 3. Keyboard and pointer (br-Q2)

The keys are CR-444's. Two places of `src/page/features/blockSelectionView.ts` change, so that the
arrows reach a blank-lines block inside a list like any other:

- **Up and Down: stops in the order of their first line.**
  - Today `neighbourStop` finds the next stop with `stop.line > endLine` of the current one. Down
    from a selected list therefore skips the blank-lines blocks inside it, while Up from the block
    after the list lands on them.
  - New order: Down goes to the first stop whose first line is after the current stop's first line.
    Up goes to the last stop whose first line is before it.
  - The stops stay the top-level body blocks and all visible blank-lines blocks (`stops`).
  - Result: with a list selected, Down goes to the first blank-lines block inside it. The next Down
    goes to the next blank-lines block inside it, or to the block after the list. Up walks back the
    same way.
  - For top-level stops the order is unchanged, because their ranges do not overlap. Without any
    blank-lines block, the block selection (BLOCK-004) keeps its index path.
- **Shift+Up/Down from a selected blank-lines block** starts the block selection on the nearest
  body block in that direction, skipping blank-lines blocks. Today `next.blank` ends the key with
  nothing done, so with two runs in one list, Shift+Down from the first would do nothing. For a
  blank-lines block inside a list, Shift+Up starts the selection on the list and Shift+Down on the
  block after the list.
- **The selection after a removal (`requestDeleteBlankLines`).**
  - Today `targetIndex` counts the body blocks that start before the run. For a run inside a list
    that selects the block after the list.
  - New: for a run inside a list, the selection goes to the top-level list that held it.
  - For a top-level run nothing changes: the following block, else the one above, else "Start
    writing". The viewport pin is unchanged.
- **Unchanged, and to keep:**
  - A click on a blank-lines block inside a list opens its insertion editor, never the list item
    editor (the click handler stops propagation). Shift+click does nothing.
  - Delete and Backspace act only on a selected one.
  - Alt+Up/Down on it moves nothing. The list item handles' Alt+Up/Down acts on a focused handle
    only.
  - Escape clears it.
  - Ctrl/Cmd+C and +X do nothing while it is selected; Ctrl/Cmd+V pastes in place of its run
    (section 5).
  - The structural navigation (BLOCK-254, Right into a list's items) never stops on it, because it
    is never mapped.

`blockSelectionView.ts` is 660 lines, so it stays under 800.

### 4. Look

- Same element and CSS as CR-444 (`.sphinx-preview-blank-lines`, the named block of
  `src/core/preview/styles/editModeStyles.ts`). Inside an item, it is as wide as the item's content
  box, not the content column.
- Its Delete block button stays at its left edge, and must not overlap the list item handles
  (`installListItemMove`, `src/page/features/listItemMove.ts`; the handles sit in their own layer,
  left of the list). The visual captures check it.
- `editModeStyles.ts` is 792 lines, under the 800-line cap. If the change needs new CSS rules (for
  example a margin inside an `li`), the Driver moves the blank-lines block's named CSS block to a
  style module of its own, wired where `editModeStyles.ts` is, rather than raising the cap.

### 5. Typing and pasting in a run inside a list (br-Q2, br-Q5)

The owner's answer (br-Q5): "Indent to the item". The host indents the typed lines to the item's
content column, so "More" stays inside the item. A line typed at the item's own level ("- c") still
adds an item.

**The message.** `replaceBlankRun` gains an optional field, `itemLine`: the host item's line, sent
by the page for a run inside a list only (section 2, point 7). It is carried on `previewEditOpen`,
`previewEditSave`, `previewEditCancel` and `previewBlocksPaste`.
- Add it to the `replaceBlankRun` type in `src/core/protocol/pageToHostMessages.ts`.
- Add it to `isBlankRunFields` in `src/core/protocol/pageToHost.ts`. It is valid only when it is
  `isSourceLine` and below `line`.
- A top-level run sends no `itemLine` and behaves exactly as today.

**The indentation (core).** Add a pure function, for example
`listItemIndent(text, itemLine): { item: string; content: string } | undefined`, in
`src/core/mapping/insertion.ts` (or a new file `src/core/mapping/listItemIndent.ts` when
`insertion.ts` would pass a size limit).
- It reads the item line by `splitLines`. It returns the item indent and the content indent (see
  "Words").
- It returns `undefined` when:
  - the line does not start with a list marker (`-`, `+`, `*`, or 1 to 9 digits followed by `.` or
    `)`) that is followed by a space, a tab or the end of the line;
  - the line is a thematic break (`- - -`, `***`);
  - the line is in the frontmatter, or it is not before the run.

**Which indent a typed block takes.**
- The block takes the **item indent** (a sibling item) when its first non-blank typed line, after
  its own leading spaces and tabs, starts with a list marker followed by a space, a tab or the end of
  the line, and is not a thematic break. Example: "- c" typed in a run between `- a` and `- b`, or
  at the end of item `a`, adds the item `- c`.
- Otherwise it takes the **content indent**. Example: "More" becomes a paragraph of the item.
- The chosen indent goes before every line of the block that is not blank, after the writer's own
  indentation is kept (`insertionText` already keeps the first line's indentation as typed). Blank
  lines of the block get nothing added.
- The separators before and after the block stay plain empty lines, as CR-444 writes them.
- The block's line endings are the document's (BLOCK-094, BLOCK-234).
- Nothing else in the file changes (br-Q4).
- In an ordered list, a typed "- c" at the item level starts another list there. That is how
  Markdown reads it, and it is written as typed.

**Where it goes in the plan.** `InsertionPlan` gains an optional `indent?: string`.
- `planBlankRunInsertion(text, line, endLine, itemLine?)` sets it from `listItemIndent`.
- `insertionText(plan, raw)` applies it: it picks the item or content indent from the first typed
  line, as above. The plan therefore carries both indents, for example
  `listIndent?: { item: string; content: string }`. The Driver names the shape.
- `planBlankRunPaste(text, line, endLine, raw, itemLine?)` passes it the same way, so a paste
  follows the same rule.
- An autosave and each later save reuse the held edit's `insertion` plan
  (`src/session/features/blockEdits.ts`, the held `ActiveBlockEdit`). So every save of that editor
  writes with the same indent.

**The host's checks.** The host never trusts `itemLine` without checking it.
- `handleEditOpen` (the `replaceBlankRun` branch beside `checkBlankRun`, around line 188), the
  re-created save of `handleEditSave` (around line 442) and the paste handler in `sourceEdits.ts`
  each call `listItemIndent` when `itemLine` is present.
- An `undefined` result is refused with that path's existing stale message: "The preview is stale.
  Refresh it before editing this block." on open, "The preview is stale. Reopen the block before
  saving." on a re-created save, and the out-of-date reason on a paste.
- A save or cancel whose `replaceBlankRun` (with its `itemLine`) differs from the held edit's is
  refused with the held-edit stale reason, as a different run is today (`sameBlankRun`).

**Unchanged from CR-444:** one separator on each side, written in one text edit. An empty Done
writes nothing. Cancel after an autosave restores the run byte for byte. The page-facing
`originalText` stays `""`, and a stale run is refused.

### 6. Removing a run inside a list (br-Q3, br-Q4)

Delete or Backspace on the selected block, or its Delete block button, goes through CR-444's path
unchanged:
- Lines `line + 1`..`endLine` go, in one text edit and one undo step.
- Line `line` stays as it is, its spaces or tabs included.
- Between two items, the one blank line left keeps the list one loose list, as a single blank line
  between items does today (br-Q3).
- No other line of the list or the file changes (br-Q4).

`previewBlankRunDelete` carries no `itemLine`. A stale run is refused as today.

### 7. Requirements

Follow the project's requirements guidelines: markers move with the code; run
`just requirements-update`; add a dated entry in `requirements/tiers/log.md`. All of it is in scope
`block-editing`.

Update the four SwRS of CR-444 (all `proposed`). The log entry gives the reason: they said runs
inside lists show nothing.

- **SwRS-MDOKFSTUDIO-BLOCK-266** (where a run shows):
  - The title and the normative text cover a run between two items of a list or inside a list item,
    shown inside the item that holds it.
  - The "Nothing is shown" scenario drops "or a list". It adds a run inside a fence, a directive, an
    HTML block or a table in a list item, and a run inside a quote, an alert, an admonition or a
    list they hold.
  - Add a scenario "Runs inside a list are shown".
- **SwRS-MDOKFSTUDIO-BLOCK-267** (arrows, Enter, click): add a scenario.
  - Down from a selected list stops on each blank-lines block inside it, in line order, then on the
    block after the list. Up walks back.
  - Shift+Up/Down from one starts the block selection on the list or on the block after it.
  - A click on one opens its insertion editor, not the list item editor.
- **SwRS-MDOKFSTUDIO-BLOCK-268** (typing or pasting):
  - The normative text adds that a block written in place of a run inside a list item takes the
    item's content indent, or the item's own indent when its first line starts with a list marker.
    The host checks the item line, and refuses it stale when it is not a list item line.
  - Add a scenario "A block typed inside a list item stays in the item", covering "More" and
    "- c".
- **SwRS-MDOKFSTUDIO-BLOCK-269** (removal): add a scenario. Removing a run between two items, or
  inside an item, keeps line `line` and leaves one list. The selection goes to the list that held
  the run.
- No new StRS. `derives_from` stays StRS BLOCK-011 and BLOCK-025, whose text is unchanged.
- New tests carry `@tests_req` for the SwRS they check. The changed code in `blankLines.ts`,
  `blockSelectionView.ts`, `insertion.ts` (or `listItemIndent.ts`), `blockRange.ts`,
  `pageToHost.ts` and `blockEdits.ts` keeps or gains its `@implements_req` markers, with at most 3
  IDs per marker block.

### 8. Shared vocabulary and docs

- `.agents/glossary/common.md`:
  - "Blank run" today says "between top-level blocks, at the start or at the end of the body". Add
    "between two items of a list or inside a list item".
  - "Blank-lines block": add that inside a list it shows in the item that holds the run, and that a
    block typed in it is indented to that item.
  - Add "Content indent" if the code uses the word (the item's content column, as in "Words").
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes, and the blank-lines block is edit-mode chrome.
- The release notes are written when the release is prepared, not in this PR.

## Out of scope

- Runs inside a quote, a GitHub alert or a MyST admonition, and in a list they hold:
  `1-inbox/blank-runs-inside-quotes-admonitions`.
- Blank lines inside a fence, a directive, an HTML block or a table, including when it sits in a
  list item: they are the block's content (CR-444, BLOCK-256 unchanged).
- Any change to `blankRuns`, to the hidden run list, to `checkBlankRun` or to the removal plan.
- Indenting anything but the block the writer types or pastes in place of a run inside a list. The
  same goes for a top-level run, an insertion bar's editor and a block edit.
- Collapsing runs on its own, on save, on render or on any other edit. Making a loose list tight.
  Re-indenting the list.
- How a list item move (handle drag, or Alt+Up/Down on a handle) carries the blank lines of an item:
  unchanged.
- Runs in an included file, in the frontmatter or in a cell of the properties table.
- Moving a blank-lines block, or dragging blocks or list items onto it.

## Evidence

The checks read the shipped files at the head under test: the real render pipeline, the real page
bundle and the real stylesheet, never a prepared copy. Each new check fails on the code before the
change (constitution, section 3). CR-444's existing tests keep their intent: "a run inside a block
gets no blank-lines block" (a block that is not a list) still passes unchanged. A CR-444 assertion
that expected nothing for a run between list items is changed only for that reason, and the commit
says so.

**Core, `test/core/mapping/`** (each in LF, CR LF and lone CR):

- `listItemIndent`:
  - `- a` gives item `""` and content of 2 spaces;
  - `  * a` gives 2 and 4 spaces;
  - `10. a` gives 4 spaces of content; `3) a` gives 3;
  - a tab before the marker is kept as is in both indents;
  - `-      code` (six spaces) gives 2 spaces of content; a bare `-` gives 2;
  - `undefined` for a paragraph line, a thematic break (`- - -`, `***`), a frontmatter line, and a
    line at or after the run.
- `planBlankRunInsertion` with `itemLine`, through `insertionText`:
  - "More" between `- a` and `- b` gives `- a`, blank, `  More`, blank, `- b`;
  - "More" between two paragraphs of an item indented 2 gives `  More`;
  - a two-line "More\nText" with a blank line between gives `  More`, an empty line, `  Text`;
  - "- c" gives `- c` at the item level; "- c" in a nested item (`  - a1`) gives `  - c`;
  - "  - sub" (a marker after two typed spaces) takes the item indent and keeps the writer's own
    two spaces after it: `  - sub` under `- a`, a sub-item of `a`;
  - without `itemLine`, the output is identical to today;
  - no bare LF in CR LF, and no CR in LF.
- `planBlankRunPaste` with `itemLine`: the same rule for pasted "More" and "- c".
- `planBlankRunRemoval` on the list texts: one blank line kept byte for byte, and re-rendering the
  result gives one top-level `ul`.

**Protocol, `test/core/protocol/pageToHost.test.ts`:** `replaceBlankRun.itemLine` is accepted when
it is a source line below `line`. It is rejected when it is at or after `line`, when it is not an
integer, or on a message type that does not take `replaceBlankRun`.

**Render, `test/core/render/`** (the real renderer, so the inputs of the placement are real). Take a
list text with four runs: one between items, one between two paragraphs of an item, one inside a
fence of an item, and one in a list inside a MyST admonition. `renderPreviewSource` gives:

- the run list with all four runs;
- a top-level `ul` whose `data-line` and `data-end-line` hold the first two runs strictly, and `li`
  elements whose `data-line` is their marker line;
- the fence's `pre` (or its mapped element), with a range that holds its run strictly;
- the admonition, as the top-level holder of the fourth run.

**Page, `test/page/runtimeBlankLines.test.ts`** (runtime bundle, one check per rule). Add a list
shape to the harness: a `ul` with mapped `li` children and mapped blocks inside them. The checks:

- a run between two items makes one blank-lines block, as the last child of the item above, never a
  direct child of the `ul`;
- a run between two paragraphs of an item makes one, between them inside that item;
- a run between two items of a nested list goes into the nested item above;
- a run inside a fence in an item, and a run inside a list held by an admonition, make none;
- a run inside a folded list makes none, and unfolding makes it;
- a content patch keeps the element of an unchanged run inside a list;
- an editor opened from one inside a list stays in its element across a patch without that run;
- Down from the selected list stops on each blank-lines block inside it, in line order, then on the
  block after the list; Up walks back through them to the list;
- Shift+Up and Shift+Down from one start the block selection on the list and on the block after it;
- a click on one posts `previewEditOpen` with `replaceBlankRun` carrying the host item's
  `itemLine`, and opens no list item editor; a top-level run's message has no `itemLine`;
- Ctrl/Cmd+V on a selected one posts `previewBlocksPaste` with the same `itemLine`;
- Delete on a selected one posts `previewBlankRunDelete`; after the removal result and the render,
  the list is selected.

**Session, `test/session/blankRunHost.test.ts`** (the real handlers, in LF and CR LF):

- `previewBlankRunDelete` on a run between the items `- a` and `- b`:
  - lines `line + 1`..`endLine` go, and the first blank line stays byte for byte (with its spaces
    when it has some);
  - one `applyWrittenEdits` call, and the rest of the text is identical.
- The same for a run between two paragraphs of an item indented with two spaces.
- Typing in a run between items:
  - a save of "More" with `itemLine` writes `  More` with one separator on each side;
  - a later autosave of "More text" replaces it with `  More text`;
  - Cancel after the autosave restores the run byte for byte.
- A save of "- c" writes `- c` at the item level.
- A re-created save (no held edit) with `itemLine` writes the same indent.
- A stale `itemLine` (a paragraph line, or a line that changed into one) is refused, with the stale
  message of open, of the re-created save and of the paste. The document does not change.
- A paste with `itemLine` writes `  More`.

**Visual (`just ci-visual`):** add a new fixture (for example
`test/visual/fixtures/93-blank-lines-in-lists.md`) with a run between two items, a run inside an
item, and a fence with blank lines in an item. Add scenarios in
`test/visual/blankLinesBlockScenarios.ts`, with checks in `test/visual/capture_blank_lines_block.py`:

- edit mode: exactly two blank-lines blocks, each inside the right `li`, as wide as the item's
  content, and none in the fence;
- one selected with the arrows: its Delete block button shows at its left edge, and its box does
  not overlap any list item handle;
- reading mode: none.

The captures are attached to the PR, as the pull-request guideline asks.

**Integration (real VS Code, `just ci-integration`, heavy run on the branch).** In
`test/integration/blankLines.test.ts`, add a second fixture, in LF and in CR LF: a list with three
blank lines between two items and three inside an item.

1. Send `previewBlankRunDelete` for the run between the items. One blank line is left, the list's
   other lines are unchanged, and there is no bare LF in CR LF. One undo brings the run back.
2. Send `previewEditSave` with `replaceBlankRun` (with its `itemLine`) for the run inside the item,
   with the text `More`. The run is replaced by `More`, indented to the item's content column, with
   one blank line on each side, and the line endings are kept. One undo brings the run back.
3. Send the same save for the run between the items, with the text `- c`. A new item `- c` sits at
   the item level, with one blank line on each side.

**Requirements:** `just requirements-lint` and `just requirements-update` pass. The updated SwRS
carry their markers at the code and the tests above.

**Gate:** `just preflight` passes (on Windows, its static stage; CI runs the others).
