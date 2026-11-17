# Review round 1 — CR 224 (Comments button hides every review mark)

Inspector, independent review of the uncommitted change in
`markdown-okf-schema-studio-wt-224` (base origin/main 0b4ede78).

Verdict: CHANGES REQUESTED

The code is correct and matches the seven owner choices. The tests are sound and fail on the
unchanged code. I am asking for two small additions before the PR: a test for the setting's link
to the thread module, and the user docs.

## What I checked

- **Owner choices 1–7 against the code.**
  - The CSS covers both attributes. Its specificity (1,2,2) beats the resolved underline rule
    (1,2,1) and the `badge-after` `display:block` rule (1,2,1).
  - `intercept` (click and dblclick) and the Enter/Space keydown return early while hidden. They
    neither prevent nor stop the event, so the page-input reveal and the edit-mode handlers
    receive it.
  - `paintFocus` is used on the attach path, so marks created by a re-apply while hidden get no
    tabindex. `visibilityChanged()` repaints `addedMarks`, which `clear()` resets, so there are no
    stale nodes.
  - `apply()` does not reopen a popover while hidden, and `openThread()` returns false while
    hidden.
  - Badges and orphan entries are `display:none`, so they leave the Tab order.
  - The compose (selection Comment) module does not depend on the thread module: it stays
    available.
  - A thread created while hidden reaches the page through `setThreads` → `apply` → `attach`, so
    it stays hidden.
  - Setting toggled while the button is off: `hidden()` ORs both attributes, so the marks stay
    hidden until both triggers say "show".
  - Popover open on Hide: it closes. For the button, the pointerdown-outside handler already
    closes it and `visibilityChanged` does it again. For the setting, `hostHandlers` →
    `visibilityChanged`.
  - A pending reply or action timer after a forced close is harmless, because `paintReply`
    returns when there is no popover.
- **Tests fail on the old code.** I extracted HEAD with `git archive` into a scratch directory,
  copied in the new and modified tests, compiled and ran them:
  - `previewStyles.test.ts`: the new test fails.
  - `commentThreads.test.ts`: the 3 new tests fail (39 pass).
  - `runtimeCommentsHidden.test.ts`: the hidden case fails and the shown case passes.

  No existing assertion was changed. There are no retries, skips or raised timeouts.
- **Real-input `scenarioHiddenReviewMarks`.**
  - It uses `waitFor` polling, not fixed sleeps.
  - It restores the Comments choice, the toolbar state and edit mode in `finally`.
  - `tabIndex: -1` is the right DOM value for a `mark` without a tabindex.
  - The edit-mode click asserts that the block editor opens and that no popover appears.
  - It would fail on the old code, where the click opens the popover and no editor opens.
- **Requirements.**
  - REVIEW-152 and REVIEW-021 are `proposed`, and their text matches the behaviour.
  - The markers are correct: `@implements_req REVIEW-152` sits on `hidden`, `visibilityChanged`
    and the hostHandlers call; `@tests_req` tags are on every new test and visual scenario.
  - StRS-REVIEW-012 (`approved`) changed only inside its generated
    `<!-- okf:links -->` block (the SwRS title). The index and coverage checks report "0 would
    change", so nothing was hand-edited.
  - The log.md entry is fine.
- **Gates (run by me).**
  - The worktree's own `.venv` now has okf_schema 0.17.0. `STUDIO_OKFREQ` is no longer needed.
  - `env -u VIRTUAL_ENV UV_NO_CONFIG=1 just check` exits 0:
    - unit: 3326/3326 pass;
    - security: 71/71 pass;
    - contracts: 0 tests, as on main;
    - boundaries, limits, markers, exports and settings all pass;
    - requirements lint/coverage: 0 changes.
  - `okfreq validate --check-links`: 1072 requirements, 0 errors, 21 warnings. The warnings are
    older and in other files.
- **Shots.**
  - `before-comments-off-*`: the highlight, the underline and the Orphaned box are still visible.
  - `after-comments-off-*`: everything is gone, the text stays, the button shows "Show comments".
  - `after-hidden-highlight-click-*`: no popover after a click on the former highlight.
  - `before-hidden-highlight-click-light`: the popover opens (the reproduced bug).
  - The visual report `out/reports/e2e/screenshots/visual/review-annotations/v29…json` shows
    `failures: []`.

## Findings

1. **major — the setting's link to the thread module is not tested**
   (`src/page/features/hostHandlers.ts:46-47`). If you delete
   `parts.commentThreads.visibilityChanged()`, no test fails. The commentThreads tests call
   `visibilityChanged()` directly. `runtimePageControls.test.ts` T15 checks only the attribute.
   The real-input and visual scenarios use the button, not the setting. So owner choices 3 and 4
   for the setting have no test: a popover open when the setting turns false must close, and the
   highlights must leave the Tab order. Constitution §3 asks for a test that fails on the previous
   code. **Fix:** add a runtime-harness test, for example in `test/page/runtimeCommentsHidden.test.ts`:
   - with comments shown, click a mark so the popover opens;
   - dispatch `previewShowComments` with `showComments: false`;
   - assert that the popover is removed;
   - optionally, assert that a mark created by `previewComments` has no tabindex, then dispatch
     `showComments: true` and assert that tabindex is `0`.
   Tag it `@tests_req SwRS-MDOKFSTUDIO-REVIEW-152` and add the method to REVIEW-152's
   verification notes.

2. **minor — the user docs still say the button hides only the chips.**
   - `docs/user/toolbar.md:12-13`: "the Comments toggle (hides or shows the gray comment chips…)".
   - `docs/user/settings.md:23-27`: "Off here hides the gray chips and the green thread chips".
   - `docs/user/review-comments.md` does not say that hiding comments also hides the highlights,
     badges and Orphaned box.

   The `package.json:240` description of `preview.showComments` is also out of date. It mentions
   gray chips only, and it was already behind before this CR. **Fix:**
   - update toolbar.md and settings.md, with one sentence in review-comments.md;
   - optionally, update the package.json `markdownDescription`;
   - add a one-line `## Unreleased` entry in `CHANGELOG.md`. Recent `fix(…)` commits do not
     always add one, but this change is visible to users.

3. **minor — REVIEW-152 verification notes: the setting path.** Once finding 1 is fixed, update
   the "Untested" line. It should no longer imply that the setting-driven close is covered only
   at module level. Today, the Criteria sentence "a popover open when comments become hidden is
   removed" is checked only through a direct `visibilityChanged()` call.

4. **nit — fixed waits in the visual check** (`test/visual/capture_comment_checks.py:380,389,393,397`).
   It uses `page.wait_for_timeout(150)` after each press and click. This copies the existing
   `check_comment_button_thread` pattern and the CSS toggle is synchronous, so the flake risk is
   low. A `page.wait_for_function` on `data-sphinx-preview-comments` would be stricter. Optional.

5. **nit — file size** (`src/page/modules/commentThreads.ts`, 787/800 lines). It is under the
   ratchet, but the next change to this module will have to split it. One option is to move
   `hidden`/`paintFocus`/`visibilityChanged` and the orphan box into a sibling module. Nothing to
   do in this CR; worth a backlog line.

6. **nit — the PR must name the approved requirement.** The generated links block of the
   approved StRS-MDOKFSTUDIO-REVIEW-012 changed, because the SwRS title changed. The
   requirements guideline asks the PR to list the approved requirements it touched, even for a
   generated block, so the owner can see it.

## Not findings (checked, fine)

- dblclick on a hidden highlight passes through, so edit mode opens the block editor. This is
  consistent with choice 1.
- Escape while hidden: no popover, so the handler returns and nothing else changes.
- A mark that has focus when the setting hides it loses its tabindex, and the browser moves the
  focus away. Acceptable.
- `runtimeHarness.ts` gains a `closest()` branch that matches the exact holder selector string.
  It is brittle, but this is the existing harness pattern.
- The `e2eGroups` count went from 410 to 412 with an extended explanation string, which matches
  the two new scenarios (v29, v30).
