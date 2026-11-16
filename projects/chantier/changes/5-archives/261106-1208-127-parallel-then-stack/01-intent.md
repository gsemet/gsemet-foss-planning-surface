# Intent

In a stack, every CR is developed in parallel against the head of the project. Only the stack
driver turns them into a stack, once they are ready. While CRs run in parallel, none stands on
another: no branch, no PR.

The one exception is the Foreman's judgement: it may chain a CR when that is more efficient, gives
the reason, and the user can turn the chain off.

This absorbs `stack-pr-base`: its gaps 1 and 2 close here, its gap 3 (a merge onto a base that is
not the default branch is not flagged) goes to `pr-readiness`.
