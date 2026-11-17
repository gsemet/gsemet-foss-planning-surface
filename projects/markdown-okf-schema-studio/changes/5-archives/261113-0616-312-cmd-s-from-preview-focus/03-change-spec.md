# Change Specification: Cmd+S saves the document from the preview

Triage: automatable (short specification, the owner does not review it). Code read at
`origin/main` `cb968299` (version 1.7.1). Cut the worktree from `origin/main`. Read
[.agents/constitution.md](../../../../constitution.md) and the project guidelines before any change;
they rank above this specification.

## Goal

When the focus is in the preview (after an edit, in a block or table-cell text box, in a
frontmatter field of the properties table, or anywhere else in the page), Cmd+S on macOS and Ctrl+S elsewhere save the Markdown document that the preview
shows, as they do in the source editor. Today nothing happens: the writer has to focus the source
editor first (seen in demo video track B, 2026-10-28).

## Decisions carried from 02-answers.md

1. Cmd+S (Ctrl+S) with the focus in the preview saves the Markdown document the preview shows
   (owner, USER-IMPACT).
2. An open block or cell editor stays open with its caret. The text typed so far is written to the
   document first, then the document is saved (owner, USER-IMPACT).
3. Frontmatter field editor (properties table): Cmd/Ctrl+S writes the typed value and closes the
   field, as a navigation does today, then saves the document (owner, 2026-11-12, option b). Block
   and cell editors still stay open (decision 2).
4. The new command is hidden from the Command Palette, as `editUndo` is (`"when": "false"` in
   `menus.commandPalette`). The key binding can be rebound in Keyboard Shortcuts (owner, USER-IMPACT).
5. Which previews: the side panel (`activeWebviewPanelId == 'markdown-okf-schema-studio.preview'`).
   The custom editor (`markdown-okf-schema-studio.editor`) is checked in a real window first: VS Code
   saves a custom text editor natively. Add `activeCustomEditorId == 'markdown-okf-schema-studio.editor'`
   to the binding only if that check shows the native save does not meet decisions 1 to 3 (the file
   is not saved, or the text typed in the last autosave delay is missing from the saved file, or the
   dirty mark comes back after the save). Record the result of the check in the PR body (advisor 4).
6. Order of operations: the host command posts a message to the page; the page flushes its pending
   autosave; the page asks the host to save; the host waits until that text reached the document,
   then calls `documents.save`. A direct host save would run before the 400 ms autosave and leave
   the document dirty again (advisor 5).
7. Format on save and other save participants run, as with any save; the preview takes their
   result as an external change, as today. The SwRS states it (advisor 6).
8. Untitled document: `save()` opens VS Code's Save As dialog; nothing special (advisor 7).
9. Requirement: a new SwRS created with `okfreq new`, scope `lifecycle-sync`, lifecycle `proposed`,
   citing SwRS-MDOKFSTUDIO-BLOCK-003 for the key path; `@implements_req` at the command and at the
   page handler (advisor 8).
10. Proof: unit and session tests on the memory host for the order of decision 6, plus one real-window
    scenario: the key reaches the binding and the dirty mark goes (advisor 9).
11. Commit type `feat:` (owner, 2026-11-12: "Cmd+S is a feature; honest commit types"; the release is
    v1.8.0). This replaces the advisor's `fix:` recommendation.
12. Batch position: last product CR of the stack, just below the release CR, so it can be left out
    without restacking (advisor batch view). The PR adds its own line under `## Unreleased` in
    `CHANGELOG.md` (rule of the batch's first CR, changelog-line-in-each-pr).

## What changes

### `package.json`

- `contributes.commands`: a new command, id `markdown-okf-schema-studio.saveDocument` (name free if
  a better one fits the glossary), title "Save the Previewed Document", category "Markdown
  OKF-Schema Studio".
- `menus.commandPalette`: `{ "command": "markdown-okf-schema-studio.saveDocument", "when": "false" }`.
- `contributes.keybindings`: `key: "ctrl+s"`, `mac: "cmd+s"`,
  `when: "activeWebviewPanelId == 'markdown-okf-schema-studio.preview'"` (plus the custom editor
  clause only per decision 5). No `!inputFocus` and no `!editorTextFocus`: the key saves from the
  find field and from every text box of the page too.

### Host: `src/host-vscode/activation.ts`

- Register the command next to `FIND_COMMAND_ID`, calling a new `manager.runSaveCommand()`;
  `// @implements_req <new SwRS>` on it.

### Session: `src/session/previewManager.ts` and `src/session/features/blockEdits.ts`

- `runSaveCommand(): boolean`, modelled on `runFindCommand` / `runEditCommand`: find the live,
  not disposed session whose `panel.active` is true; none, or no stage: return false and do
  nothing. Otherwise post the new host-to-page message (below) with the stage's document id,
  revision and request id, and return true.
- When the page is not ready (`preview.page.readyRequestId === undefined`), or the post fails, the
  host saves the document directly (nothing to flush).
- Handler of the new page-to-host save request: wait, bounded by `FLUSH_WAIT_MS`
  (`src/core/preview/flushWait.ts`), until the edits the page sent before the request reached the
  document. The existing `settleHostEdits` cannot be reused as is: it also waits for
  `!preview.edits.active`, which stays true while the editor is open (decision 2). Wait instead for
  the active block edit to have no `pendingText` and `applying === false`, and for
  `preview.edits.pendingSaves` to be empty (the frontmatter saves are already tracked there through
  `trackPendingSave`, so the frontmatter value of decision 3 is covered by the same wait). Then call
  `host.documents.save(document)` on the preview's document. A false result (Save As cancelled, refusal) is silent.
- Messages arrive in order, so the page's autosave (`previewEditSave`, `final: false`) is handled
  before the save request; this is what makes the wait sufficient.

### Protocol: `src/core/protocol/hostToPage.ts`, `pageToHost.ts`, `pageToHostMessages.ts`, `src/session/pageMessages.ts`

- Host to page: `previewSaveCommand` (render addressing, like `previewFindCommand`).
- Page to host: `previewSaveRequest` (name free), validated in `pageToHost.ts`, gate `document` in
  `PAGE_MESSAGE_GATES` (it names the document the preview shows; the render may be one behind
  after an autosave).
- Each message gets its validator test in `test/core/protocol/hostToPage.test.ts` and
  `test/core/protocol/pageToHost.test.ts`.

### Page: `src/page/features/hostHandlers.ts`, `src/page/features/blockEditor.ts`

- `hostMessages.on("previewSaveCommand", ...)` with `// @implements_req <new SwRS>`: flush the
  pending block or cell autosave without closing that editor, save an open frontmatter field as a
  flush (decision 3), then post `previewSaveRequest`.
- Frontmatter field (decision 3): call `rt.frontmatter.flushFrontmatterEditor()`
  (`src/page/features/frontmatterEditor.ts:402`), the same flush a navigation uses; it posts the
  typed value whatever it holds and closes the field. When the field already has a plain save
  waiting for its result (`plainSavePending`), wait for that result, bounded, and flush again when
  it was refused, as `flushOpenEditorsThen()` does (`blockEditor.ts:449`); post
  `previewSaveRequest` only after that. Factor the shared waiting out of `flushOpenEditorsThen()`
  rather than copying it; do not call `flushOpenEditorsThen()` itself, which also closes the block
  and cell editors.
- `flushPendingAutosave()` (`blockEditor.ts:400`) posts `postBlockEditSave(false)` only when a timer
  is pending; keep that. For a table-cell editor, copy `tableInput.value` into `tableModel` first,
  as `flushOpenEditors()` does (`blockEditor.ts:425`), so the cell's typed text is in the save. Do
  not call `flushOpenEditors()` or `flushOpenEditorsThen()`: they send a final save and close the
  editors.
- A block or cell text box keeps the focus, its value, its selection and its undo history; nothing
  in the page moves. A frontmatter field closes and the focus goes where the flush leaves it today.
- Check that no page key handler swallows Cmd/Ctrl+S (`preventDefault` is fine, `stopPropagation`
  is not), in block, cell, frontmatter, find and comment fields, so the key reaches VS Code as the
  BLOCK-003 keys do.

### Requirements

- New SwRS with `uv run --no-sync --group requirements okfreq new`, scope `lifecycle-sync`,
  `--lifecycle proposed`. Normative statement: when the writer presses the VS Code save key binding
  with the focus in the side preview, the extension SHALL write the text typed in an open block or
  table-cell editor to the document and keep that editor open with its caret, write the value typed
  in an open frontmatter field of the properties table to the document and close that field, then
  save the document the preview shows. Scenarios: nominal (no editor open: saved, dirty mark gone); open block editor
  and open cell editor (typed text saved, editor open, caret kept); open frontmatter field (typed
  value saved, field closed, as a navigation closes it); rebinding in Keyboard
  Shortcuts; boundary (no focused preview: VS Code handles the key as before; untitled document:
  Save As dialog; format on save: runs, the preview shows the result as an external change; a
  page that does not answer: the save still happens after `FLUSH_WAIT_MS`); the custom editor
  result of decision 5. Related requirements: SwRS-MDOKFSTUDIO-BLOCK-003 (key path).
  `derives_from`: the StRS that best fits after reading the scope (candidates:
  StRS-MDOKFSTUDIO-BLOCK-025 "Preview edits land exactly ...", StRS-MDOKFSTUDIO-BLOCK-008). If the
  chosen StRS is `approved` and would change, stop and ask (project guideline "Approved
  requirements").
- `@tests_req <new SwRS>` at each test below. `just requirements-update`; dated entry in
  `requirements/tiers/log.md`.

### Documentation

- `docs/user/editing.md`, the paragraph on the VS Code keys in a text box (line ~78): Cmd/Ctrl+S
  in the preview saves the document, a block or cell text box stays open, a frontmatter field
  closes; the command name to rebind it.
- `CHANGELOG.md` `## Unreleased`: one user-facing line, appended at the end of the list.
- No rendered syntax changes: the writing skill is not touched.

## Evidence

- `test/core/protocol/*`: the two messages and their payload checks.
- `test/session/` (new file, for example `saveCommand.test.ts`, memory host from
  `src/host-memory/memoryDocumentStore.ts`, whose `save` marks the document clean):
  - no focused preview: `runSaveCommand()` is false, no message, no save;
  - focused preview, no editor: the save request saves, the document is clean;
  - an autosave applied slowly (`applyEdits` delayed) then the save request: `save` is called after
    the edit is applied, and the saved text holds it;
  - the active edit stays active after the save (editor not closed);
  - a frontmatter save tracked in `pendingSaves` and applied slowly, then the save request: `save`
    is called after it is applied, and the saved text holds the value;
  - a page that never answers: the host saves after the bounded wait.
- `test/page/runtimeBlockEditor.test.ts` and `test/page/runtimeTableCellEditor.test.ts`: on
  `previewSaveCommand`, a `previewEditSave` with `final: false` holding the typed text is posted
  before `previewSaveRequest`; the editor is still open; the caret and the selection are
  unchanged; with no pending autosave, only `previewSaveRequest` is posted.
- Frontmatter field (a page test next to `test/page/runtimeEditorFlush.test.ts`): on
  `previewSaveCommand` with a field open and a value typed, the frontmatter save holding the value
  is posted before `previewSaveRequest` and the field is closed; with a plain save pending and
  refused, the flush save is posted, then `previewSaveRequest`.
- `test/security/package-contract.test.ts`: the command, its key binding and `when` clause, and its
  absence from the Command Palette.
- Real window: a new `test/integration/saveKey.test.ts` built on `./realInput/harness` like
  `editKeys.test.ts`, run from `test/integration/trusted-suite.ts` and listed in
  `test/shared/e2eGroups.ts` (group `lifecycle-sync`). Scenario: open a fixture in the side
  preview, open a block editor, type text, press `MOD+s` at once (inside the autosave delay); the
  `vscode.TextDocument` is not dirty, its text holds the typed text, and the block text box is
  still focused with its value. A second step does the same in a table cell. A third step types a
  value in a frontmatter field of the properties table and presses `MOD+s`: the document is not
  dirty, its text holds the value, and the field is closed. The decision 5 check
  of the custom editor runs in the same file.
- `just check`, `just requirements-lint`, then `just preflight`. The PR runs only the simulated jobs:
  dispatch the heavy run on the branch (`gh workflow run ci.yml --ref <branch> -f heavy=true`) and
  link its result in the PR body.

## Out of scope

- A save from the Command Palette ("File: Save" already exists there).
- Save All, auto save settings, and any change of the autosave delay.
- Closing or committing the block and cell editors on save.
- Keeping a frontmatter field open on save (option (a) of the owner's choice, not taken).
- Review comments: they live in the sidecar file, not in the document.
- The custom editor binding, unless decision 5's check requires it.
