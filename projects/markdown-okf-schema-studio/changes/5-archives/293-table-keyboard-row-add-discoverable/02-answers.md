---
title: Grill answers
date: 2026-11-11
---

# Grill answers

- Run now (owner, 2026-11-11: "Export single html et les findings"), as one stack of six PRs, bottom to top: 290, 289, 293, 292, 291, 288. The owner merges the stack.
- No GitHub issue (`issue: none`).
- Starting test: the CR takes its own QA 271 replay and fixtures from the local branch `qa/271-table-campaign-replays` (commit 87307e8f, not pushed) into its PR; the QA branch itself is never pushed.
- QA271-13: in the last cell of a table, a small hint "Tab: new row" shows; Escape on a row created by Tab that is still empty removes that row.
