# QA-04 — What this campaign covered, and what it did not

This note scopes the findings: absence of a finding in an area below means "not tested yet", not
"works".

## Covered (real VS Code window, real mouse and keyboard)

| Use case | Corpus | Result |
| --- | --- | --- |
| Open side preview from the palette | book chapter 02 | Works; discoverability gap (UX-30) |
| Read a long chapter, wheel-scroll the preview, editor follows | book chapter 02 | Works; small jump on owner switch (UX-29) |
| Type in the source with the preview open | book chapter 02 | Works; full reload per key (UX-28) |
| Edit mode: paragraph, heading, admonition (title → whole directive), code fence, blockquote, list, table cell | fixtures 02, 04, chapter 02 | Mapping correct; editing defects UX-01…UX-11 |
| Table cell edit, Tab, Escape, click-away | fixture 04 | UX-12, UX-13, UX-14 |
| Open With editor: edit, Cmd+S, Cmd+Z, write a new section | fixture 01 | Cmd+S works; UX-03, UX-10 |
| OKF properties table, schema resolution, link resolution, link click to code with marker line | okfreq-examples | Marker navigation works; UX-22, UX-23, UX-25 |
| Frontmatter edit: text, boolean, list, add field, remove required field | okfreq-examples | UX-16…UX-21 |
| Live settings change (`frontmatter.projectRoot`) | okfreq-examples | Applied without reload (good) |

Console: no webview errors or exceptions were logged during the session (only Electron's
"Unrecognized feature: 'local-network-access'" warning).

## Not covered yet (planned for the complementary report)

- Mermaid, PlantUML, math: rendering while typing, inline editing of diagrams and equations.
- Theme toggle (toolbar and VS Code theme), narrow preview widths, zoom, find widget (Cmd+F).
- Reload Window and close/reopen restoration; file rename/delete/external modification while
  previewing or while an inline editor is open.
- CRLF documents, very large documents (chapter 08, 107 KB) typing latency, empty documents.
- Wikilinks and relative links in the Obsidian vault copy; images and figures with missing files.
- Untrusted workspace and standalone files outside the workspace.
- Keyboard-only navigation between blocks (arrow keys at block edges) and accessibility.
- Coexistence with the built-in Markdown preview and the built-in Markdown Editor (1.141).
- `strictAdditionalProperties`, invalid YAML frontmatter, enum dropdowns, nested objects.
