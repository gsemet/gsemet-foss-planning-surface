---
title: Grill answers
date: 2026-11-11
---

# Grill answers

- Run now (owner, 2026-11-11: "Export single html et les findings"), as one stack of six PRs, bottom to top: 290, 289, 293, 292, 291, 288. The owner merges the stack.
- No GitHub issue (`issue: none`).
- Starting test: the CR takes its own QA 271 replay and fixtures from the local branch `qa/271-table-campaign-replays` (commit 87307e8f, not pushed) into its PR; the QA branch itself is never pushed.
- QA271-12: a spreadsheet (TSV) paste of several cells into a table cell fills the cells from the current one, rightwards and downwards, like a spreadsheet, and adds the missing rows and columns. One undo step undoes the whole paste. A single value without tab or newline pastes as today.
- Spec question (2026-11-11): a one-column copy (lines without a tab) pastes as today (one cell, line breaks become spaces, TABLE-091); only text with a tab fills cells.
