# T34 implementation — round 3

STATUS: DONE

## Summary
Fast typing on a large document no longer assigns the webview document. Two causes were found and fixed:
(1) a render that finished before the page acknowledged the previous patch fell back to a full assignment;
(2) under a backlog, the 2 s acknowledgement fallback fired although the page was still working through the
chain. The host now addresses a patch to the stage the page *will* have once it handled the messages already
sent, and treats the acknowledgements of earlier patches of the chain as proof of life.

## Feedback addressed
1. **Chained patches (coordinator points 1, 2).** `ActivePreview.patchedRequestId`: set to `next.requestId`
   in `postContentPatch`, cleared in `assignWebviewHtml` when a new document is assigned (every load of a new
   document goes through it). New `pageHasStage(preview, stage)` = `readyRequestId === stage.requestId ||
   patchedRequestId === stage.requestId`; `updatePreview` uses it instead of the plain `readyRequestId` check.
   Every other patch condition is unchanged.
   **Runtime check:** `applyContentPatch` in `scrollSync.ts` is fully synchronous (no await, timer or
   `requestAnimationFrame` before `context.documentVersion/requestId` are set; `sameContext` of the next message
   is evaluated when that message is handled, and webview messages are handled in order). Unit test
   `T34: patches sent before the page acknowledged the previous one apply in order` (three chained patches,
   ready reports 12, 13, 14).
2. **Fallback still protects the chain (point 3).** The timer is re-armed for the newest stage on every patch, as
   before. Unit test `T34: when a patch of a chain is rejected, the later ones are ignored and nothing is
   acknowledged`: a rejected first patch leaves the page untouched, the orphaned second patch is ignored and no
   `previewReady` is posted, so the newest stage never acknowledges and the host's fallback loads the full
   document (with a fresh nonce, from round 2). The host side is covered by reasoning plus the integration run.
3. **Fallback liveness (found while testing, needed for point 3 to hold under load).** A diagnostic run showed
   `FALLBACK fired stage=34 ready=2`: the page lagged behind a 32-patch chain by more than 2 s after the last
   patch, so the timer reloaded the page. A `previewReady` of an earlier stage of the same document, while the
   fallback timer is armed, now re-arms the timer for the newest stage (`handlePreviewSyncMessage`, before
   `matchesCurrentPreview`; such a report was dropped as stale before). A rejected chain still produces no
   report, so it still ends in the fallback after 2 s.
4. **Overlay (point 4).** `armPendingOverlay` uses `pageHasStage`, so the overlay of a render pending over a
   chained, not yet acknowledged page is posted (in order, after the patch) instead of waiting as
   `pendingOverlayDue`. Patches still clear the overlay on the host and hide it in the runtime. The
   `previewReady` branch (`pendingOverlayDue`, re-arm) is unchanged. RI-T34's slow-render part and RI-T43 pass.

## Files changed
- `src/extension.ts` — `patchedRequestId`, `pageHasStage`, stale-ready re-arm, overlay condition.
- `test/webview/scrollSync.test.ts` — two chain tests.
- `test/integration/realInput.test.ts` — new scenario `scenarioLargeDocumentPatched` (RI-T34 large); RI-T34 itself untouched.

## Tests written first (failing before the fix)
- New real-input scenario on a generated 70 KB chapter (70 sections: heading, two paragraphs, a table, a list; created by the scenario in the RI fixture folder, no committed fixture). Caret at the end of the body, 32 characters at 60 ms, wait for ready plus 600 ms; asserts `htmlAssignments === A0`, `contentPatches` grew, the page marker survives, the typed text and request id are in the page.
- **Red:** on this machine the unthrottled run does not reproduce (`0 html assignments, 32 content patches` at 8d1ee21's logic, `logs/T34-r3-red-trusted.log` first green run). The scenario therefore slows the webview CPU with CDP `Emulation.setCPUThrottlingRate` (rate 6, applied to the webview frame's session) during the burst, which simulates a page slower than the render. At 8d1ee21's logic: `RI-T34 large document typing: 31 html assignments, 1 content patches` then `AssertionError: typing in a large document does not assign the webview document` (`logs/T34-r3-red-trusted.log`).
- With only the chained-stage condition (point 1/2), the scenario still failed in 2 of 3 runs with 1 assignment (the 2 s fallback, see item 3; `logs/T34-impl3-prefix-full-fail.log`). With item 3, 3 of 3 trusted runs and both `full` runs passed.

## Tests added or changed
- Two runtime chain tests (above) and the large-document RI scenario. No existing test or assertion changed.

## Existing assertions changed
- None.

## Verification
- `gate.sh T34-impl3 unit types contracts` → PASS (`logs/T34-impl3-unit.log`, `-types.log`, `-contracts.log`; 654 unit tests)
- `gate.sh T34-impl3 full` → PASS twice, 266 s each (the second run's log is `logs/T34-impl3-full.log`: `RI-T34 typing: 0 html assignments, 20 content patches`, `RI-T34 large document typing: 0 html assignments, 32 content patches`). Three additional `trusted` runs with the final code also passed (`logs/T34-dbg-trusted.log`, last run).
- `gate.sh T34-impl3 visual` → PASS vs baseline, 0 new failure lines (`logs/T34-impl3-visual.log`).
- Known flake seen: the "Timed out waiting for the editor matching [data-sphinx-preview-block-editor] textarea" failure in `trusted` runs of this round (several times while my diagnostic logging was in the host, once before it); each was followed by a clean rerun. Logs `logs/T34-r3-red-trusted-flake.log`, `T34-dbg-*`. Temporary debug logging was removed (no `t34-debug` left in the source).
- Screen unlocked before every long gate. No gate or test process of mine is left running.

## Evidence for reviewers
- `logs/T34-r3-red-trusted.log` (red, 31 assignments), `logs/T34-impl3-prefix-full-fail.log` (1 assignment from the fallback), `logs/T34-impl3-full.log` (green).

## Open points / STOP reason
- The CPU throttle (rate 6) is a stand-in for the slow page of the coordinator's replay; the real replay on `02-foundations.md` should be rerun on the orchestrator side.
- `patchPropertiesTable` (frontmatter refresh / link enrichment) and the PlantUML in-place patch still require `readyRequestId === stage.requestId`; if the page is behind a chain at that moment they fall back to a full assignment. They fire after typing pauses (debounced), so they were not seen in the large-document run. Not changed (out of the requested scope).
- MINOR 3 from round 1 (PlantUML patch fallback timer) is still a follow-up.
