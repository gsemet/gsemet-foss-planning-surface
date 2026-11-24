---
title: Feature clip raw-copy-balance-edges
status: draft for the owner's review
date: 2026-11-24
---

# Feature clip: raw-copy-balance-edges

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text. Rows marked *(filmed)* describe the footage of the take; changing them means
a new take. Once approved, this file replaces `docs/demo-video/clips/raw-copy-balance-edges/clip.md`
and the clip is rendered from it again.

The pictures come from the clip merged by CR-482 (PR #501). Today that clip shows **one caption for
the whole clip**. The *Caption* rows below suggest one caption per beat instead; each one is yours to
change. If you keep one caption for every beat, the clip stays as it is.

## Clip

| Field | Content |
| --- | --- |
| Length | 8.5 s |
| Format | 1920x1080 16:9, 30 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges`: on |
| Filmed on | Windows, VS Code 1.147.0, extension 1.12.1 VSIX built from the branch |

## 1. Select across the admonition's edge

![Selection in Studio, from inside the admonition to the next paragraph](images/01-selected.jpg)

| Field | Content |
| --- | --- |
| Time | 0 to 2.6 s |
| Shot *(filmed)* | Studio in reading mode on `runbook.md` (left), the empty `notes.md` in the text editor (right). The mouse drags from "database" inside the `important` admonition to "old schema." in the next paragraph. |
| Caption *(on screen)* | Select across an **admonition** edge |
| Badge *(on screen)* | - |

## 2. Copy

| Field | Content |
| --- | --- |
| Time | 2.6 to 2.8 s |
| Shot *(filmed)* | The copy chord is pressed; the selection stays. |
| Caption *(on screen)* | Select across an **admonition** edge |
| Badge copy *(on screen)* | Ctrl+C / ⌘C |

## 3. Paste into a plain Markdown file

![The paste in notes.md, at full window](images/02-pasted.jpg)

| Field | Content |
| --- | --- |
| Time | 2.8 to 4.4 s |
| Shot *(filmed)* | The pointer moves to `notes.md`, clicks, and the paste chord is pressed. Five lines arrive. |
| Caption *(on screen)* | Paste: **raw Markdown**, not HTML |
| Badge paste *(on screen)* | Ctrl+V / ⌘V |

## 4. The added edge

![Zoom on the pasted text, the added opening line outlined](images/03-zoomed.jpg)

| Field | Content |
| --- | --- |
| Time | 4.4 to 7.6 s (zoom); outline 5.2 to 6.8 s |
| Shot *(filmed)* | Zoom (at most 2x) on the pasted lines in `notes.md`. |
| Mark *(on screen)* | Orange outline around the added line `:::{important} Before you deploy` |
| Caption *(on screen)* | **balanceEdges** on: a copy stays valid Markdown |

## 5. Back to the start (loop)

| Field | Content |
| --- | --- |
| Time | 7.6 to 8.5 s |
| Shot *(filmed)* | The zoom eases out, the pointer goes back to where it started; the last frames cross-fade into frame 0. |
| Caption *(on screen)* | **balanceEdges** on: a copy stays valid Markdown |

## Review notes

- Only one setting is shown here: with it off, a copy of the same selection gives only the plain
  lines, with no opening `:::{important}` line. That case is not filmed.
- The take's evidence (`check.json` of PR #501) shows a raw screencast of 5.1 frames per second (44
  frames for 8.5 s). Every check passed, but the pointer can look jerky. Watch the MP4 for it; a
  new take would fix it.
