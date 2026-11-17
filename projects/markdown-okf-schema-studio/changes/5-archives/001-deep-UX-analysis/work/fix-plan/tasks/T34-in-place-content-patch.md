# T34 — In-place content patch, behind a setting

| Field | Value |
| --- | --- |
| Fixes | [UX-28](../../06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md) (step 3 of 3, "Done when") |
| Decisions | D-10 |
| Depends on | T33 |
| Gate | `unit contracts full visual` |
| Risk | **High.** Touches every render. Shipped behind a kill switch; review with extra care. |
| Commit message | `perf(vscode): patch preview content in place instead of reloading the webview` |

## Goal

Typing in the source no longer navigates the webview frame. A ready render whose page "shell" is
unchanged replaces only the content of `#sphinx-myst-preview-content` inside the existing
document.

Anything unusual falls back to today's full document assignment:

- a different shell;
- a webview that is not ready;
- the first render;
- the setting turned off;
- no acknowledgement within 2 s.

The new setting is `markdownOkfSchemaStudio.preview.incrementalUpdates` (boolean). Its default
follows D-10: `true` if this task passes every gate and the review, otherwise `false` with a note
in `followups.md`.

## Design

### Pure helpers: `src/preview/contentPatch.ts` (new)

- `extractMainContent(html): { start: number; end: number; inner: string } | undefined` returns
  the inner HTML of `<main id="sphinx-myst-preview-content" …>`. Locate it with parse5 source
  locations, as `replacePropertiesTableMarkup` does; never with a regex.
- `shellKey(html): string | undefined` returns the html with:
  - the main inner HTML removed;
  - every `nonce="…"` value and the CSP `nonce-…` tokens replaced by a constant;
  - the content of the `<script … data-sphinx-preview-scroll-sync>` element removed;
  - the `<aside data-sphinx-preview-status…>…</aside>` removed.

  Two renders of the same document type, with the same features (Mermaid or not, math stylesheet,
  toolbar), give equal keys.
- `canPatch(previousHtml, nextHtml): boolean`: both keys are defined and equal, **and** the next
  main inner HTML contains no `nonce=` and no `<script`.

### Host (`src/extension.ts`)

1. **Configuration.**
   - Add `incrementalUpdates: boolean` to `PreviewConfiguration` and `readPreviewConfiguration`
     (`src/configuration/previewConfiguration.ts`).
   - Add the setting to `package.json` under `contributes.configuration`, with the description:
     "Update the preview content in place while typing instead of reloading the page. Turn off if
     the preview misbehaves."
2. **`updatePreview(preview, result)`**, after computing the new `html`, patch when **all** of
   these hold:
   - `preview.configuration.incrementalUpdates`;
   - a previous stage exists, with `preview.readyRequestId === previousStage.requestId`;
   - `canPatch(preview.webview.html, html)`;
   - the `localResourceRoots` are unchanged (same list of `fsPath`s).

   **When patching:**
   - post `previewContentPatch` with:
     - `documentId` and the **previous** `documentVersion`/`requestId`, so the webview matches
       them with `sameContext`;
     - `next: { documentVersion, requestId, initialAnchor, initialPin }`, with `initialPin` from
       T32;
     - `contentHtml` (the new main inner HTML);
     - `status`, `label`, and `diagnostics` (an array of plain strings for the status list);
   - then set `preview.stage`, `preview.webview` (the full new `html`, its diagnostics and nonce),
     `preview.status` and the panel title, as the full path does, **without** assigning the
     webview html;
   - start a 2 s timer: if `preview.readyRequestId !== result.stage.requestId` when it fires and
     the stage is still current, fall back to `assignWebviewHtml(preview, preview.webview.html)`;
   - call `scheduleDeferredPreviewWork(preview, result)` as before.

   **Otherwise:** today's path.
3. **PlantUML injection** in `scheduleDeferredPreviewWork`: when the webview is ready for this
   stage and `incrementalUpdates` is on, post `previewContentPatch` with the **current**
   identifiers as both old and new, and the injected main content, instead of `setPanelHtml`.
4. Keep `preview.webview.html` equal to the full document a reload would show. Tests depend on it.

### Runtime (`src/webview/scrollSync.ts`)

Handler for `previewContentPatch`, active only when `sameContext(message)`:

1. Close editors without cancelling: `closeFrontmatterEditor()`, then `closeBlockEdit(false)`.
2. Call `closeLinkTooltip()`.
3. Replace the content: set `main.innerHTML = message.contentHtml`. The host builds it with the
   same sanitizer as a full render.
4. Mutate `context`: set `documentVersion`, `requestId`, `initialAnchor` and `initialPin` from
   `message.next`. Delete `initialState`, which is only for the first load. Update the
   `data-sphinx-preview-document-version` and `-request-id` attributes on
   `document.documentElement`.
5. Update the status region with the T29 helper. Rebuild the diagnostics list with
   `textContent`.
6. Call `initializeContent({ restore: true })` (T33). `restoreState` uses the new
   `initialPin`/`initialAnchor`.
7. Call `contentReplaced()` so Mermaid renders the new diagrams.
8. Post `previewReady` exactly as at startup, with the new identifiers.

Validate the message shape: all fields typed, `contentHtml` a string under 20 MB. Ignore it
otherwise.

## Allowed files

- `src/preview/contentPatch.ts` (new)
- `src/extension.ts`
- `src/configuration/previewConfiguration.ts`
- `src/webview/scrollSync.ts`
- `package.json` (one configuration property)
- `test/webview/contentPatch.test.ts` (new). `test/webview/` is already in the `test:unit` glob;
  do not change the npm scripts.
- `test/configuration/previewConfiguration.test.ts`
- `test/security/package-contract.test.ts` (configuration keys list)
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T34)
- `README.md` (document the setting)

## Tests

1. **`contentPatch` unit tests:**
   - extraction on a real `buildPreviewWebviewHtml` output;
   - equal keys for two renders of the same document with different text and nonces;
   - different keys when Mermaid appears or disappears;
   - `canPatch` refuses content containing a `<script`.
2. **Runtime unit tests:**
   - the patch replaces the content, updates the identifiers and attributes, and posts
     `previewReady` with the new identifiers;
   - an open block editor is closed **without** `previewEditCancel`;
   - a patch with stale identifiers is ignored.
3. **Real-input E2E**, scenario **RI-T34**:
   - Side preview ready. Record `htmlAssignments` as `A0` and the current Playwright `Frame`.
   - Type 20 characters in the source with a 60 ms delay; wait for ready plus 600 ms.
   - Assert `htmlAssignments === A0`; the **same** `Frame` object is still attached and shows the
     typed text; its `data-sphinx-preview-request-id` equals the host's `requestId`.
   - Then turn the setting off (workspace configuration), type 3 characters, and assert
     `htmlAssignments > A0`. Restore the setting.
   - Also run once with a Mermaid fixture: after typing, the diagram is rendered (an image element
     exists) in the same frame.
4. Run the **full** integration campaign and the visual campaign. Every existing scenario must
   pass unchanged: checkbox toggles, scroll campaign, reload, frontmatter editing, insertion.

## Expected changes to existing tests

- `package-contract.test.ts`: add `markdownOkfSchemaStudio.preview.incrementalUpdates` to the
  expected keys list. Nothing else.
- `previewConfiguration.test.ts`: the default value of the new key.

## Must not change

- Every protected feature. In particular P-N1 anchoring after renders, P-E4 pending navigation,
  P-R3 Mermaid, P-R2 math, P-R5 checkboxes (their listeners are delegated; verify), and P-S1 (no
  `<script` ever enters through the patch).

## Done when

- `unit`, `contracts`, `full` and `visual` pass; RI-T34 passes.
- The report states the default chosen for the setting under D-10, and why.

## Amendment (2026-10-14, after T43, T30 and T33)

T29 was replaced by T43 (D-22). Read every "T29" reference above as follows:

- **`assignWebviewHtml`, `readyRequestId`, `htmlAssignments`**: they exist (T43) with the same
  meaning. The patch path must not call `assignWebviewHtml` and must not change
  `htmlAssignments`; the fallback timer does call it.
- **Runtime step 5, "the T29 helper"**: there is none. The status region of a rendered page is
  `<aside data-sphinx-preview-status="<status>" role="status" aria-live="polite"><strong>label</strong>`
  `[<span data-sphinx-preview-status-message>message</span>][<ul data-sphinx-preview-diagnostics>`
  `<li data-sphinx-preview-diagnostic-severity="…">text</li>…</ul>]</aside>`, built by
  `statusMarkup` in `src/preview/webview.ts`.
  - The host sends `status`, `label`, `message` (optional string) and `diagnostics` as
    `{ severity, text }[]`, where `text` is the already-formatted location plus message.
  - The runtime rebuilds the same structure with `createElement`, `setAttribute` and
    `textContent`. It replaces the existing aside, or inserts it as the first child of `body`.
    It never uses `innerHTML` for these fields.
  - `hasRenderedPreview()` reads this attribute, so it must reflect the new status.
- **T43 pending overlay**:
  - On the patch path the host calls `endPendingOverlay(preview)` (or `clearPendingOverlay`
    followed by a hide message), exactly as the full ready path does.
  - The runtime hides `[data-sphinx-preview-pending-overlay]` when it applies a patch.
- **T30 properties table**: the patched content already contains the new properties section.
  The runtime drops any `deferredPropertiesMarkup` when it applies a content patch, because
  step 1 closes the frontmatter editor first.
- **T33**: use `initializeContent({ restore: true })` and `contentReplaced()` as T33 shipped them.
  If T33's report changed a name, follow the code.
- **D-10 default**: as written. The default is `true` only if every gate and the review pass;
  otherwise `false`, with a follow-up.
- **No installs of any kind** (no network). Allowed files are unchanged, plus
  `src/preview/webview.ts` if a small export is needed: for example, exporting the diagnostic
  text formatting so the host and the markup share it.
- **T33 hand-offs** (see `reports/T33-implementation-r1.md`):
  - `initializeContent({ restore: false })` skips `restoreState()` and does not re-anchor. T34
    uses `restore: true`, as written.
  - `initializeContent` rebuilds the insert points. `applyPropertiesMarkup` avoids that while a
    block editor is open. T34 closes the block editor first (runtime step 1), so this is safe.
    Keep that order.
  - `linkNavigation.rescan()` keeps link requests it has already discovered. After a patch, links
    that are new in the content must still get their link-target discovery. Check this with a
    unit test: a patched link whose target was not known before gets its
    `previewLinkTargets` / enrichment.
