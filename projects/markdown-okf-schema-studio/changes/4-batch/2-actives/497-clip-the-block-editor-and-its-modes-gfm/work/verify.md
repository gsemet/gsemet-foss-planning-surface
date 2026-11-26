# CR-497 verify

Head: af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea

Previous judgment: 185839681b07add2de5afe33b51b1f9f742273d9 (VERIFIED). Move judged: restack onto CR-496
`d386ff61a3d5a2cda0cb54130a5ffea5600a3793`. Claims judged at af4a4aa unless marked `carried from 1858396`.
Verdict: one claim of the PR description is false (claim 12). Everything else holds.

## Head and move

1. Head and base. `git rev-parse HEAD` = af4a4aa...; `git status --porcelain` empty; `git ls-remote`
   of the CR branch = af4a4aa, of cr-496 = d386ff61 (ancestor of HEAD), main = 17b779d.
   `gh pr view 518`: OPEN, draft true, base the cr-496 branch, headRefOid af4a4aa, MERGEABLE.
   `just check-no-merge-commits`: passed (14 commits since origin/main, no merge commit). VERIFIED
2. The move. `git diff --stat 1858396 HEAD -- docs/demo-video/clips/block-editor-modes` empty (tree
   e2f79d4b at both). `git range-diff 4a47151e..18583968 d386ff61..HEAD`: commit 1 identical
   (c2adb8e9 = c86a68f5), commit 2 differs by the conflict resolution of conflicts.md only (both
   sides kept in check.test.mjs, storyboard.test.mjs, siteClips.test.ts). VERIFIED
3. Scope. `git diff --stat d386ff61 HEAD`: 23 files, +764 -2. Over src, requirements, skills,
   CHANGELOG.md, clip-kit/lib, guidelines, package.json, .github, justfile, scripts, `--name-only`
   lists only check.test.mjs and storyboard.test.mjs. editing.md diff: the GIF under the
   "Vega-Lite and Vega chart commands." sentence, indented in the item, the rest a new paragraph.
   One added site test with one `@tests_req SwRS-MDOKFSTUDIO-CORE-095`. VERIFIED

## Tests and static stage (all run at af4a4aa)

4. `just clip-kit-test`: 49 tests, 49 pass, 0 fail, 0 skipped, incl. the three modes tests. VERIFIED
5. `node --import ./scripts/register-myst-patches.mjs --test out/test/site/siteClips.test.js`
   (after `just check` compiled): 20 pass, 0 fail, incl. the modes clip test. VERIFIED
6. `just check`: exit 0. Boundaries passed (406 modules); limits passed (1340 files, 0 baseline);
   clip kit 49/49; unit 5303 tests, 5296 pass, 0 fail, 7 skipped; security 107/107; pytest 205
   passed; requirements 0 errors, 26 warnings; 0 files would change. Log
   `work/verifier/just-check-af4a4aa.log`. VERIFIED
7. Rest of the Windows static stage: `just --unstable --fmt --check` exit 0, no output;
   `just audit` exit 0 (npm: "found 0 vulnerabilities"); `just sphinx-check` exit 0 (last pytest
   run 4 passed); `just requirements-report` exit 0 (`"errors": 0`). Logs in `work/verifier/`.
   Tree clean afterwards. VERIFIED
8. `just requirements-update`: exit 0, "0 indexes updated, 0 requirement OKF projections updated",
   tree clean. VERIFIED

## The clip

9. check.json, carried from 1858396: clip folder unchanged. `passed: true`, "scenario verify passed";
   MP4 and WebM 1280x720, 15 fps, 12.000 s; GIF 960 px, 12 fps, loop 0; seam 0.995729; playback 1.004;
   win32, vsix, 20 lines ok. Judged again against the base's kit (it moved): the kit's `checkClip`
   on a copy of the committed outputs, with the take records read from C:/okfclip497: 20 lines ok,
   passed true, seam 0.99573, rate 1.004; only difference is the name of one line, "mp4 duration
   within 5 to 30 s" (was "5 to 12 s"). `parseClip` of the committed clip.md equals render
   `story.json` on length, size, fps, captions, badges, zoom, marks, logo, expectedPaste. VERIFIED
10. Stage and storyboard, carried from 1858396 (files unchanged): shipped stage identical to the
    planning stage (`cmp`); clip.md draft status; draft/live differences are those the spec section 2
    asks for or the description names; take times within 0.06 s of the drafted marks. VERIFIED
11. The look, at af4a4aa (contact-sheet.png, GIF and MP4 frames from the PR's links): edit mode,
    GFM then MyST, badges, both texts, marks in turn, no editor in the first and last frames, no
    username or home path on screen. `Select-String` for the user name over the clip folder: 0
    matches. Not checked: motion, rhythm, the loop as watched (Known gaps and the description say
    judged by watching; the owner's approval is in 02-answers.md). VERIFIED

## PR description as posted (`gh pr view 518`; equals work/pr-body.md but a trailing blank line)

12. Autonomous decisions, "At 11 s and in the last frame the faint hover outline and block handle of
    the paragraph still fade after Escape (no editor is open)". False at 11 s. The scenario and
    clip.md press Escape at 11.3 s. Command: `ffmpeg -i <downloaded MP4> -vf select=eq(n,165)+...`
    (evidence/after-mp4-end-af4a4aa.png): at 11.0 s and 11.2 s the block editor is open (MyST
    palette, text box, Done, Cancel); it is closed from 11.33 s; GIF frame 132 (11.0 s) also shows
    it open. The "11 s" comes from the contact sheet's tile labelled 00:00:11.000: `showinfo` gives
    that tile checksum 3D1DB9E5, which is the MP4 frame at 11.4667 s. The last-frame half holds.
    Fix (description only): for example "After Escape at 11.3 s the paragraph's hover outline and
    block handle show, then fade to the last frame (no editor is open); kept as filmed."
    NOT VERIFIED
13. Rendering and links: `gh api` body_html has all sections (Summary to Internal references), 1
    image, 4 links, 7 checked boxes; no STALE or UNVERIFIED mark. `curl` of GIF, MP4, WebM, clip.md
    at af4a4aa: 200; sha256 of the three media equal their `git lfs ls-files -l` oids; sizes equal
    check.json. Internal ids only under Internal references; Claude Code line last. VERIFIED
14. Summary, Deliverables, Changes, Impacts, Blast radius match the diff (claims 2, 3, 9, 11;
    no src file; extension unchanged). "The code has no render per mode":
    src/session/features/viewState.ts comment, mode changes buttons only. VERIFIED
15. Test plan: new tests (3, 4, 5); requirements (3, 8); changelog (commits are `docs:` and `test:`);
    local gates 49 tests and `just check` (4, 6); evidence line carried from 1858396 (9; the order
    "after the last clip.md edit" is not provable from files alone: out/render497.log shows render
    then check, 20 ok, and the rendered story equals the committed clip.md rows); review: `chantier
    log` note 2026-11-26T00:56:11Z "move 1858396..af4a4aa (restack) inspector approved at af4a4aa";
    CI: `gh pr checks 518` static, static-windows, visual, viewer-graph, report pass (run
    45728459032 at af4a4aa). VERIFIED
16. Other statements: take verify.json (9 github; then 9 github and 19 myst; outerHTML compare
    identical; 17 boxed; reset path none), scenario verify checks the file on disk unchanged and
    passed; Down press in take.json; CLIP_SCRATCH in out/take497.log (C:\okfclip497), port 9497 in
    that profile's DevToolsActivePort; no kit lib change (3); owner approval in 02-answers.md; macOS
    and Linux unproved (host.json win32). VERIFIED
17. Known gaps: 17 of 19 boxes, setup reset, macOS/Linux; before/after pairs captured
    (`work/verifier/evidence/before-after.md`, base d386ff61, head af4a4aa), none missing. VERIFIED

Expected `ship` line "no long gate passed at af4a4aa": no long gate is configured. No long gate and no
`just preflight` target itself was run; claims 6 and 7 run its Windows static parts one by one.

NOT VERIFIED
