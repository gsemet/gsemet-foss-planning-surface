# Visual Review

Run status: **failed**

Machine checks: [MACHINE-CHECKS.md](MACHINE-CHECKS.md) (failing applicable geometry checks)

Revision: `24d5ab9520aea0e6084600f88589ee4241cac9af`

See [run manifest](run-manifest.json) for command, dirty status and assertions.

Static generated HTML with mock VS Code host; save messages do not rerender the document. Native browser popups are not captured.

## 01 Documents and admonitions

1. **passed** [handbook-narrow-top](handbook-narrow-top.png) [notes](handbook-narrow-top.txt)
   Narrow side-panel width, the width most users actually preview at. Checks gutters and that admonition padding does not eat the usable column.
2. **failed** [handbook-narrow-table](handbook-narrow-table.png) [notes](handbook-narrow-table.txt)
   The service level table at panel width, captured after internal scrolling to its far-right Audit column. The page itself must not widen.
   Failure: sticky heading overlaps the reserved toolbar row
3. **passed** [handbook-dark-top](handbook-dark-top.png) [notes](handbook-dark-top.txt)
   Top of a long mixed document on a dark theme. Checks the h1 rule, the first note admonition, and that the paragraph following it returns to body colour.
4. **failed** [handbook-dark-third](handbook-dark-third.png) [notes](handbook-dark-third.txt)
   The first code landmark in the same document. Mid-scroll rendering of an ordered list, a fenced Python block, and a titled warning admonition.
   Failure: sticky heading overlaps the reserved toolbar row
5. **failed** [handbook-dark-bottom](handbook-dark-bottom.png) [notes](handbook-dark-bottom.txt)
   Bottom of the document. The trailing padding must keep the last paragraph reachable and visible rather than pinned against the viewport edge.
   Failure: sticky heading overlaps the reserved toolbar row
6. **passed** [handbook-light-top](handbook-light-top.png) [notes](handbook-light-top.txt)
   Same opening on a light theme. This is where a near-white admonition background on a white page would be invisible.
7. **failed** [handbook-light-failures](handbook-light-failures.png) [notes](handbook-light-failures.txt)
   The run of danger, caution, error, hint, seealso and attention blocks on a light theme. Every accent must be distinguishable from its neighbours.
   Failure: sticky heading overlaps the reserved toolbar row
8. **passed** [handbook-forced-white](handbook-forced-white.png) [notes](handbook-forced-white.txt)
   Forced white preview while the VS Code host remains dark. The page, text and note panel must all use the light palette.
9. **passed** [admonitions-narrow-full](admonitions-narrow-full.png) [notes](admonitions-narrow-full.txt)
   The same gallery at panel width, to catch wrapping inside tinted panels.
10. **passed** [admonitions-dark-full](admonitions-dark-full.png) [notes](admonitions-dark-full.txt)
   Full-page dark capture of every admonition variant. The reference for colour bleed: each paragraph between blocks must match the baseline paragraph at the top.
11. **failed** [admonitions-dark-titled](admonitions-dark-titled.png) [notes](admonitions-dark-titled.txt)
   Titled admonitions close up. Exactly one title line per block; two means the default heading is being printed above the author's title.
   Failure: sticky heading overlaps the reserved toolbar row
12. **failed** [admonitions-dark-nested](admonitions-dark-nested.png) [notes](admonitions-dark-nested.txt)
   An admonition containing a list, a code block, a table and a blockquote. Nested elements keep their own spacing and the last child has no trailing margin.
   Failure: sticky heading overlaps the reserved toolbar row
13. **passed** [admonitions-light-full](admonitions-light-full.png) [notes](admonitions-light-full.txt)
   Full-page light capture of every admonition variant, including the accent used for a generic admonition carrying an author-supplied class.
14. **passed** [chapter-dark-top](chapter-dark-top.png) [notes](chapter-dark-top.txt)
   Opening of a realistic chapter: note, prose, then a loaded figure with caption text. The caption has no generated figure number; inspect its separation from body text.
15. **failed** [chapter-figure-dark](chapter-figure-dark.png) [notes](chapter-figure-dark.txt)
   Close-up of a chapter figure referenced from a sibling external-img directory. The SVG must load and the caption must remain visible beneath it.
   Failure: sticky heading overlaps the reserved toolbar row
16. **failed** [chapter-dark-quarter](chapter-dark-quarter.png) [notes](chapter-dark-quarter.txt)
   The important-block landmark and following body-colour paragraph.
   Failure: sticky heading overlaps the reserved toolbar row
17. **failed** [chapter-dark-half](chapter-dark-half.png) [notes](chapter-dark-half.txt)
   The typeset display-equation landmark with surrounding shift-change content.
   Failure: sticky heading overlaps the reserved toolbar row
18. **failed** [chapter-dark-three-quarters](chapter-dark-three-quarters.png) [notes](chapter-dark-three-quarters.txt)
   Incident patterns landmark with back-to-back admonitions.
   Failure: sticky heading overlaps the reserved toolbar row
19. **failed** [chapter-dark-bottom](chapter-dark-bottom.png) [notes](chapter-dark-bottom.txt)
   True end of the chapter. The final paragraph names itself, so a screenshot that does not show it means the scroll stopped short.
   Failure: sticky heading overlaps the reserved toolbar row
20. **passed** [chapter-max-width-dark-full](chapter-max-width-dark-full.png) [notes](chapter-max-width-dark-full.txt)
   The full long chapter in a 1600px dark preview. Its content column stays centered at the configured 960px maximum.
21. **passed** [chapter-light-top](chapter-light-top.png) [notes](chapter-light-top.txt)
   Same chapter opening on a light theme, for side-by-side contrast review.
22. **passed** [chapter-max-width-light-full](chapter-max-width-light-full.png) [notes](chapter-max-width-light-full.txt)
   The full long chapter in a 1600px light preview. The readable column stays centered at the configured 960px maximum.
23. **passed** [nested-list-typing-dark](nested-list-typing-dark.png) [notes](nested-list-typing-dark.txt)
   Edit the user's nested plugin list with six literal spaces, Enter, and a new list item. Check exact text, caret, focus, and autosave without period substitution or blocked newlines.
24. **passed** [nested-list-typing-light](nested-list-typing-light.png) [notes](nested-list-typing-light.txt)
   Edit the user's nested plugin list with six literal spaces, Enter, and a new list item. Check exact text, caret, focus, and autosave without period substitution or blocked newlines.
## 02 Code and unresolved constructs

25. **passed** [unresolved-dark-full](unresolved-dark-full.png) [notes](unresolved-dark-full.txt)
   Citations, citation groups, build-only directives and both Mermaid syntaxes. Citation groups stay inline and both diagrams render as SVG.
26. **passed** [unresolved-light-full](unresolved-light-full.png) [notes](unresolved-light-full.txt)
   The same constructs on a light theme, including both rendered Mermaid diagrams.
27. **passed** [code-dark-table-narrow](code-dark-table-narrow.png) [notes](code-dark-table-narrow.txt)
   The sixteen-column table at 640 px, whole page, not scrolled. Short identifiers such as nw-02 and North stay on one line, and a shadow on the overflow edge shows that the table scrolls.
28. **passed** [code-dark-top](code-dark-top.png) [notes](code-dark-top.txt)
   A long TypeScript block. Checks monospace selection, padding and radius.
29. **failed** [code-dark-table](code-dark-table.png) [notes](code-dark-table.txt)
   A sixteen-column table deliberately wider than the preview. The final capture is scrolled to its FAR-RIGHT-ACCESS column without a horizontal page scrollbar.
   Failure: sticky heading overlaps the reserved toolbar row
30. **passed** [code-light-table-narrow](code-light-table-narrow.png) [notes](code-light-table-narrow.txt)
   The sixteen-column table at 640 px on a light theme, whole page, not scrolled. Short identifiers such as nw-02 and North stay on one line, and a shadow on the overflow edge shows that the table scrolls.
31. **passed** [code-light-full](code-light-full.png) [notes](code-light-full.txt)
   Whole document on a light theme: code, wide table, four-level nested list and definition list in one frame.
32. **failed** [syntax-narrow-python](syntax-narrow-python.png) [notes](syntax-narrow-python.txt)
   Python in a narrow pane, captured at the code block's far-right scroll position. Long signatures scroll internally without widening the page.
   Failure: sticky heading overlaps the reserved toolbar row
33. **failed** [syntax-dark-markdown](syntax-dark-markdown.png) [notes](syntax-dark-markdown.txt)
   A quadruple-backtick Markdown fence on a dark theme. The inner triple fences, the table and the link must appear as literal highlighted Markdown, not as rendered content that escaped the block.
   Failure: sticky heading overlaps the reserved toolbar row
34. **failed** [syntax-dark-rust](syntax-dark-rust.png) [notes](syntax-dark-rust.txt)
   Rust on a dark theme. Keywords, the attribute macro, the doc comment, the string literals and the numeric literal must each take a distinct colour.
   Failure: sticky heading overlaps the reserved toolbar row
35. **failed** [syntax-dark-python](syntax-dark-python.png) [notes](syntax-dark-python.txt)
   Python on a dark theme. Decorator, docstring, f-string and trailing comment are the tokens most likely to be mis-scoped by a highlighter.
   Failure: sticky heading overlaps the reserved toolbar row
36. **failed** [diff-dark-preview](diff-dark-preview.png) [notes](diff-dark-preview.txt)
   A fenced diff block in readonly preview on a dark theme. Added and removed lines must use distinct full-width treatments while the patch markers remain visible.
   Failure: sticky heading overlaps the reserved toolbar row
37. **failed** [syntax-light-rust](syntax-light-rust.png) [notes](syntax-light-rust.txt)
   The same Rust block on a light theme. Token colours drawn from the chart palette must stay legible against the pale code-block background.
   Failure: sticky heading overlaps the reserved toolbar row
38. **failed** [syntax-light-shell](diff-light-preview.png) [notes](diff-light-preview.txt) (alias of diff-light-preview; assertions retained)
   Shell, JSON and diff blocks on a light theme, followed by a fence labelled with an unregistered grammar that must degrade to plain monospace text.
   Failure: sticky heading overlaps the reserved toolbar row
39. **failed** [diff-light-preview](diff-light-preview.png) [notes](diff-light-preview.txt)
   A fenced diff block in readonly preview on a light theme. Green and red line treatments must remain legible against the code panel.
   Failure: sticky heading overlaps the reserved toolbar row
## 02 Context tag containers

40. **passed** [context-tags-dark-narrow](context-tags-dark-narrow.png) [notes](context-tags-dark-narrow.txt)
   Narrow dark side-panel capture of the exact adjacent YAML form plus simple and snake_case tags. The panels must wrap without widening the page or hiding the YAML code.
41. **passed** [context-tags-dark-wide](context-tags-dark-wide.png) [notes](context-tags-dark-wide.txt)
   Desktop dark capture of the exact adjacent YAML context form plus simple and snake_case tags. Literal titles, Markdown body, mapped ranges, and YAML code must remain visible.
42. **passed** [context-tags-light-narrow](context-tags-light-narrow.png) [notes](context-tags-light-narrow.txt)
   Narrow light side-panel capture of the exact adjacent YAML form plus simple and snake_case tags. The panels must wrap without widening the page or hiding the YAML code.
43. **passed** [context-tags-light-wide](context-tags-light-wide.png) [notes](context-tags-light-wide.txt)
   Desktop light capture of the exact adjacent YAML context form plus simple and snake_case tags. Literal titles, Markdown body, mapped ranges, and YAML code must remain visible.
## 03 Diagrams

44. **passed** [mermaid-map-dark](mermaid-map-dark.png) [notes](mermaid-map-dark.txt)
   The OKF knowledge-base map in the dark preview.
45. **passed** [mermaid-map-fallback](mermaid-map-fallback.png) [notes](mermaid-map-fallback.txt)
   The OKF knowledge-base map without host color variables.
46. **passed** [mermaid-map-light](mermaid-map-light.png) [notes](mermaid-map-light.txt)
   The OKF knowledge-base map in the light preview.
47. **passed** [plantuml-success-dark](plantuml-success-dark.png) [notes](plantuml-success-dark.txt)
   A successful PlantUML render on a dark preview background when plantuml is available on PATH.
48. **passed** [plantuml-success-light](plantuml-success-light.png) [notes](plantuml-success-light.txt)
   A successful PlantUML render on a white preview background when plantuml is available on PATH.
49. **passed** [plantuml-unconfigured](plantuml-unconfigured.png) [notes](plantuml-unconfigured.txt)
   Intentionally unconfigured PlantUML shows the JAR-path guidance and expandable source, not a successful diagram.
50. **passed** [plantuml-executable-not-found](plantuml-executable-not-found.png) [notes](plantuml-executable-not-found.txt)
   A missing PlantUML executable shows an actionable settings message and preserves the source.
## 04 Properties and validation

51. **passed** [frontmatter-dark](frontmatter-dark.png) [notes](frontmatter-dark.txt)
   Plain two-column frontmatter table on the dark theme: lean, no outer frame or cell backgrounds, grid separators retained and values readable on the editor background.
52. **passed** [frontmatter-light](frontmatter-light.png) [notes](frontmatter-light.txt)
   Plain two-column frontmatter table on the light theme: transparent cells keep body-text contrast against the white page.
53. **passed** [frontmatter-forced-white](frontmatter-forced-white.png) [notes](frontmatter-forced-white.txt)
   YAML frontmatter rendered at the top of the document. Metadata and inline code use readable link-blue text against the soft white-mode code background.
54. **passed** [okf-schema-narrow](frontmatter-scroll-feedback.png) [notes](frontmatter-scroll-feedback.txt) (alias of frontmatter-scroll-feedback; assertions retained)
   The OKF schema table at narrow side-panel width. The description column is hidden so the name and value columns remain readable without horizontal crowding.
55. **passed** [preview-toolbar-dark](okf-schema-dark.png) [notes](okf-schema-dark.txt) (alias of okf-schema-dark; assertions retained)
   Four preview actions share one compact toolbar chip without covering the schema properties table.
56. **passed** [okf-schema-dark](okf-schema-dark.png) [notes](okf-schema-dark.txt)
   OKF schema table on the dark theme itself (preview mode auto): lean transparent cells with grid separators, description text smaller than name/value, and title badge with readable contrast.
57. **passed** [okf-schema-table](okf-schema-table.png) [notes](okf-schema-table.txt)
   OKF frontmatter with a matching schema. The three-column properties table shows name, value, and the schema description of each field.
58. **passed** [okf-schema-missing-required-dark](okf-schema-missing-required-dark.png) [notes](okf-schema-missing-required-dark.txt)
   An OKF schema table with missing required fields. The descriptions remain plain prose, and a red summary below the table names every missing field.
59. **passed** [okf-schema-missing-required-light](okf-schema-missing-required-light.png) [notes](okf-schema-missing-required-light.txt)
   The same incomplete OKF schema in a light theme, showing the red missing-required summary below the last property row.
60. **passed** [schema-validation-error-dark](schema-validation-error-dark.png) [notes](schema-validation-error-dark.txt)
   An unsupported schema keyword produces a red diagnostic across all three table columns.
61. **passed** [schema-validation-error-narrow](schema-validation-error-narrow.png) [notes](schema-validation-error-narrow.txt)
   The full-width schema diagnostic wraps on a narrow viewport without overflowing its cell.
62. **passed** [schema-validation-error-light](schema-validation-error-light.png) [notes](schema-validation-error-light.txt)
   The schema-compilation failure uses the same full-width red treatment in a light theme.
63. **passed** [standalone-frontmatter-dark](standalone-frontmatter-dark.png) [notes](standalone-frontmatter-dark.txt)
   Standalone SKILL.md metadata on a dark theme. Generic fields stay in two columns, and nested object values appear as YAML code rather than JSON.
64. **passed** [standalone-frontmatter-light](standalone-frontmatter-light.png) [notes](standalone-frontmatter-light.txt)
   The same standalone SKILL.md metadata on a light theme, with the nested YAML code block and generic two-column table remaining legible.
## 05 Link details and loading

65. **passed** [frontmatter-link-details-dark-460](frontmatter-link-details-dark-460.png) [notes](frontmatter-link-details-dark-460.txt)
   Resolved links show fresh target metadata and a clipped long excerpt. Beta intentionally lacks the optional description. Inspect excerpt ellipsis, Alpha's line 9 label and the visible Refresh tooltip without page overflow; native link title metadata is DOM-asserted, not visible in the PNG.
66. **passed** [frontmatter-links-loading](frontmatter-links-loading.png) [notes](frontmatter-links-loading.txt)
   The properties table while filesystem-backed links are being inspected. Each linked value keeps its text and shows a small spinner immediately after it.
67. **passed** [frontmatter-links-loaded](frontmatter-links-loaded.png) [notes](frontmatter-links-loaded.txt)
   The same properties table after deferred link inspection. The spinners are gone and both resolved values are rendered as links.
68. **passed** [frontmatter-link-details-dark-900](frontmatter-link-details-dark-900.png) [notes](frontmatter-link-details-dark-900.txt)
   Resolved links show fresh target metadata and a clipped long excerpt. Beta intentionally lacks the optional description. Inspect excerpt ellipsis, Alpha's line 9 label and the visible Refresh tooltip without page overflow; native link title metadata is DOM-asserted, not visible in the PNG.
69. **passed** [frontmatter-link-details-white-460](frontmatter-link-details-white-460.png) [notes](frontmatter-link-details-white-460.txt)
   Resolved links show fresh target metadata and a clipped long excerpt. Beta intentionally lacks the optional description. Inspect excerpt ellipsis, Alpha's line 9 label and the visible Refresh tooltip without page overflow; native link title metadata is DOM-asserted, not visible in the PNG.
70. **passed** [frontmatter-link-details-white-900](frontmatter-link-details-white-900.png) [notes](frontmatter-link-details-white-900.txt)
   Resolved links show fresh target metadata and a clipped long excerpt. Beta intentionally lacks the optional description. Inspect excerpt ellipsis, Alpha's line 9 label and the visible Refresh tooltip without page overflow; native link title metadata is DOM-asserted, not visible in the PNG.
## 06 Editing

71. **passed** [edit-affordances-hover-and-open](edit-affordances-hover-and-open.png) [notes](edit-affordances-hover-and-open.txt)
   Edit mode on. A hovered list is outlined with a dashed line (a second PNG, -hover, is kept); the final frame shows a paragraph editor with its frame, line-range hint, Done and Revert.
72. **failed** [preview-edit-activation-scroll-wide](preview-edit-activation-scroll-wide.png) [notes](preview-edit-activation-scroll-wide.txt)
   A centered paragraph keeps its scroll position when its editor loads asynchronously, without transient jumps or delayed anchor corrections.
   Failure: sticky heading overlaps the reserved toolbar row
73. **failed** [math-edit-offline-dark](math-edit-offline-dark.png) [notes](math-edit-offline-dark.txt)
   KaTeX rendering is checked before interaction. The final frame shows the original $$ Markdown in the focused equation editor, not the pre-edit typeset equation.
   Failure: sticky heading overlaps the reserved toolbar row
74. **failed** [preview-edit-activation-scroll-narrow](preview-edit-activation-scroll-narrow.png) [notes](preview-edit-activation-scroll-narrow.txt)
   Opening a centered paragraph editor in a narrow preview preserves scroll throughout source loading and layout stabilization.
   Failure: sticky heading overlaps the reserved toolbar row
75. **failed** [math-edit-offline-light-narrow](math-edit-offline-light-narrow.png) [notes](math-edit-offline-light-narrow.txt)
   Offline KaTeX fonts are checked before interaction. The final narrow frame shows the original $$ Markdown editor after activation without a scroll jump.
   Failure: sticky heading overlaps the reserved toolbar row
76. **failed** [diff-dark-edit](diff-dark-edit.png) [notes](diff-dark-edit.txt)
   The same diff block in page-wide edit mode on a dark theme. Rendered line styling must remain visible while the preview is editable.
   Failure: sticky heading overlaps the reserved toolbar row
77. **failed** [diff-light-edit](diff-light-edit.png) [notes](diff-light-edit.txt)
   The same diff block in page-wide edit mode on a light theme. The rendered preview must retain its green and red line treatments.
   Failure: sticky heading overlaps the reserved toolbar row
78. **failed** [edit-table-wrapped-dark-460](edit-table-wrapped-dark-460.png) [notes](edit-table-wrapped-dark-460.txt)
   Long table-cell source wraps without overlapping rendered text or changing cell dimensions.
   Failure: sticky heading overlaps the reserved toolbar row
79. **passed** [frontmatter-scroll-feedback-edit](frontmatter-scroll-feedback-edit.png) [notes](frontmatter-scroll-feedback-edit.txt)
   Edit mode remains on after three scroll cycles; the field editor is closed and the final capture is at the top.
80. **passed** [edit-mode-dark](edit-paragraph-dark.png) [notes](edit-paragraph-dark.txt) (alias of edit-paragraph-dark; assertions retained)
   Whole-page edit mode preserves source layout while a focused paragraph editor shows its caret.
81. **passed** [edit-paragraph-dark](edit-paragraph-dark.png) [notes](edit-paragraph-dark.txt)
   Clicking a body paragraph opens its source editor while retaining the hard source lines.
82. **passed** [edit-admonition-dark](edit-admonition-dark.png) [notes](edit-admonition-dark.txt)
   Clicking an admonition title opens the complete mapped directive source.
83. **failed** [edit-table-cell-dark](edit-table-wrapped-dark-900.png) [notes](edit-table-wrapped-dark-900.txt) (alias of edit-table-wrapped-dark-900; assertions retained)
   The selected table cell is edited in place with a row and column action bar above the table.
   Failure: sticky heading overlaps the reserved toolbar row
84. **failed** [edit-table-wrapped-dark-900](edit-table-wrapped-dark-900.png) [notes](edit-table-wrapped-dark-900.txt)
   Long table-cell source wraps without overlapping rendered text or changing cell dimensions.
   Failure: sticky heading overlaps the reserved toolbar row
85. **passed** [edit-frontmatter-key-dark](edit-frontmatter-key-dark.png) [notes](edit-frontmatter-key-dark.txt)
   The expanded key suggestions show an unused property from the matching JSON Schema.
86. **passed** [edit-frontmatter-value-dark](edit-frontmatter-value-dark.png) [notes](edit-frontmatter-value-dark.txt)
   The final frame shows only the active status enum control, with the Add-field picker closed. Add and draft-save messages are checked; a simulated mock-host rejection re-enables Escape cancellation before reopening the original active value. No real persistence is claimed.
87. **passed** [edit-frontmatter-list-dark](edit-frontmatter-list-dark.png) [notes](edit-frontmatter-list-dark.txt)
   List reorder, addition and removal are exercised; the final set-as-null save is pending with the editor disabled. The mock host does not persist or rerender values.
88. **failed** [edit-table-wrapped-light-460](edit-table-wrapped-light-460.png) [notes](edit-table-wrapped-light-460.txt)
   Long table-cell source wraps without overlapping rendered text or changing cell dimensions.
   Failure: sticky heading overlaps the reserved toolbar row
89. **failed** [edit-table-wrapped-light-900](edit-table-wrapped-light-900.png) [notes](edit-table-wrapped-light-900.txt)
   Long table-cell source wraps without overlapping rendered text or changing cell dimensions.
   Failure: sticky heading overlaps the reserved toolbar row
90. **passed** [edit-frontmatter-list-light](edit-frontmatter-list-light.png) [notes](edit-frontmatter-list-light.txt)
   Light-theme list reorder/add/remove checks end with a pending set-as-null save and disabled editor; the mock host does not persist or rerender values.
91. **passed** [edit-frontmatter-boolean-dark](edit-frontmatter-boolean-dark.png) [notes](edit-frontmatter-boolean-dark.txt)
   The checkbox starts checked, is clicked once, and is captured unchecked after posting a false save to the mock host.
92. **passed** [edit-list-narrow](edit-list-narrow.png) [notes](edit-list-narrow.txt)
   Clicking one item opens the complete list, including a wrapped continuation line, in the editor.
## 07 Scrolling and sticky headings

93. **failed** [preview-sticky-headings-1](preview-sticky-headings-1.png) [notes](preview-sticky-headings-1.txt)
   Depth one keeps only the current Markdown heading visible at the top of the preview.
   Failure: rightmost preview button is covered or overlaps the sticky heading text row
   Failure: sticky heading top 0.0px overlaps toolbar bottom 50.0px
   Failure: sticky heading overlaps the reserved toolbar row
94. **failed** [preview-sticky-headings-2](preview-sticky-headings-2.png) [notes](preview-sticky-headings-2.txt)
   Depth two keeps the current heading and its parent visible at the top of the preview.
   Failure: rightmost preview button is covered or overlaps the sticky heading text row
   Failure: sticky heading top 0.0px overlaps toolbar bottom 50.0px
   Failure: sticky heading overlaps the reserved toolbar row
95. **failed** [preview-sticky-headings-3](preview-sticky-headings-3.png) [notes](preview-sticky-headings-3.txt)
   Depth three keeps the current heading and two parent levels visible in the preview.
   Failure: rightmost preview button is covered or overlaps the sticky heading text row
   Failure: sticky heading top 0.0px overlaps toolbar bottom 50.0px
   Failure: sticky heading overlaps the reserved toolbar row
96. **failed** [preview-sticky-headings-3-light-narrow](preview-sticky-headings-3-light-narrow.png) [notes](preview-sticky-headings-3-light-narrow.txt)
   Depth three remains legible in a narrow preview at the normal text size.
   Failure: rightmost preview button is covered or overlaps the sticky heading text row
   Failure: sticky heading top 0.0px overlaps toolbar bottom 50.0px
   Failure: sticky heading overlaps the reserved toolbar row
97. **passed** [frontmatter-scroll-feedback](frontmatter-scroll-feedback.png) [notes](frontmatter-scroll-feedback.txt)
   Three scroll cycles reach both ends; the final capture returns to the top of the tall frontmatter table.
98. **failed** [preview-sticky-headings-natural-growth](preview-sticky-headings-natural-growth.png) [notes](preview-sticky-headings-natural-growth.txt)
   Long, wrapped heading ancestry grows the sticky band to its rendered content height.
   Failure: rightmost preview button is covered or overlaps the sticky heading text row
   Failure: sticky heading top 0.0px overlaps toolbar bottom 50.0px
   Failure: sticky heading overlaps the reserved toolbar row
