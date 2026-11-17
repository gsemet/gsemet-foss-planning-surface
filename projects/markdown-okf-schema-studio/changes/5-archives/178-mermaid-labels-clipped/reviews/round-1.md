# Review round 1: CR 178, Mermaid labels clipped

Commit: `93afa3c0` on `change-requests/178-mermaid-labels-clipped` (worktree `markdown-okf-schema-studio-wt-178`).

## Verdict: CHANGES

The fix itself is sound. Two existing gates break because of it, and both must be fixed in this
round.

## What holds

- **Fix vs cause.** With HTML labels, Mermaid puts each label in a `foreignObject` sized from text
  measured in the page. The `<img>` data URI renders that HTML on its own, with no page CSS and
  possibly another font. If the text comes out wider there, the `foreignObject` cuts it.
  `htmlLabels: false` removes the box entirely: `createText` takes the `createFormattedText` branch
  (`<text>`/`<tspan>`), which has nothing to clip. If the widths still differ, the text can now only
  overflow its shape slightly; it is never cut. The exact font or CSS cause is still unproven, and
  `document.fonts.ready` only helps if the page has `@font-face` fonts. That is fine, because the
  fix removes the clipping mechanism whatever the cause.
- **Mermaid 12.2.0 honors the root `htmlLabels` setting.**
  `getEffectiveHtmlLabels(c) = evaluate(c.htmlLabels ?? c.flowchart?.htmlLabels ?? true)` in
  `chunk-DSNLSHJZ.mjs:5291`. The root value wins, and the flowchart default is `null`.
  - Node labels use it (`labelHelper` in `chunk-HAGFOTED.mjs:238/248`).
  - **Edge labels** use it too (`insertEdgeLabel` in `chunk-WQQL4CDK.mjs:322`), so
    "under 10 mi" is covered.
  - The only leftover is `triangle` (`chunk-HAGFOTED.mjs:4946`), which reads
    `flowchart.htmlLabels` for a layout offset only. It has no effect on clipping.
  - An in-diagram `%%{init: {flowchart: {htmlLabels: true}}}%%` cannot turn HTML labels back on,
    because the root setting takes precedence.
- **Unit test** (`mermaidPreviewEntry.test.ts`). It checks that rendering waits for `fonts.ready`
  and that `htmlLabels === false`. Both would fail on the old code: before the fix, `calls.length`
  was 1 while the fonts were still loading, and `htmlLabels` was `undefined`. No other test uses
  the stand-in, so the `mermaidInits` hook breaks nothing.
- **Real-input assertion** (`previewWindow.ts`). It decodes the `encodeURIComponent` data URI,
  which is correct for `mermaidPreview.ts:129`, and injects the SVG inline. Before the fix it
  fails twice: `foreignObjects > 0`, and the nodes have no `<text>`, so `textWidth` is 0. The shape
  selector is safe: Mermaid inserts the shape as the node's first child, so `querySelector` returns
  the shape before the label's `rect.background`. No existing assertion was weakened.
- **`foreignObject` in `test/`.** The only other hits are in `test/security/html-policy.test.ts`,
  which has nothing to do with Mermaid.

## Required changes

1. **The requirements coverage gate fails.** The new `@tests_req SwRS-MDOKFSTUDIO-DIAG-001` marker
   in `test/page/modules/mermaidPreviewEntry.test.ts` is not listed in that requirement's
   `tested_in_files`. `okfreq update-coverage requirements --diff` reports `1 files would change`
   (it adds `test/page/modules/mermaidPreviewEntry.test.ts` to `SwRS-MDOKFSTUDIO-DIAG-001.md`).
   Fix: run `just requirements-update` and commit the result.
2. **The visual check `check_mermaid_theme_switch` breaks.** It reads
   `host.querySelectorAll('.nodeLabel')` (`test/visual/capture_final_checks.py:627`). The
   `.nodeLabel` class only exists in the HTML label branch (`addHtmlSpan`), and SVG text labels
   have no such class. The check is enabled by `mermaidThemeSwitch: true`
   (`scenarioDefinitions1.ts:344`), so `labels` will be empty and the check will report
   "Mermaid theme … lost diagram labels". Fix: select `.node .label text` (keep `.nodeLabel` as an
   alternative), so the check keeps its intent.
3. **The edge label contrast check may no longer measure the right thing.** It reads
   `.edgeLabel p, .edgeLabel text` (`test/visual/capture.py:149`) and compares CSS `color` with
   the nearest ancestor `backgroundColor`. SVG text is painted with `fill`, and its background is
   `rect.background` (fill, opacity 0.5), not a CSS background. The check will mostly fall back to
   the body background, so it can pass or fail for the wrong reason. Fix: for `text` labels, use
   `getComputedStyle(label).fill` and the `.edgeLabel rect` fill. Then run the visual capture
   checks once to confirm.

## Suggestions (optional)

- **Edge labels in the real-input test.** The reported symptom includes an edge label
  ("under 10 mi"). The `foreignObject === 0` assertion already covers edges, but an explicit
  check would document it: every `g.edgeLabel` has a non-empty `<text>`.
- **The "fits its shape" check proves little.** It measures in the page, which is the same context
  Mermaid measured in, so it almost always passes. It does not show what the `<img>` displays. The
  regression guard is the `foreignObject` count. Say so in the comment, or accept it as a sanity
  check.
- **A small behaviour change.** With SVG labels, raw HTML in labels (`<b>`, `fa:` icons) is shown
  as plain text, and only Markdown bold/italic stay styled. Consider adding a line to the CHANGELOG
  or the SwRS.
- **README picture.** The intent asks to regenerate the README picture `myst-diagrams-and-figure`
  once the fix is in. This commit does not do it, so track it in the driver's PR step.
- **Leftover helper.** `normalizeSvgForDataImage` (`<br>` → `<br />`) now only matters for diagrams
  that still emit HTML. That is harmless, so keep it.
