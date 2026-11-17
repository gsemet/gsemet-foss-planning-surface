---
title: Grill answers
date: 2026-11-11
---

# Grill answers

- Run now (owner, 2026-11-11: "Export single html et les findings"), as one stack of six PRs, bottom to top: 290, 289, 293, 292, 291, 288. The owner merges the stack.
- No GitHub issue (`issue: none`).
- Starting test: the CR takes its own QA 271 replay and fixtures from the local branch `qa/271-table-campaign-replays` (commit 87307e8f, not pushed) into its PR; the QA branch itself is never pushed.
- QA271-09: the label rename popover must not cover the first table cells nor swallow their clicks.
- Spec question (2026-11-11): a label on the first line of the document followed by a table keeps the popover below; accepted, and described as it behaves in MYST-038.
