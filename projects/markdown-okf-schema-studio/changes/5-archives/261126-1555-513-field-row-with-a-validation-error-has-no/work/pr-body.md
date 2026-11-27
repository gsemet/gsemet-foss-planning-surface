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
- Tests: `test/core/preview/fieldIssueStyles.test.ts` checks the shipped stylesheet, including the colours it resolves to with the values of a dark and of a light VS Code theme.
- Visual tests: four scenarios in `test/visual/scenarioDefinitions2.ts` (field rows and whole-table warning, light and dark) check the computed styles of the rendered page in the Current mode, with status colours that `test/visual/themes.ts` sets on the page as a VS Code theme does. They use two new fixtures in `test/visual/fixtures/` and one schema file that cannot be parsed. `test/site/e2eGroups.test.ts`, which counts the visual scenarios, now expects four more.
- `CHANGELOG.md`: one line under `## Unreleased`.

## Impacts

A visible change: rows with an error or a warning are coloured in the properties table.

Current preview mode, pages of the visual test harness. The pictures before the change set no status colour on the page; the pictures after it set the status colours of a VS Code theme (in the light pictures the warning colour is a darker stand-in).

| | Before (at `e2b2235`, carried from `9d7e788`) | After (at `223a8c4`, carried from `7f7cc06`) |
| --- | --- | --- |
| Field rows, light | ![Field rows before, light](https://github.com/user-attachments/assets/1ac3d1bd-7598-4268-8eb5-ad2665250e16) | ![Field rows after, light](https://github.com/user-attachments/assets/6c9459ee-c35d-4a18-80f8-f1a35546b781) |
| Field rows, dark | ![Field rows before, dark](https://github.com/user-attachments/assets/3c77d15d-7b8c-46d3-a3aa-cbedd572371d) | ![Field rows after, dark](https://github.com/user-attachments/assets/a8a387fd-d5e9-4d57-91a5-62824e2543fc) |
| Whole-table warning, light | ![Table warning before, light](https://github.com/user-attachments/assets/c016f740-069f-4b0b-9002-4677f065dbcf) | ![Table warning after, light](https://github.com/user-attachments/assets/17821188-0654-4c86-a6dd-e851e3d902ae) |
| Whole-table warning, dark | ![Table warning before, dark](https://github.com/user-attachments/assets/28155425-22fb-4cb5-932a-5f2fcea1a739) | ![Table warning after, dark](https://github.com/user-attachments/assets/9bae17fa-9f2f-450d-a393-9fc6cb484b93) |

The default **Cream** mode with the colour values of a dark VS Code theme set on the page (at `223a8c4`, carried from `7f7cc06`): the marked rows keep the colours of the Cream palette.

![Field rows in Cream over a dark theme](https://github.com/user-attachments/assets/b544bb92-19fe-4ec1-a56d-c8b8972873a0)

![Whole-table warning in Cream over a dark theme](https://github.com/user-attachments/assets/7006b9c4-07f7-403b-86b1-6e19d2421a7d)

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

- [x] New or changed tests at `223a8c4` (carried from `cd3b8e6`; they fail on the previous code): `test/core/preview/fieldIssueStyles.test.ts` and the four visual scenarios of `test/visual/scenarioDefinitions2.ts`
- [x] Requirements at `223a8c4` (carried from `cd3b8e6`): `SwRS-MDOKFSTUDIO-FMSCHEMA-084` and `SwRS-MDOKFSTUDIO-FMSCHEMA-023` updated. Source files `src/core/preview/styles/propertiesStyles.ts` and `src/core/preview/styles/pageChromeStyles.ts` (markers in their `.markers.ts` files); test files `test/core/preview/fieldIssueStyles.test.ts` and `test/visual/scenarioDefinitions2.ts`. `just requirements-update` changes no file; requirement validation reports 0 errors and 26 warnings
- [x] Changelog at `223a8c4` (carried from `cd3b8e6`): one line under `## Unreleased` in `CHANGELOG.md`, with the number of this pull request
- [x] Local gates at `223a8c4` (carried from `cd3b8e6`): `just preflight` passed on Windows, where it runs the static stage only (unit tests: 5375, 5367 pass, 0 fail, 8 skipped; other Node runs 56/56 and 116/116; Python 296 and 4 passed); the `frontmatter-schema` visual group passed (35 scenarios)
- [x] Evidence: before at `e2b2235` (carried from `9d7e788`), after at `223a8c4` (carried from `7f7cc06`), under Impacts
- [x] Review: approved at `223a8c4` (carried from `7f7cc06`)
- [x] Verified at `223a8c4` (carried from `cd3b8e6`)
- [x] CI green at `223a8c4`

## Internal references

- CR-513 field-error.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

