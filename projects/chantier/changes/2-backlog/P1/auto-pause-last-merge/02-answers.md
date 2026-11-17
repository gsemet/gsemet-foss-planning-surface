---
type: cr-answers
description: The user's answers to the grill of the automatic pause at a batch's last merge.
---

# Answers

## auto-pause-Q1: who pauses when the last CR merges

2026-11-17, the user chose the recommended answer: the CLI, at once: the `order merged` of a batch's last CR runs the pause itself, the merged CRs' worktrees and branches removed with it; the steering session then only writes the retro and offers the close.

## auto-pause-Q2: the close

2026-11-17, the user chose the recommended answer: offered, on the user's yes: the steering session shows the bilan and asks at once, unprompted; `close --yes` only on the user's yes, as today.

Spec critic: yes, it changes the CLI's lifecycle (a pause run by `order merged`) and the steering session's contract.

## Spec questions (2026-11-17)

- auto-pause-Q2b (pending orders): the automatic pause marks done every pending order the CLI fully applied (`applied: true`); only a note, a QA order or the drop of a live CR blocks it.
- auto-pause-Q3 (git refuses a removal): keep the worktree (no `--force`), print a `cleanup: ... not removed` line and pause anyway; the user decides at `close`.
- auto-pause-Q4 (other ends): `handback released`, `cancel` and `order drop` of the last CR also pause and clean at once.
- auto-pause-Q5 (AGENTS.md): yes, the PR amends `AGENTS.md` to name this git exception of the CLI.
- auto-pause-Q6 (`status` flag): keep the line "every CR is merged or cancelled, not paused: <what blocks>".
- auto-pause-Q7 (a Driver that may still run): the CLI skips any merged CR whose agent the record still holds, prints `cleanup: <cr> kept: agent <id> still held`, and still pauses; the steering session removes that worktree once the Driver has ended.
- auto-pause-Q8 (Windows, an open worktree): the CLI removes only worktrees whose Driver has ended (Q7); the spec states the partial-delete case and points to `git worktree prune` and the user's word for a leftover folder; one test runs on Windows with an open handle.
- The steering session offers or runs `close` only after its retro critic has handed back (close-batch-agents-only, close-agents-Q5).
