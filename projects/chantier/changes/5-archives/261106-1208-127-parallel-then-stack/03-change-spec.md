# In a stack, CRs run in parallel on main; only the stack driver stacks them

## Problem

PR 55 and PR 57 merged onto another CR's branch instead of main. CR-122 (PR 56) made a CR start on
the default branch, but three things still let a PR stand on another CR:

- `ship` records `_stack_base`, the CR's future place in the stack, before any stack exists, so the
  record names another CR's branch while the forge may say main.
- No card says which base a Driver gives its PR, nor that only the stack driver sets a base on
  another CR.
- A chain with no real dependency can only come from the plan, before the batch opens. The Foreman,
  who sees the work, cannot propose one, and nothing lets the user turn one off as such.

## Change

The rule, in `concepts.md`: a batch's CRs run in parallel, each on the default branch, each PR on
the default branch. A stack is made afterwards, by the stack driver. A CR stands on another only by
a dependency: a real one (`depends.json`) or a chain the Foreman decided.

The Driver, in `driver.md`: the PR's base is the `base` that `take` printed, never another. A
Driver does not retarget a PR.

The CLI:

- `stack` marks each CR it orders as stacked.
- `ship` records the place in the stack for a stacked CR, and the start base for any other, so the
  record always says what the forge should say.
- `take stack` still prints the place each CR will take.

A dependency's PR exists when the dependent starts: `after` already waits for ready or merged, so a
PR on a CR's branch always stands on a branch with a PR.

The chain, in `foreman.md`, `routing.md` and `chief-of-staff.md`:

- The Foreman may chain a queued CR when that costs less than rebasing, for instance small work on
  the same lines. A shared file alone is no reason. It never chains a CR that has started.
- It sends `chain <cr> after <cr>: <reason>` to the Chief of Staff and leaves the CR queued.
- The Chief of Staff records it at once with `order after` and `order note`: this does not wait for
  the user. Its next report has a line with the chain and its reason.
- The user turns it off with a word, while the CR is queued: `order after <cr> --note -`. Once the
  CR has started, the chain stands until the stack driver restacks.

No new CLI command: `order after` and `order note` carry the chain.

Docs: `README.md` and `docs/use-cases.md` say that CRs run in parallel and that the stack comes
after; `docs/use-cases.md` no longer says each PR is based on the one below it from the start.

## Out of scope

- How a PR says it is not ready on the forge, and a merge onto a base that is not the default
  branch: `pr-readiness`.
- `open --parallel`, which stays: a batch with no stack at the end.
- Batch-06's own stack, which the stack driver is finishing under order O-27.

## Proof

- `just check` and `just scenario`.
- The scenario's stack section: before `stack`, `ship` records the default branch for every
  independent CR; after `stack`, the CR under it. A chain through `order after` starts on the
  ready CR's branch, and `order after <cr> --note -` puts a queued CR back on the default branch.
