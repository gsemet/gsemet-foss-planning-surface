# No edit stays on Saving Markdown for good

Tests prove that every save of a block editor, a table cell editor or a frontmatter field ends
in the rendered result or in a shown error. Each hang the tests find is a bug, and this CR fixes
it. Cancel and Escape always close a block or cell editor, even while it shows "Saving
Markdown…". The save already asked for with Done goes on, and its text is kept. If that save then
fails, or the file changes outside the preview before it is written, the editor stays open or
reopens with the typed text and the reason. If the page cannot show it, VS Code offers to copy the
text. There is no time limit, no timeout message and no retry.

Short name: `save-guard`. Destination: the running batch-09, in its stack.

## Goal

CR `blank-run-edit-stuck-saving` (part A, short name `blank-save`) fixes the one hang the issue
found: a blank-lines block's editor stayed on "Saving Markdown…" because the content patch never
closed it. Nothing yet stops the next hang of that kind. This CR proves, with one test per save
path, that each path ends. It fixes the paths that do not end, and it makes the new Cancel rule
safe.

The owner's answers (`02-answers.md`):

- **Every save ends, and a hang is a bug** (save-guard-Q1 as amended by Q8 and Q9):
  - every save path (blocks, table cells, frontmatter) ends in success or in a shown error;
  - a block that stays on "Saving…" must never happen; when it does, it is a bug to fix, not a
    case the writer handles;
  - **tests only**: there is no time limit and no timeout or retry message. A hang the tests find
    is fixed in this CR.
- **Q9 replaces Q2, Q3 and Q5**: the frontmatter time limit, the timeout message, the 10-second
  limit and its measure are all gone.
- **Cancel during "Saving…" closes the editor, and the save goes on** (save-guard-Q4); the text is
  kept.
- **Stack order** (save-guard-Q6): after `blank-run-edit-stuck-saving`, before
  `blank-line-block-per-line`.
- **Spec critic on Fable** (save-guard-Q7): this CR changes the BLOCK-053 refusal scenario.
- **A cancelled save that fails reopens the editor** (save-guard-Q10): on that block, with the
  typed text and the error shown. Nothing is lost, and no VS Code warning is shown.
- **A block clicked after Cancel, before the save ends, opens when the save ends**
  (save-guard-Q11).
- **A frontmatter save that changes nothing closes the field with no message** (save-guard-Q12).
- **A file changed outside the preview while a cancelled save waits** (an undo, another edit)
  **reopens the editor** with the typed text and a message that the file changed, as for a
  failure (save-guard-Q13).
- **A click on a frontmatter field after Cancel waits for the end of the save**, as a block click
  does. On a failure the block editor reopens and the click is dropped (save-guard-Q14).
- **The other edit gestures do nothing until the save ends** (save-guard-Q15), as today while
  "Saving Markdown…" shows. These are a block move, a delete, a paste, a checkbox, a row or
  list-item drag (with its own `previewEditOpen`), a file drop and a replace.
- **Without Cancel, an editor on "Saving…" whose file changes outside the preview stays open**
  with the typed text and the "file changed" message, as in Q13 (save-guard-Q16).
- **A failure the page cannot show** (the page was reloaded, so it has no record and answers
  `reopened: false`): the host shows a VS Code message with a "Copy text" action that puts the
  unsaved text on the clipboard; nothing is lost (save-guard-Q17).

The Chief of Staff's decisions on the first specification's critic findings:

1. **Cancel during an in-flight final save also tells the host that the page editor is gone.**
   The host ends its edit keeping the text as written (no restore), and the next block opens.
2. **A pending block navigation is dropped on that Cancel or Escape.** The editor closes, the save
   completes, and nothing else opens or moves.
3. **The file-size limits hold** (see "Size limits").
4. **Requirements**: BLOCK-053, BLOCK-006 and BLOCK-047 are handled as in section 8.
5. **No part A double fix.**

Also kept: **Escape stays ignored while a frontmatter save is in flight**
(StRS-MDOKFSTUDIO-FMEDIT-001, SwRS-MDOKFSTUDIO-FMEDIT-004); the tests prove that save always ends.

## What this CR builds on

- **Part A** (`blank-run-edit-stuck-saving`, the branch below this one in the stack) changes
  `applyContentPatch` (`src/page/features/contentPatch.ts`):
  - a blank-lines block's editor (`replaceBlankRun`) stays open across a content patch only while
    no final save of it is in flight;
  - the condition becomes `state.activeBlockEdit?.replaceBlankRun && !state.activeBlockEdit.finishing`;
  - once a final save was posted, the patch closes the editor with `closeBlockEdit(false)`.

  Part A carries its own regression test. This CR does not repeat that fix or its test, and does
  not change that condition.
- **Part C** (`blank-line-block-per-line`, above this one) is out of scope.

## What exists today

Read from the code at `main` (`d762a732`); the Driver reads it again on top of part A.

### Block and cell editor, final save

`postBlockEditSave(true)` (`src/page/features/blockEditor.ts`) sets `edit.finishing = true`, shows
"Saving Markdown…" and posts `previewEditSave` with `final: true`. The block editor and the table
cell editor share it.

The message carries:

- `documentId`, `revision` and `requestId`, taken from the page's current render (`context`);
- `editId`, `line`, `endLine`, `originalText` and `editedText`;
- `insertAfterLine`, `replaceBlankRun` and `deleteWhenEmpty` when they apply;
- the pin and anchor fields, and `flush`.

It is called by Done, Ctrl/Cmd+Enter, a blur, the move chord (`moveBlockFromEditor`, with
`thenMove`), the arrow and Tab navigation (`navigateBlockEdit`, `tabThroughTableCells`), a click
on another block (`editMode.ts`, `blockSelectionView.ts`) and `flushOpenEditors`.

The editor closes only on:

- **a content patch**: `applyContentPatch` calls `closeBlockEdit(false)`;
- **`previewEditSource` with `done: true`**: `receiveBlockEditSource`
  (`src/page/features/blockSourceEditor.ts`) closes only `if (edit.finishing)`, then resumes the
  pending navigation (SwRS-MDOKFSTUDIO-BLOCK-263);
- **a full page replacement**.

An error answer keeps the editor open: `finishing` becomes false, the pending navigation and
selection are cleared, and the error shows (SwRS-MDOKFSTUDIO-BLOCK-216). The editor keeps its
text. Done then posts a new final save, which the host matches to its held edit or re-creates
from the document.

### While `finishing` is true

These all return early:

- `postBlockEditSave`;
- `cancelBlockEdit` (`if (!edit || edit.finishing) return;`, under `@implements_req
  SwRS-MDOKFSTUDIO-BLOCK-053`);
- `cancelTableCellEdit` (`src/page/features/tableCellEditor.ts`, first line `if
  (edit.finishing) return;`, under `@implements_req SwRS-MDOKFSTUDIO-TABLE-025`);
- the document-level Escape of the cell editor's `bindKeys`.

The Cancel button (`createEditorButtons`), Escape in the text box (through
`rt.selection.finishEditorWithSelection("cancel", …)`) and Escape in a cell all reach these
functions.

This is the BLOCK-053 refusal scenario "Cancel is ignored while the final save is in flight". The
page test `Cancel and Escape are ignored while the final save is in flight`
(`test/page/blockReq.requirements.test.ts`) checks it.

A click on another block while `finishing` is true only records the navigation
(`rememberPendingBlockNavigation`). The navigation resumes after the save
(`resumePendingBlockNavigation` in `editMode.ts`, called on `done` and from `initializeContent`
after a patch).

The other edit gestures check `state.activeBlockEdit` and do nothing while an editor is open:

- `tableRowMove.ts:215` and `listItemMove.ts:159`, which post their own `previewEditOpen`;
- `listItemMove.ts:124`;
- `blockMoves.ts:65`;
- `blockSelectionView.ts:217`, `:250` and `:411` (delete, paste, replace);
- `fileDrop.ts:25`;
- the frontmatter openers, `frontmatterEditor.ts:184` and `frontmatterValueEditor.ts:19`.

`closeBlockEdit(cancel)` clears the pending navigation only when `cancel` is true. It posts
`previewEditClosed` only when `edit.reportClose` is set.

### The host

The host side is `src/session/features/blockEdits.ts` and the lock is
`src/core/state/editLock.ts`.

- **`handleEditOpen`** refuses with "Another Markdown block is already being edited." while
  `preview.edits.active` is set. It refuses as stale unless the page's revision is the current
  document and stage revision (`currentPreviewDocument`). Only then does it call
  `openPageEditor`, which records `lock.pageEditorId`.
- **`handleEditSave`** (lines 447 to 560):
  - with no held edit, it re-creates one from the document, which needs a current revision and a
    matching `originalText`;
  - with a held edit, it refuses as "The preview block edit is stale" any save whose `editId`,
    `documentId`, `revision`, `requestId`, `line`, `endLine`, `originalText`, `insertAfterLine` or
    `replaceBlankRun` differs from that edit (lines 532 to 545);
  - otherwise it queues the text, and `drainActiveBlockEdit` applies it.
- **Completion.** When a final save is drained, `completeActiveBlockEdit` calls
  `releaseActiveBlockEdit`. That sets `edits.active = undefined` and calls `lock.release()`,
  which clears `held` **and `pageEditorId`** and runs the queued work. Then it asks for an
  immediate render. It posts `done: true` only when nothing is left to render (and the edit was
  not cancelled).
- **Apply failure or rejection.** `drainActiveBlockEdit` posts an error and sets
  `finalRequested = false`. **It leaves `edits.active` set**: the editor stays open on the page
  and shows the error. A "source block changed" refusal instead releases the host edit and keeps
  the page editor (`releaseHostEditKeepingEditor`).
- **Outside change.**
  - While a final save is requested or text is pending, `trackOutsideChange` returns false. The
    caller in `hostEvents.ts` (lines 332 to 343) then releases the edit without writing that text
    (`releaseActiveBlockEdit(session, true)`), and renders. The editor still open on "Saving…"
    closes on the patch, and its text is lost.
  - With nothing pending, a conflicting change posts "The source block changed outside the
    preview while it was being edited. Copy your text, then reopen the block." It keeps the page
    editor open (BLOCK-191).
- **`previewEditClosed`** calls `closePageEditor(editId)`. That clears `pageEditorId` when it
  matches, and drains the queued work only when `held` is false. `previewEditorWatch` makes the
  page report a close (`reportClose`, host side `watchedPageEditorId`).
- **`onReady`** releases a held edit when the page reports `blockEditOpen: false`.
- **Renders and reloads.** Render results wait while `pageEditorId` is set (`shouldDeferResult`,
  STAB-03). A full reload waits while `held` or `pageEditorId` is set (`shouldDeferReload`). A
  full page replacement clears `edits.active`.
- **Notifications and clipboard.** The `HostUi` port (`src/host-api/hostUi.ts`) offers
  `showInformation`, `showWarning` and `showError` with a message only (no action buttons), and
  `writeClipboard`. Only `src/host-vscode/vscodeHost.ts` calls `vscode.window`; the session tests
  use a fake `HostUi` (`test/session/blockFixture.ts`).
- **Test hook.** `holdEditSourcesForTests` (`src/host-vscode/testHooks.ts`) holds the sources of
  opened editors back.

### Protocol

In `src/core/protocol/hostToPage.ts`, `previewEditSource` and `previewFrontmatterResult` are
addressed as `render` and have no payload validator (`isValid`). The content patch has one, with
a 20 MB bound (`MAX_PATCH_CONTENT_LENGTH`). `previewEditSave` texts have no length bound.

### Frontmatter saves

Three places post `previewFrontmatterSave` and disable the control:

- `saveValue` (`src/page/features/frontmatterValueEditor.ts`, "Saving frontmatter…",
  `saving = true`);
- `saveKey` (`src/page/features/frontmatterEditor.ts`, "Saving frontmatter key…"; it disables
  the control without setting `saving`);
- `postFrontmatterAction` (field menu add or remove, `saving = true`).

`receiveFrontmatterResult` handles the answer:

- on `saved: true` it shows "Saved. Refreshing preview…" and keeps the editor waiting;
- the content patch closes the editor (`closeFrontmatterEditor("content patch")`);
- an error re-enables the control, shows the error and runs `afterResult`
  (SwRS-MDOKFSTUDIO-FMEDIT-019).

`bindKeys` ignores Escape while `edit.saving || edit.control?.disabled`.

On the host, `handleSave` (`src/session/features/frontmatter.ts`) runs the plan, the schema check
and then `applyWrittenEdits`. It posts `saved: true` when the apply resolves true, and an error
otherwise. `applyWrittenEdits` (`src/session/sessionDocuments.ts`) resolves true for an edit that
changes no text.

## Words

- **Final save**: the `previewEditSave` with `final: true` that `postBlockEditSave(true)` posts.
  For the frontmatter, any `previewFrontmatterSave`.
- **Save path**: one way a save can be answered. That is the content patch, `done`, an error
  answer, a host refusal, an apply failure or rejection, an outside change, a hidden panel, a
  document switch or a full page replacement.
- **Detached save**: a block or cell editor's final save that continues after the writer closed
  the editor with Cancel or Escape (save-guard-Q4). The page has no editor for it any more; the
  host completes it. If it fails, or the file changes outside the preview before it is written,
  the page reopens the editor.
- **Edit in flight**: an open block or cell editor, or a detached save not yet ended. While an
  edit is in flight, the other edit gestures do nothing.

Add "Detached save" and "Edit in flight" to `.agents/glossary/common.md`.

## What changes

### 1. Cancel and Escape close a block or cell editor during a final save (Q4, decision 2)

**`cancelBlockEdit`** (`blockEditor.ts`) no longer returns early on `finishing`. When `finishing`
is true, the page:

- clears `pendingBlockNavigation` (with its `thenMove`, the Tab-added row and the click target)
  and `pendingBlockSelection`;
- records the detached save (section 2);
- posts `previewEditClosed` with the editor's `editId`, whatever `reportClose` says;
- closes the editor with `closeBlockEdit(false)`. It posts no `previewEditCancel` and no second
  final save.

The save goes on. When it ends in success, nothing else opens or moves, except what the writer
clicked after the Cancel (section 2).

With no final save in flight, the behaviour is unchanged (BLOCK-053):
`closeBlockEdit(edit.hasAutosavedChange === true)`.

**`cancelTableCellEdit`** (`tableCellEditor.ts`): its first line `if (edit.finishing) return;`
becomes a call to `cancelBlockEdit()` and a return, when `edit.finishing` is true. This runs
before the Tab-added-row and kept-cell branches, so a cell during a final save posts neither
`previewEditCancel` nor a second save. Otherwise the function is unchanged (TABLE-025), and its
marker stays.

**The document-level Escape of the cell editor's `bindKeys`** no longer returns on `finishing`.
It reaches `cancelTableCellEdit` as for any Escape.

**`finishEditorWithSelection("cancel", …)`** keeps its rule. With the editor closed, the selection
goes to the edited block at once. Its quiet `pendingBlockSelection` of the same block, which is
set when `hasAutosavedChange`, may stay: it reselects the same block after the patch and moves
nothing.

### 2. The detached save on the page: its record, its end, and what waits for it (Q11, Q14, Q15)

**The record.** Add one field `detachedSave?: DetachedSave` to the page state (`pageRuntime.ts`).
Put the `DetachedSave` type in its own small module, for the size limit. Section 1 sets it, with
everything a reopened editor needs to send a retry the host accepts:

- **the final save message the page posted**, whole, minus the one-shot fields (pin, anchor,
  `flush`): `documentId`, `revision`, `requestId`, `editId`, `line`, `endLine`, `originalText`,
  `editedText`, `insertAfterLine`, `replaceBlankRun`, `deleteWhenEmpty`;
- **the editor fields that shape its text**: `trailingLineEnding`, `singleLine`,
  `deleteWhenEmpty`, `hasAutosavedChange` (always true after a posted final save), and
  `convertedText` when set;
- **the cell-session state** of a cell editor: `cellTextAtOpen`, `keptCellChange`, `tabAddedRow`,
  `tableRowIndex` and `tableColumnIndex`;
- **the block's lookup keys**, the same ones `rememberPendingBlockNavigation` records: block id,
  source line, tag name, and the table rank.

**Its end.** The record ends only on an answer that names its `editId`:

- `previewEditSource` with `done`: success (below);
- `previewEditSource` with `error`: a failure, or a file changed outside (section 4).

A content patch alone does not end it, because a render already in flight when the writer
cancelled can arrive before the save's answer. A full page replacement discards the page's state,
the record with it.

**`done` and the render that follows.** The host answers every end of a detached edit (section
3). When a render follows the save, `done` carries a new optional field `renderFollows: true`. The
record then stays in a "render pending" phase until the next content patch or full page.

**What waits.** While the record is set (in either phase), an edit is in flight:

- **a block or cell open** (`openBlockEditor`) does not post `previewEditOpen`. It records the
  target with `rememberPendingBlockNavigation`, the same way a click during "Saving Markdown…"
  does today (save-guard-Q11);
- **a click on a frontmatter field** (key, value, field action: `frontmatterEditor.ts:184`,
  `frontmatterValueEditor.ts:19`) does not open it. It is recorded as one pending field open, and
  a later click replaces it (save-guard-Q14);
- **the other edit gestures do nothing** (save-guard-Q15): block moves, delete, paste, checkbox,
  row and list-item drags (with their direct `previewEditOpen`), file drop and replace. One page
  helper, for example `rt.blockEditor.editInFlight()` (true when `state.activeBlockEdit` or
  `state.detachedSave` is set), replaces the `state.activeBlockEdit` test at each guard listed in
  "What exists today". The Driver searches for any other guard on `state.activeBlockEdit` that
  blocks an edit gesture and switches it too.

**After a success** (`done`, then the patch when `renderFollows`): the page clears the record. It
then runs the pending field open if there is one, otherwise `resumePendingBlockNavigation`. The
open thus carries the new revision, and the host's stale check passes. The navigation pending at
the time of the Cancel was dropped (section 1); what runs here is what the writer clicked after
it.

**After a failure** (section 4): the record is cleared, the block editor reopens, and the pending
block navigation and the pending field open are dropped.

### 3. The detached edit on the host (decision 1)

All in `blockEdits.ts`; the lock's API goes in `editLock.ts` if a method is needed.

- **Detach.** `previewEditClosed` for the `editId` of `preview.edits.active` marks the edit
  `detached` (a new flag on `ActiveBlockEdit`). This applies when the edit is not
  `cancelRequested` and the host has not already answered its final save with an error. The
  lock's `pageEditorId` is cleared as today.
- **Every end gets an answer naming its `editId`:**
  - **success**: the edit completes as `completeActiveBlockEdit` does, with no restore, and the
    host posts `done: true`, with `renderFollows: true` when it asks for a render. Today `done` is
    posted only when nothing renders;
  - **an apply failure or rejection, or the "source block changed" refusal**: the error answer
    with `unsavedText` (section 4);
  - **an outside change**: section 4;
  - **an idle edit at the detach** (nothing applying or pending; for example its final save had
    nothing new to write): it completes at once, with the same answers.
- **No release without an answer.** `onReady` does not release a detached edit
  (`blockEditOpen: false` is expected: the page has no editor for it). A full page replacement and
  a document switch still release it: the page's state is gone with it.
- **Do not clear a newer page editor.** Releasing a detached edit frees only the host hold
  (`held`). If a `pageEditorId` other than the detached `editId` was recorded since, it is kept,
  and the queued render waits for that editor (STAB-03).
- **An open that arrives during a detached edit** (a message already in flight; the page's wait
  makes it rare):
  - `handleEditOpen` does not refuse it with "Another Markdown block is already being edited.";
  - it holds it, at most one. A later open replaces it, and the replaced one is answered with the
    usual "Another Markdown block is already being edited." error, so its frame never stays on
    "Loading Markdown source…";
  - on success, the held open is handled with its usual checks;
  - on a failure, it is refused with that same error, since the failed editor reopens.

### 4. A final save that fails or meets an outside change keeps its text on screen (Q10, Q13, Q16, Q17)

The rule: the editor stays open, or reopens, on that block, with the text the writer typed and the
reason in its status line. That is the state an editor is in today after a refused final save
(BLOCK-216). Nothing is lost. No VS Code message is shown, except when the page cannot show the
text (Q17, below).

**How the page learns of it.** The host tells it with a `previewEditSource` that names the
`editId` and carries `error` and a new optional field `unsavedText`: the final text the host did
not write. Add the field to `PreviewEditSourceMessage` (`src/core/protocol/hostToPage.ts`). The
host adds it to every error answer to a final save:

- a refusal of `handleEditSave`: the message's `editedText`. It is posted on receipt, often before
  the page's Cancel reaches the host;
- an apply failure or rejection in `drainActiveBlockEdit`: the text being applied;
- the drain's "source block changed" refusal: the same;
- an outside change while a final save is requested or text is pending (below).

**An outside change while a final save waits** (save-guard-Q13 for a detached edit, Q16 for an
editor still open on "Saving…"). In `hostEvents.ts`, instead of today's silent release and
render, the host:

- posts the error "The file changed outside the preview before your text was saved. Copy your
  text, then reopen the block." with `unsavedText` (the pending or last final text), for the
  edit's `editId`;
- releases the host edit keeping the page editor (`releaseHostEditKeepingEditor`), as the
  conflict path of `trackOutsideChange` does today, so the text is not written;
- keeps `pageEditorId` set to that `editId` (it still is for an open editor; it is recorded again
  for a detached one), so the render waits for the editor.

For an editor still open (Q16), the page needs nothing new: it receives the error for its open
`editId`, so today's error answer applies (BLOCK-216). The editor stays open, `finishing` becomes
false, the text box keeps the typed text, the status shows the message, and the pending
navigation is cleared. The page posts no `previewEditReopen` for it. From there the writer is
where today's conflict message leaves them: a retry may meet the stale refusal, and Cancel or
Escape closes the editor, which releases the waiting render. For a detached edit (Q13), the page
reopens the editor as below.

**The page's answer: a positive signal.** On an error answer carrying `unsavedText` for an
`editId` it has no open editor for, the page always answers with a new page-to-host message
`previewEditReopen` (`editId`, `reopened: boolean`, addressed own-id, with its validator in
`src/core/protocol/pageToHost.ts`):

- `reopened: true` when it held the detached record for that `editId` and reopened the editor
  (below);
- `reopened: false` when it has no record for it (the page was replaced or reloaded) or cannot
  find the block.

**The host on a failure, until the page answers.** It keeps the edit as a failure leaves it today:

- held, for a drain failure;
- released with `releaseHostEditKeepingEditor`, for the "source block changed" refusal and the
  outside change.

It also records the `editId` as `pageEditorId` again (`lock.openPageEditor`), so renders and
reloads wait, and it keeps the `unsavedText` it sent, keyed by that `editId`, until the page
answers. This is also what happens when the page's `previewEditClosed` arrives after the host
already answered that final save with an error (the Cancel crossed the error): the close does not
detach the edit, and the host waits for `previewEditReopen`.

- On `reopened: true`, the host sets `watchedPageEditorId` to that `editId`: the reopened editor
  has `reportClose` set and reports its close like any watched editor. It forgets the kept text
  and then behaves as today after a failure.
- On `reopened: false` (save-guard-Q17), the host closes the page editor and releases the edit
  (`releaseActiveBlockEdit(preview, true)`), and renders. It also shows a VS Code warning with a
  **"Copy text"** action, for example "Your Markdown edit to <file name> could not be saved, and
  the preview could not show it again: <reason>". When the writer picks "Copy text", the host
  puts the kept `unsavedText` on the clipboard (`HostUi.writeClipboard`). Dismissing the message
  writes nothing. The host then forgets the kept text.

**The action button goes through the `HostUi` port.** `showWarning` takes no actions today. Add
optional action labels to it, for example `showWarning(message: string, ...actions: string[]):
PromiseLike<string | undefined>` resolving to the chosen label, implemented in
`src/host-vscode/vscodeHost.ts` (the one place that calls `vscode.window.showWarningMessage`) and
in every fake `HostUi` of the tests. The session code calls only the port; no `vscode` call is
added outside `src/host-vscode`. Existing callers pass no actions and are unchanged.

**The page's reopen.** On that error for `detachedSave.editId`:

- the page finds the block with the same lookup as `resumePendingBlockNavigation` (block id first,
  then source line and tag, then the table cell);
- it reopens a block or cell editor on it **with the same `editId` and without posting
  `previewEditOpen`**. A new internal entry, for example `reopenDetachedEdit(record, error, text)`,
  builds the editor as `openBlockEditor` does. It then sets the state that the source answer and
  the error answer would set today, from the record:
  - `originalText`, `trailingLineEnding`, `insertAfterLine`, `replaceBlankRun`,
    `deleteWhenEmpty`, `singleLine` and the cell-session state;
  - `hasAutosavedChange` true;
  - the text box holds `unsavedText` (or the record's `editedText` when the answer has none);
  - `finishing` false and `lastPostedText` cleared;
  - the status shows the error with `hintReplaced`;
  - `reportClose` set;
- the editor sends its retries with the record's `documentId`, `revision` and `requestId`, not the
  page's current render. Add one optional `BlockEdit` field, for example `saveIdentity`, read by
  `postBlockEditSave` when set. So a retry matches the held host edit (lines 532 to 545), even if
  a render reached the page in between;
- the caret goes to the end of the text, and the text box has the focus;
- the page posts `previewEditReopen` with `reopened: true`, clears `detachedSave`, and drops the
  pending block navigation and the pending field open (save-guard-Q14).

From there the writer is where BLOCK-216 leaves them today. Done posts a final save with that
`editId`, and Cancel or Escape cancels with `previewEditCancel`, because something reached the
document or was asked to.

**No other editor can be open at the failure.** While the record is set, no block, cell or field
editor opens (section 2), so the reopen never meets one.

### 5. Each save path ends: the hangs found, and the new rules

**Found by reading, fixed in this CR, with a failing test on the code before:**

- **H1, the frontmatter save that writes the text already there.**
  - Cause: a value, key or field action whose plan leaves the document text unchanged. One
    example is a YAML editor text that differs from `initialYaml` only in formatting and
    serialises to the same YAML. Another is any other no-op plan, since `planFrontmatterSave`
    does not refuse one.
  - What happens: `applyWrittenEdits` resolves true, so the host posts `saved: true`. No document
    change follows, so there is no render and no content patch. The field stays on "Saved.
    Refreshing preview…" with its control disabled and Escape ignored, for good.
  - Fix: in `handleSave`, when the planned text equals the document text, the host writes nothing
    and posts `previewFrontmatterResult` with `saved: true` and a new optional field
    `unchanged: true`. On `unchanged: true`, `receiveFrontmatterResult` closes the field editor at
    once with no message (save-guard-Q12), through `closeFrontmatterEditor("unchanged save")`.
    That applies the deferred properties markup, and `afterResult` runs.
  - The Driver first proves the hang with a failing test. If a no-op apply does fire a document
    change in the test host and the hang does not reproduce, the Driver reports it. The fix is
    then kept only if the real VS Code apply behaves as `applyWrittenEdits` says.
- **The outside change during "Saving…" loses the typed text** (save-guard-Q16). Today the host
  releases the edit without writing the queued text and renders, and the patch closes the editor.
  Fixed by section 4.

**Rules the new Cancel makes necessary** (no failing case exists before the change, because Cancel
did nothing during a save; the checks fail before only because the editor does not close):

- a detached edit that fails or meets an outside change gets its editor back (section 4).
  Without that, its text would be lost and its held edit would refuse every later open;
- a failure the page cannot show offers the text through "Copy text" (section 4, Q17);
- a detached edit always gets an answer naming its `editId`, and `onReady` does not release it
  (section 3);
- releasing a detached edit does not clear a newer page editor's lock (section 3).

**Read and found to end (each gets its test in the Evidence):**

- a host refusal of the final save gives an error answer;
- an apply failure or rejection gives an error answer;
- nothing to write gives `done`;
- a write gives a render, which ends in a content patch, a full page replacement, or a failed
  render (`setStatus` replaces the page);
- a hidden panel renders when shown (`renderIfDirty`);
- a patch never acknowledged gives a reload (`armContentPatchFallback`);
- an outside change gives an error answer (section 4);
- a document switch: `forgetPage`, and the new document replaces the page;
- the blank-lines editor's patch is closed by part A;
- frontmatter: an error answer, a content patch or a full replacement end the field editor.

The Driver reads these paths again on top of part A. **Any test that does not end is a new hang:
fix it here, and name it and its cause in the commit and the PR body.**

### 6. The frontmatter Escape rule is unchanged

Escape stays ignored while a frontmatter save is in flight, and the control stays disabled
(FMEDIT-001, FMEDIT-004). Nothing in `bindKeys`, `saveValue`, `saveKey` or
`postFrontmatterAction` changes, except H1's handling of `unchanged: true`. The openers also wait
while a detached save is in flight (section 2).

### 7. What stands against these rules today, and is changed here

- The early returns on `finishing` in `cancelBlockEdit`, `cancelTableCellEdit` and the cell
  editor's document-level Escape (section 1).
- The page test `Cancel and Escape are ignored while the final save is in flight`
  (`test/page/blockReq.requirements.test.ts`, `@tests_req SwRS-MDOKFSTUDIO-BLOCK-053`) asserts the
  old rule.
  - It is rewritten to the new rule and renamed `Cancel and Escape close the editor while the
    final save is in flight`. It is neither deleted nor kept as is.
  - Its assertion's intent changes because the owner changed the rule (save-guard-Q4), and the
    commit says so.
  - Its second half (Escape before any save cancels as usual) stays.
- The host's silent release and render on an outside change while a final save is requested or
  text is pending (section 4, save-guard-Q13 and Q16). Any test that asserts it changes with the
  rule and is named in the commit.
- The host posts `done` only when nothing renders; for a detached edit it now always posts it.
- `HostUi.showWarning` gains optional actions; its fakes in the tests follow.
- Any other existing test that asserts that Cancel or Escape does nothing during "Saving…" (the
  Driver finds them with `just check`) is handled the same way, and each one is named in the
  commit.

### 8. Requirements and vocabulary

Follow the project's requirements guidelines (IDs from `okfreq new`, markers move with the code,
`just requirements-update`, a log entry).

- **SwRS-MDOKFSTUDIO-BLOCK-053** (block-editing):
  - New title, for example "Cancel and Escape restore the saved text, or close the editor during
    a final save". It must be at most the guideline's title length.
  - The description adds: during a final save, the editor closes with no previewEditCancel, and
    the save completes.
  - The refusal scenario "Cancel is ignored while the final save is in flight" becomes a nominal
    scenario, "Cancel during a final save closes the editor and the save completes". It covers:
    - no previewEditCancel and no second final save;
    - the text kept in the document;
    - the pending navigation dropped;
    - a block or field clicked afterwards opening after the end.
  - Verification notes: the rewritten test by its new name. The criterion "cancelBlockEdit
    returns without a message when finishing is true" becomes "cancelBlockEdit closes the editor
    with previewEditClosed and no previewEditCancel when finishing is true". Add the session
    tests of section 3.
- **SwRS-MDOKFSTUDIO-BLOCK-216** (a refused open or save keeps the typed text and says why):
  - a scenario "A save that fails after Cancel, or meets a change of the file, reopens the editor
    with the typed text and the reason". It includes the dropped clicks;
  - a scenario "A change of the file while the editor saves keeps the editor open with the typed
    text and the reason" (Q16);
  - a scenario "A failure the preview cannot show offers the text to copy" (Q17).
- **SwRS-MDOKFSTUDIO-TABLE-025** (table-editing): a scenario "Escape or Cancel in a cell during a
  final save closes the editor with no message". It includes a cell left earlier, a Tab-added row
  and the focus outside the cell editor. Add its test to the verification notes.
- **SwRS-MDOKFSTUDIO-BLOCK-191** (the host holds and ends the block edit): a scenario "The page
  closed the editor during its final save". It covers:
  - the edit completing with no restore and always answered;
  - the open accepted after the end;
  - a newer editor's lock kept;
  - a failure or an outside change keeping the page editor lock until the page confirms the
    reopen;
  - on `reopened: false`, the release and the "Copy text" message.

  And a scenario "An outside change during a final save keeps the text unwritten and the editor
  open" (Q16).
- **New SwRS** (block-editing), title for example "Every final save of a block or cell editor
  ends": each save path listed in section 5 ends in a closed editor or a shown error. It derives
  from StRS-MDOKFSTUDIO-BLOCK-006 and depends on BLOCK-216, BLOCK-263 and BLOCK-191.
- **The gestures during an edit in flight** (save-guard-Q15): a scenario on the SwRS that already
  says a gesture waits for an open editor. The Driver finds it from the markers at the guards; if
  none exists, a new SwRS "No edit gesture runs while an edit is in flight". It covers the open
  editor and the detached save.
- **Frontmatter** (frontmatter-editing):
  - a scenario on SwRS-MDOKFSTUDIO-FMEDIT-019 (or the frontmatter save SwRS the guidelines point
    to): "A save that changes no text closes the field editor with no message";
  - a scenario stating that every frontmatter save (value, key, field action) ends in a closed
    editor or a shown error;
  - a scenario on the field-open SwRS: "A field clicked while a cancelled block save is in flight
    opens when it ends, and is dropped if it fails" (save-guard-Q14).
- **StRS-MDOKFSTUDIO-BLOCK-006** (`proposed`): its wording changes with the code, with no
  re-approval. "Cancel or Escape as restoring the block" gets the nuance "or, once Done was
  pressed, as closing the editor while the save completes; if that save cannot be written, the
  typed text comes back in the editor, or is offered to copy".
- **SwRS-MDOKFSTUDIO-BLOCK-047**: no change. Its boundary scenario "A second final save is
  refused while the first is in flight" stays true, because there is no retry and nothing posts
  a second final save. The first specification's changes to it are dropped.
- **Glossary**: "Detached save" and "Edit in flight" (see "Words"). No "Save time limit" and no
  "Timed-out editor".
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes.

### Protocol validators

- **`previewEditSource`**: add an `isValid` that accepts:
  - `error` as a string;
  - `done` and `renderFollows` as `true`;
  - `unsavedText` as a string of at most 20 MB (the content patch's bound; one constant shared
    with `MAX_PATCH_CONTENT_LENGTH`);
  - the other fields as typed today.
- **`previewFrontmatterResult`**: add an `isValid` that accepts `saved` and `unchanged` as `true`,
  and `error` as a string.
- **`previewEditReopen`** (page to host): `editId` a string, `reopened` a boolean.

### Size limits (decision 3)

- `src/page/features/pageRuntime.ts` is 793 lines (limit 800): it gets only the `detachedSave`
  field and the `saveIdentity` field, with a one-line comment each. The `DetachedSave` type lives
  in its own module. If more is needed, move a type out rather than pass the limit.
- `src/page/features/blockEditor.ts` (649) takes the Cancel change only. The record, its end, the
  wait, the reopen and `editInFlight` go in a new module, for example
  `src/page/features/detachedSave.ts`.
- `test/page/runtimeFrontmatterEditor.test.ts` is 1 396 lines (limit 1 500): new frontmatter tests
  go in a new file, not there.
- `src/session/features/blockEdits.ts` (729): the detached-edit handling, the kept unsaved text
  and the "Copy text" message go in a small module beside it, for example
  `src/session/features/detachedEdits.ts`, if they would pass its limit.

## Out of scope

- The hang part A fixes and its regression test (CR `blank-run-edit-stuck-saving`).
- One blank-line block per blank line (CR `blank-line-block-per-line`).
- Any time limit, timeout message, retry message, `stale` mark on host refusals, or save-to-render
  measure (save-guard-Q9).
- Undoing a save on Cancel: the save asked for with Done is kept (save-guard-Q4).
- The frontmatter Escape rule during a save (unchanged, section 6).
- An autosave that fails while the final save is queued. It ends in an error, not in "Saving…";
  pressing Done again may then meet a "source block changed" refusal. It is noted here, not
  changed.
- Merging the typed text into a file changed outside: the writer copies it and reopens the block,
  as today's conflict message says.
- The release notes, written when the release is prepared.

## Evidence

The checks run the real page bundle, the real host session code and the real protocol module at
the head under test, never a prepared copy. Each check for a fix or a new rule fails on the code
before the change (constitution, section 3), and the Driver shows each failure once. The checks
marked "before and after" prove an already-ending path and pass on both.

**Page, every save path ends** (new file `test/page/runtimeSaveEnds.test.ts`; before and after).
Each check runs for a paragraph editor and for a table cell editor: type, press Done ("Saving
Markdown…" shows), then send one of these answers:

1. a content patch: the editor is closed;
2. `previewEditSource` `done: true`: the editor is closed;
3. an error answer (each host refusal text of `handleEditSave`, "VS Code could not apply the
   Markdown edit.", and the "file changed outside the preview" text with `unsavedText`): the
   editor is open, `finishing` is false, the error shows, the text is kept, and no
   `previewEditReopen` is posted;
4. a full page replacement: no editor;
5. the move chord, the arrow and Tab navigation, a Tab-added row and a click on another block,
   each followed by `done` or a patch: the editor closes, and the pending navigation then opens
   its target.

In every run the end state is a closed editor or a shown error, never `finishing` with no answer
pending.

**Page, Cancel during a final save** (new file `test/page/runtimeDetachedSave.test.ts`):

6. Cancel, and in another run Escape in the text box, during "Saving Markdown…":
   - the editor closes and `state.activeBlockEdit` is undefined;
   - one `previewEditClosed` with its `editId` is posted;
   - no `previewEditCancel` and no second `previewEditSave` is posted.
7. The same in a cell editor:
   - with a cell left earlier (kept-cell branch);
   - with a Tab-added row;
   - with Escape while the focus is outside the cell editor (`bindKeys`).
8. Dropped navigation. Press the move chord, an arrow at the block edge, Tab on the last row, and
   a click on another block; each posts the final save. Then press Cancel. Then send `done` (in
   another run `done` with `renderFollows` and then a patch): no editor opens, no block moves,
   and the selection is on the edited block.
9. A content patch alone after the Cancel (a render already in flight) does not end the detached
   save: a following error for its `editId` still reopens the editor.
10. A block opened after the Cancel (save-guard-Q11): a double-click on another block posts no
    `previewEditOpen`.
    - After `done` without `renderFollows`, one `previewEditOpen` is posted for that block.
    - After `done` with `renderFollows`, none is posted until the patch, then one is posted with
      the page's new revision.
11. A frontmatter field clicked after the Cancel (save-guard-Q14): no field editor opens until the
    end. It opens after `done` (and the patch when `renderFollows`), and it does not open after a
    failure.
12. **An edit in flight** (save-guard-Q15), one table-driven test. Run each gesture in two states,
    with an editor open and with a detached save: a block move, a delete, a paste, a checkbox
    toggle, a table row drag, a list-item drag, a file drop and a replace. Each posts nothing
    (no edit message and no `previewEditOpen`) and changes nothing.
13. Cancel with no final save posted behaves as BLOCK-053 says, with and without an autosave
    (before and after for the Escape half).

**Page, a detached save that fails** (save-guard-Q10; same file). Run each check for a paragraph
editor, a cell editor (with a kept cell and a Tab-added row), an insertion editor
(`insertAfterLine`) and a blank-lines block editor (`replaceBlankRun`). Type "new words", press
Done (keep the posted `previewEditSave` as M1), press Escape, then send `previewEditSource` with
`error` and `unsavedText: "new words"` for that `editId`:

14. The editor is open again on the same block (the same cell, the same insertion point), with the
    same `editId`; no `previewEditOpen` was posted; the text box holds "new words"; the status
    shows the error; `finishing` is false; the text box has the focus. The page posted
    `previewEditReopen` with `reopened: true`.
15. Done then posts M2. M2 equals M1 in every field except the one-shot pin, anchor and `flush`
    fields: the same `documentId`, `revision`, `requestId`, `editId`, `line`, `endLine`,
    `originalText`, `editedText`, `insertAfterLine`, `replaceBlankRun` and `deleteWhenEmpty`. This
    holds even when a content patch arrived between the Cancel and the error. M1 and M2 feed the
    host test "retry after a reopen" below.
16. Escape in the reopened editor posts `previewEditCancel` (BLOCK-053, after an autosave).
17. An error answer without `unsavedText`: the editor reopens with M1's `editedText`.
18. A block and a field clicked between the Cancel and the error: no `previewEditOpen` is posted
    and no field editor opens, before or after the error; only the failed editor reopens.
19. An error with `unsavedText` for an `editId` the page has no record of: the page posts
    `previewEditReopen` with `reopened: false` and opens nothing.
20. **Outside change** (save-guard-Q13): the error "The file changed outside the preview before
    your text was saved…" with `unsavedText` reopens the editor with the typed text and that
    message.

The rewritten test of `test/page/blockReq.requirements.test.ts` carries `@tests_req
SwRS-MDOKFSTUDIO-BLOCK-053`. The cell checks carry `@tests_req SwRS-MDOKFSTUDIO-TABLE-025`, the
reopen checks carry `@tests_req SwRS-MDOKFSTUDIO-BLOCK-216`, and the path checks carry the new
SwRS's `@tests_req`.

**Page, frontmatter** (a new `test/page/runtimeFrontmatterSaveEnds.test.ts`). For a value save, a
key rename and a field action (add and remove):

- an error answer: the control is enabled, the error shows, and Escape closes (before and after);
- `saved: true` then a content patch: the field editor is closed (before and after);
- **H1**: `saved: true` with `unchanged: true`: the field editor is closed at once, no message
  shows, and the deferred properties table is applied;
- while each save is in flight, Escape does nothing and the control is disabled (the rule kept;
  before and after).

**Host** (`test/session/`, for example a new `test/session/detachedSave.test.ts` beside
`blankRunHost.test.ts`):

- **H1**: a `previewFrontmatterSave` whose plan leaves the text unchanged (for example a YAML text
  that serialises to the same frontmatter) gets `saved: true, unchanged: true`, and the document
  is untouched. This fails before the fix: no `unchanged`, and no render follows.
- **Decision 1, (a)** (before and after): a final save is written and completed. Then
  `previewEditClosed` for its `editId`, then a `previewEditOpen` at the rendered revision. The
  open is accepted (`previewEditSource` with `originalText`), and the document holds the saved
  text.
- **Decision 1, (b)** (before and after): an autosave is applied, and the final save is queued or
  applying (the apply held back). Then `previewEditClosed`, then the apply resolves. The edit
  completes with no restore, `edits.active` is undefined, and the render runs. A
  `previewEditOpen` at the rendered revision is accepted.
- **Every detached end is answered**: in (b) the page gets `done: true` with
  `renderFollows: true`; with nothing to render, `done: true` alone. A `previewReady` with
  `blockEditOpen: false` before the apply resolves does not release the detached edit.
- **Decision 1, (c)**: as in (b), but a `previewEditOpen` arrives before the apply resolves, and a
  second one after it.
  - The first is answered with "Another Markdown block is already being edited." when the second
    replaces it.
  - The second is answered after the detached edit ends.
  - When that answer opens an editor, its `pageEditorId` is still set after the release, and the
    render result of the detached save waits for it.
- **Failure** (Q10): as in (b), with the apply failing, and in another run rejecting.
  - The page gets `previewEditSource` with the `error`, the `editId` and `unsavedText` equal to
    the final text; no VS Code message is shown.
  - `pageEditorId` is that `editId` again, so a render waits.
  - After `previewEditReopen` with `reopened: true`, `watchedPageEditorId` is that `editId`, and
    no VS Code message is shown.
- **Retry after a reopen**: after that failure and the reopen, M2 from page check 15 is accepted
  against the held edit (no "stale" refusal) and written.
- **Refusal crossing the close**: a final save refused by `handleEditSave`, then
  `previewEditClosed` for its `editId`.
  - The refusal carries `unsavedText`.
  - The close does not detach anything and does not clear `pageEditorId`.
  - After `previewEditReopen` with `reopened: true`, M2 is handled as today after a refusal.
- **The failure meets a page with no record** (Q17): after a failure, `previewEditReopen` with
  `reopened: false`.
  - The edit is released, `pageEditorId` is cleared, the render runs, and a later
    `previewEditOpen` at the rendered revision is accepted.
  - The fake `HostUi` records one warning that names the file and offers the "Copy text" action.
  - When the fake picks "Copy text", `writeClipboard` receives the `unsavedText` exactly. In
    another run it dismisses the message, and `writeClipboard` is not called.
  - The same holds after an outside change met by `reopened: false`.
- **Source block changed**: the drain's refusal of a detached edit carries `unsavedText`, and
  `pageEditorId` is that `editId` again.
- **Outside change, detached** (Q13): a detached edit with its final save queued (the apply held
  back). A change of the document from outside the preview gives the "file changed" error with
  `unsavedText`. The edit's text is not written, `pageEditorId` is that `editId`, and the render
  waits for the page's answer. Before the change: a silent release and render (this check fails).
- **Outside change, editor still open** (Q16): the same, with no `previewEditClosed` (the page
  editor still on "Saving…"). The page gets the "file changed" error with `unsavedText` for its
  `editId`; the text is not written; `pageEditorId` stays that `editId` and the render waits; no
  VS Code message is shown. After `previewEditClosed` for it, the render runs. Before the change:
  a silent release and render, and no error (this check fails).
- `previewEditClosed` after a `previewEditCancel` (an edit with `cancelRequested`) still restores
  the original text: the detached rule does not apply (before and after).

**Host port** (the `vscodeHost.ts` adapter, in its existing unit tests if any, otherwise checked
through the real VS Code run): `showWarning` with actions passes them to
`vscode.window.showWarningMessage` and resolves to the chosen label; without actions it behaves
as today.

**Protocol** (the protocol tests of `hostToPage.ts` and `pageToHost.ts`):

- `previewEditSource` with `unsavedText` (a string within the bound), `renderFollows: true` and
  `done: true` is accepted;
- a non-string `unsavedText`, a text over the bound, or `renderFollows` or `done` other than
  `true` is refused;
- `previewFrontmatterResult` with `unchanged: true` is accepted, and with a non-`true` `unchanged`
  is refused;
- `previewEditReopen` without a boolean `reopened` is refused.

**Real VS Code** (`just ci-integration`, on the heavy run): one scenario in
`test/integration/previewEditing.test.ts` or its real-input group.

- Add a test hook beside `holdEditSourcesForTests` in `src/host-vscode/testHooks.ts`, for example
  `holdBlockEditAppliesForTests`. It holds the drain's apply of the active preview's block edit
  until `release()`.
- Steps:
  1. With the hook set, type in a paragraph, press Done, then press Escape.
  2. Assert that the editor frame is gone while the apply is still held.
  3. Release the hook.
  4. The file holds the typed text, and no editor shows "Saving Markdown…".
  5. Open the next block: its editor opens with its source.

**Requirements:** `just requirements-lint` and `just requirements-update` pass. Every updated or
new SwRS has its `@implements_req` at the code above and its `@tests_req` at each test above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

Technical choices the answers leave to the specification, for the Chief of Staff to check:

1. **The page ends a detached save only on an answer naming its `editId`** (`done` or an error),
   and the host answers every end. A render in flight therefore cannot end it early. `done`
   carries `renderFollows`, so the clicked block opens on the new render.
2. **The host holds an open that arrives during a detached edit** (at most one, the replaced one
   answered), as a second line behind the page's wait.
3. **A failed detached save reopens with the same `editId`, the first save's identity and no new
   `previewEditOpen`**. The reopened editor is in exactly the state BLOCK-216 leaves today, and its
   retry matches the held host edit.
4. **The page confirms the reopen with `previewEditReopen`**. The host keeps the editor's lock
   until that answer and releases on `reopened: false`. This is a positive signal in place of
   ignoring a close.
5. **The host sends the unsaved text** (`unsavedText` on every error answer to a final save). The
   page's record is the fallback.
6. **The outside change (Q13, Q16) reuses today's conflict path**: an error that tells the writer
   to copy the text, the host edit released, and the page editor kept. For an open editor the page
   needs no change.
7. **One `editInFlight()` helper** guards every edit gesture, for the open editor and the detached
   save alike (Q15).
8. **H1 is fixed on the host** with `unchanged: true`, rather than by a YAML-normalising check on
   the page. The host is the one place that knows the text did not change.
9. **The `detached` flag applies only to an edit that is not `cancelRequested`**, so today's
   Cancel before Done (restore) is untouched.
10. **The new texts are bounded at 20 MB**, the content patch's bound, and validated.
11. **The "Copy text" message (Q17) is a warning through `HostUi.showWarning` with optional
    actions**, and the host keeps the unsaved text only until the page answers
    `previewEditReopen`. Its wording names the file and the reason.

## Open questions

None. Q10 to Q17 answered every behaviour question this specification raised.
