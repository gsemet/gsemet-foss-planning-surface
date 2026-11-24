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
on the right. It shows two texts in turn. The scene is new (a new stage document and a new take).
The pictures and times below come from the Griller's trial take and render of 2026-11-24 (a scratch
copy of the merged kit, changed for two captions, three marks and the combined badges).

## Clip

| Field | Content |
| --- | --- |
| Length | 9.8 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges`: on |
| Filmed on | Windows, VS Code 1.147.0, extension 1.12.1 VSIX built from the branch (trial take; the batch films again) |
| Stage | `stage/runbook.md` (opened in Studio, left) and the empty `stage/notes.md` (text editor, right) |

## 1. Copy on the left, paste on the right

![The selection, from inside the bold to inside the warning, copied](images/01-selected.jpg)

![The paste in notes.md](images/02-pasted.jpg)

| Field | Content |
| --- | --- |
| Time | 0 to 4.4 s (drag 0.3 to 2.6 s, copy at 2.6 s, click in `notes.md` at 3.7 s, paste at 4.2 s) |
| Shot *(filmed)* | Studio in reading mode on `runbook.md` (left), the empty `notes.md` in the text editor (right). The mouse drags from "migrations", in the middle of the bold "database migrations first" inside the untitled `important` admonition, to "every worker" inside the `warning` admonition. Copy chord. The pointer moves to `notes.md` and clicks. Paste chord. |
| Text 1 *(on screen)* | From the preview, select and copy **raw Markdown** |
| Badge copy *(on screen)* | Ctrl+C / ⌘C |
| Badge paste *(on screen)* | Ctrl+V / ⌘V |

## 2. Zoom on the pasted text

![Zoom, mark 1 on the added opening line](images/03-zoomed.jpg)

![Mark 2 on the added opening bold](images/04-mark-bold.jpg)

![Mark 3 on the added closing line](images/05-mark-closing.jpg)

| Field | Content |
| --- | --- |
| Time | 4.4 to 9.8 s (zoom from 4.5 s, held to 8.8 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the pasted lines in `notes.md`, the closing `:::` in view. |
| Mark 1 *(on screen)* | Orange outline around the added line `:::{important}`, 5.0 to 6.2 s |
| Mark 2 *(on screen)* | Orange outline around the added opening `**` before "migrations", 6.2 to 7.4 s |
| Mark 3 *(on screen)* | Orange outline around the added closing `:::`, 7.4 to 8.6 s |
| Text 2 *(on screen)* | Partial syntax is pasted as valid Markdown |

Expected paste, the scenario's check (added by the setting: the opening `:::{important}` line, the
opening `**` and the last `:::`). The trial take pasted exactly this text.

```markdown
:::{important}
**migrations first**, then restart the workers one at a time.
:::

The deploy script checks the migration version and refuses to start the workers on an old schema.

:::{warning}
Never restart every worker
:::
```

## Review notes

- With the setting off, the same selection copies from `migrations first**` to `every worker`,
  with no opening line, no opening `**` and no closing `:::`. That case is not filmed.
- The trial's raw screencast ran at 4 frames per second (5.1 for the merged take): the pointer is
  drawn smooth by the kit, but the selection grows by steps. A 15 fps output does not change it.
- Watch the trial: MP4 at 1280x720, 15 fps (`raw-copy-trial-720p15.mp4`), and the kit's 1920x1080
  MP4, WebM and GIF, in the Griller's scratch folder; not in the repository.
