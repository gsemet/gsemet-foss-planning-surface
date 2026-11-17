# README as a short showcase, details in docs/

User request (2026-10-25). The README (454 lines, 14 sections) became a feature catalogue.

## Decisions (user interview)

- README = short showcase. It shows clearly what the extension brings, why to use it, how
  beautiful and elegant it is, and the WYSIWYG editing that others do not offer (MyST, grids…).
- Put the differentiators forward: elegant themes, auto-margin mode that favours reading wide
  tables and text, diff since the last commit, integrated Mermaid and PlantUML, and the others
  found by the research below.
- Detailed feature documentation and settings move to Markdown files under `docs/` in the
  repository (no Read the Docs site for now). Existing engineering docs in `docs/` stay.
- Screenshots only (demo videos come later, see backlog P4 record-demo-video).
- Screenshots are produced by automatic scenarios in the existing screenshot suite, on a
  polished demo document, so they stay reproducible and current.
- Screenshot theme: Cream only (plus at most one small row showing the three themes).
- Comparison: research in detail which current features are not supported by other Markdown
  extensions, including the recent changes to VS Code's built-in Markdown editor and preview.
  Show the result in the README only where verified, with the date of the check.
