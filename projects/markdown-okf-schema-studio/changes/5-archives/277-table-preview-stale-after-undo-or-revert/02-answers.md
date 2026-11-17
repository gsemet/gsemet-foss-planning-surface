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
- The preview must always match the buffer after an undo or a revert.

## Spec review (owner, 2026-11-10)

- Narrow scope: the open editor's own table always matches the buffer; other blocks still wait for the editor to close (BLOCK-191 and BLOCK-193 not widened).
