# Verify CR-493

Head: da86d6e8d995c8d4ec4d067628735bdff30e2a1e

All claims judged at da86d6e8 (the pushed head, PR 512 draft, head matches).

1. `just clip-kit-test` at da86d6e8: 38 tests, 38 pass, 0 fail; includes "prepared refusals: a length outside 5 to 30 s; 30.0 s is accepted" and "the shipped advanced-renderings-tour clip.md reads as the clip the owner reviews". PASS.
2. `npm run compile` then `node scripts/node-test.mjs unit out/test/site/siteClips.test.js`: 15 pass, 0 fail, incl. "the shipped editing page plays the renderings tour clip as video". PASS. `just check` and `just ci-static` were NOT re-run by the verifier (only the two commands above); PR test plan cites them as the coder's runs.
3. `git grep -n "5 to 12"` at da86d6e8: only the `check.json` of 8 merged clips (comment-thread, diff-side-by-side, drag-list-item, export-html, paste-spreadsheet-cells, raw-copy-balance-edges, slash-menu-grid, theme-switch), as the spec allows. Nothing in the kit, recipe or glossary. PASS.
4. Diff of check.mjs/storyboard.mjs: `MAX_LENGTH = 30`; `durationLine` exported, built from MIN_LENGTH/MAX_LENGTH, used by `checkClip`. PASS.
5. check.json (committed take): passed true; "mp4 duration within 5 to 30 s" ok 16.000 s; MP4 and WebM 1280x720 15 fps; duration = Length; GIF 1.85 MB, ladder step 0; loop seam SSIM 0.99577; "Studio in reading mode at the start" ok; no paste line; verifyPassed true; playback rate 1.003; platform win32; extension source vsix; vscode 1.147.0. PASS.
6. Contact sheet, 03-zoomed, 04-mark-1..09-mark-6, first-last viewed: Studio in Cream, reading mode, marks on Mermaid, PlantUML (drawn, no error), Vega-Lite, Vega, equation, SVG in turn and inside the zoom, each with the right caption; no tooltip, no dirty tab, no username or path (grep of clip.md, check.json, scenario.mjs for "gaeta"/"C:\Users": none). Remarks, not failures: 03-zoomed is caught mid-scroll with the Vega caption on; the Vega bar chart y-axis ticks are cramped (height 80, disclosed). Not judged (cannot from stills): motion, rhythm, the loop as watched, the scroll smoothness. PASS for stills.
7. PR 512: draft true, head da86d6e8; posted body equals work/pr-body.md (one trailing line). Body sections match the diff (kit change, clip folder, editing.md, tests); Autonomous decisions disclose the stage size reductions and the scrollTo way; Known gaps lists the unjudged motion and the Windows-only take. Review box: `chantier log` shows "r1 inspector approved at 4a47151e" and "r1 committed as e0d723d5, 114e4d13, da86d6e8" (approved tree committed): accepted. No long gate pass at da86d6e8 (ship "off" says so); not required for this claim set. Image URLs use raw/<head sha>, which resolve only once pushed (head is pushed). The GIF's rendering on the PR page was not opened by the verifier. PASS with that note.

VERIFIED
