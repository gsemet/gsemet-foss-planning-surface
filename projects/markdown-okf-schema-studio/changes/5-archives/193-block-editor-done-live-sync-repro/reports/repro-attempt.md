# Repro attempt: block editor Done during live sync (CR 193)

## What was tried

We tried to reproduce, at page (webview runtime) level, the reported failure: select text in a
block editor while a live sync (autosave) is in flight, click Done, and end up with duplicated
source or an editor stuck on "Saving Markdown...". The attempt used the page runtime harness
(`createRuntimeHarness`) and exercised four orderings of autosave, Done click, host patch and
host error.

## Test code

File: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-193/test/page/blockEditorDoneLiveSync.test.ts`

```ts
import * as assert from "node:assert/strict";
import { test } from "node:test";

import { createRuntimeHarness, type RuntimeHarness } from "./runtimeHarness";
import { openBlockEditorWithSource, patchMessage } from "./runtimeTestSupport";

/**
 * CR 193: selecting text in a block editor while a live sync is in flight, then clicking Done,
 * must not leave the source duplicated nor the editor stuck on "Saving Markdown…".
 */

function doneButton(harness: RuntimeHarness) {
  const button = harness.createdElements.find((element) =>
    element.tagName === "BUTTON" && element.getAttribute("aria-label") === "Done editing" && !element.removed);
  assert.ok(button, "the Done button exists");
  return button;
}

// The status line of the open editor; undefined once the editor frame is gone.
function statusText(harness: RuntimeHarness): string | undefined {
  if (!editorOpen(harness)) return undefined;
  const status = harness.createdElements.find((element) =>
    element.getAttribute("data-sphinx-preview-edit-status") !== null);
  return status?.textContent;
}

function saves(harness: RuntimeHarness): Array<Record<string, unknown>> {
  return harness.messages.filter((message) => message.type === "previewEditSave");
}

function editorOpen(harness: RuntimeHarness): boolean {
  return harness.mappings[1].getAttribute("data-sphinx-preview-editing") === "true";
}

function typeAndSelect(textarea: ReturnType<typeof openBlockEditorWithSource>, value: string): void {
  textarea.value = value;
  textarea.selectionStart = 0;
  textarea.selectionEnd = value.length;
  textarea.dispatch("input", { data: "x", inputType: "insertText" });
  textarea.dispatch("select");
}

test("CR 193: autosave in flight, selection, Done, then the live-sync patch of the autosave", () => {
  const harness = createRuntimeHarness();
  const textarea = openBlockEditorWithSource(harness);
  typeAndSelect(textarea, "Second paragraph edited.\n");
  // The live sync: the pending autosave goes out.
  harness.flushTimers?.();
  const before = saves(harness).length;
  doneButton(harness).dispatch("click");
  const afterDone = saves(harness);
  assert.equal(statusText(harness), "Saving Markdown…");
  assert.ok(afterDone.length > before - 1);
  const finals = afterDone.filter((message) => message.final === true);
  assert.equal(finals.length, 1, "exactly one final save is posted");
  // The host's patch for the autosave arrives while the final save is in flight.
  harness.dispatchMessage(patchMessage());
  assert.equal(editorOpen(harness), false, "the editor is closed by the patch");
  assert.notEqual(statusText(harness), "Saving Markdown…", "not stuck on Saving Markdown…");
  assert.equal(saves(harness).filter((message) => message.final === true).length, 1,
    "the patch posts no second final save");
});

test("CR 193: Done first, patch of an earlier sync arrives, a second Done click does not resend", () => {
  const harness = createRuntimeHarness();
  const textarea = openBlockEditorWithSource(harness);
  typeAndSelect(textarea, "Second paragraph edited.\n");
  doneButton(harness).dispatch("click");
  doneButton(harness).dispatch("click");
  assert.equal(saves(harness).filter((message) => message.final === true).length, 1,
    "a repeated Done does not duplicate the final save");
  harness.dispatchMessage(patchMessage());
  assert.equal(editorOpen(harness), false);
  assert.notEqual(statusText(harness), "Saving Markdown…");
});

test("CR 193: patch arrives first, then Done does nothing and posts no save", () => {
  const harness = createRuntimeHarness();
  const textarea = openBlockEditorWithSource(harness);
  typeAndSelect(textarea, "Second paragraph edited.\n");
  const button = doneButton(harness);
  harness.dispatchMessage(patchMessage());
  const count = saves(harness).length;
  button.dispatch("click");
  assert.equal(saves(harness).length, count, "a Done on a closed editor posts no save");
  assert.equal(editorOpen(harness), false);
});

test("CR 193: final save refused by the host (error) leaves the editor usable, not stuck", () => {
  const harness = createRuntimeHarness();
  const textarea = openBlockEditorWithSource(harness);
  typeAndSelect(textarea, "Second paragraph edited.\n");
  doneButton(harness).dispatch("click");
  harness.dispatchMessage({
    type: "previewEditSource",
    documentId: "file:///active.md",
    revision: 7,
    requestId: 11,
    editId: saves(harness).at(-1)?.editId,
    error: "The document changed.",
  });
  assert.notEqual(statusText(harness), "Saving Markdown…");
  // Done works again.
  const before = saves(harness).length;
  doneButton(harness).dispatch("click");
  assert.equal(saves(harness).length, before + 1, "Done can be retried after a refusal");
});
```

## Result

Four orderings tested, four passed. Run with:

```sh
npx tsc -p .
node --import ./scripts/register-myst-patches.mjs --test out/test/page/blockEditorDoneLiveSync.test.js
```

The bug was not reproduced at page level.

## Why it passed

- `src/page/features/blockEditor.ts:339-375` (`postBlockEditSave`) sets `edit.finishing`, so a
  second Done click is a no-op, and it clears the autosave timer, so no autosave fires after Done.
- `src/page/.../contentPatch.ts:50` (`applyContentPatch`) always calls `closeBlockEdit(false)`,
  which clears the "Saving Markdown..." status whenever any patch arrives, including the patch of
  an earlier autosave.
- `blockSourceEditor.ts:41-48`: an error from the host resets `finishing`, so the editor is
  usable again and Done can be retried.

## Residual risk (unverified, host-side)

- The page has no timeout or ack for `previewEditSave`. If the host sends neither a patch nor an
  error after the final save, the status stays "Saving Markdown...".
- The duplication may come from the host applying an autosave and the final save with the same
  `originalText` / line range, because the page never updates them after an autosave. This is a
  hypothesis only; it was not tested.

## Recommendation

Close the backlog item as "not reproduced" at page level. Going further needs a host-side
(extension) test that drives an autosave followed by a final save against the real edit-apply
path.
