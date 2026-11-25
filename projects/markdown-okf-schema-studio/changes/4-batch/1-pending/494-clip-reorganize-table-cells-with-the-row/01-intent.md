# Feature clip: reorganize a table with its row and column handles

This clip shows that a table in Studio is reorganized by hand, without retyping a cell. In edit
mode each body row has a handle on its left and each column a handle above it. The clip drags the
row "Fix the login bug" to the top of the table, then drags the "Due" column to the first place.
The raw Markdown of the same file, open beside the page, follows each move: whole lines change
order for the row, and every line's cells change order for the column, each cell keeping its own
spacing. A user sees that moving rows and columns is one drag, one edit and one undo.

It is made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): two captions in turn, orange
marks in turn, 1280x720 at 15 fps, no card, the logo top right, a loop, 12.0 s (two drags and a
zoom fit in the kit's limit). It films the mouse drags the way the merged `drag-list-item` clip
does (CDP mouse in edit mode). The clip lives in `docs/demo-video/clips/table-anchors/`.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`. The
batch films the trial take from this draft, puts its pictures in the storyboard, renders the clip
and opens the PR with the clip watchable (the GIF inline, the MP4 and the WebM linked at the PR's
head). The owner reviews the storyboard and the clip in that draft PR (Q3).
