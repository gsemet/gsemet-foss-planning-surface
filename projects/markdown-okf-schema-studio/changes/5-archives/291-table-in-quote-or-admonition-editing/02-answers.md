---
title: Grill answers
date: 2026-11-11
---

# Grill answers

- Run now (owner, 2026-11-11: "Export single html et les findings"), as one stack of six PRs, bottom to top: 290, 289, 293, 292, 291, 288. The owner merges the stack.
- No GitHub issue (`issue: none`).
- Starting test: the CR takes its own QA 271 replay and fixtures from the local branch `qa/271-table-campaign-replays` (commit 87307e8f, not pushed) into its PR; the QA branch itself is never pushed.
- QA271-11: a table inside a quote or an admonition (Note, etc.) gets the same cell editing as a top-level table, instead of the raw block editor.
- Spec question (2026-11-11): row and column drag handles and "Convert to list-table" on a table inside a container are out of scope: no handles, Convert disabled with its reason; a backlog item follows.
- Addendum (owner, 2026-11-11, after round 1): the spec's premise was wrong (row and column handles already show on a table inside a container on main, and a drop did nothing). Keep the working handles: the coder's fix in `tableRowMove.ts` (source holding exactly one pipe table) stays, recorded in the PR's "Autonomous decisions", with boundary rows for TABLE-002, TABLE-007, TABLE-035 and TABLE-070. "Convert to list-table" stays disabled with its reason.
