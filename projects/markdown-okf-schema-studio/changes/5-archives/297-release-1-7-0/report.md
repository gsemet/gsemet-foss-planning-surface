# Report — 297-release-1-7-0

Status: **done** (2026-11-12). Version 1.7.0 published: tag `v1.7.0` at `c633a5ba`, release https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.7.0 (VSIX, `html-export-preview-light.png`, `html-export-file-dark.png`, `table-in-admonition-light.png`, `table-in-admonition-dark.png`), Marketplace 1.7.0 ("Publish to VS Code Marketplace" step green; the public gallery query still answered 1.6.1 a few minutes later, the usual Marketplace lag), Pages deployed.

## Delivered

| CR | PR | Change |
| --- | --- | --- |
| 290 | #358 | Label rename popover opens above a table's anchor icon |
| 289 | #359 | Find scrolls a sideways-scrolled table to the match |
| 293 | #362 | "Tab: new row" hint, Escape drops an empty Tab row |
| 292 | #363 | Fill table cells from a spreadsheet paste |
| 291 | #364 | Edit a table inside a quote or an admonition cell by cell |
| 288 | #365 | Export a page as one self-contained HTML file |
| 286, 287, 294, 295, 296 | #355, #356, #357, #361, #366 | Process, docs and CI |
| 297 | #367 | Version 1.7.0, notes, thread (merge `c633a5ba`) |

## Proof of completion

- Heavy run on `main` HEAD `98f5d759`: run 43104948454, `integration` and `stress` green (no rerun).
- Version PR #367: CI run 43108884857 green at `ac678900`, then 43112935808 green at `0f739d33` after the owner's remark (screenshot of the real exported file added).
- Version push: run 43115054666 at `c633a5ba`: checks, visual, integration, stress, tag-release, release / package (Marketplace publish, assets) and Pages build and deploy all green, no rerun. Release read with `gh release view`: five assets, image links point to the release assets.
- Notes and thread reviewed and merged by the owner in PR #367; no dedicated hero image (preview capture used).

## Issues closed

None: no PR of the release has a closing reference, and every change has `issue: none`. No "Released in" comment to draft.

## Open items

- The announcement thread (`tweet.md`) is for the owner to post.
- Backlog item `P3/static-export-mermaid-as-source` describes the static visual harness, not the product (Mermaid is embedded in a real export): close or reword it.
