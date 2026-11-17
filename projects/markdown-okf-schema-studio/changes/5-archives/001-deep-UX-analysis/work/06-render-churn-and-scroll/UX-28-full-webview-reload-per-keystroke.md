# UX-28 — Each keystroke in the source editor reloads the whole preview document

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Measured (CDP `framenavigated` events on the webview frame) |
| Area | Live preview while typing in the text editor |
| Related | PERF-05 in `../deep-analysis-review/05-performance-webview-lifecycle.md` (code-level analysis) |

## Use case

An author types in the source editor with the side preview open, on a real chapter
(`book/chapters/02-foundations.md`, 70 KB, figures and admonitions).

## Measurement

Typing 52 characters at 60 ms per key produced **41 full webview navigations** (each one replaces
the whole HTML document of the webview). Across the first session, 71 navigations were recorded for
about 120 typed characters in total.

## Observed effect

- The preview text lags behind the typing by a few characters and catches up at pauses (visible in
  [u03-typing-after.jpg](../../evidence/u03-typing-after.jpg) compared with mid-typing captures).
- Every navigation re-decodes images, re-runs scripts, re-applies the scroll anchor, and resets
  any webview-local state (text selection, open tooltips, find widget matches).
- No visible blank flash was captured on this chapter (no Mermaid). Mermaid-heavy and very long
  chapters were not measured in this campaign (see the complementary report).

## Where it comes from

`src/extension.ts` `handleQueueState` (L749-L792) calls `setStatus` → `setPanelHtml` (full
`webview.html` assignment) for `debouncing` and `building`, then `updatePreview` assigns the result;
link enrichment and PlantUML injection assign `webview.html` again.

## Suggested direction

Follow PERF-05: show pending state with `postMessage`, and patch the content region in place
(`postMessage` with the new body HTML, or morphdom-style diffing) instead of replacing the document.

## Test to add

E2E budget: type N characters with `keyboard.type`, count webview `framenavigated` events, assert
`<= 1` per settled render (or 0 once in-place patching exists).

## Done when

Typing in the source never navigates the webview frame.
