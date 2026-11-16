# A stack's PRs stand on a base that exists

The user, on PR 55 of batch-06: "ca ressemble a une PR stack a moitier fait, est ce qeu tu es sur
que les CR driver n'essaye pas de faire la stack tout seul ?" Then, on the gap found: file a CR.

What happened in batch-06 (mode stack, 4 slots, CRs started in parallel):

- Each CR Driver pushes and opens its own PR on the base the state computes, as `driver.md` asks.
  No stack driver ran (`stack_agent: null`), so nobody ordered or restacked the whole.
- CR-121 could not open its PR: its base, CR-120's branch, was not on the remote.
- CR-122 still opened PR 55 on CR-121's branch, a branch with no PR. The user merged PR 55 and it
  landed on that branch, not on main.
- CR-123's base was CR-122's branch, gone after that merge: `gh pr create` failed ("Base ref must
  be a branch"), after `just scenario` had passed at f78c146.

The gaps:

1. The cards do not say who opens a CR's PR while a parallel stack is not ordered yet: the CR
   Driver, or the stack driver once it orders the stack.
2. Nothing refuses or warns about a PR on a base that has no PR, or no remote branch.
3. A merged PR whose base is not the default branch is not flagged before the user merges it.

CR-122's rule (the base of a CR with no dependency is the default branch) closes part of it once
merged; a CR with a real dependency, and a PR on a base without a PR, stay open.
