# The Chief of Staff judges a refused force push and runs it; it asks the user only on doubt or failure

The user's words (2026-11-11): "Non c'est parce que le classifier veut empêcher des règles
destructives dans des sous agents. Je veux que tu sois capables de juger si c es légitime ou
pas et que tu pousses automatiquement si tu le peux et tu me demande uniquement quand tu penses
que c'est pas bon ou que tu n'y arrive pas".

## What happened

In batch-09 a CR-165 Driver's `--force-with-lease` after a rebase was refused by Claude Code's
auto-mode classifier ("Git Destructive"; it blocks destructive git in subagents). The Chief of
Staff, steering directly, asked the user before running the push, although
`chief-of-staff.md` "A refused force push" already makes the push the Chief of Staff's own,
after a branch check. The user wants no question in the normal case.

## What main says today (b3b2da4)

- `chief-of-staff.md`, "A refused force push": the Chief of Staff runs the push from the main
  checkout after checking the branch is the CR's own (via `handoff`) and never the default
  branch; a refused branch or a failed lease is answered to the Foreman.
- `driver.md`: a force push the host refuses is run by the Chief of Staff.
- Nothing says when the user is asked, nor what to do when the host refuses the Chief of Staff's
  own push too.

## What the user wants

- The Chief of Staff judges whether the push is legitimate (its own judgement, beyond the branch
  check: for instance the local head is a rebase of the remote one onto the default branch, the
  gate passed at it) and pushes without asking.
- It asks the user only when it judges the push not right, or when it cannot push (the host
  refuses it too, the lease fails).
- Written in the cards, in direct mode and in Foreman mode, never as a per-session agreement.
