## Summary

Studio now has a short feature clip that shows review in the page itself: a sentence is selected in the preview, the **Comment** button is pressed, a comment is typed and saved with Ctrl+Enter / ⌘Enter, the sentence is highlighted, and a click on it opens the thread with its Reply box and its Resolve and Delete buttons. The clip is made with the clip kit and the feature clip process, filmed in a real VS Code window with the packaged extension. This pull request is a **draft** until the maintainer approves the storyboard and the clip in it.

## Deliverables

The clip (11.3 s, silent, loops), played from this pull request's head `7a02a84`:

![The comment thread clip: select a sentence, comment, save, open the thread](https://github.com/gsemet/markdown-okf-schema-studio/raw/7a02a841ed5a119ac951e3e36b4100a4edf9bfc5/docs/demo-video/clips/comment-thread/comment-thread.gif)

- MP4: https://github.com/gsemet/markdown-okf-schema-studio/raw/7a02a841ed5a119ac951e3e36b4100a4edf9bfc5/docs/demo-video/clips/comment-thread/comment-thread.mp4
- WebM: https://github.com/gsemet/markdown-okf-schema-studio/raw/7a02a841ed5a119ac951e3e36b4100a4edf9bfc5/docs/demo-video/clips/comment-thread/comment-thread.webm

What the clip proves (the take's own check, `check.json`, at `7a02a84`): `proposal.comments.json` holds one thread with the filmed quote "We drop support for Node 18 in this release." and one comment by `Reviewer`, "Can we keep it one more release?", `resolved: false`; `proposal.md` is unchanged; MP4 and WebM 1280x720 at 15 fps, GIF 960 px at 12 fps, loop seam SSIM 0.99661, playback rate 1.005, reading mode off, no paste widget.

What the maintainer judges: motion, rhythm, the loop as watched, the two caption texts and their times, the storyboard `docs/demo-video/clips/comment-thread/clip.md`.

Deviation from the feature clip process: the process has the maintainer approve the storyboard before the take. Here the storyboard is reviewed after the take, in this pull request, and the pull request stays a draft until then. A row marked *(on screen)* changed in review is a render (`just clip comment-thread render`, then `check`); a row marked *(filmed)* is a retake, done as a follow-up.

## Blast radius

Grade: **1**. Only documentation assets and one docs page change; no source, no requirement. A plain `git revert` removes the clip folder and the image line.

## Autonomous decisions

- The thread is closed at the end of the clip by a click beside the paragraph, not by Escape: every key press of a take needs a badge, and Escape would add an unwanted badge and move the kit's last key frame.
- The storyboard splits the size and the frame rate into their own `Size` and `Frame rate` fields and adds a `Zoom` row, as the kit reads them.
- The clip is 11.3 s long, not the draft's 10.8 s: the pointer's trip made the close click come too late, so the take was re-timed (zoom released at 9.6 s, close click at about 10.4 s) to keep the playback rate at 1.0.
- The GIF is placed under the paragraph "To start a thread, select text in the preview" of `docs/user/review-comments.md`, with an alt text that describes the sequence.
- The thread opens on a click on the highlight, because Studio opens no thread by itself after Save.

## Known gaps

- Windows only: no macOS or Linux take; the ⌘Enter badge is a caption, not a filmed key.
- An empty `comments.authorName` (the Git user name is then shown) is not filmed, to keep personal data off screen.
- Motion, rhythm, the loop as watched and the GIF playing in the rendered pull request page are not checked by the author. **UNVERIFIED:** that GitHub plays the Git LFS GIF inline.
- The popover shows the date of the take (11/25/2026).
- The contact-sheet tile at 8.475 s shows no mark although the MP4 shows mark 2 there.

<details>
<summary>Details</summary>

## Changes

- `docs/demo-video/clips/comment-thread/`: the live storyboard `clip.md` (status draft), the scenario `scenario.mjs`, the stage `stage/proposal.md`, and the rendered MP4, WebM, GIF, poster, contact sheet, first/last frames, key frames `frames/*.png` and `check.json`.
- `docs/user/review-comments.md`: the GIF added after the paragraph that explains how to start a thread.
- No change to the clip kit, the process guideline, `src/`, requirements, README, changelog or release notes.

## Impacts

A new demo clip and one image on the review comments page; no change to the extension's behaviour. The clip, played at `7a02a84`:

![The comment thread clip at the pull request head](https://github.com/gsemet/markdown-okf-schema-studio/raw/7a02a841ed5a119ac951e3e36b4100a4edf9bfc5/docs/demo-video/clips/comment-thread/comment-thread.gif)

[MP4](https://github.com/gsemet/markdown-okf-schema-studio/raw/7a02a841ed5a119ac951e3e36b4100a4edf9bfc5/docs/demo-video/clips/comment-thread/comment-thread.mp4) and [WebM](https://github.com/gsemet/markdown-okf-schema-studio/raw/7a02a841ed5a119ac951e3e36b4100a4edf9bfc5/docs/demo-video/clips/comment-thread/comment-thread.webm) at the same head.

## Test plan

- [x] New or changed tests: none, no behaviour change
- [x] Requirements: no behaviour change
- [x] Changelog: no user-facing change
- [x] Local gates at `7a02a84`: `just check`, `just preflight` (static stage on Windows), `just clip comment-thread all --vsix …` (check.json passed)
- [x] Review: Inspector approved at `f42acf7`, committed as `7a02a84`; Verifier VERIFIED at `7a02a84`
- [x] CI green at `7a02a84` (static, static-windows, viewer-graph, visual, checks, report)

## Internal references

- CR-486 clip-comment-thread, batch batch-09, stacked on CR-484 (the clip kit's storyboard, captions and marks).

</details>
