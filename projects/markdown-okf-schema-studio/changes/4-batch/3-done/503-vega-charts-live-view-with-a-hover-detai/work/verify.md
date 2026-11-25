Head: 1f209e139e616a8748817a49951cbf3d9627ad2d

VERIFIED

Description-only pass at 1f209e1 (no move since the previous judgment, kept as verifier/verify-1f209e1-pass1.md).
That judgment found every code claim holding; only description claims D1 and D2 failed. Both and the changed
Review line are judged again here; the rest is carried.
Worktree clean (`git status --porcelain`: 0 lines); `git ls-remote origin` of the branch and `gh pr view 523`
headRefOid are both 1f209e139e616a8748817a49951cbf3d9627ad2d.
Posted body: `gh pr view 523 --json body` compared line by line with work/pr-body.md: equal, 61 lines each.

## Judged at 1f209e1

D1. Known gaps matches the two finished attempts of the heavy run. PASS.
- `gh run view 45706313890 --attempt 1 --json ...jobs`: completed, failure; integration, report, checks failure;
  stress, viewer-graph, visual, static, static-windows success.
- `--attempt 2`: completed, failure; the same three jobs failure, the same five success.
- integration-a1.log:2753 `LAUNCH TIMEOUT: trusted-suite.js exceeded its 900000 ms deadline ... last heartbeat step: diff-preview-scroll`;
  :689 `STEP done: open-at-line (22126 ms)`.
- integration-a2.log:685 `STEP failed: open-at-line (12624 ms): TIMEOUT: locator.count did not return within 10000 ms (frame )`.
- report-a2.log:384 `FAILED integration: integration manifest status is failed`.
- `gh run view 45580228461`: main, head 4a47151, integration, report, checks failure, stress and viewer-graph success;
  `--log-failed`: `LAUNCH TIMEOUT: trusted-suite.js ... last heartbeat step: lifecycle`.
- The bullet states each of these; the attempt 2 cause is said to be undiagnosed.
- Not covered: `gh run view 45706313890 --json attempt,status` shows attempt 3 in_progress. It is not judged (brief).
  "failed on both attempts" describes attempts 1 and 2 only and needs an update once attempt 3 ends.

D2. The picture proof names its SHA and why it carries. PASS.
- Body: "pictures taken at 4404b98, carried to 1f209e1: the chart code is unchanged since".
- `git diff --stat 4404b98 124a348 -- src`: empty. `git diff --stat 4404b98 1f209e1 -- src`: only
  src/page/modules/widthMode.ts (base change on code block breakout, claim 6 of the previous judgment).
- verify-124a348.md claim 6: "PR images (cream, dark hover shots): captured at 4404b98, product unchanged since."

R. Review line "the move to 1f209e1 approved at 1f209e1 (one commit left out with the clip changes...)". PASS.
- `chantier log CR-503`: `2026-11-25T22:09:19Z driver note note=move 124a348..1f209e1 (restack) inspector approved at 1f209e1`.
- The left-out commit: previous claim 1 (range-diff: commit 124a348 skipped).

Other proof also read: integration-a1.log:1556 `PASS real-input screenshot: diagrams/r01-live-chart-hover` (Test plan, Real window);
`gh pr checks 523`: static, static-windows, visual, viewer-graph, checks, report pass (run 45706072543).

## Carried from the previous judgment at 1f209e1 (same head, nothing moved)

- Claims 1 to 10: move patch-id, unit and chart page tests, no `myst-vega-image`, clips left in the base, requirements and
  changelog, unchanged chart code, real window, PR checks, local gate note, Review note.
- Claim 11, description rest: draft, base, Changes against the 40 changed files, no failing role name.
- From 124a348: picture content, byte identity of the uploaded images, no username or home path; theme-switch take;
  tests failing on the previous code; Summary, Deliverables diagram, Impacts, Blast radius; the CSSOM style gap.
- Note, not re-judged: the pictures sit in Deliverables and Impacts is one line referring to the visible change.

No before/after capture again and no gate run: nothing moved.
