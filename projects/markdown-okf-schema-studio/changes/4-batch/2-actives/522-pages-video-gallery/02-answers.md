Short name: `vidéos`

Destination: running batch batch-11.

# Answers

- 2026-11-27, owner, destination: « tu as un cr sur une gallerie de video. met la dans le batch » (the batch then running, batch-11).

## Facts read at `origin/main` before the grill (not decisions)

- 18 feature clips under `docs/demo-video/clips/<clip>/` (MP4, WebM and GIF, in Git LFS; WebM 235 to 626 KB, GIF 1.1 to 3.1 MB), and one presentation video, `docs/demo-video/short-demo-01/output/short-demo-01.mp4` (12 MB).
- The Pages site already has a screenshot gallery (`gallery.html`); its docs pages show a clip as a looping video of the WebM.
- SwRS CORE-086 names the six links of the site header; CORE-086, CORE-096 and StRS CORE-008 are `req_lifecycle: proposed`.
- The feature clip guideline says the README is not changed: it keeps its presentation video.

## Series 1, 2026-11-27, owner

- `vidéos-Q1` (which videos the gallery shows): « Tout » : the 18 feature clips and the presentation video; a new clip enters the gallery automatically.
- `vidéos-Q2` (where it lives): « Page à part » : a new page of the site with its own « Videos » link in the header.
- `vidéos-Q3` (how a video plays): « Au clic » : a still picture; the video starts on a click.
- `vidéos-Q4` (the light GIFs in the README): « Dans ce CR » : the videos are chosen now, in this change request.

## Series 2, 2026-11-27, owner

- `vidéos-Q5` (editing clips shown as GIFs in the README, several choices): `slash-menu-grid`, `table-anchors`, `figure-editor`. (`paste-spreadsheet-cells`, offered and recommended, was not chosen.)
- `vidéos-Q6` (review and OKF clips shown as GIFs in the README, several choices): `diff-side-by-side`, `radio-buttons`. (`comment-thread`, offered and recommended, was not chosen.)
- `vidéos-Q7` (weight): « Tels quels » : the existing clip GIFs, at most 3 MB each, none regenerated.
- `vidéos-Q8` (placement in the README, the one-minute demo video staying at the top): the owner answered « No preference ». The Chief of Staff takes the recommended option as a routine gap: each GIF goes in the section of its feature, in place of the still picture that shows the same thing, else added to that section.

## After the first specification, 2026-11-27, Chief of Staff (routine gaps)

- Correction: there are 17 feature clips, not 18. The Chief of Staff miscounted in the facts above and in `vidéos-Q1` (18 clips and the presentation video, so 19 videos); the owner's answer, « Tout », does not depend on the count. No clip in flight was meant.
- `table-anchors` stays in the README section « Highest respect for the raw Markdown », where the specification put it: the clip shows the raw table following the drag.
- The one-minute demo video staying at the top of the README is the project's current rule (feature clip guideline) and was stated in `vidéos-Q8`; the owner gave no separate decision on it.
- Spec critic: no (a site page and README pictures; no product behaviour and no approved requirement; a wrong point costs one round).

## What follows from these answers

- The five chosen GIFs weigh about 7.3 MB together (1.1, 1.7, 1.8, 1.4 and 1.3 MB).
- The feature clip guideline sentence « The README is not changed: it keeps its presentation video » no longer holds: the change updates it.

## During the run, 2026-11-27, owner (ask A-1; `evidence/click-probe.txt`)

- `vidéos-Q9` (as specified, with no script and `preload="none"`, a click on the picture starts nothing in Chromium; only the play button does): « Clic sur l'image (Recommandé) » : a few script lines make a click on the picture start the video; no video byte loads before the click (`preload="none"` stays); one more round is accepted. This replaces the specification's « with no script ».
