# Verify CR-496 (okf-frontmatter clip)

Head: 39d3eb31801f1679b444e52afa9951ca2ec3daef

All claims judged at 39d3eb31801f1679b444e52afa9951ca2ec3daef. Base is CR-493's branch (spec's origin/main superseded).

## Claims

1. `just clip-kit-test` at the head: `ℹ tests 41 / pass 41 / fail 0`, including "the shipped okf-frontmatter clip.md reads as the clip the owner reviews", "the stage ... byte for byte", "changes the status line only, on a page with no type and no schema folder". Judged at 39d3eb31.
2. `check.json` at the head: `passed: true`; mp4 and webm 1280x720 at 15 fps, 11.533 s vs Length 11.5 s; gif 960 px at 12 fps, loopCount 0; loopSeamSsim 0.995531 (in [0.98, 1.0)); `verifyPassed: true`; playbackRate 1.005; editMode on, paste false; platform win32; extensionSource vsix; all 20 checks ok. Judged at 39d3eb31.
3. Committed media at the head: `ffprobe` gives mp4 h264 1280x720 15/1 11.533 s; webm vp9 1280x720 15/1 11.534 s; gif 960x540 25/2 (12.5 reported by ffprobe for the 12 fps ladder, check.json says 12/1) 11.5 s. Sizes on disk equal check.json bytes (mp4 331710, webm 234683, gif 1224198): real LFS content, not pointers. `git lfs ls-files` lists all 12 media files. Judged at 39d3eb31.
4. Stage, scenario, docs page: `stage/release-note.md` is the spec's text (no type, five fields, tags list, `= this.status`); `docs/user/okf.md` gains the one GIF image after the "Studio makes that metadata comfortable" paragraph, before "Linked-File Annotations", alt text as spec. `clip.md` read in full: front matter, `## Clip` table, the two sections, Expected result block, review notes with measured times, "Not checked by the author" line, as spec. The only non-clip files in the diff of the two commits are the kit tests, `siteClips.test.ts` and `docs/user/okf.md`; no `src/` change. Judged at 39d3eb31.
5. Looked at the contact sheet and each key frame (Read of the png, copies in `evidence/`):
   - contact-sheet.png: 12 frames, edit mode, Names and Values table with five rows, no Description column or type icon, frame 0 reads "Status: draft", text box in the status cell (0.96 s to 3.83 s) with "Add field / Remove field" menu under it, then published in row and body, save badge at 4.79 s, Text 1 until about 6.2 s then Text 2, mark 1 on the status row, mark 2 on the Status line.
   - editing.png: pointer and ripple on `draft`, status row highlighted, edit mode, Text 1. Matches the PR's own gap (taken at the click, box not yet drawn).
   - 01-selected.png: `published` typed in the status cell box, body still "Status: draft".
   - 02-pasted.png: box closed, row and body read `published`, badge "Ctrl Enter / Cmd Enter", Text 1.
   - 04-mark-1.png: zoom, orange outline on the status row, Text 2. 05-mark-2.png: orange outline on "Status: published", Text 2.
   - 03-zoomed.png (no mark; the outline just fading in, faint) and first-last.png (left frame 0, right last frame; the right one shows a faint ghost residue next to "draft", disclosed in Known gaps).
   - No dirty dot on the tab; window title is "release-note.md - workspace - Visual Studio Code"; no user name, home folder or path in any image. No tooltip or hover at frame 0.
   Judged at 39d3eb31.
6. Text scan of the clip folder's md, mjs and json for the user name and `C:/Users`: no match. Judged at 39d3eb31.
7. PR #517: draft, open, head 39d3eb31801f1679b444e52afa9951ca2ec3daef, base CR-493's branch. Posted body equals `work/pr-body.md` (only a trailing newline differs). The GIF, MP4 and WebM raw URLs name the head sha and answer HTTP 200 (GIF GET downloads 1224198 bytes = the file). Summary, Deliverables, Changes, Deviation section, Known gaps (stepwise 3 fps, first-last ghost, editing.png at the click, no "Saving" text) match the diff and the images. No role name used as the doer; "Review" and "CI green" boxes unchecked, which is true at this head. Judged at 39d3eb31.
8. Review box: `$CHANTIER log CR-496` has "r1 approved at da86d6e8 ..., committed as 39d3eb31" by the Driver; the PR body does not claim a Review line. Not an issue.
9. CI at the head (`gh pr checks 517`): static pass, static-windows pass, viewer-graph pass; visual pending (re-run 1 after a job timeout, infra); integration, stress, release-check, toc-loop skipping. Not a CR failure; the ship event notes no long gate passed.

## Not checked

Motion, rhythm and the loop as watched (no video playback); the raw screencast at 3 fps retimed (stepwise look); no new take run (the display is shared); `just check` and `just ci-static` not rerun (CI static and static-windows pass at the head); the visual CI job result is pending.

## Images vouched (evidence/)

contact-sheet.png (the whole clip in 12 frames), editing.png (click), 01-selected.png (typed published in box), 02-pasted.png (saved, badge), 04-mark-1.png (status row mark), 05-mark-2.png (Status line mark).

VERIFIED
