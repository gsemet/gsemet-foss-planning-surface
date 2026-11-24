---
title: Feature clip paste-spreadsheet-cells
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: paste-spreadsheet-cells

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/paste-spreadsheet-cells/clip.md` and the clip is rendered from it.

The clip is one continuous shot: the copy on the right, the paste on the left, then a zoom on the
table. It shows two texts in turn. The times below are the Griller's proposal; the batch's trial
take sets the real ones and adds the pictures.

The spreadsheet is `tasks.tsv` in VS Code's text editor: the kit films the VS Code window only (a
CDP screencast of its page), so a spreadsheet application cannot be in the shot. A spreadsheet copy
puts the same tab-separated `text/plain` on the clipboard, and the table cell reads only that.

## Clip

| Field | Content |
| --- | --- |
| Length | 11.0 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none of Studio; for the TSV to read as columns, `"[plaintext]": { "editor.tabSize": 22 }` and `editor.renderWhitespace: none` in the clip's profile |
| Filmed on | to be filmed by the batch |
| Stage | `stage/release-checklist.md` (Studio, left, edit mode: a table of 2 columns, a header and 1 row) and `stage/tasks.tsv` (text editor, right: 5 lines of 3 tab-separated values, a header included) |

## 1. Copy the cells, paste into the table

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 0 to 4.8 s (drag 0.3 to 1.8 s, copy at 2.0 s, click on the cell "Task" at 3.2 s, paste at 3.8 s, click on the empty page below the table at 4.5 s) |
| Shot *(filmed)* | Studio on `release-checklist.md` (left), `tasks.tsv` (right). The mouse drags over the five lines of `tasks.tsv`. Copy chord. The pointer moves to the table and clicks its header cell "Task": the cell editor opens. Paste chord. The table grows to 3 columns ("Due" added) and 5 lines (3 rows added). A click below the table closes the cell editor. |
| Text 1 *(on screen)* | Copy cells from a sheet, **paste** into a table |
| Badge copy *(on screen)* | Ctrl+C / ⌘C |
| Badge paste *(on screen)* | Ctrl+V / ⌘V |

## 2. Zoom on the table

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 4.8 to 11.0 s (zoom from 5.0 s, held to 10.0 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the rendered table in Studio: Task, Owner, Due; four task rows. |
| Mark 1 *(on screen)* | Orange outline around the added column "Due", 5.6 to 7.2 s |
| Mark 2 *(on screen)* | Orange outline around the three added rows, 7.2 to 8.8 s |
| Text 2 *(on screen)* | Cells fill right and down, **rows and columns** added |

Expected result, the scenario's check: `release-checklist.md` on disk (auto-save is on) is exactly
this text (the delimiter cell of the added column as the table model writes it; the trial take
confirms it):

```markdown
# Release 2.4 checklist

| Task | Owner | Due |
| --- | --- | --- |
| Freeze the branch | Ana | Mon |
| Run the migrations | Ben | Tue |
| Restart the workers | Chen | Wed |
| Announce the release | Dev | Thu |
```

## Review notes

- VS Code's copy also puts `text/html` on the clipboard; the cell editor reads `text/plain` first
  (a text with a tab is a grid paste), so the HTML is ignored. Check it in the trial.
- The drag must cover the five whole lines, the last line break optional (one final line break is
  dropped). A partial first or last line would paste a partial cell.
- The paste goes from the clicked cell: clicking the header cell "Task" makes the header and the
  existing row take the same values again; only "Due" and the three rows are new, which the marks
  show.
- How the cell editor closes (a click below the table, Done, or Ctrl+Enter) is settled in the
  trial; Escape is Cancel and is not used.
- The clip ends with the larger table and starts with the small one: the loop seam relies on the
  kit's return to the start.
