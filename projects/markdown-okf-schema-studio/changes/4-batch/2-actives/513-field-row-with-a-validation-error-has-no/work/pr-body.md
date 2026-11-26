## Summary

When a document's frontmatter has a schema, a field with a validation error (for example `status: publshed` against a list of allowed values) was only signalled by the small badge in the title of the properties table: the row itself looked like any other. This change marks the rows that carry an error or a warning, so the faulty field is visible at a glance.

## Deliverables

What each kind of row of the properties table shows:

| Row | Before | After |
| --- | --- | --- |
| Field with an error | plain | name in the error colour on a light red background, wavy underline in that colour under the value |
| Field with a warning | plain | name in the warning colour on a light background of that colour, wavy underline in that colour under the value |
| Warning about the whole table (for example "Schema could not be parsed: ...") | plain | warning colour on a light background of that colour, spanning the table, text wrapping |
| Error about the whole table | red on light red | unchanged |
| Information rows | plain | unchanged |
| Field with an error or a warning whose value is being edited | plain | name marked as above, no underline under the open editor |

The value text keeps its own colour. The colours come from the editor theme, with a fallback where the theme sets none. In edit mode, a marked name cell still highlights under the pointer like the other editable cells, and its text keeps the colour of its severity.

## Changes

- `src/core/preview/styles/propertiesStyles.ts`: new style rules for error and warning field rows and for whole-table warning rows; the edit-mode hover of a marked name cell; no underline on a cell being edited. The markup, the validation, the messages and the badge are unchanged.
- Requirements: the software requirement (SwRS) `SwRS-MDOKFSTUDIO-FMSCHEMA-084` now states how a field row with an error or a warning looks, with two new scenarios (no underline during an edit, and the hover of a marked name cell in edit mode); the software requirement `SwRS-MDOKFSTUDIO-FMSCHEMA-023` states the look of the whole-table warning row. Markers are in the companion marker file.
- Tests: `test/core/preview/fieldIssueStyles.test.ts` checks the shipped stylesheet; four visual scenarios (field rows and whole-table warning, light and dark) check the computed styles of the rendered page, with two fixtures and one schema file that cannot be parsed; the test that counts the visual scenarios now expects four more.
- `CHANGELOG.md`: one line under `## Unreleased`.

## Impacts

A visible change: rows with an error or a warning are coloured in the properties table, in light and dark themes. Before and after screenshots: provisional, not yet attached.

## Blast radius

Grade: **1**. Style rules of the properties table only; a plain `git revert` restores the previous look.

## Autonomous decisions

- A value cell being edited has no wavy underline, because the underline was also drawn on the open editor and its field menu. The requirement states it and a test checks it.
- In edit mode, a marked name cell takes the same hover background as the other editable cells in place of its severity background, so the pointer feedback stays the same on every row. The requirement states it and a test checks it.
- While the branch was moved onto a newer base, conflicts in requirement files were resolved by keeping the entries of both changes and generating the file lists again.

## Known gaps

- **UNVERIFIED:** no test in a real VS Code window checks the new look; it is checked on the rendered preview page of the visual test harness.
- In the visual scenarios the whole-table warning message fits on one line at 900 px, so its wrapping is checked on the stylesheet only.
- The hover highlight of a marked name cell and the missing underline during an edit are checked on the stylesheet; no visual scenario covers them.

## Human decisions

- A field with an error shows its name in red on a light red background, with a wavy underline under its value; a field with a warning shows the same in the warning colour.
- Warnings that concern the whole table are coloured too, on a light background of the warning colour.

## Test plan

- [ ] New or changed tests (they fail on the previous code): provisional
- [ ] Requirements: `SwRS-MDOKFSTUDIO-FMSCHEMA-084` and `SwRS-MDOKFSTUDIO-FMSCHEMA-023` updated, markers in code and tests, `just requirements-update`: provisional
- [ ] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`: provisional
- [ ] Local gates at `1a48862`: provisional
- [ ] Evidence: provisional
- [ ] Review: provisional
- [ ] Verified: provisional
- [ ] CI green: provisional

## Internal references

- CR-513 field-error.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
