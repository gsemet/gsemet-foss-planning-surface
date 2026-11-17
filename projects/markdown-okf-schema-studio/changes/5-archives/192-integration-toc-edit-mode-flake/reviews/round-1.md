# 192 — Inspector review, round 1

Worktree `markdown-okf-schema-studio-wt-192`, branch `change-requests/192-integration-toc-edit-mode-flake`,
base `cb1f2adc`. Uncommitted diff: `test/integration/realInput/harness.ts` (+164 −12),
`test/integration/realInput/run.ts` (+6), `test/shared/stressPlan.ts` (+2).
Gates: `just check` green (Coder log `/private/tmp/claude-502/cr192-driver/coder-r1-check.log`,
requirements 1067/0/0, pytest 80 passed). Not re-run.

## What is good

- No `force: true`, no skipped test, no weakened assertion. The per-attempt budget stays at 1.5 s, and
  the new 10 s wait (`harness.ts:385`) waits on state: the current render showing the wanted mode.
- The retry is no longer blind. The helper clicks again only when the probe shows the click never
  reached the page, or when the frame was replaced (`harness.ts:371-378`). If the page received the
  click and ignored it, the helper fails at once (`harness.ts:380`). This makes the helper stricter,
  so it cannot hide a product bug. It only makes one show sooner.
- The probe only records. It adds a capture-phase `click` counter and a window `error` listener, with
  no `preventDefault`/`stopPropagation`. It is re-installed per document, because it is keyed on
  `window`. `page.evaluate` on the workbench only reads.
- The return type and contract are kept: the helper still returns `currentPreviewFrame(page)`.
  I found no caller (89 call sites) that wraps `setEditMode` in `assert.rejects`/`try` or depends on
  the old slow failure when the toggle is absent or `aria-disabled`. The new fail-fast messages
  (`harness.ts:350-351`) are an improvement.
- The stress list is correct. The key order of `run.ts:41-59` matches `stressPlan.ts`, which
  `runStress` asserts. The wrapper closes the sidebar that the scenario's `finally` reopens with
  `toggleSidebarVisibility` (`tocWindow.ts:210`). Cost is about 10 × (5-8 s + two theme switches),
  which is acceptable for a scenario that has failed twice. The scenario leaves edit mode on, but
  `table-tab`, `slash-menu`, `alert-dropdown` and the others already do, so this adds no new
  coupling between stress scenarios.
- No overlap with PR #193: it touches none of these three files.
- `diagnosis.md` is honest. Proven items are proven (the compiled line mapping, the throw site, and
  the fact that the artifacts hold no page state). The ranking is explicitly labelled "none proven".

## Findings

1. **[must fix] A page that has not booted yet is clicked, and then reported as a product bug.**
   `harness.ts:345` clicks whenever `state.mode !== wanted`, and that includes `mode === null`.
   `data-sphinx-preview-edit-mode` exists only at runtime. It is set by
   `contentPatch.ts:98` `initializeContent` → `applyEditMode`, which runs *after* `runtime.ts:422`
   `rt.editMode.bindButton()`. No server HTML sets it (`grep preview-edit-mode src/` outside styles).
   Meanwhile `findCurrentFrame` (`harness.ts:116-134`) matches on server-rendered attributes only, and
   many callers call `setEditMode` right after `waitForRender` (`harness.ts:102`). `waitForRender`
   checks the host phase, not `webviewReady`. One example is
   `textEditing.ts` `scenarioFrontmatterStructuralMinimalPatch`, a stress scenario. In that window the
   probe counts the click, because the probe is the test's own listener. No toggle handler is bound
   yet. Then the after-read sees `null`, or the boot value, and `harness.ts:380` throws "the toggle
   received click… page shows mode …", which points at the product. The old helper recovered from
   this with its retry. **Fix:** treat `mode === null` as "runtime not booted". Wait on state for the
   attribute to be set, or for `getActivePreviewForTests().webviewReady`, before the first click. Do
   not click, and do not count the attempt, while it is null.

2. **[must fix, diagnosis text] Cause 2's mechanism is wrong.** `diagnosis.md` says "Playwright's
   in-frame hit check does not see the workbench". Playwright 1.64.1, the version in the worktree,
   runs `_checkFrameIsHitTarget` before every non-forced click
   (`node_modules/playwright-core/lib/coreBundle.js`). It walks `frame.parentFrame()` up to the
   workbench and checks that each iframe element is the hit target at the click point. If it is not,
   the click is retried until the action timeout. So a workbench element that covers the webview
   produces a Playwright *click timeout* ("… intercepts pointer events"), not a silently lost click.
   That does not fit the observed 6.9 s step. Correct the text. Cause 2 then narrows to "a cover or
   relayout between the hit check and the dispatched mouse events", or input routing to the
   webview's out-of-process iframe dropping the event. Re-rank accordingly. The `workbenchHit` field
   can stay, because it is cheap evidence.
   Optional, inferred: also list the hypothesis that the toggle is *not idempotent*. If a click
   arrived after the old helper's 1.5 s window, the old helper's re-click could cancel it
   (on→off→on). The new counter makes that visible (`clicks` +2).

3. **[should fix] A diagnostic read can turn into the failure itself.** `harness.ts:310`
   `frame.locator(EDIT_TOGGLE).boundingBox()` uses Playwright's default 30 s locator timeout. It runs
   inside the 1.5 s poll at `harness.ts:357-366`. If the toggle disappears between the `evaluate`
   and this call, for example during a same-frame document load, the call blocks for up to 30 s. It
   then throws `locator.boundingBox: Timeout …`. That error is not a detached-frame error, so
   `waitFor` rethrows it. It also does not match the string checked at `harness.ts:368`, so
   `setEditMode` fails with a Playwright timeout and none of the recorded state. **Fix:** give this
   read a short timeout and make it non-fatal (`.catch(() => null)` → `workbenchHit: "unreadable"`).
   Better still, compute the point from `frame.frameElement().boundingBox()` plus the in-frame rect
   that the `evaluate` already returns. The same goes for the `page.evaluate` that follows.

4. **[should fix] The failure wording overclaims.** The probe counts clicks at `document`, in the
   capture phase (`harness.ts:265-267`). That proves the event reached the page with a target inside
   the toggle. It does not prove that the toggle's `click` listener ran. A listener between the
   document and the button that calls `stopPropagation` would look identical. Reword
   `harness.ts:381` and the doc comment at `harness.ts:322-333` to "the click reached the toggle in
   the page" or similar, so that the next failure is read correctly. The message already carries
   `errors[]`, so a throw in `applyEditMode` (cause 1) will show. That part is good.

5. **[must, delivery] Present this as instrumentation, not as a fix.** No cause is proven. The
   change makes the next failure name its cause, and it puts `toc` under stress (rule 12). It does
   not remove the flake. The PR body must say so: what was observed, what the helper now records,
   and which outcomes would point at a product bug (`editMode.ts` `applyEditMode`, or the
   theme-render path). The backlog item must stay open, or be replaced by a follow-up, until a run
   records the state. If the stress job reproduces it, that run's message is the diagnosis to act
   on. Closing the backlog item as "fixed" would ignore the flake.

## Non-blocking notes

- `run.ts:55-58`: `closeSidebar` is not in a `finally`. That is fine, because a failure aborts the
  round anyway.
- `let after = undefined as … | undefined; let replaced = false as boolean;` (`harness.ts:355-356`)
  works around TypeScript narrowing inside a closure. It is acceptable and the comment explains it.
- A run where a retried click succeeds logs its attempts (`harness.ts:397`), which is good. The
  Driver should grep heavy and stress logs for `setEditMode … switched on click #` and report any
  match, because a lost click on a green run is still evidence.

## Verdict

**CHANGES REQUESTED.** Fix findings 1, 2 and 5. Findings 3 and 4 are strongly recommended, because
both are small and both protect the diagnostic value of the change.
