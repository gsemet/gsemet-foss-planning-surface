## Summary

The preview's floating toolbar was a main row of four buttons followed by four rows of three, which made it tall. It is now four buttons wide on four rows of four, with the same 16 buttons, behaviour and collapse.

## Deliverables

New layout (rows 2 to 4 are the group the collapse button hides):

| Row | Col. 1 | Col. 2 | Col. 3 | Col. 4 |
| --- | --- | --- | --- | --- |
| Main | Refresh | Edit | Export | Collapse |
| Navigation | Anchor | Theme | Back | Next |
| View | Width | Fold | Zoom out | Zoom in |
| Review | Table of contents | Side-by-side | Diff | Comments |

The Tab order follows the rows. The expanded toolbar is still exactly as wide as the collapsed one (134 px).

## Changes

- `previewToolbar.ts` builds the rows `main`, `navigation`, `view` and `review`; no button markup changes.
- The pending-changes overlay moves up to 160 px when the toolbar is expanded (62 px collapsed, unchanged), so it sits right under the four rows.
- Requirements updated to the new rows, including a fix of the collapsed Tab order in the collapse requirement (Refresh, Edit, Export, Show view controls).
- Tests that assert the row order, Tab order and overlay offset are updated; their intent (rows, counts, order, width) is unchanged because the decided layout changed. The Side-by-side button test moved with its row.
- User docs, README toolbar images, glossary, changelog and row-number comments updated.

## Impacts

Visible change: the expanded toolbar is shorter (four rows instead of five).

Before (cream theme, then dark):

![Before: expanded toolbar, five rows](./before-expanded.png)
![Before: expanded toolbar, dark](./before-expanded-dark.png)

After:

![After: expanded toolbar, four rows of four](./after-expanded.png)
![After: expanded toolbar, dark](./after-expanded-dark.png)

## Blast radius

Grade: 1. Markup order, one CSS offset and tests/docs; a plain `git revert` restores the previous layout.

## Approved requirements changed

- StRS-MDOKFSTUDIO-LAYOUT-003: the Width button is now on the third toolbar row (rationale and known issue updated). The owner agreed to this change explicitly; owner review requested.

## Autonomous decisions

- Other README images that still show the old toolbar (for example the showcase hero) were not regenerated.
- A stale row number in SwRS LAYOUT-020 and in `docs/user/settings.md` was corrected with the rest.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [x] Local gates: `just check`, `just ci-visual` (475 scenarios)
- [ ] Review
- [ ] CI green
