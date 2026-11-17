# P9 migration table (regenerated after B2b, post-D32)

Numbers and groups follow `tools/old_to_new.json` (authoritative; includes the D32 split into
`frontmatter-schema` v01-v19 and `frontmatter-editing` v01-v06). B2a applied the ids, B2b the A rows
(`capture: false`) and the kept step lists. The Real window section is unchanged (T1 will move the
former frontmatter real rows r01-r17 to `frontmatter-editing`).

Old id → new id. New visual ids are `<group>/vNN-<slug>-<theme>-<width>`, real-window ids
`<group>/rNN-<slug>`. PNG paths: `out/reports/e2e/screenshots/visual/<group>/<file>.png`, step PNGs
`<file>--<step>.png`. Numbers are assigned in campaign order and become permanent at the end of
B2a (new scenarios take the next free number of their group). PNG location: `screenshots/visual/<group>/`.
After plan-review R1 the only D/M rows are the 4 exact aliases (action M); every former D/M row
with other checks is A (assertion-only), see `tools/overrides.mjs`.

## Visual

| Old id | Action | New id | Step PNGs kept | Step PNGs dropped | Note |
| --- | --- | --- | --- | --- | --- |
| handbook-dark-top | K | rendering-core/v01-handbook-top-dark-900 |  |  |  |
| handbook-dark-third | K | rendering-core/v02-handbook-mid-code-dark-900 |  |  |  |
| handbook-dark-bottom | A | rendering-core/v03-handbook-bottom-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. same lock as chapter-dark-bottom (end of page reachable above the bottom padding); the chapter sentinel is the stronger check |
| handbook-light-top | K | rendering-core/v04-handbook-top-light-900 |  |  |  |
| handbook-forced-white | K | theme-zoom/v01-forced-white-handbook-white-900 |  |  |  |
| handbook-forced-cream | K | theme-zoom/v02-forced-cream-handbook-cream-900 |  |  |  |
| admonitions-forced-cream-full | K | theme-zoom/v03-forced-cream-admonitions-full-cream-900 |  |  |  |
| code-tables-forced-cream | K | theme-zoom/v04-forced-cream-code-tables-full-cream-900 |  |  |  |
| frontmatter-forced-cream | K | theme-zoom/v05-forced-cream-properties-cream-900 |  |  |  |
| edit-paragraph-forced-cream | A | theme-zoom/v06-forced-cream-paragraph-editor-cream-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. editor chrome on cream is captured by edit-palette-cream (same palette, frame and buttons) |
| handbook-light-failures | A | myst/v01-failure-admonitions-light-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. crop of the admonition run already whole in admonitions-light-full; accent checks are page checks |
| handbook-narrow-top | K | rendering-core/v05-handbook-top-dark-460 |  |  |  |
| handbook-narrow-table | K | layout-width/v01-narrow-table-scroll-dark-460 |  |  |  |
| admonitions-dark-full | K | myst/v02-admonition-gallery-full-dark-900 |  |  |  |
| admonitions-light-full | K | myst/v03-admonition-gallery-full-light-900 |  |  |  |
| admonitions-dark-titled | A | myst/v04-admonition-titles-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. viewport crop of admonitions-dark-full; the one-title-per-block rule is a page check |
| admonitions-dark-nested | A | myst/v05-admonition-nested-content-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. viewport crop of admonitions-dark-full (nested list/code/table/quote visible there) |
| admonitions-narrow-full | K | myst/v06-admonition-gallery-full-dark-460 |  |  |  |
| unresolved-dark-full | K | myst/v07-citations-toctree-unresolved-full-dark-900 |  |  |  |
| unresolved-light-full | K | myst/v08-citations-toctree-unresolved-full-light-900 |  |  |  |
| nested-list-typing-dark | K | block-editing/v01-nested-list-typing-dark-460 |  |  |  |
| nested-list-typing-light | A | block-editing/v02-nested-list-typing-light-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. same typing assertions as nested-list-typing-dark; theme and width add nothing |
| editor-keyboard-wrapped-narrow | K | block-editing/v03-wrapped-paragraph-keyboard-dark-460 | selected |  |  |
| context-tags-dark-wide | K | myst/v09-context-tags-dark-900 |  |  |  |
| context-tags-dark-narrow | A | myst/v10-context-tags-dark-460 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme/width matrix: wrapping kept by context-tags-light-narrow |
| context-tags-light-wide | A | myst/v11-context-tags-light-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme/width matrix: light kept by context-tags-light-narrow |
| context-tags-light-narrow | K | myst/v12-context-tags-light-460 |  |  |  |
| mermaid-map-dark | K | diagrams/v01-mermaid-map-dark-900 |  |  |  |
| mermaid-map-light | K | diagrams/v02-mermaid-map-light-900 |  |  |  |
| mermaid-map-fallback | K | diagrams/v03-mermaid-map-fallback-900 |  |  |  |
| plantuml-success-light | K | diagrams/v04-plantuml-success-light-900 |  |  |  |
| plantuml-success-dark | K | diagrams/v05-plantuml-success-dark-900 |  |  |  |
| plantuml-unconfigured | K | diagrams/v06-plantuml-unconfigured-light-900 |  |  |  |
| plantuml-executable-not-found | K | diagrams/v07-plantuml-not-found-light-900 |  |  |  |
| code-copy-button-light | K | code-blocks/v01-copy-button-light-900 | hover |  |  |
| code-copy-button-dark | K | code-blocks/v02-copy-button-dark-900 |  | hover |  |
| code-copy-button-cream | A | code-blocks/v03-copy-button-cream-900 |  | hover |  |
| code-dark-top | K | code-blocks/v04-typescript-block-dark-900 |  |  |  |
| code-dark-table | K | layout-width/v02-wide-table-scroll-dark-900 |  |  |  |
| code-dark-table-narrow | K | layout-width/v03-table-identifiers-nowrap-dark-640 |  |  |  |
| code-light-table-narrow | A | layout-width/v04-table-identifiers-nowrap-light-640 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. same identifier-split machine check as code-dark-table-narrow |
| code-light-full | K | rendering-core/v06-mixed-blocks-full-light-900 |  |  |  |
| chapter-dark-top | K | rendering-core/v07-chapter-top-dark-900 |  |  |  |
| chapter-figure-dark | K | myst/v13-figure-external-svg-dark-900 |  |  |  |
| chapter-dark-quarter | A | rendering-core/v08-chapter-quarter-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. colour-bleed checks are page checks run by chapter-dark-top on the same page |
| chapter-dark-half | K | myst/v14-display-math-dark-900 |  |  |  |
| chapter-dark-three-quarters | A | rendering-core/v09-chapter-three-quarters-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. back-to-back admonitions are covered by admonition-gallery-full |
| chapter-dark-bottom | K | rendering-core/v10-chapter-bottom-sentinel-dark-900 |  |  |  |
| chapter-light-top | A | rendering-core/v11-chapter-top-light-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme pair of chapter-dark-top; light body is captured by handbook-light-top |
| chapter-max-width-dark-full | K | layout-width/v05-max-content-width-full-dark-1600 |  |  |  |
| chapter-max-width-light-full | A | layout-width/v06-max-content-width-full-light-1600 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. same centring check as the dark capture; theme-independent geometry |
| syntax-dark-markdown | K | code-blocks/v05-markdown-fence-dark-900 |  |  |  |
| syntax-dark-rust | K | code-blocks/v06-rust-dark-900 |  |  |  |
| syntax-dark-python | K | code-blocks/v07-python-dark-900 |  |  |  |
| syntax-light-rust | K | code-blocks/v08-rust-light-900 |  |  |  |
| syntax-light-shell | M | → code-blocks/v10-shell-json-diff-unknown-light-900 |  |  | alias of the same page and scroll; its unknown-grammar lock moves to the diff capture | **removed in B2a**
| diff-dark-preview | K | code-blocks/v09-diff-fence-dark-900 |  |  |  |
| diff-light-preview | K | code-blocks/v10-shell-json-diff-unknown-light-900 |  |  |  |
| diff-dark-edit | A | code-blocks/v11-diff-fence-edit-mode-dark-900 |  |  | was M: its checks have no equal elsewhere, kept assertion-only. near-identical PNG; add an edit-mode toggle check inside the preview scenario |
| diff-light-edit | A | code-blocks/v12-diff-fence-edit-mode-light-900 |  |  | was M: its checks have no equal elsewhere, kept assertion-only. near-identical PNG; same toggle check |
| syntax-narrow-python | K | code-blocks/v13-python-overflow-dark-460 |  |  |  |
| frontmatter-forced-white | K | theme-zoom/v07-forced-white-properties-white-900 |  |  |  |
| okf-schema-table | K | frontmatter-schema/v01-okf-schema-table-white-900 |  |  |  |
| okf-schema-narrow | A | frontmatter-schema/v02-okf-schema-narrow-hidden-description-dark-460 |  |  | was M: its checks have no equal elsewhere, kept assertion-only. alias; the hidden Description column check joins the narrow scroll-stress capture |
| frontmatter-links-loading | K | frontmatter-schema/v03-links-loading-dark-900 |  |  |  |
| frontmatter-links-loaded | A | frontmatter-schema/v04-links-loaded-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. same state as frontmatter-link-details-dark-900 (loaded links, dark, 900) |
| preview-toolbar-dark | M | → frontmatter-schema/v05-okf-schema-table-dark-900 |  |  | alias; toolbar-over-properties lock becomes a line of okf-schema-dark | **removed in B2a**
| edit-mode-dark | M | → block-editing/v04-paragraph-editor-open-dark-900 |  |  | alias of the same state | **removed in B2a**
| edit-paragraph-dark | K | block-editing/v04-paragraph-editor-open-dark-900 |  |  |  |
| edit-admonition-dark | K | block-editing/v05-admonition-editor-open-dark-900 |  |  |  |
| edit-affordances-hover-and-open | K | block-editing/v06-hover-outline-then-editor-dark-900 | hover |  |  |
| edit-affordances-narrow | K | block-editing/v07-editor-status-wrap-dark-460 |  | hover |  |
| edit-palette-light | K | palette-slash/v01-palette-popups-light-900 | alert, bar, colour, colour-code, emoji, grid, menu |  |  |
| edit-palette-tall-light | K | palette-slash/v02-palette-sticky-tall-editor-light-900 | end, top |  |  |
| edit-palette-tall-dark | K | palette-slash/v03-palette-sticky-tall-editor-dark-900 |  | end, top |  |
| edit-palette-tall-narrow-360 | K | palette-slash/v04-palette-not-sticky-narrow-dark-360 | end | top |  |
| palette-mode-strict-light | K | palette-slash/v05-mode-strict-light-900 | palette | insert-point |  |
| palette-mode-strict-dark | A | palette-slash/v06-mode-strict-dark-900 |  | insert-point, palette | was D: its checks have no equal elsewhere, kept assertion-only. theme repeat of the strict button set |
| palette-mode-gfm-light | K | palette-slash/v07-mode-gfm-light-900 | palette | insert-point |  |
| palette-mode-gfm-dark | A | palette-slash/v08-mode-gfm-dark-900 |  | insert-point, palette | was D: its checks have no equal elsewhere, kept assertion-only. theme repeat of the GFM button set |
| palette-mode-myst-light | K | palette-slash/v09-mode-myst-light-900 |  | insert-point, palette |  |
| palette-mode-myst-dark | A | palette-slash/v10-mode-myst-dark-900 |  | insert-point, palette | was D: its checks have no equal elsewhere, kept assertion-only. -palette PNG is byte-identical to edit-palette-dark; scenario PNG to its -insert-point |
| slash-menu-strict-light | K | palette-slash/v11-slash-strict-light-900 |  | filtered, flip, nomatch, open |  |
| slash-menu-gfm-light | K | palette-slash/v12-slash-gfm-light-900 | filtered, flip, nomatch, open |  |  |
| slash-menu-myst-light | K | palette-slash/v13-slash-myst-light-900 |  | filtered, flip, nomatch, open |  |
| slash-menu-myst-dark | K | palette-slash/v14-slash-myst-filtered-dark-900 |  | filtered, flip, nomatch, open |  |
| edit-palette-dark | K | palette-slash/v15-palette-above-editor-dark-900 |  | alert, bar, colour, colour-code, emoji, grid, menu |  |
| edit-palette-cream | K | palette-slash/v16-palette-above-editor-cream-900 |  | alert, bar, colour, colour-code, emoji, grid, menu |  |
| edit-palette-narrow-360 | K | palette-slash/v17-palette-wraps-narrow-dark-360 | emoji, grid, menu | alert, bar, colour, colour-code |  |
| edit-insert-point-hover | K | block-editing/v08-insert-point-hover-light-900 | hover |  |  |
| edit-insert-after-final-figure | K | block-editing/v09-insert-after-final-figure-light-900 |  |  |  |
| edit-insert-after-final-image | K | block-editing/v10-insert-after-final-image-light-900 |  |  |  |
| edit-first-block-top-wide | A | layout-width/v07-first-block-top-light-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. superseded by first-element-gap-h1-900 (40 px gap is stricter than the 20 px minimum); PNG near-identical |
| edit-first-block-top-narrow | A | layout-width/v08-first-block-top-dark-460 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. superseded by first-element-gap-h1-460 |
| edit-empty-document-start-writing | A | layout-width/v09-empty-start-writing-light-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. superseded by first-element-gap-empty-900 (Start writing at 40 px) |
| edit-empty-document-enter-opens-editor | K | block-editing/v11-empty-doc-enter-opens-editor-light-900 |  |  |  |
| edit-list-narrow | K | block-editing/v12-list-item-opens-whole-list-dark-460 |  |  |  |
| edit-table-wide-end-dark | K | table-editing/v01-wide-table-end-key-dark-900 | end |  |  |
| edit-table-cell-dark | M | → table-editing/v04-cell-editor-wraps-dark-900 |  | arrowdown, cell-bar, cell-emoji, end, open | alias that still writes 5 secondary PNGs byte-identical to its canonical (harness bug) | **removed in B2a**
| edit-table-wrapped-light-900 | K | table-editing/v02-cell-editor-wraps-light-900 | arrowdown, cell-bar, cell-emoji, open | end |  |
| edit-table-wrapped-light-460 | K | table-editing/v03-cell-editor-wraps-light-460 | open | arrowdown, cell-bar, cell-emoji, end |  |
| edit-table-wrapped-dark-900 | K | table-editing/v04-cell-editor-wraps-dark-900 | open | arrowdown, cell-bar, cell-emoji, end |  |
| edit-table-wrapped-dark-460 | A | table-editing/v05-cell-editor-wraps-dark-460 |  | arrowdown, cell-bar, cell-emoji, end, open |  |
| edit-frontmatter-key-dark | K | frontmatter-editing/v01-edit-key-suggestions-dark-900 |  |  |  |
| edit-frontmatter-value-dark | K | frontmatter-editing/v02-edit-enum-value-dark-900 |  |  |  |
| edit-frontmatter-list-dark | K | frontmatter-editing/v03-edit-list-dark-900 |  |  |  |
| edit-frontmatter-list-light | A | frontmatter-editing/v04-edit-list-light-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme pair of edit-frontmatter-list-dark (same reorder/add/remove checks) |
| edit-frontmatter-boolean-dark | K | frontmatter-editing/v05-edit-boolean-white-900 |  |  |  |
| preview-edit-activation-scroll-wide | K | block-editing/v13-activation-keeps-scroll-dark-900 |  |  |  |
| preview-edit-activation-scroll-narrow | K | block-editing/v14-activation-keeps-scroll-light-460 |  |  |  |
| math-edit-offline-dark | K | myst/v15-math-edit-source-offline-dark-900 |  |  |  |
| math-edit-offline-light-narrow | K | myst/v16-math-edit-source-offline-light-460 |  |  |  |
| preview-sticky-headings-1 | K | toolbar-navigation/v01-sticky-depth-1-dark-900 |  |  |  |
| preview-sticky-headings-2 | K | toolbar-navigation/v02-sticky-depth-2-dark-900 |  |  |  |
| preview-sticky-headings-3 | K | toolbar-navigation/v03-sticky-depth-3-oscillation-dark-900 |  |  |  |
| preview-sticky-headings-3-light-narrow | K | toolbar-navigation/v04-sticky-depth-3-light-460 |  |  |  |
| preview-sticky-headings-natural-growth | K | toolbar-navigation/v05-sticky-wrapped-growth-dark-460 |  |  |  |
| okf-schema-dark | K | frontmatter-schema/v05-okf-schema-table-dark-900 |  |  |  |
| okf-schema-missing-required-dark | K | frontmatter-schema/v06-missing-required-dark-900 |  |  |  |
| okf-schema-missing-required-light | K | frontmatter-schema/v07-missing-required-light-900 |  |  |  |
| schema-validation-error-dark | K | frontmatter-schema/v08-schema-compile-error-dark-900 |  |  |  |
| schema-validation-error-light | A | frontmatter-schema/v09-schema-compile-error-light-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme pair; the light variant is kept at 460 px (schema-validation-error-narrow) |
| schema-validation-error-narrow | K | frontmatter-schema/v10-schema-compile-error-light-460 |  |  |  |
| frontmatter-scroll-feedback | K | frontmatter-schema/v11-okf-schema-narrow-scroll-stress-dark-460 |  |  |  |
| frontmatter-scroll-feedback-edit | A | frontmatter-editing/v06-okf-schema-narrow-scroll-stress-edit-dark-460 |  |  | was M: its checks have no equal elsewhere, kept assertion-only. near-identical PNG; run the three cycles again with edit mode on inside one scenario |
| frontmatter-dark | K | frontmatter-schema/v12-properties-plain-dark-900 |  |  |  |
| frontmatter-light | K | frontmatter-schema/v13-properties-plain-light-900 |  |  |  |
| standalone-frontmatter-dark | K | frontmatter-schema/v14-generic-yaml-skill-dark-900 |  |  |  |
| standalone-frontmatter-light | A | frontmatter-schema/v15-generic-yaml-skill-light-900 |  |  |  |
| bare-urls-light-wide | K | gfm/v01-bare-urls-light-900 |  |  |  |
| inline-code-dark | K | rendering-core/v12-inline-code-full-dark-900 |  |  |  |
| inline-code-light | K | rendering-core/v13-inline-code-full-light-900 |  |  |  |
| inline-code-white | A | rendering-core/v14-inline-code-full-white-900 |  |  |  |
| inline-code-cream | K | rendering-core/v15-inline-code-full-cream-900 |  |  |  |
| orphan-box-document-end | K | review-annotations/v01-orphan-box-end-padding-dark-900 |  |  | the PNG never shows the box (removed before capture): keep the short box in place for the capture |
| inline-code-narrow | K | rendering-core/v16-inline-code-narrow-full-dark-460 |  |  |  |
| first-element-gap-paragraph-900 | K | layout-width/v10-first-gap-paragraph-edit-light-900 |  |  |  |
| first-element-gap-paragraph-460 | A | layout-width/v11-first-gap-paragraph-edit-light-460 |  |  |  |
| first-element-gap-paragraph-1600 | A | layout-width/v12-first-gap-paragraph-edit-light-1600 |  |  |  |
| first-element-gap-h1-900 | A | layout-width/v13-first-gap-h1-edit-light-900 |  |  |  |
| first-element-gap-h1-460 | A | layout-width/v14-first-gap-h1-edit-light-460 |  |  |  |
| first-element-gap-h1-1600 | K | layout-width/v15-first-gap-h1-edit-light-1600 |  |  |  |
| first-element-gap-h2-900 | A | layout-width/v16-first-gap-h2-edit-light-900 |  |  |  |
| first-element-gap-h2-460 | A | layout-width/v17-first-gap-h2-edit-light-460 |  |  |  |
| first-element-gap-h2-1600 | A | layout-width/v18-first-gap-h2-edit-light-1600 |  |  |  |
| first-element-gap-h3-900 | A | layout-width/v19-first-gap-h3-edit-light-900 |  |  |  |
| first-element-gap-h3-1600 | A | layout-width/v20-first-gap-h3-edit-light-1600 |  |  |  |
| first-element-gap-table-900 | A | layout-width/v21-first-gap-table-edit-light-900 |  |  |  |
| first-element-gap-table-460 | A | layout-width/v22-first-gap-table-edit-light-460 |  |  |  |
| first-element-gap-table-1600 | A | layout-width/v23-first-gap-table-edit-light-1600 |  |  |  |
| first-element-gap-image-900 | A | layout-width/v24-first-gap-image-edit-light-900 |  |  |  |
| first-element-gap-image-460 | A | layout-width/v25-first-gap-image-edit-light-460 |  |  |  |
| first-element-gap-image-1600 | A | layout-width/v26-first-gap-image-edit-light-1600 |  |  |  |
| first-element-gap-admonition-900 | A | layout-width/v27-first-gap-admonition-edit-light-900 |  |  |  |
| first-element-gap-admonition-460 | A | layout-width/v28-first-gap-admonition-edit-light-460 |  |  |  |
| first-element-gap-admonition-1600 | A | layout-width/v29-first-gap-admonition-edit-light-1600 |  |  |  |
| first-element-gap-properties-900 | A | layout-width/v30-first-gap-properties-edit-light-900 |  |  |  |
| first-element-gap-properties-460 | A | layout-width/v31-first-gap-properties-edit-light-460 |  |  |  |
| first-element-gap-properties-1600 | A | layout-width/v32-first-gap-properties-edit-light-1600 |  |  |  |
| first-element-gap-properties-docs-900 | A | layout-width/v33-first-gap-properties-docs-edit-light-900 |  |  |  |
| first-element-gap-properties-docs-460 | K | layout-width/v34-first-gap-properties-docs-edit-light-460 |  |  |  |
| first-element-gap-properties-docs-1600 | A | layout-width/v35-first-gap-properties-docs-edit-light-1600 |  |  |  |
| first-element-gap-properties-issues-900 | A | layout-width/v36-first-gap-properties-issues-edit-light-900 |  |  |  |
| first-element-gap-properties-issues-460 | A | layout-width/v37-first-gap-properties-issues-edit-light-460 |  |  |  |
| first-element-gap-properties-issues-1600 | A | layout-width/v38-first-gap-properties-issues-edit-light-1600 |  |  |  |
| first-element-gap-empty-900 | K | layout-width/v39-first-gap-empty-edit-dark-900 |  |  |  |
| first-element-gap-empty-460 | A | layout-width/v40-first-gap-empty-edit-dark-460 |  |  |  |
| first-element-gap-empty-1600 | A | layout-width/v41-first-gap-empty-edit-dark-1600 |  |  |  |
| first-element-gap-paragraph-read-900 | A | layout-width/v42-first-gap-paragraph-read-light-900 |  |  |  |
| first-element-gap-h1-read-900 | A | layout-width/v43-first-gap-h1-read-light-900 |  |  |  |
| first-element-gap-h2-read-900 | A | layout-width/v44-first-gap-h2-read-light-900 |  |  |  |
| first-element-gap-h3-read-900 | A | layout-width/v45-first-gap-h3-read-light-900 |  |  |  |
| first-element-gap-table-read-900 | A | layout-width/v46-first-gap-table-read-light-900 |  |  |  |
| first-element-gap-image-read-900 | A | layout-width/v47-first-gap-image-read-light-900 |  |  |  |
| first-element-gap-admonition-read-900 | A | layout-width/v48-first-gap-admonition-read-light-900 |  |  |  |
| first-element-gap-properties-docs-read-900 | A | layout-width/v49-first-gap-properties-docs-read-light-900 |  |  |  |
| first-element-gap-paragraph-360 | A | layout-width/v50-first-gap-paragraph-edit-light-360 |  |  |  |
| first-element-gap-h1-360 | A | layout-width/v51-first-gap-h1-edit-light-360 |  |  |  |
| first-element-gap-table-360 | A | layout-width/v52-first-gap-table-edit-light-360 |  |  |  |
| first-element-gap-properties-360 | A | layout-width/v53-first-gap-properties-edit-light-360 |  |  |  |
| first-element-gap-empty-360 | A | layout-width/v54-first-gap-empty-edit-dark-360 |  |  |  |
| toolbar-rows-expanded-light-900 | K | toolbar-navigation/v06-toolbar-expanded-light-900 |  |  |  |
| toolbar-rows-collapsed-light-900 | K | toolbar-navigation/v07-toolbar-collapsed-light-900 |  |  |  |
| toolbar-rows-expanded-light-360 | K | toolbar-navigation/v08-toolbar-expanded-light-360 |  |  |  |
| toolbar-rows-collapsed-light-360 | K | toolbar-navigation/v09-toolbar-collapsed-light-360 |  |  |  |
| toolbar-rows-expanded-dark-900 | K | toolbar-navigation/v10-toolbar-expanded-dark-900 |  |  |  |
| toolbar-rows-collapsed-dark-900 | K | toolbar-navigation/v11-toolbar-collapsed-dark-900 |  |  |  |
| toolbar-rows-expanded-dark-360 | K | toolbar-navigation/v12-toolbar-expanded-dark-360 |  |  |  |
| toolbar-rows-collapsed-dark-360 | K | toolbar-navigation/v13-toolbar-collapsed-dark-360 |  |  |  |
| toolbar-rows-expanded-white-900 | A | toolbar-navigation/v14-toolbar-expanded-white-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. white matrix: toolbar on white is covered by real-input 38-toolbar-*-white |
| toolbar-rows-collapsed-white-900 | A | toolbar-navigation/v15-toolbar-collapsed-white-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. white matrix |
| toolbar-rows-expanded-white-360 | A | toolbar-navigation/v16-toolbar-expanded-white-360 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. white matrix |
| toolbar-rows-collapsed-white-360 | A | toolbar-navigation/v17-toolbar-collapsed-white-360 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. white matrix |
| toolbar-rows-expanded-cream-900 | K | toolbar-navigation/v18-toolbar-expanded-cream-900 |  |  |  |
| toolbar-rows-collapsed-cream-900 | K | toolbar-navigation/v19-toolbar-collapsed-cream-900 |  |  |  |
| toolbar-rows-expanded-cream-360 | A | toolbar-navigation/v20-toolbar-expanded-cream-360 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. cream at 360 adds no state beyond light-360 and cream-900 |
| toolbar-rows-collapsed-cream-360 | A | toolbar-navigation/v21-toolbar-collapsed-cream-360 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. cream at 360 adds no state beyond light-360 and cream-900 |
| first-element-gap-paragraph-360-collapsed | A | layout-width/v55-first-gap-paragraph-edit-collapsed-light-360 |  |  |  |
| first-element-gap-table-360-collapsed | K | layout-width/v56-first-gap-table-edit-collapsed-light-360 |  |  |  |
| first-element-gap-paragraph-auto-900 | A | layout-width/v57-first-gap-paragraph-edit-auto-light-900 |  |  |  |
| first-element-gap-properties-auto-900 | A | layout-width/v58-first-gap-properties-edit-auto-light-900 |  |  |  |
| first-element-gap-empty-auto-900 | A | layout-width/v59-first-gap-empty-edit-auto-dark-900 |  |  |  |
| first-element-gap-paragraph-full-900 | A | layout-width/v60-first-gap-paragraph-edit-full-light-900 |  |  |  |
| first-element-gap-properties-full-900 | A | layout-width/v61-first-gap-properties-edit-full-light-900 |  |  |  |
| first-element-gap-empty-full-900 | A | layout-width/v62-first-gap-empty-edit-full-dark-900 |  |  |  |
| first-element-gap-paragraph-dark-900 | A | layout-width/v63-first-gap-paragraph-edit-dark-900 |  |  |  |
| first-element-gap-properties-dark-900 | A | layout-width/v64-first-gap-properties-edit-dark-900 |  |  |  |
| first-element-gap-table-dark-900 | A | layout-width/v65-first-gap-table-edit-dark-900 |  |  |  |
| width-modes-light-900 | A | layout-width/v66-width-cycle-light-900 |  |  |  |
| width-modes-light-1600 | A | layout-width/v67-width-cycle-light-1600 |  |  |  |
| width-modes-dark-900 | A | layout-width/v68-width-cycle-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme-independent geometry; the final PNG only shows Margin (≈ width-mode-break-margin) |
| width-modes-dark-1600 | A | layout-width/v69-width-cycle-dark-1600 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme-independent geometry |
| width-modes-cream-900 | A | layout-width/v70-width-cycle-cream-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme-independent geometry |
| width-modes-cream-1600 | A | layout-width/v71-width-cycle-cream-1600 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme-independent geometry |
| width-mode-break-margin-900 | K | layout-width/v72-break-margin-light-900 |  |  |  |
| width-mode-break-auto-900 | K | layout-width/v73-break-auto-light-900 |  |  |  |
| width-mode-break-full-900 | K | layout-width/v74-break-full-light-900 |  |  |  |
| width-mode-break-margin-1600 | K | layout-width/v75-break-margin-light-1600 |  |  |  |
| width-mode-break-auto-1600 | K | layout-width/v76-break-auto-light-1600 |  |  |  |
| width-mode-break-full-1600 | K | layout-width/v77-break-full-light-1600 |  |  |  |
| width-mode-break-margin-460 | K | layout-width/v78-break-margin-light-460 |  |  |  |
| width-mode-break-auto-460 | A | layout-width/v79-break-auto-light-460 |  |  |  |
| width-mode-break-full-460 | A | layout-width/v80-break-full-light-460 |  |  |  |
| width-mode-break-margin-dark-900 | A | layout-width/v81-break-margin-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme repeat of the 900 px margin geometry |
| width-mode-break-auto-dark-900 | K | layout-width/v82-break-auto-dark-900 |  |  |  |
| width-mode-break-full-dark-900 | A | layout-width/v83-break-full-dark-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme repeat of the 900 px full geometry |
| readme-margin-break-cream | K | layout-width/v84-break-auto-readme-cream-1200 |  |  |  |
| toc-column-light-900 | K | toolbar-navigation/v22-toc-margin-light-900 |  |  |  |
| toc-column-light-900-auto | K | toolbar-navigation/v23-toc-auto-light-900 |  |  | PNG identical to Margin: add a wide table to 30-toc so Auto differs |
| toc-column-light-900-full | K | toolbar-navigation/v24-toc-full-light-900 |  |  |  |
| toc-column-dark-1600 | A | toolbar-navigation/v25-toc-margin-dark-1600 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme/width repeat; 1600 px kept in Full |
| toc-column-dark-1600-auto | A | toolbar-navigation/v26-toc-auto-dark-1600 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. PNG identical to dark-1600 margin |
| toc-column-dark-1600-full | K | toolbar-navigation/v27-toc-full-dark-1600 |  |  |  |
| toc-column-light-460 | K | toolbar-navigation/v28-toc-hidden-narrow-light-460 |  |  | renamed: the column is hidden under 760 px by design |
| toc-column-dark-460 | A | toolbar-navigation/v29-toc-hidden-narrow-dark-460 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme repeat of the hidden-column state |
| comment-chips-light-theme | K | review-annotations/v02-comment-todo-chips-light-900 |  |  |  |
| comment-chips-dark-theme | K | review-annotations/v03-comment-todo-chips-dark-900 |  |  |  |
| comment-chips-dark-cream | A | review-annotations/v04-comment-todo-chips-cream-900 |  |  |  |
| figure-anchors-light-theme | K | myst/v17-figure-width-align-anchor-full-light-900 |  |  |  |
| figure-anchors-dark-theme | K | myst/v18-figure-width-align-anchor-full-dark-900 |  |  |  |
| figure-anchors-dark-cream | A | myst/v19-figure-width-align-anchor-full-cream-900 |  |  |  |
| frontmatter-link-details-white-900 | A | frontmatter-schema/v16-links-details-white-900 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme/width matrix of the same link-detail checks |
| frontmatter-link-details-white-460 | K | frontmatter-schema/v17-links-details-white-460 |  |  |  |
| frontmatter-link-details-dark-900 | K | frontmatter-schema/v18-links-details-dark-900 |  |  |  |
| frontmatter-link-details-dark-460 | A | frontmatter-schema/v19-links-details-dark-460 |  |  | was D: its checks have no equal elsewhere, kept assertion-only. theme/width matrix of the same link-detail checks |

## Real window

| Suite / capture | Action | New id | Note |
| --- | --- | --- | --- |
| checkbox/01-reading-unchecked | K | gfm/r01-task-reading-unchecked |  |
| checkbox/02-reading-checked | K | gfm/r02-task-reading-checked |  |
| checkbox/03-edit-mode-unchecked | K | gfm/r03-task-edit-unchecked |  |
| checkbox/04-edit-mode-checked | K | gfm/r04-task-edit-checked |  |
| real-input/08-frontmatter-value-minimal-patch | K | frontmatter-schema/r01-value-minimal-patch |  |
| real-input/09-frontmatter-rename-minimal-patch | K | frontmatter-schema/r02-rename-minimal-patch |  |
| real-input/10-frontmatter-remove-minimal-patch | K | frontmatter-schema/r03-remove-minimal-patch |  |
| real-input/11-frontmatter-title-enter | K | frontmatter-schema/r04-title-enter-saves |  |
| real-input/12-frontmatter-title-multiline | K | frontmatter-schema/r05-title-multiline |  |
| real-input/26-boolean-one-click | K | frontmatter-schema/r06-boolean-one-click |  |
| real-input/27-list-click-edits | K | frontmatter-schema/r07-list-click-edits |  |
| real-input/28-list-enter-adds | K | frontmatter-schema/r08-list-enter-adds |  |
| real-input/29-list-link-warning | K | frontmatter-schema/r09-list-link-warning |  |
| real-input/30-frontmatter-actions-value | K | frontmatter-schema/r10-row-actions-layout |  |
| real-input/31-frontmatter-actions-picker | K | frontmatter-schema/r11-add-field-picker-layout |  |
| real-input/32-required-remove-disabled | K | frontmatter-schema/r12-required-remove-disabled |  |
| real-input/33-custom-key-added | K | frontmatter-schema/r13-custom-key-added |  |
| real-input/34-link-diagnostic-tooltip | K | frontmatter-schema/r14-link-diagnostic-tooltip |  |
| real-input/t41-add-field-position | K | frontmatter-schema/r15-add-field-position |  |
| real-input/t41-custom-key-plain | K | frontmatter-schema/r16-custom-key-plain |  |
| real-input/t41-escape-on-picker | K | frontmatter-schema/r17-escape-on-picker | byte-identical to t41-custom-key-plain: capture with the picker open before Escape |
| frontmatter/description-dark-collapsed-after-refresh-narrow | A | frontmatter-schema/r18-description-collapsed-after-refresh-dark-narrow | byte-identical to -collapsed |
| frontmatter/description-dark-collapsed-after-refresh | A | frontmatter-schema/r19-description-collapsed-after-refresh-dark-wide | byte-identical to -collapsed |
| frontmatter/description-dark-collapsed-narrow | K | frontmatter-schema/r20-description-collapsed-dark-narrow |  |
| frontmatter/description-dark-collapsed | K | frontmatter-schema/r21-description-collapsed-dark-wide |  |
| frontmatter/description-dark-expanded-again-narrow | A | frontmatter-schema/r22-description-expanded-again-dark-narrow | byte-identical to -expanded |
| frontmatter/description-dark-expanded-again | A | frontmatter-schema/r23-description-expanded-again-dark-wide | byte-identical to -expanded |
| frontmatter/description-dark-expanded-narrow | K | frontmatter-schema/r24-description-expanded-dark-narrow | clip to the preview frame (2400 px window makes the table unreadable) |
| frontmatter/description-dark-expanded | K | frontmatter-schema/r25-description-expanded-dark-wide | clip to the preview frame (2400 px window makes the table unreadable) |
| frontmatter/description-white-collapsed-after-refresh-narrow | A | frontmatter-schema/r26-description-collapsed-after-refresh-white-narrow | byte-identical to -collapsed |
| frontmatter/description-white-collapsed-after-refresh | A | frontmatter-schema/r27-description-collapsed-after-refresh-white-wide | byte-identical to -collapsed |
| frontmatter/description-white-collapsed-narrow | K | frontmatter-schema/r28-description-collapsed-white-narrow |  |
| frontmatter/description-white-collapsed | K | frontmatter-schema/r29-description-collapsed-white-wide |  |
| frontmatter/description-white-expanded-again-narrow | A | frontmatter-schema/r30-description-expanded-again-white-narrow | byte-identical to -expanded |
| frontmatter/description-white-expanded-again | A | frontmatter-schema/r31-description-expanded-again-white-wide | byte-identical to -expanded |
| frontmatter/description-white-expanded-narrow | K | frontmatter-schema/r32-description-expanded-white-narrow | clip to the preview frame (2400 px window makes the table unreadable) |
| frontmatter/description-white-expanded | K | frontmatter-schema/r33-description-expanded-white-wide | clip to the preview frame (2400 px window makes the table unreadable) |
| frontmatter/links-dark-hover | K | frontmatter-schema/r34-links-hover-dark |  |
| frontmatter/links-dark-long-ellipsis | K | frontmatter-schema/r35-links-long-ellipsis-dark | clip to the preview frame |
| frontmatter/links-dark-original | K | frontmatter-schema/r36-links-original-dark | clip to the preview frame; at window scale ≈ description-expanded |
| frontmatter/links-dark-saved-target | K | frontmatter-schema/r37-links-saved-target-dark | byte-identical to description-expanded: clip to the changed excerpt |
| frontmatter/links-marker-removed | K | frontmatter-schema/r38-links-marker-removed |  |
| frontmatter/links-white-hover | K | frontmatter-schema/r39-links-hover-white |  |
| frontmatter/links-white-long-ellipsis | K | frontmatter-schema/r40-links-long-ellipsis-white | clip to the preview frame |
| frontmatter/links-white-original | K | frontmatter-schema/r41-links-original-white | clip to the preview frame; at window scale ≈ description-expanded |
| frontmatter/links-white-saved-target | K | frontmatter-schema/r42-links-saved-target-white | byte-identical to description-expanded: clip to the changed excerpt |
| frontmatter/marker-navigation-destination | K | frontmatter-schema/r43-marker-navigation-destination |  |
| real-input/38-toolbar-dark-cream | K | theme-zoom/r01-host-dark-mode-cream |  |
| real-input/38-toolbar-dark-current | K | theme-zoom/r02-host-dark-mode-current |  |
| real-input/38-toolbar-dark-dark | A | theme-zoom/r03-host-dark-mode-dark | forced dark on a dark host looks like current |
| real-input/38-toolbar-dark-white | K | theme-zoom/r04-host-dark-mode-white |  |
| real-input/38-toolbar-light-cream | K | theme-zoom/r05-host-light-mode-cream |  |
| real-input/38-toolbar-light-current | K | theme-zoom/r06-host-light-mode-current |  |
| real-input/38-toolbar-light-dark | K | theme-zoom/r07-host-light-mode-dark |  |
| real-input/38-toolbar-light-white | K | theme-zoom/r08-host-light-mode-white |  |
| real-input/36-title-bar-button | K | toolbar-navigation/r01-title-bar-button |  |
| real-input/38-anchor-disabled | K | toolbar-navigation/r02-anchor-disabled-open-with |  |
| real-input/38-anchor-enabled | K | toolbar-navigation/r03-anchor-enabled-with-editor |  |
| real-input/39-quick-open-beside-preview | K | toolbar-navigation/r04-quick-open-beside-preview |  |
| real-input/01-paragraph-blur-commit | K | block-editing/r01-paragraph-blur-commit |  |
| real-input/02-ctrl-enter-commit | K | block-editing/r02-mod-enter-commit |  |
| real-input/03-arrow-navigation | K | block-editing/r03-arrow-down-into-table |  |
| real-input/07-image-editing | K | block-editing/r04-arrow-up-into-image |  |
| real-input/13-escape-cancels-block | A | block-editing/r05-escape-cancels-block | final frame = initial frame (≈ 02) |
| real-input/15-typing-undo-grouping | A | block-editing/r06-typing-one-undo-step | final frame shows only the restored text |
| real-input/16-undo-stays-open-with | A | block-editing/r07-undo-stays-in-editor-open-with |  |
| real-input/16-undo-stays-side | K | block-editing/r08-undo-stays-in-editor |  |
| real-input/17-enter-continues-list | K | block-editing/r09-enter-continues-list |  |
| real-input/18-tab-indents | K | block-editing/r10-tab-indents |  |
| real-input/20-caret-at-click | K | block-editing/r11-caret-at-click |  |
| real-input/21-edit-hover | K | block-editing/r12-edit-hover |  |
| real-input/22-editor-frame-and-buttons | K | block-editing/r13-editor-frame-and-buttons |  |
| real-input/23-edit-mode-no-reflow | K | block-editing/r14-edit-mode-no-reflow |  |
| real-input/24-start-writing-open | K | block-editing/r15-start-writing-open |  |
| real-input/25-block-inserted | K | block-editing/r16-insert-point-adds-block |  |
| real-input/25b-insert-after-figure-with-newline | K | block-editing/r17-insert-after-final-figure |  |
| real-input/25b-insert-after-figure-without-newline | A | block-editing/r18-insert-after-final-figure-no-eol | PNG ≈ with-newline |
| real-input/32-save-keeps-list-in-place | K | block-editing/r19-save-keeps-list-in-place |  |
| real-input/block-selection-01-shift-click | K | block-editing/r20-shift-click-selects-blocks |  |
| real-input/move-keys-01-alt-down | K | block-editing/r21-alt-down-moves-block |  |
| real-input/move-keys-02-chord | K | block-editing/r22-move-chord-keeps-editor |  |
| real-input/move-selection-01-alt-arrows | K | block-editing/r23-alt-arrows-move-selection |  |
| real-input/p11-slash-no-command | K | palette-slash/r01-slash-no-command |  |
| real-input/p11-slash-open | K | palette-slash/r02-slash-open |  |
| real-input/t20-shortcuts | K | palette-slash/r03-shortcuts-bold-todo | capture after Ctrl+/ (TODO wrapped) instead of after undo (≈ t21/t22) |
| real-input/t21-palette | K | palette-slash/r04-palette-bold-heading | capture with the language list open (end state ≈ t20/t22) |
| real-input/t22-link-panel | K | palette-slash/r05-link-panel | capture with the link panel open |
| real-input/t25-alert-dropdown | K | palette-slash/r06-alert-dropdown |  |
| real-input/t32-figure-editor | K | palette-slash/r07-figure-editor-form |  |
| real-input/04-table-cell-enter | K | table-editing/r01-cell-enter-saves |  |
| real-input/06-table-padded-edit | K | table-editing/r02-padded-table-minimal-diff |  |
| real-input/07-table-compact-edit | A | table-editing/r03-compact-table-minimal-diff | PNG ≈ 06 (same tables, one word apart) |
| real-input/14-escape-cancels-table-cell | A | table-editing/r04-escape-cancels-cell | final frame = initial frame |
| real-input/24-table-tab | K | table-editing/r05-tab-adds-row |  |
| real-input/25-table-toolbar | K | table-editing/r06-cell-bar-in-flow |  |
| real-input/33-save-keeps-table-in-place | K | table-editing/r07-save-keeps-table-in-place |  |
| real-input/t35-table-cell-bold | K | table-editing/r08-cell-bold-shortcut |  |
| real-input/comment-block-edit | K | review-annotations/r01-comment-block-opens-editor |  |
| real-input/comments-01-popover | K | review-annotations/r02-review-thread-popover |  |
| real-input/05-open-with-editor | K | lifecycle-sync/r01-open-with-editor |  |
| real-input/19-preview-keeps-markdown | K | lifecycle-sync/r02-preview-keeps-markdown |  |
| real-input/26-focus-change-still | K | lifecycle-sync/r03-focus-change-keeps-scroll |  |
| real-input/27-hidden-preview-catches-up | K | lifecycle-sync/r04-hidden-preview-catches-up |  |
| real-input/30-properties-in-place | K | lifecycle-sync/r05-linked-file-patched-in-place |  |
| real-input/34-content-patched | K | lifecycle-sync/r06-content-patched-in-place |  |
| real-input/35-status-two-lines | K | lifecycle-sync/r07-status-page-missing-source |  |
| real-input/38-edit-mode-remembered | K | lifecycle-sync/r08-edit-mode-remembered |  |
| real-input/43-pending-overlay | K | lifecycle-sync/r09-pending-overlay |  |
| scroll/01-solo-bottom | K | lifecycle-sync/r10-scroll-solo-bottom |  |
| scroll/02-return-top | K | lifecycle-sync/r11-scroll-return-top |  |
| scroll/03-paired-aligned-bottom | K | lifecycle-sync/r12-scroll-paired-bottom |  |
| scroll/04-preview-independent-bottom | K | lifecycle-sync/r13-scroll-preview-independent |  |
| scroll/05-source-independent-bottom | K | lifecycle-sync/r14-scroll-source-independent |  |
| scroll/06-keyboard-return | K | lifecycle-sync/r15-scroll-keyboard-return |  |
| reload/01-before-window-reload | K | lifecycle-sync/r16-before-window-reload |  |
| reload/02-after-window-reload | K | lifecycle-sync/r17-after-window-reload |  |
| reload/03-after-close-reopen | K | lifecycle-sync/r18-after-close-reopen |  |
