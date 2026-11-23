# No edit stays on Saving Markdown for good

Tests prove that every save of a block editor, a table cell editor or a frontmatter field ends
in the rendered result or in a shown error. Each hang the tests find is a bug, and this CR fixes
it. Cancel and Escape always close a block or cell editor, even while it shows "Saving
Markdown…". The save already asked for with Done goes on, and its text is kept. There is no time
limit, no timeout message and no retry.

Short name: `save-guard`. Destination: the running batch-09, in its stack.

## Goal

CR `blank-run-edit-stuck-saving` (part A, short name `blank-save`) fixes the one hang the issue
found: a blank-lines block's editor stayed on "Saving Markdown…" because the content patch never
closed it. Nothing yet stops the next hang of that kind. This CR proves, with one test per save
path, that each path ends. It fixes the paths that do not end, and the one the new Cancel rule
would create.

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

The Chief of Staff's decisions on the first specification's critic findings:

1. **Cancel during an in-flight final save also tells the host that the page editor is gone.**
   The host ends its edit keeping the text as written (no restore), and the next block opens.
2. **A pending block navigation is dropped on that Cancel or Escape.** The editor closes, the save
   completes, and nothing else opens or moves.
3. **The file-size limits hold** (see "Size limits").
4. **Requirements**: BLOCK-053, BLOCK-006 and BLOCK-047 are handled as in section 6.
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
cell editor share it. It is called by Done, Ctrl/Cmd+Enter, a blur, the move chord
(`moveBlockFromEditor`, with `thenMove`), the arrow and Tab navigation (`navigateBlockEdit`,
`tabThroughTableCells`), a click on another block (`editMode.ts`, `blockSelectionView.ts`) and
`flushOpenEditors`.

The editor closes only on:

- **a content patch**: `applyContentPatch` calls `closeBlockEdit(false)`;
- **`previewEditSource` with `done: true`**: `receiveBlockEditSource`
  (`src/page/features/blockSourceEditor.ts`) closes only `if (edit.finishing)`, then resumes the
  pending navigation (SwRS-MDOKFSTUDIO-BLOCK-263);
- **a full page replacement**.

An error answer keeps the editor open: `finishing` becomes false, the pending navigation and
selection are cleared, and the error shows (SwRS-MDOKFSTUDIO-BLOCK-216).

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
(`rememberPendingBlockNavigation`), and the navigation resumes after the save
(`resumePendingBlockNavigation` in `editMode.ts`, called on `done` and from `initializeContent`
after a patch).

`closeBlockEdit(cancel)` clears the pending navigation only when `cancel` is true. It posts
`previewEditClosed` only when `edit.reportClose` is set.

### The host

The host side is `src/session/features/blockEdits.ts` and the lock is
`src/core/state/editLock.ts`.

- **`handleEditOpen`** refuses with "Another Markdown block is already being edited." while
  `preview.edits.active` is set. It refuses as stale unless the page's revision is the current
  document and stage revision (`currentPreviewDocument`). Only then does it call
  `openPageEditor`, which records `lock.pageEditorId`.
- **`handleEditSave`** refuses mismatches with `postEditSourceError`. Otherwise it queues the
  text, and `drainActiveBlockEdit` applies it.
- **Completion.** When a final save is drained, `completeActiveBlockEdit` calls
  `releaseActiveBlockEdit`. That sets `edits.active = undefined` and calls `lock.release()`,
  which clears `held` **and `pageEditorId`** and runs the queued work. Then it asks for an
  immediate render, or posts `done: true` when nothing is left to render (and the edit was not
  cancelled).
- **Apply failure or rejection.** `drainActiveBlockEdit` posts an error and sets
  `finalRequested = false`. **It leaves `edits.active` set**: the editor stays open on the page
  and shows the error, and the writer goes on from there. A "source block changed" refusal
  instead releases the host edit and keeps the page editor (`releaseHostEditKeepingEditor`).
- **`previewEditClosed`** calls `closePageEditor(editId)`. That clears `pageEditorId` when it
  matches, and drains the queued work only when `held` is false.
- **`handleEditCancel`** restores `originalText`.
- **Renders.** Render results wait while `pageEditorId` is set (`shouldDeferResult`, STAB-03).
  `onReady` releases a held edit when the page reports `blockEditOpen: false`. A full page
  replacement clears `edits.active`.

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
  host completes it.

Add "Detached save" to `.agents/glossary/common.md`.

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

The save goes on. When its end arrives (content patch, `done`), nothing else opens or moves.

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

### 2. The host ends a detached save, and the next block opens (decision 1)

**Page.** Add `detachedSaveEditId?: string` to the page state (`pageRuntime.ts`). It is set by
section 1 and cleared when the detached save ends, which is any of:

- a content patch;
- a full page replacement;
- `previewEditSource` with `done` or `error` for that `editId` (today such an answer finds no
  editor and is dropped).

While it is set, `openBlockEditor` does not post `previewEditOpen`. It records the target with
`rememberPendingBlockNavigation`, the same way a click during "Saving Markdown…" does today. When
the end arrives, the page clears the mark and calls `resumePendingBlockNavigation`.
`initializeContent` already does this after a patch; add it for `done` and `error`. So the next
block the writer opens after that Cancel opens once the save ended, against the new rendering.
The open does not meet a stale page revision.

This is a new gesture after the Cancel. The navigation pending at the time of the Cancel was
dropped (section 1).

**Host** (`blockEdits.ts`; the lock's API in `editLock.ts` if a method is needed):

- **Mark the edit detached.** `previewEditClosed` for the `editId` of `preview.edits.active`,
  when that edit is not `cancelRequested`, marks it `detached` (a new flag on `ActiveBlockEdit`).
  The lock's `pageEditorId` is cleared as today.
- **Idle edit.** If the edit has nothing left to apply (not `applying`, no `pendingText`), it is
  released at once with `releaseActiveBlockEdit(preview, true)`, and the document is rendered:
  the text stays as written, with no restore. This covers an edit whose final save already
  failed (`finalRequested = false`, error posted to the closed editor).
- **Busy edit.** Otherwise the edit drains as today and completes with no `done`; the render
  follows as usual.
- **Detached failure.** An apply failure or rejection of a detached edit releases it at once:
  `edits.active = undefined` and the host hold is freed. The error is shown as a VS Code warning,
  through the same path `postEditSourceError` uses for a flush refusal (SwRS-MDOKFSTUDIO-BLOCK-205),
  because the page has no editor to show it. Without this, the edit stays held for good and every
  later open is refused with "Another Markdown block is already being edited.". This is a hang of
  the edit lock that the new Cancel rule would create.
- **Do not clear a newer page editor.** Releasing a detached edit frees only the host hold
  (`held`). If a `pageEditorId` other than the detached `editId` was recorded since, it is kept,
  and the queued render waits for that editor (STAB-03). This prevents a late completion from
  closing a newer editor.
- **An open that arrives during a detached edit.** `handleEditOpen` does not refuse a
  `previewEditOpen` with "Another Markdown block is already being edited." when the active edit
  is detached. It holds the open (at most one; a later one replaces it) until the detached edit
  is released, then handles it with its usual checks. The page's wait (above) makes this rare; it
  covers a message already in flight.

`trackOutsideChange` and the full page replacement keep releasing a detached edit, as they do any
active edit.

### 3. Each save path ends: the hangs found by reading, and their fixes

**Found and fixed in this CR:**

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
    `unchanged: true` (`src/core/protocol/hostToPage.ts`, with its validator). On
    `unchanged: true`, `receiveFrontmatterResult` closes the field editor at once
    (`closeFrontmatterEditor("unchanged save")`). That applies the deferred properties markup,
    and `afterResult` runs.
  - The Driver first proves the hang with a failing test. If a no-op apply does fire a document
    change in the test host and the hang does not reproduce, the Driver reports it, and the fix
    is kept only if the real VS Code apply behaves as `applyWrittenEdits` says.
- **H2, the detached edit whose save fails** (section 2): it held the host edit for good.
- **H3, the late completion that cleared a newer editor's lock** (section 2).

**Read and found to end (each gets its test in the Evidence):**

- a host refusal of the final save gives an error answer;
- an apply failure or rejection gives an error answer;
- nothing to write gives `done`;
- a write gives a render, which ends in a content patch, a full page replacement, or a failed
  render (`setStatus` replaces the page);
- a hidden panel renders when shown (`renderIfDirty`);
- a patch never acknowledged gives a reload (`armContentPatchFallback`);
- an outside change releases the edit and renders;
- a document switch: `forgetPage`, and the new document replaces the page;
- the blank-lines editor's patch is closed by part A;
- frontmatter: an error answer, a content patch or a full replacement end the field editor.

The Driver reads these paths again on top of part A. **Any test that does not end is a new hang:
fix it here, and name it and its cause in the commit and the PR body.**

### 4. The frontmatter Escape rule is unchanged

Escape stays ignored while a frontmatter save is in flight, and the control stays disabled
(FMEDIT-001, FMEDIT-004). Nothing in `bindKeys`, `saveValue`, `saveKey` or
`postFrontmatterAction` changes, except H1's handling of `unchanged: true`.

### 5. What stands against these rules today, and is changed here

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
- Any other existing test that asserts that Cancel or Escape does nothing during "Saving…" (the
  Driver finds them with `just check`) is handled the same way, and each one is named in the
  commit.

### 6. Requirements and vocabulary

Follow the project's requirements guidelines (IDs from `okfreq new`, markers move with the code,
`just requirements-update`, a log entry).

- **SwRS-MDOKFSTUDIO-BLOCK-053** (block-editing):
  - New title, for example "Cancel and Escape restore the saved text, or close the editor during
    a final save". It must be at most the guideline's title length.
  - The description adds: during a final save, the editor closes with no previewEditCancel, and
    the save completes.
  - The refusal scenario "Cancel is ignored while the final save is in flight" becomes a nominal
    scenario, "Cancel during a final save closes the editor and the save completes". It covers no
    previewEditCancel, no second final save, the text kept in the document, the pending navigation
    dropped, and the next block opening after the end.
  - Verification notes: the rewritten test by its new name. The criterion "cancelBlockEdit
    returns without a message when finishing is true" becomes "cancelBlockEdit closes the editor
    with previewEditClosed and no previewEditCancel when finishing is true". Add the session test
    of section 2.
- **SwRS-MDOKFSTUDIO-TABLE-025** (table-editing): a scenario "Escape or Cancel in a cell during a
  final save closes the editor with no message". It includes a cell left earlier, a Tab-added row
  and the focus outside the cell editor. Add its test to the verification notes.
- **SwRS-MDOKFSTUDIO-BLOCK-191** (the host holds and ends the block edit): a scenario "The page
  closed the editor during its final save". It covers the edit completing with no restore, a
  failure released and shown as a warning, the open accepted after the end, and a newer editor's
  lock kept.
- **New SwRS** (block-editing), title for example "Every final save of a block or cell editor
  ends":
  - each save path listed in section 3 ends in a closed editor or a shown error;
  - it derives from StRS-MDOKFSTUDIO-BLOCK-006 and depends on BLOCK-216, BLOCK-263 and BLOCK-191.
- **Frontmatter** (frontmatter-editing): a scenario on SwRS-MDOKFSTUDIO-FMEDIT-019 (or the
  frontmatter save SwRS the guidelines point to): "A save that changes no text closes the field
  editor". Also a scenario stating that every frontmatter save (value, key, field action) ends in
  a closed editor or a shown error.
- **StRS-MDOKFSTUDIO-BLOCK-006** (`proposed`): its wording changes with the code, with no
  re-approval. "Cancel or Escape as restoring the block" gets the nuance "or, once Done was
  pressed, as closing the editor while the save completes".
- **SwRS-MDOKFSTUDIO-BLOCK-047**: no change. Its boundary scenario "A second final save is
  refused while the first is in flight" stays true, because there is no retry and nothing posts
  a second final save. The first specification's changes to it are dropped.
- **Glossary**: "Detached save" (see "Words"). No "Save time limit" and no "Timed-out editor".
- The writing skill `skills/writing-for-markdown-okf-schema-studio/` is not concerned: no rendered
  syntax changes.

### Size limits (decision 3)

- `src/page/features/pageRuntime.ts` is 793 lines (limit 800).
  - The one new state field and its comment fit.
  - If the Driver needs more, move a type out of the file (for example the `BlockEdit` pending
    navigation types) rather than pass the limit.
- `test/page/runtimeFrontmatterEditor.test.ts` is 1 396 lines (limit 1 500): new frontmatter tests
  go in the new file below, not there.
- `src/session/features/blockEdits.ts` (729) and `blockEditor.ts` (649) have room. If
  `blockEdits.ts` would pass its limit, put the detached-edit handling in a small module beside
  it.

## Out of scope

- The hang part A fixes and its regression test (CR `blank-run-edit-stuck-saving`).
- One blank-line block per blank line (CR `blank-line-block-per-line`).
- Any time limit, timeout message, retry message, `stale` mark on host refusals, or save-to-render
  measure (save-guard-Q9).
- Undoing a save on Cancel: the save asked for with Done is kept (save-guard-Q4).
- The frontmatter Escape rule during a save (unchanged, section 4).
- Other messages: block moves, pastes and cuts, checkbox toggles, label renames, find and replace,
  `previewEditCancel` of an editor before Done.
- An autosave that fails while the final save is queued. It ends in an error, not in "Saving…";
  pressing Done again may then meet a "source block changed" refusal. It is noted here, not
  changed.
- The release notes, written when the release is prepared.

## Evidence

The checks run the real page bundle, the real host session code and the real protocol module at
the head under test, never a prepared copy. Each check for a fix fails on the code before the
change (constitution, section 3), and the Driver shows each failure once. The checks that prove an
already-ending path pass before and after.

**Page, every save path ends** (new file `test/page/runtimeSaveEnds.test.ts`). Each check runs for
a paragraph editor and for a table cell editor: type, press Done ("Saving Markdown…" shows), then
send one of these answers:

1. a content patch: the editor is closed;
2. `previewEditSource` `done: true`: the editor is closed;
3. an error answer (each host refusal text of `handleEditSave`, and "VS Code could not apply the
   Markdown edit."): the editor is open, `finishing` is false, the error shows and the text is
   kept;
4. a full page replacement: no editor;
5. the move chord, the arrow and Tab navigation, a Tab-added row and a click on another block,
   each followed by `done` or a patch: the editor closes, and the pending navigation then opens
   its target.

In every run the end state is a closed editor or a shown error, never `finishing` with no answer
pending.

**Page, Cancel during a final save** (same file):

6. Cancel, and in another run Escape in the text box, during "Saving Markdown…":
   - the editor closes and `state.activeBlockEdit` is undefined;
   - one `previewEditClosed` with its `editId` is posted;
   - no `previewEditCancel` and no second `previewEditSave` is posted.
7. The same in a cell editor:
   - with a cell left earlier (kept-cell branch);
   - with a Tab-added row;
   - with Escape while the focus is outside the cell editor (`bindKeys`).
8. Dropped navigation. Press the move chord, an arrow at the block edge, Tab on the last row, and
   a click on another block; each posts the final save. Then press Cancel. Then send a content
   patch, or `done` in another run: no editor opens, no block moves, the selection is on the
   edited block.
9. An open after that Cancel. Double-click another block before the end: no `previewEditOpen` is
   posted. After the patch (or `done`, or an error for the detached `editId`), one
   `previewEditOpen` is posted for that block, with the page's new revision.
10. Cancel with no final save posted behaves as BLOCK-053 says, with and without an autosave.

The rewritten test of `test/page/blockReq.requirements.test.ts` carries `@tests_req
SwRS-MDOKFSTUDIO-BLOCK-053`, the cell checks carry `@tests_req SwRS-MDOKFSTUDIO-TABLE-025`, and the
path checks carry the new SwRS's `@tests_req`.

**Page, frontmatter** (same new file, or a new `test/page/runtimeFrontmatterSaveEnds.test.ts`).
For a value save, a key rename and a field action (add and remove):

- an error answer: the control is enabled, the error shows, and Escape closes;
- `saved: true` then a content patch: the field editor is closed;
- **H1**: `saved: true` with `unchanged: true`: the field editor is closed at once and the
  deferred properties table is applied;
- while each save is in flight, Escape does nothing and the control is disabled (the rule kept).

**Host** (`test/session/`, beside `blankRunHost.test.ts`, for example a new
`test/session/detachedSave.test.ts`):

- **H1**: a `previewFrontmatterSave` whose plan leaves the text unchanged (for example a YAML text
  that serialises to the same frontmatter) gets `saved: true, unchanged: true`, and the document
  is untouched. This fails before the fix: no `unchanged`, and no render follows.
- **Decision 1, (a)**: final save written and completed; then `previewEditClosed` for its
  `editId`; then a `previewEditOpen` at the rendered revision. The open is accepted
  (`previewEditSource` with `originalText`). The document holds the saved text, not the original.
- **Decision 1, (b)**: an autosave applied, the final save queued or applying (the apply held
  back), then `previewEditClosed`, then the apply resolves. The edit completes with no restore,
  `edits.active` is undefined, and the render runs. A `previewEditOpen` at the rendered revision
  is accepted.
- **Decision 1, (c)**: as in (b), but the `previewEditOpen` arrives before the apply resolves. It
  is not refused with "Another Markdown block is already being edited."; it is answered after the
  detached edit is released. When that answer opens an editor, its `pageEditorId` is still set
  after the release, and the render result of the detached save waits for it.
- **H2**: as in (b) with the apply failing, or rejecting. The edit is released
  (`edits.active` undefined), a warning is shown, and a later `previewEditOpen` is not refused
  with "Another Markdown block…". This fails before the fix.
- `previewEditClosed` after a `previewEditCancel` (an edit with `cancelRequested`) still restores
  the original text: the detached rule does not apply.

**Protocol:** the host-to-page validator accepts `previewFrontmatterResult` with
`unchanged: true`, and refuses a non-`true` value.

**Real VS Code** (`just ci-integration`, on the heavy run): one scenario in
`test/integration/previewEditing.test.ts` or its real-input group. Type in a paragraph, press
Done, press Escape at once, then open the next block. The first block holds the typed text in the
file, the next block's editor opens, and no editor shows "Saving Markdown…".

**Requirements:** `just requirements-lint` and `just requirements-update` pass. Every updated or
new SwRS has its `@implements_req` at the code above and its `@tests_req` at each test above.

**Gate:** `just preflight` passes (on Windows its static stage; CI runs the others).

## Decided in the spec

Technical choices the answers leave to the specification, for the Chief of Staff to check:

1. **The page waits for a detached save's end before it opens another block.** It reuses today's
   pending navigation during "Saving…". The open then carries the new revision, so the host's
   stale check passes and decision 1's "the next block opens" holds. Without the wait, the host
   would answer an early open with "The preview is stale".
2. **The host holds an open that arrives during a detached edit** (at most one) instead of
   refusing it, as a second line behind the page's wait.
3. **A detached edit's failure is shown as a VS Code warning** (the flush refusal's path), since
   the page has no editor left.
4. **H1 is fixed on the host** with `unchanged: true`, rather than by a YAML-normalising check on
   the page. The host is the one place that knows the text did not change.
5. **The `detached` flag applies only to an edit that is not `cancelRequested`**, so today's
   Cancel before Done (restore) is untouched.

## Open questions

1. **A cancelled save that fails.** When the writer pressed Escape during "Saving…" and that save
   then fails, the page has no editor left. This specification shows the error as a VS Code
   warning; the typed text is then not in the file. Is a warning enough, or should the editor
   reopen with the typed text and the error?
2. **Opening a block during a cancelled save.** A block opened after Cancel and before the save
   ended opens once the save ended, a moment later. Is that delay acceptable, or should such a
   click be ignored?
3. **A frontmatter save that changes nothing** (H1). This specification closes the field at once,
   with no message. Is a silent close right, or should it say "No change"?
