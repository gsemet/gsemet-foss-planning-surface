# Enter and click in an admonition open the selected element

In the Studio preview, in edit mode, an admonition (a MyST `{note}`-style directive, backtick or
colon fence, a `:class: dropdown` included) or a GitHub alert (`> [!NOTE]`) opens today as one
block, whatever the writer aims at: Enter on a list item or a paragraph reached with the arrows
opens the whole admonition, and so does a click in its body. After this change, the whole
admonition opens only when the admonition itself is selected or pointed at (keyboard selection of
the admonition, or a click on its title or its frame); otherwise exactly the element reached with
the arrows, or the element under the pointer, opens. From the editor of a list item inside an
admonition, the move chord moves that list inside the admonition, and Down or Up at the edge of
the list keeps the caret in the editor. The keyboard navigation clip is re-filmed to show it, down
to an item of a nested sub-list, and the user guide follows.

Short name: `enter-admonition`. Destination: running batch batch-09 (stack). Found while filming
the keyboard navigation clip (CR-501, merged with PR #522), frame
`changes/4-batch/3-done/501-clip-keyboard-navigation-in-nested-admon/evidence/finding-enter-on-item-opens-admonition.jpg`.
No issue.

## Goal, in the user's terms

- An admonition selected as a whole (what the keyboard gives when Down reaches it) opens whole
  with Enter.
- With the arrows (Right to go in, Up and Down inside, Right again into a list), the writer goes
  down to an inner element; Enter then opens that element only: the paragraph, the list, the list
  item or the block of the list item that is selected (answer 1).
- With the mouse, the writer points straight at the element to open: a click on a list item or a
  paragraph of the body opens it; a click on the title or the frame opens the whole admonition.
  GitHub alerts behave the same (answer 3).
- In the editor of a list item inside an admonition, Cmd+Alt+Up/Down (Ctrl+Alt elsewhere) moves
  that list among the blocks of the admonition, never out of it (answer 5); Down at the end of the
  last item and Up at the start of the first keep the caret in the editor (answer 6).
- The keyboard navigation clip shows the new path: from the keyboard only, down to an item of the
  nested sub-list of the admonition, Enter opens that item alone, one word changes, save (answers
  7 and 9). The `> ` markers of an alert block stay in its editor (answer 8).

## Root cause (read on origin/main)

`editingElementFor` in `src/page/features/mappedBlocks.ts` promotes any target inside
`[data-okf-github-alert], aside.admonition, details.admonition` (context-tag panels,
`myst-context-admonition`, excepted) to the whole admonition **before** it looks at the `exact`
option. The structural Enter (`handleKey` in `src/page/features/structuralNavigationView.ts`)
calls `openMappedEditor(..., exact = true)` for an inner block, but the promotion wins, so the
whole admonition opens. The unit test `CR 157: Enter on an inner block opens that block's editor`
in `test/page/runtimeStructuralNavigation.test.ts` passes only because its "admonition" is a plain
mapped element without the `admonition` class. The click path (`pageInput.ts` click handler, then
`openMappedEditor` without `exact`) gets the same promotion, by design today (SwRS-MDOKFSTUDIO-BLOCK-014
S1 and S3 rows on admonitions and alerts, added on 2026-10-29).

The editor keys of an item (`src/page/features/blockEditor.ts`) only know top-level blocks:
`moveBlockFromEditor` moves `topLevelBlockOf(item)` past its top-level neighbour, and
`adjacentMappedBlock` steps from the last item to the top-level block after `topLevelBlockOf(item)`.
Today this was hardly reachable, since an item in an admonition never opened alone.

## What changes

### 1. The editing element (`src/page/features/mappedBlocks.ts`, `editingElementFor`)

New rule, for the click and the keyboard alike:

- Let `adm` be the nearest admonition around the target (same selector as today, context-tag
  panels still skipped).
- The whole admonition (its range from `sourceRangeForAlert`, unchanged: directive opening fence
  to closing fence; alert marker line to last quoted line, with the indentation of an alert inside
  a list item) is the editing element only when the target **is** `adm` itself (a click on its
  frame, padding or the gap between inner blocks lands on the admonition element; a keyboard
  selection of the admonition passes the admonition), or the target is inside the title of `adm`
  (`.admonition-title` that is a direct child of `adm`, `summary.admonition-title` for a dropdown;
  this holds whether the title element is mapped or not).
- Otherwise the target is a block of the body: the list rules apply as today (a list item opens
  that item, the nearest item winning; the list itself, outside its items, opens the whole list;
  with `exact`, a block inside an item opens on its own with `sourceRangeForInnerBlock`), and a
  block not in a list opens on its own lines (`{ element: target, sourceRange: undefined }`, as
  for any block).
- A list **around** the admonition never takes over a body block: the list lookup
  (`closest("ul, ol")`, `closest("li")`) is bounded by `adm`, so a paragraph in the body of an
  alert indented in a list item opens that paragraph, not the outer item. Only a list inside `adm`
  (between the target and `adm`) is considered.
- A nested admonition: the nearest one decides. A click in the body of the inner one opens the
  pointed block; on the inner title or frame, the inner admonition; the outer one opens only from
  its own title or frame.
- Reword to the new rule the comments that state the old one:
  - the comment at the head of `editingElementFor`;
  - `src/core/render/mystNormalize.ts`, next to `data-okf-github-alert` ("a click in its body
    opens the whole alert");
  - `src/core/render/mystGithubAlerts.ts`, the doc comment of `mapAlertSourceLines` (about line
    166-170: the `githubAlert` flag "so the page can open the whole alert in one block editor"):
    the flag lets the title or the frame open the whole alert in one block editor.

Which element opens is decided in `editingElementFor` only: `structuralNavigationView.ts`,
`blockSelectionView.ts`, `pageInput.ts` and `editMode.ts` need no change for it, since they all
go through it. As a consequence of the new rule, which the requirements below record:

- the edit-hover outline (`editHoverTarget` in `src/page/features/editMode.ts`, SwRS-MDOKFSTUDIO-BLOCK-017)
  outlines the pointed body block, and the admonition only over its title or frame, since it
  outlines what a click would open;
- the caret context of a click (`clickCaretContext`) is read in the opened element;
- Enter or Space on a focused body block (BLOCK-014 S2, "like a click") opens that block;
- Enter on a top-level selected admonition (`blockSelectionView.ts`, `openMappedEditor(block, block)`)
  still opens the whole admonition.

The editor of a body block holds the lines of that block exactly as they are in the file
(`previewEditSource` gives them): for a GitHub alert, its `> ` quote markers (and the list-item
indentation of an indented alert) are part of the text, as they are for a block in a plain block
quote today (answer 8: the markers stay; no new mechanism).

### 2. The move chord from an item editor inside an admonition (answer 5)

Scope: the editor of a list item (`edit.target` is an `LI`, the case `moveBlockFromEditor` turns
into `topLevelBlockOf` today) whose nearest admonition (the same selector and the same
context-tag exception as in section 1) lies inside its top-level block. The chord from any other
editor is unchanged (see open questions 1 and 2). An item with no admonition around it is
unchanged (the whole top-level list moves, BLOCK-130 S6).

Page side, `src/page/features/blockEditor.ts` and `src/page/features/blockMoves.ts`:

- **What moves.** The body block of `adm` that holds the item: the member of
  `rt.blocks.mappedChildren(adm)` that contains the `LI`, that is the outermost list of the
  admonition's body around the item. For an item of a nested sub-list, that outermost list moves
  with all its items, as the top-level rule does today for a nested item.
- **Past which neighbour.** The previous or next member of `mappedChildren(adm)`, in source order:
  a paragraph, another list, a code block, a nested admonition taken whole. Included blocks
  (`isIncludedBlock`) are not neighbours, as in `bodyBlockNeighbour`. The admonition's title
  is not a mapped child and is never crossed; nor is the fence or the alert marker line. A new
  inner-neighbour function sits beside `bodyBlockNeighbour` (which stays top-level only).
- **No neighbour inside the admonition** (the list is the first block of the body and the chord is
  up, or the last and the chord is down): the key is consumed and nothing happens, as BLOCK-130 S7
  says for the last block; nothing is saved by the chord, the editor stays open, the list never
  leaves the admonition.
- **Nested admonitions.** The nearest admonition around the item bounds the move: a list in the
  body of an inner admonition moves among the inner admonition's body blocks only. An alert
  indented in a list item: the alert bounds the move, the outer item and its list are not moved.
- **The host message.** The same `previewBlockMove` as today (`postBlockMove`): `line` and
  `endLine` of the inner list, `neighbourLine` and `neighbourEndLine` of the inner neighbour, the
  direction. No new message, no new field (SwRS-MDOKFSTUDIO-BLOCK-259 unchanged). Both paths of
  `moveBlockFromEditor` reach it through `requestBlockMove` in `blockMoves.ts`:
  - nothing to save: `closeBlockEdit(true)`, then `requestBlockMove(list, direction, "edit", offset)`
    at once;
  - unsaved text: `rememberPendingBlockNavigation(list, "end", undefined, undefined, {direction,
    caretOffset})`, then `postBlockEditSave(true)`; after the save renders,
    `resumePendingBlockNavigation` (`src/page/features/editMode.ts`, the `thenMove` branch) finds the
    list again (its breadth-first walk already reaches inner blocks) and calls
    `rt.blockMoves.requestBlockMove(target, direction, "edit", caretOffset)`; when that returns
    false it only reopens the list's editor (`openMappedEditor(target, target, {offset}, false)`).
  - `requestBlockMove` takes its neighbour from `bodyBlockNeighbour`, which knows top-level blocks
    only: for an inner list it finds none and returns false. So the inner neighbour (above) must be
    used by `requestBlockMove` itself (or by a variant both paths call), not only by
    `moveBlockFromEditor`; otherwise the save path saves the item, reopens the editor and moves
    nothing.
- **After the render.** `settleBlockMove`, `resumeBlockMove`, `runStaleRetry` and
  `finishMoveRefusal` find the moved block with `rt.blocks.bodyBlockAtLine`, which knows
  top-level blocks only. They must find an inner list too (for example the breadth-first walk
  that `resumePendingBlockNavigation` already does over mapped children), so that the moved list's
  editor opens at its new place with the caret at the remembered offset, as for a top-level list
  (BLOCK-130 S6), and so that a stale or refused move settles on it.

Host side, `planBlockMove` in `src/core/mapping/blockMove.ts` (via `planBlockMoveEdit` in
`src/core/edits/sourceEdits.ts`, `handleBlockMove` in `src/session/features/sourceEdits.ts`):

- In a MyST admonition (backtick or colon fence) the body blocks are plain lines and the
  separator is a real blank line: the planner works as today. Where the swap would glue a block to
  the opening fence, an option line or the closing fence, it adds a blank line (BLOCK-117 S4);
  MyST accepts it.
- In a GitHub alert every body line carries the quote prefix (`> `, or the list-item indentation
  then `> ` for an alert indented in a list item), and the separator between two body blocks is a
  prefix-only line (`>`), which the planner counts as non-blank text today, so it refuses the
  move ("Text between the two blocks ... prevents the move."); a blank line it would add (`""`)
  would cut the quote in two. The planner learns the container prefix: when both blocks and the
  lines between them share one quote prefix, a line that holds only that prefix counts as blank,
  and a separator line it adds carries the prefix. Mixed prefixes (the two blocks not in the same
  quote) are refused, with the existing refusal for ranges that do not match the document
  (BLOCK-124) or a new reason; the Driver picks the existing one when it fits and says which.
- Top-level moves stay byte-identical to today (the existing tests of
  `test/core/mapping/blockMove.test.ts` pass unchanged).
- The ranges stay untrusted, checked against the document as today (BLOCK-124).

### 3. Down and Up at the edge of a list inside an admonition (answer 6)

`adjacentMappedBlock` in `src/page/features/blockEditor.ts`: when the edited item, or the item that
holds the edited inner block, has no previous (Up) or next (Down) sibling `LI`, and its list lies
inside an admonition (same selector and exception as in section 1), it returns `undefined`:
`navigateBlockEdit` returns false and the key stays with the text box, the caret stays where it is
and the editor stays open, as the editor of a paragraph of the admonition does today (BLOCK-079 S6
last row). Between items of the same list, Down and Up still open the next or previous item. Lists
outside admonitions are unchanged (the next or previous top-level block opens). For an item of a
nested sub-list inside an admonition, Down past its last sibling keeps the caret too (the rule
looks at the item's own siblings and the admonition around it).

### 4. Requirements (`requirements/tiers/`)

All touched requirements have `req_lifecycle: proposed`; none is `approved`, so no owner approval
is needed. The approved StRS-MDOKFSTUDIO-BLOCK-003 is not changed (its path "the writer clicks a
rendered block and its editor opens with the lines of the block" still holds); if the Driver finds
it must change, stop and report, per "Approved requirements" of
`requirements/guidelines/project.guidelines.md`.

- **SwRS-MDOKFSTUDIO-BLOCK-014** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-014.md`):
  - S1 "Paragraph, image or admonition": a click on the title or the frame of the admonition or
    of the alert opens the whole directive or alert (ranges as today); a click on a paragraph or
    a list item of the body opens that paragraph or item on its own lines.
  - S3, the two rows "a paragraph or a list item in the body of a MyST admonition" and "... of a
    GitHub alert, also an alert indented in a list item": rewritten. The pointed paragraph or
    list item opens on its own lines (the list rules of the rows above apply inside the body);
    the title or the frame opens the whole admonition or alert; a list around the admonition or
    alert never takes over a block of its body; nested admonitions: the nearest one decides;
    context-tag panels unchanged (MYST-013).
  - The `editingElementFor` part of the Criteria and the Verification notes follow the new tests.
- **SwRS-MDOKFSTUDIO-BLOCK-254** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-254.md`):
  - Normative statement and description: Enter opens the editor of the selected element only:
    the selected cell, list, list item, block of a list item, or block inside an admonition, alert,
    card or tab (the Driver keeps the wording to what the code does for cards and tabs; checking
    them is part of the work).
  - New scenario `S5 (nominal): Walking an admonition`, declared in `scenarios:`: GIVEN edit mode
    on, no editor open, an admonition (and, as a row, a GitHub alert) selected by the keyboard
    whose body holds a paragraph and a list of items, one with a nested sub-list; WHEN the writer
    presses Enter; or ArrowRight, then Enter; or ArrowRight, ArrowDown, ArrowRight, then Enter;
    or goes on down to an item of the nested sub-list, then Enter; or comes back to the admonition
    with ArrowLeft, then Enter; THEN Enter on the admonition opens the whole admonition, Enter on
    its paragraph opens the paragraph only, Enter on an item opens that item only (a nested item on
    its own line), and back on the admonition Enter opens it whole again; with the lines of each.
  - The S3 sentence "A click on a list item opens the item, not the block under the click
    (BLOCK-014): only the keyboard reaches a block inside an item" stays.
- **SwRS-MDOKFSTUDIO-BLOCK-004**: unchanged (Enter on a selected top-level block opens that block).
  Checked: its text does not contradict the new rule.
- **SwRS-MDOKFSTUDIO-BLOCK-017** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-017.md`): S2 gets
  two rows: "a paragraph or a list item in the body of an admonition or an alert": the pointed
  paragraph or item; "the title or the frame of an admonition or an alert": the whole admonition.
- **SwRS-MDOKFSTUDIO-BLOCK-262** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-262.md`):
  - S5 row "A click on an item of a list in an alert or an admonition | The whole container opens
    in its editor, as before (SwRS-MDOKFSTUDIO-BLOCK-014)" becomes: the clicked item opens in its
    editor; a click on the title or the frame of the alert or admonition opens the whole container
    (SwRS-MDOKFSTUDIO-BLOCK-014).
  - S2 sentence "In an open list item editor, the Cmd/Ctrl+Alt chord still moves the whole list
    (BLOCK-130)" gains: for a list inside an admonition or an alert, the list moves among the
    blocks of that admonition (SwRS-MDOKFSTUDIO-BLOCK-130).
  - Related requirements: the line "SwRS-MDOKFSTUDIO-BLOCK-014: a click on a list item edits that
    item; in an alert or an admonition, the whole container" becomes: a click on a list item edits
    that item, also in an alert or an admonition, whose title or frame edits the whole container;
    the BLOCK-130 line (the chord in a list item editor moves the whole list) adds "inside its
    admonition when it has one".
- **SwRS-MDOKFSTUDIO-BLOCK-130** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-130.md`): new
  scenario `S8 (nominal): The move chord in a list item editor inside an admonition`, declared in
  `scenarios:`:

  | Input | Outcome |
  | --- | --- |
  | The chord down in the editor of an item of a list in the body of a MyST admonition, a paragraph after the list | The item is saved if changed, the list and the paragraph swap inside the admonition, the fence and the title stay, and the list's editor opens at its new place with the caret at the same offset |
  | The same in a GitHub alert, also an alert indented in a list item | The same; every line keeps its quote prefix |
  | An item of a nested sub-list | The outermost list of the admonition's body moves, with all its items |
  | The list is the first block of the body and the chord is up, or the last and the chord is down | The key is consumed and nothing happens; the list never leaves the admonition |
  | A list in the body of an admonition nested in another | The list moves among the inner admonition's blocks only |

- **SwRS-MDOKFSTUDIO-BLOCK-117** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-117.md`): new
  scenario `S7 (boundary): Two blocks inside one quote prefix`: two blocks of a GitHub alert body
  (also indented in a list item) swap; the `>` separator line is kept as it is; an added separator
  line carries the prefix; blocks under different prefixes are refused. Its Verification notes name
  the new core tests.
- **SwRS-MDOKFSTUDIO-BLOCK-124**: only if the refusal of mixed prefixes uses a new reason, a row
  for it.
- **SwRS-MDOKFSTUDIO-BLOCK-079** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-079.md`), S6: the two
  rows "ArrowDown at the end of the last item's editor ... past the list, opens" and "ArrowDown at
  the end of the editor of a block inside a list item ... past the last item, the next top-level
  block opens" say "for a list outside an admonition"; a new row: "ArrowDown at the end of the last
  item's editor, or ArrowUp at the start of the first item's editor (or of a block inside them), of
  a list inside an admonition or an alert, a nested sub-list included | The key stays with the text
  box and the editor stays open".
- **SwRS-MDOKFSTUDIO-GFM-009**: no normative change. Its comments in `mystNormalize.ts` and
  `mystGithubAlerts.ts` are reworded (section 1).
- `just requirements-update`, then a dated `## 2026-11-26` (or the day of the change) entry in
  `requirements/tiers/log.md`, sub-heading `### Enter and click in an admonition open the selected element`,
  naming the reversal of the 2026-10-29 entry "A click in the body of a GitHub alert opens the
  whole alert", the chord and the edge keys of an item editor in an admonition, and the owner's
  answers of 2026-11-26.

### 5. Tests

Each changed assertion says why in the commit (constitution, section 3): the owner reversed the
behaviour on 2026-11-26.

- `test/session/alertBlockEditOpen.test.ts` (Markdown rendered and mapped like the preview,
  `createMappedBlocks(...).editingElementFor`):
  - "a click on either paragraph of a two-paragraph alert opens the whole alert..." becomes: a
    click on either paragraph opens that paragraph's lines; a click on the alert title (and on the
    alert element itself) opens marker line to last quoted line.
  - "a click on a list item inside an alert opens the whole alert" becomes: opens that item.
  - "a click on the paragraph of the second alert of the layout fixture opens that whole alert"
    becomes: opens that paragraph.
  - "a click on a paragraph in the body of a MyST admonition opens the whole directive" and "a
    click in the body of a colon-fence admonition opens the whole directive, also from a list
    item" become: the pointed paragraph or item opens; the title opens the whole directive, in a
    backtick and a colon fence.
  - New: a paragraph in the body of an alert indented in a list item opens that paragraph, not the
    outer item and not the alert; the alert's title opens the alert's indented lines.
  - New: nested admonitions: inner body block opens alone, inner title opens the inner directive,
    outer title opens the outer directive.
  - New, keyboard (`{ exact: true }`, as in `test/session/listItemEditOpen.test.ts`): on a MyST
    admonition and a GitHub alert, the admonition opens whole, its paragraph, its list, its item,
    an item of a nested sub-list and a block of an item each open on their own lines.
  - "each of several consecutive alerts opens only its own lines", "an alert inside a list item
    opens on its own indented lines" and the context-tag test stay, the first two driven from the
    title.
  - The existing markers name BLOCK-014 fragments `#S4` and `#S10` for alert and admonition
    tests, which are the link and horizontal-rule scenarios; the rewritten tests name the
    scenario they check (`#S1`, `#S3`, BLOCK-254 `#S5`).
- `test/page/runtimeStructuralNavigation.test.ts`: the page fixture's admonition becomes a real
  `aside` of class `admonition note` (and a second case with `data-okf-github-alert`), so that
  `CR 157: Enter on an inner block opens that block's editor` fails on origin/main and passes
  after; a new test walks Right, Down, Right, Enter into a list item of the admonition and checks
  the `previewEditOpen` lines of the item; another walks on into a nested sub-list item; Enter on
  the selected admonition still opens 70 to 75. Markers `@tests_req SwRS-MDOKFSTUDIO-BLOCK-254#S5`.
- `test/page/blockReq.requirements.test.ts` (or the hover tests of BLOCK-017 wherever they are):
  the hover outline over a body paragraph of an `aside.admonition` is the paragraph, over its
  title the admonition. Marker `@tests_req SwRS-MDOKFSTUDIO-BLOCK-017#S2`.
- The chord (section 2), `test/page/runtimeBlockMoves.test.ts` (or the block editor tests that hold
  BLOCK-130 S6 and S7 today), marker `@tests_req SwRS-MDOKFSTUDIO-BLOCK-130#S8`: from an item
  editor of a list in an `aside.admonition` (and in a `data-okf-github-alert`), the chord posts
  `previewBlockMove` with the lines of the inner list and of its inner neighbour, not of the
  admonition; with a nested sub-list item, the outermost body list; the first or last body block
  posts nothing and the editor stays open; a list in an inner admonition takes its neighbour in the
  inner admonition; after the rendered move, the list's editor opens at its new lines with the
  caret offset (the settle finds an inner block). With unsaved text: the save is posted first and
  no move yet; then, after the save renders (the pending navigation resumes through
  `resumePendingBlockNavigation` and `requestBlockMove`), `previewBlockMove` is posted with the
  lines of the inner list and of its inner neighbour, and after that move renders the list's editor
  opens at its new lines with the caret offset. Each fails on origin/main (today the whole
  admonition, or nothing, is sent; on the save path the editor reopens with no move).
- The planner (section 2), `test/core/mapping/blockMove.test.ts`, marker
  `@tests_req SwRS-MDOKFSTUDIO-BLOCK-117#S7`: two blocks of an alert body swap with their `>`
  separator kept; the same in an alert indented in a list item (`   > `); a swap that needs an
  added separator writes the prefix; blocks under different prefixes are refused; a swap of two
  blocks of a colon-fence and a backtick-fence admonition body, also next to the fences (blank line
  added, BLOCK-117 S4). The alert cases fail on origin/main (refused today).
- The edge keys (section 3), the tests of BLOCK-079 S6 (`test/page/runtimeStructuralNavigation.test.ts`
  or the block editor navigation tests that hold S6 today), marker
  `@tests_req SwRS-MDOKFSTUDIO-BLOCK-079#S6`: Down at the end of the last item's editor (and Up at
  the start of the first) of a list in an admonition, and of a nested sub-list's last item, keeps
  the editor open and posts no save; Down between items still opens the next item; a list outside
  an admonition still opens the next top-level block. The first fails on origin/main.
- Visual scenarios in `test/visual/alertEditingScenarios.ts` (Chromium, real clicks and keys):
  `gfm/v09-alert-body-opens-whole-alert-dark-900` and
  `block-editing/v22-admonition-body-opens-whole-directive-dark-900` are replaced (new ids that
  say the new behaviour, for example `...-body-opens-pointed-paragraph-...`): a click on the
  second paragraph opens that paragraph only (`previewEditOpen` lines and editor text of the
  paragraph, `> The second paragraph of the note.` for the alert), the admonition stays rendered
  around the hidden paragraph; one more scenario per kind, a click on the title opens the whole
  admonition with the editor texts the current scenarios assert. One keyboard scenario: Down to
  the admonition, Right, Down, Right, Enter opens the first list item only. The file's header
  comment is updated.
- `test/visual/scenarioIds.ts` holds the description of each visual id: the entries
  `gfm/v09-alert-body-opens-whole-alert-dark-900` (about line 705) and
  `block-editing/v22-admonition-body-opens-whole-directive-dark-900` (about line 728) move to the
  new ids with texts that say the new behaviour (a click on the second paragraph opens that
  paragraph only), and the new title and keyboard scenarios get their entries.
- Visual scenarios that open an admonition by a click on its body to reach its head line: in
  `test/visual/admonitionTypePickerScenarios.ts`, `palette-slash/v36` to `v39` (the
  `OPEN_ON_TYPE` helper, marker `SwRS-MDOKFSTUDIO-PALETTE-269#S1`, called on
  `aside.admonition.note > p:last-child`), and in `test/visual/releaseShowcaseScenarios.ts`
  `rendering-core/v27-release-1-3-showcase-cream-1200` (same target, then ArrowUp and ArrowLeft).
  They rely on the whole admonition opening so that ArrowUp reaches `> [!NOTE]` or `:::{note}`;
  after the change that click opens the paragraph only. They now open the admonition by a click
  on its `.admonition-title` (`aside.admonition.note > .admonition-title`), with the caret moves
  adjusted so the caret still lands on the last letter of the type, and the comments next to
  `OPEN_ON_TYPE` and in the showcase scenario ("The click lands mid-way along the ... body, so
  ArrowUp ...") rewritten to the new gesture. Their screenshots and assertions stay the same (the
  type list at the caret); the intent of no assertion changes.
- `test/integration/realInput/qa210Replays.ts`, `scenarioAlertLazyContinuation` (about lines
  132-158, markers GFM-009 `#S1` and `#S10`, runs on push to main or a heavy run): it clicks the
  alert's body paragraph ("Line one") and asserts an editor holding `> [!NOTE]` and the lazy line,
  so it fails after the change (the paragraph editor holds the lazy line but not the marker line).
  Its intent, stated in its doc comment, is that the lazy line renders inside the alert and that
  the editor opened from the alert holds it. Either it opens the alert from its title
  (`.admonition-title` of the alert) and keeps its assertions, or it keeps the body click and
  asserts the paragraph-only editor (the lazy line and the paragraph's own `> ` lines, no
  `> [!NOTE]`); the Driver picks one and the commit says why the gesture or the assertion changed.
- Checked on origin/main and still valid after the change, no edit needed beyond wording:
  - `scenarioCrlfAlertEditKeepsLineEndings` in the same file (about line 448) clicks the body
    paragraph of a one-paragraph alert, presses End, types, Enter, types; its assertions (CRLF in
    the buffer, `(?:> ?)?` before the new line, the alert renders the new line, one editor open)
    hold for the paragraph editor too; its message "the alert editor is still open" may be reworded.
    The Driver confirms it on the heavy run.
  - `test/visual/capture_edit_checks.py`, edit target `admonition`: it clicks "Calibration gate",
    the title of the `{warning}` of fixture 08-okf-schema, so the whole directive still opens and
    its "both fences" check holds.
  - `test/page/runtimeBlankLinesContainers.test.ts` ("a click on a blank-line block in an
    admonition, a panel and an alert opens its own editor"), `test/visual/capture_table_in_container.py`
    and `test/integration/realInput/tableInContainer.ts` (a table in an alert or an admonition opens
    the cell editor) already expect the inner element.
  - No other test under `test/` or the clips clicks, or presses Enter on, the body of an
    admonition or an alert to open it whole (searched for admonition and alert selectors followed by
    a body element, `editingElementFor` and `sourceRangeForAlert`); the keyboard navigation clip is
    section 6.
- Real VS Code window (push to main only): `test/integration/listItemMoves.ts` holds "the
  whole-list chord of an item editor" (BLOCK-262 Verification notes); a step with the chord from an
  item of a list in an alert, checking the file, is the Driver's call. A step in
  `test/integration/realInput/blockKeys.ts` doing the keyboard walk into an admonition item is
  optional too. The re-filmed clip (section 6) runs this path in a real window in any case.
- Every test above fails on origin/main where the behaviour changes (constitution, section 3).

### 6. The keyboard navigation clip and the user guide (answers 7 and 9)

The clip `docs/demo-video/clips/keyboard-navigation/` is re-filmed in this pull request, per
`docs/demo-video/guidelines/feature-clip-process.guidelines.md` (a changed action means a new
take): one continuous shot, keyboard only, the pointer parked, on Windows, from a VSIX built from
the branch (`just clip keyboard-navigation all --vsix <path>`, then `render` and `check`). No
second clip (answer 9). The stage file `stage/release-plan.md` stays as it is (a colon-fence
`:::{note} Before the release`, a sentence, a list whose second item "Build the packages" holds the
sub-list "the VSIX", "the docs site", then "Post the announcement").

**The key path**, read from the structural cursor on origin/main (`structuralMove` in
`src/page/modules/structuralCursor.ts`: Right goes to the first selectable mapped child, Up and
Down move among siblings and stop at the edges; the children are `rt.blocks.mappedChildren`, in
`structuralNavigationView.ts`):

1. Scene 1, unchanged: `E` (edit mode on), Down (the heading), Down (the admonition), Enter (the
   whole admonition opens, `:::{note} Before the release` to `:::`), Escape (closed, still
   selected). This keeps answer 1 on screen: the admonition selected whole opens whole.
2. Scene 2, longer: Right (the sentence), Down (the list), Right (the first item), Down (the
   second item "Build the packages"), Right (the first mapped child of that item), then down to
   the sub-list and Right into it (its first item, "the VSIX"). Whether the second item's first
   mapped child is its own text (a `p`, as a tight item renders it, see "a paragraph of a tight
   item keeps its wrapped line" in `test/session/listItemEditOpen.test.ts`) or the nested `ul`
   directly decides whether one Down sits between them: expected path "Right, Down, Right"
   (paragraph, sub-list, "the VSIX"), else "Right, Right". The Driver confirms it with the page
   test of section 5 (the walk into a nested sub-list item) before the take, and the clip films
   what that test shows; each press is checked in the scenario.
3. Scene 3: Enter on "the VSIX" opens that item alone (`previewEditOpen` of its one line, the
   editor text `  - the VSIX`, with its indentation as in the file, the caret at its end after
   "VSIX", by `focusTextControlAtLastContent`): no caret walk is needed any more. Ctrl+Backspace
   (Option+Backspace on macOS) deletes "VSIX"; "extension" is typed (no badge); Ctrl/Cmd+Enter
   saves. The item reads "the extension"; nothing else changes. Mark 1 around the saved sub-item.
   The word is the Driver's to adjust in the storyboard if a better one fits ("one word changes"
   is the owner's requirement); the target is the first sub-item to keep the clip short.

That is 15 presses (16 with the extra Down), the same seven badge kinds as today (`E`, `↓`,
`Enter / ↩`, `Esc`, `→`, `Ctrl+⌫ / ⌥⌫`, `Ctrl+Enter / ⌘↩`): no new badge.

**Length and budget.** The kit allows 5 to 30 s (`Length` row; `storyboard.test.mjs` asserts
`> 12 && <= 30`). At the current spacing (presses 1.6 s apart, a badge shows 1.2 s and fades over
0.33 s) plus the typed word and Mark 1, the clip runs about 27 to 29 s; the Driver may tighten the
spacing to about 1.5 s if the badges still do not overlap (`validateStory`). It must stay at most
30 s with every press of the path; if it cannot, stop and report (shortening the story is the
owner's choice, not the Driver's). The GIF budget is 3 MB (MP4 10 MB, WebM 3 MB); the take at
20 s gave a 1.68 MB GIF at step 0, so about 2.3 to 2.5 MB is expected at 28 s; over 3 MB, the kit's
ladder applies and `check.json` reports the step. The "Length" review note says why the clip needs
more than 12 s (the extra level of the sub-list).

**`clip.md`** (the live storyboard):
- header paragraph: the number of presses and the story (down to a sub-item);
- `## Clip`: `Length`, the `Stage` description unchanged;
- scene 2: `Time`, `Shot` (the walk down to "the VSIX"), Pictures (new frames: the second item
  selected, the sub-list selected, the sub-item selected); the zoom stays on the admonition, its
  hold moved to the new end;
- scene 3: `Time`, `Shot` (Enter opens "the VSIX" alone, caret at its end, word deleted and
  typed, saved), Pictures (the sub-item in its editor, the word changed, Mark 1), `Mark 1` times;
  the captions keep their text ("Press E, then the arrows pick a block", "Right goes one level
  deeper", "Change a word and save, no mouse at all") unless the Driver has a reason, which the
  storyboard test then follows;
- "Expected result": the selected element after each press (heading, admonition, the admonition
  editor, the admonition, sentence, list, first item, second item, [its text,] sub-list, "the
  VSIX"), then a block editor holding `  - the VSIX` alone, then after the save the sub-item reads
  "the extension" and `release-plan.md` on disk is the stage with that one word changed;
- review notes: remove "Deviation: Enter on the selected item opens the whole admonition editor"
  and rewrite "Changing one word" (no caret walk; the item editor opens on the sub-item's line);
  "What Right selects" covers the walk into the sub-list; "Length" and the take facts (VS Code and
  extension versions, raw frames, sizes) come from the new take; the note on the `⌥` badge stays.

**`scenario.mjs`**: the header comments (lines 2-5, "Enter opens the whole admonition ... the caret
goes to the end of 'Friday'"), the steps from 9 on (the walk into the sub-list, each press checked
with `expectState`; Enter checked on an editor whose value is the sub-item's line; no caret walk),
`EXPECTED = STAGE.replace("  - the VSIX", "  - the extension")`, the mark on the saved sub-item,
and the notes it returns.

**Storyboard tests**, kept passing with `just clip-kit-test`:
- `docs/demo-video/clip-kit/lib/storyboard.test.mjs`, "the shipped keyboard-navigation clip.md
  reads as the clip the owner reviews" (about line 825): the `ids` array of presses becomes the
  new path (`edit, down, down, enter, escape, right, down, right, down, right, [down,] right,
  enter, delete-word, save`), the `filmed` times and the zoom time follow the storyboard; the length
  bound, the badges map, the zoom id and the single mark stay; the macOS refusal of the `⌥` badge
  stays as it is. "the stage of the keyboard-navigation scenario is the shipped stage file, and the
  save changes one word" (about line 866): "Friday occurs once" becomes the sub-item occurring
  once, the changed line is `[8]`, `before[7]` is `  - the VSIX`, `after[7]` is `  - the extension`.
- `docs/demo-video/clip-kit/lib/check.test.mjs` (about line 93): the keyboard-navigation checks
  stay `{ editMode: "off", paste: false }`; no change expected.

**Outputs**: the frames, `check.json`, contact sheet, first and last frames, poster, MP4, WebM and
GIF are replaced by the new take's (Git LFS).

**The user guide** `docs/user/editing.md`:
- "Inline editing" (about line 46, "A click on a list item edits that item only..."): a click in
  the body of an admonition or an alert edits the pointed paragraph or item; its title or frame
  edits the whole admonition;
- the keyboard paragraph (about lines 124-130): Enter on an admonition opens it whole, and on an
  element reached with the arrows opens that element only, also inside an admonition; in the
  editor of an item of a list inside an admonition, Down at the end of the last item and Up at the
  start of the first keep the caret, and Cmd+Alt+Up/Down (Ctrl+Alt elsewhere) moves that list
  among the admonition's blocks;
- the GIF alt text (line 132) follows the new clip, for example: "In edit mode, from the keyboard
  only: E turns edit mode on, Down selects a note admonition, Enter opens it whole and Escape
  closes it, Right goes inside it, Down reaches its list, the arrows go down to an item of a nested
  sub-list, Enter opens that item alone, one word is changed and Ctrl+Enter saves".

### 7. CHANGELOG

One line under `## Unreleased` in `CHANGELOG.md`, per "CHANGELOG line" of
`.agents/guidelines/pull-request.guidelines.md`, for example: "In edit mode, Enter on an element
reached with the arrows inside an admonition or a GitHub alert, and a click on one, now open that
element only (the title or the frame opens the admonition whole); in an item editor there, the move
chord moves the list inside the admonition and Down or Up at its edge keeps the caret (CR-<n>
enter-admonition, PR #<n>)".

## Decisions carried from `02-answers.md`

- Answer 1: an admonition selected entirely (as the keyboard gives it) opens whole with Enter;
  with the arrows the writer goes down into its elements and Enter opens only the selected one;
  pointing with the mouse selects the element to open directly. Sections 1, 4 (BLOCK-254), 5.
- Answer 2: specified for batch-09; the mouse was asked again (answers 3 and 4).
- Answer 3: a click in the body opens the pointed list item or paragraph; the title or the frame
  opens the whole admonition; GitHub alerts included. Sections 1, 4 (BLOCK-014, BLOCK-017), 5.
- Answer 4: grilled enough, specified for batch-09.
- Answer 5 (B): from the editor of a list item inside an admonition or alert, the move chord moves
  that list inside the admonition, not the whole admonition. Sections 2, 4 (BLOCK-130, BLOCK-117,
  BLOCK-262), 5.
- Answer 6 (A): Down at the end of the last item, Up at the start of the first, of such a list keep
  the caret in the editor. Sections 3, 4 (BLOCK-079), 5.
- Answer 7 (B): this change re-films the keyboard navigation clip and keeps the user guide in
  step. Section 6.
- Answer 8 (A): a block of a GitHub alert body opens with its `> ` markers. Section 1.
- Answer 9 (A): the re-filmed clip goes down, keyboard only, to an item of the nested sub-list,
  opens that item alone, changes a word and saves; no second clip. Section 6.
- The inbox anomalies join batch-09 and ship in the next release (owner, 2026-11-26).

## Out of scope

- Editing a block of an alert body without its `> ` markers (answer 8).
- Cards, tabs, grids, block quotes and context-tag panels: no behaviour change intended; only
  their wording in BLOCK-254 is checked against the code.
- Opening the editor on the title line alone.
- The chord from an editor that is not a list item's (a paragraph, the list itself, a block inside
  an item) inside an admonition: unchanged by this specification (open questions 1 and 2).
- Lists outside admonitions: their chord and edge keys are unchanged.
- The writing skill: no rendered syntax changes.

## Evidence

- `just check`, `just clip-kit-test` and `just requirements-lint` pass; `just requirements-update`
  run and its files committed; `just preflight` passes (on Windows the static stage; CI runs the
  visual stage, which holds the new visual scenarios).
- The unit, page and core tests of section 5 fail on origin/main and pass on the branch (name the
  failing assertions in the PR body).
- The re-filmed clip: `check.json` passed, its length (at most 30 s) and GIF size (at most 3 MB,
  ladder step named) quoted in the PR body, the GIF shown in the PR body; the contact sheet shows
  each selection of the path, the sub-item alone in its editor and Mark 1 on "the extension".
- Scenario steps, in a Studio preview in edit mode, on a page with a `:::{note}` holding a
  sentence and a list of three items (the second with two sub-items) then a sentence, and a
  `> [!TIP]` alert holding two paragraphs and a list:
  1. Down until the note is selected, Enter: the whole note opens (opening to closing fence).
     Escape.
  2. Right, Down, Right, Enter: only the first item opens. Escape. Walk on to the first sub-item,
     Enter: only that sub-item opens, on its one line.
  3. In the first item's editor, Up at its start: the caret stays. In the last item's editor, Down
     at its end: the caret stays. In the last sub-item's editor, Down at its end: the caret stays.
  4. In an item's editor, Ctrl+Alt+Down (Cmd+Alt on macOS): the list and the sentence after it
     swap inside the note, the list's editor opens at its new place; Ctrl+Alt+Down again: nothing
     happens (last block of the body). Ctrl+Alt+Up twice: back in place, then nothing.
  5. Click the sentence of the note: only the sentence opens. Click the second item: only that
     item opens. Click the title "Note": the whole note opens. Click the padding of the frame:
     the whole note opens.
  6. Same on the alert: a paragraph opens alone with its `> ` marker, an item opens alone, the
     title opens the alert from `> [!TIP]` to its last quoted line; in an item's editor, the chord
     swaps the list with a paragraph and every line keeps its `> `.
  7. Hover the sentence: only the sentence is outlined; hover the title: the whole note is
     outlined.
- No host or setting dependency: no host and default matrix.

## Open questions

1. The chord from the editor of a paragraph (or any non-list block) of an admonition body moves
   nothing today (`bodyBlockNeighbour` finds no top-level neighbour for it, BLOCK-130 S7 "the key
   is consumed"). Answer 5 covers the list item editor only. Should it also move that block among
   the admonition's blocks, which the section 2 machinery would allow at little cost, or stay as it
   is?
2. The same for the editor of the list itself (opened by Enter on the selected list) and of a block
   inside an item, inside an admonition: today they move nothing either. Same choice as question 1.
3. When the host refuses an inner move (for example text between the two blocks), the reason is
   shown today next to the "+" insert point of the moved top-level block (BLOCK-109); inner blocks
   have no insert point bar. Where should the reason show: next to the admonition's insert point,
   a short message in the editor, or nowhere (the key is consumed and nothing moves)? This
   specification does not decide it.
