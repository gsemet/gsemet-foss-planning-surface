# Verify CR-448 (blank-line runs inside lists)

Head: ea5c383fb534a683d42a5caa9dbd72a9c5390ccf

Pass 2 at ea5c383 (rebased twice onto main, base now 9c70477a). Claims 1-5 below were judged at 8ecec6bb8d1d497ecb23c191a71313bae00919cf and are carried from 8ecec6b: `git range-diff 8ecec6b...ea5c383` shows `1: 8ecec6bb = 4: ea5c383f feat(editor): show blank-line runs inside lists as blank-lines blocks` (the other three commits are main's, new in the range), and `git diff --stat 8ecec6b ea5c383 -- src` prints nothing: the CR's patch and src are unchanged; the gate pass `work/gates/20261121-140123.log` (first line `gate CR-448 ... head 8ecec6bb...`, `result: pass`) is carried the same way. CI at ea5c383: `gh run view 44909893956 --json headSha,conclusion,jobs` gives `headSha ea5c383fb534a683d42a5caa9dbd72a9c5390ccf`, `success`, jobs static, static-windows, visual, integration, stress, report, gallery, checks all `success` (heavy run, at the pushed head). `gh pr view 463 --json headRefOid` gives `ea5c383f...`.

## Description pass at ea5c383: NOT VERIFIED

Command: `gh pr view 463 --json body --jq .body`, diffed against `work/pr-body.md`.
Output: the posted body differs from `work/pr-body.md` on lines 33 and 84-88. The forge still says `after at 1aa7966`, `Local gates at 1aa7966`, `Evidence: ... after at 1aa7966`, `Review: approved at 15a0ef0`, `Verified at 1aa7966`, `CI green at 1aa7966: pending`. `1aa7966` is not in ea5c383's history (an earlier rebase's head), so those proofs name a SHA that is neither the head nor a carried one. The edited `work/pr-body.md` was not posted.
Also in `work/pr-body.md` (fix before posting): "Review: approved before the commit" names no SHA (the Driver's notes: `r2 inspector approved at 15a0ef09e3763f7ed52ce60130da8ccfaba1ed5b`; write `approved at 15a0ef0`, carried to ea5c383 by the range-diff above); "long gate `just preflight` pass at `ea5c383` (carried from `8ecec6b`)" reads as run at ea5c383: say `pass at 8ecec6b, carried`.
Sections, Deliverables, Changes and Known gaps match the diff and the known gap (no undo after save for "More", "- c" between items and "- c" in an item). Images: the five attached are the ones of the evidence pairs at 8ecec6b (carried from 8ecec6b, same patch); not re-downloaded in this pass.

## Claims 1-6 (judged at 8ecec6bb8d1d497ecb23c191a71313bae00919cf, carried from 8ecec6b: patch unchanged by range-diff)

1. Core, protocol, render, page and session tests of the spec pass at the head.
   Command: `npm run compile`, then `node scripts/node-test.mjs unit out/test/core/mapping/blankRunInList.test.js out/test/core/mapping/listItemIndent.test.js out/test/core/protocol/pageToHost.test.js out/test/core/render/blankRunsInLists.test.js out/test/page/runtimeBlankLines.test.js out/test/session/blankRunInListHost.test.js out/test/session/previewManager.test.js out/test/site/e2eGroups.test.js`
   Output (`work/verifier/unit.log`): `ℹ tests 158`, `ℹ pass 158`, `ℹ fail 0`. The files cover each spec line: indent function (LF/CRLF/CR), insertion and paste with `itemLine` with a re-render asserting one list, removal, `itemLine` protocol validation, page placement/arrows/Shift/click/paste/Delete/patch survival, session save/autosave/cancel/stale. VERIFIED.
2. `test/core/render/blankRunsInLists.test.ts` (judged for what it proves). It renders a real list text and asserts the run list `4-6 10-12 18-19 22-23 26-27`, the `ul` range `[3,23]` holding the first runs strictly, `li` ranges starting at marker lines, the fence's `code` range holding its run, and the `aside` as top-level holder of the admonition run. It passes on old code because no render code changed: it proves the real renderer gives the page the ranges its placement rule reads (spec "Render"), not new behaviour. Accepted as a guard test; documented in the PR body. VERIFIED.
3. Page behaviour in edit mode with the real bundle and stylesheet: two blank-lines blocks, each in the right `li`, none in the fence; selected block shows its Delete button at the left edge with no overlap; reading mode shows none; typing "More" and an autosave keeps the editor in an `li` of the re-rendered list.
   Command: `npm run visual:render`, then `uv run --no-sync --group docs python test/visual/capture.py --workers 1 --scenario block-editing/v44-... v47 v48 v49 v50`.
   Output: `passed: block-editing/v44-blank-lines-block-light-900`, `v47-blank-lines-in-lists-light-900`, `v48-blank-lines-in-lists-selected-dark-900`, `v49-blank-lines-in-lists-reading-light-900`, `v50-blank-lines-in-lists-typing-light-900`; `{"status": "passed", "scenario_count": 5, "screenshot_count": 5}`. Images in `work/verifier/evidence/` (opened and looked at: each shows what its description says, no username or home folder). VERIFIED.
4. The new visual checks fail on the old code (constitution, section 3).
   Command: same render and capture on a detached worktree of base e0c7836c with the head's fixture, scenarios and capture script copied in.
   Output: `failed: ...v47`, `failed: ...v48`, `passed: ...v49` (reading mode, expected), `failed: ...v50`; `93-blank-lines-in-lists--light--sticky-3--default.html: blank lines in lists: 0 blocks (0 in the fence), expected 2 and none in the fence`. VERIFIED. Not run on the base: the core, page and session unit tests (they import modules the base lacks, so they cannot run there); the PR body says they fail on the previous code and I did not re-prove it for them.
5. Real VS Code integration (spec "Integration": delete between items, save "More" in an item, "- c" between items, "- c" in an item, LF and CR LF) passes at the head.
   Command: `gh run view 44907374042 --json headSha,jobs` (heavy run on the branch).
   Output: `sha 8ecec6bb8d1d497ecb23c191a71313bae00919cf`, jobs `integration success`, `stress success`, `visual success`, `static success`, `static-windows success`; log (`work/verifier/ci-heavy.log`) `STEP start: blank-lines`, `STEP done: blank-lines (6416 ms)`. The test file (`test/integration/blankLines.test.ts`) has the four saves with expected text per eol and the delete with undo. VERIFIED. Gap noted below.
6. PR #463 at head: `gh pr view 463 --json headRefOid,isDraft,statusCheckRollup`: `h 8ecec6bb...`, draft, `static`, `static-windows`, `visual`, `viewer-graph`, `report`, `checks` all `SUCCESS` on the pull_request run. VERIFIED.

## Not judged here

- The PR description as posted (no screenshots attached yet; Review and CI boxes unchecked; Known gaps still says the integration steps "were not run locally", which stays true but CI has now run them). Judge it on the description pass after the images are attached.
- The Review box (no `carry`/review note was read in this pass).

## Gaps (do not change the verdict)

- The integration steps for "More" in an item, "- c" between items and "- c" in an item do not press undo after the save (spec Integration point 2 asks that one undo brings the run back); only the delete steps do. The session tests cover the single-edit write.
- In the capture, the blocks of the first item are narrower than the second item's (right edge ~1487 vs ~1655 px): the floating toolbar at the top right narrows blocks beside it; the visual check on width passed.

NOT VERIFIED
