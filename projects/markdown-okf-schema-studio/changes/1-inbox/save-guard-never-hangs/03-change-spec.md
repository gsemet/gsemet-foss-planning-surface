# No edit stays on Saving Markdown for good

Every final save of a block or table cell editor ends, within 10 seconds at most, in the rendered
block or in a message the editor shows. A frontmatter save is bounded the same way, its "Saved.
Refreshing preview…" wait included. Cancel and Escape always close a block or cell editor, even
while it shows "Saving Markdown…"; the save the writer already asked for with Done goes on.

Short name: `save-guard`. Destination: the running batch-09, in its stack.

## Goal

CR `blank-run-edit-stuck-saving` (part A, short name `blank-save`) fixes the one hang the issue
found: the editor of a blank-lines block stayed on "Saving Markdown…" because the content patch
never closed it. That fix does not stop the next hang of the same kind. Today nothing on the page
bounds the wait for the answer of a final save: a save whose answer never comes (no content patch,
no `done`, no error) leaves the editor on "Saving Markdown…" for good, and Done and Cancel do
nothing while it waits. This CR makes sure no edit, of any block kind, can hang that way again.

The owner's answers (`02-answers.md`):

- **Tests and a guard** (save-guard-Q1): every final save ends in success or in a shown error,
  with a time limit; Cancel always closes the editor.
- **The frontmatter time limit runs until the editor closes or an error shows** (save-guard-Q2):
  "Saved. Refreshing preview…" is bounded too.
- **A neutral timeout message** (save-guard-Q3): "No answer yet; your text may already be saved",
  Done to try again, Cancel to close. A stale refusal on the retry reads as already saved or
  changed, and tells the writer to close the editor.
- **Cancel during "Saving…" closes the editor and the save goes on** (save-guard-Q4); the text
  is kept.
- **10 seconds, checked by a measure** (save-guard-Q5): the save-to-render time on the largest
  fixture; back to the owner through the Chief of Staff if the slowest time is over half the limit.
- **Stack order** (save-guard-Q6): after `blank-run-edit-stuck-saving`, before
  `blank-line-block-per-line`.

Project rules: this change follows the project's constitution (`.agents/constitution.md`), its
`AGENTS.md` (requirements, completion gate `just preflight`) and the requirements guidelines named
there. This specification restates none of them.

## What this CR builds on

- **Part A** (`blank-run-edit-stuck-saving`, the branch below this one in the stack) changes
  `applyContentPatch` (`src/page/features/contentPatch.ts`): the exception that keeps a blank-lines
  block's editor open across a content patch (`replaceBlankRun`, CR-444 fix 7) holds only while no
  final save of that editor is in flight (`finishing`); once one was posted, the patch closes the
  editor with `closeBlockEdit(false)`. Part A carries its own regression test. This CR does not
  repeat that fix or its test; it extends A's condition to the timed-out state (section 2).
- **Part C** (`blank-line-block-per-line`, above this one) is out of scope (see "Out of scope").

## What exists today

Read from the code at `main` (`d9b3cd6b`); the Driver reads it again on top of part A.

- **Block and cell editor, final save.** `postBlockEditSave(true)` in
  `src/page/features/blockEditor.ts` sets `edit.finishing = true`, shows "Saving Markdown…" in
  `edit.status` and posts `previewEditSave` with `final: true`. Nothing starts a timer. The editor
  closes only on:
  - a content patch (`applyContentPatch` calls `closeBlockEdit(false)`);
  - `previewEditSource` with `done: true`, handled in `receiveBlockEditSource`
    (`src/page/features/blockSourceEditor.ts`), which closes only `if (edit.finishing)`
    (SwRS-MDOKFSTUDIO-BLOCK-263);
  - an error answer (`previewEditSource` with `error`) does not close it: it sets
    `finishing = false`, clears `lastPostedText`, `pendingBlockNavigation` and
    `pendingBlockSelection`, and shows the error (SwRS-MDOKFSTUDIO-BLOCK-216).
- **While `finishing` is true**, `postBlockEditSave` returns early (Done does nothing), and so do
  `cancelBlockEdit` (`blockEditor.ts`, `if (!edit || edit.finishing) return;`) and
  `cancelTableCellEdit` (`src/page/features/tableCellEditor.ts`, `if (edit.finishing) return;`
  under the `@implements_req SwRS-MDOKFSTUDIO-TABLE-025` marker). This is the
  SwRS-MDOKFSTUDIO-BLOCK-053 refusal scenario "Cancel is ignored while the final save is in
  flight", checked by the page test `Cancel and Escape are ignored while the final save is in
  flight` (`test/page/blockReq.requirements.test.ts`, `@tests_req SwRS-MDOKFSTUDIO-BLOCK-053`).
  The Cancel button (`createEditorButtons`), Escape in the text box (`blockSourceEditor.ts`,
  through `rt.selection.finishEditorWithSelection("cancel", ...)`) and Escape in a cell
  (`tableCellEditor.ts`, the keydown handler and the document-level handler of `bindKeys`) all
  reach these two functions.
- **The host.** `handleEditSave` (`src/session/features/blockEdits.ts`) refuses a save that does
  not match the document or the held edit with `postEditSourceError`: "The preview is stale.
  Reopen the block before saving." (twice), "The source block changed while it was being edited."
  (twice), a `BlockRangeRefusal` of `currentSourceEdit`, and "The preview block edit is stale.
  Reopen the block before saving.". After a final save that wrote text, `completeActiveBlockEdit`
  releases the host edit and asks for a render; with nothing to render it posts `done: true`. A
  retried final save that arrives after the host already completed the first one re-creates the
  edit from the document and meets one of these refusals, because the block already holds the new
  text or the page's revision is old.
- **Frontmatter saves.** Three places post `previewFrontmatterSave` and set `edit.saving = true`
  with the controls disabled: `saveValue` in `src/page/features/frontmatterValueEditor.ts`
  ("Saving frontmatter…"), `saveKey` (key rename, "Saving frontmatter key…") and
  `postFrontmatterAction` (field menu add or remove) in `src/page/features/frontmatterEditor.ts`.
  `receiveFrontmatterResult` (`frontmatterEditor.ts`) shows "Saved. Refreshing preview…" on
  `saved: true` and keeps `saving` true; the editor closes when the content patch calls
  `closeFrontmatterEditor("content patch")`. On an error it shows the error with
  `data-state="error"`, sets `saving` false, enables the controls again, records `refusedText`,
  runs `afterResult` and puts the focus back (SwRS-MDOKFSTUDIO-FMEDIT-019). Nothing bounds either
  wait.
- **Timers in tests.** The page harness (`test/page/runtimeHarness.ts`) has `advanceTimers(ms)`
  (honours delays) and `flushTimers()` (runs every timer, ignoring its delay).

## Words

- **Final save**: the `previewEditSave` with `final: true` that Done, Ctrl/Cmd+Enter, a blur out of
  the editor, a move chord or a flush posts (`postBlockEditSave(true)`); for the frontmatter, any
  `previewFrontmatterSave`.
- **Save time limit**: `FINAL_SAVE_TIMEOUT_MS`, 10 000 ms, the most a final save or a frontmatter
  save waits for its end before the editor shows the timeout message.
- **Timed-out editor**: a block or cell editor whose final save reached the save time limit with no
  end; it stays open, with its text, until it closes.

Add "Save time limit" and "Timed-out editor" to `.agents/glossary/common.md`.

## What changes

### 1. One save time limit (save-guard-Q5)

Add `export const FINAL_SAVE_TIMEOUT_MS = 10_000;` to `src/page/pageSettings.ts`, beside
`AUTOSAVE_DELAY_MS`, with a comment that names the measure of the Evidence. Block, cell and
frontmatter saves use this one constant.

### 2. Every final save of a block or cell editor ends (save-guard-Q1, Q3)

State: add to `BlockEdit` (`src/page/features/pageRuntime.ts`) `finalSaveTimer?: number` and
`finalSaveTimedOut?: boolean`. If `blockEditor.ts` would pass 800 lines, put the timer code in a
new module (for example `src/page/features/finalSaveGuard.ts`) rather than grow the baseline.

- **Start.** When `postBlockEditSave(true)` posts a final save, it starts (or restarts) one timer
  of `FINAL_SAVE_TIMEOUT_MS` on that edit. A final save that closes the editor without posting
  (unchanged text, nothing autosaved) starts none. This covers the block editor and the table cell
  editor, which share `postBlockEditSave`, and every caller of it (Done, Ctrl/Cmd+Enter, blur, the
  move chord `moveBlockFromEditor`, `flushOpenEditors`, `blockSelectionView.ts`, `editMode.ts`).
- **Clear.** The timer is cleared:
  - in `closeBlockEdit`, which covers a content patch, `done: true`, Cancel and every other close;
  - in `receiveBlockEditSource` when an error answer arrives for that edit.
- **Timeout.** When the timer fires and `state.activeBlockEdit` is still that edit with
  `finishing` true:
  - `finishing` becomes false, `lastPostedText` is cleared, `pendingBlockNavigation` and
    `pendingBlockSelection` are cleared, as the error answer does today, and
    `finalSaveTimedOut` becomes true (it stays true until the editor closes);
  - the status line shows exactly: **"No answer yet; your text may already be saved. Press Done
    to try again, or Cancel to close the editor."** (`hintReplaced` set as for an error);
  - Done posts the final save again (`postBlockEditSave(true)`, which restarts the timer);
  - the writer can go on typing; the editor keeps its text.
- **A late end still closes the editor.** While `finalSaveTimedOut` is true:
  - a content patch closes the editor. For an ordinary block this is today's behaviour; for a
    blank-lines block editor, part A's condition in `applyContentPatch` ("a final save was
    posted") is extended from `finishing` to `finishing || finalSaveTimedOut`;
  - `done: true` closes it: the check in `receiveBlockEditSource` becomes
    `if (edit.finishing || edit.finalSaveTimedOut)`, and the pending navigation resumes only when
    `finishing` was true (after a timeout it was cleared);
  - a late error answer shows its text, as today, except a stale refusal (next item).
- **A stale refusal on the retry** (save-guard-Q3).
  - Host: every refusal that `handleEditSave` posts (the six `postEditSourceError` calls listed in
    "What exists today", the `BlockRangeRefusal` included) carries a new optional field
    `stale: true`. Add `stale?: true` to `PreviewEditSourceMessage`
    (`src/core/protocol/hostToPage.ts`) and pass it through `postEditSourceError` (an optional
    parameter). Refusals of other messages (open, cancel, apply failures, outside changes) do not
    carry it.
  - Page: when an error answer with `stale: true` arrives and the editor is timed out
    (`finalSaveTimedOut`), the status shows exactly **"Already saved, or the block changed since.
    Press Cancel to close the editor."** in place of the host's text. The editor stays open with
    its text (see open question 1). Without `finalSaveTimedOut`, the host's text shows as today.

### 3. Cancel and Escape always close a block or cell editor (save-guard-Q4)

- `cancelBlockEdit` (`blockEditor.ts`) no longer returns early on `finishing`:
  - **a final save in flight (`finishing`) or a timed-out editor (`finalSaveTimedOut`)**: the
    editor closes with `closeBlockEdit(false)`: no `previewEditCancel`, no second final save. The
    save the writer asked for with Done goes on and completes on the host; its text is kept in the
    document. The page stops waiting for it. A late `done` or error for that `editId` finds no
    editor and is ignored, as today; the content patch of its render applies as for any patch;
  - **no final save posted**: unchanged (BLOCK-053): `closeBlockEdit(edit.hasAutosavedChange)`.
- `cancelTableCellEdit` (`tableCellEditor.ts`): its first line `if (edit.finishing) return;` is
  replaced: when `edit.finishing || edit.finalSaveTimedOut`, it calls `cancelBlockEdit()` at once
  (close, no message), before the Tab-row and kept-cell branches, so Cancel and Escape in a cell
  during a final save post neither `previewEditCancel` nor a second final save. Otherwise it is
  unchanged (TABLE-025). The `@implements_req SwRS-MDOKFSTUDIO-TABLE-025` marker stays at the
  function.
- The host side is unchanged: its edit lock is released when the save ends, and the page reports
  the close with `previewEditClosed` when the editor has `reportClose`, as today. The page's next
  `previewReady` carries `blockEditOpen: false`.
- `finishEditorWithSelection("cancel", ...)` (`blockSelection*.ts`) keeps its rule; with the
  editor closed and nothing pending, the selection goes to the edited block at once.

### 4. Every frontmatter save ends (save-guard-Q2, Q3)

State: add `saveTimer?: number` to `FrontmatterEdit` (`pageRuntime.ts`).

- **Start.** Each of the three places that post `previewFrontmatterSave` (`saveValue`, `saveKey`,
  `postFrontmatterAction`) starts one timer of `FINAL_SAVE_TIMEOUT_MS` on the edit, beside
  `saving = true`. Use one helper of the frontmatter editor (for example
  `rt.frontmatter.startSaveTimer(edit)`) so the three places share it.
- **It runs until the editor closes or an error shows** (save-guard-Q2). It is cleared in
  `closeFrontmatterEditor` (which the content patch calls) and on an error result in
  `receiveFrontmatterResult`. A `saved: true` result does not clear it: "Saved. Refreshing
  preview…" is bounded by the same timer, counted from the post.
- **Timeout.** When it fires with that edit still `state.activeFrontmatterEdit` and `saving`
  true, the editor takes the existing error path of `receiveFrontmatterResult` (factored into one
  function both use): the status shows exactly **"No answer yet; your text may already be saved.
  Press Enter to try again, or Escape to close the editor."** with `data-state="error"`, `saving`
  becomes false, the controls are enabled again, `refusedText` is recorded, `plainSavePending`
  becomes false, `afterResult` runs and the focus comes back as for a refusal. Enter saves again
  (`saveValue` or `saveKey`), Escape closes the editor (FMEDIT-019). A result that arrives after
  the timeout for the same `editId` is handled as today (a `saved: true` shows "Saved. Refreshing
  preview…", an error shows its text); the content patch still closes the editor.
- The frontmatter editor's Escape and Cancel behaviour is otherwise unchanged (its control is
  disabled during a save, so the timeout is what gives the writer Escape back).

### 5. What stands against these rules today, and is changed here

- The early return on `finishing` in `cancelBlockEdit` and in `cancelTableCellEdit` (section 3).
- The page test `Cancel and Escape are ignored while the final save is in flight`
  (`test/page/blockReq.requirements.test.ts`, `@tests_req SwRS-MDOKFSTUDIO-BLOCK-053`) asserts the
  old rule. It is rewritten to the new one and renamed (for example `Cancel and Escape close the
  editor while the final save is in flight`), not deleted and not kept: its assertion's intent
  changes because the owner changed the rule (save-guard-Q4), and the commit says so
  (constitution, section 3). Its second half (Escape before any save cancels) stays.
- Existing page tests that call `flushTimers()` while a final save or a frontmatter save waits now
  also fire the save time limit. The Driver runs `just check` early, finds them, and moves each to
  `advanceTimers` with a delay below the limit, or answers the save first; an assertion's intent
  never changes for this, and each changed test is named in the commit.

### 6. Requirements, vocabulary and docs

Follow the project's requirements guidelines: IDs come from `okfreq new`, markers move with the
code, run `just requirements-update`, add a dated entry in `requirements/tiers/log.md`.

- **Update SwRS-MDOKFSTUDIO-BLOCK-053** (scope `block-editing`): the normative text says Cancel and
  Escape always close the editor; the refusal scenario "Cancel is ignored while the final save is
  in flight" becomes a nominal scenario "Cancel during a final save closes the editor and the save
  completes" (no `previewEditCancel`, no second final save; the text is kept in the document), with
  a row for a timed-out editor. Its verification notes change with it:
  - the Method line of `test/page/blockReq.requirements.test.ts` names the rewritten test by its
    new title;
  - the criterion "cancelBlockEdit returns without a message when finishing is true" becomes
    "cancelBlockEdit closes the editor without a message when finishing or finalSaveTimedOut is
    true".
- **Update SwRS-MDOKFSTUDIO-TABLE-025** (scope `table-editing`): a scenario "Escape or Cancel in a
  cell during a final save closes the editor with no message", its test in the verification notes,
  and `finalSaveTimedOut` in its criteria.
- **Update SwRS-MDOKFSTUDIO-BLOCK-263**: `done: true` also closes a timed-out editor.
- **New SwRS (block-editing)**, title for example "A block editor's final save always ends": when
  no end comes within the save time limit, the page shows the timeout message and enables Done and
  Cancel again; Done retries; a late content patch or `done` still closes the editor; a stale
  refusal on a timed-out editor shows the "Already saved, or the block changed since" message. It
  holds for the block editor and the table cell editor. It derives from StRS-MDOKFSTUDIO-BLOCK-006
  and depends on BLOCK-216 and BLOCK-263.
- **Frontmatter (frontmatter-editing)**: a scenario on SwRS-MDOKFSTUDIO-FMEDIT-019 (the field save
  "shows the progress and the outcome"), or a new SwRS if the requirements guidelines prefer it: a
  save with no end within the save time limit, before or after "Saved. Refreshing preview…", shows
  the timeout message, enables the field again, and Enter retries.
- **StRS.** StRS-MDOKFSTUDIO-BLOCK-006 says Cancel or Escape restores the block. That holds for an
  editor before Done; during a final save, Done was already pressed. Its text is not changed by
  this CR (open question 2). If the Driver finds that it must change, its re-approval goes to the
  owner through the Chief of Staff before the change is ready.
- **Glossary** (`.agents/glossary/common.md`): "Save time limit" and "Timed-out editor", as in
  "Words".
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes.

## Out of scope

- The hang part A fixes (the content patch that did not close a blank-lines block's editor) and
  its regression test: in CR `blank-run-edit-stuck-saving`.
- One blank-line block per blank line, typing, pasting and deleting one line: CR
  `blank-line-block-per-line`.
- A time limit for other messages: block moves, pastes and cuts (`blocksFlight` and the move
  timeouts), checkbox toggles, label renames, find and replace, the open of an editor
  (`previewEditOpen`) and its cancel (`previewEditCancel`).
- Undoing a save on Cancel: the save the writer asked for with Done is kept (save-guard-Q4).
- The host's own waits and timers (`CONTENT_PATCH_ACK_TIMEOUT_MS`, `PENDING_OVERLAY_DELAY_MS` in
  `src/session/features/pageLoadState.ts`).
- The release notes, written when the release is prepared.

## Evidence

The checks run the real page bundle, the real host session code and the real protocol module at the
head under test, never a prepared copy. Each check below fails on the code before the change
(constitution, section 3); the Driver shows each failure once before the fix.

**Page, block and cell editor** (new file, for example
`test/page/runtimeFinalSaveGuard.test.ts`, with the harness's `advanceTimers`; one check per rule,
each run for an ordinary paragraph editor and for a table cell editor):

1. Type, press Done: "Saving Markdown…" shows. Advance `FINAL_SAVE_TIMEOUT_MS − 1`: still saving,
   nothing posted. Advance 1 more: the status reads the timeout message exactly, `finishing` is
   false, the text box holds the typed text.
2. After the timeout, Done posts one more `previewEditSave` with `final: true` and "Saving
   Markdown…" shows again; a second wait of the limit shows the message again.
3. After the timeout, a content patch closes the editor (`state.activeBlockEdit` undefined); in
   another run, `previewEditSource` `done: true` closes it.
4. After the timeout and Done, an error answer with `stale: true` shows "Already saved, or the
   block changed since. Press Cancel to close the editor."; an error answer with `stale: true`
   before any timeout shows the host's text; an error answer without `stale` after the timeout shows
   the host's text.
5. An error answer before the limit stops the timer: advancing past the limit changes nothing.
6. A content patch or `done` before the limit closes the editor, and advancing past the limit
   posts nothing and throws nothing.
7. Cancel, and in another run Escape, during "Saving Markdown…": the editor closes,
   `state.activeBlockEdit` is undefined, no `previewEditCancel` and no second `previewEditSave` is
   posted. The same after a timeout. For the cell editor this includes a session with a cell left
   earlier and a Tab-added row (the branches of `cancelTableCellEdit`): still no message.
8. Cancel with no final save posted behaves as BLOCK-053 says (with and without an autosave).

The rewritten `test/page/blockReq.requirements.test.ts` test (section 5) carries
`@tests_req SwRS-MDOKFSTUDIO-BLOCK-053`; the cell checks carry
`@tests_req SwRS-MDOKFSTUDIO-TABLE-025`; the timeout checks carry the new SwRS's `@tests_req`.

**Blank-lines block on top of part A** (in `test/page/runtimeBlankLines.test.ts`, beside part A's
regression test): open the editor of a blank-lines block, type, press Done, advance past the limit
(timeout message shows), then apply a content patch: the editor closes and the held block is gone.
This fails with part A's condition alone (`finishing` only).

**Page, frontmatter** (`test/page/runtimeFrontmatterEditor.test.ts`, with `advanceTimers`):

- a value save with no result: after the limit, the status reads the frontmatter timeout message
  with `data-state="error"`, the control is enabled, and Enter posts `previewFrontmatterSave`
  again;
- `saved: true`, then no content patch: after the limit (counted from the post), the same message
  replaces "Saved. Refreshing preview…" and the control is enabled;
- a key rename (`saveKey`) and a field action (`postFrontmatterAction`) with no result: the same;
- an error result or a content patch before the limit: advancing past it changes nothing.

**Host and protocol:**

- `test/session/` (the file that covers `handleEditSave` refusals, for example beside
  `blankRunHost.test.ts`): a retried final save after the first one wrote and completed is refused
  with `stale: true`; a refusal of `handleEditCancel` and an apply failure carry no `stale`.
- The protocol test of `hostToPage.ts` (if the page validates the message) accepts
  `previewEditSource` with `stale: true`.

**Save-to-render time (measure for save-guard-Q5).** Nothing measures it today. In the real VS
Code integration run (`just ci-integration`, LF), on the largest Markdown fixture among
`test/integration/fixtures` and the visual fixtures (the Driver names it by size; the large chapter
of `test/probe/largeChapter.ts`, used by `test/integration/performanceProbe.ts`, is a candidate if
it is larger), record five times the time from the page's final `previewEditSave` of a one-paragraph
edit to the content patch that closes the editor. Write the slowest and the median next to
`FINAL_SAVE_TIMEOUT_MS` in the change's review description (the PR or MR body) and in the run's
report. The limit holds when the slowest time is at most half of it (5 000 ms). Otherwise the
Driver reports the numbers, and the value goes back to the owner through the Chief of Staff before
the change is marked ready.

**Visual** (`just ci-visual`): one capture of a block editor showing the timeout message, and one of
a frontmatter field showing it, attached as the pull-request guideline asks.

**Requirements:** `just requirements-lint` and `just requirements-update` pass; every updated or new
SwRS has its `@implements_req` at the code above and its `@tests_req` at each test above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

Technical choices the answers leave to the specification, for the Chief of Staff to check:

1. **One constant in `src/page/pageSettings.ts`**, shared by block, cell and frontmatter saves.
2. **The host marks stale refusals** (`stale: true` on every refusal of `handleEditSave`) rather
   than the page matching message texts, so the page's stale-retry wording does not depend on
   English strings.
3. **The timed-out state lasts until the editor closes**, so a late patch or `done` closes it and a
   stale refusal of the retry is recognised.
4. **Cancel on a timed-out editor also closes without `previewEditCancel`**: the first save may
   already be written, and Q4 keeps it.
5. **The frontmatter message names its keys** (Enter, Escape), since the field editor has no Done
   or Cancel button; its first sentence is the owner's wording.

## Open questions

1. A stale refusal on the retry (save-guard-Q3, "close the editor"): this specification shows
   "Already saved, or the block changed since. Press Cancel to close the editor." and leaves the
   editor open, so the writer can still copy the text. Should the editor close by itself instead?
2. StRS-MDOKFSTUDIO-BLOCK-006 says "Cancel or Escape as restoring the block". This specification
   keeps it unchanged, reading it as the rule before Done. Is that reading right, or does the StRS
   need a re-approved nuance for Cancel during a final save?
3. A stale refusal on a frontmatter retry: this specification shows the host's message as today
   (the frontmatter host does not mark stale refusals; `FRONTMATTER_STALE` also covers a schema
   mismatch). Should the frontmatter editor get the "already saved or changed" wording too?
