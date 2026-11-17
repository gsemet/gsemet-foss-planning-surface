# T23 — Field actions sit inside the editing row; tooltips stay visible

| Field | Value |
| --- | --- |
| Fixes | [UX-20](../../03-frontmatter-editing/UX-20-row-menu-overlaps-and-clipped-tooltips.md) |
| Decisions | D-23 |
| Depends on | T03, T22 |
| Gate | `unit trusted visual` |
| Risk | Medium (P-E7 add/remove flows and blur-save logic depend on the menu) |
| Commit message | `fix(vscode): keep frontmatter field actions inside the edited row` |

## Goal

- The ⊞/⊟ actions and the add-field picker render **inside the editing cell, in normal flow**,
  after the editor control. They never cover another row's value.
- The buttons show short text labels: `Add field`, `Remove field`, and `Add` for the picker's
  confirm button. The clipped CSS pseudo-tooltips are disabled for this menu; native `title`
  tooltips remain.
- One-line text values open a one-row textarea that grows with its content.

## Context to read first

- `src/webview/scrollSync.ts`:
  - `createFrontmatterMenu(edit, anchor, properties)`, which appends to `document.body` and is
    positioned by `positionMenu` plus scroll/resize listeners;
  - `closeFrontmatterEditor`, which removes the menu and listeners;
  - `openFrontmatterEditor` and `openFrontmatterKeyEditor`, which call `createFrontmatterMenu`;
  - the blur and focusout guards that ignore targets inside `[data-okf-frontmatter-menu]`;
  - `resizeTextarea` and `control.rows`.
- `src/preview/previewStyles.ts`:
  - `.sphinx-preview-frontmatter-menu`, its buttons, `.sphinx-preview-frontmatter-picker`;
  - the shared tooltip rules (`[data-tooltip]::after`, around the `.sphinx-preview-frontmatter-menu button[data-tooltip]` selectors);
  - `[data-okf-frontmatter-editor] > textarea`.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/preview/previewStyles.ts`
- `test/webview/scrollSync.test.ts`
- `test/webview/previewStyles.test.ts`
- `test/visual/scenarios.ts` (`machineChecks` on frontmatter-editing scenarios)
- `test/visual/capture.py` (only checks about the old floating menu placement)
- `test/integration/realInput.test.ts` (add RI-T23)

## Steps

1. Write the tests first and record the failures.
2. `createFrontmatterMenu`:
   - append `menu` to `edit.editor` (after the control and the status), not to `document.body`;
   - delete `positionMenu`, its listeners, and the CSS custom-property writes. Keep
     `edit.frontmatterMenu`; set `edit.frontmatterMenuPositionListener` to `undefined`;
   - keep every attribute and every `data-okf-frontmatter-operation`;
   - remove the `edit.frontmatterMenuPositionListener?.()` calls, or keep them harmless.
3. Buttons: append `span.sphinx-preview-frontmatter-menu-label` with text `Add field`,
   `Remove field`, or `Add` (confirm). Keep `aria-label`, `title` and `data-tooltip`.
4. CSS:
   - `.sphinx-preview-frontmatter-menu`: `position: static; display: flex; flex-wrap: wrap; width: auto; max-width: 100%; margin: 4px 0 0;`.
     Remove `top`/`left` and the fixed `z-index`.
   - Buttons: `width: auto; padding: 0 8px; gap: 4px; display: inline-flex; align-items: center; border-radius: 14px;`.
   - Picker controls: `min-width: 0; max-width: 100%`.
   - Disable the pseudo-tooltip for this menu:
     `.sphinx-preview-frontmatter-menu button[data-tooltip]::after { content: none; }`.
     Delete the frontmatter-menu selectors from the shared tooltip rules if that is simpler.
5. Text fields: set `control.rows = 1` for the text-field textarea. Make sure the CSS min-height
   for `[data-okf-frontmatter-editor] > textarea` is at most about one line (for example
   `min-height: 1.6em`). `resizeTextarea` already grows it.
6. `scenarios.ts`: add `machineChecks: ["overlay-covers-text", "overlay-clipped"]` to the
   frontmatter-editing scenarios (search for `editTarget` values that open frontmatter editors).

## Tests

**Unit:**

- After opening a value editor, `menu.parentElement === edit.editor` and the menu is not in
  `body`.
- The key editor: the same.
- The labels exist.
- The blur of the control with `relatedTarget` inside the menu still does not save.
- Add and remove still post the same messages (existing tests).

**`previewStyles.test.ts`:** the new static menu rule and `content: none` for its tooltips.

**Real-input E2E**, scenario **RI-T23**:

- Call `page.setViewportSize({ width: 1100, height: 900 })` with the sidebar and the auxiliary bar
  closed. The editor and the side preview split the width, so the preview frame is about 540 px
  wide.
- Read the frame width from `(await frame.frameElement()).boundingBox()`, record it in the note,
  and assert it is between 480 and 620 px.
- Open the `scope` value editor in the middle of an F1-like requirement → capture with
  `required: ["overlay-covers-text", "overlay-clipped"]`.
- Click **Add field**, then capture again with the same required checks.

## Expected changes to existing tests

- `scrollSync.test.ts` → "frontmatter floating bar follows the active field and stays within the
  viewport". It asserts the floating placement (`--sphinx-preview-frontmatter-menu-*`,
  `data-placement`). Replace it with assertions that the menu is inside the editor and that no
  position properties are set. Keep the test name meaningful: rename it to "frontmatter field
  actions render inside the edited row".
- `previewStyles.test.ts` assertions on `position: fixed` for the frontmatter menu.
- `capture.py` checks of the floating menu position.

List each change.

## Must not change

- Add, remove and rename behaviour and messages (T24/T25 change the add flow, not this task).
- The table toolbar (T18).
- Link tooltips (`.sphinx-preview-link-tooltip`).

## Done when

- The `unit`, `trusted` and `visual` gates pass, with the required machine checks green.
- The reviewer looked at the 540 px captures: nothing covers another row, and labels are readable.
