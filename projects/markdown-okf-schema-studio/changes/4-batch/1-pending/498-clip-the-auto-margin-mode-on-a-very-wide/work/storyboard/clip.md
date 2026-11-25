---
title: Feature clip wide-table-auto-width
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: wide-table-auto-width

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/wide-table-auto-width/clip.md` and the clip is rendered from it.

The clip is one continuous shot: the page in Margin with a very wide table cut at the column, one
click on the Width button, the same page in Auto with the table broken out of the column, then a
light zoom and two marks. It shows two texts in turn. The times below are the Griller's proposal;
the batch's trial take sets the real ones and adds the pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 10.6 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none: every setting at its default (`preview.maxContentWidth` 960 px; the width mode is a view choice, set off camera to Margin) |
| Filmed on | to be filmed by the batch |
| Stage | `stage/deploys.md` (Studio, the whole window, reading mode, Cream theme): a heading, a paragraph of two lines, a table of 17 columns (service, team, region, tier, twelve months, total) and five rows, a closing sentence, all in view |

Off camera (`setup`): the toolbar expanded (a new workspace starts collapsed), reading mode, the
Cream theme (the default), the TOC closed (the default), and the Width button clicked until it
reads "Width: Margin", so frame 0 is Margin whatever the workspace stored. The button cycles
Margin, Auto, Full width.

## 1. Margin: the table is cut at the column

Pictures: from the batch's trial take (`frames/margin.png`).

| Field | Content |
| --- | --- |
| Time | 0 to 2.8 s (the pointer moves to the Width button from 0.3 s; click at 2.5 s) |
| Shot *(filmed)* | Studio on `deploys.md` in Margin. The heading and the paragraph sit in the centred column; the table starts at the column's left edge and is cut at its right edge after the first few months, with the shaded edge of a table that scrolls sideways. The pointer moves to the Width button, the first button of row 3, and clicks. |
| Text 1 *(on screen)* | In **Margin**, a wide table is cut at the column |

## 2. Auto: the table takes the width it needs

Pictures: from the batch's trial take (`frames/auto.png`, `frames/04-mark-1.png`,
`frames/05-mark-2.png`).

| Field | Content |
| --- | --- |
| Time | 2.8 to 10.6 s (the pointer leaves the toolbar by 3.4 s; zoom from 3.8 s, held to 9.6 s, then back to the start for the loop) |
| Shot *(filmed)* | At the click the table breaks out of the column on both sides, centred on the pane, and shows all twelve months and the total with no sideways scroll; the heading, the paragraph and the closing sentence do not move. The pointer moves off the toolbar to the blank right of the heading. A light zoom (close to 1x: the table is almost as wide as the pane) on the paragraph and the table. |
| Zoom | page, hold to 9.6 s |
| Mark 1 *(on screen)* | Orange outline around the table, broken out of the column, 4.4 to 6.6 s |
| Mark 2 *(on screen)* | Orange outline around the paragraph, still in the narrow column, 6.8 to 9.0 s |
| Text 2 *(on screen)* | In **Auto**, the table breaks out; the text keeps its column |

Expected result, the scenario's check (visible state, read from the preview; the file is never
changed):

- At frame 0 the page's width mode is Margin (`data-sphinx-preview-width="margin"`, the button's
  title "Width: Margin"); the table is no wider than the column and overflows it: its `scrollWidth`
  is larger than its `clientWidth`, and it carries `data-sphinx-table-overflow="true"`.
- After the click the width mode is Auto (title "Width: Auto"); the table's top-level block carries
  `data-sphinx-preview-wide`, its box is wider than the paragraph's box on both sides, its centre is
  within 2 px of the pane's centre, and it no longer overflows (`scrollWidth` at most `clientWidth`
  plus 1).
- The paragraph's left edge and width are the same before and after the click.
- `deploys.md` on disk is byte for byte `stage/deploys.md`.

## Review notes

- Which tables break out (`src/page/modules/widthMode.ts`, `docs/user/wide-tables.md`): in Auto a
  table breaks out only when the sum of its column minimums is wider than the column. A token
  column (every body cell at most three words: a name, a number) counts at its natural width and
  never wraps; a prose column counts about 24 characters. Every column of this table is a token
  column, so its minimum is its natural width.
- The sizes, from the CSS at origin/main: the column is 960 px minus two gutters of 78 px, about
  804 CSS px (`maxContentWidth` 960, `box-sizing: border-box`, gutter `clamp(16px, 8vw, 78px)`).
  The room in Auto is the pane minus 32 px (no TOC), about 1120 to 1240 CSS px in the kit's window.
  The table is designed for about 950 CSS px in Auto: wider than the column, narrower than the room,
  so it breaks out and fits whole. In Margin each column keeps its 5em floor (about 93 px), so the
  table needs about 1580 px and shows only the first four or five months. The trial must measure the Auto width; if it
  is outside the band, drop the Total column or shorten the month row, never change a setting.
- A table wider than the room would break out to the room and still scroll: that is why the table
  is not wider.
- The table comes after the heading and the paragraph, so it starts below the expanded toolbar's
  three rows; the trial checks the toolbar does not cover the table's right end in Auto.
- The width change has no animation: the table jumps at the click. The trial says whether that
  reads well; no kit change is proposed for it.
- The zoom is almost 1x: the result is the whole width of the pane. It is there because the kit
  shows a mark only during a zoom.
- The pointer leaves the Width button after the click, so its tooltip ("Width: Auto") is not in the
  zoom.
- Loop seam: the clip starts in Margin and ends in Auto, and relies on the kit's return to the
  start (export-html passed at SSIM 0.98870 with a larger change). If `check` refuses the seam, the
  fallback adds two clicks after the zoom (Full width at 10.2 s, Margin at 10.8 s; Length 11.8 s),
  Text 2 running to the end; see auto-width-Q10.
- The table style (service, team, region, tier, months) is the one of the wide table of the CR
  `clip-adapt-the-export-video-long-page-sa`, for consistency between the two clips; this clip adds
  a Total column.
