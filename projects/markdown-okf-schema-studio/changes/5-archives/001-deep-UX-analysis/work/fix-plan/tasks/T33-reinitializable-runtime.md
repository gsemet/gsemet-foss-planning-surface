# T33 — Refactor: make the content-dependent runtime re-initializable

| Field | Value |
| --- | --- |
| Fixes | [UX-28](../../06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md) (preparation for step 3) |
| Depends on | T32 |
| Gate | `unit trusted scroll reload visual` |
| Risk | Medium (pure refactor of startup code; **no behaviour change allowed**) |
| Commit message | `refactor(vscode): make preview content initialization repeatable` |

## Goal

Prepare T34, which replaces the content inside the existing document. Every part of the runtime
that binds to **content elements** at startup must become callable again on new content. The
startup order and behaviour must stay exactly as today. **The refactor must change no observable
behaviour.** Every existing test passes unchanged.

## Inventory (verify it by reading the runtime end to end)

Content-bound initialization in `createScrollSyncScript`, all near the end of the runtime:

| Item | Today |
| --- | --- |
| Checkboxes | `initializeCheckboxes()` |
| Edit mode | `applyEditMode(editMode)` → `setFrontmatterEditCells`, and T28 insertion points |
| Description column | `applyDescriptionVisibility()` |
| Image layout | `document.querySelectorAll("img").forEach(image => image.addEventListener("load", stabilizeLayout …))` |
| Details persistence | `document.querySelectorAll("details").forEach(element => element.addEventListener("toggle", …))` |
| Wide tables | `markWideTables()` (T19) |
| Measuring and anchoring | `measure()`, `restoreState()`, `updateStickyHeadings()`, `resumePendingBlockNavigation()`, the `previewReady` message |
| Link discovery | `installLinkNavigation(document, window, vscode, context)` captures `links` once (`linkNavigation.ts`) |
| Mermaid | `out/bundle/mermaidPreview.js` renders `.myst-mermaid-diagram` elements once, at load (`mermaidPreview.ts`) |

Listeners registered on `document` or `window` (delegated click, keydown, scroll, resize, message,
the ResizeObserver on `main`) are **not** content-bound. They stay registered once.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/webview/linkNavigation.ts`
- `src/webview/mermaidPreview.ts`
- `test/webview/scrollSync.test.ts`, `test/webview/linkNavigation.test.ts` (add tests only)

## Steps

1. **Runtime.** Extract
   `function initializeContent(options) { … }`, with `options: { restore: boolean }`:
   - it performs, in today's order, the content-bound items above, from checkboxes to
     `resumePendingBlockNavigation`;
   - **it does not post `previewReady`**; the caller does;
   - startup calls `initializeContent({ restore: true })`, then posts `previewReady` exactly as
     today.

   Keep the startup sequence identical: compare the order of calls before and after, and list it
   in the report.
2. **`linkNavigation.ts`.** Make `installLinkNavigation` return `{ rescan(): void }`.
   - `rescan` re-queries `a[data-sphinx-preview-navigation]`, observes the links not yet observed,
     and replaces the `links` array used by the `previewLinkTargets` handler.
   - The `context` object is read at call time (it already spreads `...context` when posting), so
     a later mutation of `context` is honoured.
   - Startup behaviour is unchanged. Store the return value in the runtime
     (`const linkNavigation = (…)(document, window, vscode, context);`) and call
     `linkNavigation.rescan()` from `initializeContent` **only when `options.restore === false`**.
     At startup, the install already scanned.
3. **`mermaidPreview.ts`.** Wrap the per-diagram rendering in `renderDiagrams(diagrams)`; call it
   at load as today. Add a listener `document.addEventListener("studio:content-replaced", …)` that
   renders `.myst-mermaid-diagram` elements without `data-render-state`. Give each `mermaid.render`
   call a unique id, using a module counter, not only the index.
4. Add a runtime function `contentReplaced()` that dispatches `studio:content-replaced` on
   `document`, guarded with `typeof CustomEvent === "function"`. Do not call it yet; T34 does.

## Tests

- **All existing tests pass unchanged.** This is the main criterion.
- `linkNavigation.test.ts`: `rescan()` observes newly added links, and a `previewLinkTargets`
  message then updates them.
- `scrollSync.test.ts`: the startup message sequence (types and order of the first messages
  posted) is identical to the pre-refactor sequence. Capture it in a test that you write **before**
  refactoring, against the current code.

## Expected changes to existing tests

None. If any existing test needs a change, the refactor changed behaviour: STOP.

## Must not change

- Anything observable. This includes the `reload`, `scroll` and `visual` gates: they must pass
  with no assertion edits.

## Done when

- All five gates pass. The report lists the startup call order, before and after, and they are
  identical.
