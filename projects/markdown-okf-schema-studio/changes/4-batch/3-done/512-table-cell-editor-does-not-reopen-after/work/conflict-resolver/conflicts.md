# CR-512 conflicts

## Stack restack onto 9d7e788a

- Branch: `chantier/batch-09/cr-512-cell-editor-reopen-after-a-grid-paste-re`
- Rebase: old base `89cae5ff`, new base `9d7e788a`; head `e76c0843` became `54d1da62` (one commit, same message, no merge commit). Not pushed.
- No earlier `conflicts.md` was found in this CR folder.

### Hunk 1: `requirements/tiers/log.md`, under `## 2026-11-26`

- Base side: the two CR-505 entries ("Scenario coverage of the trust and security behaviours (CR-505, round 3)" and "StRS acceptance tests of trust and security, and the acceptance job (CR-505, first round)").
- Branch side: the entry "Grid paste from a header cell: the missed editor reopen did not reproduce (CR-512)".
- Choice: both sides kept, text unchanged. The CR-512 entry is on top, then CR-505 round 3, then CR-505 first round, under the single date heading, one blank line between entries. Against the base the file differs only by the six added lines of the CR-512 entry. No byte-order mark, as before.

The seven other files of the commit applied without conflict.

## Fast gate

- Command, as run in the worktree at `54d1da62`: `just check` (output in `work/conflict-resolver/restack-54d1da62-just-check.log`).
- Result: pass, exit 0. Unit 5359 pass, 0 fail, 7 skipped (5366); security 116 pass; clip kit 56 pass; release tests 254 passed; contracts 0 tests (the tree has no `*.contract.ts` file); requirements lint passed, with W2 broken cross-link warnings. Worktree clean afterwards.
- Not run: `just preflight` and the heavy CI (real VS Code window).
