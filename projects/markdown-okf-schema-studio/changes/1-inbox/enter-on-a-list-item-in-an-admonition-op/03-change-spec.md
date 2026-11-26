# Enter and click in an admonition open the selected element

In the Studio preview, in edit mode, an admonition (a MyST `{note}`-style directive, backtick or
colon fence, a `:class: dropdown` included) or a GitHub alert (`> [!NOTE]`) opens today as one
block, whatever the writer aims at: Enter on a list item or a paragraph reached with the arrows
opens the whole admonition, and so does a click in its body. After this change, the whole
admonition opens only when the admonition itself is selected or pointed at (keyboard selection of
the admonition, or a click on its title or its frame); otherwise exactly the element reached with
the arrows, or the element under the pointer, opens.

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
go through it. The keys of the editor that then opens are not decided there: what they do from
the editor of an item inside an admonition is open question 2, and this change does not alter
them. As a consequence of the new rule, which the requirements below record:

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
quote today. See open question 1.

### 2. Requirements (`requirements/tiers/`)

All touched requirements are `proposed`; none is `approved`, so no owner approval is needed. The
approved StRS-MDOKFSTUDIO-BLOCK-003 is not changed (its path "the writer clicks a rendered block
and its editor opens with the lines of the block" still holds); if the Driver finds it must
change, stop and report, per "Approved requirements" of
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
    whose body holds a paragraph and a list of items; WHEN the writer presses Enter; or
    ArrowRight, then Enter; or ArrowRight, ArrowDown, ArrowRight, then Enter; or the same, then
    ArrowLeft twice, then Enter; THEN Enter on the admonition opens the whole admonition, Enter on
    its paragraph opens the paragraph only, Enter on the first item opens that item only, and
    back on the admonition Enter opens it whole again; with the lines of each.
  - The S3 sentence "A click on a list item opens the item, not the block under the click
    (BLOCK-014): only the keyboard reaches a block inside an item" stays.
- **SwRS-MDOKFSTUDIO-BLOCK-004**: unchanged (Enter on a selected top-level block opens that block).
  Checked: its text does not contradict the new rule.
- **SwRS-MDOKFSTUDIO-BLOCK-017** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-017.md`): S2 gets
  two rows: "a paragraph or a list item in the body of an admonition or an alert": the pointed
  paragraph or item; "the title or the frame of an admonition or an alert": the whole admonition.
- **SwRS-MDOKFSTUDIO-BLOCK-262** (`swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-262.md`): S5 row
  "A click on an item of a list in an alert or an admonition | The whole container opens in its
  editor, as before (SwRS-MDOKFSTUDIO-BLOCK-014)" becomes: the clicked item opens in its editor;
  a click on the title or the frame of the alert or admonition opens the whole container
  (SwRS-MDOKFSTUDIO-BLOCK-014). The Related requirements line "SwRS-MDOKFSTUDIO-BLOCK-014: a
  click on a list item edits that item; in an alert or an admonition, the whole container"
  becomes: a click on a list item edits that item, also in an alert or an admonition, whose title
  or frame edits the whole container.
- **SwRS-MDOKFSTUDIO-GFM-009**: no normative change. Its comments in `mystNormalize.ts` and
  `mystGithubAlerts.ts` are reworded (section 1).
- `just requirements-update`, then a dated `## 2026-11-26` (or the day of the change) entry in
  `requirements/tiers/log.md`, sub-heading `### Enter and click in an admonition open the selected element`,
  naming the reversal of the 2026-10-29 entry "A click in the body of a GitHub alert opens the
  whole alert" and the owner's answers of 2026-11-26.

### 3. Tests

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
    admonition and a GitHub alert, the admonition opens whole, its paragraph, its list, its item
    and a block of its item each open on their own lines.
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
  the `previewEditOpen` lines of the item; Enter on the selected admonition still opens 70 to 75.
  Markers `@tests_req SwRS-MDOKFSTUDIO-BLOCK-254#S5`.
- `test/page/blockReq.requirements.test.ts` (or the hover tests of BLOCK-017 wherever they are):
  the hover outline over a body paragraph of an `aside.admonition` is the paragraph, over its
  title the admonition. Marker `@tests_req SwRS-MDOKFSTUDIO-BLOCK-017#S2`.
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
- Real VS Code window (optional, the Driver's call): a step in
  `test/integration/realInput/blockKeys.ts` doing the same keyboard walk into an admonition item
  (runs on push to main only).
- Every test above fails on origin/main where the behaviour changes (constitution, section 3).

### 4. CHANGELOG

One line under `## Unreleased` in `CHANGELOG.md`, per "CHANGELOG line" of
`.agents/guidelines/pull-request.guidelines.md`, for example: "In edit mode, Enter on a list item
or a paragraph reached with the arrows inside an admonition or a GitHub alert, and a click on one,
now open that element only; the title or the frame of the admonition opens it whole (CR-<n>
enter-admonition, PR #<n>)".

## Decisions carried from `02-answers.md`

- Answer 1: an admonition selected entirely (as the keyboard gives it) opens whole with Enter;
  with the arrows the writer goes down into its elements and Enter opens only the selected one;
  pointing with the mouse selects the element to open directly. Sections 1, 2 (BLOCK-254), 3.
- Answer 2: specified for batch-09; the mouse was asked again (answers 3 and 4).
- Answer 3: a click in the body opens the pointed list item or paragraph; the title or the frame
  opens the whole admonition; GitHub alerts included. Sections 1, 2 (BLOCK-014, BLOCK-017), 3.
- Answer 4: grilled enough, specified for batch-09.
- The inbox anomalies join batch-09 and ship in the next release (owner, 2026-11-26).

## Out of scope

- Editing a block of an alert body without its `> ` markers (open question 1).
- Cards, tabs, grids, block quotes and context-tag panels: no behaviour change intended; only
  their wording in BLOCK-254 is checked against the code.
- Opening the editor on the title line alone.
- The keyboard navigation clip and the user guide: what this change does about them is open
  question 3; this specification does not decide it.
- The keys of an item editor inside an admonition (chord move, Down past the last item): open
  question 2; unchanged by this specification.
- The writing skill: no rendered syntax changes.

## Evidence

- `just check` and `just requirements-lint` pass; `just requirements-update` run and its files
  committed; `just preflight` passes (on Windows the static stage; CI runs the visual stage, which
  holds the new visual scenarios).
- The unit and session tests of section 3 fail on origin/main and pass on the branch (name the
  failing assertion in the PR body).
- Scenario steps, in a Studio preview in edit mode, on a page with a `:::{note}` holding a
  sentence and a list of three items, and a `> [!TIP]` alert holding two paragraphs and a list:
  1. Down until the note is selected, Enter: the whole note opens (opening to closing fence).
     Escape.
  2. Right, Down, Right, Enter: only the first item opens. Escape. Right on it, Enter: its first
     block opens alone.
  3. Click the sentence of the note: only the sentence opens. Click the second item: only that
     item opens. Click the title "Note": the whole note opens. Click the padding of the frame:
     the whole note opens.
  4. Same three steps on the alert: a paragraph opens alone with its `> ` marker, an item opens
     alone, the title opens the alert from `> [!TIP]` to its last quoted line.
  5. Hover the sentence: only the sentence is outlined; hover the title: the whole note is
     outlined.
- No host or setting dependency: no host and default matrix.

## Open questions

1. A block of a GitHub alert body opens with its `> ` quote markers in the editor (the lines as
   in the file, like a block of a plain block quote today). Is that acceptable, or should the
   editor hide the markers and put them back on save? This specification assumes the markers stay
   (no new mechanism); a change would be a further CR.
2. After a click (or Enter) opens one list item inside an admonition, the editor's keys act on
   the top-level block, not on the admonition's inside: Cmd/Ctrl+Alt+Up/Down from that item
   editor saves the item and moves the whole admonition (`moveBlockFromEditor` uses
   `topLevelBlockOf` in `src/page/features/blockEditor.ts`, for an `LI` target), and Down at the
   end of the last item (Up at the start of the first) leaves the admonition for the block after
   (before) it (`adjacentMappedBlock`, same file, steps past `topLevelBlockOf(item)`). Today this
   was hardly reachable, since an item in an admonition never opened alone. Keep it as is, or
   should the chord move only the list inside the admonition and Down stop at the admonition's
   edge (a further change to SwRS-MDOKFSTUDIO-BLOCK-130 and SwRS-MDOKFSTUDIO-BLOCK-079)?
3. The keyboard navigation clip (CR-501, merged in PR #522) films the old behaviour:
   `docs/demo-video/clips/keyboard-navigation/clip.md` (lines 68-129: "Enter on the item opens the
   whole admonition in its editor", the caret walked Up five times inside the whole admonition
   source, and the checks that follow), its `scenario.mjs`, frames and GIF; and the user guide
   `docs/user/editing.md` (around lines 126-132) shows that GIF with the alt text "Right selects
   the first item, Enter opens the admonition editor". Should this change re-film the clip and
   update the guide in the same pull request, update only the guide's text and alt text and leave
   the re-filming to a new CR, or leave both to a new CR?
