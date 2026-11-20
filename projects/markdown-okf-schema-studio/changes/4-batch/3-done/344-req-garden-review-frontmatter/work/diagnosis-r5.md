# Diagnosis r5: heavy run 44283551410, real-input red at realinput-t16

Verdict: **the base's (CR-343) bug, deterministic, not a flake, not CR-344's.** The assertion
added by CR-343's commit 225e73b9 (rebased as f9c37f6d on CR-343's branch at 01a6eaf4) cannot pass:
it measures the clicked paragraph, which the block editor hides (`display: none`) and keeps in the
DOM. No heavy run triggered on CR-343's branch: the code proof below decides the question.

## Reproduction

`gh workflow run ci.yml --ref chantier/batch-06/cr-344-cr -f heavy=true` (run 44283551410), job
integration, step real-input. Log: `work/ci-44283551410.log`, lines 1124-1267.

```
1124 PASS real-input screenshot: block-editing/r14-edit-mode-no-reflow
1125 Real-input failure, at the failing step: scenario fixture realinput-t16
1223 Real-input integration failed: AssertionError [ERR_ASSERTION]: paragraph at line 3 changed height from 67.171875 to 0
     at out/test/integration/realInput/editorWidgets.js:787:20
     at async scenarioEditModeNoReflow (editorWidgets.js:763:5)
     at async run (realInput/run.js:287:9)
1234 STEP failed: real-input (96957 ms)
```

## (1) Scenario and step

`realinput-t16` is the fixture of `scenarioEditModeNoReflow` (RI-T16),
`test/integration/realInput/editorWidgets.ts:769-834`, called from `realInput/run.ts:273`. The
failing check is the loop at line 822-824, after the click on the first paragraph (line 819):

```ts
const heights = () => ... frame.locator("p[data-sphinx-source-line]").evaluateAll(... getBoundingClientRect().height)
...
await ... locator("p[data-sphinx-source-line]").nth(0).click();
await waitForEditor(page, "[data-sphinx-preview-block-editor] textarea");
const clicked = await heights();
for (const [line, height] of Object.entries(clicked)) {
  assert.ok(Math.abs(height - (reading[line] ?? Number.NaN)) <= 2, `paragraph at line ${line} changed height ...`);
}
assert.equal(Object.keys(clicked).length, Object.keys(reading).length - 1, "only the clicked block became an editor");
```

"Line 3" is the first paragraph (DOCUMENT = heading, blank, `paragraph(0)` at line 3): the clicked one.

Who wrote it:

```
$ git log --format='%h %ad %s' --date=iso -S "only the clicked block became an editor" --all -- test/integration/realInput/editorWidgets.ts
f9c37f6d 2026-11-17 23:54:20 +0100 docs: add use case diagrams and validation scenarios to block and table requirements
225e73b9 2026-11-17 23:54:20 +0100 docs: add use case diagrams and validation scenarios to block and table requirements
```

225e73b9 is the base's tip (CR-343, `git log ee592ea3..225e73b9`: abb5cd82, bcb958e7, 225e73b9);
f9c37f6d is the same commit on CR-343's rebased branch (origin at 01a6eaf4), so the bug is still
there. Main (ee592ea3) has only the before/after measures of RI-T16, which pass (log line 1124).

CR-344 does not touch it:

```
$ git diff --stat 225e73b9 HEAD -- test/integration/realInput/editorWidgets.ts test/integration/realInput/common.ts \
    src/page/features/blockEditor.ts src/page/features/editMode.ts src/page/features/blockSourceEditor.ts \
    src/core/preview/styles/editModeStyles.ts src/core/preview/styles/contentLayoutStyles.ts
(empty)
```

CR-344's only `realInput/run.ts` change adds `scenarioTodoToggle` earlier in the sequence; it
cannot change the result (the failure is by construction, below).

## (2) Cause: the clicked paragraph stays in the selector with height 0

- `src/page/features/blockEditor.ts:289` `renderedTarget.setAttribute("data-sphinx-preview-editing", "true")`
  and `:294` `renderedTarget.insertAdjacentElement("afterend", element)`: the paragraph is kept,
  the editor is inserted after it, synchronously on open (before the textarea `waitForEditor` waits for).
- `src/core/preview/styles/editModeStyles.ts:38-40`:
  `[data-sphinx-preview-editing="true"] { display: none !important; }`.
- The paragraph keeps `data-sphinx-source-line`, so `p[data-sphinx-source-line]` still matches it
  and `getBoundingClientRect().height` is 0: the loop fails on it every time (67.17 to 0), and the
  next assertion (count = reading - 1) would fail too, since the count does not drop.

Every element is deterministic (attribute set at open, CSS rule `!important`, `evaluateAll`
includes hidden elements), so it is not a flake. Before this check the scenario passed the
reflow and hover checks (screenshot r14 PASS, hover `deepEqual` passed).

## preview-editing step

Not reached in this run: `test/integration/trusted-suite.ts:198` runs `real-input`, then `:205`
`preview-editing`; the suite stops at the first failed step (log line 1234, then 1267
`ci-integration: FAILED`, no `STEP start: preview-editing` in the log). The r4 fix is therefore
neither confirmed nor refuted by this run.

## Place to fix (CR-343's branch, not CR-344)

`test/integration/realInput/editorWidgets.ts`, RI-T16 click check (after line 821): measure only
visible paragraphs, e.g. select `p[data-sphinx-source-line]:not([data-sphinx-preview-editing="true"])`
in `clicked`, or skip entries whose element has `data-sphinx-preview-editing`, so the hidden clicked
paragraph drops out and the count check holds. Then a heavy run on CR-344 also gets to preview-editing.
