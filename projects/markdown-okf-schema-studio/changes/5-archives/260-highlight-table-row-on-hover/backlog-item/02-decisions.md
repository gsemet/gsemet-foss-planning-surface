# Decisions

## Owner (2026-11-04)

Option B, Accent tint: see the prototypes in [01-intent.md](01-intent.md).

- Even rows: `--studio-editor-foreground` at 3%.
- Hovered row: `--studio-focusBorder` at 12%.
- Heading: `--studio-focusBorder` at 24%.

## Plan

One CR, one PR. Not started; next free number when it opens.

1. Styles in `src/core/preview/styles/contentBlockStyles.ts`, on the page's tables, with `color-mix`
   and the tokens above, so that a VS Code theme is followed too. The heading rule replaces
   `--studio-textBlockQuote-background`.
2. Leave out the frontmatter properties table: `propertiesStyles.ts` keeps it without backgrounds.
3. Edit mode, in `editModeStyles.ts`: the hover stays below the row and column handles, the cell
   selection and the change bars.
4. Requirements: one SwRS in `rendering-core` for the three colours; `just requirements-update`, and
   a line in `requirements/tiers/log.md`.
5. Tests: a visual scenario per theme with a real hover, checking the three colours, and one in edit
   mode with the handles. Expect the README and gallery images that show a table to change.
6. Changelog line in `## Unreleased`. The writing skill needs no change: no syntax changes.

To check at review: the heading contrast in Dark, and a table that scrolls sideways, whose overflow
shading must stay visible through the even rows.
