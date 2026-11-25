---
title: Feature clip figure-editor
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: figure-editor

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/figure-editor/clip.md` and the clip is rendered from it.

The clip is one continuous shot: the Edit figure button, the form filled from the keyboard, Apply,
then a zoom on the rewritten directive and on the figure drawn in its new place. It shows two texts
in turn. The times below are the Griller's proposal; the batch's trial take sets the real ones and
adds the pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 12.0 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none (default palette mode and Cream theme; edit mode is set off camera) |
| Filmed on | to be filmed by the batch |
| Stage | `stage/harbour-guide.md` (Studio, the whole window, edit mode): a heading, a sentence, a `{figure}` of `stage/harbour-light.svg` (400x240, centred, an alt text and a one-line caption, no other option) and a paragraph of three lines under it |

Off camera (`setup`): edit mode on, no block editor open, the pointer parked in the right margin,
away from the figure (no Edit figure button and no hover outline at frame 0).

## 1. Edit figure, fill the form

Pictures: from the batch's trial take (key frames `button`, `form`, `filled`).

| Field | Content |
| --- | --- |
| Time | 0 to 6.0 s (pointer on the figure at 0.8 s, click on Edit figure at 1.6 s, the form shown by about 2.0 s, click in Caption at 2.8 s, caption typed by 3.8 s, Width typed by 4.4 s, Align by 4.7 s, Name typed by 5.3 s, Enter at 5.6 s) |
| Shot *(filmed)* | Studio in edit mode on `harbour-guide.md`. The pointer moves onto the figure: the Edit figure button shows at its top right. The pointer clicks it: the figure's text box opens with the edition palette and, between them, the Figure form (Source, Alt text, Caption, Legend, Width, Align, Name), filled from the directive. The pointer clicks in Caption; its text is selected and replaced by "Harbour light at dusk, from the north pier.". Tab, Tab: Width gets "40%". Tab: Align is set to Right from the keyboard (its list is not opened). Tab: Name gets "fig-harbour-light". Enter: the form closes and the text box holds the rewritten directive. |
| Text 1 *(on screen)* | **Edit figure** opens one form for the whole figure |

## 2. The directive, then the page

Pictures: from the batch's trial take (`03-zoomed`, `04-mark-1`, `05-mark-2`, and the key frame `rendered`).

| Field | Content |
| --- | --- |
| Time | 6.0 to 12.0 s (zoom from 6.2 s, held to 11.0 s; save chord at 8.6 s; then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the text box and the paragraph under it: the directive now has the lines `:width: 40%`, `:align: right` and `:name: fig-harbour-light` under the kept `:alt:` line, and the new caption. Save chord: the text box closes and the figure is drawn at 40% of the column, floating right, with the new caption; the paragraph wraps on its left. |
| Zoom | figure, hold to 11.0 s |
| Mark 1 *(on screen)* | Orange outline around the three new option lines in the text box, 6.8 to 8.2 s |
| Badge save *(on screen)* | Ctrl+Enter / ⌘Enter |
| Mark 2 *(on screen)* | Orange outline around the rendered figure and its caption, 9.2 to 10.8 s |
| Text 2 *(on screen)* | Apply writes the **options** into the file |

Expected result, the scenario's check: `harbour-guide.md` on disk (auto-save is on) is exactly this
text, followed by one newline:

```markdown
# Harbour guide

The north pier is open to walkers from dawn to dusk. Keep to the marked path.

:::{figure} harbour-light.svg
:alt: A lighthouse on a rock at dusk
:width: 40%
:align: right
:name: fig-harbour-light

Harbour light at dusk, from the north pier.
:::

The light was built in 1874 and still guides the fishing boats home. Its beam turns once every
ten seconds and reaches eighteen nautical miles on a clear night. The keeper's cottage beside it
is now a small museum, open on weekend afternoons from April to October.
```

And, read from the preview after the save chord:

- the `figure` has the class `align-right` and its image has `data-okf-width` `40%`;
- its id is `fig-harbour-light` and its caption reads "Harbour light at dusk, from the north pier.";
- no block editor is open; `harbour-light.svg` on disk is byte for byte the stage file.

## Review notes

- What the form writes comes from `applyValues` and `serializeFigure` in
  `src/page/modules/figureDirective.ts`: the opening line and the `:alt:` line are kept as read, the
  new options are appended in the order width, align, name, one blank line stays before the caption,
  and the edited caption replaces the body (SwRS-MDOKFSTUDIO-PALETTE-160). The expected text above
  is derived from that code; the take proves it.
- The button, the fields, their order and the keys come from `src/page/modules/figurePanel.ts` and
  `openFigurePanel` in `src/page/features/editorChrome.ts` (SwRS-MDOKFSTUDIO-PALETTE-153): the
  "Edit figure" button over a hovered figure in edit mode, the form named "Edit figure" inserted
  above the text box, Source focused first, Enter in a one-line field (Name) applies, Tab goes
  through Source, Browse..., Alt text, Caption, Legend, Width, Align, Name.
- Apply only rewrites the text box: the editor stays open and auto-save (400 ms) writes the file.
  The save chord closes the box so the page shows the figure in its new place
  (`docs/user/editing.md`, "Inline editing"). The rendering of width, alignment, caption and id is
  SwRS-MDOKFSTUDIO-MYST-031 (`src/core/directives/figure.ts`, `src/page/modules/figureSizes.ts`).
- Browse... is not filmed: it opens the system file dialog, outside the filmed page. The Source
  field is left as it is.
- Align is a `<select>`. Its open list may be drawn outside the screencast, so the clip sets it from
  the keyboard ("r" on the focused list picks Right) and never opens it. If the trial shows that the
  key does not change it, `run` sets it with the frame's `selectOption` and the shot shows only the
  value change.
- The keys of the form (Tab, typed text, Enter) go through `page.keyboard`, without a badge, like the
  typed keys of the slash-menu-grid clip; only the save chord has a badge.
- The name is the figure's label: it becomes the figure's id, the target of a `{ref}`. No `{ref}` is
  filmed; the clip shows the `:name:` line and checks the id.
- The zoom must hold the text box before the save and the figure after it: `run` takes the union of
  the text box and the paragraph under it as the zoom rectangle. If the figure lands outside it at
  the trial, the rectangle is widened, never a second zoom.
- The Legend field stays empty: a legend would add a second paragraph and about 1 s of typing.
- If the trial runs past 12 s, the Name step is dropped first (figure-editor-Q8).
- The clip ends with the small floating figure and starts with the large centred one: the loop seam
  relies on the kit's return to the start.
