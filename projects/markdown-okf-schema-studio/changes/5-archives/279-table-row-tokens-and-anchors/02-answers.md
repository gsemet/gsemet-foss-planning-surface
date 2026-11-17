---
title: Grill answers
date: 2026-11-10
---

# Grill answers

Owner's triage of QA campaign 271 (2026-11-10), and the batch decision of the same day.

- Priority P2, run now as part of a stack of six CRs (277 to 282), shipped as a stack of PRs; the
  owner merges the stack.
- Starting test: the CR takes its own QA 271 replay from the local branch
  `qa/271-table-campaign-replays` (commit 87307e8f, not pushed) into its PR; the QA branch itself
  is not pushed.
- No GitHub issue (`issue: none`).
- `^id` tokens in table rows: the owner never writes them; they come from other tools or agents. A column move must not carry them into the middle of the row; a trailing token must not make the handles inert.

## Spec review (owner, 2026-11-10)

- Accepted: on a column move, a trailing `^id` in the last cell moves after the closing pipe (`| a | b | ^row-b`) and no longer shows in the preview.
