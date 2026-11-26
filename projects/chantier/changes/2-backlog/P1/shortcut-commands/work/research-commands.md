# What the owner types, 2026-11-15 to 2026-11-25

A research subagent's pass over the owner's Claude Code transcripts (2026-11-25). 826 free messages in 25 sessions kept (the 25th partial). Counted by hand on messages cut at 230 characters, with a partial full-text check: orders of magnitude only. A message may count twice. AskUserQuestion answers and Copilot are not covered.

Slash commands typed: `/compact` 42, `/chantier-board` 13, `chief-of-staff` 6, `griller` 2, `status` 1, `chantier` 1.

## The four commands asked for

| Command | Messages | Note |
| --- | --- | --- |
| `batch-start` | 26 | 39 with changes of shape |
| `batch-pause` | 6 | weak: mostly "open or stay paused" |
| `batch-close` | 12 | in 2 sessions; 4 with a release, so a `--release` option is worth asking about |
| grill to pending | 23 | 10 with a grill or a specification, 13 new requests sent straight to the batch |

## Other recurring patterns

Reporting a merge 79 (includes an ambiguous "fait"); adding existing CRs to the batch 29; release 22; autonomy or night run 19; what is left 18; budget or rounds 17; status 17; board link or restart 16; seeing the questions 12; resume 12; opening a Griller session 7.

## Proposed, not picked by the owner

1. `/chantier:autonomy` (strongest): "I am leaving". Before the owner goes, name what would block (permissions, budget, open questions), then go on without questions until the report. Options: `--budget`, `--rounds`, `--answers ask|fable`, `--deliver stack`, `--release` (never by default). 19 messages in 5 sessions over 7 days, 13 since the 20th; 34 distinct messages with budget and rounds. It replaces no merge, permission prompt, refusal, ungranted release approval or CLI limit.
2. `/chantier:batch-add` (medium): add `inbox`, `P1`, `ready` or named items to the running batch, specifying what is missing. Options: `--now`, `--end`, `--grill`. 29 messages in 4 sessions, 19 since the 20th. Short messages that are already understood, so little gain per use; worth merging with grill to pending (52 messages together).

Set aside: "what is left and the questions" (close to `status`), the board link, merges (the watcher's job). `/chantier:status` was typed once against 17 free-text requests: a command may not change the habit.
