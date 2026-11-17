# CR 196 repro attempt (headless, 1 round)

## What was tried
Page-runtime test (test/page/runtimeFindFromBlockEditor.test.ts, test/page harness): focus in the block
editor textarea; Cmd/Ctrl+F keydown on the textarea (page leaves it, no preventDefault); host
previewFindCommand delayed; characters "XY" typed into the textarea during the delay; message delivered so
find.open() focuses the find field; the textarea blurs and BLOCK-047 commits. Caveat: the harness fires no
blur by itself, so the test patches focus() to dispatch one.

## Result
The test (assertions written as "gap keys stay out of the Markdown and end in the find query") FAILS:
previewEditSave carries "Second paragraph.XY". Mechanism confirmed, but it is the ordinary edit path:
the keys were typed into a field that still held the focus, were visible to the reader, and were committed
by the normal blur save (blockSourceEditor.ts:148; relatedTarget outside the editor frame). Nothing is
corrupted or lost silently; the window is one host round trip (milliseconds). No page-side way to tell a
gap key from a real edit. Judged a UX nuance, not a data-integrity defect -> no fix, no PR, nothing committed.

## TOOLBAR-009 row
"Cmd/Ctrl+F in a block editor field: the key is left to the field; the bar does not open." Code: findBar.ts
leaves the key, but package.json when-clause (!editorTextFocus && !inputFocus; inputFocus is not set by a
textarea inside a webview) matches, runFindCommand posts previewFindCommand and find.open() opens the bar.
So the REQUIREMENT row is wrong against the code (not verified in a real window). Options: reword the row,
or make the page open/handle it deliberately. No test covers the full path.

## Test code
```ts
import * as assert from "node:assert/strict";
import { test } from "node:test";

import { createRuntimeHarness, RuntimeElement } from "./runtimeHarness";
import { openBlockEditorWithSource } from "./runtimeTestSupport";

/**
 * CR 196: Cmd/Ctrl+F pressed with the focus in a block editor text box. The page leaves the key to
 * VS Code (findBar.ts), which runs the find command in the extension host and posts
 * `previewFindCommand` back: the bar opens one round trip later. Keys typed in that gap reach the
 * text box; when the find field then takes the focus the editor commits on blur (BLOCK-047).
 */

// @tests_req SwRS-MDOKFSTUDIO-TOOLBAR-009
test("CR 196: keys typed between Cmd/Ctrl+F in a block editor and the find command stay out of the Markdown", () => {
  const harness = createRuntimeHarness({ trackFocus: true });
  const textarea = openBlockEditorWithSource(harness);
  assert.equal(textarea.value, "Second paragraph.");
  textarea.focus();

  // A real browser blurs the element that loses the focus; the harness `focus()` does not.
  const originalFocus = RuntimeElement.prototype.focus;
  RuntimeElement.prototype.focus = function (this: RuntimeElement, options?: FocusOptions): void {
    const previous = harness.document.activeElement as RuntimeElement | null;
    originalFocus.call(this, options);
    if (previous && previous !== this) previous.dispatch("blur", { relatedTarget: this });
  };
  try {
    // (2) The key, as the page sees it: the target is the text box, the page leaves it alone.
    let prevented = 0;
    harness.dispatchWindow("keydown", {
      target: textarea, code: "KeyF", key: "f", metaKey: true, ctrlKey: true, altKey: false, shiftKey: false,
      preventDefault: () => { prevented += 1; }, stopPropagation: () => undefined,
    });
    assert.equal(prevented, 0, "the page leaves the key to VS Code");
    assert.equal(harness.createdElements.some((element) => element.getAttribute("data-find-input") !== null), false,
      "the find bar is not open yet: its command is still on the way");

    // (4) The gap: the reader keeps typing, the characters land in the focused text box.
    const type = (text: string): void => {
      for (const character of text) {
        const target = harness.document.activeElement as RuntimeElement;
        target.value = `${target.value}${character}`;
        target.dispatch("input", { target });
      }
    };
    type("XY");
    assert.equal(textarea.value, "Second paragraph.XY", "the gap characters reached the text box");

    // (5) The host's command arrives: the find field takes the focus, the text box blurs.
    harness.dispatchMessage({ type: "previewFindCommand", documentId: "file:///active.md", revision: 7, requestId: 11, command: "open" });
    const findInput = harness.createdElements.find((element) => element.getAttribute("data-find-input") !== null);
    assert.ok(findInput, "the find bar is built");
    assert.equal(harness.document.activeElement, findInput, "the find field holds the focus");
    harness.flushTimers();
    type("Z");

    const saves = harness.messages.filter((message) => message.type === "previewEditSave");
    assert.ok(saves.length > 0, "the blur committed the editor");
    for (const save of saves) {
      assert.doesNotMatch(String(save.editedText), /XY/u, "the characters typed in the gap did not reach the Markdown");
    }
    assert.equal(findInput.value, "XYZ", "the typed keys are not lost: they ended in the find query");
  } finally {
    RuntimeElement.prototype.focus = originalFocus;
  }
});
```
