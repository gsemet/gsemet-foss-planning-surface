# Task: collapse button for the frontmatter properties table

## Files (start here)

- The frontmatter table render: `src/core/frontmatter` (properties table HTML) and its header.
- The Description column collapse, to reuse its icon, style and toggle pattern: search `src/page`
  and `src/core/preview` for the description column toggle.
- Page state that survives a re-render but not a reload: see how `src/page/runtime.ts` and
  `src/page/features/pageRuntime.ts` keep per-document page state across content patches.

## Change

A toggle button in the frontmatter header collapses the table (header stays visible) and expands
it. State kept across re-renders and incremental patches of the same open document; not persisted
(reload or newly opened document: shown). Keyboard accessible (`button`, `aria-expanded`).

## Tests first

- Unit/page test that fails today: the header has the button; clicking it hides the table and sets
  `aria-expanded="false"`; a content patch keeps it collapsed; a fresh page load shows it.
- e2e scenario in group `frontmatter-schema` (simulated), with a light and dark screenshot for the PR.

## Requirements

New SwRS in scope `frontmatter-schema` (created `proposed`), markers per `rules.md`. If the writing
skill lists frontmatter UI, check whether it needs a line (constitution, section 6).

## Gates (foreground)

- `just check`
- The e2e group touched, simulated (no real VS Code window).
- `just requirements-update`
