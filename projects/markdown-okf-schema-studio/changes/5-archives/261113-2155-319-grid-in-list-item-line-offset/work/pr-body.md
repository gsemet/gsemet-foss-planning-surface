## Summary

In edit mode, clicking a card (title or body) of a `{grid}` written on a list item line (`- ::::{grid} 2`, `1. ::::{grid} 2`) opened the block editor one line too early when the grid body starts with a blank line. The same offset hit a standalone `{card}` body, a `{tab-set}` panel in a list item, and a quote inside a list item. The editor now opens on the clicked line.

## Deliverables

None beyond the fix: one line-mapping helper.

## Changes

- `directiveBody` (`src/core/render/mystGridToctree.ts`) now locates a directive body through a general container-prefix strip (`stripContainerPrefix`, replacing the quote-only strip). It reads the opener as quote and list-item levels, strips the marker from the opener and the item indentation (and quote markers) from the following lines, so the blank first line is kept and the line numbers match the source.
- Tests: the render-level table in `gridCardTitleSourceLine.test.ts` gains rows for bullet, ordered, nested, quote-in-list and list-in-quote grids, a standalone card, plus regression rows and a tab-panel test.
- Requirement SwRS-MDOKFSTUDIO-BLOCK-258 gets a boundary scenario for list items; requirements log and changelog updated.

## Impacts

No visual change; the editor opens on the clicked line. Line numbers (card / title / body) from the new render-level test, run on `main` with the new test file and on this branch:

| Input (opener on line 3) | Before | After |
| --- | --- | --- |
| `- ::::{grid} 2`, `* ::::{grid} 2`, `1.`, `10.`, nested bullet, list item in a quote (blank first line) | 4 / 4 / 5 | 5 / 5 / 6 |
| quote inside a list item | 5 / 5 / 6 | 6 / 6 / 7 |
| standalone `{card}` in a list item, body | body 4 | body 5 |
| `{tab-item}` panel in a list item | `data-line` 4 | `data-line` 5 |

Test file: 26 pass / 9 fail on `main`, 35 pass / 0 fail on this branch (the 9 are the new list-item rows and the tab-panel test).

## Blast radius

Grade: 1. Local to line mapping of directive bodies; a plain revert restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS-MDOKFSTUDIO-BLOCK-258 updated, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [x] Local gates: `just check`, `just requirements-lint`, render tests (35/35) pass; local `just preflight` stopped at the real VS Code integration stage, so the branch heavy CI run is the proof (green)
- [x] Review
- [x] CI green (including the heavy run on the branch)

## Autonomous decisions

- Also fixed, because they share the same function and cause: the standalone `{card}` body, the `{tab-set}` panel line, and a quote inside a list item.
- Follow-up, not fixed here: a tab right after the list marker (`-<TAB>::::{grid} 2`) renders no card at all on `main`, for a reason other than the line offset. It was not investigated; worth filing as its own issue.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
