# Perf measurements (node v25.4, darwin; compiled copy of repo in ./out; medians, ms)
Compile OK via `npx tsc -p . --outDir $SCRATCH/out` (no errors). Doc "n" = generator target lines; real lines in col 2.

| n | lines | inKB | parse | renderMyst | renderPreviewDocument | htmlKB | annotateSourceMappings | rewriteSphinxHtml | createDocumentIndex | reanchor x100 (stay/moved) | heapMB(after gc) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1k | 1164 | 25 | 7 | 24 | 21-26 | 80 | 3 | 6-9 | 1 | 1.1/1.0 | 24 |
| 10k | 11123 | 315 | 160 | 440-480 | 430-460 | 838 | 40 | 70 | 6 | 5.6/4.4 | 28 |
| 50k | 55367 | 1586 | 2261 | 3777 | 3539 | 4182 | 644 | 386 | 30 | 17/14 | 47 (245 after 2 more renders, rss 749) |
| 100k | ~110k | ~3200 | 8101 (1 run) | - | 13501 (1 run) | - | - | - | - | - | 411 (rss 1045) |
Scaling 10k->50k (5x lines): parse 14x, render 8x. 50k->100k (2x): parse 3.6x.

Typing (10k doc, 50 single-char edits mid-doc): renderPreviewDocument median 418 ms (max 580); + annotate+sanitize 518 ms;
changedLineRanges 0.5 ms. Host patch path (rendering.ts postContentPatch) sends the whole contentHtml; no incremental render.

CPU profile 50k doc (2 renders + 1 parse, 10.4 s samples): see report.
Activation: require(bundle) with Proxy vscode stub: 47-54 ms, heap +8.5 MB, rss +33-37 MB (fresh build == shipped out/bundle/extension.js). activate() not measured (stub too fragile).
Bundles (minified): extension 1798 KB (out/bundle/extension.js 1.84 MB, map 6.5 MB), preview.js 301 KB, preview.css 145 KB, mermaidPreview.js 5.26 MB, plantumlPreview.js 3.44 MB.
Sanitizer stress: see bench-sanitizer*.mjs outputs in report.
