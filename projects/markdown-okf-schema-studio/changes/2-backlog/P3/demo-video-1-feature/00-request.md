# 170 — Demo video of the extension, three approaches in parallel (EXPLORATORY)

Type: explore · Priority: P2 · Approved by the user, 2026-10-28 · No CI, no product code, no PR to
main (deliverables go to `-assets` branches). Not part of the 1.0.0 gate: it must never slow CR 169
or the release.

## Intent (user, 2026-10-28, verbatim French)

> Tu vas lancer une CR exploratoire pour enregistrer une démo vidéo avec sous titre, souris
> enregistrée, zoom, montage dynamique sympa pour faire la démo de l'extension. Pas de ci, tu pourras
> utiliser computer use si besoin ou un quelconque autre tool l'essentiel c'est la qualité de
> sortie.
>
> But démo de présentation hyper sympa.
>
> Tu m'en fait 3 en //, sur 3 solutions différentes. Tu peux utiliser certain tool toi même à la
> place de sous agent.

## Goal

A presentation demo that makes someone want to install the extension: subtitles, a visible
recorded mouse, zooms on the action, dynamic editing. Output quality is the only criterion. Three
videos, same storyboard, three different production techniques, so the user can compare and pick.

## Common output spec (all three tracks)

- 1920x1080, 30 or 60 fps, H.264 MP4 (`yuv420p`, plays in GitHub, Slack and the Marketplace), 60 to
  90 s. Plus a 15 s cut-down as MP4 and an optimised GIF (≤ 10 MB) for the README.
- English subtitles: burned in (styled, readable, max two lines) and a separate `.srt`.
- Visible cursor with smooth motion and a click ripple; zoom-in on each action, zoom-out between
  scenes; no dead time (cut waits, speed up typing beyond a few words).
- No voice. Music optional and only if royalty-free with a licence that allows reuse; record the
  source and licence; deliver a silent version too.
- Cream theme by default, one scene in Dark. Toolbar real (five rows, motion on).
- Demo content: the repository's demo fixtures (e.g. `test/visual/fixtures/70-release-showcase.md`)
  or a new demo document under the track's own folder; no personal or employer data on screen
  (clean VS Code profile, no other extensions' clutter, neutral workspace name).

## Storyboard (same for the three)

1. Title card: "Markdown OKF Schema Studio 1.0" and the tagline "Read, review and edit rich Markdown
   in one page".
2. Open a Markdown file → Open Preview: the styled page appears (front matter table, prose).
3. Edit where you read: click a paragraph, type, bold with Cmd+B; save; the page updates.
4. Slash menu: type `/` in a new block, insert a MyST admonition or a table.
5. MyST: cards and tabs (switch a tab).
6. Diagrams and charts: a Mermaid diagram and a Vega-Lite chart render.
7. Review: add a comment thread on a sentence; the change bar shows the edit.
8. Navigation: table of contents, the toolbar unrolling, theme switch Cream → Dark.
9. End card: Marketplace link, "Works with your coding agent" (plugin line).

A track may cut or merge scenes if it improves the result; it records why.

## Tracks

| Track | Technique | Recording | Editing |
| --- | --- | --- | --- |
| A "Scripted headless" | Playwright Chromium on the headless preview page (the visual harness), interactions scripted | CDP screencast or Playwright video at 2x device scale; cursor and click ripple injected in the page | ffmpeg: crops/zoompan per scene from a scene list, burned ASS subtitles, crossfades |
| B "Real VS Code + auto-zoom" | A real VS Code window (Electron, clean profile), driven by Playwright Electron or computer use | Screen recording of that window (ffmpeg avfoundation or `screencapture -v`), mouse positions logged with timestamps | Post-processing "Screen Studio" style: zoom and pan that follow the logged cursor with easing, smoothed cursor, subtitles |
| C "Motion design" | Remotion (React video), or an equivalent programmatic editor | Short clips and stills captured with Playwright (headless page) | Composition: animated title and end cards, smooth camera zooms, callouts, kinetic subtitles, transitions |

## Decisions

- Each track has its own Driver, worktree and `-assets` branch
  (`change-requests/170-demo-video-{a,b,c}-assets`); tools (Remotion, moviepy, etc.) are installed
  in the track's own scratch folder, never added to the extension's `package.json` or `pyproject`.
- Track B runs a real VS Code window locally: the user allows it for this CR (exception to the
  "no local real-window tests" constraint, limited to track B). It must not use the user's own VS
  Code profile or windows; it uses a throwaway `--user-data-dir` and `--extensions-dir`, and it
  avoids running while CR 169 needs the machine for anything heavy.
- Each Driver opens the result and checks frames (title, each scene, subtitles legible, cursor
  visible, no clipped UI, no personal data) before hand-back; the Chief of Staff watches all three.
- Hand-back per track: the MP4s, `.srt`, GIF, a contact sheet (one frame per scene), the scripts to
  regenerate, and a short note (time spent, what worked, limits, what it would take to automate).

## Direction for the plan (user, 2026-10-29; still brainstorming, not a plan yet)

- **Goal of this CR, restated:** describe under `docs/demo-video/` the scenarios and the base
  elements (demo documents, capture setup, art direction, pacing, cover and end card, subtitle
  style, formats) needed to rebuild the demo videos from time to time, and to keep them
  homogeneous across takes and releases. The three exploratory tracks and the storyboards in this
  folder are inputs to that, not the deliverable.
- Series kept so far: short videos horizontal (`10-short-videos-horizontal/`), short videos
  vertical (`10-short-videos-vertical/`), demo presentation (`11-demo-presentation/`), chapter
  showcase (`12-chapter-showcase/`, added 2026-10-31: one dynamic demo in chapters, after the
  rhythm of a reference video chosen by the user).
- **Requirement to lock:** the sticky section header shows the heading markers (`#`, `##`, …)
  on purpose. This is intended behaviour, not a bug: write it explicitly in a requirement and get
  it approved by the owner (the stakeholder requirement on "the reader always sees the section
  being read", StRS-MDOKFSTUDIO-TOOLBAR-004, with a SwRS stating the `#` markers). The backlog item
  `sticky-header-shows-hashes` is withdrawn as a bug; whether a long heading wrapping to two lines
  and hiding the first line of the section is acceptable is still to be decided.
