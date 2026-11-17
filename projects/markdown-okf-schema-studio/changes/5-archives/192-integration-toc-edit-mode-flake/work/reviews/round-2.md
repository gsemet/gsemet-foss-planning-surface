# 192 — Inspector review, round 2

Worktree `markdown-okf-schema-studio-wt-192`, branch `change-requests/192-integration-toc-edit-mode-flake`.
Uncommitted diff: `test/integration/realInput/harness.ts` (+203 −12), `test/integration/realInput/run.ts` (+6),
`test/shared/stressPlan.ts` (+2). Gates: green per `/private/tmp/claude-502/cr192-driver/coder-r2-check.log`
(pytest 80 passed, requirements 1067/0/0, lint and coverage unchanged). I did not run them again.

## Round-1 findings

1. **Fixed. No click before the page has booted.** `harness.ts:369` `waitForEditModeRuntime` waits on state:
   a current frame whose `<html>` carries `data-sphinx-preview-edit-mode`. It is bounded by `waitFor`'s 10 s
   default, and its timeout message names the last mode and `webviewReady`. Inside `withCurrentFrame`, the
   predicate `clickable` requires `state.mode !== null`, so a replacement frame that has not booted is never
   clicked. Loop bounds: the `click -= 1; continue` branch (`harness.ts:380-386`) runs only when mode is
   null, and it increments `bootWaits` before the check, so the fifth unbooted read throws. In the worst case
   there are 3 counted clicks and 4 boot waits, each with its own time limit, so the loop cannot run forever.
   Every iteration that clicks is counted. The "replaced" and "never reached" outcomes `continue` to the
   next `click`, and every other outcome returns or throws. I checked that the boot order matches the
   premise: `runtime.ts:422` `rt.editMode.bindButton()` runs before `runtime.ts:436` → `contentPatch.ts:98`
   `applyEditMode`.
2. **Fixed. The diagnosis is corrected.** `diagnosis.md` now has an explicit "Round 2 correction" paragraph
   on `_checkFrameIsHitTarget` (a lasting cover gives a click timeout, not a lost click). The lost-click
   cause is re-ranked last (cause 4) and narrowed to a race between the hit check and the dispatched mouse
   events, or to OOPIF input routing. The pre-boot cause (2) and the non-idempotent re-click cause (3) are
   added. Each cause is labelled "Inferred", and only the line mapping, the throw site and the missing
   artifacts are labelled "Proven". That split is honest.
3. **Fixed. The diagnostic reads are bounded and non-fatal.** `harness.ts:312` uses `boundingBox({ timeout: 250 })`
   with `.catch(() => null)`, and the workbench `page.evaluate` has `.catch(() => "unreadable")`. The
   final failure path also turns an `editToggleState` error into a string (`then(..., String)`), so a
   diagnostic read can no longer replace the real failure.
4. **Fixed. The wording is corrected.** The doc comment and the messages now say "reached the toggle in the
   page". The comment states that the counter does not prove the toggle's own listener ran.
5. **Addressed in the CR text. It remains a delivery duty.** `diagnosis.md` ("What the test change does")
   says that this is instrumentation plus stress coverage, not a proven fix. It says the backlog item stays
   open and that logs must be grepped for `setEditMode … switched on click #`. The Driver must carry this
   into the PR body and into the backlog handling. See note C.

## Re-checks

- **Nothing is weakened.** There is no `force: true` (the one hit, `harness.ts:81`, is `fs.rmSync`), no
  skipped test and no changed assertion. The per-attempt window stays at 1.5 s. The new 10 s waits
  (`harness.ts:369` and `:424`) wait on state, return as soon as the state holds, and fail loudly with the
  recorded state. Before this change, the 1.5 s at `:424` led to a blind re-click. Now nothing is
  re-clicked there, so the longer limit cannot hide a race. It only turns a revert into a loud failure.
- **The helper cannot hide a product bug.** I checked that the toggle handler is synchronous
  (`editMode.ts:198-214` → `applyEditMode`, `editMode.ts:47-74`, which sets the attribute in the same
  task). So when the probe counts a click and the mode on that same read is not the wanted one, the page
  really did not apply the toggle. The fail-fast at `harness.ts:418-421` is sound and cannot blame the
  product falsely. A late or failed click can no longer be covered by a blind re-click.
- **Callers stay compatible.** There are 90 call sites in 21 files, and the signature and return value
  (`currentPreviewFrame(page)`) are unchanged. No caller expects a rejection. `realWindowGaps.ts:53` and
  `common.ts:96` (`leaveEditModeOff`) call the helper right after `findCurrentFrame`, and they now wait for
  boot instead of clicking an unbound toggle, which is an improvement. `leaveEditModeOff` still swallows
  errors, as before. The untrusted read-only scenario does not call `setEditMode`. The
  `integrationEditModeRestore.test.ts` source check still passes, because `tocWindow.ts` already contains
  both calls.
- **TypeScript.** The `as` casts on `after` and `replaced` (`harness.ts:396-397`) stop TypeScript from
  narrowing variables that the closure assigns. Narrowing after `after === undefined` is correct, and the
  helper ends with an explicit `throw` after the loop, so the function has no implicit `undefined` return.
  The compile gate is green.
- **Stress.** `run.ts` and `stressPlan.ts` keep the same key order, and the wrapper closes the sidebar that
  the scenario reopens. This is unchanged from round 1 and still correct.

## Non-blocking notes (no further round needed)

A. **A late click on a green run passes silently.** At `harness.ts:389`, take an attempt that was judged
   "lost" (the counter did not move within 1.5 s) whose click then lands late and switches the mode. The
   next iteration sees `mode === wanted` and returns at `:389`, without the `console.log` at `:436`. The
   diagnosis promises that "a green run with a retried click logs the attempts too", but this is exactly
   the late-delivery evidence for cause 3/4, and it is lost. It takes one line to fix: when
   `click > 1 && attempts.length > 1`, log the attempts before the return at `:389` (the `before.state.clicks`
   in the record already shows the late arrival). This is recommended, but it does not block: the test
   outcome is correct either way.
B. **`harness.ts:410-411` gives the wrong label.** `after === undefined` without `replaced` can also mean
   that every read in the 1.5 s window failed with a detached-frame error before `isDetached()` turned true.
   The label "the clicked frame was replaced" is almost always right anyway. This is cosmetic.
C. **What the Driver must deliver for finding 5.** The PR body must say "instrumentation + stress coverage,
   no proven cause". It must list the outcomes that point at the product: "reached the toggle … page shows
   mode on" (`editMode.ts` `applyEditMode`, check `errors[]`), "then the current render shows" (the
   theme-render path), and a boot timeout (`runtime.ts`). The backlog item must stay open or get a
   follow-up. Also grep the heavy and stress logs for `switched on click #`.
D. **Pre-existing behaviour, which this change does not alter.** When `withCurrentFrame` re-runs the action
   after a detached-frame error thrown *during* the click, the click on the old frame is not recorded. The
   old frame is gone, so this does not affect the outcome.

## Verdict

**APPROVE.** All five round-1 findings are fixed, or are carried to delivery (5, note C). The change
weakens nothing, keeps every caller compatible, and does not mask a product bug. Note A is a cheap
improvement to the evidence, and I recommend it if the Driver runs another round for other reasons.
