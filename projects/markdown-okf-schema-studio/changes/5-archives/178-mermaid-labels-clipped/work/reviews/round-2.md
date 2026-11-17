# Review round 2: CR 178, Mermaid labels clipped

Commits: `93afa3c0` (fix) and `21ab4d40` (round-1 fixes) on `change-requests/178-mermaid-labels-clipped`
(worktree `markdown-okf-schema-studio-wt-178`).

## Verdict: APPROVE

All three required changes from round 1 are done correctly. Nothing blocks the merge.

## What was checked

I checked against Mermaid 12.2.0 from the worktree `node_modules`. I rendered the demo diagram in
headless Chromium with `htmlLabels: false` and the real config shape.

1. **Edge label contrast (`test/visual/capture.py`).**
   - Labels in the SVG namespace now read `fill`. Their background is the `.edgeLabel rect`
     (`rect.background`) fill.
   - The ancestor `backgroundColor` loop runs only when no rect fill was found. The body is the last
     fallback.
   - Probe result: edge text `fill` is the theme text colour. The rect fill is
     `edgeLabelBackground`, with dark palette `rgb(204,204,204)` on `rgb(37,37,38)`, and light
     `rgb(31,31,31)` on `rgb(240,240,240)`. The check therefore measures the real pair.
   - HTML path: a `.edgeLabel p` element is XHTML, so `isSvgText` is false. It reads `color`, gets
     no rect, and runs the ancestor loop as before. The HTML path is unchanged.
2. **Theme-switch selector (`capture_final_checks.py`).** `.nodeLabel, .node .label text` returns
   one entry per node label: "Review telemetry", "Ready?", "Dispatch fleet", "Hold and inspect".
   Wrapped lines are joined without spaces in `textContent`. That is fine, because the check only
   compares modes with each other.
3. **Edge-label assertion (`previewWindow.ts`).** The demo diagram has two labelled edges (`Yes`,
   `No`) and one unlabelled edge.
   - Mermaid creates `.edgeLabel` elements only for the two labelled edges, so no empty `<text>`
     with width 0 trips the `every(width > 0)` test.
   - The probe gave widths of about 22.7 px and 18.8 px.
   - It found `foreignObject` 0.
   - The assertion is valid and would fail with HTML labels, where there is no `.edgeLabel text`.
4. **Side effect: labels are now plain text.** I verified it in the probe:
   - `<b>bold</b>` shows literally as `<b> bold </b>`.
   - `fa:fa-car` shows as the text `fa:fa-car`.
   - `<br>` is still a line break.

   The CHANGELOG entry states the raw-HTML case. No SwRS, README or doc describes HTML, icons or
   Markdown in Mermaid labels. I grepped `requirements/`, `docs/` and `README.md` for `htmlLabels`,
   `foreignObject`, `fa:` and label HTML/Markdown, and found no hits.
   - DIAG-005 and DIAG-006 ("keeps its node labels"), and DIAG-008 (edge label contrast), still
     hold.
   - The DIAG-001 scenario "Line-break tags in the SVG" still describes the kept
     `normalizeSvgForDataImage` helper, so it needs no edit.
5. **SwRS-MDOKFSTUDIO-DIAG-001.md.** The only requirement change on the branch adds the one
   generated `tested_in_files` line, `test/page/modules/mermaidPreviewEntry.test.ts`, in sorted
   order. `okfreq update-coverage requirements --check` reports `0 files would change`.

## Suggestions (optional, non-blocking)

- **CHANGELOG.** Also name `fa:` icons. They now show as the literal text `fa:fa-…`. Before, they
  were an `<i>` with no Font Awesome CSS inside the image, so they were already invisible. Suggested
  wording: "Raw HTML or `fa:` icon names inside a label now show as plain text."
- **Contrast check.** The `.edgeLabel rect` has `opacity: 0.5`, and the check uses its fill as
  opaque. With the current palettes the shown background stays in the same light or dark family,
  so the result does not change. A stricter check would blend the rect fill with the body
  background at that opacity.
- **README picture.** The `myst-diagrams-and-figure` regeneration is still to be tracked in the PR
  step, as noted in round 1.
