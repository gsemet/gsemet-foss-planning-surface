## Summary

When a document's frontmatter has a schema, a field with a validation error (for example `status: publshed` against a list of allowed values) was only signalled by the small badge in the title of the properties table: the row itself looked like any other. This change marks the rows that carry an error or a warning, so the faulty field is visible at a glance.

## Deliverables

What each kind of row of the properties table shows:

| Row | Before | After |
| --- | --- | --- |
| Field with an error | plain | name in the error colour on a red-tinted background, wavy underline in that colour under the value |
| Field with a warning | plain | name in the warning colour on a background tinted with that colour, wavy underline in that colour under the value |
| Warning about the whole table (for example "Schema could not be parsed: ...") | plain | warning colour on a background tinted with that colour, spanning the table, text wrapping |
| Error about the whole table | red on a tinted background | unchanged |
| Information rows | plain | unchanged |
| Field with an error or a warning whose value is being edited | plain | name marked as above, no underline under the open editor |

The value text keeps its own colour. In the **Current** preview mode the colours are the VS Code theme's, with a fallback where the theme sets none. In the **Dark**, **White** and **Cream** modes (Cream is the default) they come from the palette of the mode, so the marked rows look the same on a dark and on a light VS Code theme. In edit mode, a marked name cell still highlights under the pointer like the other editable cells, and its text keeps the colour of its severity.

## Changes

- `src/core/preview/styles/propertiesStyles.ts`: new style rules for error and warning field rows and for whole-table warning rows; the edit-mode hover of a marked name cell; no underline on a cell being edited. The markup, the validation, the messages and the badge are unchanged.
- `src/core/preview/styles/pageChromeStyles.ts`: the Dark, White and Cream palettes declare an error background and a warning colour of their own, read only by the rows this change styles.
- Requirements: the software requirement (SwRS) `SwRS-MDOKFSTUDIO-FMSCHEMA-084` now states how a field row with an error or a warning looks, with three new scenarios (no underline during an edit, the hover of a marked name cell in edit mode, marked rows in a forced preview mode); the software requirement `SwRS-MDOKFSTUDIO-FMSCHEMA-023` states the look of the whole-table warning row, with one new scenario for the forced modes. Markers are in the companion marker files.
- Tests: `test/core/preview/fieldIssueStyles.test.ts` checks the shipped stylesheet, including the colours it resolves to with the values of a dark and of a light VS Code theme; four visual scenarios (field rows and whole-table warning, light and dark) check the computed styles of the rendered page, with two fixtures and one schema file that cannot be parsed; the test that counts the visual scenarios now expects four more.
- `CHANGELOG.md`: one line under `## Unreleased`.

## Impacts

A visible change: rows with an error or a warning are coloured in the properties table. Before and after screenshots: provisional, not yet attached.

## Blast radius

Grade: **1**. Style rules of the properties table and two new colour variables in the three forced preview palettes; a plain `git revert` restores the previous look.

## Autonomous decisions

- In the Dark, White and Cream modes, the marked rows take their error background and warning colour from the palette of the mode instead of the VS Code theme: mixing the two made the default Cream mode on a dark theme hard to read (contrast about 2:1). The requirements state it and tests check it.
- A value cell being edited has no wavy underline, because the underline was also drawn on the open editor and its field menu. The requirement states it and a test checks it.
- In edit mode, a marked name cell takes the same hover background as the other editable cells in place of its severity background, so the pointer feedback stays the same on every row. The requirement states it and a test checks it.
- While the branch was moved onto newer bases, conflicts in requirement files were resolved by keeping the entries of both changes and generating the file lists again.

## Known gaps

- In the Dark, White and Cream modes the whole-table error row, which this change leaves as it was, still takes its background from the VS Code theme and is hard to read on a theme of the opposite lightness (contrast about 2:1).
- In the Current mode the colours are the VS Code theme's own: with the values of the Default Light Modern theme, a marked name or whole-table warning has a contrast of about 2.6:1 to 2.7:1.
- No automated test of the repository checks the new look in a real VS Code window.
- No visual scenario covers the hover highlight of a marked name cell, the missing underline during an edit or a forced mode over a VS Code theme; they are checked on the stylesheet.
- In the visual scenarios the whole-table warning message fits on one line at 900 px, so no repository test shows it wrapping.

## Human decisions

- A field with an error shows its name in red on a red-tinted background, like the whole-table error row, with a wavy underline under its value; a field with a warning shows the same in the warning colour.
- Warnings that concern the whole table are coloured too, on a background tinted with the warning colour.

## Test plan

- [ ] New or changed tests (they fail on the previous code): provisional
- [ ] Requirements: provisional
- [ ] Changelog: provisional
- [ ] Local gates: provisional
- [ ] Evidence: provisional
- [ ] Review: provisional
- [ ] Verified: provisional
- [ ] CI green: provisional

## Internal references

- CR-513 field-error.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
