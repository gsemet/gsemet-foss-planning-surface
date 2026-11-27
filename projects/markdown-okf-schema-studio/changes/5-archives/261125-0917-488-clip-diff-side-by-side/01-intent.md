# Feature clip: diff since the last commit, then side by side

This clip shows how Studio answers "what changed in this file?" without leaving the page. The Diff
button of the floating toolbar marks with a green bar each block changed since the last Git commit;
then the Side-by-side button turns each changed block into a small before/after card, the removed
words struck through on the left and the added words underlined on the right. Reviewing an agent's
edit is the daily use: the clip shows it in one continuous shot of about 11 s.

It is made with the clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`) as the CR
`short-demo-video-of-the-smart-raw-markdo` leaves them: two captions in turn, several orange marks
in turn, 1280x720 at 15 fps, no card, the logo top right, a loop. This CR depends on it. The clip
lives in `docs/demo-video/clips/diff-side-by-side/`.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`: the
committed version of the document and the working copy that changes two blocks. The batch films a
trial take, puts its pictures in the storyboard and gets the owner's review of the storyboard before
the final take and before the render (the recipe's gates). Then it opens the PR with the clip
watchable in its description: the GIF inline, the MP4 and the WebM linked at the PR's head.
