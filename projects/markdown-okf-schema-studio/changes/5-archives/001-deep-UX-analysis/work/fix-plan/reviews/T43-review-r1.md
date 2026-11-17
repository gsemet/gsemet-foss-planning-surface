# T43 review — round 1

Base: 50eab0f · Reviewed diff: 8 files, +435/-21 (src 4 files +227/-21; tests 4 files, additions only)

## Gates
- compile, unit, types, contracts: PASS (`T43-*.log`, `T43-impl2-*.log`).
- visual: PASS vs baseline, 0 new failures (`T43-visual.log`; pre-existing sticky-headings failures are baseline).
- full / scroll: orchestrator's first `T43-full.log` failed (solo-block-anchored "no scroll feedback"),
  scroll x3 gave PASS/FAIL/FAIL. Implementer r2: `T43-impl2-scroll{1,2,3}` PASS x3 and `T43-impl2-full.log` PASS;
  18 instrumented runs show the failures happened before `activate()` or under load average 32, with
  no T43 code path executed (one request per preview, no overlay, no mid-test assignment).
  `T43-scroll4-scroll.log` was still running when read (all scenarios so far PASS); `T43r2-full` not yet present.
  The checklist rule (two clean reruns) is satisfied by r2's evidence; the orchestrator should
  confirm with scroll4/5 + T43r2-full. If any of those fail **with ACTIVATE/RESOLVE reached**, reopen.
- Code reading supports "not caused by T43": `assignWebviewHtml` always performs the real
  assignment (only the counter/overlay bookkeeping depends on `changed`), so no render is ever
  skipped; the scroll suite does not keep a render pending > 1.5 s; the only behavioural change on
  an edit is that the intermediate pending page is no longer assigned, which removes a reload
  rather than adding one.

## Done-when
- [x] Pending over a rendered page assigns nothing — `handleQueueState` branch `if (preview.stage)`; RI-T43 "pending must not assign the webview html", logged "assignments 0, paragraph shift 0 px".
- [x] One assignment per edit — RI-T43 "one html assignment for a fast edit" (red: `3 !== 1` in `T43-red-trusted.log`) and "one html assignment for the slow edit".
- [x] Overlay after 1.5 s, same frame, no movement, below toolbar, two lines — RI-T43 asserts + screenshot.
- [x] Overlay gone after ready — RI-T43 "the overlay is gone".
- [x] First render / stale / error / missing-source unchanged — `setStatus` still used when `stage` is undefined; failed branch calls `setStatus("stale"|"error")` (assigns page as before); `setMissingSource`, `showPending(clearContent)` unchanged apart from the funnel.
- [x] `rg "webview\.html =" src/extension.ts` only in `assignWebviewHtml` (verified in diff: all 9 sites routed).
- [x] Host html equals shown page — `preview.webview.html` is not touched on pending; deferred PlantUML update uses `shownStatus ?? status` so it re-renders the status the page actually shows.

## Protected features checked
- P-L5 (render lifecycle): ready path unchanged except `endPendingOverlay` + funnel; failed path unchanged except `endPendingOverlay`. Covered by unit + full + RI-T43.
- P-N1 (scroll stability): pending no longer reloads, so no scroll change; RI-T43 paragraph-top within 1 px; scroll suite (see Gates).
- P-S2/P-S4 (message protocol / escaping): `previewPendingOverlay` is host→webview only, gated by `sameContext`, `visible` boolean and label/message strings ≤ 500 checked; texts set via `textContent`. Unit test "invalid or foreign pending overlay messages are ignored". `readyRequestId` is set only after `isPreviewSyncMessage` + `matchesCurrentPreview`.
- P-E8 (read-only): overlay is non-interactive (`pointer-events: none`), no edit path added.
- Accessibility: `role="status"`, `aria-live="polite"`.
- Frozen UX-22 / UX-24 / UX-34: untouched.
- Runtime template (conventions §2): no backtick or `${` added, no global setTimeout, DOM APIs only inside the runtime.

## Timer lifecycle (verified by reading)
- Cleared on changed assignment (`assignWebviewHtml` → `clearPendingOverlay`), on ready and failed (`endPendingOverlay`, posts `visible:false` if shown), on dispose (`disposePreview`), on document switch (`showPending(clearContent)` assigns a new status page; and the callback is also guarded by `preview.stage !== stage`).
- Callback is guarded by `disposed`, `status === "pending"`, unchanged stage and queue phase; if the page has not reported ready it sets `pendingOverlayDue`, posted on the next matching `previewReady`.
- Identical-string handling is correct: VS Code's `Webview.html` setter ignores an unchanged value, so not resetting `readyRequestId` there is right.

## Visual
Screenshot `43-pending-overlay.png`: overlay at top right directly below the floating toolbar,
"Preview pending" bold over "Rendering the active buffer.", readable in the dark theme, covers no
heading or paragraph text, no content shift. OK.

## Findings
1. [MINOR] `test/integration/realInput.test.ts`:`scenarioPendingOverlayWithoutReload` — render delay 6 s instead of the task's 3 s. Justified in the report (screenshot must fit between 1.5 s and ready). Accept.
2. [MINOR] `src/extension.ts`:`armPendingOverlay` — if `showPending(clearContent)` ever produced an identical string (same message twice), `clearPendingOverlay` would not run; harmless because the timer callback checks `preview.stage !== stage`. Optional follow-up: call `clearPendingOverlay(preview)` explicitly at the top of `showPending` when `clearContent` is true.
3. [NIT] README has no pending-banner description, so no doc update is required; a one-line note about the delayed overlay could be added later.

## Existing assertions changed
None (test diff contains additions only). OK.

VERDICT: PASS
