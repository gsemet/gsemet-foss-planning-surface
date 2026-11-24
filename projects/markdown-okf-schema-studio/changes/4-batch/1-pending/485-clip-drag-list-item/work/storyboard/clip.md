---
title: Feature clip drag-list-item
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: drag-list-item

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/drag-list-item/clip.md` and the clip is rendered from it.

The clip is one continuous shot: the drag in the page on the left, then a zoom on the raw text on
the right. It shows two texts in turn. The times below are the Griller's proposal; the batch's trial
take sets the real ones and adds the pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 10.5 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none |
| Filmed on | to be filmed by the batch |
| Stage | `stage/release-steps.md` opened twice: in Studio (left, edit mode) and in the built-in text editor (right) |

## 1. Drag the item by its handle

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 0 to 4.2 s (pointer on the handle at 0.9 s, press at 1.2 s, drag 1.2 to 2.6 s, drop at 2.6 s, the raw text changes about 3.0 s) |
| Shot *(filmed)* | Studio in edit mode on `release-steps.md` (left), the same file as raw text (right). The pointer moves to the handle left of item 2, "Build the packages." (title "Drag to move item (Alt+Up, Alt+Down)"), presses and drags it up above item 1, "Tag the release.", then drops. The item moves with its two sub-items; the page shows 1 Build the packages, 2 Tag the release, 3 Run the smoke tests, 4 Publish the notes. The raw text on the right changes to the same order. |
| Text 1 *(on screen)* | Drag a list item by its **handle**, sub-items come along |

## 2. Zoom on the raw text

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 4.2 to 10.5 s (zoom from 4.4 s, held to 9.5 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the list in the text editor (right), the heading in view. |
| Mark 1 *(on screen)* | Orange outline around the moved lines, "1. Build the packages." and its two sub-items, 5.0 to 6.6 s |
| Mark 2 *(on screen)* | Orange outline around the numbers 1. to 4., 6.6 to 8.2 s |
| Text 2 *(on screen)* | The **raw text** follows, numbers kept in order |

Expected result, the scenario's check: `release-steps.md` on disk (auto-save is on) is exactly this
text:

```markdown
# Release steps

1. Build the packages.
   - Linux and macOS
   - Windows
2. Tag the release.
3. Run the smoke tests.
4. Publish the notes.
```

## Review notes

- The handle uses HTML drag and drop (`draggable`, `dragstart`, `dragover`). The kit's mouse goes
  through CDP into the preview webview; whether Chromium turns that mouse drag into drag events there
  is the first thing the trial proves. If it does not, stop and report: Alt+Up on the focused handle
  moves the item too, but it is not the drag the clip shows.
- The handle shows on hover in edit mode only: the pointer must reach it before the press, and
  `setup` checks edit mode is on.
- Opening the same file in the text editor beside Studio is done off camera (Reopen Editor With,
  in the second group); both stay on one file, so the raw text updates as soon as the page writes.
- The clip ends with the new order and starts with the old one: the loop seam relies on the kit's
  return to the start.
