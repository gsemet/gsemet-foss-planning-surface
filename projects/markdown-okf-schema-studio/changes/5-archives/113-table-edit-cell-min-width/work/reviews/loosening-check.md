Verdict: APPROVE

- The original intent was a stuck hover outline from the click that opens the editor; blockEditor.ts:249 clears the hover on open, and the outlined element is the one that gets data-sphinx-preview-editing="true" (blockEditor.ts:278), so a stuck outline lands on the edited block.
- The new check fails on any outlined element that is inside .sphinx-preview-block-editor or carries the editing attribute, which covers exactly that regression and an outline left inside the editor.
- The dropped case is an outline on some other block. After the editor opens, the page can reflow under the stationary pointer, and editHoverTarget (editMode.ts:39) then outlines whatever block is under it. That outline is correct, and the old zero-count assertion would flag it falsely.
- Residual gap: a stuck outline on a non-edited element that was not reflow-driven would pass. This is minor, and the failure message now names the offending tags.
