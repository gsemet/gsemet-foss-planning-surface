Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: table-editing StRS and SwRS

Scope `table-editing`: 15 StRS, 120 SwRS (TABLE), reviewed against `inventory/table-editing.md`, the
sources and tests of `markdown-okf-schema-studio-wt-059-b3` (`src/page/modules/markdownTable.ts`,
`tableEditActions.ts`, `src/page/features/tableCellEditor.ts`, `blockEditor.ts`, `blockSourceEditor.ts`,
`editMode.ts`, `pageInput.ts`, `editModeStyles.ts`, `editPaletteStyles.ts`, `paletteActions.ts`), the
defect classes of `reviews/layout-width-swrs.md` and `reviews/frontmatter-editing-swrs.md`, and the
already written `requirements/tiers/swrs/block-editing`. Read-only; no lint, no build, no test run.
One throw-away `markdown-it.render` call (no repo file touched) settled SwRS-104.

Verdict: REVISE

## What passed

- Structure: 120 SwRS and 15 StRS, all `draft`, `derives_from` / `derived_by` consistent both ways
  (script check: 0 mismatches). Every heading equals its title, every description equals its
  Normative behavior paragraph, every SwRS has exactly two scenarios, no leftover placeholder
  (the "TODO" in SwRS-090 is the real action name). No requirement text names a backlog item or an
  inventory id.
- Coverage: F-TABLE-001..054 are all mapped except the two gaps listed in defect 15.
- Spot-read against the code: about 85 of the 120 SwRS (about 70 percent), all 9 Known issues.
- Numbers and texts verified in the code: 400 ms (`AUTOSAVE_DELAY_MS`), 500 ms pointer window,
  40 percent bar limit, 4 px gap of `stickyBarShift`, 2 px status centring, 2 px selected-cell outline,
  grid 1..9 (`/^([1-9])x([1-9])$/`), delimiter rule `/^:?-{3,}:?$/`, five bar buttons with labels
  "Row +", "Row −", "Col +", "Col −", "List table" and their titles, status strings
  "Header · column N of M" / "Row R of T · column N of M", Done / Cancel accessible names,
  "Loading Markdown table source…", "Raw Markdown editor" / "Raw Markdown block", refusal sentences
  ("Nothing was changed.", "A pipe table has one header row; this table has N.", "This is already a
  pipe table."), fence length rule, the nine-table corpus, palette modes (table strict, htmlTable and
  columnAlign gfm, tableCaption / listTable / pipeTable myst), cell scope of the inline group.
- Known issues confirmed true: 062 (column buttons set `columnsChanged`, `serialize` rewrites every
  line), 093 (no paste handler on the cell textarea, `serialize` keeps the line break), 116 (the
  action falls to `insertBlockAt` at `selectionEnd`, which can split a `{list-table}` or HTML table),
  050 (the "four-action" text is in `scenarioIds.ts` for v02 to v05), 072 (the refusal branch cannot
  run for a table that parses), 034 (the first half: `openMappedEditor` returns on `!edit.tableModel`).
- SwRS-104 Known issue is true and precise. `markdown-it` 14.3.3 is the only copy in the lock file
  (`myst-parser` hoists to it) and its `escapedSplit` has no code-span rule. Rendering
  `| a | b |` / `| --- | --- |` / ``| `x|y` | z |`` gives the two cells "`x" and "y`" and drops z;
  the editor's `splitRow` keeps ``x|y`` in one cell, so a click on the second rendered cell opens z.
- The "untested" claims I probed are honest: 002, 012, 020, 033, 060 (button state), 065 (tall
  bar), 071, 072, 078, 093, 120 have no test; the cited tests for the rest exist (every quoted test
  title was matched in the cited file, except those named in defect 13).

## Defects (17)

1. SwRS-034, three defects in one requirement.
   - Bundled: one SHALL carries three outcomes (show the message, drop the pending navigation, let the
     writer keep editing after a refused save). Fix: split into "A refusal message is shown in the
     cell editor status" and "A refused save drops the pending navigation and keeps the typed text".
   - Overclaimed verification: the cited test (`table editing switches cells without losing changes
     and finalizes before leaving the table`, lines 500-525) asserts only that `pendingBlockNavigation`
     is cleared and that editing continues; it never reads the status text or the text box value after
     the error. Criteria "The status text equals the host message" is read from
     `blockSourceEditor.ts:receiveBlockEditSource` (`edit.status.textContent = message.error`), not
     tested. Fix: say so.
   - Known issue incomplete and it duplicates SwRS-MDOKFSTUDIO-BLOCK-216 (refused open). "Until Escape
     closes it" is not the only exit: edit mode off (`applyEditMode` calls `closeBlockEdit(false)` when
     `originalText` is unset) and a content patch also close it; there is no Done or Cancel button
     and Refresh stays disabled (`openBlockEditor`). Fix: reduce the Known issue to the table-cell
     facts (message in the region, content stays hidden, clicks on any cell or block ignored because
     `!edit.tableModel`) and cite BLOCK-216 for the rest.
   - Description says "the status of the cell editor", scenario 1 says "the bar status": say "the
     status line of the editor (in the table bar once the text box exists)".

2. SwRS-104. The Known issue is right (see "What passed") but the requirement is inconsistent.
   Scenario 2 "Renderer" asserts a rendering behaviour that the normative paragraph does not cover and
   no test checks (rendering belongs to the gfm / myst scopes). Criteria says "the renderer difference
   is the known issue below", but the Known issues section is above Verification notes. Fix: delete
   scenario 2 and replace it by a boundary of the editor (a code span with a closing run of a
   different length, ``` ``a|b` ```: the pipe splits, `splitRow` closes only on an equal run); keep the
   renderer fact in the Known issue; state in Verification notes "renderer difference checked with
   markdown-it 14.3.3, no test"; replace "below" by "above".

3. SwRS-084. The Normative text is false for most tables: "a pipe table without alignment colons ...
   converted to a list-table and back ... SHALL give the original table text". `gridToPipe` writes the
   canonical `| a | b |` with `---` delimiters, so a padded, compact, indented or long-dash table does
   not come back byte for byte (`markdownTable.ts:gridToPipe`). The test
   (`pipe -> list-table -> pipe is lossless for simple tables`, listTable.test.ts:36-54) only uses
   canonical sources. Fix: restrict to "a pipe table written in the canonical style (`| a | b |`,
   `---` delimiters)" and add the loss (padding, indentation, delimiter width) to scenario 2 or to a
   Known issue; rename the heading accordingly.

4. SwRS-092. Wrong evidence. The second cited test, `T34: color works in a table cell without escaping
   the pipes` (editActions.test.ts:1197), asserts that the colour action itself leaves `f|oo`
   unescaped; the escaping lives in `textEditing.ts:cellSafeEdit`, called from
   `textControls.ts:applyTextEdit`. The only escape evidence is the `T35` link test. Also unstated: the
   function escapes every unescaped pipe, code span included (unlike SwRS-091), and "colour" in the
   SHALL has no test. Fix: drop the T34 citation, add "also inside a code span of the inserted text"
   to scenario 1, and say colour is untested.

5. SwRS-063 and SwRS-088, wrong cause. The text says the popover closes "because the whole bar is
   rebuilt" and 088 says "the same cell group in the new bar". The bar element is reused:
   `renderTableCellEditor` does `const menu = edit.tableMenu || ...; menu.textContent = ""` and refills
   it. The popover and the link panel close because `renderTableCellEditor` starts with
   `edit.closeLinkPanel?.(false); edit.cellPalette?.closePopover(); edit.cellSlash?.close();`, and that
   function also runs on every cell switch (`switchTableCell`: Tab, arrows, click), so the behaviour
   is wider than "a row or column button" and no SwRS states it. Fix: 063 Known issue "renderTableCellEditor
   closes the popover, the link panel and the slash menu every time the editor is rendered: after a row
   or column button and after every move to another cell"; add the cell-switch case to scenario 2 or a
   new SwRS; 088 normative "refill the same bar with the same cell group". (Inventory F-TABLE-051 calls
   it "kept"; if the owner keeps it, say "by design" and drop the Known issue label.)

6. SwRS-051. "Draw a thin rule before the column group and before the table group" is not what the CSS
   does. `editModeStyles.ts:353-366` matches every button carrying `data-sphinx-table-group="column"`
   or `"table"` (the attribute is set on each button, there is no group element), so a rule is drawn
   before Col + and before Col − (and before List table). Fix: either state the real behaviour ("a thin
   rule before each of Col +, Col − and List table, none before the row buttons") with a Known issue
   "the rule also separates Col + from Col −", or have the CSS fixed in the backlog; check
   `table-editing/v02` once by eye before choosing.

7. SwRS-072. Awkward description ("When the table text of the bar's List table button is refused by
   the conversion"). Proposed wording, same for title scenario 1 and the Normative paragraph: "When the
   conversion behind the table bar's List table button refuses the table, the extension SHALL show the
   refusal reason in the bar status and save nothing." Also add the third outcome the handler has
   (`else if (converted)`): when `convertTable` returns undefined, the button does nothing at all (see
   defect 8). Keep the Known issue.

8. SwRS-093 (and SwRS-070), missed consequence. After a pasted line break the table text no longer
   parses (`parse` finds rows of different lengths), so `detectTable` returns undefined and
   `convertTable(serialize(model), "list-table")` returns undefined: the List table button silently does
   nothing (`tableCellEditor.ts`, handler of "Convert to list-table"). Fix: add to 093's Known issue:
   "while the pasted line break is in the cell, the List table button does nothing and shows no
   message", and cite it from 072.

9. SwRS-054 Known issue 1 and SwRS-050 Known issue are not behaviours. "No table-editing scenario has
   a width of 360 px" is a missing test, and the "four-action" wording is a stale description in
   `test/visual/scenarioIds.ts`. The guideline reserves "Known issue" for how the extension behaves.
   Fix: move both to Verification notes (SwRS-054 already says "No scenario is narrower than 460 px";
   scenario 2 of 054 is "not covered by any scenario", keep it as a boundary) and keep only the
   dangling separator as Known issue of 054 (true: the separator is `flex: none; align-self: stretch`).
   Same in StRS-008 ("no check exists for the bar in a 360 px pane").

10. Missed Known issues, same hazard as the confirmed SwRS-116.
    - SwRS-119: HTML table with the caret inside a `{list-table}` or inside an existing `<table>`:
      `htmlTable` finds no pipe table (`tableAtCaret`) and inserts a new 2 x 2 table at `selectionEnd`
      (`insertBlockAfterSelection`), splitting that table. Add the Known issue next to 116's.
    - SwRS-106 and 107: the Table action with the caret in a row of an existing table inserts the new
      table after the caret with `lead = "\n\n"`, which splits the existing table the same way; scenario 1
      of 107 shows the split only for a paragraph. Add a Known issue or a boundary scenario.

11. Bundled SHALLs (one SwRS, several behaviours). Split, or keep one outcome and give the other its own SwRS.
    - SwRS-036: Shift+Tab moves to the previous cell, and Shift+Tab in the first header cell does
      nothing. Split.
    - SwRS-053: centre the status vertically, and hide it when empty. Split.
    - SwRS-062: write every line canonically, and keep the alignment colons. Keep the colons in the
      scenario, drop them from the SHALL.
    - SwRS-075: offers List table, offers Pipe table, offers neither. One SwRS per action (the
      guidelines ask for one per palette action).
    - SwRS-079: refuses "already a pipe table" / "already a list-table", and returns nothing for a
      non-table. Split.
    - SwRS-082: drops colons going to a list-table, and writes them coming from HTML. Split by
      direction.
    - SwRS-087: the picker opens inside the viewport, and Escape closes only the picker. Split.
    - SwRS-088: moves the group into the rebuilt bar, and destroys it on close. Split.
    - SwRS-092: escapes pipes, and replaces line breaks. Split.
    - SwRS-033 (post the final save, and close without save when unchanged) and SwRS-066 (recompute on
      resize, and stop on close) have the same shape; split or accept as one lifecycle.

12. Duplicates of block-editing SwRS (cite by id, keep only what the cell does differently).
    - SwRS-029 (Escape during IME) = BLOCK-055.
    - SwRS-031 (host flush request, `previewEditFlushed`) = BLOCK-207; SwRS-030 (link / Back / Next saves
      first, flush flag) = BLOCK-211 and BLOCK-213. The only cell-specific code is the table branch
      of `flushOpenEditors` (it copies `tableInput.value` into the model first): keep that as the one SwRS.
    - SwRS-046 (handled keys stay in the page) = BLOCK-076 and BLOCK-077; the SwRS itself says "The
      policy is page-wide ... this requirement states the cell case".
    - SwRS-047 (select all) = BLOCK-078, same sentence in its Criteria.
    - SwRS-045 (undo / redo stay in the box) = BLOCK-074; SwRS-044 (marker wrapping) = BLOCK-069 and 070.
    - SwRS-025 to 027 (Escape / Cancel, previewEditCancel only after an autosave) = BLOCK-053 and 056;
      SwRS-013 (400 ms) = BLOCK-042 (the cell-specific part is "the whole serialised table").
    - SwRS-001 scenario 2 (properties table cell) = BLOCK-025.
    Fix: replace each by a one-line cross-reference in the rationale of the owning StRS, or keep one
    cell SwRS per behaviour that really differs (cell wording, model, caret positions).

13. Verification notes that name a test that does not show the claim.
    - SwRS-066: the Method says unit test `CR 034: the table toolbar rides down ...` covers resize and
      listener removal; that test only dispatches `scroll` (`scrollTo`) and never a `resize`, and never
      checks `removeEventListener`. Both are read from `syncTableMenuSticky` / `closeBlockEdit`: say
      "resize and removal untested".
    - SwRS-064 Criteria: "equals the stickyBarShift result" is not asserted; the test checks `> 0`, the
      stuck mark, "inside the viewport" and "not below the table end".
    - SwRS-038 (ArrowLeft / ArrowRight) cites the visual step `arrowdown` of v02, which is ArrowDown.
    - SwRS-114 cites "the choice checks of alignColumn": no test has that title; the assertions
      (`"justify"`, no choice) sit in `T26: columnAlign works from a body row, outside pipes and in
      tables without edge pipes` (editActions.test.ts:854-861).
    - SwRS-097 says "each cell of every corpus table": the test skips the delimiter row
      (`if (row === 1) continue`). Say "every header and body cell".
    - SwRS-110: the cited test (`T30: ref, doc, cite, dropdown, tableCaption and roleKbd are myst-only`)
      covers one of the six actions; the other five modes are read from `paletteActions.ts` only.

14. StRS rationale leaks implementation, numbers and test facts (guideline: no implementation detail, no
    message names, no pixel values). StRS-001 (file paths `src/page/features/...`, aria labels), StRS-002
    ("400 ms", "serialised table", "final save", "within 3 px"), StRS-004 and StRS-005 ("final save",
    "posted before the navigation message"), StRS-007 ("scroll assertions of the visual check bite on
    macOS only because a headless Linux browser..."), StRS-008 ("360 px pane", test gap, see defect 9),
    StRS-010 ("40 percent", "translated"), StRS-009 and 013 ("canonical style"). Fix: keep these in
    the SwRS, leave the StRS with the user-visible effect ("the table does not jump", "my text is kept").
    StRS-013 description also says "a writer or a reviewer saves": only the writer saves.

15. Inventory lines not fully mapped.
    - F-TABLE-049, first sentence (a read-only preview has no cell editor, table bar or table action):
      no SwRS of this scope says it (SwRS-034 and StRS-015 point to "trust-security", whose SwRS
      directory does not exist yet). Add a note to the orchestrator so trust-security owns it, or add
      one SwRS here.
    - F-TABLE-042..045 slash entries (`/table`, `/grid`, `/tbl`, `/align`, `/left`, `/center`, `/right`,
      `/caption`, `/list-table`, `/pipe`, `/convert`, `/html`): the guidelines ask one SwRS per slash
      entry; SwRS-110 covers modes only. Confirm palette-slash owns them.

16. SwRS-111. The Normative text says the cell becomes ":---", ":---:" or "---:". `alignColumn` keeps the
    cell width: `dashes = Math.max(3, core.length - colons)`, so "|----------|" becomes ":---------".
    SwRS-112 explains padding but 111 is literally false for any cell longer than three characters. Fix:
    "... with a colon on the left (left), on both sides (center) or on the right (right) of the
    existing dashes, keeping at least three dashes".

17. Untested SwRS with `annotation_exemption: false`. SwRS-002, 012, 020, 033, 071, 072, 078, 093, 120 (and
    the no-test boundaries of 054, 060, 065) have no test, so `okfreq trace` will report them as
    non-exempt without `@tests_req`. Not a text defect, but the verification notes must not be read as
    covered: decide per SwRS between a backlog test (the code is unit-testable; 012 and 120 are the
    cheapest) and an exemption with a reason.


## Re-check

Scope re-read in `markdown-okf-schema-studio-wt-059-b3`: 15 StRS, 129 SwRS files (121 active, 8
deprecated: 026, 027, 029, 030, 044, 045, 046, 047). Read-only; no lint, no build, no test run.
Checks made: script check of `derives_from` / `derived_by` (0 mismatches, 0 dangling, 0 duplicate
uuid), every `Unit test ... in test/...` title matched against the cited file (all found; the five
parametrised titles of `markdownTablePreservation.test.ts` and the "T30:" prefix are matches),
all cross-scope ids resolved and checked for lifecycle, no relative link or inventory id in the
text, and the changed or new claims read against `tableCellEditor.ts`, `blockEditor.ts`,
`blockSourceEditor.ts`, `editMode.ts`, `markdownTable.ts`, `tableEditActions.ts`,
`editActionHelpers.ts`, `textEditing.ts`, `stickyBar.ts`, `editModeStyles.ts`.

Verdict: FIX-REQUIRED

### Status of the 17 earlier defects

Fixed and verified against the code: 1 (034 reduced, new 121; the Known issue is true:
`switchTableCell` and `openMappedEditor` both return on `!edit.tableModel`), 2 (104), 3 (084),
4 (092), 5 (063, 088), 6 (051, the CSS at `editModeStyles.ts:353-366` matches the new text),
7 (072), 8 (093, 070, 072), 9 (050, 054, StRS-008), 10 (106, 107, 116, 119), 11 (split into 122,
123, 124, 125, 126, 127, 128, 129; 033, 066 and 023 kept as one rule each, accepted as before),
13 (all six), 14 (StRS rationale is now free of paths, pixels and message names), 16 (111).
Defect 12 is only partly fixed: see 1, 2 and 3 below. Defect 15 is accepted: F-TABLE-049 is
owned by block-editing and trust-security according to the inventory, the slash entries by
palette-slash. Defect 17 is dropped: leaving untested SwRS non-exempt is the convention of every
scope (P10.5 closes the gaps).

### Answer to the analyst's doubt (archived duplicates)

- SwRS-029 (Escape during an IME composition) is NOT covered by BLOCK-055. BLOCK-055 says "in the
  text box" of a block editor, its Criteria names "the Escape branch of the keydown listener" and
  its test is `Escape during IME composition neither cancels nor saves a block edit`
  (`runtimeBlockEditor.test.ts:533`, it drives `blockSourceEditor.ts:321`). The cell has its own
  listener with its own condition (`tableCellEditor.ts:398`, `event.key === "Escape" &&
  !event.isComposing`) and its own test (`runtimeTableCellEditor.test.ts:842`). Two
  independent code paths: TABLE-029 must come back.
- The other archived ones are acceptable duplicates, because the behaviour is carried by ONE
  shared function and the block SwRS already names the cell:
  046 = BLOCK-076 (the SwRS itself says "serves the table cell"), 047 = BLOCK-078 (names TABLE-047's
  case), 044 = BLOCK-069/070 and 045 = BLOCK-074 (both go through `textControls.wrapSelectionInControl`
  and `keepUndoInControl`, tests of the cell sit in `runtimeBlockEditor.test.ts`),
  026/027 = BLOCK-053 (both buttons and Escape call the shared `blockEditor.cancelBlockEdit` and
  `createEditorButtons`), 030 = BLOCK-211 and BLOCK-212 (shared `flushOpenEditors`; the cell branch
  is kept in the active TABLE-031).

### Defects

1. SwRS-MDOKFSTUDIO-TABLE-029 wrongly archived (duplicate of BLOCK-055 is false).
   Evidence: see "Answer" above; `tableCellEditor.ts:398` versus `blockSourceEditor.ts:321`,
   `runtimeTableCellEditor.test.ts:842` versus `runtimeBlockEditor.test.ts:533`. StRS-004's
   rationale ("but not during an IME composition") and its `derived_by` list 029, so with 029
   archived the rule has no active SwRS and the cell test is orphaned.
   Fix: set `lifecycle: draft` on SwRS-029 (keep id, uuid, text, `derives_from`
   StRS-004), keep it in StRS-004 `derived_by`; add to its Verification notes "The block editor
   equivalent is SwRS-MDOKFSTUDIO-BLOCK-055; the cell has its own listener". Do not re-archive.

2. StRS-MDOKFSTUDIO-TABLE-007, rationale: dangling cite to an archived id.
   Evidence: the rationale lists "SwRS-MDOKFSTUDIO-BLOCK-069, 070, 074, 076, 077 and 078";
   BLOCK-077 has `lifecycle: deprecated` (merged into BLOCK-076, whose text already says "every
   other keydown goes on to VS Code").
   Fix: "(SwRS-MDOKFSTUDIO-BLOCK-069, 070, 074, 076 and 078)"; keep the Ctrl+Tab clause.

3. StRS-MDOKFSTUDIO-TABLE-005, rationale: incomplete cite for Back.
   Evidence: the StRS title and need speak of "follow a link, press Back"; the rationale cites BLOCK-207,
   211 and 213, but "Back right after typing saves first" is BLOCK-212 (draft). With TABLE-030
   archived into the BLOCK ids, Back has no cited owner.
   Fix: "(SwRS-MDOKFSTUDIO-BLOCK-207, 211, 212 and 213)".

4. SwRS-MDOKFSTUDIO-TABLE-112: wrong mechanism (same class as the fixed defect 16).
   Evidence: `alignColumn` computes `dashes = Math.max(3, core.length - colons)` first, so a
   delimiter cell longer than three dashes keeps its width by giving up DASHES; trailing spaces
   are used only when the cell has exactly three dashes. The unit test shows it
   (`| ------ |` right becomes `| -----: |`, no space taken). The Normative text says the colons are
   fitted "by taking room from its trailing spaces", and Scenario 1 says "the colon takes room from
   the trailing spaces" for a GIVEN that includes `|----------|`, which has no trailing space.
   Fix: Normative: "When the delimiter cell is longer than the minimum, the extension SHALL keep
   its width by taking the room of the colons from its dashes (never below three) and, for a
   cell of exactly three dashes, from its trailing spaces (keeping at least one), and SHALL replace
   an alignment already there." Scenario 1: `|----------|` left gives `|:---------|` (dash given up) and
   `| ---      |` left gives `| :---     |` (trailing space given up).

5. SwRS-MDOKFSTUDIO-TABLE-069: bundled SHALL (new in this revision, same class as the earlier defect 11).
   Evidence: one SHALL reveals the bar again when a layout change hides it, and a second SHALL leaves the
   page alone when the bar size is unchanged; each has its own scenario and its own code path
   (`scrollCore`/edit anchor restore versus the size comparison) and its own test
   (`a later layout change that pushes the toolbar above the reading offset is revealed again`
   versus `a toolbar that is already visible causes no extra scroll`).
   Fix: keep the reveal as the SHALL of 069 and make the unchanged-size case Scenario 2 only (drop
   "and SHALL leave the page alone when the bar size is unchanged" from the SHALL), or split it into a
   new SwRS under StRS-010.
