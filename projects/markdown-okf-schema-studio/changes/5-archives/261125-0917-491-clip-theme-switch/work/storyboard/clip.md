---
title: Feature clip theme-switch
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: theme-switch

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/theme-switch/clip.md` and the clip is rendered from it.

The clip is one continuous shot: two clicks on the Theme button, then a zoom on the diagram and the
chart. It shows two texts in turn. The times below are the Griller's proposal; the batch's trial
take sets the real ones and adds the pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 10.5 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none (the theme is a view choice kept per workspace, set off camera) |
| Filmed on | to be filmed by the batch |
| Stage | `stage/handbook.md` (Studio, the whole window, reading mode): a heading, a sentence, a `tip` admonition, a Mermaid flowchart and a Vega-Lite bar chart, all in view |

Off camera (`setup`): the toolbar expanded (a new workspace starts collapsed), reading mode, and the
Theme button clicked from Cream (the default) through the current theme to Dark, so frame 0 is Dark.
The button cycles current, Dark, White, Cream.

## 1. Two clicks, three palettes

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 0 to 4.0 s (click at 1.0 s: White; click at 2.6 s: Cream; each fade about 0.2 s) |
| Shot *(filmed)* | Studio on `handbook.md` in Dark. The pointer moves to the Theme button of row 2 and clicks: the whole page, the admonition, the diagram and the chart turn White. It clicks again: Cream. The pointer then moves off the toolbar. |
| Text 1 *(on screen)* | One click turns the **whole page** to another theme |

## 2. Zoom on the diagram and the chart

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 4.0 to 10.5 s (zoom from 4.2 s, held to 9.5 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the flowchart and the bar chart, in Cream: the boxes, arrows, bars and axis labels in the Cream palette. |
| Mark 1 *(on screen)* | Orange outline around the flowchart, 4.8 to 6.6 s |
| Mark 2 *(on screen)* | Orange outline around the bar chart, 6.6 to 8.4 s |
| Text 2 *(on screen)* | Diagrams and charts **follow** the theme |

Expected result, the scenario's check (visible state, read from the preview; the file is never
changed):

- After the first click the page's theme mode is White, after the second Cream (the theme button's
  label reads "Cream theme (click for current theme)").
- After the second click, the Mermaid SVG and the Vega-Lite chart were drawn again: their fill and
  text colours differ from the ones read at frame 0 (Dark).
- `handbook.md` on disk is byte for byte `stage/handbook.md`.

## Review notes

- The clip ends in Cream and starts in Dark: the loop seam is a theme change. The kit's return to
  the start covers it; if the SSIM check refuses, two more clicks (Cream, current, Dark) are too long
  for 12 s, so the clip would start in Cream and go to Dark through the current theme instead
  (owner's choice at the gate).
- The diagram and the chart are drawn again after each switch: the trial must show they are redrawn
  before the zoom starts; a late redraw shows the old colours for a few frames.
- The toolbar tooltip ("Dark theme (click for white theme)") slides in on hover; the pointer leaves
  the button after the second click so it does not stay in the zoom.
- The current VS Code theme is the kit's Default Light Modern, close to White: that is why the clip
  skips it.
