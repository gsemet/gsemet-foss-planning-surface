# CR-497 verify

Head: 185839681b07add2de5afe33b51b1f9f742273d9

All claims judged at 185839681b07add2de5afe33b51b1f9f742273d9 (worktree clean, `gh pr view 518` headRefOid equal).

1. check.json (committed, read): `passed: true`; MP4 and WebM 1280x720, 15 fps, 12.000 s = Length 12; GIF 960 px, 12 fps, loop count 0; loopSeamSsim 0.995729; playbackRate 1.004; verifyPassed true; readingMode on; checks paste false; platform win32; extensionSource vsix; 20 check lines all ok.
2. `just clip-kit-test`: 37 tests, 37 pass, 0 fail, incl. "the shipped block-editor-modes clip.md reads as the clip the owner reviews" and "the stage of the block-editor-modes scenario is the shipped stage file, byte for byte".
3. `just compile`, then `node --import ./scripts/register-myst-patches.mjs --test out/test/site/siteClips.test.js`: 15 pass, 0 fail, incl. "the shipped editing page plays the block editor modes clip as video".
4. `cmp` of shipped `stage/release-plan.md` with the planning `work/storyboard/stage/release-plan.md`: identical.
5. Scope: `git diff origin/main...HEAD --name-only` outside the clip folder: check.test.mjs, storyboard.test.mjs (tests only), docs/user/editing.md, test/site/siteClips.test.ts. No src/, no kit lib code, no skill change. editing.md diff: GIF under the "Full mode adds..." sentence, indented as the item, rest of item a new paragraph, as the spec.
6. Looked at contact-sheet.png, first-last.png, frames/mode-select.png, frames/myst.png: Studio in edit mode; palette reads "GitHub (GFM)" then "MyST" with the second row of MyST buttons; badges Ctrl Shift M / (shift-cmd)M then down arrow; Text 1 in the GFM beat, Text 2 from the switch; mark 1 on the MyST buttons (6 s), mark 2 on the alert (8 s), mark 3 on the tip (9 s), in turn; no Problems panel; no editor open at the last frame (faint hover outline while fading, noted in clip.md); no tooltip at frame 0. Window title reads "release-plan.md - workspace"; no username or home path on screen; `grep -c gaeta` on clip.md, check.json, scenario.mjs gives 0. Not checked: motion, rhythm, the loop as watched.
7. clip.md: front matter status draft, rows and times match check.json take values, "Deviation" and review notes present.
8. PR description as posted (`gh pr view 518`): draft true; body renders (sections, GIF, MP4/WebM links at the head SHA 18583968...), Summary, Deliverables and Changes match the diff (clip folder, four test cases, editing.md GIF, no src); no image with a personal name; Known gaps lists the 17 of 19 buttons, the unchecked motion, and the unexercised setup reset. Known gap of the spec's "Autonomous decisions" list is not in the body (the section is optional in the template).
9. CI at the head: static, static-windows, viewer-graph, visual pending at the time of this check; not proof.
10. before/after: not captured, the CR is docs, media and tests with no UI change of the extension; the clip is the evidence.

Not run: `just check`, `just preflight` (the Coder reports `just check` green; CI static pending).

VERIFIED
