# A video gallery on the Pages site, and five GIFs in the README

## Intent

A visitor of the project's GitHub Pages site finds the application's videos in one place, a new
gallery dedicated to videos. A reader of the README sees some features in motion, as light GIFs.

## Decided (owner)

- Priority P2 (2026-11-26, `intake/request.md`).
- For the batch running on 2026-11-27, batch-11 (`02-answers.md`).
- The gallery shows the 18 feature clips and the presentation video; a new clip enters it
  automatically (`vidéos-Q1`).
- It is a new page of the site with its own « Videos » link in the header (`vidéos-Q2`).
- A video shows a still picture and starts on a click (`vidéos-Q3`).
- The README GIFs are part of this change request (`vidéos-Q4`).
- The README shows the GIFs of `slash-menu-grid`, `table-anchors`, `figure-editor`,
  `diff-side-by-side` and `radio-buttons` (`vidéos-Q5`, `vidéos-Q6`), the existing files, none
  regenerated (`vidéos-Q7`).
- The one-minute demo video stays at the top of the README.

## Decided by the Chief of Staff (routine gap)

- Each GIF goes in the section of its feature, in place of the still picture that shows the same
  thing, else added to that section (`vidéos-Q8`, the owner had no preference).

## To grill

Nothing open.

## Facts for the specification

The code and requirement facts are in `02-answers.md`. `scripts/package-extension.mjs` rewrites the
image links of the packaged README to `media.githubusercontent.com`, which serves Git LFS files.
