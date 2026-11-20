# Diagnosis r6: RI-T16 reopen step, "edit mode to still be on in the reopened preview"

## Verdict

**The test is wrong, not the product.** The reopen step added by this CR (commit 29fc05b8,
`test/integration/realInput/editorWidgets.ts` lines 833-838) expects a new preview to start in
edit mode. Since b84b0585 ("fix(render): always open a document in preview mode", 2026-11-03,
already on main) the product does the opposite on purpose, and the SwRS that carry the behaviour
require it. The step can never pass: this is a fixed outcome, not a race. Changing the timeout or
the readiness signal would not help.

## Reproduction

- CI heavy run 44292249060 at 06c93715, job `integration`, log `work/ci-44292249060.log`
  lines 1119-1232. `r14-edit-mode-no-reflow` passes (line 1119). The hover, click and Escape
  steps pass. Then `waitFor` at editorWidgets.js:799 (ts 837) times out with
  `Timed out waiting for edit mode to still be on in the reopened preview`.
- No local run is needed to prove it. The page's start code decides the outcome without any
  timing (see the cause below). `test/page/runtimeOpenInPreview.test.ts`,
  `a fresh panel starts in preview mode, whatever the workspace remembers`, already asserts that
  outcome in the fast suite, and it passes.

## Cause, with evidence

1. `closeAllEditors()` disposes the webview, and `openSidePreview(source)` builds a **fresh
   panel**: `vscode.getState()` returns nothing. A webview's saved state survives only a reload
   or restore of the same panel, never a close followed by an open.
2. `src/page/runtime.ts:365-372` (`@implements_req SwRS-MDOKFSTUDIO-LIFE-170`, `LIFE-172`):
   ```ts
   // A document opens in preview mode. Only the page of the same document that reloads keeps the
   // edit mode its saved state holds; neither another document's state nor the workspace choice does.
   state.editMode = rt.editModeButton && !savedOfOtherDocument ? saved?.editMode === true : false;
   ```
   With no saved state, `editMode` is false. The workspace value
   (`WorkspaceChoices.editMode`, `src/session/workspaceChoices.ts:165`: "no page reads it at
   start: every document opens in preview mode") is never read. `contentPatch.ts:105` then sets
   `html[data-sphinx-preview-edit-mode="off"]` on render.
3. The requirements:
   - SwRS-MDOKFSTUDIO-LIFE-172, scenario "A fresh panel": GIVEN no saved state and a stored
     workspace edit mode of true, WHEN a document opens, THEN the page starts in preview mode.
   - SwRS-MDOKFSTUDIO-LIFE-170, "Edit mode" row: the stored value is "none: the stored edit
     mode is not applied at start (see LIFE-172)", and the default is off. The row "Preview in a
     trusted workspace whose stored edit mode is true" gives "the page still starts in preview
     mode".
   - The scenario's markers are `@tests_req StRS-MDOKFSTUDIO-BLOCK-001` and
     `SwRS-MDOKFSTUDIO-BLOCK-001`. SwRS-BLOCK-001 is about the Edit button: it toggles edit mode
     and tidies up on exit, and it says nothing about reopening. The reopen step was written from
     the **StRS-BLOCK-001** text: "start that preview in edit mode when it was last in edit
     mode", the user_need "I reopen a document to find the preview in the edit mode I last
     chose", Path 2 "The preview opens in the edit mode last chosen", and the CR's own new diagram
     line `[*] --> Editing: new preview, edit mode last on`. The change spec (03-change-spec.md
     line 207, "close and reopen the preview, edit mode still on") also follows that text.
4. So the StRS-BLOCK-001 text is stale against its own derived SwRS (LIFE-170 and LIFE-172) and
   against the product's behaviour since b84b0585. The CR's product diff does not touch the start
   path: `src/page/features/editMode.ts` only moves annotations, and `runtime.ts` is unchanged.

## Smallest fix (CI rule 12: deterministic signal, no sleep, no retry)

In `test/integration/realInput/editorWidgets.ts`, keep the reopen step but assert what LIFE-172
requires. `waitForRender(source)` is already the deterministic readiness signal, and the attribute
is set by the render's content patch:

```ts
    // Reopen: a fresh panel starts in preview mode, whatever edit mode was last chosen (LIFE-172).
    await closeAllEditors();
    await openSidePreview(source);
    await waitForRender(source);
    const reopened = await withCurrentFrame(page, (frame) =>
      frame.locator("html").getAttribute("data-sphinx-preview-edit-mode"));
    assert.equal(reopened, "off", "a fresh preview starts in preview mode (SwRS-MDOKFSTUDIO-LIFE-172)");
```

Then add `@tests_req SwRS-MDOKFSTUDIO-LIFE-172` to the RI-T16 doc block. The alternative is to
drop the four lines altogether, if the step should stay out of a BLOCK-001 scenario.

The requirements and spec text must follow, because the CR wrote or kept the wrong wording:
- In StRS-BLOCK-001, change the diagram line `[*] --> Editing: new preview, edit mode last on`
  to the actual start: a new preview starts in Reading, and only a reload of the same document
  keeps Editing.
- In SwRS-BLOCK-001's verification note, replace "the step that closes the preview and reopens
  it to see edit mode still on" with "...to see it start in preview mode".
- Log the contradiction between StRS-BLOCK-001 (description, user_need, Path 2 "edit mode last
  chosen", "The choice is remembered per workspace") and LIFE-170/172 in
  `requirements/tiers/log.md` as an owner question. BLOCK-001 is `proposed`, so the CR may
  reword it, but which behaviour wins is a product decision. The code and SwRS have said preview
  mode since b84b0585.

## Side note (not this CR's fault)

Line 803 `await new Promise((resolve) => setTimeout(resolve, 300));` is a sleep that breaks
rule 12. It comes from b963b829 (2026-10-27), before this CR, and it is not why the run is red.
