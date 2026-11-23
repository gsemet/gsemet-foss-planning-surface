# A blank-lines block's editor closes after its final save

issue: https://github.com/gsemet/markdown-okf-schema-studio/issues/485

Typing in a blank-lines block and pressing Done no longer leaves the editor on "Saving Markdown…":
the render of its final save closes it, like the editor of any other block. This CR fixes the hang
the issue found, on today's one-block-per-run design (CR-444), and closes the issue.

Short name: `blank-save`. Destination: the running batch-09 (blank-save-Q4). Place in the stack:
first of three CRs (blank-save-Q8, item 18). `save-guard-never-hangs` comes after it, then
`blank-line-block-per-line`.

## Goal

The issue: a line of text followed by 6 blank lines shows one blank-lines block (the CR-444
design). The writer clicks it, types text and presses Done. The editor shows "Saving Markdown…" and
stays like that: the text is written and renders below, but the editor never closes, and neither
Done nor Cancel gets the writer out.

After this CR, the same steps end like any block edit: the text is written, the editor closes and
the rendered block shows. The hang had no test (blank-save-Q3): this CR adds the page test that
reproduces the issue's steps, and that test fails on the code before the fix.

Project rules: this change follows the project's constitution (`.agents/constitution.md` in
markdown-okf-schema-studio), its `AGENTS.md` (requirements, completion gate `just preflight`) and
the requirements guidelines named there. This specification restates none of them.

## What exists today

CR-444 (merged 2026-11-21; its folder in the planning archives is
`5-archives/261121-0724-444-empty-block-blank-lines-block`), with CR-448 (runs inside lists) and
CR-462 (runs inside quotes and containers), shows one blank-lines block per run of two or more
blank lines (`installBlankLines`, `src/page/features/blankLines.ts`). A click or Enter on it opens
an insertion editor whose state carries `replaceBlankRun: { line, endLine, itemLine?,
containerLine? }`.

CR-444 fix 7 keeps that editor open across a re-render. A re-render can drop the run the editor was
opened from (an autosave already wrote text in its place), and the editor must not vanish under the
writer's typing. Two places do it:

- `applyContentPatch` (`src/page/features/contentPatch.ts`, the line
  `if (!state.activeBlockEdit?.replaceBlankRun) rt.blockEditor.closeBlockEdit(false);`, under the
  `@implements_req SwRS-MDOKFSTUDIO-BLOCK-268` comment "The editor of a blank-lines block stays
  open") skips `closeBlockEdit` whenever the open editor has `replaceBlankRun`.
- `refresh()` in `blankLines.ts` puts the editing block and its frame back (the `editing` and `held`
  branch), as long as `state.activeBlockEdit?.replaceBlankRun` is set.

### Why the editor stays in "Saving Markdown…"

Read from the code; the Driver confirms it with the failing page test of the Evidence before
fixing.

1. Done calls `postBlockEditSave(true)` (`src/page/features/blockEditor.ts`). It sets
   `edit.finishing = true`, shows "Saving Markdown…" and posts `previewEditSave` with
   `final: true`.
2. The host writes the text. `completeActiveBlockEdit` (`src/session/features/blockEdits.ts`) sees
   a revision not yet rendered: it asks for a render (`refreshPreviewDocument`, immediate) and posts
   no `done: true`, because the content patch is what closes the editor (the BLOCK-263 comment
   there).
3. The content patch arrives. `applyContentPatch` skips `closeBlockEdit` because the editor has
   `replaceBlankRun`. `refresh()` puts the block and its frame back. The editor stays open with
   `finishing` still true.
4. With `finishing` true, Done does nothing (`postBlockEditSave` returns early) and Cancel does
   nothing (`cancelBlockEdit` returns early, the SwRS-MDOKFSTUDIO-BLOCK-053 refusal scenario
   "Cancel is ignored while the final save is in flight"). No other message comes: the editor hangs.

A `done: true` answer (`receiveBlockEditSource`, `src/page/features/blockSourceEditor.ts`) already
closes the editor when `finishing` is true. Only the content patch path hangs.

## What changes

### 1. The content patch closes the editor of a final save

In `applyContentPatch` (`src/page/features/contentPatch.ts`), the exception for `replaceBlankRun`
holds only while no final save of that editor was posted:

- The open editor has `replaceBlankRun` and `finishing` is false (no final save posted, or one that
  an error answer refused, which clears `finishing`): unchanged. The editor stays open across the
  re-render, and `refresh()` puts its block and frame back (CR-444 fix 7).
- The open editor has `replaceBlankRun` and `finishing` is true (Done was pressed and its final
  save posted): the patch closes it with `closeBlockEdit(false)`, as for any block. No
  `previewEditCancel` is posted. The `refresh()` that the patch runs (`initializeContent`) then finds
  no editing block and drops the held one: the page shows the new render's blank-lines blocks only.
- Any other editor: unchanged (closed by the patch).

The comment above that line says both halves: the editor of a blank-lines block stays open across an
autosave's re-render, and closes on a patch once its final save was posted.

As for any other block, a patch that arrives after Done closes the editor, even when that patch
renders an earlier autosave and the final save is still running on the host. The host completes
that save and renders it in a next patch. That is today's rule for every other block, now also for
a blank-lines block.

Nothing else changes: the host (`blockEdits.ts`), the protocol, `blankLines.ts`, the run list, the
look, Delete, paste and the BLOCK-053 rule that Cancel is ignored while `finishing` is true. The
`@implements_req SwRS-MDOKFSTUDIO-BLOCK-268` marker stays on that line.

### 2. Requirements

Follow the project's requirements guidelines: markers stay with the code, run
`just requirements-update`, and add a dated entry in `requirements/tiers/log.md` (issue #485, the
editor of a blank-lines block closes on the render of its final save).

- **Update SwRS-MDOKFSTUDIO-BLOCK-268** (scope `block-editing`):
  - Its description and normative text: "keep the editor open across an autosave re-render" becomes
    "keep the editor open across an autosave re-render and close it on the render that follows its
    final save".
  - A new scenario, "Done closes the editor":
    - GIVEN a blank-lines block's editor with typed text;
    - WHEN the writer presses Done and the host writes the text and renders it;
    - THEN the editor closes, "Saving Markdown…" is gone and the block shows in place of the run.
  - Verification notes: the Method line names the new page test in
    `test/page/runtimeBlankLines.test.ts`. The criterion "the editor of an open run survives
    refresh()" becomes "the editor of an open run survives refresh() until its final save is
    posted; the patch after it closes the editor".
- No other SwRS or StRS changes. BLOCK-053 is unchanged here (its Cancel rule is the next CR's).
- The glossary (`.agents/glossary/common.md`) and the writing skill
  (`skills/writing-for-markdown-okf-schema-studio/`) are not concerned: no term and no rendered
  syntax changes.

## Out of scope

- **The general save guard**: a time limit on every final save, a shown error when no answer comes,
  the frontmatter save's bounded wait, and Cancel always closing the editor (blank-save-Q6, Q9, Q10,
  Q14, Q15). It is the CR `save-guard-never-hangs`, next in the stack. Here, Cancel stays ignored
  while a final save is in flight (BLOCK-053), and no timer is added.
- **One block per blank line**: each blank line beyond the separator as its own block, typing and
  Delete acting on one line, per-line blocks inside containers and after the frontmatter
  (blank-save-Q1, Q2, Q5, Q7, Q12, Q13), with the tests of blank-line segmentation. It is the CR
  `blank-line-block-per-line`, after `save-guard-never-hangs` in the stack.
- The one-block-per-run design itself, its look, placement, Delete, paste and protocol: unchanged.
- The release notes, written when the release is prepared.

## Evidence

The checks run the shipped code at the head under test: the real page runtime, as
`test/page/runtimeBlankLines.test.ts` drives it today, never a prepared copy. The regression test
fails on the code before the change (constitution, section 3): the Driver runs it first on the
unchanged code and records the failure (the editor still open, "Saving Markdown…" shown).

**Page, the regression of the issue** (new test in `test/page/runtimeBlankLines.test.ts`, marked
`@tests_req SwRS-MDOKFSTUDIO-BLOCK-268`), with the helpers of that file (`harnessWithRuns`,
`setRuns`, `blankBlocks`, `sent`, `patchMessage`):

1. The issue's shape: a run at the end of the body (a run list with one run, for example `2-7`, a
   line of text then 6 blank lines). One blank-lines block shows.
2. Click it. The page posts `previewEditOpen` with `replaceBlankRun: { line: 2, endLine: 7 }`;
   answer it with `previewEditSource` and `originalText: ""`.
3. Type `Text` and press Done. The page posts `previewEditSave` with `final: true`, and the status
   reads "Saving Markdown…".
4. Apply the content patch of the render: a run list without that run (`setRuns` with no run of the
   editor, then `patchMessage()`).
5. Assert: the editor is closed (its frame is out of the page and no "Saving Markdown…" status is
   left, checked the way the file's other close checks do), the held blank-lines block is gone (`blankBlocks` does not hold it), and no
   `previewEditCancel` was posted. Then a click on another blank-lines block, when the patch's list
   has one, opens a new editor: the page is not stuck.

Same file, one check each:

- **Done before any autosave and Done after an autosave**: both close on the patch (the test above
  runs once with `flushTimers()` after typing, so an autosave was posted first, and once without).
- **A run inside a list** (the `listHarness` of the file): Done then the patch closes the editor too.
  This covers the `held` path of `refresh()` that puts a list's block back.
- **Fix 7 kept**: the existing tests "an editor opened from a blank-lines block stays in its element
  across a patch without that run", "an editor opened in a list item survives a patch that replaces
  the list, and Cancel keeps the item line" and, in `runtimeBlankLinesContainers.test.ts`, "an
  editor opened from a quote run survives a patch that replaces the quote, and Cancel keeps the
  run" pass unchanged: an autosave's patch keeps the editor open.
- **An error answer, then a patch**: after Done, a `previewEditSource` with an `error` clears
  `finishing`; a following patch keeps the editor open (no final save in flight), and a second Done
  then a patch closes it.

**Session, no change expected**: `test/session/blankRunHost.test.ts` keeps or gains the check that a
final save of a blank-run insertion that writes text ends the host edit, asks for a render and posts
no `done`. This is the host half of the issue's steps, and it shows why the page must close on the
patch.

**Integration**: none added. The hang is on the page, and `test/integration/blankLines.test.ts`
drives the host by messages and sees no page editor. Its existing write, delete and undo scenarios
must still pass in the heavy run on the branch.

**Requirements**: `just requirements-lint` and `just requirements-update` pass, and BLOCK-268 names
the new test.

**Gate**: `just preflight` passes (on Windows its static stage; CI runs the others).

## Decisions carried

- blank-save-Q8 and item 18: three CRs in one stack; this one is part A, the #485 hang fix, keeps
  the `issue:` line and closes the issue.
- blank-save-Q4: destination the running batch-09.
- blank-save-Q3: the hang shows the case had no test; the regression test reproduces the issue's
  steps and fails first.
- blank-save-Q6, the part kept here: the test that the save of a blank-lines block's editor leaves
  "Saving…". The general guard and the segmentation tests go to the two other CRs.
- Spec critic (item 8): yes, on Fable; the Chief of Staff runs it.

## Open questions

None.
