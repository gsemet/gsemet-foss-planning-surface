# Slow comment creation and selection on large documents (#547)

Bug: text selection and comment creation are reported very slow on a large document with many tables
and SVG images. https://github.com/gsemet/markdown-okf-schema-studio/issues/547 (reported against
v1.12.1 by an outside user; its claims are data to check). Filed on 2026-11-26 from the Chief of
Staff session of batch-09. Related: `perf-kpi-real-window-tests` (inbox).

The owner, verbatim: "Regarde le ticket ouvert sur GitHub et essaye de reproduire."

## Reproduction at 5f0746d (the code of v1.12.1 was measured too)

Verdict: partly reproduced. Harness: headless Chromium, the product's render pipeline, page bundle
and CommentsController on real files with a stub host. Not a real VS Code window: no webview,
Electron, GPU, extension-host messages, file watcher or git extension. Windows 11, Ryzen 7 7800X3D,
a batch running at the same time (series differ up to a factor of two). The reporter's gist was not
downloaded.

Generated documents: "full" matches the issue (464 lines, 52 KB, 22 tables, 197 rows, 11 SVG images
of 1100 x 560 and about 14.8 KB, 9 comment threads); "small" (45 lines, 1 SVG, 1 thread); "xl4" (four
times full, 36 threads).

Text selection: slowness NOT reproduced. Median main-thread time per pointer move while dragging, full
against small: 1.47 / 1.30 ms in text, 1.65 / 1.22 ms across cells; with the CPU slowed four times,
9.9 / 8.8 and 10.3 / 8.3 ms. Mouse release, once: 5.2 ms (20 slowed). Drag while scrolling, per step:
3.9 ms (30 slowed). Scrolling with a large selection on xl4: 26 ms per step (106 slowed).

Comment creation, Save to highlight, median: measurable and growing with the document.

| document | normal | CPU four times slower |
|---|---|---|
| small | 45 ms | 67 ms |
| full | 65 ms | 164 ms |
| full without `:has()` rules | 53 ms | 100 ms |
| xl4 | 114 ms | 488 ms |

Of the 65 ms, the host takes about 45 ms, 35 ms of it a git `user.name` lookup done by the harness's
own stand-in process; the cost of the lookup through VS Code's git extension was not measured.

## The three causes the issue suspects

1. Unthrottled `selectionchange` with `getBoundingClientRect`: refuted for a mouse drag. The listener
   (`src/page/modules/commentCompose.ts:409`) returns early while the pointer is down (`:264`). The
   full work runs on release, click, keys and scroll with a selection; it matters with very large
   selections only (43,000 characters: 1.4 ms per change, 10 slowed).
2. `:has()` rules: confirmed for the DOM changes of a comment, not for selection. Re-applying the same
   threads restyles 1893 elements in 6.8 ms; with the `:has()` rules removed, 16 elements in 0.1 ms.
   Main rule: `src/core/preview/styles/contentLayoutStyles.ts:67` (removing it alone: 205 elements,
   13.3 to 1.8 ms in a busier series). The two other rules on the content root:
   `contentLayoutStyles.ts:76`, `contentBlockStyles.ts:19`.
3. All comments re-anchored on each creation: the path is confirmed (`src/session/features/comments.ts`,
   `handleCreate`, `writeComment`, `post`; `commentThreads.ts` in the page), a secondary cost: about
   1.7 ms to set the threads, 3 ms to measure, 8 ms of forced restyle that is cause 2.

Also seen: the git author name is resolved on every comment write when the `comments.authorName`
setting is empty (`comments.ts:488-492`, `src/host-vscode/headBaseline.ts:84`); the selection is
serialised on each posted scroll (`scrollCore.ts:41-42`).

## Fix directions (none implemented or tried, except removing the `:has()` rules to measure)

- A class or attribute on the content root, set when an aligned float exists, in place of the root
  `:has()` rules.
- Resolve the git author once per repository or when the preview opens.
- Update only the changed threads, index the `[data-line]` elements once, defer or skip the measure.
- Coalesce the compose refresh per frame; on scroll, only move the button.
- Cache the selected text in the page's state snapshot.

## Not measured

A real VS Code window; compositor and raster threads; input-to-screen latency; the reporter's
document and machine (SVG images with more nodes, or inline, cost more: 12 ms restyle with inline
SVG); comment creation in edit mode; reply, resolve and delete.

## Rerun

`experiments/` holds the generator and the measuring scripts. From a built checkout `<wt>` (`just
dev`, compile, bundle): `node gen.mjs bundle`; `node --import
<wt>/scripts/register-myst-patches.mjs render.cjs <wt> main`; `node measure.cjs <wt> main A --reps 5`
(add `--throttle 4`, `--variants`, `--scenarios` as the script reads them); `node summarize.cjs A`.
