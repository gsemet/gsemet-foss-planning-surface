## Summary

On Windows, `just preflight` runs only the static stage, so visual and real VS Code window failures
show up only in CI, often at the very end of a change. This adds a rule to the change request
process: a change that adds or changes visual, integration or stress scenarios pushes a draft pull
request after its first round and dispatches the heavy CI, so the next round starts from the real
CI result.

## Deliverables

None beyond the guideline text: one new bullet, "Early heavy CI", in
`.agents/guidelines/change-requests-lifecycle.guidelines.md`.

```text
round 1 -> checkpoint commit -> rebase + just check -> push -> draft PR (provisional body)
        -> gh workflow run ci.yml --ref <branch> -f heavy=true -> round 2 reads the run
```

## Changes

- New "Early heavy CI" bullet between "Pull request" and "CI": scope, early push steps, stack and
  open-pull-request cap handling, how to read the run (head SHA check), and when to dispatch again.
- It states that it overrides the Driver card's "gate before the first push" for these changes.
  The requirements check and `just preflight` keep their places before ready.

## Impacts

No visible change: process documentation only.

## Blast radius

Grade: 1. A text-only change to a process guideline; a plain `git revert` restores the previous process.

## Test plan

- [ ] New or changed tests: none (documentation only)
- [ ] Requirements: No behaviour change
- [ ] Changelog: No user-facing change
- [ ] Local gates: `just check` and `test/build/test_guideline_isolation.py` (9 passed)
- [x] Review (approved at 6774cd7)
- [x] CI green (gh pr checks 457 at 6774cd7)

## Autonomous decisions

- The fast gate named in the bullet is `just check`, as the project instructions name it.

## Known gaps

None.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
