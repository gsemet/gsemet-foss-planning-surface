## Summary

A `::::{grid}` of cards written inside a GitHub alert (`> [!NOTE]` or `> **Note**`) was cut: the note held only the first card, the other cards fell outside it, and the grid's closing line, the alert's end and the text after the alert turned into a code block. The alert now holds the whole grid and the text after it renders after the note, as on GitHub.

## Deliverables

The alert's colon fence is now one colon longer than the longest colon fence in its body (at least three), so the nested containers close before the note does.

| Alert body | Fence before | Fence now |
| --- | --- | --- |
| plain text | `:::{note}` | `:::{note}` (unchanged) |
| `::::{grid}` of `:::{card}` | `:::{note}` (cut) | `:::::{note}` |

## Changes

- `expandGithubAlertsWithLines` scans the alert body for colon fences and lengthens the admonition fence; the line count and the `data-line` mapping are unchanged.
- SwRS-MDOKFSTUDIO-GFM-009 gets a row, criteria and method for the case; requirements log entry.
- Tests in `alertInsideColonContainer.test.ts`: both alert heads, line mapping of note, grid and cards, plain alert unchanged.

## Impacts

No visual change for documents that worked. Rendered structure for a `::::{grid}` of two cards inside `> [!NOTE]`, followed by `After.`:

| | Before | After |
| --- | --- | --- |
| note | holds a grid with card A only | one note holding the grid with cards A and B |
| card B | a separate block outside the note | inside the grid, inside the note |
| closing lines and `After.` | swallowed into a `<pre><code>` block | `After.` is a paragraph after the note |

## Blast radius

Grade: **1**. Local to the alert expansion; an alert without a colon fence in its body is byte-for-byte unchanged. `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased`
- [x] Local gates: `just preflight` static and visual stages pass; the integration stage (real VS Code) failed locally on a timing timeout unrelated to this change, covered by the heavy CI run
- [x] Review
- [x] CI green (pull request jobs and the heavy run)
