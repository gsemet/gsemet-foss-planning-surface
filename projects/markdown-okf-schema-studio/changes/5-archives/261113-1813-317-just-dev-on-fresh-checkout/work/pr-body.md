## Summary

A new git worktree has no `node_modules` (it is gitignored), so the first gate run there failed with "tsc not found". The worktree guideline symlinked the main checkout's `node_modules`, and the main checkout can have none. The rule is now explicit: run `just dev` first in a new worktree or a clean checkout, before any build, check, test or gate.

## Deliverables

Before and after, the dependency lines of the worktree recipe:

```diff
 git worktree add -b change-requests/<id>-<slug> ../<repo>.worktrees/<id> origin/main --no-track
-ln -s "$PWD/node_modules" ../<repo>.worktrees/<id>/node_modules
-(cd ../<repo>.worktrees/<id> && uv sync --group requirements)
+(cd ../<repo>.worktrees/<id> && just dev)
```

## Changes

- `.agents/guidelines/local-worktree.guidelines.md`: the recipe runs `just dev` in the worktree; the paragraph states the rule and why `node_modules` is no longer symlinked.
- `AGENTS.md` (Setup): one bullet pointing to that rule.

## Impacts

No visual change: process text only, no product behaviour.

## Blast radius

Grade: 1. Two documentation files; a plain `git revert` restores the previous text.

## Autonomous decisions

- The `node_modules` symlink is dropped from the worktree recipe. `npm ci` replaces `node_modules`, so through the symlink `just dev` would wipe and reinstall the main checkout's dependencies. Each worktree runs its own `just dev` instead.

## Test plan

- [ ] New or changed tests (they fail on the previous code) <!-- none: documentation only -->
- [x] Requirements: No behaviour change
- [x] Local gates: `just preflight` in the worktree after `just dev`: ci-static and ci-visual pass; the local real-VS-Code integration stage fails (and ci-report/ci-gallery with it), covered by a heavy CI run on the branch
- [x] Review
- [x] CI green (heavy run on the branch: all jobs pass)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
