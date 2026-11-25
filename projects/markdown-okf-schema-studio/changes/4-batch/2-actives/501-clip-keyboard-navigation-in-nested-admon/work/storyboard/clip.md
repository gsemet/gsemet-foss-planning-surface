---
title: Feature clip keyboard-navigation
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: keyboard-navigation

**This is the live storyboard.** The clip is built from this file: edit any row marked
*(on screen)*, save, and run `just clip keyboard-navigation render`, then `check`. Rows marked
*(filmed)* describe the take: changing them means a new take. The owner reviews this file and the
clip in the pull request; the times and pictures come from the batch's take. `**bold**` in a text
takes the orange accent.

The clip is one continuous shot, and the mouse is never used: the pointer stays still in the
bottom right corner of the page the whole time. Eleven key presses, each shown as a badge: `E`
turns edit mode on, the arrows pick and descend, Enter opens, Escape closes, Ctrl/Cmd+Enter saves.
It shows three texts in turn.

## Clip

| Field | Content |
| --- | --- |
| Length | 20.0 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none: every setting at its default |
| Filmed on | Windows, the VS Code version and the extension version written in `check.json`, VSIX built from the branch |
| Stage | `stage/release-plan.md` (Studio, the whole window, reading mode, Cream): a heading, a `note` admonition titled "Before the release" that holds a sentence and a list of three items (the second one with two sub-items), then a closing sentence |

Off camera (`setup`): the toolbar expanded (so the Edit toggle is in view), Studio in reading mode,
the page in Cream, no block selected. The keyboard focus is given to the page with one click in the
blank right margin of the page (in reading mode a margin click selects and opens nothing), then the
pointer is parked in the bottom right corner of the page, off every block and off the zoom. Frame 0
shows no selection ring and no hover.

## 1. E for edit mode, the arrows pick a block

Pictures: ![Edit mode on](frames/edit-on.png) ![The admonition selected](frames/admonition-selected.png) ![The whole admonition in its editor](frames/admonition-editor.png) ![The editor closed, the admonition still selected](frames/admonition-back.png)

| Field | Content |
| --- | --- |
| Time | 0 to 7.8 s (E at 0.6 s, Down at 2.2 and 3.6 s, Enter at 5.2 s, Escape at 7.0 s) |
| Shot *(filmed)* | Studio on `release-plan.md` in reading mode. `E`: the Edit toggle of the toolbar turns on. Down: the heading is selected (the first press takes the block nearest the top of the pane). Down: the selection ring moves to the admonition. Enter: the whole admonition opens in its source editor, from `:::{note} Before the release` to the closing `:::`. Escape: the editor closes with nothing changed, and the admonition stays selected. |
| Text 1 *(on screen)* | Press **E**, then the arrows pick a block |
| Badge edit *(on screen)* | E |
| Badge down *(on screen)* | ↓ |
| Badge enter *(on screen)* | Enter / ↩ |
| Badge escape *(on screen)* | Esc |

## 2. Right goes one level deeper

Pictures: ![Zoom on the admonition, its sentence selected](frames/sentence-selected.png) ![The list selected](frames/list-selected.png) ![The first item selected](frames/item-selected.png)

| Field | Content |
| --- | --- |
| Time | 7.8 to 12.6 s (zoom from 8.0 s; Right at 8.6 s, Down at 10.2 s, Right at 11.8 s) |
| Shot *(filmed)* | Zoom (at most 2x) on the admonition. Right: the selection goes inside the admonition, to its sentence. Down: the selection moves to the list below the sentence, inside the admonition. Right: the selection goes inside the list, to its first item "Tag the release on Friday". |
| Zoom | admonition, hold to 19.2 s |
| Text 2 *(on screen)* | **Right** goes one level deeper |
| Badge right *(on screen)* | → |

## 3. Edit one item, save

Pictures: ![The item alone in its editor](frames/item-editor.png) ![The word changed](frames/word-changed.png) ![Mark 1 on the saved item](frames/04-mark-1.png)

| Field | Content |
| --- | --- |
| Time | 12.6 to 20.0 s (Enter at 13.4 s, Ctrl+Backspace at 15.0 s, "Thursday" typed from 15.4 to 16.0 s, Ctrl+Enter at 16.8 s; then back to the start for the loop) |
| Shot *(filmed)* | Enter: the first item alone opens in its editor, the caret at the end of its text. Ctrl+Backspace (Option+Backspace on macOS) deletes the last word, "Friday"; "Thursday" is typed. Ctrl/Cmd+Enter: the editor closes, the item reads "Tag the release on Thursday" and stays selected; the rest of the admonition is unchanged. |
| Mark 1 *(on screen)* | Orange outline around the saved item, 17.4 to 19.0 s |
| Text 3 *(on screen)* | Change a word and **save**, no mouse at all |
| Badge delete-word *(on screen)* | Ctrl+⌫ / ⌥⌫ |
| Badge save *(on screen)* | Ctrl+Enter / ⌘↩ |

Expected result, the scenario's check (read from the preview after each press, and from disk):

- After `E`, the page is in edit mode (`data-sphinx-preview-edit-mode` is `on`); it was `off` at
  the start.
- After each press the selected element (`data-sphinx-preview-block-selected`) is, in turn: the
  heading, the admonition, (Enter) a block editor whose text starts with `:::{note} Before the
  release` and ends with `:::`, (Escape) no editor and the admonition, the sentence "Run these steps
  in order, one person per step.", the list, its first item.
- After the second Enter, the block editor holds the first item only (not the whole list or the
  whole admonition).
- After Escape, `release-plan.md` on disk is byte for byte `stage/release-plan.md`.
- After Ctrl/Cmd+Enter, no editor is open, the first item is selected and reads "Tag the release on
  Thursday", and `release-plan.md` on disk (after the autosave) is `stage/release-plan.md` with
  `Friday` replaced by `Thursday`, nothing else changed.

## Review notes

- **The `E` key and the Enter key.** The owner's request uses `e` at step 6 to open the list for
  editing. In Studio `E` alone turns edit mode on from reading mode (SwRS-MDOKFSTUDIO-LIFE-172,
  `src/page/features/editMode.ts`) and does nothing in edit mode; Enter opens the selected block,
  item or inner block (SwRS-MDOKFSTUDIO-BLOCK-004, SwRS-MDOKFSTUDIO-BLOCK-254,
  `src/page/features/blockSelectionView.ts`, `src/page/features/structuralNavigationView.ts`). The
  clip keeps the owner's intent, "how easy it is to enter editing with `e`", by pressing `E` first,
  and uses Enter at step 6 (keyboard-nav-Q6).
- **What Right selects.** Right on the admonition selects its first inner block, the sentence
  (owner's step 3, as written). Down then selects the list (owner's step 4). Right on the list
  selects its first item, not the list: the list is already selected by Down
  (`src/page/modules/structuralCursor.ts`, `docs/user/editing.md` "A list has three levels"). The
  clip edits that first item (keyboard-nav-Q7).
- **How the first block is selected without the mouse.** In edit mode with no selection, the first
  Down selects the block nearest the top of the pane, here the heading; a second Down reaches the
  admonition (`stepSelection` in `blockSelectionView.ts`). Right with nothing selected would select
  the first block of the page too. The keyboard focus itself is given to the page off camera, with
  one margin click in `setup` (keyboard-nav-Q8).
- **The admonition title.** The trial checks that Right lands on the sentence, not on the title "Before
  the release". Right goes to the first mapped block inside the admonition (`mappedChildren` in
  `src/page/features/mappedBlocks.ts`), and SwRS-MDOKFSTUDIO-BLOCK-254 says "its first inner
  block". If the take shows the title selected first, it is a finding against the feature, reported
  with what was selected, and the clip waits.
- **Changing one word.** The editor opens with the caret at the end of the item's text
  (`focusTextControlAtLastContent` in `src/page/features/textControls.ts`), so the changed word is
  the last one: Ctrl+Backspace on Windows deletes it (a native text box key; Studio does not take
  it). On macOS the same key is Option+Backspace: the scenario presses `Control+Backspace` on
  Windows and `Alt+Backspace` on macOS, never `ControlOrMeta`, which would be Cmd+Backspace (delete
  to the line start) on macOS. The letters of "Thursday" are typed with no badge, as the address of
  `export-html` was: the typed word shows in the editor (keyboard-nav-Q9).
- **The badge of the word delete.** `Ctrl+⌫ / ⌥⌫` passes the storyboard check when filmed on
  Windows. Filmed on macOS, the kit would refuse it: its combined form wants `⌘` in the second group,
  and this key has `⌥`. The take is filmed on Windows, so no kit change is needed now; the smallest
  change, if a macOS take is wanted later, is to accept `⌥` as well as `⌘` in the second group of
  `isCombinedBadge` (`clip-kit/lib/storyboard.mjs`).
- **Length.** 20 s: eleven presses about 1.6 s apart (a badge shows 1.2 s and fades over 0.33 s, so
  two badges never overlap, except the two Down presses 1.4 s apart, the same key), plus the mark.
  The 30 s limit of the kit comes from the CR `clip-the-advanced-renderings-tour`
  (keyboard-nav-Q5). The GIF budget (3 MB) at 20 s may need the kit's ladder (10 fps, 800 px);
  `check.json` reports the step used.
- **The loop seam.** The clip starts in reading mode with "Friday" and ends in edit mode with
  "Thursday" and the item selected. The differences are small (the Edit toggle, one word, one ring),
  but the seam SSIM (at least 0.98) is measured by `check`. If it fails, the fallback is a last
  Escape press at 19.4 s, badge Esc: it moves the selection up from the item to the list, which
  the zoom no longer shows; if that is still not enough, the batch reports it in the PR and the
  owner decides on a retake (keyboard-nav-Q10).
- **The pointer.** It never moves, so the keyboard selection ring is never hidden by a pointer move
  (`bindHover` in `editMode.ts`).
- The edit is a real change to the file: the take restores the stage before each run (the kit
  copies `stage/` into a fresh workspace).
