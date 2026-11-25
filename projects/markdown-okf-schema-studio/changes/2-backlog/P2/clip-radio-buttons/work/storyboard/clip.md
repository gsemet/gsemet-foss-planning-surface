---
title: Feature clip radio-buttons
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: radio-buttons

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/radio-buttons/clip.md` and the clip is rendered from it.

The clip is one continuous shot: one click on an option of the radio group in the page on the left,
then a zoom on the raw text on the right. It shows two texts in turn. The times below are the
Griller's proposal; the batch's trial take sets the real ones and adds the pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 10.5 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none: every setting at its default |
| Filmed on | to be filmed by the batch |
| Stage | `stage/plan.md` opened twice: in Studio (left, reading mode) and in the built-in text editor (right) |

Off camera (`setup`), as in the merged `drag-list-item` clip: the editor split, Studio reopened on
the left with "Reopen Editor With...", the text editor on the right, reading mode checked, the
three radio controls found, and the pointer parked in the blank area below the list. The scenario
declares `checks = { editMode: "off", paste: false }`.

## 1. Click an option

Pictures: from the batch's trial take (key frame `chosen`).

| Field | Content |
| --- | --- |
| Time | 0 to 4.2 s (pointer on the second option's control at 0.9 s, click at 1.3 s, the page shows it selected at once, the raw text shows the moved `x` by about 2.3 s, key frame `chosen` at 3.4 s) |
| Shot *(filmed)* | Studio in reading mode on `plan.md` (left): the heading, the sentence, the label "Approach:" and three round controls in place of the bullets, the first one selected. The same file as raw text (right), with its `- (x)` and `- ( )` lines. The pointer moves to the round control of "Cache the page between sessions" and clicks: that control shows the dot, the first one is cleared. On the right, line 7 changes to `- ( ) Render the visible blocks first` and line 8 to `- (x) Cache the page between sessions`. |
| Text 1 *(on screen)* | Lists of ( ) and (x) become a **radio group** |

## 2. Zoom on the raw text

Pictures: from the batch's trial take (`frames/03-zoomed.png`, `frames/04-mark-1.png`,
`frames/05-mark-2.png`).

| Field | Content |
| --- | --- |
| Time | 4.2 to 10.5 s (zoom from 4.45 s, held to 9.5 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the lines "Approach:" to "Leave as is" in the text editor (right). |
| Zoom | raw, hold to 9.5 s |
| Mark 1 *(on screen)* | Orange outline around the new `(x)` of "Cache the page between sessions", 5.0 to 6.6 s |
| Mark 2 *(on screen)* | Orange outline around the old option, now `( )`, of "Render the visible blocks first", 6.6 to 8.2 s |
| Text 2 *(on screen)* | One click moves the **(x)** in the file |

Expected result, the scenario's check: in the page, the control of "Cache the page between
sessions" has `aria-checked="true"` and the two others `"false"`; `plan.md` on disk (auto-save is
on) is exactly this text:

```markdown
# Plan: faster preview start

The preview takes two seconds to open on large files.

Approach:

- ( ) Render the visible blocks first
- (x) Cache the page between sessions
- ( ) Leave as is
```

## Review notes

- Behaviour checked at `origin/main`: the syntax and the "one click moves the `x`" rule in
  `skills/writing-for-markdown-okf-schema-studio/SKILL.md` and `docs/user/editing.md` (radio choice
  lists); rendering in `src/core/render/radioMarkers.ts` and `radioGroups.ts` (`.myst-radio`,
  `role="radio"`, `aria-checked`, `data-myst-radio-line`, `data-myst-radio-column`), the look in
  `src/core/preview/styles/contentLayoutStyles.ts` (round controls in place of the bullets); the
  click in SwRS-MDOKFSTUDIO-GFM-040 (render) and SwRS-MDOKFSTUDIO-GFM-041 (choice: in reading or
  edit mode, the page shows the choice at once, two lines change, one undo step, no block editor
  opens).
- The scenario clicks the `.myst-radio` control whose `data-myst-radio-line` is 8 (1-based source
  line of "Cache the page between sessions", one-based per `src/core/render/radioMarkers.ts`). It
  reads the right editor's lines as `drag-list-item` does.
- Reading mode is chosen so no edit-mode handles or block outlines show; the choice works in both
  modes (GFM-041).
- After the click the chosen option keeps the focus. Its ring is drawn on `:focus-visible` only,
  so a mouse click should show no ring; the trial checks the frames.
- The clip ends with the second option chosen and starts with the first: the loop seam relies on
  the kit's return to the start, as in `drag-list-item` (a two-character change in the text and a
  dot that moves).
- Not filmed: the keyboard (Space, Enter, arrows), the undo, the refusal while a block editor is
  open, numbered and nested groups. Caption 1 names the syntax as plain text, because the clip's
  caption pill renders only `**bold**`, not code.
- The merged kit has no `README` in `docs/demo-video/clip-kit/`; the recipe and the merged clips are
  the reference used. No kit change is needed: the clip uses the same helpers as `drag-list-item`
  (`open`, `setup`, `moveTo`, `click`, `zoom`, `mark`, `keyFrame`, `workspaceFile`).
