# T29 review — round 1

Base: fed90bd · Reviewed diff: 6 files, +273/-28

## Gates
unit, types, contracts: PASS (logs/T29-impl-*.log). full: PASS 228 s (189 s at the PHASE3
checkpoint; the extra time comes from the new settle waits in `waitForRender`). visual: PASS, 0 new
failure lines. The full gate passes only because `waitForRender` was broadened (finding 2). Without
that change, the report records ten consecutive failing runs in existing scenarios.

## Done-when
- [x] `rg "webview\.html =" src/extension.ts` matches only inside `assignWebviewHtml`.
- [x] unit gate passes; tests "T29: a previewStatus message updates the status region in place" and
  "T29: invalid or foreign previewStatus messages are ignored".
- [x] RI-T29 passes (logged delta 2, earlier run 1).
- [ ] Must-not-change "Anchoring: no extra scroll on status updates": not met. The visible content
  moves by the banner height (finding 1).
- [ ] trusted/scroll gates pass *without weakening existing tests*: not met (finding 2).

## Protected features checked
- P-L5 / P-N1 (render lifecycle, navigation): ready, failure, missing-source and first-render paths
  still go through `setStatus`/`assignWebviewHtml` with unchanged strings. The host `html` string is
  kept in sync through `setPreviewStatus`. OK.
- P-S2 (stale identifiers): `previewStatus` is posted with the current stage ids. The runtime checks
  `sameContext`. `previewReady` passes `matchesCurrentPreview` before `readyRequestId` is set. OK.
- P-S4 (escaping): label and message are written with `textContent` and limited to 500 characters. OK.
- Scroll anchoring (docs/scroll-anchoring.md, "the runtime owns anchoring"): REGRESSED. See finding 1.
- P-E8 (read-only mode): no new interactive control. OK.

## Findings

1. [BLOCKER] `src/webview/scrollSync.ts`:`applyPreviewStatus`: the reading position jumps by
   about 23 px each time a render starts. I confirmed this by reading the code:
   - `setPreviewStatus` (`src/preview/webview.ts`) inserts the `<aside data-sphinx-preview-status>`
     as the **first child of `<body>`**, above `#sphinx-myst-preview-content`.
   - `previewStyles.ts` hides only `[data-sphinx-preview-status="success"]`
     (`position:absolute; 1px`). `pending` is in flow, about 23 px according to the RI-T16 evidence
     (1005 vs 982).
   - `previewStyles.ts` sets `html, body { overflow-anchor: none; }`, so the browser does not
     compensate.
   - `applyPreviewStatus` changes the attribute and texts, then returns. It does not re-measure and
     does not re-anchor.
   - The `ResizeObserver(stabilizeLayout)` watches only `#sphinx-myst-preview-content`. The aside
     sits outside it, and the size of `main` does not change. So no observer fires.

   Result: `success` → `pending` pushes every block 23 px down while the reader is scrolled anywhere.
   The next ready render goes through a reload, which runs `restoreState()` → `applyAnchor()` with
   `initialAnchor`, so the content snaps back. That is a down-and-up jump on every keystroke burst.
   Before T29 the pending page was a reload, and `restoreState()` re-applied the anchor. There was a
   flash, but no shift. RI-T18's "selected cell moved -22 px" failure is the same defect seen by a
   test.

   Fix:
   - In `applyPreviewStatus`, after the DOM update, re-run the same path that image loads use:
     call `stabilizeLayout()`. It runs `measure()` + `applyAnchor()` + `updateStickyHeadings()` in
     the next animation frame.
   - Better still, to avoid a one-frame visible shift: record
     `const before = region.getBoundingClientRect().height` before the update. After the update,
     call `measure(); applyAnchor(); updateStickyHeadings();` synchronously. This re-anchors through
     `programmaticScroll`, so no `previewScroll` echo is posted.
   - When `editAnchor` is set (a cell edit is open), `applyAnchor` already keeps that element's
     viewport top. Do not add a separate path.
   - At scrollY 0 with no anchor, the content may move down. That matches the old reload, which
     also showed the banner at the top. Do not special-case it.
   - Do not change the banner CSS or markup (a follow-up covers that).

   Tests to add:
   - Unit, `test/webview/scrollSync.test.ts`: "T29: an in-place pending status keeps the anchored
     block's viewport top".
     - Build a harness with `previewStatus: "success"` and several mapped blocks.
     - Scroll to a middle block and flush the frames.
     - Record that block's `getBoundingClientRect().top`.
     - Make the fake status element's height grow from 0 to 23 when its attribute becomes
       `pending`, and offset the blocks' tops by that height (extend the fake DOM only as needed).
     - Dispatch the `previewStatus` pending message, then flush the frames and timers.
     - Assert that the block's viewport top is unchanged (±0.5) and that no `previewScroll` message
       was posted.
     - The test must fail on the current code. Paste the red run in the report.
   - Real input, `scenarioPendingWithoutReload` (RI-T29), or a new RI-T29b on a fixture longer than
     the viewport:
     - Scroll the side preview to the middle.
     - In the same frame, measure the `getBoundingClientRect().top` of the first block whose top is
       ≥ 0.
     - Set `setRenderDelayForTests(500)`, type one character, and wait for the same frame to show
       `pending`.
     - Let one animation frame pass, then measure the same block again. Assert |delta| ≤ 2 px.
     - Record the red run (it should show about 23 px).

2. [BLOCKER] `test/integration/realInput/harness.ts`:`waitForRender`: the change is a weakened
   synchronisation that hides finding 1. It now waits for `success` plus 600 ms without a new
   assignment, for **every** real-input scenario. So the suite no longer exercises clicks,
   measurements or edits while a follow-up render is pending. That is exactly where the user meets
   the jump. The amendment pre-authorized setup waits only per scenario, with banner-height evidence.
   It did not authorize a harness-wide quiescence wait.

   Next round:
   - Restore `waitForRender` to its fed90bd body exactly: same predicate, default timeout, no
     `quietSince`, no status check.
   - Keep `htmlAssignmentCount()`.
   - Once finding 1 is fixed, run the full gate. If an existing scenario still fails only from
     layout measured with the banner visible (for example RI-T16's `scrollHeight`, which changes by
     the banner height even when the anchor holds), keep a **per-scenario** setup wait as the
     amendment allows, and quote the evidence. RI-T16's `measure()` wait is acceptable on that
     basis: `scrollHeight` legitimately includes the banner.
   - Any failure of the "moved -22 px", missed-click or detached-element kind must disappear with
     the fix, not with a wait.
   - If RI-T29's own pre-edit settle loop is still needed, keep it local to RI-T29.

3. [MAJOR] No red-first evidence (checklist C9, interaction bug). I checked by reading the code
   that RI-T29 would fail on the old path: `setStatus` → `setPanelHtml` assigns a changed string,
   so `htmlAssignments` increments and the old frame is replaced. The "same frame reports pending"
   wait or the `atPending === before` assertion would fail. So the test is meaningful. Still, for
   findings 1 and 2 the next round must paste real red excerpts for the new unit test and the new
   real-input check, obtained by temporarily removing the re-anchor call.

4. [MINOR] Open points from the report:
   - (a) Late `previewReady`: `matchesCurrentPreview` filters out reports with older ids before
     `readyRequestId` is set. The remaining risk is a ready report from a replaced document that has
     the *same* requestId (an enrichment re-assign with changed html). The in-place message would
     then reach a document that is still loading. The host string stays correct, and the next load
     shows the right state. Acceptable; log it as a follow-up.
   - (b) A missing status element is ignored silently. Rendered pages always contain the aside
     (`setPreviewStatus` inserts it), so this is acceptable.
   - (c) Dropping non-security diagnostics when pending matches the old `setStatus("pending")`
     behaviour. Not a regression.

5. [NIT] `realInput.test.ts`:`scenarioPendingWithoutReload`: the `try {` / `await waitFor` block
   is not indented, and the `lastSeen` debug string is long. Format it.

## Existing assertions changed
- RI-T16 `measure()` setup wait: OK (amended task, 23 px evidence, assertions unchanged). Re-check it
  after finding 1.
- `waitForRender` settle wait: NOT JUSTIFIED. It is harness-wide, outside the per-scenario
  authorization, and it masks a product regression (finding 2).

VERDICT: CHANGES REQUESTED
