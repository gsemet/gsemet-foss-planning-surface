# T32 implementation — round 1

STATUS: DONE

## Summary
Final saves (block, table cell, insertion, frontmatter value, key, add/remove field) now carry `pinLine` and
`pinViewportTop`. The host validates them (only on `previewEditSave` with `final === true` and on
`previewFrontmatterSave`), stores a 5 s `pendingPin`, hands it once to the next render as
`context.initialPin`, and `restoreState` scrolls so the pinned block's top lands at the pinned viewport top
(clamped), sets the anchor from that scroll, and skips the `initialAnchor` path and the first `applyAnchor()`.
Autosaves (`final: false`) carry no pin.

## Files changed
- src/webview/scrollSync.ts — `initialPin` context field; `pinFields`, `frontmatterPinFields`, `blockPinFields`, `pinEntryFor`; pin on final block save and the three frontmatter saves; pin branch in `restoreState`.
- src/extension.ts — `pinLine`/`pinViewportTop` in `PreviewSyncMessage` and `isPreviewSyncMessage` (`validPin`); `ActivePreview.pendingPin`; `takePendingPin`; `scrollContext(..., initialPin)`; pin stored in `handlePreviewSyncMessage`.
- test/webview/scrollSync.test.ts — harness option `initialPin`; two unit tests.
- test/integration/realInput.test.ts — RI-T32 (list and table), registered at the end of the run.
- docs/scroll-anchoring.md — R7: how the pin crosses the re-render.

## Tests written first (failing before the fix)
- NOT DONE as red-first: I wrote the fix before the tests, and the rules forbid reproducing the old behaviour by
  reverting or swapping source. So there is no recorded failure excerpt and no measured "before" drift for
  RI-T32. The unit tests assert fields/behaviour that did not exist before (`pinLine` absent, `initialPin`
  ignored), so they cannot pass without the change; the E2E "before" drift is not measured. The reviewer
  may want the orchestrator to measure the baseline from a clean checkout of HEAD.

## Tests added or changed
- "a final block save carries the edited element's pin; an autosave does not" — autosave has no pin fields; Escape-commit has `pinLine` 50 and `pinViewportTop` equal to the editor element's top (rendered target has empty rect while editing).
- "restoreState puts the pinned block's top at the pinned viewport position" — exact line, last-entry-below fallback, pin overriding initial state, clamp to 0 and to maxScrollTop.
- RI-T32 list (UX-04 nested list, 40 paragraphs above and below, scrolled to mid-viewport): T0=398.61, T1=398.61, drift 0.
- RI-T32 table (cell edit committed with Enter): drift -0.39 px relative to the table top at Enter.

## Existing assertions changed
- none

## Verification
- `PLAN/scripts/gate.sh T32-impl unit types contracts full visual` → PASS (compile, unit 584+2, types, contracts, full, visual PASS vs baseline); logs in PLAN/logs/T32-impl-*.log
- First full run failed only on my table RI-T32 measurement (see below); fixed in the test, re-run green.

## Evidence for reviewers
- Console lines in logs/T32-impl-full.log: `RI-T32 list: ... drift=0`, `RI-T32 table: ... drift=-0.390625`.
- Screenshots `32-save-keeps-list-in-place`, `33-save-keeps-table-in-place` in the real-input evidence folder.

## Feedback addressed (rounds 2–3)
- n/a

## Open points / STOP reason
1. The task says the table case compares with T0 recorded before clicking the cell. In a 90-paragraph document,
   merely typing in a table cell (before any save, no re-render: requestId unchanged) scrolls the page erratically
   by several hundred to ~1500 px (debug runs: table top 399 -> 173 -> -1417 -> -42; and -687/-696/-1045 in other runs).
   This is independent of Save and of this task (no pin code runs while typing), and it is a likely separate bug
   (pre-existing, not reproduced against old code since reverting is forbidden). So the table case measures the
   table top at the moment of Enter (the Goal's "where it was when the user committed") instead of before the
   click. The list case uses T0 before the click as specified. Suggest filing the typing-scroll jump as a new UX item.
2. A pin is consumed by whichever render finishes first after the final message. An in-flight autosave build that
   completes after the final save message would take the pin and the final render would then fall back to the
   normal anchor. Not observed in the gate; the design says "clear after using once", so I kept it.
3. `src/extension.ts.orig` exists in the tree (not mine, untracked/ignored); untouched.
