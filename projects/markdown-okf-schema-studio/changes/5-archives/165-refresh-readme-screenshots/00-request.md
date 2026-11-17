# Refresh the README screenshots to the current UI (five-row toolbar)

Type: docs · Priority: P1 · Filed 2026-10-28 · Part of release 1.0.0 (CR 163, whose release notes
use these pictures). Run in parallel from `origin/main`, not stacked.

## User request (verbatim, French)

> margin-break-cream.png n'a pas la bonne toolbar. reverifie aussi tout le reste.

## Audit by the main session (images/readme on origin/main d48739d7)

Outdated (show the old three-row floating toolbar, or an even older one):

- `showcase-hero.png`, `margin-break-cream.png`, `myst-cards-tabs-cream.png` (and `-dark`),
  `showcase-schema-cream.png`, `theme-cream.png`, `theme-white.png`, `theme-dark.png`
- `edit-frontmatter.png` (old blue-accent toolbar, dark)
- `myst-admonitions.png` (much older toolbar: sun icon, blue accent, cropped at the right edge)

Current (no toolbar, or current palette): `showcase-myst-edit.png`, `slash-menu.png`,
`showcase-diagrams-cream.png`, `charts-cream.png`, `charts-dark.png`,
`showcase-comment-thread.png`, `showcase-diff-cream.png`. `toolbar-collapsed/expanded.png`
were refreshed by #167.

Not checked: `inline-editing.png`, `myst-diagrams-and-figure.png`, `schema-properties.png`,
`open-*.png`, `preview-beside-editor.png` — check them too.

## Expected

- Regenerate every README picture from its capture scenario (captureRegistry / visual scenarios)
  so all of them show the current UI: five-row toolbar (collapsed or expanded as each scene
  needs), current palette, current theme colours. No hand edits of PNGs.
- A cropped toolbar (myst-admonitions) is a bug in the scene framing: fix the crop.
- Keep file names, so README links do not change. LFS as today.
- PR with before/after pairs in the body (the -assets branch convention).

## Decision (user, 2026-10-28, via Chief of Staff): option A

1. Regenerate the headless (Playwright visual) pictures now: add a `--visual-only` flag to the
   README generator (skips the real-window crops) and a crop check for the toolbar.
2. Open the PR (ready) after this first part, so the release notes can use the pictures early.
3. After CR 161 merges: rebase, run heavy CI on the PR branch, take the six real-window pictures
   (myst-admonitions, myst-diagrams-and-figure, inline-editing, open-with-editor,
   open-preview-to-side, preview-beside-editor) from its real-input capture artifact, regenerate
   them with the generator's crops, and push them to the same PR. Fix the myst-admonitions crop box
   in the capture registry.

## Part 1 merged (2026-10-28)

PR #177 (headless pictures, `--visual-only`, toolbar crop check) merged as `cea56337`. Part 2 (the
six real-window pictures) stays open as agreed with the user: follow-up PR from `origin/main` on
branch `change-requests/165-readme-real-window-pictures`, same PRD folder.
