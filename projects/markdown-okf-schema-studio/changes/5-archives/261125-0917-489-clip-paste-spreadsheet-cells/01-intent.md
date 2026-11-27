# Feature clip: paste spreadsheet cells into a table

This clip shows that a table in Studio takes a block of spreadsheet cells as a spreadsheet would:
copy the cells, click a cell of the table, paste. The cells fill from the clicked cell to the right
and down, and the columns and rows the table lacks are added. Moving a list of tasks or figures from
a sheet into a Markdown document is a common chore; the clip shows it done in one paste.

The kit films the VS Code window only, so the "spreadsheet" is a tab-separated file, `tasks.tsv`,
open in VS Code's text editor beside Studio. A copy from Excel, LibreOffice or Google Sheets puts the
same tab-separated text on the clipboard, which is what the table cell reads.

It is made with the clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`) as the CR
`short-demo-video-of-the-smart-raw-markdo` leaves them: two captions in turn, several orange marks
in turn, combined key badges, 1280x720 at 15 fps, no card, the logo top right, a loop. This CR
depends on it. The clip lives in `docs/demo-video/clips/paste-spreadsheet-cells/`.

The storyboard draft is `work/storyboard/clip.md`, with the stage in `work/storyboard/stage/`. The
batch films a trial take, puts its pictures in the storyboard and gets the owner's review of the
storyboard before the final take and before the render (the recipe's gates). Then it opens the PR
with the clip watchable in its description: the GIF inline, the MP4 and the WebM linked at the PR's
head.
