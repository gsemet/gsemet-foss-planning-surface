# Verify CR-450

Head: 1bc77341d7f575a2dc5092bdc867e0087458e136

All claims judged at 1bc77341 (worktree HEAD, `git rev-parse HEAD`).

1. Gate pass at head. `work/gates/20261121-153530.log` first line: `gate CR-450 branch chantier/batch-07/cr-450-mutation-testing-campaign-on-src-core-re head 1bc77341d7f575a2dc5092bdc867e0087458e136`, command `just preflight`.
2. No test removed or merged. `git diff --name-status origin/main..HEAD -- test/` shows only `A` entries (`git diff --stat origin/main..HEAD -- test/`: 21 files, 1750 insertions, 0 deletions): 19 `*.holes.test.ts` plus `test/build/mutationReport.test.ts`, `mutationTools.test.ts`.
3. Requirements. `git diff --stat origin/main..HEAD -- requirements`: 26 files, 30 insertions, 0 deletions (log entry and generated coverage lines only). No `src/` and no `.github/` change in the diff stat. `.gitignore` gains only `/.stryker-tmp/`.
4. Single TypeScript. `npm ls typescript` -> `typescript@7.0.2` only; `grep -c typescript-checker package-lock.json` -> 0.
5. `just mutation-core` is in no check target: `grep -n mutation justfile` shows it only at its own target (lines 516-524), not in check, ci-static or preflight.
6. Real short run at head: `STUDIO_MUTATION_FILES="src/core/scroll/anchorPolicy.ts,src/core/state/navigationHistory.ts" just mutation-core`, exit 0 (log: `work/verifier-mutation-core.log`):
   - self-test passed: `typescript 7.0.2 loaded, tsgo spawned`, type-breaking replacement -> `CompileError: TS2322 ...`, type-valid -> `Passed`;
   - checker processes start `typescript 7.0.2, project opened, 0 baseline error(s)`; sandbox `npm run compile` green in `.stryker-tmp/sandbox-*`; dry run `Initial test run succeeded. Ran 2958 tests` with `perTest` coverage; core phase done in 2 min 39 s;
   - others phase ran and the reader wrote `out/reports/mutation/summary.md`: 65 CompileError, 216 Killed, 45 Survived, 1 Timeout, 2 NoCoverage; scroll 78.2% (matches the PR's "after" table value 78.2), state 98.1% on the sampled file only.
7. PR #461 description: posted body equals `work/pr-body.md` (only a trailing newline differs); renders (sections, mermaid fence, details fold), no images, figures consistent with the diff (19 holes test files, 2 tool tests, justfile, gitignore, dependency, docs lines). Known gaps list the unverified/accepted items. Review box `approved at 1bc7734 (carried from 2f25a63)` matches driver notes "r3 inspector approved at 2f25a634 ... rebase only changed log.md".
8. Not re-run (carried from evidence files, no multi-hour campaign): the sampled 51-file run figures (`evidence/r2-summary.md`) and the 19-file re-run (`evidence/r3-rerun.md`, 416 -> 97 cluster holes). Spot check of item 6 agrees with them for scroll. These figures are the Coder's, not reproduced here.

Note: the "Verified at 1bc7734" and "CI green" boxes of the PR are unchecked, expected before the verdict and CI.

VERIFIED
