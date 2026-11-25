# Verify CR-501

Head: 66b84782df697c6ed9b7ec8119c7b1064fae8ee7

Basis: the Chief of Staff's ruling (Q12) on the last scenes (Enter opens the whole admonition editor, caret by Up x5 + Right, no badge) is the authority for steps 9 to 12. No retake.

Claims, each judged at 66b84782:
1. Kit tests: `just clip-kit-test` -> tests 40, pass 40, fail 0.
2. Site test: `node scripts/node-test.mjs unit out/test/site/siteClips.test.js` -> tests 16, pass 16, fail 0; "the shipped editing page plays the keyboard navigation clip as video" passes. (Plain `node --test` fails on every site test with a markdown-it ESM resolution error: the project runner is the proof, not a CR matter.)
3. `just check` -> exit 0; `just ci-static` -> "ci-static: passed" (PR body's local gates claim).
4. Take: check.json `passed: true`, 20 s, 1280x720, 15 fps, h264, no audio, GIF 1.60 MB loop 0, loop seam SSIM 0.98998, playbackRate 1.003, `verifyPassed: true` (scenario verify compares release-plan.md to the expected text with Friday->Thursday, no box open). All 20 checks ok. Matches PR body figures.
5. Frames: contact-sheet.png, admonition-editor-2.png, word-changed.png opened: reading mode -> E -> heading/admonition selected -> Enter editor (Esc closes) -> zoom, sentence, list, first item selected -> admonition editor (lines 3-11), caret on Friday line, "Thursday" typed with Ctrl+Backspace badge, final frame shows "Tag the release on Thursday" outlined. Captions and badges legible, pointer never moves. Made-up paths only: window title "release-plan.md - workspace"; `grep -ril gaeta` on the clip folder and editing.md: no match.
6. Deviation (Q12) is reported in PR body "Deviation" and "Known gaps"; clip.md rows 73/104 describe the admonition editor and Up x5 + Right; the stale "Changing one word" note is listed in Known gaps.
7. PR description (gh pr view 522) equals work/pr-body.md (diff: a trailing blank line only); media links name the head 66b84782; PR is a draft; sections match the diff (clip folder, editing.md, kit tests, site test; no src/ change: `git diff --stat` shows none).
8. Review box: PR body has `Review` unchecked (no "approved" claim), so nothing to judge.

VERIFIED
