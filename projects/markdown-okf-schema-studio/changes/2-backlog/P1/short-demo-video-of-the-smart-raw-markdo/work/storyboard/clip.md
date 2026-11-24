---
title: Feature clip raw-copy-balance-edges
status: draft for the owner's review
date: 2026-11-24
---

# Feature clip: raw-copy-balance-edges

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file replaces
`docs/demo-video/clips/raw-copy-balance-edges/clip.md` and the clip is rendered from it again.

The clip is one continuous shot, as merged by CR-482 (PR #501): the action on the left, then a zoom
on the right. It shows two texts in turn.

## Clip

| Field | Content |
| --- | --- |
| Length | 8.5 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges`: on |
| Filmed on | Windows, VS Code 1.147.0, extension 1.12.1 VSIX built from the branch |

## 1. Copy on the left, paste on the right

![Selection in Studio, from inside the admonition to the next paragraph](images/01-selected.jpg)

![The paste in notes.md](images/02-pasted.jpg)

| Field | Content |
| --- | --- |
| Time | 0 to 4.4 s |
| Shot *(filmed)* | Studio in reading mode on `runbook.md` (left), the empty `notes.md` in the text editor (right). The mouse drags from "database", inside the `important` admonition, to "old schema." in the next paragraph (0 to 2.6 s). Copy chord at 2.6 s. The pointer moves to `notes.md` and clicks. Paste chord at 4.2 s. |
| Text 1 *(on screen)* | From preview, select and copy **raw Markdown** |
| Badge copy *(on screen)* | Ctrl+C / ⌘C |
| Badge paste *(on screen)* | Ctrl+V / ⌘V |

## 2. Zoom on the pasted text

![Zoom on the pasted text, the added opening line outlined](images/03-zoomed.jpg)

| Field | Content |
| --- | --- |
| Time | 4.4 to 8.5 s (zoom held to 7.6 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the five pasted lines in `notes.md`. |
| Mark *(on screen)* | Orange outline around the added line `:::{important}`, 5.2 to 6.8 s                   |
| Text 2 *(on screen)* | Partial syntax are pasted as valid Markdown      |

## Review notes

- With the setting off, a copy of the same selection gives the lines without the opening
  `:::{important}` line. That case is not filmed.
- The take's evidence (`check.json` of PR #501) records a raw screencast of 5.1 frames per second
  (44 frames for 8.5 s). Every check passed, but the pointer may look jerky: watch the MP4 for it.
  A new take would fix it.
