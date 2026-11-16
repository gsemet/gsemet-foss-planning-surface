# Answers

Recorded by the Chief of Staff, 2026-11-11, while steering batch-09 (no grill during a running
batch; the user's words below are the decision).

## The rule

User: "Non c'est parce que le classifier veut empêcher des règles destructives dans des sous
agents. Je veux que tu sois capables de juger si c es légitime ou pas et que tu pousses
automatiquement si tu le peux et tu me demande uniquement quand tu penses que c'est pas bon ou
que tu n'y arrive pas".

- The steering session (the Chief of Staff in direct mode; in Foreman mode the Chief of Staff,
  who receives the push line from the Foreman) judges a Driver's refused force push and runs it
  without asking the user.
- It asks the user only when it judges the push not legitimate, or when it cannot push (the
  host refuses it too, or the lease fails).
- Why the Driver's push is refused: the host's auto-mode classifier blocks destructive git in
  subagents ("Git Destructive"). The steering session's own push is not refused the same way
  (proved 2026-11-11: the Chief of Staff's `git -C <worktree> push --force-with-lease=...` went
  through in batch-09).

## Encode it in chantier

User: "Encode cette règles dans Chantier pour que ça n'arrive pas".

- The rule goes in the cards, so every user gets it; no per-session agreement and no memory.
- The Chief of Staff's card must also say plainly that the push is not a question for the user:
  in batch-09 the Chief of Staff asked although its card already made the push its own.

## Defaults taken (the user was not asked; changeable at review)

- Legitimacy is judged, not a fixed list. The card names what the judgement looks at: the
  branch is the CR's own and never the default branch (today's check), the local head contains
  the remote head's work rebased onto the default branch, the gate passed at the local head.
- What the user hears: a pushed branch is reported in the next report, not asked.

## The specification's open questions (2026-11-11)

Taken with the spec-writer's recommended answers, as for the batch's other specifications (the
user said to launch the specs and the batch; no grill while a batch runs). Changeable at review.

1. The gate did not pass at the local head: sent back to the Driver
   (`push refused <branch>: no long gate passed at <sha>`), not asked to the user.
2. The lease fails: the user is told at once; nothing waits for the user's word.
3. The host refuses the Chief of Staff's own push too: the message carries the exact push
   command, for the user to run or allow.
