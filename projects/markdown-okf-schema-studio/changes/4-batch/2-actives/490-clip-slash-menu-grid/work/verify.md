# Verify CR-490 clip-slash-grid

Head: d5e68210b4c9392e3faf66a561567b835dc3096a

All claims judged at d5e68210 unless noted.

1. Evidence 1, kit tests: `fnm exec -- just clip-kit-test` -> `tests 26, pass 26, fail 0`, including "the shipped slash-menu-grid clip.md reads as the clip the owner reviews" (parses shipped clip.md, EXPECTED vs the Expected result block) and the `checks` test (diff adds `resolveChecks(grid.checks)` = `{editMode:"on", paste:false}`). VERIFIED.
2. Evidence 1, site test: `fnm exec -- npm run compile`, then `node --import ./scripts/register-myst-patches.mjs --test out/test/site/siteClips.test.js` -> `pass 10, fail 0`, "the shipped slash menu page plays the grid clip as video" passes; it reads the shipped docs/user/slash-menu.md. VERIFIED.
3. Evidence 1/4, `just check`, `ci-static`, preflight: gate logs `work/gates/check.log` (first line `d5e68210b4c9392e3faf66a561567b835dc3096a`), `preflight.log` (first line the same SHA; ends `ci-static: passed`, `exit 0`); `git status --short` clean after my runs. I did not rerun them. VERIFIED (by the gate logs at the head).
4. Evidence 2, `check.json` at the head: `passed: true`; mp4 and webm 1280x720 15 fps, mp4 11.533 s vs Length 11.5 s; gif 960 px, 12 fps, loopCount 0; `loopSeamSsim` 0.996812; check "Studio in edit mode at the start" ok with no paste line; `verifyPassed: true`; `playbackRate` 1.004; `platform: win32`, `extensionSource: vsix`; all 19 checks ok. VERIFIED. The take itself is not repeatable by me: I read the committed file, not a fresh take.
5. Evidence 3, images looked at (contact-sheet, first-last, six key frames):
   - `slash-menu`: menu at the caret under `/grid`, Grid highlighted, Table below. OK.
   - `grid-form`: "Insert grid", Columns 2, Gutter 2, Cards 2. OK.
   - `01-selected`: `::::{grid} 2` text, "Card 1" selected. OK.
   - `02-pasted`: box closed, two cards, keycaps `Ctrl Enter / ⌘ Enter`. OK.
   - `03-zoomed`, `04-mark-1`: two cards side by side, orange outline around both in 04. OK.
   - Text 1 in section 1, Text 2 in section 2, logo top right. OK.
   - No tooltip, no username or home path seen (window title "onboarding.md - workspace").
   - Dirty tab: `slash-menu.png` (and contact-sheet frame at 4.79 s) shows the tab's unsaved dot, which the spec's "no dirty tab" would reject. It is disclosed in clip.md review notes and in the PR's Known gaps ("left as filmed"). The top of the VS Code window is cut in the zoomed frames (menu bar text); also disclosed in Known gaps. Both accepted as disclosed, not hidden. VERIFIED with those two noted cosmetics.
6. Shipped clip.md / scenario.mjs vs spec: read both. Scenario exports stage, open, settings, checks, EXPECTED, setup, run, verify; imports nothing; uses MyST mode check, slash highlight check, key frames `slash-menu` and `grid-form`, only the save chord logged as a press. clip.md has Size, Frame rate, Zoom, Mark 1, Badge save `Ctrl+Enter / ⌘Enter`, two captions with the spec's texts. VERIFIED. `git diff` against the base shows no change to `src/` or the kit lib (only two test files). VERIFIED.
7. docs page: `git diff <base>..HEAD -- docs/user/slash-menu.md` adds the GIF with the spec's alt text after the bullet list and before the screenshot. VERIFIED. LFS: `git lfs ls-files` lists the 12 outputs of the clip folder.
8. Evidence 5, PR body: `gh pr view 506 --json body,isDraft,headRefOid` -> isDraft true, head d5e68210b4c9392e3faf66a561567b835dc3096a. The posted body equals `work/pr-body.md` (only a trailing blank line differs). GIF, MP4, WebM and clip.md links use the head SHA; `curl -IL` on the GIF raw URL -> 302 then `200 image/gif`, 1069524 bytes (same size as check.json), repo PUBLIC. Sections follow the template; Summary, Deliverables, Deviation, Autonomous decisions and Changes match the diff (clip folder, slash-menu.md, two kit test files, siteClips test); no `src/` claim. Known gaps names the UNVERIFIED motion/rhythm/loop, the dirty dot and the cut zoom top. Role names: only "CR-490 ... batch-09" in Internal references. `Review: approved at d5e6821` matches the Driver's note "r1 approved at 8197e4fd, committed as d5e68210" (`chantier log CR-490`). The two unticked lines (`Verified at NONE`, `CI green at NONE`) are the Driver's to fill at hand-back; CI is green per the prompt. Images show no username or home path. VERIFIED. Rendering of the GIF on the PR page as played by GitHub was not looked at in a browser: UNVERIFIED (the raw URL resolves).
9. Motion, rhythm, the loop as watched, the storyboard's texts and times as a viewer judges them: UNVERIFIED, owner's (named in the PR). first-last.png shows the seam frames (right frame has the cards fading), SSIM 0.9968.

Not proved: macOS and Linux takes; GFM-mode `/grid`; the Linux CI leg beyond the prompt's CI note.

Verdict: VERIFIED
