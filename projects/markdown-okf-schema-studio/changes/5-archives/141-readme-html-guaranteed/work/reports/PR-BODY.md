## Summary

README-style HTML now renders in the preview the way GitHub renders it: centred `<div align>` and
`<p align>`, `<br>`, sized `<img>`, linked logos and badge rows, `<picture>` with
theme-following `<source>`, `<details>`, `<kbd>`, `<sub>`, `<sup>`. Markdown after a blank
line inside an HTML block is rendered. In edit mode each top-level HTML block is a frame titled with
its literal opening tag (for example `<div align="center">`); a click edits only that block's raw
source. The sanitizer is unchanged: no new allowed attribute, no script, no event handlers.

## Deliverables

Preview, before and after (cream and dark):

| Before | After |
| --- | --- |
| ![before cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cf58d61a5b3f8ac08c9b0eed2800e44c882a11c2/before-cream.png) | ![after cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cf58d61a5b3f8ac08c9b0eed2800e44c882a11c2/after-cream.png) |
| ![before dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cf58d61a5b3f8ac08c9b0eed2800e44c882a11c2/before-dark.png) | ![after dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cf58d61a5b3f8ac08c9b0eed2800e44c882a11c2/after-dark.png) |

Edit mode, before and after:

| Before | After |
| --- | --- |
| ![before edit cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cf58d61a5b3f8ac08c9b0eed2800e44c882a11c2/before-edit-cream.png) | ![after edit cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cf58d61a5b3f8ac08c9b0eed2800e44c882a11c2/after-edit-cream.png) |
| ![before edit dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cf58d61a5b3f8ac08c9b0eed2800e44c882a11c2/before-edit-dark.png) | ![after edit dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/cf58d61a5b3f8ac08c9b0eed2800e44c882a11c2/after-edit-dark.png) |

The edit-mode titles use the `openingTagTitle` helper (`src/core/render/blockTagTitle.ts`);
the HTML handling lives in `src/core/render/mystRawHtml.ts` with styles in
`src/core/preview/styles/htmlBlockStyles.ts`.

## Test plan

- Unit tests for the raw-HTML pass and styles (fail with the pass disabled); suite 2846 passing.
- A real VS Code window scenario (`readme-html`) that fails before and passes after.
- `just check` is green up to the known requirements-coverage baseline churn, unrelated.

## Autonomous decisions

- Only top-level HTML blocks get an edit-mode frame; nested elements stay inside their parent's frame.
- Fixture uses local SVGs; no side-by-side with GitHub's own rendering was captured.
- Stacked on the edit-mode tag-title change.

## Internal references

CR 141 (readme-html-guaranteed), built on CR 140.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
