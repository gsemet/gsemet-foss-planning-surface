# UX-08 — Raw Markdown, code, and tables are edited in a proportional font

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed |
| Area | Inline block editing |
| Evidence | [adm3-3.jpg](../../evidence/adm3-3.jpg) (code fence), [adm3-8.jpg](../../evidence/adm3-8.jpg) (table inside an admonition) |

## Observed

The block textarea inherits the preview body font. Code fences lose their indentation alignment,
pipe tables lose column alignment (`| first    | second   |` no longer lines up with its header),
and directive options (`:class: tip`) look like prose. There is no syntax colouring.

## Expected

Raw source is edited in the editor font (`--vscode-editor-font-family`, size and tab size), like
the source editor next to it.

## Where it comes from

`src/preview/previewStyles.ts`, `.sphinx-preview-block-editor` rules (from L370): no
`font-family` override for the textarea.

## Suggested direction

Use `var(--vscode-editor-font-family)` and `tab-size` for `.sphinx-preview-block-editor
textarea`. A lightweight Markdown highlighter is optional.

## Done when

A code fence or table opened inline keeps its column alignment.
