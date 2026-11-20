# Verify CR-347

Head: 3766a40e039ec45f86c91cf98a1bdca72fc38de8

All claims judged at 3766a40e (worktree `git rev-parse HEAD` equals it).

1. Lint at head: `just requirements-lint` exit 0, 0 error lines (only W2 broken-cross-link warnings on
   unrelated palette-slash SwRS); "0 indexes would change", "0 files would change", "main paths: 87 StRS
   checked, 563 SwRS citations, all valid".
2. Markers at head: `just check-markers` -> "9 companion file(s), 406 in-force SwRS marked, 30 files on the
   marker baseline" (pass).
3. One use case, one diagram: loop over StRS files of rendering-core, diagrams, trust-security: every
   non-deprecated StRS has `### Use case diagram` (6 + 5 + 6 = 17); only deprecated StRS and index.md lack it.
4. Nothing deleted: `git diff --name-status c3b9802 HEAD -- requirements | grep -c '^D'` -> 0 (merged ones are
   status deprecated/superseded). Only `test/integration/realInput/markers.ts` deleted, as the body says.
5. Re-approvals: CORE-001, DIAG-001, DIAG-006 carry approved_by gaetan@xeberon.net, approved_at
   2026-11-17T19:27:51+01:00, verified.at the same value.
6. CI at 3766a40e: `gh pr checks 418`: static, static-windows, visual, report, checks pass; gallery etc. skipping.
   `gh run view 44354351564`: success at headSha 3766a40e; integration and stress success, gallery skipped.
7. Long gate: log `work/gates/20261118-175812.log` first line "gate CR-347 branch ... head
   3766a40e039ec45f86c91cf98a1bdca72fc38de8", `$ just preflight` (pass recorded by the CLI).
8. Review box "approved at 3766a40e": STATUS.md note "move 46ef6780..3766a40e inspector approved at
   3766a40e039ec45f86c91cf98a1bdca72fc38de8" matches.
9. PR description: posted body on PR 418 equals work/pr-body.md (diff: one trailing blank line only). Summary,
   Deliverables, Changes match the diff (309 files: requirements, src markers, test markers/tests, markers.ts
   deletion). Mermaid fence and details fold present; no image; internal references (CR-347, batch, #415)
   only under Internal references. Known gaps list covers the gaps named in the brief; no STALE mark.
   Test plan claims each have proof above (1, 2, 6, 7, 8).

No screenshots expected (no visual change); no before/after evidence captured, none needed.
Unit tests were not re-run locally; CI at the head ran them (claim 6).

VERIFIED
