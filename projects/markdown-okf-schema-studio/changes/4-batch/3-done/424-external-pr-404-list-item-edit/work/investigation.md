# Investigation: CR-424, external PR 404 (list item edit scope, list items in the TOC)

- Worktree: `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-424`, base
  `3d1c337` (CR-351), head `d582d00` (author pspozio, cherry-picked from PR head `3de1bc46`).
- PR 404 was read only (no comment, review or edit).
- Checks I ran in the worktree: `just check-settings` passed (20 settings). `just check-markers`
  passed (404 in-force SwRS marked, 25 files on the baseline, baseline unchanged).
  `just requirements-lint` reported 0 index, projection or coverage changes, and 92 StRS with 578
  citations, all valid; it gave only the existing W2 warnings.
- `work/conflicts.md` records that `just check` passed at `d582d00` (4091 tests, 0 failures).

## Findings

1. **OWNER-QUESTION: approved StRS-MDOKFSTUDIO-BLOCK-003 contradicts the change.** The StRS was
   approved by gaetan@xeberon.net on 2026-11-18T10:55+01:00. Its "Rationale and constraints" say
   "A click on a list item edits the list that holds it". The PR does not change this StRS.
   - Under it, the PR changes proposed BLOCK-014 and BLOCK-017, the hover test, alertBlockEditOpen,
     editorWidgets r12, capture_comment_checks, capture_edit_checks and scenario v12.
   - The owner's PR comments 7008522495 and 7010349650 (2026-11-19) ask for this behaviour. They
     came after the approval, and they record no agreement to change BLOCK-003.
   - This hits the stop rule: the change needs a re-approved StRS.
   - Exact question: "Do you agree to change StRS-BLOCK-003 to 'A click on a list item edits that
     item; a click on the list itself, outside its items, edits the whole list', and to re-approve
     it (approved_by gaetan@xeberon.net, approved_at now)?"
   - If yes: record the agreement in `03-change-spec.md`, edit the StRS, reset approved_by and
     approved_at, and add a PR section "Approved requirements changed".
2. **OWNER-QUESTION: Cmd/Ctrl+Alt+Up/Down in a list item editor now does nothing.**
   - SwRS-BLOCK-130 (proposed) says the move chord in a block editor's text box saves and then
     moves the block. Before the PR, this moved the whole list. Now it does nothing, and the gap is
     written as a "Known issue" in BLOCK-014, not in BLOCK-130.
   - No requirement covers this behaviour, which hits the stop rule.
   - Exact question: "In a list item editor, should Cmd+Alt+Up/Down (a) do nothing for now, with a
     Known issue in BLOCK-130 and a backlog CR, (b) move the whole list as before, or (c) move the
     item among its siblings?"
3. **BLOCKING-FIX: hidden change to the arrow at the edge of non-list inner editors.**
   - `adjacentMappedBlock` in `src/page/features/blockEditor.ts` (line 163) now walks any
     non-top-level target up to its top-level block: `while (top && !blocks.includes(top))`. Before,
     it used `blocks.indexOf(edit.target)` and returned undefined, which left the key to the text box.
   - So an inner block editor (for example a paragraph inside an admonition, BLOCK-254) now jumps
     to the next top-level block at the edge. The inner block of a list item (exact mode) does the
     same and skips the sibling items. Neither BLOCK-079 nor any other requirement asks for this,
     and the owner did not.
   - Fix that keeps the contributor's intent: apply the walk-up only when the target is an `LI`, or
     an inner block whose parent is an `LI` (step to the sibling item first). Every other target
     keeps `blocks.indexOf(edit.target)`.
   - Add a test that an admonition inner block editor still leaves the arrow at the edge to the
     text box.
4. **BLOCKING-FIX: the stepping between sibling items belongs to SwRS-BLOCK-079, not BLOCK-014.**
   - BLOCK-079 (proposed, "Arrow keys at the edges open the previous or next block") owns this
     behaviour. The PR put the arrow row in BLOCK-014 and marked `adjacentMappedBlock` with
     `@implements_req BLOCK-014`.
   - Move the item and list-exit rows to BLOCK-079's criteria, change the marker to BLOCK-079, and
     give the new arrow tests in `listItemEditOpen.test.ts` and `runtimeBlockEditor.test.ts`
     `@tests_req BLOCK-079`. BLOCK-079 derives from proposed StRS-BLOCK-008, which already covers
     this.
5. **BLOCKING-FIX: SwRS-BLOCK-001 (proposed) is now stale.**
   - Line 71 says the pointer over a list item outlines the whole list, which the list no longer
     carries.
   - Line 107 cites the test "edit mode hover marks the whole list that a click would edit", which
     the PR renamed.
   - Rewrite the row as "the item is outlined; the list is outlined only outside its items", and
     cite the renamed test.
6. **BLOCKING-FIX: proposed StRS-MDOKFSTUDIO-TOOLBAR-006 does not cover list items in the TOC.**
   - Its statement is "a column that lists the document's headings", and constraint line 47 says
     "the column lists h1 to h4". New TOOLBAR-138 derives from it, yet goes beyond it.
   - The owner asked for the opt-in in comment 7010349650, and the StRS is proposed, so it can be
     edited without re-approval.
   - Add "and, when the writer turns on the setting, the list items under them, each cut to its
     first line or about 80 characters".
7. **BLOCKING-FIX: TOOLBAR-138 does not specify the attribute `data-sphinx-preview-toc-list-item`.**
   Only a test reads it. Either name it in TOOLBAR-138's criteria as the hook for styling, or drop
   it and let the test find the rows another way. Dead attributes are not allowed.
8. **BLOCKING-FIX: the footnote and `[TOC]` exclusions are tested only on a fake DOM.**
   - `LIST_ITEM_EXCLUDED` in `src/page/modules/tocColumn.ts` holds `nav.okf-toc, section.footnotes,
     table, [hidden]`. `nav.okf-toc` matches `mystToc.ts`. The `section.footnotes` class is not
     checked against rendered markup.
   - Add a test that renders real Markdown with footnotes, a `[TOC]` and a table, then checks that
     the TOC lists none of their items. Fix the selector if the renderer emits another class.
9. **BLOCKING-FIX: the "Structure:" paragraph of `docs/user/editing.md` (lines 108-114) is
   incomplete.**
   - The new item-click paragraph is right, but "Structure:" does not mention the list, item and
     inner-block levels, Right and Left between them, the arrow stepping between items, or the
     known issue from finding 2.
   - Add one or two sentences covering these.
10. **BLOCKING-FIX: the log entry in `requirements/tiers/log.md` is incomplete.**
    - The entry is "A click on a list item edits that item; list items can be listed in the TOC",
      under `## 2026-11-20`. It has no verification results.
    - It does not mention BLOCK-003 (finding 1), TOOLBAR-006, BLOCK-001, BLOCK-079 or BLOCK-130.
    - Complete it after the edits, with the commands run and their results.
11. **BLOCKING-FIX: the commit message breaks the commit guideline.**
    - Its last paragraph describes the tests, which the body must not do. Remove that paragraph.
    - Keep pspozio as author, the `feat(editor):` subject and `Assisted-by: Claude:Opus-5.5`.
    - request.md asks for Co-authored-by lines, but the project guideline says "Do not use
      Co-Authored-By", and project rules outrank the process (constitution 8). So add none.
    - Our follow-up rounds go in their own commits, each with its own Assisted-by trailer.
12. **BLOCKING-FIX: the PR body must list each changed assertion with its reason**, to meet
    constitution 3. These are:
    - the runtimeBlockEditor hover test (list to item, renamed);
    - alertBlockEditOpen ([1,8] to [8,8], plus originalText);
    - editorWidgets r12 (ul to the nested li);
    - capture_comment_checks (UL to LI);
    - capture_edit_checks v12 (list to item);
    - scenarioIds v12, renamed `block-editing/v12-list-item-opens-item-dark-460`, with new lock text.
    The body must also name PR 404 and its author pspozio.
13. **BLOCKING-FIX: run `just requirements-update`** after findings 1 and 4 to 7. Then run
    `just check-markers` and `just requirements-lint` until they report 0 changes.
14. **OK/KEPT: the behaviour stays within the owner's ask.**
    - A click on an item edits the item. A click on the list itself edits the list.
    - Right goes down to the inner blocks (`structuralCursor.ts` is unchanged, so this already
      existed). Enter opens the selected node (`structuralNavigationView.ts`). Left goes back up.
    - The TOC option is opt-in, and each entry is cut to about 80 characters.
    - The commit message says the owner asked for this, and PR comments 7008522495 and 7010349650
      confirm it.
15. **OK/KEPT: the ordered-list counter CSS and the tagName reopen fix are correct.**
    - In `editModeStyles.ts`, `counter-increment: list-item` on the editor after an edited `ol > li`
      keeps the numbers of the next items.
    - `PendingBlockNavigation.tagName`, with a fallback to the line alone, reopens the editor on the
      right element when an item and its first block start on the same line.
16. **OK/KEPT: the setting `preview.listItemsInToc` is wired correctly.**
    - It is a startup setting (boolean, resource scope, default false, order 25) in
      `settingsRegistry.ts`, marked `@implements_req TOOLBAR-138`.
    - `package.json` was regenerated from the registry, and `just check-settings` passes.
    - The addition to the package-contract allow-list is legitimate.
17. **OK/KEPT: boundaries and file sizes.**
    - `tocColumn.ts` imports `readPreviewBootSettings` from core, as `chipToggle.ts` already does,
      and dependency-cruiser passes inside `just check`.
    - Largest src file: `pageRuntime.ts` at 728 lines, under 800. `tocColumn.ts` is 501 lines.
    - Largest test files: `previewStyles.test.ts` at 1485 and `runtimeBlockEditor.test.ts` at 1446,
      both under 1500.
18. **OK/KEPT: requirement IDs and markers.**
    - TOOLBAR-138 is the next free ID on main and on every batch-06 branch.
    - BLOCK-014, BLOCK-017, BLOCK-254 and TOOLBAR-040 are all proposed, so editing them with the
      code is allowed.
    - Each block holds at most 3 IDs, and the marker baseline did not grow.
19. **OK/KEPT: no format-specific code.** List items are mapped generically, and the session tests
    use the real renderer.
20. **OK/KEPT: CHANGELOG (Unreleased), glossary, settings and toolbar docs.**
    - The glossary entry "List item editor" is in alphabetical order.
    - The MarkSpec link in `settings.md` was requested by the owner.
    - The writing skill needs no change: no rendered syntax changed.
21. **OK/KEPT: security.**
    - The PR adds no network call, script or external resource.
    - TOC text is set with `textContent`, so it is not injected as HTML.
    - The only external link is in the docs.
22. **OK/KEPT: the cost of a large TOC.** With the option on, a big document can list thousands of
    entries. It is opt-in, and the docs can mention it. This cannot be measured in CI.
23. **OK/KEPT: the changed assertions are legitimate once finding 1 is agreed.** Each has a comment
    that says why, and each follows the owner's requested behaviour. The new tests fail on the old
    code.

## File-edit checklist for the Coder (after the owner answers 1 and 2)

- [ ] `requirements/tiers/strs/.../StRS-MDOKFSTUDIO-BLOCK-003.md`: change the item sentence and
      reset approved_by and approved_at, only with the agreement recorded in `03-change-spec.md`
      (finding 1).
- [ ] `requirements/tiers/strs/.../StRS-MDOKFSTUDIO-TOOLBAR-006.md`: cover the list items in the
      statement and at line 47 (finding 6).
- [ ] `requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-001.md`: fix the line 71 row
      and the line 107 test name (finding 5).
- [ ] `SwRS-MDOKFSTUDIO-BLOCK-079.md`: add the item and list-exit rows. In `SwRS-MDOKFSTUDIO-BLOCK-014.md`,
      remove the arrow row (finding 4).
- [ ] `SwRS-MDOKFSTUDIO-BLOCK-130.md`: apply the owner's answer to finding 2, and remove the known
      issue from BLOCK-014 if it moves.
- [ ] `SwRS-MDOKFSTUDIO-TOOLBAR-138.md`: name `data-sphinx-preview-toc-list-item`, or drop it in
      `tocColumn.ts` and its test (finding 7).
- [ ] `src/page/features/blockEditor.ts`: limit the walk-up to item targets, and change the marker
      on `adjacentMappedBlock` to BLOCK-079 (findings 3 and 4).
- [ ] Tests:
  - a new admonition inner-block edge test;
  - `@tests_req BLOCK-079` on the item arrow tests;
  - a rendered footnote, `[TOC]` and table exclusion test for the TOC (findings 3, 4 and 8).
- [ ] `docs/user/editing.md`: complete the "Structure:" paragraph (finding 9).
- [ ] `requirements/tiers/log.md`: complete the entry (finding 10).
- [ ] `just requirements-update`, `just check-markers`, `just requirements-lint`, then `just check`
      (finding 13).
- [ ] Our own commits: Assisted-by, no Co-authored-by, nothing about tests in the body. Leave
      pspozio's commit as it is, except that the tests paragraph comes out if the Driver rewrites
      its message (finding 11).
- [ ] PR body: the changed assertions with their reasons, PR 404, pspozio, and an "Approved
      requirements changed" section (findings 1 and 12).

## Evidence plan for the Verifier

- **Hosts:**
  - Windows, locally: `just check` and the unit and session suites.
  - Heavy CI with `gh workflow run ci.yml --ref <branch> -f heavy=true`: ci-visual and the real
    VS Code integration (editorWidgets r12, realInput `blockKeys.ts`). Run it on Linux, plus macOS
    for the Cmd+Alt chord if finding 2 changes the code.
- **Before and after screenshots, light and dark:**
  - `block-editing/v06`: the hover outline on an item, and on the list outside its items.
  - `block-editing/v12-list-item-opens-item-dark-460`: the item editor at 460 px.
  - The TOC with `preview.listItemsInToc` off and on, at 900 px and in the narrow rail.
  - An ordered list whose next items keep their numbers while an item is being edited.
- **Real window, to prove:**
  - a click on an item opens only that item, with the caret at the clicked word;
  - a click on the list outside its items opens the whole list;
  - Right, Left and Enter move through list, item and inner block;
  - the arrow at an item's edge goes to the sibling item, then past the list;
  - the arrow at the edge of an admonition inner block behaves as before (finding 3);
  - task lists and nested lists work;
  - Cmd/Ctrl+Alt+Up/Down in an item editor does what the owner chose in finding 2;
  - with the setting on, the TOC excludes footnotes, `[TOC]` and tables, and each entry is cut to
    about 80 characters.
- **Cannot be shown:** the TOC's cost on a document with thousands of list items (finding 22).
