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
on the right. It shows two texts in turn. The scene is new (a new stage document and a new take):
the pictures below are still the merged take's, and the trial take replaces them.

## Clip

| Field | Content |
| --- | --- |
| Length | 8.5 s (set again by the trial take: the selection and the paste are longer) |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | `markdownOkfSchemaStudio.preview.rawCopy.balanceEdges`: on |
| Filmed on | Windows, VS Code 1.147.0, extension VSIX built from the branch (new take to come) |
| Stage | `stage/runbook.md` (opened in Studio, left) and the empty `stage/notes.md` (text editor, right) |

## 1. Copy on the left, paste on the right

![Merged take, to be replaced: selection in Studio](images/01-selected.jpg)

![Merged take, to be replaced: the paste in notes.md](images/02-pasted.jpg)

| Field | Content |
| --- | --- |
| Time | 0 to 4.4 s (set again by the trial take) |
| Shot *(filmed)* | Studio in reading mode on `runbook.md` (left), the empty `notes.md` in the text editor (right). The mouse drags from "migrations", in the middle of the bold "database migrations first" inside the untitled `important` admonition, to "every worker" inside the `warning` admonition. Copy chord. The pointer moves to `notes.md` and clicks. Paste chord. |
| Text 1 *(on screen)* | From preview, select and copy **raw Markdown** |
| Badge copy *(on screen)* | Ctrl+C / ⌘C |
| Badge paste *(on screen)* | Ctrl+V / ⌘V |

## 2. Zoom on the pasted text

![Merged take, to be replaced: zoom on the pasted text](images/03-zoomed.jpg)

| Field | Content |
| --- | --- |
| Time | 4.4 to 8.5 s (zoom held to 7.6 s, then back to the start for the loop; set again by the trial take) |
| Shot *(filmed)* | Zoom (at most 2x) on the pasted lines in `notes.md`, the closing `:::` in view. |
| Mark *(on screen)* | Orange outline around the added line `:::{important}`, 5.2 to 6.8 s |
| Text 2 *(on screen)* | Partial syntax are pasted as valid Markdown |

Expected paste, the scenario's check (added by the setting: the opening `:::{important}` line, the
opening `**` and the last `:::`). A different paste at the trial take is a finding against the
feature, not a reason to change the scene.

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
- The new take is filmed at 15 fps: the merged take's raw screencast of 5.1 frames per second
  (`check.json` of PR #501) is replaced.
