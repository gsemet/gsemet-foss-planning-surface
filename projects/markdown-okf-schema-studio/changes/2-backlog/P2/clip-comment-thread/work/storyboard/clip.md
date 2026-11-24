---
title: Feature clip comment-thread
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: comment-thread

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/comment-thread/clip.md` and the clip is rendered from it.

The clip is one continuous shot: the selection and the comment, then a zoom on the open thread. It
shows two texts in turn. The times below are the Griller's proposal; the batch's trial take sets the
real ones and adds the pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 10.8 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | `markdownOkfSchemaStudio.comments.authorName`: `Reviewer` (the kit's profile) |
| Filmed on | to be filmed by the batch |
| Stage | `stage/proposal.md` (Studio, the whole window, reading mode); no `proposal.comments.json` at frame 0 |

## 1. Select a sentence and comment

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 0 to 5.0 s (drag 0.3 to 2.0 s, click Comment at 2.6 s, typing 2.9 to 4.3 s, save at 4.6 s) |
| Shot *(filmed)* | Studio in reading mode on `proposal.md`. The mouse drags over the sentence "We drop support for Node 18 in this release." The small Comment button appears beside the selection; the pointer clicks it. The box "Write a comment" opens; the text "Can we keep it one more release?" is typed. Save chord. The sentence is highlighted. |
| Text 1 *(on screen)* | Select a passage and **comment** on it in the page |
| Badge save *(on screen)* | Ctrl+Enter / ⌘Enter |

## 2. The thread, zoomed

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 5.0 to 10.8 s (click on the highlight at 5.4 s, zoom from 5.8 s, held to 9.8 s, the thread closed with Escape at 10.0 s, then back to the start for the loop) |
| Shot *(filmed)* | The pointer clicks the highlighted sentence: the thread popover opens under it with the author "Reviewer", the date, the comment, the Reply box and the Resolve and Delete buttons. Zoom (at most 2x) on the highlighted sentence and the popover. |
| Mark 1 *(on screen)* | Orange outline around the highlighted sentence, 6.3 to 7.5 s |
| Mark 2 *(on screen)* | Orange outline around the Reply box and the Resolve button, 7.5 to 8.9 s |
| Text 2 *(on screen)* | Threads live in **.comments.json**, next to the file |

Expected result, the scenario's check: `proposal.comments.json` exists next to `proposal.md`
(read from disk), and `proposal.md` is unchanged. The ids and dates change at each take; the rest is
exact:

```json
{
  "version": 1,
  "document": "proposal.md",
  "threads": [
    {
      "id": "<any>",
      "anchor": { "line": "<the paragraph line>", "quote": "We drop support for Node 18 in this release.", "...": "prefix, suffix, endLine as written" },
      "resolved": false,
      "createdAt": "<the take's time>",
      "comments": [
        { "id": "<any>", "author": "Reviewer", "createdAt": "<the take's time>", "body": "Can we keep it one more release?" }
      ]
    }
  ]
}
```

## Review notes

- If the thread opens by itself after Save, the click on the highlight at 5.4 s is dropped and the
  times move up.
- The popover shows the take's date: harmless, but it ages the clip. No personal name: the author is
  the profile's `Reviewer`.
- The take must start with no comments file: the stage holds none, and the kit copies the stage into
  a fresh workspace at each take; check that a failed take leaves none behind.
- A typed reply (as the intake allows) would add about 2 s and push the clip past 12 s; not filmed.
  The `.comments.json` file is named by Text 2 only, not shown: showing it would need a second pane.
- The selection must start and end on the sentence's own characters (the kit's `selectText`), so
  the quote stored is exactly the sentence.
