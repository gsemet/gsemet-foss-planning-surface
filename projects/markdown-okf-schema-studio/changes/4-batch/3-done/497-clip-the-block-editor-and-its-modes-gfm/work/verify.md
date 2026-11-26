# CR-497 verify

Head: af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea

Description pass at the same head as the previous judgment (this CR's `work/verify.md` at af4a4aa,
NOT VERIFIED on claim 12 only). The branch has not moved; one bullet of the posted description was
reworded. Claim 12 is judged again, claims 13, 15 (CI line) and the head are rechecked; the others
are carried from that report, because neither the head nor the text they judge changed.

## Head and edit

1. Head and base. `git rev-parse HEAD` = af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea;
   `git status --porcelain` empty; `git ls-remote origin`: CR branch af4a4aa, cr-496 d386ff61,
   main 17b779d. `gh pr view 518`: draft true, base the cr-496 branch, headRefOid af4a4aa.
   VERIFIED
- The edit. `gh api graphql ... userContentEdits` (`verifier/pr-edits.log`), diff of the version of
  2026-11-26T01:54:35Z (the one the previous report judged) against 02:32:17Z (current): one line,
  `-- At 11 s and in the last frame the faint hover outline and block handle of the paragraph still
  fade after Escape (no editor is open); kept as filmed.`
  `+- After Escape at 11.3 s the paragraph's hover outline and block handle show, then fade up to the
  last frame (no editor is open); kept as filmed.`
  `diff` of `gh pr view 518 --json body` against `work/pr-body.md`: only a trailing blank line.

## Carried (judged at af4a4aa by the previous report; head unchanged, text not edited)

2. carried from af4a4aa. Move 1858396..af4a4aa: `git diff --stat 1858396 HEAD --
   docs/demo-video/clips/block-editor-modes` empty (tree e2f79d4b at both); `git range-diff
   4a47151e..18583968 d386ff61..HEAD`: commit 1 identical, commit 2 differs by the conflict
   resolution only (both sides kept in check.test.mjs, storyboard.test.mjs, siteClips.test.ts).
   `just check-no-merge-commits` passed. VERIFIED
3. carried from af4a4aa. Scope: `git diff --stat d386ff61 HEAD`: 23 files, +764 -2; no src,
   requirements, skills, CHANGELOG, clip-kit/lib, guideline, package.json, .github, justfile or
   scripts change besides check.test.mjs and storyboard.test.mjs; editing.md gains the GIF in the
   palette modes item; one site test with one `@tests_req SwRS-MDOKFSTUDIO-CORE-095`. VERIFIED
4. carried from af4a4aa. `just clip-kit-test`: 49 tests, 49 pass, 0 fail, 0 skipped. VERIFIED
5. carried from af4a4aa. `node --import ./scripts/register-myst-patches.mjs --test
   out/test/site/siteClips.test.js`: 20 pass, 0 fail. VERIFIED
6. carried from af4a4aa. `just check`: exit 0; boundaries and limits passed; unit 5303 tests, 5296
   pass, 0 fail, 7 skipped; security 107/107; pytest 205 passed; requirements 0 errors, 26
   warnings (`verifier/just-check-af4a4aa.log`). VERIFIED
7. carried from af4a4aa. `just --unstable --fmt --check`, `just audit` ("found 0
   vulnerabilities"), `just sphinx-check`, `just requirements-report` (`"errors": 0`): exit 0
   (logs in `verifier/`). VERIFIED
8. carried from af4a4aa. `just requirements-update`: exit 0, "0 indexes updated, 0 requirement OKF
   projections updated", tree clean. VERIFIED
9. carried from 1858396 (through the previous report: clip folder unchanged). check.json
   `passed: true`, "scenario verify passed"; MP4 and WebM 1280x720, 15 fps, 12.000 s; GIF 960 px,
   12 fps, loop 0; seam 0.995729; playback 1.004; win32. The base kit's `checkClip` at af4a4aa on
   the committed outputs: 20 lines ok, passed true. VERIFIED
10. carried from 1858396 (files unchanged): shipped stage identical to the planning stage (`cmp`);
    clip.md draft status; take times within 0.06 s of the drafted marks. VERIFIED
11. carried from af4a4aa. The look (contact sheet, GIF and MP4 frames from the PR's links): edit
    mode, GFM then MyST, badges, both texts, marks in turn, no editor in the first and last frames,
    no username or home path. Motion, rhythm and the loop as watched not checked (Known gaps aside,
    the description says they are judged by watching; owner approval in 02-answers.md). VERIFIED

## PR description as posted

12. judged at af4a4aa. Reworded bullet: "After Escape at 11.3 s the paragraph's hover outline and
    block handle show, then fade up to the last frame (no editor is open); kept as filmed."
    - Media are the head's: `sha256sum` of the GIF, MP4, WebM = `git lfs ls-files -l` oids
      (dd4bf38f..., 8e2d9390..., 3bd121f7...).
    - Escape at 11.3 s: `scenario.mjs:286-287` `await until(11.3); await
      page.keyboard.press("Escape");`; clip.md line 70 "Escape at 11.3 s".
    - MP4 frames (ffmpeg extract, crop 920x60 at 170,265, frames 168 to 179;
      `verifier/evidence/after-mp4-tail-af4a4aa.png`): 168 and 169 (11.20, 11.27 s) editor open;
      170 (11.33 s) editor gone, outline and handle show; 171 to 175 full; 176 to 179 fade; frame
      179 still faint, no editor. GIF frames 135 to 143 show the same.
    - Per-frame colour distance from frame 0 (mean absolute RGB difference of a fixed region, frames decoded by ffmpeg; output in
      `verifier/escape-measure-af4a4aa.log`), handle region: MP4 165-169 12.65 (editor), 170-175
      115.6, 176 73.78, 177 42.43, 178 18.76, 179 4.72; WebM 170-175 114.6, then 74.02, 43.45,
      18.07, 4.01; GIF 136-140 114.7, 141 74.48, 142 19.24, 143 4.92. Outline top, MP4: 171-175
      about 75, then 49.11, 26.13, 11.83, 3.00.
    VERIFIED
13. judged at af4a4aa. `gh api .../pulls/518` body_html: h2 Summary, Deliverables, Changes,
    Impacts, Blast radius, Test plan, What the clip proves, Deviation from the feature clip
    process, Autonomous decisions, Known gaps, Internal references; 1 image; 7 boxes, 7 checked;
    STALE 0, UNVERIFIED 0; the new bullet renders as one list item. Links, carried from af4a4aa
    (URLs not edited): GIF, MP4, WebM, clip.md 200, media sha256 equal the LFS oids; internal ids
    only under Internal references; Claude Code line last. VERIFIED
14. carried from af4a4aa. Summary, Deliverables, Changes, Impacts, Blast radius match the diff
    (claims 2, 3, 9, 11). "The code has no render per mode": viewState.ts comment. VERIFIED
15. carried from af4a4aa. Test plan: new tests (3, 4, 5); requirements (3, 8); changelog (`docs:`
    and `test:` commits only); local gates (4, 6); evidence line carried from 1858396 (9). Review:
    `chantier log` (read again) note 2026-11-26T00:56:11Z "move 1858396..af4a4aa (restack)
    inspector approved at af4a4aa". CI, run again: `gh pr checks 518`: static, static-windows,
    visual, viewer-graph, report, checks pass (run 45728459032); the rest skipping. VERIFIED
16. carried from af4a4aa. Other statements (take verify.json: 9 github, then 9 github and 19 myst,
    outerHTML identical, 17 boxed, reset path not exercised; file on disk unchanged; Down in
    take.json; CLIP_SCRATCH and port 9497; no kit lib change; owner approval; Windows only).
    VERIFIED
17. carried from af4a4aa. Known gaps: 17 of 19 boxes, setup reset, macOS/Linux; before/after pairs
    captured (`verifier/evidence/before-after.md`, base d386ff61, head af4a4aa), none missing. The
    earlier failed claim 12 was fixed, not accepted, so it needs no bullet. VERIFIED

Expected `ship` line "no long gate passed at af4a4aa": no long gate is configured. No long gate and no
`just preflight` target itself was run; claims 6 and 7 run its Windows static parts one by one.

VERIFIED
