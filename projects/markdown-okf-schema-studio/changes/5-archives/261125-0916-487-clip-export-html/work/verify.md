# Verify CR-487 clip-export

Head: 743d2741f44228227f32e96bf0e2e1c5861675c6

All claims judged at 743d2741f44228227f32e96bf0e2e1c5861675c6.

1. `just clip-kit-test`: 26 tests, 26 pass, 0 fail (includes "the shipped export-html clip.md reads as the clip the owner reviews").
2. Site test, after `npm run compile`: `node scripts/node-test.mjs unit out/test/site/siteClips.test.js` gives 10 pass, 0 fail, including "the shipped toolbar page plays the export clip as video".
3. check.json (read at head): passed true; MP4 and WebM 1280x720 at 15 fps, 12 s = Length 12 within one frame; GIF 960 px, 12 fps; loop seam SSIM 0.98870; "Studio in reading mode at the start" ok (off); paste false; verifyPassed true; playbackRate 1.003; platform win32; extensionSource vsix; all 20 checks ok.
4. Viewed contact-sheet.png, frames/save-dialog.png, frames/release.png, frames/04-mark-1.png: Dark Studio with the expanded toolbar and Export tooltip; save dialog with `team-handbook.html`, path `C:\okfclip\export-html\workspace\`, no user name; palette with the badge `Ctrl Shift P / ⇧⌘P`; browser page in Dark with flowchart and tabs; Text 1 during the export, Text 2 during the zoom; mark 1 on the flowchart, mark 2 on the Release panel after the click; no dirty tab. Not checked: motion, rhythm, the loop as watched (owner's). A thin title-bar strip at the top of zoomed frames is declared in the PR body.
5. Preflight: work/gates/preflight.log ends `ci-static: passed`, `EXIT 0`, and holds the site test line for the export clip. `gh pr checks 508`: static, static-windows, visual, viewer-graph, report, checks pass; rest skipping (by design on a PR); run 45530003036 at head 743d2741.
6. PR 508 (draft, head 743d2741): body equals pr-body.md (diff: one trailing newline). Summary, Deliverables, Changes match the diff stat (clip folder, 2 test files, toolbar.md GIF). GIF and MP4/WebM links name the head sha; the draft state and the owner's storyboard review are stated. No image shows a user name or home folder (frames viewed). Known gaps: PR body lists no UNVERIFIED claim; none required. Review box: unchecked in the Test plan, no claim made.

Not claimed: the take was not retaken (by the brief).

VERIFIED (code pass)

## Description pass (PR 508 body as posted), judged at 743d2741f44228227f32e96bf0e2e1c5861675c6

Command: `gh pr view 508 --repo gsemet/markdown-okf-schema-studio --json body,headRefOid,isDraft` -> headRefOid 743d2741f44228227f32e96bf0e2e1c5861675c6, isDraft true.
- OK: image, MP4 and WebM links name the head SHA; sections of the project template present; Known gaps present; no CR, batch or round id in the body; Summary, Deliverables, Changes match `git diff 8197e4fd..HEAD --stat` (clip folder, 2 clip-kit tests, siteClips test, toolbar.md); Review box `approved at 743d274` matches the log notes `r2 approved at 8197e4fd..., committed as 743d2741`; `verified at 743d274` matches the verdict at that head.
- FAIL: Test plan line "Review: inspector approved at 743d274" names an agent role (Inspector) as the doer of the work. `.agents/guidelines/pull-request.guidelines.md` line 17 forbids agent roles in the body; chantier pr-template "The rules" says the same outside Internal references. Fix: "Review: approved at 743d274".

NOT VERIFIED (description)


## Description pass 2 (posted body of PR 508, head 743d2741f44228227f32e96bf0e2e1c5861675c6)

Command: gh pr view 508 --json body,headRefOid (headRefOid = 743d2741f44228227f32e96bf0e2e1c5861675c6).

- OK: Review line now reads "Review: approved at 743d274, verified at 743d274"; no role name in the body. Matches log notes (r2 approved at 8197e4fd, committed as 743d2741; verdict at that head).
- OK: image, MP4, WebM links name the head SHA; sections present; Known gaps present; Summary, Deliverables, Changes match git diff 8197e4fd 743d2741 --stat (clip folder, 2 clip-kit tests, siteClips test, toolbar.md).

VERIFIED (description)
