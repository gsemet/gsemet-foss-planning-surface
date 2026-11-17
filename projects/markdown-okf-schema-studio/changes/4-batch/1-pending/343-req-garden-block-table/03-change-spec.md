# Change specification: garden the requirements of block-editing and table-editing

Source: CR requirements-gardening, `evidence/audit-block-table.md` (the findings and the mapping) and
`evidence/audit-synthesis.md`, read at Studio `main` dedbdb2a. This CR changes requirement text,
requirement relations, `@implements_req` / `@tests_req` markers, a few CSS constants and tests. It
changes no product behaviour (02-answers.md).

Depends on (land first, this branch stacks on them): req-use-case-diagrams (the `### Use case diagram`
rule and its site rendering) and req-marker-gate (at most 3 IDs per marker comment, companion files
name the scenario per ID, a shrinking baseline of offenders).

## Goal

A human reviewer understands each block-editing and table-editing use case by reading its StRS. Each
SwRS is one observable behaviour, linked by markers on the code that does it and on the tests that
check its scenarios. Every StRS has a validation test on a real scenario and a use-case diagram.

## Rules that frame the work (read, not restated)

- Studio `.agents/constitution.md` (sections 1, 3, 4), `requirements/guidelines/requirements.guidelines.md`,
  `requirements/guidelines/project.guidelines.md` ("Main paths of a StRS", "During a change",
  "Approved requirements"), and the rules added by req-use-case-diagrams and req-marker-gate as they
  landed in `project.guidelines.md` and `scripts/check-marker-companions.mjs`.
- okfreq is run as `uv run --no-sync --group requirements okfreq` (the justfile's `{{ okfreq }}`).
- IDs below drop `MDOKFSTUDIO-` (BLOCK-042 = SwRS-MDOKFSTUDIO-BLOCK-042). Line numbers are those of
  dedbdb2a; the two sibling CRs shift some of them: find each site by the function or test name given.

## Decisions carried from 02-answers.md

1. Published requirements are never deleted. Every merge and every split goes through
   `okfreq supersede OLD NEW [NEW...] --yes` (or `okfreq archive` for a requirement with no
   replacement). No `okfreq retire`, no `git rm` of a requirement file.
2. The owner keeps three decisions; the Driver brings them back and does not take them alone:
   - the re-approval of every approved StRS whose authored text changes (BLOCK-003, BLOCK-025,
     TABLE-001, TABLE-012 in this scope);
   - any `draft` -> `proposed` change (none exists in these two scopes: every in-force requirement is
     `proposed` or `approved`; new requirements are created `proposed`, per `project.guidelines.md`);
   - any merge or split below that the Driver doubts after reading the code: it stops on that item,
     writes the doubt in the CR's folder, and goes on with the rest.
3. The specification follows the audit report; the owner did not review it. No spec critic.

## Gated work: approved StRS (owner re-approval first)

These four StRS are `approved` (`approved_by: gaetan@xeberon.net`, `approved_at:
2026-11-12T12:30:00+01:00`). Their authored text changes only after the owner's recorded agreement
(open question Q1). Without it, their text stays as is and only the ungated work below applies.
With it, set `approved_at` to the time of the agreement (ISO 8601 with UTC offset), record the
agreement in this CR's `02-answers.md` through the Chief of Staff, and list the four under "Approved
requirements changed" in the PR body with the owner's review requested.

| StRS | Text change asked |
|---|---|
| BLOCK-025 | Remove the stale "Known issue" bullet (line 96: CRLF second save refused, see BLOCK-234); BLOCK-234 and `test/session/blockReq.requirements.test.ts:492` show it fixed. Add the use-case diagram. |
| BLOCK-003 | Trim the 7-bullet rationale (drop the 2 pointers to other scopes). Add the diagram. Its Main paths cite BLOCK-014, 017, 026, 033: all stay valid (see the BLOCK-029/033 merge below, which keeps BLOCK-033). |
| TABLE-001 | Cut the 18 rationale bullets to the constraints a writer sees (drop the ~8 that only say something "belongs to" another scope). Add the diagram. |
| TABLE-012 | Split the two needs: supersede TABLE-012 by two new StRS, "A writer formats the text of a table cell" (children TABLE-085, 091, TABLE-018 context) and "A writer inserts and shapes a table from the palette" (children TABLE-106, 111, 115, 117). Each new StRS gets Main paths built from the current TABLE-012 path, a diagram and a validation test. |

Relations of an approved StRS (children added or removed through the SwRS' `derives_from`) are not
authored text of that StRS; the Driver changes them in the ungated work and lists the approved StRS
whose generated Links changed in the PR body (open question Q2 confirms this reading).

## Ungated work

### 1. StRS text (all `proposed`)

- **TABLE-008** (H): replace "five labelled buttons (Row +, Row −, Col +, Col −, List table)" by the
  seven buttons the code and `test/integration/realInput/editorWidgets.ts:941` show: "Row above",
  "Row below", "Row −", "Col left", "Col right", "Col −", "List table"
  (`src/page/features/tableCellEditor.ts`, the `addAction` calls). Remove the two statements that a
  column operation rewrites the table in one fixed style and loses padding and indentation (line 52
  and the Known issue at line 56): TABLE-055, StRS-TABLE-011 and `markdownTable.test.ts:372` say the
  opposite. Keep the other Known issue (separator at a line end).
- **BLOCK-001**: path 2 names edit mode ("view choices" -> edit mode).
- **BLOCK-006**: shorten `user_need` (about 110 words, five needs) to "never lose typed text"
  (autosave, keep or drop, leave safely); the "edits land exactly" part is BLOCK-025's. Its children
  become 042, 047, 053, 193, 205, 216 plus the shared rules by `depends_on` (section 3).
- **TABLE-011**: split the two needs by `okfreq supersede StRS-TABLE-011 <new A> <new B> --yes`:
  A "A writer converts a table between pipe, list-table and HTML forms" (children: the merged
  conversion SwRS of section 2, TABLE-094); B "A table edit changes only the lines it touches"
  (children TABLE-094, BLOCK-234 by `depends_on`). Create both with `okfreq new` in
  `requirements/tiers/strs/table-editing/`, `--lifecycle proposed`.
- **TABLE-006**: stays; it is no longer thin once BLOCK-003 and BLOCK-069 derive from it (section 3)
  and the TABLE-035 split adds three children.
- Every StRS whose Main paths cite a superseded SwRS gets its path updated to the replacement ID
  (`scripts/check_main_paths.py` refuses a superseded citation). For an approved StRS this is gated:
  the merges below are chosen so that no approved Main path cites a superseded ID.

### 2. SwRS merges and splits (owner rule: supersede, never delete)

Create each new SwRS with `okfreq new ... --lifecycle proposed --derives-from <StRS>`, fold the
scenarios of the superseded ones into it (nominal, refusal, boundary; one scenario table when the
inputs are equivalent), then `okfreq supersede`. Move every marker of a superseded ID to its
replacement in the same commit.

| Old (superseded) | New / survivor | Parent StRS | Notes |
|---|---|---|---|
| BLOCK-236, 237, 238, 239, 240, 241, 242, 243, 244, 245 | new "The host ignores a malformed block-editing message and changes nothing" (one table: message, required fields) | BLOCK-025; `depends_on` TRUST-052 | X5. Implementation markers on the validators move to the new ID. Tests: `test/core/protocol/pageToHost.test.ts:173, 190-193, 281, 294` keep their assertions with the new ID; add one refusal test per message of 236-239 (today only the oracle test `pageStateMessages.test.ts:220-229`). |
| TABLE-070, 073, 074, 076, 080 | new "A table converts between pipe, list-table and HTML forms without loss, or is refused with a reason" | new StRS A (TABLE-011 split) | Bar button and palette/slash actions are entry-point scenarios; 076 is the refusal ("Nothing was changed."), 080 the fidelity boundary (cells, escapes, alignment). Implementation markers: `convertTableAtCaret` (`tableEditActions.ts:162`), `tableConversion.ts:57/82/268`, and add the pipe and HTML writers. |
| TABLE-003, 004, 005 | TABLE-055 (survivor) | TABLE-008 | 055 already cites 003 and 004; 005 (buttons on a list-table) becomes a boundary scenario. Markers of 003/004 on `tableStructure.ts:18/33` become TABLE-055. |
| BLOCK-029 | BLOCK-033 (survivor) | BLOCK-003 | Both specify the status line with Done and Cancel. BLOCK-033 survives because the approved BLOCK-003 Main paths cite it. Fold 029's scenarios ("cell that cannot be parsed", "grows with its text") into 033. |
| BLOCK-002 | BLOCK-014 (survivor) | BLOCK-003 | Hit area of a horizontal rule becomes a boundary scenario of "what a click opens". |
| BLOCK-129 | BLOCK-109 (survivor) | BLOCK-014 | "The page applies a move result only for its own render" becomes a boundary scenario. |
| TABLE-102 | TABLE-094 (survivor) | TABLE-011 split (A and B) | How a row is split into cells: boundary scenarios of 094. |
| TABLE-118 | BLOCK-255 (survivor) | BLOCK-003 and TABLE-001 | Same rule (a late open keeps the find focus) for block and cell editors. |
| BLOCK-258 | new "A card title or option opens on its own line" (BLOCK-003) + new "A one-line editor commits on Enter and leaves on Tab" (BLOCK-008) | as stated | Its 10 sites are split between the two new IDs by what each branch does; `html-sanitizer.ts:95` goes with the first. |
| TABLE-035 | four new: (a) Tab and the arrows move between cells; (b) Tab in the last cell adds a row and shows the hint (`tableTabRow.ts`); (c) the cell left shows its typed text rendered (`tableCellEditor.ts:75`, `cellInlineMarkdown`); (d) the cell is revealed in the table's scroll box (`revealCellInTable`) | TABLE-006 | `okfreq supersede SwRS-TABLE-035 <a> <b> <c> <d> --yes`; its 9 marker sites each go to the one new ID their branch does. |

Rewordings in place (same contract, proposed, no supersede):

- TABLE-013: observable wording ("moving to another cell keeps every change; the whole session is one
  undo step"), not "remember each change in the table model".
- BLOCK-191: observable ("a change inside the open block ends the edit with an error and keeps the
  text"), not the host edit lock.
- BLOCK-102 / BLOCK-253: remove the Enter scenario from BLOCK-102 (the button); BLOCK-253 keeps Enter
  and ArrowDown for the keyboard selection.
- BLOCK-069: complete the truncated title ("... stay in the").

Left as they are: TABLE-117 (its convert-to-HTML half overlaps the new conversion SwRS; see Q4),
TABLE-006 SwRS width (acceptable per audit), BLOCK-069 width.

### 3. Parents (`derives_from` and `depends_on`)

| SwRS | Change |
|---|---|
| BLOCK-257 | derives BLOCK-003 instead of BLOCK-001 |
| BLOCK-001 (SwRS) | drop StRS-BLOCK-016 |
| BLOCK-004, BLOCK-254 | derive BLOCK-008 instead of BLOCK-016 |
| BLOCK-033, BLOCK-148, BLOCK-169 | drop StRS-BLOCK-006 (148 and 169 stay under BLOCK-016) |
| BLOCK-003, BLOCK-069 | add StRS-TABLE-006 |
| TABLE-120 | derives TABLE-001 instead of TABLE-012 |
| BLOCK-255 | add StRS-TABLE-001 (after the TABLE-118 merge) |
| BLOCK-025's children | keep only 042, 058, 094, 117, 124, 127, 169, 174, 216, 234, 256 and the new validator SwRS; drop BLOCK-025 from the `derives_from` of 003, 041, 053, 069, 109, 130, 156, 166, 191, 205 (each keeps its use-case parent). BLOCK-042 stays because the approved BLOCK-025 Main paths cite it. |
| BLOCK-041 (shared rule) | one parent, StRS-BLOCK-003; every other StRS that derived it gets `depends_on: [SwRS-MDOKFSTUDIO-BLOCK-041]` in its frontmatter (BLOCK-014, 016, 025, 006, and in other scopes FMEDIT-008, FMEDIT-001, GFM-003, MYST-009, REVIEW-008). |
| BLOCK-058 (shared rule) | one parent, StRS-BLOCK-025; same `depends_on` on every other StRS that derived it. |

A StRS frontmatter accepts `depends_on` (base schema; checked on a copy of the bundle: `okfreq
validate` 0 errors, `update-coverage` projects a "Depends on" group in its Links).

Constraint (Q3): `scripts/check_main_paths.py` requires each SwRS cited in a Main path to derive from
that StRS. BLOCK-041 is cited in the Main paths of FMEDIT-001, GFM-003, MYST-009; BLOCK-058 in those of
BLOCK-006, BLOCK-014, FMEDIT-008, GFM-003, REVIEW-015. Until Q3 is answered, keep the derivation for
each StRS whose Main paths cite the shared rule, and apply `depends_on` only to the others.

SwRS of other scopes derived from these StRS (LIFE-169/170/173, TRUST-001/005/059/064/065, PALETTE-031)
are left to the CR of their scope; this CR does not edit their files.

### 4. Implementation markers (`@implements_req`)

At most 3 IDs per marker comment (marker-gate rule); each marker on the declaration or branch that
does the behaviour.

- CSS headers (X2): `src/core/preview/styles/editModeStyles.ts:1-12` and `contentBlockStyles.ts:6-19`.
  Move this scope's IDs (BLOCK-002->014, 014, 017, 029->033, 087, 109, 140, 254, 258->new, TABLE-006,
  048, 064) onto named CSS constants, one per behaviour (for example `HR_HIT_AREA_CSS` for the `hr`
  rule at `contentBlockStyles.ts:490`), concatenated into the existing template so the produced CSS is
  byte-identical (check with a snapshot or string equality before/after). IDs of other scopes in
  those headers (DIAG-001, ...) stay for their CR. Markers stay outside the CSS string.
- Hub functions (X3): split the stacks on `openBlockEditor` (`blockEditor.ts:224-228`),
  `closeBlockEdit` (`blockEditor.ts:39-43`), `openMappedEditor` (`editMode.ts:128-131`),
  `receiveBlockEditSource` (`blockSourceEditor.ts:45-52`) and `renderTableCellEditor`
  (`tableCellEditor.ts:263-265`) onto the branch of each behaviour.
- TABLE-055: on the six structural `addAction` calls of `renderTableCellEditor` (Row above to Col −).
- BLOCK-033: add on `createEditorButtons` (`blockEditor.ts:523`) and on the immediate frame insertion.
- TABLE-034: on the code that keeps the text and drops the navigation, not only the dispatcher
  `blockSourceEditor.ts:52`.
- TABLE-091: remove from `renderTableCellEditor`; it stays on `escapeCellPipes`
  (`markdownTable.ts:114`) and `cellSafeEdit` (`textEditing.ts:278`).
- TABLE-001: remove from `serializePipe` (`markdownTable.ts:275`); TABLE-002/007 also off it.
- BLOCK-094: remove from `handleEditOpen` (`blockEdits.ts:160`).
- BLOCK-205: move from `postEditSourceError` (`blockEdits.ts:120`) to the "save refused during a
  flush warns" branch.

### 5. Test markers (`@tests_req`)

- `test/integration/realInput/markers.ts:4-65`: remove every BLOCK-*, TABLE-* and StRS-BLOCK/TABLE
  marker; put each on the scenario function that checks it (the scenario files of
  `test/integration/realInput/`), or name the scenario per ID in the companion as the marker-gate rule
  asks. Drop a marker that no scenario backs. Other scopes' lines stay for their CR.
- `test/page/modules/editActions.test.ts:38-51` and `tableInsertAfterTable.test.ts:7-9`: move
  TABLE-073/074/076 (now the conversion ID), 106, 111, 115, 117 onto their tests (`editActions.test.ts`
  htmlTable 757-825, columnAlign 883-904, tableCaption 1077, list/pipe table 1404-1438).
- `test/integration/previewEditing.test.ts:240-256`: the one `run()` with 17 markers; put this scope's
  IDs next to the step that checks each, at most 3 per comment; BLOCK-174 next to the empty-clipboard
  step (around :1410).
- TABLE-013: add at `runtimeTableCellEditor.test.ts:636` ("switches cells without losing changes ...");
  remove from `:19` (the row/column toolbar test); TABLE-034 stays only for the refused-save part (`:712`).
- BLOCK-148: add at `runtimeBlockSelection.test.ts:194, 209, 220`.
- BLOCK-102: add at `runtimeBlockMoves.test.ts:374` ("a failed render offers no Start writing point").
- BLOCK-109: add at `runtimeBlockMoves.test.ts:131`.
- BLOCK-001: remove from `runtimeBlockEditor.test.ts:365` (a BLOCK-017 test).
- BLOCK-014: add at `test/page/blockReq.requirements.test.ts:453` (malformed previewEditSource).
- `slashMenu.test.ts:247`: TABLE-106 -> TABLE-085 (it checks the cell palette contents).
- Every entry of this scope in the marker-gate baseline is removed; the baseline only shrinks.

File-size ratchet (1 500 lines in `test/`): `runtimeTableCellEditor.test.ts` is at 1 499,
`editActions.test.ts` at 1 498, `previewEditing.test.ts` at 1 454. Move markers line for line; when a
file would grow past the limit, first move a coherent group of tests to a new file (markers move with
them).

### 6. StRS validation tests (a real scenario each)

Put the `@tests_req StRS-...` marker on the real scenario (integration or real-input), not in a
companion list.

| StRS | Validation scenario |
|---|---|
| BLOCK-001 | Mark `scenarioEditModeNoReflow` (`realInput/editorWidgets.ts:745`, layout kept). Add a real-window step: edit mode on, close and reopen the preview, edit mode still on. |
| BLOCK-003 | `previewEditing.test.ts:244` (keep) and `scenarioCaretAtClick` / `scenarioEditAffordances` (`editorWidgets.ts:670/705`). |
| BLOCK-006 | `scenarioFlushBeforeLink`, `scenarioFlushBeforeBack`, `scenarioFlushBeforeTabSwitch` (`realInput/flushBeforeNavigate.ts:235/254/275`). |
| BLOCK-008 | `scenarioEnterContinuesList` (`editorWidgets.ts:383`), `scenarioArrowNavigation` (`blockKeys.ts:392`), `editKeys.test.ts:38`. |
| BLOCK-011 | `scenarioInsertBlocksFromPreview` (`realInput/renderPatching.ts:514`). |
| BLOCK-014 | `blockMove.test.ts:37` (exists), `scenarioBlockMoveKeys` (`blockKeys.ts:245`). |
| BLOCK-016 | `scenarioBlockSelection` (`blockKeys.ts:306`) for Shift+click; add a real Ctrl+C / Ctrl+V step there or next to it if it has none. |
| BLOCK-025 | `blockClipboard.test.ts:82`, `blockMove.test.ts:36` (exist). |
| TABLE-001 | `editorWidgets.ts:549-576` (type in a cell, Enter commits), `scenarioFlushCellAndFrontmatter` (`flushBeforeNavigate.ts:298`), `scenarioTableEscapeKeepsCellsLeft` (`tableEscape.ts:43`). |
| TABLE-002 | `scenarioRowMoves` / `scenarioColumnMoves` (`test/integration/tableMoves.ts:257/301`). |
| TABLE-006 | `scenarioTableTab` (`editorWidgets.ts:791`, RI-T17). |
| TABLE-008 | `scenarioTableToolbar` (`editorWidgets.ts:867`) and `test/integration/tableStructureReal.ts` (presses every structural button in a real window; the audit missed it). |
| New A (convert) | `scenarioConversionRoundTrip` (`tableMoves.ts:195`). |
| New B (minimal diff) | `scenarioTableMinimalDiff` (`blockKeys.ts:476`, RI-T04). |
| TABLE-012 or its two successors | cell formatting: `scenarioTableCellBold` (`blockKeys.ts:446`, RI-T35); insertion: add one real-input scenario (slash menu, Table 3x2, Column alignment, Enter, buffer checked). |

### 7. Scenarios no test checks (add a test each)

BLOCK-001 "hover and click do not reflow" (if `scenarioEditModeNoReflow` does not cover hover/click);
BLOCK-053 Escape during an IME composition; BLOCK-079 "remembered in the webview state" and "page
replaced before the save is rendered"; BLOCK-140 Shift+mousedown does not extend the text selection;
BLOCK-166 a held key sends one request until the host answers; BLOCK-174 empty clipboard (a unit test
with its marker, beside the integration step); BLOCK-058 "cancelled session" and "no visible text
editor"; BLOCK-033 (ex-029) "cell that cannot be parsed" and "grows with its text" (unit, today visual
only); TABLE-018 a pointer press in the last 500 ms; TABLE-035 (a) "final save cannot be posted";
TABLE-106 size limits and malformed or out-of-range size; the conversion SwRS "escaped pipes",
"canonical round trip", "list-table read in every fence style"; TABLE-094 the 4 untested scenarios of
ex-TABLE-102; the validator SwRS refusals of ex-236 to 239.

Unit tests go in the existing `test/page/`, `test/core/`, `test/session/` files of the behaviour.
A new test that fails reveals a bug: do not fix the code in this CR; write the behaviour as a
"Known issue: ..." line in the SwRS, keep the test asserting today's behaviour or skip it with the reason, and
note the bug in the CR's folder for the backlog (constitution section 1).

### 8. Use-case diagrams

Each in-force StRS of the two scopes (13 kept plus the new ones; BLOCK-026 is deprecated) gets one
`### Use case diagram` section with one Mermaid fence, per the req-use-case-diagrams rule. Kind and
content per the audit's item 6 of each StRS: state for BLOCK-001, 008, 016, TABLE-006; sequence for
the others. A diagram shows only what a cited SwRS specifies. The four approved StRS are gated (Q1).

### 9. Records

- `just requirements-update`, then a dated entry in `requirements/tiers/log.md` (`## 2026-MM-DD`,
  `### Garden block-editing and table-editing`): the old-to-new mapping of section 2, the reparenting,
  the StRS text changes and the owner's re-approval (or its absence), the verification results.
- PR body (Tests section): every requirement ID added, superseded or changed, with its source and test
  files; "Approved requirements changed" when Q1 is granted.

## Out of scope

- Deleting any requirement file (owner: never).
- Product behaviour, including fixing a bug a new test reveals.
- SwRS and StRS files of other scopes, except the one-line `depends_on` frontmatter of section 3.
- Making the diagram section mandatory (req-use-case-diagrams, later).
- The marker-gate script and the diagram rendering themselves (sibling CRs).

## Coordination

The six req-garden CRs edit shared files (`realInput/markers.ts`, the marker-gate baseline,
`editActions.test.ts` header, the CSS headers, `requirements/tiers/log.md`). Each removes only its own
scopes' lines; rebase conflicts on these files are resolved by keeping both sides' removals.

## Evidence

- `just requirements-lint` (validate with `--check-links`, `lint --check`, `update-coverage --check`,
  `check_main_paths.py`: last line `main paths: ... all valid`).
- `uv run --no-sync --group requirements okfreq trace requirements --json`: no unknown ID, no marker
  on a superseded or deprecated ID, every in-force non-exempt SwRS of the two scopes with an
  implementation and a test marker; no marker comment over 3 IDs in the touched files.
- `just check` (includes `check-markers` with the shrunk baseline, `check-limits`, unit and contract
  tests: the moved CSS constants produce identical CSS).
- `just preflight` (on Windows the static stage); the new and newly marked real-window scenarios run
  in CI's real VS Code jobs: trigger `gh workflow run ci.yml --ref <branch> -f heavy=true` before the
  PR leaves draft, and report its result.
- Counts in the PR: in-force SwRS of the two scopes before (86) and after (about 75: 24 merged into 7,
  BLOCK-129 folded, BLOCK-258 into 2, TABLE-035 into 4).

## Open questions (for the owner)

- **Q1. Re-approval of the four approved StRS** (table "Gated work"): BLOCK-025 (stale CRLF known
  issue removed, diagram), BLOCK-003 (rationale trimmed, diagram), TABLE-001 (rationale trimmed,
  diagram), TABLE-012 (superseded by two StRS, diagrams). Recommendation: agree to all four; the
  meaning of BLOCK-003, BLOCK-025 and TABLE-001 does not change. Without agreement those files keep
  their text and get no diagram.
- **Q2. Children of an approved StRS.** Changing which SwRS derive from an approved StRS (BLOCK-025
  loses about 25 children, TABLE-001 gains TABLE-120 and BLOCK-255, TABLE-012 loses TABLE-120) changes
  only its generated Links. Recommendation: not a text change, no re-approval; listed in the PR.
- **Q3. Shared rules cited in Main paths.** `check_main_paths.py` and `project.guidelines.md` accept
  only derived SwRS in a Main path, so BLOCK-041 and BLOCK-058 cannot become `depends_on` for the 7
  StRS whose paths cite them. Recommendation: in this CR keep those derivations; open a small CR that
  lets a Main path cite a SwRS the StRS `depends_on` (rule and script), which all six garden CRs use.
- **Q4. TABLE-117** (convert to HTML and insert an HTML table in one SwRS). Recommendation: leave it
  unchanged here (it is cited in the approved TABLE-012 Main paths); revisit with the TABLE-012 split.
