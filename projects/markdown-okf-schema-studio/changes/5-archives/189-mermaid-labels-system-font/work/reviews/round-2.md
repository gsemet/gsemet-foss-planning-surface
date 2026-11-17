# CR 189: Inspector review, round 2

Verdict: **APPROVE**

Reviewed: the uncommitted changes in worktree wt-178, 9 modified and 3 new files. The round 2 edit
touches only `SwRS-MDOKFSTUDIO-DIAG-005.md` and the regenerated `requirements/tiers/swrs/diagrams/index.md`.
The code and tests are unchanged since round 1, which approved them.

## Round 1 request: resolved

`SwRS-MDOKFSTUDIO-DIAG-005` (lifecycle proposed) no longer says the font comes from the theme:

- description and normative text: "take its colours from the preview theme variables" (font dropped);
- table row "Font | --sphinx-preview-font" removed;
- fallbacks: "#f0f0f0, #1f1f1f, #808080 and #ffffff. The font is not a theme value;
  SwRS-MDOKFSTUDIO-DIAG-001 pins it.";
- known issue and criteria lines no longer list the font as an untested theme colour.

The index entry for DIAG-005 matches the new description word for word.

## Consistency DIAG-005 / DIAG-001 / code

- DIAG-001's new scenario "Labels fit their boxes in the picture" holds the pinned font: the
  `myst-mermaid-measure` element with a pinned system stack and 16px, and the same family and size in
  the Mermaid configuration and theme variables.
- DIAG-005 now covers colours only and points to DIAG-001 for the font. Nothing overlaps or
  contradicts.
- Code agrees: `mermaidPreview.ts` sets `fontFamily: MERMAID_FONT_FAMILY` and
  `fontSize: MERMAID_FONT_SIZE` (from `src/core/render/mermaidFont.ts`) and no longer reads
  `--sphinx-preview-font`.
- `SwRS-MDOKFSTUDIO-DIAG-007` still mentions "the sans-serif font" in its text and index line. It is
  `superseded` (by DIAG-005), so it is a historical record and correctly left unchanged.

## Scope

- No StRS file changed. No file under `requirements/tiers/strs` appears in the status.
- Changed files: CHANGELOG, DIAG-001, DIAG-005, diagrams index, `contentBlockStyles.ts`,
  `mermaidPreview.ts`, `previewWindow.ts`, `chartPage.ts`, `mermaidPreviewEntry.test.ts`, plus the new
  `mermaidFont.ts`, `mermaidLabelFit.test.ts` and `mermaidImageLabels.ts`. All are intended (round 1
  set plus the DIAG-005 fix).

## Gates

- `uv run --group requirements okfreq validate --check-links --project-root .` gives
  **1067 requirements, 0 errors, 0 warnings**.

## Still open (driver, not a code defect)

The CR's proof items from round 1 still apply: a heavy real-window run with a picture of "Yes", "No" and
"Hold and inspect" shown whole, and `images/readme/myst-diagrams-and-figure.png` regenerated from that
run.
