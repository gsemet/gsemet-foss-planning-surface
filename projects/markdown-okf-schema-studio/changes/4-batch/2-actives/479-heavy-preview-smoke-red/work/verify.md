Head: 0303eaf7aa8ef99c145efa902758671ce6db1fd1

Verdict: VERIFIED (re-judged after the Review box fix)

Claims (judged at 0303eaf unless carried):

1. Heavy run green at the head. VERIFIED at 0303eaf.
   `gh run view 45244689744 --json headSha,conclusion,jobs` -> headSha 0303eaf7..., conclusion success;
   integration, stress, visual, static, static-windows, viewer-graph, report, gallery, checks: success.
2. Local gate. carried from 8b86515: work/gates/preflight-8b86515.log EXIT 0; the move was a clean rebase on main
   (per the brief; `git diff --stat origin/main...HEAD` shows the same 14 files, 4 commits); CI at the new head is green (claim 1).
3. Fix matches spec. carried from 8b86515 (diff verified earlier: pendingShow in rendering.ts, awaited in previewManager.ts requestDocument; tests; no CI file touched).
4. PR #495 body at 0303eaf (`gh pr view 495 --json body`): renders; Summary, Deliverables, Changes match the diff stat; heavy run link present; Known gaps rewritten and consistent (no stale UNVERIFIED); no images. OK, EXCEPT:
   - FAIL: the Review box says `Review: approved at 0303eaf (round 6 inspector, rebased)`. `chantier log CR-479` has no note of an approved pass at 0303eaf
     (approvals are at 3a32623 and "committed as 8b86515"; the 0303eaf entries are only `ship` lines; no `carry` event, `grep -i carry` finds none).
     Rule: a Review box needs a Driver note of an approved pass at the cited SHA. Fix: cite `carried from 8b86515` (or 3a32623) after recording the carry, or have a note of the approval at 0303eaf.

Re-check at 0303eaf: `gh pr view 495 --json body` line 59 now reads "Review: approved at 8b86515 (round 6 inspector APPROVE), carried over the clean rebase onto main to 0303eaf".
`chantier log CR-479` has "r6 approved at 3a32623, committed as 8b86515" and the rebase note "inspector APPROVE of round 6 at 8b86515 carries". The earlier failure is fixed; claim 4 now VERIFIED.

Re-check 2 at 0303eaf: Review box line 59 reads 'approved at 0303eaf (round 6 inspector APPROVE, carried over the clean rebase onto main)'; log note 19:20:39 records the carry to 0303eaf. VERIFIED.
