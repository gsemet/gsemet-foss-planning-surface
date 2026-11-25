---
title: Feature clip export-html
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: export-html

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/export-html/clip.md` and the clip is rendered from it.

The clip is one continuous shot: the export in Studio on the left, then the exported file in a
browser on the right, zoomed. It shows two texts in turn. The times below are the Griller's
proposal; the batch's trial take sets the real ones and adds the pictures.

The browser is VS Code's built-in Simple Browser, inside the filmed window: the kit films the VS
Code window only (a CDP screencast of its page), so an outside browser cannot be in the shot. The
Simple Browser does not load `file://` pages, so `setup` starts a small static server on
`http://localhost:5170/` over the workspace (Node.js, off camera) and the scenario stops it after
`verify`.

## Clip

| Field | Content |
| --- | --- |
| Length | 12.0 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | `files.simpleDialog.enable`: on (the save dialog is VS Code's own, inside the window, not the system dialog) |
| Filmed on | to be filmed by the batch |
| Stage | `stage/team-handbook.md` (Studio, the whole window, reading mode, Dark theme): a heading, a sentence, a Mermaid flowchart and a tab set of two tabs |

Off camera (`setup`): the toolbar expanded, the Theme button clicked from Cream to Dark (through
the current theme), the local server started.

## 1. Export, then open the file

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 0 to 5.6 s (click Export at 0.8 s, Enter in the save dialog at 2.0 s, command palette at 2.8 s, "Simple Browser: Show" chosen at 4.0 s, the address entered at 5.0 s, the page shown at 5.6 s) |
| Shot *(filmed)* | Studio on `team-handbook.md` in Dark. The pointer clicks the Export button of row 1 ("Export to HTML"). VS Code's save dialog opens at the top with `team-handbook.html` proposed; Enter. Command palette chord; "Simple Browser: Show" is typed and chosen; `localhost:5170/team-handbook.html` is typed; Enter. The Simple Browser opens on the right with the exported page, in Dark. |
| Text 1 *(on screen)* | **Export** the page to one HTML file |
| Badge palette *(on screen)* | Ctrl+Shift+P / ⇧⌘P |

## 2. The same page in the browser

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 5.6 to 12.0 s (zoom from 6.0 s, held to 11.0 s; click on the tab "Release" at 8.4 s; then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the Simple Browser: the heading, the flowchart and the tab set in Dark, as in Studio. The pointer clicks the tab "Release": its panel replaces "Review". |
| Mark 1 *(on screen)* | Orange outline around the flowchart, 6.6 to 8.0 s |
| Mark 2 *(on screen)* | Orange outline around the tab set, after the click, 8.6 to 10.2 s |
| Text 2 *(on screen)* | Any browser shows the **same themed page** |

Expected result, the scenario's check (read from disk and from the Simple Browser's frame):

- `team-handbook.html` exists next to `team-handbook.md`, and it is the only new file in the
  workspace.
- It loads nothing from another file or the network: no `src` or `href` to a local file, the
  flowchart embedded as SVG.
- It carries the Dark theme mode of the page at the export.
- In the Simple Browser, after the click, the panel "We release on Thursday, after the smoke tests."
  is shown and "Every change gets one approving review." is hidden.
- `team-handbook.md` on disk is byte for byte `stage/team-handbook.md`.

## Review notes

- The command palette part (about 3 s) is the slowest beat. Option for the gate: `setup` opens the
  Simple Browser on the right before the take, on the address that does not exist yet, and the clip
  only clicks its reload button after the export; it saves about 2 s but shows a "not found" page at
  frame 0.
- The Simple Browser page is a webview inside the window, like Studio's preview: the trial checks it
  is in the screencast frames (the recipe's trial point (a)).
- With `files.simpleDialog.enable` on, the save dialog is a VS Code input; without it, the system
  dialog is outside the filmed page and the take would hang.
- The address bar shows `localhost:5170`: no personal path. The port is free on the take's machine
  or the scenario picks another and the caption is unchanged.
- The clip ends with the Simple Browser open on the right and starts without it: the loop seam
  relies on the kit's return to the start.
