# Feature clip: diff since the last commit, then side by side

Studio has a feature clip kit (`docs/demo-video/clip-kit/`, CR-482, PR #501) and a recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`). The CR `short-demo-video-of-the-smart-raw-markdo`
gives them a Markdown storyboard the owner reviews, two captions in turn, several marks in turn,
combined key badges and a PR whose review plays the clip. This CR makes one more clip with the kit and
the recipe as that CR leaves them.

Clip: Diff marks the blocks changed since the last commit in the preview, then Side-by-side shows
each as a before/after with the changed words marked. One continuous shot: open a Markdown file with
uncommitted changes, switch Diff on, then switch Side-by-side.

The clip lives in `docs/demo-video/clips/diff-side-by-side/` with its storyboard `clip.md`, its stage
document and its scenario; the batch films the take, renders the GIF, MP4 and WebM, and opens the PR.
