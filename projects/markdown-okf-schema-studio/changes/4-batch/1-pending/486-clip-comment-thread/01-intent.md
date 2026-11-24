# Feature clip: a comment thread on a passage

This clip shows review in the page itself: select a sentence in the preview, press the small
Comment button, write the comment and save it. The passage is highlighted, and a click on it opens
the thread with its Reply box and its Resolve and Delete buttons. The thread is stored in the
`.comments.json` file next to the document, so it is versioned in Git with the Markdown and needs no
server. Reviewing what an agent wrote, and leaving it notes, is the use the clip sells.

It is made with the clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`) as the CR
`short-demo-video-of-the-smart-raw-markdo` leaves them: two captions in turn, several orange marks
in turn, combined key badges, 1280x720 at 15 fps, no card, the logo top right, a loop. This CR
depends on it. The clip lives in `docs/demo-video/clips/comment-thread/`.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`. The
batch films a trial take, puts its pictures in the storyboard and gets the owner's review of the
storyboard before the final take and before the render (the recipe's gates). Then it opens the PR
with the clip watchable in its description: the GIF inline, the MP4 and the WebM linked at the PR's
head.
