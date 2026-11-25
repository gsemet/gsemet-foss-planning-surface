# Feature clip: keyboard navigation in nested admonitions and lists

This clip shows that a writer can edit a nested part of a page without touching the mouse. From
reading mode, `E` turns edit mode on, Down selects a block, Enter opens the whole admonition and
Escape closes it again. Then Right goes one level deeper (into the admonition, then into its list),
Down moves among the inner blocks, Enter opens one list item alone, one word is changed, and
Ctrl/Cmd+Enter saves. Every key press shows as a badge, in its Windows and macOS forms.

It is made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): captions in turn (three here,
one per beat), an orange mark, 1280x720 at 15 fps, no card, the logo top right, a loop. The story
truly needs more than 12 s: eleven key presses, each badge readable before the next one, make a
clip of 20 s. The 30 s limit of the kit comes from the CR `clip-the-advanced-renderings-tour`, so
this CR goes after it (`depends.json`). The clip lives in `docs/demo-video/clips/keyboard-navigation/`.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`. The
batch films the trial take from this draft, puts its pictures in the storyboard, renders the clip
and opens the PR with the clip watchable (the GIF inline, the MP4 and the WebM linked at the PR's
head). The owner reviews the storyboard and the clip in that PR, which stays a draft until the
owner approves it.
