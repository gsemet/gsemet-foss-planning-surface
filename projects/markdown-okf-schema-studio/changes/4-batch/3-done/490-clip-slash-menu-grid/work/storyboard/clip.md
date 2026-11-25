---
title: Feature clip slash-menu-grid
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: slash-menu-grid

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/slash-menu-grid/clip.md` and the clip is rendered from it.

The clip is one continuous shot: the typed command and the menu, then a zoom on the rendered grid.
It shows two texts in turn. The times below are the Griller's proposal; the batch's trial take sets
the real ones and adds the pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 11.5 s |
| Format *(on screen)* | 1280x720 16:9, 15 fps, silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | `markdownOkfSchemaStudio.editing.defaultPaletteMode`: `myst` (Grid is a MyST command; the default GFM mode does not list it) |
| Filmed on | to be filmed by the batch |
| Stage | `stage/onboarding.md` (Studio, the whole window, edit mode): a heading and one paragraph |

## 1. Type /grid, pick Grid

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 0 to 6.2 s (click at the end of the paragraph at 0.8 s, two Enter at 1.6 s, `/grid` typed 2.0 to 2.6 s, Enter at 3.4 s, Enter in the form at 4.6 s, save at 5.8 s) |
| Shot *(filmed)* | Studio in edit mode on `onboarding.md`. The pointer clicks at the end of the paragraph: its text box opens with the edition palette. Two Enter make an empty line; `/grid` is typed: the slash menu opens at the caret, Grid (MyST) highlighted first, Table under it. Enter: the "Insert grid" form opens (Columns 2, Gutter 2, Cards 2). Enter: the `{grid}` text is written in the box, "Card 1" selected. Save chord: the box closes and the page renders a grid of two cards. |
| Text 1 *(on screen)* | Type **/grid** in a block to insert a card grid |
| Badge save *(on screen)* | Ctrl+Enter / ⌘Enter |

## 2. Zoom on the grid

Pictures: from the batch's trial take.

| Field | Content |
| --- | --- |
| Time | 6.2 to 11.5 s (zoom from 6.4 s, held to 10.5 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the paragraph and the two rendered cards, "Card 1" and "Card 2", side by side. |
| Mark 1 *(on screen)* | Orange outline around the two cards, 7.0 to 8.8 s |
| Text 2 *(on screen)* | A MyST **card grid**, rendered in place |

Expected result, the scenario's check: `onboarding.md` on disk (auto-save is on) is exactly this
text (the blank lines between the paragraph and the grid as the insertion writes them; the trial
take confirms them):

```markdown
# Onboarding

Welcome to the team. Pick the track that fits your first week.

::::{grid} 2
:gutter: 2

:::{grid-item-card} Card 1

Content
:::

:::{grid-item-card} Card 2

Content
:::
::::
```

## Review notes

- `/grid` matches two commands: Grid (MyST, its label) and Table (its alias "grid"). In MyST mode
  the MyST group wins a near tie, so Grid should be first; the trial checks the highlighted entry
  before Enter.
- The two Enter before `/grid` leave an empty line in the box; the grid is inserted after the
  selection, so a stray blank line may stay. Whatever the trial writes is read against the expected
  text above, and a difference is a finding, not a scenario fix.
- The cards keep their placeholder titles "Card 1", "Card 2" and body "Content": typing a real title
  over the selected "Card 1" would add 2 s or more. The owner may ask for it at
  the gate.
- The clip ends with the grid and starts without it: the loop seam relies on the kit's return to the
  start.
