# Diagnosis CR-439 red CI (head d5fb2548)

## 1. Visual (run 44843222793): caused by this CR. Not a flake.

Reproduction (local, Windows, reproduces exactly):

    npm run visual:render
    uv run --no-sync --group docs python test/visual/capture.py --scenario palette-slash/v05-mode-strict-light-900 --workers 1

Output: `failed: ... 05-long-chapter--light--sticky-3--default.html: check_palette_mode: Locator.wait_for:
Timeout 2000ms exceeded. waiting for locator(".sphinx-preview-block-editor").locator("textarea") to be visible`
(same message as CI; v06 to v10 share the page and the check).

Cause: `test/visual/capture_comment_checks.py:1059` (check_palette_mode) picks the insertion point with
`main .sphinx-preview-insert-point:not(.sphinx-preview-insert-point--start) button` `.nth(3)`, then
`click(force=True)` and expects the insertion editor to open. Each point held 3 buttons
(insert, move up, move down; `insertPoints.ts` createInsertPoint then `blockMoves.ts` addMoveButtons), so index 3
was the "Insert a block here" button of the second point. This CR appends a 4th button, the Delete block
button (`src/page/features/blockMoves.ts` addMoveButtons, new `createDeleteBlockButton`, class
`sphinx-preview-delete`). Index 3 is now the Delete button of the first point: the forced click deletes a block
(or starts a delete) and no editor opens, so the textarea wait times out. The product is right; the test
selector counted buttons by position.

Proof the selector is the only problem: probe `work/debugger/probe_selector.py` (outside the project; it
re-defines check_palette_mode with the selector `button:not(.sphinx-preview-delete)` and runs the same scenario):

    uv run --no-sync --group docs python <probe_selector.py>   (from the worktree)
    passed: palette-slash/v05-mode-strict-light-900
    {"status": "passed", "scenario_count": 1, "screenshot_count": 1}

Minimal fix: in `test/visual/capture_comment_checks.py:1059` select the insert button, not by position among all
buttons, e.g. `... .sphinx-preview-insert-point:not(.sphinx-preview-insert-point--start) > button:not([data-sphinx-move]):not(.sphinx-preview-delete)` with `.nth(1)`
(the second point's insert button, same target as before), or equivalently keep `button:not(.sphinx-preview-delete)` `.nth(3)`.
Also grep the visual and integration tests for other positional `button` indexes in insert points
(`test/integration/realInput/blockKeys.ts:299` uses `[data-sphinx-move='down']` `.nth(1)`, which is unaffected;
`renderPatching.ts:547,602` already exclude `[data-sphinx-move]` but would match both the insert and the delete
button if there is no `.first()`: check that `button:not([data-sphinx-move])` resolves to one element, since the
Delete button now also matches and Playwright strict mode fails on 2 matches. Those run in the heavy job).

## 2. Integration checkbox-toggle (heavy run 44843255214): flake of the frame lookup, not this diff (no proof of the contrary; not locally reproducible).

Evidence: the failure is `findCurrentFrame` (harness.ts:130) `locator.count` on a frame (url empty) exceeding its
own 10 s guard, in `currentPreviewFrame` called at checkboxToggle.test.ts first frame lookup, before edit mode
is turned on. The CR's page changes (delete button, delete keys, `deleteWhenEmpty`) act only in edit mode, and the CR
touches no integration code except the new emptyBlocks test and its line in trusted-suite.ts. The failure dump shows the
correct frame already present (fake.html, version 1, request 1, document tasks.md), so the render was fine; a
Playwright call on a transient empty frame hung. That is the class the harness comment cites (CI run 43500084136).
Earlier steps of the same run (preview-smoke, stock-coexistence, scroll-sync) passed; main heavy run 44830737763 passed.

Caveat: an unproven flake. To settle it, re-run the heavy job on the branch after the visual fix:
`gh workflow run ci.yml --ref chantier/batch-07/cr-439-empty-blocks-leave-no-blank-lines-and-a- -f heavy=true`.
If checkbox-toggle fails again at the same call, escalate. Note: a later heavy step may also fail on the
`button:not([data-sphinx-move])` matches (section 1), which the cut-off run could not reach.

## 3. Integration emptyBlocks (run 44847413533): the test sends messages the host validator rejects (test bug, deterministic)

Failure: `AssertionError: lf: the autosave wrote the placeholder line` (emptyBlocks.test.ts:102), in the second fixture
(`empty-blocks-emptied-lf`); the first fixture (Delete block, LF, plus its undo) passed. The step lasted 5813 ms: the
20 x 250 ms retries of `untilApplied` ran out, so every send was silently dropped (no "stale" or error log line).
Not a flake, not the CI environment, not timing, not the autosave flush.

Cause: `sender()` (test/integration/emptyBlocks.test.ts:38-46) adds `pinViewportTop: 200` to every message. For a
`previewEditSave` the validator `hasValidStateFields` (src/core/protocol/pageToHost.ts:150-155) accepts `pinViewportTop`
only together with a valid `pinLine` AND only on a final save (`pinOwner`). So:

- the autosave (`final: false`) with `pinViewportTop` is malformed: `isPageToHostMessage` is false, `PageMessageDispatcher.handle`
  (pageMessages.ts:110-113) returns undefined, the document never changes;
- the two final saves (`final: true, deleteWhenEmpty: true`) carry `pinViewportTop` without `pinLine`: also malformed, so they
  would fail next (`direct` fixture, and the second half of `emptied`).
- `previewBlocksDelete` is validated by its own function (pageToHost.ts:292-320) where `pinViewportTop` alone is valid, which is why
  the Delete fixture passed.

Proof (probe `work/debugger/probe_pin.cjs`, runs the compiled validator; `node <probe> <worktree>`):

    autosave + pinViewportTop (test as written)      false
    autosave without pin                             true
    final+deleteWhenEmpty + pinViewportTop only      false
    final+deleteWhenEmpty + pinLine+pinViewportTop   true
    final+deleteWhenEmpty, no pin                    true
    previewBlocksDelete + pinViewportTop             true

Product code is fine: protocol allows `deleteWhenEmpty` only with `final: true` (pageToHost.ts:163-164), the handler
(blockEdits.ts:421-509, 336-409) and `planEmptiedBlockRemoval` were read and nothing drops this message once valid. Not run
end to end: the integration suite needs VS Code under a screen (CI; Windows runs only the static stage), so the claim
rests on the validator probe plus the code reading; the heavy job re-run is the end-to-end check.

Fix (test only, test/integration/emptyBlocks.test.ts):
1. In `sender`, drop `pinViewportTop: 200` from the base fields (the Delete block message does not need it either).
2. For the two final saves add `pinLine: 3, pinViewportTop: 200` (final saves are the pin owners); leave the autosave and
   `previewBlocksDelete` without pin fields (or keep it on Delete only).
No product change. Then re-run: `gh workflow run ci.yml --ref chantier/batch-07/cr-439-empty-blocks-leave-no-blank-lines-and-a- -f heavy=true`.
Residual risk: after this, the next assertions of this test (expected text, one or two undos, CRLF) have never run, so they may
show a separate failure; they are unverified by this diagnosis.
