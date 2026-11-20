# Diagnosis: `paste-url` red in the heavy dispatch of 768570c (run 44647675614)

## Verdict

A race between the test and the page-state gate of the host, not a defect of CR-350. The CR cannot
cause it: the integration job builds and runs byte-identical code at abeb761 and 768570c. The
wait that fails (`pasteUrl.test.ts:155`) checks a host value that, since b84b0585 (2026-11-03,
"always open a document in preview mode"), **no product code reads**, and that the specification
lets stay stale (SwRS-MDOKFSTUDIO-LIFE-169, refusal scenario "A stale message stores nothing":
a `previewEditModeChanged` naming an older render is dropped before its handler). The fix is in
the test (CI rule 12: a flake fixed at its cause), not in the product.

## Reproduction

- CI: `gh workflow run ci.yml --ref chantier/batch-06/cr-350-build-the-gallery-and-site-on-a-heavy-ci -f heavy=true`
  (failed on attempts 1 and 2 of run 44647675614; green at abeb761 run 44639811161 and e5b4b27 run 44639515404).
- Local, one scenario in a loop (one VS Code window at a time, not run by me: it opens a real
  window on the desktop shared with the other batch agents):
  `STUDIO_REAL_INPUT_SCENARIO=paste-url npm run test:integration` (trusted-suite.ts:226).
  `paste-url` is not in the stress plan, so `stress_scenarios` cannot loop it.

## What the logs prove

Step timings (`STEP start/done` lines, logs saved in `work/debugger/`):

| Run | Commit | grid-card-editor-blur | paste-url |
| --- | --- | --- | --- |
| 44639515404 (green) | e5b4b27 | 4369 ms | done 2385 ms |
| 44639811161 (green) | abeb761 | 4171 ms | done 2470 ms |
| 44647675614 attempt 1 | 768570c | 4413 ms | failed 12560 ms |
| 44647675614 attempt 2 | 768570c | 4042 ms | failed 12422 ms |

- The step order is the same in all runs (20 identical steps up to `paste-url`); same VS Code
  1.147.0 (286f582d), runner images differ per run (20261111.82, 20261116.202, 20261111.196):
  nothing points at the runner.
- 12.4-12.5 s = the healthy 2.4 s + the 10 s default of `waitFor` (harness.ts:51-68): every step
  before line 155 ran at its normal speed and passed, and the host still held `true` for the whole
  10 s.
- `setEditMode(page, false)` (line 154) returned without error, so either its click reached the
  toggle and the page then showed and kept `data-sphinx-preview-edit-mode="off"`
  (harness.ts:500-532), or the page already showed off (harness.ts:488).
- `CodeWindow: failed to load (code -3)` appears in a green run's `paste-url` too: not the cause.

## What the logs do not prove

- Which page message was dropped and why: the host drops a stale `previewEditModeChanged`
  silently (`reportStaleEdit`, src/session/pageMessages.ts:237-255, answers only edit saves,
  opens, checkboxes and front-matter saves), and nothing logs the stage identity. The artifacts
  (`e2e-integration-attempt-2`, under `work/debugger/artifacts-44647675614/`) hold only the
  screenshots and the manifest, no host trace and no hang dump for this step.
- Why the window was hit twice in a row at 768570c and never in the three green runs: with
  identical code, this is timing; two runs are too few to give a rate.

## Code paths

Write path of the stored edit mode:

1. Page, src/page/features/editMode.ts:221-236: the toggle click posts `previewEditModeChanged`
   with `context.revision` and `context.requestId` (the identity of the render the page holds),
   then `applyEditMode(false)`.
2. Host, src/session/pageMessages.ts:131-132 then `handlePageState` (:266-304): the message is in
   the `page-state` family (:57); `manager.matchesCurrent` (src/session/previewManager.ts:170-186)
   requires `message.revision === stage.activeDocumentRevision` and
   `message.requestId === stage.requestId`; otherwise `reportStaleEdit` and return: dropped.
3. Handler, src/session/features/viewState.ts:63-67 -> `WorkspaceChoices.setEditMode`
   (src/session/workspaceChoices.ts:171-173): `workspaceState.update` (VS Code's Memento sets the
   value in memory at once, so a handled message is seen by the next poll).

Read path: `storedEditModeForTests` (src/host-vscode/testHooks.ts:194-197) reads
`choices.editMode` (workspaceChoices.ts:165-168). No other reader: the page boots its edit mode
from the panel's saved state only (src/page/runtime.ts:370-371), which `setMode` updates itself
(editMode.ts:231-235).

The only ways for the host to hold `true` for 10 s after the toggle went off are therefore (a) the
off message dropped at the gate (page identity older than the host's stage: the host staged a
newer render and its content patch, src/page/features/contentPatch.ts:68-69, had not reached the
page when the toggle was clicked), or (b) `setEditMode` returning at harness.ts:488 with no click.
(a) is the likely one: `paste-url` toggles off right after the autosave reaches the buffer
(pasteUrl.test.ts:143-154) with no wait for the render that follows; `drop-files` waits for it
first (`waitForRender(source)`, dropFiles.test.ts:132) and passed in every run. Neither is proved
without a host trace.

## Why the wait is obsolete

CR 152 (724841e6, 2026-10-28) added the wait because the stored edit mode then made the next
preview open in edit mode. b84b0585 (2026-11-03, after it) made every document open in preview
mode: the stored value seeds no page any more (workspaceChoices.ts:165 says so). The wait now
guards a cause that no longer exists, and it asserts something the specification does not promise
(LIFE-169 drops a stale report by design).

## Fix (at the cause, test only; no product change)

1. test/integration/pasteUrl.test.ts:155: remove the `storedEditModeForTests` wait (and its
   import, line 6). Keep `setEditMode(page, false)` (line 154): it already waits until the page's
   current render keeps edit mode off, which is what the next scenario depends on (it opens its
   own preview, booted from its own saved state).
2. Same for test/integration/dropFiles.test.ts:138 (and the import, line 8) and
   test/integration/findInPreview.test.ts:368 (keep the page-side wait at :366-367; `editModeBefore`
   at :109 and the diagnostic at :151 can stay or go).
3. Update the stale rationale: the comments at pasteUrl.test.ts:151-153, dropFiles.test.ts:137 and
   the docblock of test/build/integrationEditModeRestore.test.ts:10-17 (the guard itself, "who turns
   edit mode on turns it off", stays valid and needs no change), and SwRS-MDOKFSTUDIO-BLOCK-004 /
   PALETTE-264 if they describe the workspace wait.
4. Optional, product observability only: log a dropped page-state message's type and both
   identities at debug level in `reportStaleEdit`, so the next race of this family names itself.

If the owner prefers to keep a host-side check instead, the test must first wait for the render
the autosave starts (`await waitForRender(source)`, as dropFiles.test.ts:132 does) before
`setEditMode(page, false)`; that narrows the window but does not close it, so I do not recommend it.

Proof by repetition (rule 12): after the fix, a heavy dispatch at the fix's head, plus a local loop
of `STUDIO_REAL_INPUT_SCENARIO=paste-url` (and `drop-files`), green every time.

## Not done

- No local real-window run (shared desktop, parallel batch agents).
- The comparison runs 44651923296 (CR-349 at abeb761) and 44651927198 (main 24c9eef) had not
  finished their `integration` job when I wrote this; a red `paste-url` in either would confirm
  that the race is independent of CR-350.
