# T33 review — round 1

Base: a9d4545 · Reviewed diff: 5 files, +675/-24 (3 src, 2 test; tests are additions only)

## Gates
- types: PASS (logs/T33-types.log, logs/T33-impl-types.log)
- unit: PASS 624/624 (logs/T33-unit.log, logs/T33-impl-unit.log)
- contracts: PASS 2/2 (logs/T33-contracts.log)
- trusted / scroll / reload: PASS (logs/T33-impl-*.log)
- visual: PASS, 0 new failure lines vs baseline (logs/T33-impl-visual*.txt)
- full: still running at review time (logs/T33-full.log ends mid-run at "PASS scroll E2E:
  solo-reading-anchored"). The orchestrator must confirm it ends PASS before committing.
No new failure compared with the T00 baseline in any completed log.

## Done-when
- [x] `initializeContent({ restore })` holds the content-bound items in their previous relative
  order; it does not post `previewReady`; startup calls it with `restore: true` then posts
  `previewReady` with the same payload — evidence: diff of `scrollSync.ts`, test
  `T33: the startup sequence of effects and messages is stable`.
- [x] `installLinkNavigation` returns `{ rescan }`; `rescan` re-queries, observes only unobserved
  links (WeakSet), replaces `links`; `context` read at call time — evidence: 4 `T33:` tests in
  `linkNavigation.test.ts`. Startup path unchanged (`links.forEach(observe)` = previous
  `observer.observe` per link, each link once).
- [x] `mermaidPreview.ts`: `renderDiagrams`, module counter, `studio:content-replaced` listener.
  Startup ids are identical to before (counter increments for every diagram, including empty
  ones, exactly like `index`).
- [x] `contentReplaced()` added, guarded by `typeof CustomEvent === "function"`, not called.
- [x] Startup order listed before/after in the report; content-bound calls in identical relative
  order. The interleaving with non-content calls differs (analysed below).
- [x] No existing assertion changed.

## Deviation analysis (listeners and applyTheme now run before the content-bound calls)
All of startup is one synchronous task; no DOM event, ResizeObserver, IntersectionObserver,
`load`, `decode()` promise or `message` callback can be delivered during it. So a listener
registered earlier in the same task sees exactly the same events as before. Item by item:
- `applyEditMode(editMode)` / `initializeCheckboxes()` moved after the toolbar listeners, the
  conditional `postAnchorModeChanged()` and `applyTheme`. At startup `applyEditMode` posts nothing
  (no active block/frontmatter edit exists), and `postAnchorModeChanged` reads only
  `anchorToEditor` (set by `applyAnchorMode`, which still runs first). Message order unchanged.
  `aria-pressed`/disabled of the anchor button is set by `applyAnchorMode`/`applyPairing`, still
  first; edit button attributes are set only by `applyEditMode`; final DOM state identical.
- `applyTheme` sets two root attributes; `updateStickyHeadings` still runs after it, and
  `measure()` ran after it before as well. No content call reads them earlier than before.
- `applyDescriptionVisibility()` now runs after the document listeners: listener registration does
  not read DOM; it still runs after `updateStickyHeadings` and before `markWideTables`, as before.
- `restoreState()` / `window.scrollTo`: the scroll listener was already registered before it
  pre-refactor; unchanged. ResizeObserver on the content still registered before `measure()`.
- `resumePendingFrontmatterEdit()`: same position (after `resumePendingBlockNavigation`, before
  `previewReady`).
- `previewReady`: same payload, still after `measure`/`restoreState`/resume calls.
- details `toggle` listeners now registered before `previewReady` instead of after: same task,
  callback only persists state; not observable.
- Image listeners now go through a WeakSet: at startup each image is new, so identical.
Conclusion: no observable behaviour difference.

## Startup-trace test
It records, in 7 scenarios, all attribute/listener/DOM-mutation/focus calls on content fake
elements in order, the posted message types in order and final `scrollY`, and was frozen against
the base code. It deliberately ignores the toolbar-button `addEventListener` calls and the two
`applyTheme` root attributes (the only items whose position moves). A mutation check reported in
the implementation report shows it fails on a content-order swap. Adequate guard.

## Protected features checked
- P-E8 (read-only): `applyEditMode`/`initializeCheckboxes` unchanged and still called once at
  startup; trusted gate PASS.
- P-S2 (version checks): message handlers untouched.
- P-S4 (innerHTML escaping): no new innerHTML.
- Scroll anchoring / restore / pending block navigation: scroll and reload gates PASS, trace test.
- Link navigation (UX-22 frozen): resolution and messages untouched; startup observation identical.
- Mermaid rendering: startup ids identical; visual gate PASS.
- Webview template rules (conventions §2): no backticks or `${` added in the template, no global
  `setTimeout`, `CustomEvent` guarded.

## Findings
1. [MINOR] mermaidPreview.ts:`renderDiagrams` — on success, verify the code sets
   `data-render-state` (not only on error); otherwise the `studio:content-replaced` filter
   (`renderState === undefined`) would re-render already rendered diagrams in T34. No impact in
   T33 (event never dispatched). Fix in T34 if needed, with a test that dispatching the event twice
   renders each diagram once.
2. [NIT] scrollSync.ts:`initializeContent` — `restore: false` does not anchor; already noted as a
   T34 open point in the report.

## Existing assertions changed
None.

VERDICT: PASS
