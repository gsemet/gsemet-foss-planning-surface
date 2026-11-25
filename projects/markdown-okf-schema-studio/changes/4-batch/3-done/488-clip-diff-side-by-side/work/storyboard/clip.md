---
title: Feature clip diff-side-by-side
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: diff-side-by-side

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/diff-side-by-side/clip.md` and the clip is rendered from it.

The clip is one continuous shot: the two toolbar clicks, then a zoom on one diff card. It shows two
texts in turn. The times below are the Griller's proposal; the batch's trial take sets the real
ones and adds the pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 11.0 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none (defaults: `markdownOkfSchemaStudio.preview.showIncomingChanges` on) |
| Filmed on | to be filmed by the batch |
| Stage | `stage/deploy-guide.md` (Studio, the whole window, reading mode), in a workspace that is a Git repository whose last commit holds `stage/deploy-guide.committed.md` as `deploy-guide.md` |

Stage, what changes since the commit (two blocks; the heading and the last paragraph do not change):

- Paragraph: "Tuesday" becomes "Wednesday", and "and the smoke tests" is added after "nightly build"
  ("is green" becomes "are green").
- Ordered list: "one at a time" becomes "two at a time" (item 2), "ten minutes" becomes "thirty
  minutes" (item 3).

Off camera (`setup`): `git init`, commit the committed version, write the working copy (not
committed, saved); the toolbar expanded (a new workspace starts collapsed), reading mode, the Diff
button switched off so the green bars are hidden at frame 0.

## 1. Diff marks the changed blocks

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 0 to 3.4 s (click Diff at 1.2 s, the green bars at 1.4 s) |
| Shot *(filmed)* | Studio in reading mode on `deploy-guide.md`, the toolbar open top right. The pointer moves to the Diff button of row 4 ("Show changes since last commit") and clicks. A green bar appears left of the paragraph and of the list; the heading and the last paragraph get none. |
| Text 1 *(on screen)* | Diff marks every block **changed** since the last commit |
| Mark 1 *(on screen)* | Orange outline around the two green bars, 1.8 to 3.2 s |

## 2. Side-by-side, then zoom on a card

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 3.4 to 11.0 s (click Side-by-side at 3.4 s, zoom from 4.6 s, held to 10.0 s, then back to the start for the loop) |
| Shot *(filmed)* | The pointer moves one button left, to Side-by-side ("Show side-by-side changes since last commit"), and clicks. The paragraph and the list each become a card: the block at the last commit on the left, as it is now on the right. Zoom (at most 2x) on the paragraph's card. |
| Mark 2 *(on screen)* | Orange outline around the struck "Tuesday" (left), 5.4 to 6.8 s |
| Mark 3 *(on screen)* | Orange outline around the underlined "Wednesday" (right), 6.8 to 8.2 s |
| Mark 4 *(on screen)* | Orange outline around the underlined "and the smoke tests" (right), 8.2 to 9.6 s |
| Text 2 *(on screen)* | Side-by-side shows **before and after**, word by word |

Expected result, the scenario's check (visible state, read from the preview; the file is never
changed):

- Two diff cards, no more: the paragraph and the list.
- Paragraph card: "Tuesday" and "is" struck on the left; "Wednesday", "and the smoke tests" and
  "are" underlined on the right.
- List card: "one" and "ten" struck on the left; "two" and "thirty" underlined on the right.
- `deploy-guide.md` on disk is byte for byte `stage/deploy-guide.md`, and `git status` shows it
  modified only.

## Review notes

- The kit has no Git step: the scenario's `setup` makes the repository and the commit off camera
  (Git on `PATH`, a neutral `user.name` and `user.email` set in the repository only, so no personal
  name shows).
- The green bars need a trusted workspace and a file known to Git: the kit's profile turns workspace
  trust off, so the workspace counts as trusted; check it in the trial.
- The Diff choice is kept per workspace: `setup` switches it off after the page opens, so frame 0
  has no bars. The toolbar tooltips slide in on hover: the pointer should not rest on a button
  during the zoom.
- The clip ends with the cards shown and starts without them: the loop seam relies on the kit's
  return to the start; if the SSIM check refuses, the scenario clicks Side-by-side and Diff off at
  the end.
- If a word the diff marks differs from this list (for example "is"/"are" kept as one change), it
  is a finding to read, not a scenario fix (recipe, section 6).
