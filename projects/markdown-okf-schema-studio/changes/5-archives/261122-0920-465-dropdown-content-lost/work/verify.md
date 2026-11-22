# Verify CR-465

Head: 18a2ea9c8ad9b7d767037bdaf32352bda750d654

Gate pass: work/gates/20261122-094307.log, first line `gate CR-465 ... head 18a2ea9c8ad9b7d767037bdaf32352bda750d654`, last line `result: pass at 18a2ea9c8ad9b7d767037bdaf32352bda750d654` (just preflight, Windows static stage). CI at the head green per the Driver's note (heavy run 45004711104).

## Claims

1. New tests pass at 18a2ea9c. Command (worktree): `node --import ./scripts/register-myst-patches.mjs --test --test-name-pattern="dropdown" out/test/core/render/mystFeatures.test.js out/test/page/runtimeLineMarkerPlacement.test.js` (after `tsc -p .`). Output: 4 tests, pass 4, fail 0, including "the dropdown directive keeps its body in both fence styles" and "a line in the body of a closed dropdown directive opens it and is marked, from the real render". (Without the patch loader the run fails on markdown-it-dollarmath: that is the project's runner, scripts/node-test.mjs, which registers it.)
2. Before/after render, light and dark. Before at 1a5b98bb: `details` elements print `<details></details>` x3. After at 18a2ea9c: `<details class="admonition dropdown" data-line="5" data-end-line="9"><summary class="admonition-title">Closed colon dropdown</summary><p data-line="6" ...`; the `:open:` one has `open=""` (data-line 11-15); the untitled one has summary "Details" (data-line 17-19). Pictures opened and looked at: work/verifier/evidence/{before,after}-{light,dark}.png; after shows the three titles, body of the open one visible, closed ones collapsed; before shows three bare "Details" and no body. See work/verifier/before-after.md. No username or home path visible.
3. Source untouched: the fix only changes render rules (git diff origin/main...HEAD --stat: mystNormalize.ts, mystBlockTransforms.ts and tests/docs; no edit-path file).
4. PR description (gh pr view 479 body at 18a2ea9c): identical to work/pr-body.md modulo a trailing newline; sections render; Summary, Deliverables and Changes match the diff (9 files: CHANGELOG, requirements log + SwRS MYST-006 + index, skill, 2 src files, 2 tests). No image attached yet. Pending for the Driver: the Deliverables line "Screenshots before/after: **UNVERIFIED:** not captured yet" must be replaced by the captured evidence, and the Test plan boxes and Review box are the Driver's; Known gaps bullet for HTML export is present. Judged as acceptable until the placeholder is filled; the description must not ship with "UNVERIFIED not captured yet" now that the pairs exist.
5. Known gap, not failed: HTML export of the new dropdown not run (given).

VERIFIED

## Description pass at 18a2ea9c8ad9b7d767037bdaf32352bda750d654

Head: 18a2ea9c8ad9b7d767037bdaf32352bda750d654

6. Posted body (`gh pr view 479 --json body`) judged at 18a2ea9c: template sections present (Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps, then fold with Changes, Impacts, Test plan, Internal references); CR-465 only under Internal references; no role names; Impacts has before/after evidence (three empty details versus bodies, screenshots in Deliverables); Known gaps lists HTML export not run.
7. Images: `curl -w %{http_code}` on the four raw URLs (assets commit edabe18c) returns 200 image/png; sha1 of each equals the file in work/verifier/evidence/ (before/after, light/dark), which claim 2 opened and checked for content and no username or home path.
8. Review box: Driver log has "r2 approved at 08b64c02 ... committed as 4a1ced2b", matching "approved at 4a1ced2".
9. CI: `gh pr checks 479` all pass or skipping at 18a2ea9c (run 45004689656); heavy run 45004711104 `success`, headSha 18a2ea9c, event workflow_dispatch.
10. Claim 4's placeholder objection is resolved: no UNVERIFIED or STALE mark remains.

VERIFIED
