# T29 review — round 2

Base: fed90bd · Reviewed diff: 6 files, +392/-26

## Gates
compile, unit, types, contracts: PASS (logs/T29r2-*.log). full: PASS 199 s, no assertion failure in
`logs/T29r2-full.log`; RI-T29 logs `html assignments for one edit: 1`. visual: PASS, 0 new failure
lines against the baseline. The round-1 "selected cell moved -22 px" failure (seen in
`logs/T29-dbg-full.log`), the missed clicks and the detached-element failures are gone. The only
per-scenario wait left is RI-T16's `measure()` wait.

## Done-when
- [x] `rg "webview\.html =" src/extension.ts` matches only inside `assignWebviewHtml`.
- [x] Unit tests for `previewStatus` (in-place update, invalid or foreign messages ignored, and the
  new test "T29: an in-place pending status keeps the anchored block's viewport top").
- [x] RI-T29 passes (delta 1). RI-T29b passes (reading position kept while scrolled).
- [ ] Must-not-change "Anchoring: no extra scroll on status updates": met when the page is scrolled,
  **not met at scrollY 0 while an inline editor is open** (finding 1).

## Round-1 findings
- Finding 1 (re-anchor): fixed for scrollY > 0. `applyPreviewStatus` calls `measure()`, then
  `applyAnchor()` synchronously; `applyAnchor` scrolls through `programmaticScroll`, so the scroll
  handler posts no `previewScroll`. At scrollY 0 it does not re-anchor, which leaves the problem in
  finding 1 below.
- Finding 2: `waitForRender` matches the fed90bd body exactly. I extracted both versions and
  diffed them: identical. `htmlAssignmentCount()` is kept.
- Finding 3: red excerpts are given for the unit test (250 → 273) and for RI-T29b
  (`logs/T29-impl2-red5-trusted.log`, 23.8 → 46.2 px, banner 22.4 px). Both tests were run against
  the round-1 tree. Accepted.
- Finding 5: formatted. The settle loop is extracted to `waitForRenderChurnToSettle`.

## Protected features checked
- P-L5 / P-N1: first-render, failure, missing-source and ready paths still go through
  `setStatus` and `assignWebviewHtml` with unchanged strings. The `extension.ts` diff is unchanged
  since round 1.
- P-S2: `previewStatus` carries the current stage identifiers. The runtime gates on `sameContext`.
- P-S4: label and message are written with `textContent` and capped at 500 characters.
- P-E8: no new control.
- Scroll anchoring (`docs/scroll-anchoring.md`): restored for scrolled pages (unit test and
  RI-T29b). Regressed for an open editor at the top of the page (finding 1).
- RI-T29b leak check: the anchor button sets `preview.configuration.scrollPreviewWithEditor` and
  the webview `vscode.setState`. Both belong to that preview panel. `withDocument` →
  `closeAllEditors()` disposes the side preview, so the setting cannot reach later scenarios. OK.

## Findings

1. [MAJOR] `src/webview/scrollSync.ts`:`applyPreviewStatus` — an open inline editor at scrollY 0
   jumps about 23 px down under the caret.
   - The function computes `scrolledAway = window.scrollY > 0` and skips `applyAnchor()` at the
     top. That also skips the `editAnchor` branch of `applyAnchor`, which is the mechanism that
     keeps an open block, table-cell or frontmatter editor at its viewport top (round 1 said to
     rely on it).
   - Concrete case: a document at the top, block editor open on paragraph 1, and a render becomes
     pending. Triggers include an arrow-key transfer that saves the block, a table cell save, or
     typing in the source. The banner enters the flow and the textarea moves 22–23 px down. On the
     next ready reload it moves back up.
   - Before T29 this case was a reload: the editor was either dropped or reopened through
     `pendingBlockNavigation`. In both cases, nothing moved under a live caret. Keeping the editor
     open is the improvement T29 brings, so the editor must also stay still.
   - The plain reading case is fine as it is: at the top with no editor, the content moves down by
     the banner height, as with the old pending reload, whose page showed the same in-flow banner
     at scrollY 0.

   Fix, in `applyPreviewStatus`:
   - replace `const scrolledAway = window.scrollY > 0;` with
     `const keepPosition = window.scrollY > 0 || Boolean(editAnchor?.element);`;
   - use `if (keepPosition) applyAnchor();`.

   Do not change `applyAnchor`.

   Unit test to add, in `test/webview/scrollSync.test.ts`: "T29: an in-place pending status keeps
   an open editor still at the top of the page".
   - Reuse the fake DOM of the existing T29 anchoring test.
   - Start with `scrollY` 0 and enough content that `maxScrollTop() >= 23`.
   - Open a block editor on the first mapped block, using the same helper the existing
     edit-anchor tests use. This sets `editAnchor`.
   - Record the editor element's `getBoundingClientRect().top`.
   - Grow the status element to 23 px and offset the blocks by 23.
   - Dispatch the pending `previewStatus` message, then flush the frames and timers.
   - Assert that the editor's viewport top is unchanged (±0.5), that `scrollY` is 23 (±0.5), and
     that no `previewScroll` was posted.
   - Keep a companion assertion, in this test or in a sibling test: with no editor and scrollY 0,
     `scrollY` stays 0.
   - Run it red on the current tree first and paste the excerpt.

   Expected fallout: the scroll suite's keyboard-navigation check
   `assert.equal(await keyboardFrame.evaluate(() => window.scrollY), 0)` in
   `test/integration/scroll-sync-suite.ts` saw 22 in the round-2 intermediate run, because it
   measured while the pending banner was visible. That is the pre-authorized class: a layout
   measurement during the in-place banner, with a delta equal to the banner height.
   - Before that assertion, add the same setup-only wait as RI-T16: the current frame's
     `[data-sphinx-preview-status]` is `success` and `getActivePreviewForTests()?.phase === "ready"`,
     with a 10 s timeout.
   - Do not change the assertion.
   - `scroll-sync-suite.ts` is not in the Allowed files. List it in the report with the 22 px
     evidence, and have the orchestrator confirm it before the gate.
   - Then run `PLAN/scripts/gate.sh T29-impl3 unit types contracts full visual`.

2. [MINOR] Round-1 finding 4(a) (a late `previewReady` with the same requestId) is still open. It
   belongs in `followups.md`, as the report says.

## Existing assertions changed
- RI-T16 `measure()` setup wait: OK (amended task, banner-height evidence, assertions and 2 px
  tolerance unchanged).
- `waitForRender`: restored, no change against fed90bd. OK.
- No other existing assertion was modified.

VERDICT: CHANGES REQUESTED
