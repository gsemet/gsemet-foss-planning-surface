# T32 — The edited block stays put after Save

| Field | Value |
| --- | --- |
| Fixes | [UX-11](../../01-inline-block-editing/UX-11-edited-element-drifts-after-save.md) |
| Depends on | T31 |
| Gate | `unit trusted scroll` |
| Risk | Medium (P-N1 rule R7) |
| Commit message | `fix(vscode): keep the edited block in place across the post-save render` |

## Goal

Rule R7 of `docs/scroll-anchoring.md` is enforced across the re-render that follows a commit: after
a block, table-cell or frontmatter save, the edited element's **viewport top** in the new render
is within 3 px of where it was when the user committed.

## Design

- **Webview.** On every **final** save, add two optional fields to the message: `pinLine` and
  `pinViewportTop`.
  - Final saves are: `postBlockEditSave(true)` with a message posted, the frontmatter
    `saveValue`, `postFrontmatterAction`, and the key save.
  - `pinLine`:
    - block or table edit: `edit.line`;
    - insertion (T28): `max(1, insertAfterLine + 1)`;
    - frontmatter: `1`, the properties section.
  - `pinViewportTop`: the current `getBoundingClientRect().top`
    - of `edit.renderedTarget || edit.target` for blocks. Measure the **rendered** element, which
      is hidden while editing; if its rect height is 0, use the editor element instead;
    - of the selected cell's table for table edits;
    - of `[data-okf-properties]` for frontmatter.
- **Host.** In `isPreviewSyncMessage`, accept `pinLine` (safe integer ≥ 1) and `pinViewportTop`
  (finite, |value| ≤ 100000) only on `previewEditSave` (when `final === true`) and
  `previewFrontmatterSave`.
  - When such a message is accepted, store
    `preview.pendingPin = { documentId, line, viewportTop, expiresAt: Date.now() + 5000 }`.
  - `scrollContext(...)` adds `initialPin: { line, viewportTop }` when a non-expired pin exists for
    the document. `updatePreview` clears the pin after using it once.
- **Runtime.** In `restoreState`, before the existing `initialAnchor` logic, when
  `context.initialPin` is set:
  1. choose the layout entry with `sourceLine === pin.line`, else the last entry with
     `sourceLine <= pin.line`;
  2. compute `target = clamp(entry.top - pin.viewportTop, 0, maxScrollTop())` and call
     `programmaticScroll(target)`;
  3. set `anchor = { line: lineAtScroll(target), owner: "preview" }`;
  4. skip the `initialAnchor` path.

  Later layout changes (images) keep this anchor through `applyAnchor`, as today.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/extension.ts`
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T32)
- `docs/scroll-anchoring.md` (R7: one sentence on how the pin crosses the re-render)

## Tests

**Unit:**

- A final block save carries `pinLine` and `pinViewportTop`; an autosave (`final: false`) does not.
- `restoreState` with an `initialPin` scrolls so that the entry's top equals `pin.viewportTop` in
  the viewport; it also clamps.

**Real-input E2E**, scenario **RI-T32**:

- **List case.** The UX-04 nested-list fixture, with 40 filler paragraphs above it so the list is
  mid-document; scroll it to the middle of the viewport.
  - Record the list's viewport top `T0`.
  - Click "Refrigerated goods", press `${MOD}+End`, `Enter`, type `Frozen goods`, press
    `${MOD}+Enter`.
  - After the re-render, the new list's top must be within 3 px of `T0`.
- **Table case.** The same check for a table cell committed with `Enter`.

Both must fail before the fix, or show more than 3 px of drift. Record the measured drift.

## Expected changes to existing tests

None.

## Must not change

- Anchoring when no save happened (the initial anchor path), and source-led scrolling (R4).
- The echo guard.

## Done when

- The `unit`, `trusted` and `scroll` gates pass; RI-T32 passes, with before/after drift in the
  report.
