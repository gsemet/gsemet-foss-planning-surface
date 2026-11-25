# Verify CR-500

Head: b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5

All claims judged at b0e6c6d9 (PR 516, draft, base chantier/batch-09/cr-493-...). Images and video not opened (brief); motion and rhythm are not claimed.

1. `just clip-kit-test` at b0e6c6d9: tests 39, pass 39, fail 0; includes "the shipped export-html clip.md reads as the clip the owner reviews" and "the stage of the export-html clip holds the page the clip claims". Held.
2. `docs/demo-video/clips/export-html/check.json`: passed true, length 18, mp4/webm 1280x720 15 fps 18.000 s, GIF 2976631 bytes (2.84 MB, ladder step 1, 10 fps 960 px), loopSeamSsim 0.989751, verifyPassed true, playbackRate 1.004, platform win32, extensionSource vsix, "scenario verify passed" ok, "Studio in reading mode at the start" ok. Held.
3. `git ls-files docs/demo-video/clips/export-html`: 22 files, no release.png, no team-handbook.md; `git grep -n team-handbook`: empty (exit 1). Held.
4. Stage: `stage/platform-report.md` LF only (0 CR), identical to the storyboard draft modulo CR (diff empty); clip.md front matter `status: draft for the owner's review`, date 2026-11-25, Length 18.0 s, three sections with times 0-5.8, 5.8-10.0, 10.0-18.0, Zoom page hold to 17.0 s, marks 11.8-13.0, 14.0-15.2, 15.4-16.6, Text 3 as spec, measured-times and "Not checked by the author" notes present. toolbar.md alt text is the spec's. Held.
5. PR 516: draft true, base cr-493 branch. GIF, MP4, WebM and clip.md URLs at the head sha: curl -IL gives HTTP 200 for each. Body holds "Deviation from the feature clip process", Known gaps, Autonomous decisions, and matches the diff (10 non-png files: storyboard test, clip folder, toolbar.md). `gh pr checks 516`: static, static-windows, visual, viewer-graph, report, checks pass; others skipping (heavy jobs by design). Held.

Not run: `just check`/preflight (cited in PR body as run by the author; CI static and static-windows green at this head).

VERIFIED

## Description-only pass at b0e6c6d9c6d69b07d1f95724033b6c1ed9bf1df5

Posted PR 516 body equals work/pr-body.md (diff: one trailing blank line only); links use b0e6c6d; PR head b0e6c6d; `gh pr checks 516`: static, static-windows, visual, viewer-graph, report, checks pass, others skipping; Review box matches log note "r2 inspector approved at da86d6e"; Known gaps as in the template. VERIFIED.
