# T33 implementation — round 1

STATUS: DONE

## Summary
The content-bound startup code of the webview runtime now lives in `initializeContent({ restore })`.
Startup calls it with `restore: true`, then posts `previewReady` as before. `installLinkNavigation`
returns `{ rescan }`, which `initializeContent` calls only when `restore` is false. The Mermaid
script renders through `renderDiagrams(...)` and listens for `studio:content-replaced`. The runtime
gets a `contentReplaced()` function that nothing calls yet (T34 does). No observable behaviour
changed: the gates for `unit trusted scroll reload visual` plus `types contracts` all pass.

## Files changed
- `src/webview/scrollSync.ts` — `initializeContent(options)`, `contentReplaced()`, `const linkNavigation = …`; the content-bound startup calls moved into the function.
- `src/webview/linkNavigation.ts` — returns `{ rescan() }`; `links` is replaced on rescan; each link is observed once (`WeakSet`).
- `src/webview/mermaidPreview.ts` — `renderDiagrams`, module id counter, `studio:content-replaced` listener.
- `test/webview/scrollSync.test.ts` — added the startup-trace test (appended at the end).
- `test/webview/linkNavigation.test.ts` — added 4 rescan tests.

## Startup call order (before / after)
Inventory check: I read the runtime end to end. The T43 overlay (`applyPendingOverlay`, body-level
element, listeners on `window`) and the T30 `applyPropertiesMarkup` add no startup code. What
`applyPropertiesMarkup` re-runs (`setFrontmatterEditCells`, `applyDescriptionVisibility`,
`refreshInsertPoints`, `measure`) is already covered by `applyEditMode`, `applyDescriptionVisibility`
and `measure` in `initializeContent`. `resumePendingFrontmatterEdit()` was missing from the task's
inventory; it is content-bound and is included.

Before:
1. applyPreviewThemeMode, applyAnchorMode, applyPairing
2. **applyEditMode(editMode), initializeCheckboxes()**
3. toolbar button listeners, conditional `postAnchorModeChanged()`
4. applyTheme
5. **updateStickyHeadings()**
6. window listeners (scroll, resize, visualViewport, message)
7. **applyDescriptionVisibility()**
8. document listeners (click x5, mouseover, mouseout, focusin, focusout, dblclick, keydown)
9. **img load/decode listeners**
10. ResizeObserver on `main`
11. **markWideTables(), measure(), restoreState(), resumePendingBlockNavigation() if rendered, resumePendingFrontmatterEdit()**
12. post `previewReady`
13. **details toggle listeners**

After:
1. applyPreviewThemeMode, applyAnchorMode, applyPairing
2. toolbar button listeners, conditional `postAnchorModeChanged()`
3. applyTheme
4. window listeners
5. document listeners
6. ResizeObserver on `main`
7. `initializeContent({ restore: true })` = **applyEditMode, initializeCheckboxes, updateStickyHeadings, applyDescriptionVisibility, img listeners, markWideTables, measure, restoreState, resumePendingBlockNavigation if rendered, resumePendingFrontmatterEdit, details toggle listeners**
8. post `previewReady`

The bold content-bound calls run in exactly the same relative order. The lists are not literally
identical in one respect, which the task could not avoid with a single function: the non-content
items (listener registration, `applyTheme`) now run before the content calls instead of between
them. This is not observable: no event can fire synchronously during startup, and `applyTheme` only
sets two root attributes that nothing in `initializeContent` reads before `updateStickyHeadings`
(which ran after `applyTheme` before and still does). The order of document listeners is
unchanged, so every `stopImmediatePropagation` precedence holds. The only moves of a registration
relative to a content call: the details `toggle` listener now registers before `previewReady`
instead of after; its callback only persists state and fires asynchronously.

## Tests written first
- `T33: the startup sequence of effects and messages is stable` — written and frozen against the
  pre-refactor code (PASS there). It records, for 7 scenarios (reading mode, edit mode, untrusted
  workspace, saved anchor mode differing, pinned position, pending block navigation, pending new
  field), every `setAttribute/removeAttribute/addEventListener/appendChild/insertBefore/
  insertAdjacentElement/insertAdjacentHTML/remove/focus` call on the fake elements in order, the
  posted message types in order, and the final `scrollY`. It leaves out two things that the
  refactor moves and that are content-independent: `addEventListener` on the four toolbar buttons
  and the two `applyTheme` root attributes. After the refactor it passes without edits. A
  mutation check (moving `applyDescriptionVisibility` after `markWideTables`) made it fail, then I
  restored the code.

## Tests added or changed
- `T33: installing returns a rescan and the startup scan observes each link once` — `rescan` exists; startup observes each link once.
- `T33: rescan observes only the links that are not observed yet` — a new link is observed; a second rescan observes nothing.
- `T33: after a rescan, discovery and target hints apply to the new links` — new links trigger `previewLinkDiscover`; a `previewLinkTargets` message then sets their state and title.
- `T33: a context mutated after install is honoured by posts and by the hint check` — the `context` object is read at call time.

## Existing assertions changed
- None.

## Verification
- `gate.sh T33-impl types unit contracts` → PASS (logs/T33-impl-types.log, T33-impl-unit.log: 624/624, T33-impl-contracts.log: 2/2)
- `gate.sh T33-impl trusted` → PASS, first run (logs/T33-impl-trusted.log)
- `gate.sh T33-impl scroll` → PASS (logs/T33-impl-scroll.log)
- `gate.sh T33-impl reload` → PASS (logs/T33-impl-reload.log)
- `gate.sh T33-impl visual` → PASS vs baseline, 0 new failure lines (logs/T33-impl-visual.log; screenshots in logs/visual-T33-impl; tracked folder restored)
- Screen was unlocked before every long gate. No background process of mine is left.

## Open points / STOP reason
For T34, not defects of this task:
- `restore: false` skips `restoreState()` and does not call `applyAnchor()`; T34 must anchor after replacing the content (as `applyPropertiesMarkup` does with `measure(); applyAnchor();`).
- `initializeContent` calls `applyEditMode(editMode)`, which rebuilds the insert points. `applyPropertiesMarkup` skips that while a block editor is open (`!activeBlockEdit`); T34 must not call `initializeContent` while an editor is open, or add that guard.
- `rescan()` keeps the `discovered` request set. A new link whose request string was already discovered gets no new `previewLinkDiscover`, so it has no state/title until the host answers again. Clearing `discovered` was not in the task, so I left it.
- `closeLinkTooltip()` and the pending overlay (body-level `aside`) are not part of `initializeContent`; T34 handles them as `applyPropertiesMarkup` already does for the tooltip.
- Mermaid: the `studio:content-replaced` listener is registered at module load, and it waits for the Mermaid import, so an event during loading is served afterwards. In-flight diagrams are tracked in a `WeakSet`, so they are not rendered twice. The initial render has one extra microtask delay compared with before (Mermaid was rendered in the same job as `initialize`).
- Mermaid and `contentReplaced()` have no unit test (module-level script; nothing calls the function yet). The `trusted` and `visual` gates, which include Mermaid fixtures, pass.
