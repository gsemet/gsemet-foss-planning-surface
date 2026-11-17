---
title: Change spec - table preview stale after an undo or a revert
cr: 277
date: 2026-11-10
issue: none
source: QA campaign 271, QA271-05 (c3-2), QA271-06 (c6-1), Medium, P2
base: origin/main a12a16bc
---

# Change spec: table preview stale after an undo or a revert

Invariant the owner set (02-answers): after an undo, a redo or a revert, the preview table shows
what the buffer holds. Read the code from `origin/main`; the line numbers below are those of
a12a16bc.

## 1. Root cause hypothesis

The intent guessed one cause. Reading the code, these are two separate mechanisms with one
symptom. Each one is enough to break the invariant on its own.

### 1a. QA271-05 (c3-2): the host holds the render while a cell editor is open

- `src/core/state/editLock.ts`, `EditLock.shouldDeferResult()` returns true as long as
  `pageEditorId` is set, that is from the page's `previewEditOpen` until it closes
  (SwRS-MDOKFSTUDIO-BLOCK-193, "Page updates wait while an inline editor is open").
- `src/session/features/rendering.ts` (about line 369): a finished render is queued under
  `"render-result"` through `manager.edits.deferPageWork` while `shouldDeferResult()` holds. It
  reaches the page only when the editor closes. This matches "after Cancel it catches up".
- `src/session/hostEvents.ts`, `refreshPreview()` (about line 285): an outside change is checked
  against the open edit only when the host holds one (`session.edits.active`, created at the first
  save). In c3-2 every Col − is a structural final save (`structural()` in
  `src/page/features/tableCellEditor.ts`, about line 358). It ends the host edit, re-renders, and
  the editor reopens in the cell through the pending block navigation
  (`rememberPendingBlockNavigation`, resumed in `initializeContent` of
  `src/page/features/contentPatch.ts`). The reopened editor has not saved, so `edits.active` is
  undefined: the undos go to `refreshPreviewDocument`, and the render they cause is deferred
  behind the open page editor. Nothing compares the change with the editor's table, so no conflict
  error is shown (`trackOutsideChange` in `src/session/features/blockEdits.ts` runs only with a
  host edit). Done would then commit a 1-column model over the restored table.
- Why only sometimes ("two undos pass"): probably focus. `commitCellEditorOnFocusLoss` (in
  `tableCellEditor.ts`) closes the editor when the webview loses focus, and the deferred render
  then flows. When the reopen by pending navigation lands after Meta+1 already moved the focus to
  the source, the editor opens without focus and no blur ever comes. It stays open and holds every
  render. The third undo only adds time. The unit tests in section 3 must confirm or refute this
  before the fix. The fix below does not depend on the trigger.

### 1b. QA271-06 (c6-1): the keyed morph keeps a table node the page rewrote

- `src/page/modules/contentMorph.ts`, `installContentMorph().replace()`: a top-level block is
  kept when the hash of the incoming host HTML equals the hash recorded when the node was
  inserted (`sources` WeakMap, `describe(html)`). The record is never updated when the page
  changes the node's content itself.
- `src/page/features/tableCellEditor.ts`, `switchTableCell()` (about line 79): on Tab, an arrow
  key or a click, the cell left gets the typed text written into its DOM with `setCellInline`
  (SwRS-MDOKFSTUDIO-TABLE-035). The table node now shows `alpha X`, but its recorded key is still
  that of the host HTML with `alpha`.
- In c6-1, no render carrying `alpha X` replaced the table before the revert. The external
  rewrite of the open, dirty file changes the order or drops a render in the deferred queue: a
  newer `"render-result"` replaces an older one, and the guard `result.stage.requestId <
  preview.stage.requestId` disposes it. Without the rewrite, an `alpha X` render reached the page,
  the node was replaced and its key updated, and the bug does not show (checked by QA). Revert File
  then brings the buffer back to `alpha`. The incoming table HTML hashes to the key still recorded
  on the mutated node, so `planKeyedMorph` keeps the stale node, while the paragraph, whose HTML
  changed, is replaced. This explains the "half refreshed" preview exactly.
- The exact render that went missing does not need to be found. The defect is that a node whose
  content the page wrote keeps a key that claims it is still the host's HTML.

## 2. Behaviour to build

1. Outside change under an open table cell editor (fixes 1a). When the document changes outside
   the preview (`isOutsideChange` in `src/core/preview/updatedRanges.ts`: undo, redo, or a change
   that is neither typed by the writer nor applied by the preview, Revert File included) and the
   change overlaps the source lines of the table that has a cell editor open in the page, the host
   lets the render of the new buffer through at once (`forceNextResult` path, the deferred
   `"render-result"` dropped). It also releases a host edit of that table, if any, without writing.
   The content patch closes the cell editor without writing (`closeBlockEdit(false)`), and no
   pending block navigation reopens it. The table shows the buffer. A change elsewhere keeps
   today's BLOCK-193 behaviour: it waits for the editor (see the open question).
   - The host needs the page editor's range while no host edit exists. Record `line` / `endLine`
     (and whether it is a cell editor) from the `previewEditOpen` message next to the editor id
     (`EditLock.openPageEditor` or `EditState`), and rebase it on each change. The offsets come
     from the document; reuse `rebaseBlockRange` from `src/core/state/blockRange.ts`. If the open
     message does not say that the editor is a cell editor, add an optional field to the
     page-to-host message, validated in `src/core/protocol/pageToHost.ts`.
   - Prose block editors are out of scope. They keep BLOCK-191's conflict error (the editor stays
     open with the reader's text). Only the table cell editor closes, because its text is
     autosaved live, so the buffer already holds it.
2. A rewritten block is never kept by the morph (fixes 1b). `ContentMorph` gets
   `invalidate(node: Node)`, which forgets the recorded key of the top-level block of the content
   container that contains `node`. `switchTableCell` calls it after `setCellInline`, and so does
   any other page path that writes text into a rendered cell. Grep `setCellInline` and the
   `renderedCellContent` writes. `restoreTableCellContent` puts back the original nodes and does
   not need it. The next content patch then rebuilds that table, whatever HTML it carries.
3. Secondary, only if the section 3 tests confirm the focus trigger: the pending block
   navigation does not reopen a cell editor after a structural save when the webview no longer has
   focus (`document.hasFocus()` false), consistent with "A cell editor must never stay open
   without focus". Do not ship it without a failing test.

## 3. Tests first (each must fail on a12a16bc)

Unit and contract:

- `test/page/modules/contentMorph.test.ts`: a recorded block, then `invalidate(child)`, then
  `replace()` with the same HTML: the node is replaced (kept 0). A block that is not invalidated
  is still kept (no regression for LIFE-069 / PERF-05).
- `test/page/runtimeTableCellEditor.test.ts` (or a new `test/page/runtimeTableCellStale.test.ts`):
  open the `alpha` cell, type ` X`, Tab, Escape. Apply a content patch whose table HTML equals the
  first render (`alpha`): the `td` shows `alpha`, not `alpha X`. This is the QA271-06 unit
  reproduction.
- `test/core/state/editLock.test.ts` and/or `test/core/state/blockRange.test.ts`: the page
  editor range is recorded at open, rebased by a change before it, and reported overlapping by a
  change inside it.
- `test/host/previewTiming.test.ts`: (a) page cell editor open, no host edit, outside undo
  overlapping the table: the render result is posted, not deferred. (b) The same with a host edit
  held: the edit is released without a write and the render is posted. (c) Outside change in
  another block: still deferred (BLOCK-193 kept). (d) A change the preview applied itself, or text
  typed in the source: still deferred.
- If the focus trigger of 1a is confirmed: a page runtime test where the pending navigation
  resumes with `document.hasFocus()` false and no cell editor opens.

Real input (real mouse and keys on the workbench), new file
`test/integration/realInput/tableStaleRender.ts`, wired in `test/integration/realInput/run.ts`
(a key such as `"table-stale-render"`):

- `scenarioUndoUnderCellEditorRendersTable` (replay 271-c3-2): fixture with the Alignment table
  and one earlier edit elsewhere in the undo stack. Click `c1`, Col − twice, Meta+1, Meta+z three
  times. Assert: the buffer equals the original, the `Left` table has 3 cells in row 0, and no
  `[data-sphinx-preview-table-cell-editor]` is left over the old structure.
- `scenarioRevertAfterExternalWriteRendersCell` (replay 271-c6-1, both parts): type ` X` in
  `alpha`, then rewrite the paragraph line on disk with `fs.writeFileSync` (the disk-write helper
  the sheet asks for, in `common.ts` if it is reusable). Then Tab, Escape, focus the source, and
  run `workbench.action.files.revert`. Assert: the buffer equals the disk, a `td` shows `alpha`,
  none shows `alpha X`, and the paragraph shows `EXTERNAL`.

Replays promoted from `qa/271-table-campaign-replays` (87307e8f) into the PR, unchanged:

- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c3-2-undo-after-column-deletes-leaves-preview-table-stale.json`
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c6-1-revert-file-leaves-preview-cell-stale.json`
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c6-1-revert-file-leaves-preview-cell-stale-part2.json`
- their fixtures `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/structure-tables.md`
  and `.../assets/synth/c6-concurrency.md`

Cite each replay name in the header comment of `tableStaleRender.ts`, as `qa210Replays.ts` does.

Visual (headless): add a page-level check that applies a content patch after a Tab rewrite and
asserts the rebuilt cell, if the table-editing group's convention calls for one
(`test/visual/capture_*.py` plus `test/visual/scenarioIds.ts`). Otherwise the group's existing
captures must stay green.

## 4. Requirements (okfreq; read `requirements/guidelines/` first)

None of the requirements touched is `approved` (all `req_lifecycle: proposed`), so no owner
agreement is needed.

| ID | Action | Status after |
| --- | --- | --- |
| SwRS-MDOKFSTUDIO-TABLE-119 (next free in table-editing; check against the stack) | New: "An outside change of the table under an open cell editor closes the editor and shows the buffer". Covers undo, redo, revert and an external write; the editor closes without a write; a change elsewhere waits as in BLOCK-193 | `proposed` (`okfreq new … --lifecycle proposed`), derives from StRS-MDOKFSTUDIO-TABLE-001 (or the table StRS that covers editing in place) |
| SwRS-MDOKFSTUDIO-LIFE-069 | Amend: add a scenario "a block whose content the page rewrote (a table cell left with Tab) is rebuilt by the next patch even when its host HTML is unchanged" | stays `proposed` |
| SwRS-MDOKFSTUDIO-BLOCK-193 | Amend: state the exception (a render of an outside change that overlaps an open table cell editor's table is not held), with a depends_on link to TABLE-119 | stays `proposed` |
| SwRS-MDOKFSTUDIO-BLOCK-191 | Amend: for a table cell editor, a conflicting outside change releases the edit and closes the editor instead of keeping it open with an error | stays `proposed` |
| SwRS-MDOKFSTUDIO-TABLE-035 | Touch markers only (the `invalidate` call sits next to its `setCellInline`); no text change | unchanged |

Add `@implements_req` next to the new code (`hostEvents.ts`, `blockEdits.ts`, `editLock.ts`,
`contentMorph.ts`, `tableCellEditor.ts`) and `@tests_req` at each test. Run
`just requirements-update`, add a dated entry in `requirements/tiers/log.md`, and run
`okfreq validate --check-links --project-root .` before the PR.

## 5. Files expected to change (for ordering the stack)

Source:

- `src/session/hostEvents.ts` (`refreshPreview`)
- `src/session/features/blockEdits.ts` (`openPageEditor`, `trackOutsideChange`, page editor range)
- `src/core/state/editLock.ts` (page editor range), possibly `src/core/state/blockRange.ts`
- `src/core/protocol/pageToHost.ts`, only if the open message needs a cell-editor flag
- `src/page/modules/contentMorph.ts` (`invalidate`)
- `src/page/features/tableCellEditor.ts` (`switchTableCell`; secondary: reopen without focus)
- `src/page/features/pageRuntime.ts` (`ContentMorph` / parts type), possibly
  `src/page/features/contentPatch.ts` (clear the pending navigation when the patch closes a cell
  editor) and `src/page/features/blockEditor.ts` (the `editorOpen` payload)

Tests: `test/page/modules/contentMorph.test.ts`, `test/page/runtimeTableCellEditor.test.ts` (or
the new `runtimeTableCellStale.test.ts`), `test/core/state/editLock.test.ts`,
`test/core/state/blockRange.test.ts`, `test/host/previewTiming.test.ts`, the new
`test/integration/realInput/tableStaleRender.ts`, `test/integration/realInput/run.ts`, possibly
`test/integration/realInput/common.ts`, and possibly `test/visual/capture_*.py` and
`test/visual/scenarioIds.ts`.

Requirements and docs: the four SwRS above plus the new one, `requirements/tiers/swrs/table-editing/index.md`,
`requirements/tiers/swrs/block-editing/index.md`, `requirements/tiers/swrs/lifecycle-sync/index.md`,
the generated coverage files, `requirements/tiers/log.md`, and `CHANGELOG.md`.

Skill: the five replay and fixture files listed in section 3. `structure-tables.md` is shared
with the c3-3 replay (CR `table-in-quote-or-admonition-editing`, not in this stack). Within the
stack, only identical copies of the same fixture can collide.

Likely overlaps in the stack: `tableCellEditor.ts` (279, 282, perhaps 280), `blockEditor.ts`
(280 or 282), `run.ts`, `requirements/tiers/log.md`, the scope indexes, `CHANGELOG.md`, and the
next free TABLE SwRS ID (allocate in stack order). The host-side files (`hostEvents.ts`,
`blockEdits.ts`, `editLock.ts`, `contentMorph.ts`) are probably unique to this CR. 281
(front matter) only meets it in BLOCK-193 if it touches the deferred properties table.

## 6. Blast radius

- The render deferral (BLOCK-193) is the guard that keeps open editors alive through saves and
  theme or diagram updates. The exception is narrowed to outside changes that overlap an open cell
  editor's table. The preview's own saves (`isApplying`) and the writer typing in the source must
  never hit it: tests (d) and (c) guard this. A wrong range rebase would close a cell editor under
  the writer's hands. Check that typing in the source next to the table does not close it.
- The morph `invalidate` costs one rebuild of the table on the next patch: any Mermaid or image
  inside that table is redrawn (rare in a cell). No other block is affected.
- A content patch closing the editor must not post a final save (that would overwrite the undo)
  and must not reopen it through the pending navigation.
- Integration stress: the real-window suites that edit tables while renders are in flight
  (`tableEscape`, `wideTableTab`, `blockKeys`, `renderPatching`) are the ones to watch.

## 7. Gates

- `just check` (format, TypeScript, boundaries, file size: `tableCellEditor.ts` is about 600
  lines, keep new logic in `contentMorph.ts` and the host files; unused exports, unit, contract)
  and `just requirements-lint`.
- Headless visual of the group: `uv run --no-sync --group docs python test/visual/capture.py
  --group table-editing` (and `--group lifecycle-sync` because of the morph change), after
  `npm run visual:render`.
- Heavy CI on the branch (real VS Code integration and stress):
  `gh workflow run ci.yml --ref <branch> -f heavy=true`. Both new real-input scenarios must pass
  there, and the two promoted replays must pass when run with the QA skill.
- `just preflight` before the task is complete (constitution, section 4).

## 8. Open question (owner)

- A change outside the edited table (for example the third undo of c3-2, which touches another
  block) still waits for the open cell editor to close (BLOCK-193). That other block stays stale
  until then. The spec's default keeps this, because rendering under an open editor is what
  BLOCK-193 forbids. The editor's own table is always correct after this CR. If "the preview
  always matches the buffer after an undo or a revert" should also cover the other blocks, then
  any undo, redo or revert must close every open inline editor and render, prose editors
  included. That is a wider change to BLOCK-191 and BLOCK-193. Default if no answer: keep the
  narrow scope.
