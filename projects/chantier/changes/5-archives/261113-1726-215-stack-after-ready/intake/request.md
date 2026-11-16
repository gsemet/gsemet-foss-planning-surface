Work on a stack once it is ready (insert, restack after a merge, record) is manual, refused or leaves the record wrong. Fix: `forge-stack` inserts and rebuilds; the record follows a restack; the stack driver gets its `take stack` from the Foreman; `ship` flags stale SHAs; a merge needs one restack at most.

Merged on 2026-11-13 from the batch-15 retro items below (the user's word: "regroupe en moins de CR").

## From `forge-stack-insert`

Batch-15: inserting CR-213 below the release in GitHub stack #155 was refused to the stack driver and the Foreman by the permission check; the Chief of Staff, on the user's yes, ran POST /stacks/155/unstack, gh pr edit 154 --base <CR-213 branch>, then POST /stacks (stack #157). forge-stack has no insert: add one (unstack, retarget the PR above, re-create bottom to top, read back), and fix forge_stack.py's docstring, which says the API cannot add a PR to a stack or dissolve one: POST /stacks/{n}/add (append on top) and POST /stacks/{n}/unstack exist.

## From `order-after-ready-cr`

Batch-15: after CR-213 was inserted below CR-212 (release), 'order after CR-212' was refused ('it is ready, not queued'), so the record kept CR-212's base on CR-211's branch. An insertion must be able to change a ready CR's base: 'stack' (the recorded order) sets it, or 'order after' accepts a ready CR with a restack note.

## From `stack-driver-take-race`

Batch-15: the Foreman recorded the stack driver's id before it ran 'take stack', which then refused it, twice. The Foreman runs 'take stack' and passes its output in the prompt, or 'take stack' gives a read-only form for the stack driver.

## From `stale-test-plan-shas`

Batch-15: after the first post-merge restack the PR bodies' Test plan SHAs stayed stale until asked. 'ship' after a restack prints the PR body lines whose SHA is now stale.

## From `stack-merge-restack-cost`

Batch-15 retro: merging a stack of 16 PRs bottom-up needs a restack (force pushes, a CI per PR) after each merge: hours, and blocked when a force push is refused. Fix: let the user merge several PRs at once, or the whole stack top-down, and restack once (see CR-211 parallel-rebase-cost).
