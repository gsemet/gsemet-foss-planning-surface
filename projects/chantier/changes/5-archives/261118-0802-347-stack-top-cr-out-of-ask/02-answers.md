---
type: cr-answers
description: The user's word on a CR taken on top of a ready stack, and the working choices made for it.
---

# Answers

## Settled by the Chief of Staff

### The request

2026-11-18, the user's word (French, translated): "file all six and run them in batch-24". This
CR is one of the six retro points of batch-24 kept by the retro critic; it runs as
`intake/request.md` writes it, with no grill.

### Working choices

1. **"Kept out of that stack's ask" means `forge-stack show` (and so `create`/`rebuild`, which
   read the same plan) lists such a CR under `to come:`, not in the stack as it stands.** The
   Foreman's partial ask copies its `<cr>=<link>` pairs and its `to come:` tail from that read,
   so the ask follows. Batch-24's block was check 2's `missing #304` on CR-342's draft.
2. **Which CR is kept out:** a `working` CR with a PR that the stack driver has not placed yet
   (`stacked` false in the record). It joins the stack as it stands when the stack driver names
   it in `stack <cr>…`, at the take that follows its PR, as the cards already say. A CR the
   stack driver placed while working stays a draft on top, as today. A `ready` CR not placed
   yet is left as it is: the Foreman's next `take stack` already places it before any ask.
3. **"Based on the CR just before it in the stack order":** `take` records as the start base the
   nearest earlier CR of the batch (lower order, not ended, neither fix nor release) whose branch
   exists: it has a PR, or its worktree is made. This replaces concepts' "a branch with no PR is
   never a base": a branch with a worktree exists locally, so a Driver can start on it.
   **Superseded by A below.**
4. **No wait added:** a CR taken in the same turn as the CR before it, before that CR's Driver
   made its worktree, starts on the next one below, as today. The Foreman does not hold a take
   for a worktree (slots stay full); choice 1 keeps that CR out of the ask either way.
5. **No new CLI command or flag,** and no change to the five checks' wording: the change is one
   predicate in `stacks.py`, read by `forge-stack`'s plan and by `take`.
   (After A: read by `forge-stack`'s plan only; `take` is unchanged.)
6. **Out of scope:** the conflicts of a final-order restack between CRs that touch the same
   files (no base choice removes them), and the order of CRs within a stack.

## Settled by the Chief of Staff (after the spec critic)

The user is away; the Chief of Staff settles in the user's place, inside the request's intent,
with the critic's recommended option.

A. **Start base (critic findings 1 and 2), option (a):** keep CR-333's rule, "the nearest
   earlier CR of the batch that has a PR", set by the user after batch-23 (PRs formed a tree on
   branches with no PR or no commit). A worktree that exists does not prove the branch is on the
   forge, and the later Driver's `gh pr create --base` / `glab mr create --target-branch` against
   an unpushed branch fails. This CR ships only the `to come:` part; choice 3 is dropped, and
   `start_on_for`, `core/records.py`, `concepts.md`'s "Stack" and "Dependencies" base lines,
   `driver.md`'s base rule (lines ~733-736), `foreman.md`'s first take and 13-bis stay as they
   are. Findings 3 and 4 (conditional on keeping choice 3) so need no edit.
