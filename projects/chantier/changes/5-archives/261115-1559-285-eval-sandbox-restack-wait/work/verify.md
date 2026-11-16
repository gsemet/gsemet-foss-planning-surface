Head: 4f60e01dd8a0fb52861d5ae31aa3d0a82673b898

Claims, all judged at 4f60e01:
1. `just eval-dry-run` passes ("dry run: 8 of 8 cases as expected"). Its merge-refused line: "failed and an unprefixed PR: merge exits 2 at once ...; a forever-pending PR: waits (bound patched small), then exits 2 `after waiting`; a pending-then-green PR: waits, then merges". Its stale-lock line: "CI FAILURE, merge refused, audit exit 1 with `FAIL [J5]` on PR 1".
2. `just check` passes (190 passed; release-notes ok). Linux/macOS/Windows: CI check x3 green per the brief; Windows run here.
3. sandbox.py read against the spec: CHECKS_WAIT, CHECKS_TRIES = 10, 31 (30 sleeps = 300 s, `bound`), `waiting for the checks of PR #m at its head sha7 (up to N s)` printed once, flushed; refusal gets `after waiting 300 s`; whole check redone from merged_with each read; empty rollup waits; failed/cancelled still immediate. Docstring and README's three places say it (git diff origin/main...HEAD).
4. PR body (work/pr-body.md) matches the diff (4 files, Changes list); posted body equals it except one blank line. Known gaps names the real-run claims (GitHub rollup shape, 300 s). Evidence: `git diff origin/main...HEAD --stat` = README, dry_run, sandbox, sandbox_forge.

VERIFIED

Description pass (same head 4f60e01dd8a0fb52861d5ae31aa3d0a82673b898; code claims 1-3 carried from 4f60e01: no code move):
5. Posted body (`gh pr view 236 --json body`) vs work/pr-body.md: diff shows only one blank line differs. Sections follow the template; Test plan boxes checked with SHAs 4f60e01 / 9d04743 / e257a8a; no role names or internal refs outside Internal references; no STALE mark; Known gaps names the real-run UNVERIFIED claims. Changes list matches the 4-file diff.
6. Review box `approved at 9d04743, committed as e257a8a (rebased to 4f60e01)`: `chantier log CR-285` has "r2 approved at 9d04743, committed as e257a8a, rebased clean to 4f60e01". CI: `gh pr checks 236`: check x3, eval-dry-run, scenario all pass; PR head oid = 4f60e01dd8a0fb52861d5ae31aa3d0a82673b898.

VERIFIED

---
Move pass: rebase 4f60e01 -> 86ab0d1 (base 9d04743 -> f257647, README conflict resolved).

Head: 86ab0d1037cd333cc158c9a229b7d18aba66bcdd

Claims, judged at 86ab0d1:
7. `just eval-dry-run` passes: "dry run: 11 of 11 cases as expected"; its merge-refused line: "a failed and an unprefixed PR: merge exits 2 at once ...; a forever-pending PR: waits (bound patched small), then exits 2 `after waiting`; a pending-then-green PR: waits, then merges"; stale-lock: "CI FAILURE, merge refused, audit exit 1 with `FAIL [J5]`".
8. `just check` passes at 86ab0d1: "All checks passed!", "200 passed in 32.20s", "release-notes ... ok". Windows run here; CI `gh pr checks 236`: check x3, eval-dry-run, scenario pass.
9. `git range-diff 9d04743..4f60e01 f257647..86ab0d1`: the CR's patch differs only in the evals/README.md kit-table line (conflict resolved to carry both sides' text, base's added detectors and this CR's wording). `git diff origin/main...HEAD --stat`: README, dry_run, sandbox, sandbox_forge (4 files, 90+/22-).
10. Claim 3 (sandbox.py against the spec): carried from 4f60e01: range-diff shows sandbox.py and sandbox_forge.py unchanged by the move.
11. Posted body (`gh pr view 236 --json body`) vs work/pr-body.md: identical except one blank line. Test plan lines 47-51 name 86ab0d1 (and 9d04743 for the first review), 200 tests, 11 of 11 cases: all match the runs above. Matches the 4-file diff; no STALE; Known gaps keeps the real-run UNVERIFIED claims (carried from 4f60e01: unchanged).
12. Review box `approved at 9d04743; ... move approved at 86ab0d1`: `chantier log CR-285` has "move 4f60e01..86ab0d1 (conflict) inspector approved at 86ab0d1037cd..." and "r2 approved at 9d04743". PR head oid = 86ab0d1037cd333cc158c9a229b7d18aba66bcdd.

VERIFIED

---
Move pass: rebase 86ab0d1 -> d662a73 (conflict) -> 430187c (clean, base 5ad2c27).

Head: 430187cd961d9bdd6b035d9d50e4a1e05da2f12e

Claims, judged at 430187c:
13. `just check` passes: "235 passed in 37.31s", "release-notes ... ok" (CI check x3 pass per `gh pr checks 236`).
14. `just eval-dry-run` passes: "dry run: 16 of 16 cases as expected"; merge-refused line: "failed and unprefixed: merge exits 2 at once; forever-pending: waits (bound patched small), then exits 2 `after waiting`; pending-then-green: waits, then merges"; stale-lock still `FAIL [J5]`.
15. cmd_merge in evals/kit/sandbox.py (`git diff origin/main...HEAD`): CHECKS_WAIT, CHECKS_TRIES = 10, 31 (bound 300 s, 30 sleeps); whole check redone from merged_with each read; `waiting for the checks of PR #m at its head sha7 (up to 300 s)` printed once, flushed; final refusal gets `after waiting 300 s`; checks_pending is false for not-open, unprefixed, or any finished non-SUCCESS check, so those refuse at once; empty rollup waits; merge_async head from the passing read. README three places (A merge, kit row, sandbox.py merge paragraph) and docstring say it. 4 files in diff.
16. Review box: `chantier log CR-285` has "r2 inspector approved at 9d04743" and "move 86ab0d1..d662a73 (conflict) inspector approved at d662a73"; the clean rebase to 430187c is carried (note "clean rebase d662a73..430187c"). Matches the box. PR head oid = 430187c.
17. FAILED: posted body (identical to work/pr-body.md except one blank line) line 47 says "`just check` (223 tests)" at 430187c; at 430187c `pytest --co` collects 235 tests and `just check` prints "235 passed". The stated count is wrong, so the claim is not proven as written. Otherwise the body matches the diff, has no STALE mark, Known gaps names the real-run claims.

NOT VERIFIED

---
Description pass at 430187c (claim 17 re-judged; claims 13-16 carried: no code move).

Head: 430187cd961d9bdd6b035d9d50e4a1e05da2f12e

18. `just check` at 430187c: "235 passed in 37.07s", "release-notes ... ok". Posted body (`gh pr view 236 --json body`) vs work/pr-body.md: `diff` shows one trailing blank line only. Test plan now says "`just check` (235 tests)" and "(16 of 16 cases)", matching the runs (claims 13, 14). Sections follow the template, matches the 4-file diff, no STALE mark, Known gaps names the real-run claims, review box matches `chantier log` (claim 16). PR head oid = 430187cd961d9bdd6b035d9d50e4a1e05da2f12e.

VERIFIED
