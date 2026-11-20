# CR-426 verification

Head: cc3a627e2b09ebb998854b46f735d122c3f97cc0
Base: origin/main 82c11a472250b6b808476ec797c2106481ddbd15
Second verification at the same head (no move: cc3a627..cc3a627). Only the PR description changed
(the Review box), in `pr-body.md` and on the forge; it is judged again (claims 7 and 8). Claims 1-6
are carried from the first verification at cc3a627: no commit, rebase or base change since
(`git rev-parse HEAD`: `cc3a627e2b09ebb998854b46f735d122c3f97cc0`, `git status --short`: empty).

## Claims

1. **Fail-before: the busy-wait alone, with only `setTimeout` mocked, fails both tests.** At
   cc3a627 (carried from cc3a627: same head, no move). `fnm exec -- npm run compile`, then in the
   git-ignored compiled `out/test/node-services/build/buildQueue.test.js` lines 94 and 126 changed
   from `["setTimeout", "Date"]` to `["setTimeout"]` (sed), then
   `fnm exec -- node --test out/test/node-services/build/buildQueue.test.js`: exit 1,
   `ℹ pass 10`, `ℹ fail 2`; "retains a successful result as stale after a failed newer build":
   `AssertionError ... assert.ok(pending.has(2))`; "still renders a build whose buffer already
   moved on, and cleans up on dispose": `false !== true`. Log: `work/verifier/before-busywait-setTimeout-only.log`.
   Restored by `npm run compile`. PASS.
2. **After: the file passes 20 runs in a row.** At cc3a627 (carried from cc3a627: same head, no
   move). `for i in $(seq 20); do fnm exec -- node --test out/test/node-services/build/buildQueue.test.js > /dev/null 2>&1 || break; echo "run $i pass"; done`:
   `run 1 pass` .. `run 20 pass`; one more run: `ℹ tests 12`, `ℹ pass 12`, `ℹ fail 0`. Log:
   `work/verifier/after-20-runs.log`. PASS.
3. **Only the test file changes; no src/, requirements/, assertion, test-name or marker change.**
   At cc3a627 (carried from cc3a627: same head, no move). `git diff --stat origin/main..HEAD`:
   `test/node-services/build/buildQueue.test.ts | 32 +++++++++++++++++++++--------`, 1 file.
   `git diff --name-only origin/main..HEAD -- src requirements`: empty. PASS.
4. **Commit type and cause.** At cc3a627 (carried from cc3a627: same head, no move).
   `git log -1 --format=%B HEAD`: subject `test: read one clock in the build queue tests`; the body
   names the cause. PASS.
5. **Long gate.** At cc3a627 (carried from cc3a627: same head, no move). Gate log
   `work/gates/20261120-102525.log`, first line:
   `gate CR-426 branch chantier/batch-06/cr-426-flaky-test-test-node-services-buildqueue head cc3a627e2b09ebb998854b46f735d122c3f97cc0`;
   last line `result: pass at cc3a627e2b09ebb998854b46f735d122c3f97cc0` (`just preflight`). PASS.
6. **CI.** At cc3a627 (carried from cc3a627: same head, no move). `gh pr view 432 --json headRefOid,statusCheckRollup`:
   head `cc3a627e2b09ebb998854b46f735d122c3f97cc0`; checks, report, static, static-windows, visual
   SUCCESS; the rest SKIPPED, none failed. PASS.
7. **Review box (`Review: approved at cc3a627 (carried from ac487ff: same patch, rebased onto
   main)`).** Judged again at cc3a627. `$CHANTIER log CR-426`, line 13:
   `driver note note=r1 approved at 80940a3, committed as ac487ff9` (and line 12:
   `r1 inspector approved at 80940a3c...`): an approved-pass note names ac487ff, the SHA the box
   carries from. `git show ac487ff9 | git patch-id --stable` and `git show cc3a627 | git patch-id --stable`:
   both `c97461d344ca5e340482a5d4bd7a7fdbdba98198`, so the pushed commit is the reviewed patch
   rebased cleanly. PASS.
8. **PR description.** Description-only pass, judged again at cc3a627 (head unchanged:
   `git rev-parse HEAD` = cc3a627e2b09ebb998854b46f735d122c3f97cc0; claims 1-7 carried from
   cc3a627). `diff pr-body.md <(gh pr view 432 --json body -q .body)`: only `62a63`, one trailing
   empty line, so the posted body is the local file. Follows `.github/PULL_REQUEST_TEMPLATE.md`
   (all sections; no internal id outside the last "Internal references" section, which names
   CR-426, `work/verify.md` and two logs that exist in `work/verifier/`). Renders (sections,
   table, task list; no image, so no image look). Summary, Deliverables and Changes match the diff
   (one file, `test/node-services/build/buildQueue.test.ts`, per `gh pr diff 432 --name-only`).
   Test plan boxes: tests box proved by claims 1-2, local gates by claim 5, review by claim 7, CI
   box by `gh pr view 432 --json headRefOid,statusCheckRollup`: head cc3a627, checks, static,
   static-windows, visual, report SUCCESS, integration and stress SKIPPED (not run on a PR), none
   failed (claim 6). Known gaps "None": no UNVERIFIED claim, no uncaptured pair, no accepted
   failure. No STALE mark. PASS.

## Evidence

`work/verifier/evidence/before-after.md` (carried from cc3a627: same head, no move).

Worktree clean at cc3a627 (`git status --short`: empty).

Note for the Driver: the copy of the posted body used for claim 8 was written to the session
scratchpad, outside this agent's `writes:` folders; removing it afterwards was refused with:
`refused: a shell write to C:/Users/gaeta/AppData/Local/Temp/claude/350cf196c0f59593/6eae8e55-4c71-4c8e-b28c-7788a8975d81/scratchpad/posted.md is outside the folders this agent may write in (...); the shell follows the same rule as Write and Edit`.
It holds only the public PR body and is left in place.

## Verdict

VERIFIED at cc3a627e2b09ebb998854b46f735d122c3f97cc0.
