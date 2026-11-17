# Answers

## 2026-11-13: the layout

Owner, 2026-11-13: « normalement tu as compris la reorg, evidement en 4x4. liste moi chaque ligne ».
Chief of Staff's reading of the annotated screenshot: the same 16 controls, in today's reading
order, reflowed into a 4 × 4 grid (each arrow shows a control wrapping up to the end of the row
above):

1. refresh · edit · export · collapse (⌃)
2. link · back · forward · coffee
3. zoom out · zoom in · view ▯ · view ≡
4. view ▯▯ · ⌄ · the two round buttons (♪, comment)

Not confirmed: the owner corrected it (below).

## 2026-11-13: the owner's layout

Owner, 2026-11-13, correcting the reading above (the owner's table, as given):

| Row | Col. 1 | Col. 2 | Col. 3 | Col. 4 |
| --- | --- | --- | --- | --- |
| 1 | refresh | edit | export | collapse (⌃) |
| 2 | link | coffee | back | forward |
| 3 | margin (▯) | collapse titles (≡) | zoom out | zoom in |
| 4 | table of contents (▯▯) | diff | changes | comments |

The coffee goes next to the link; the zoom pair moves to the end of row 3, after the two view
toggles; row 4 holds the table of contents, diff, changes and comments. Open: which of today's
controls are "diff" and "changes" (today's ⌄ and the round ♪-like button), and whether the round
buttons stay round.

## 2026-11-13: mapped to the code

Owner, 2026-11-13: « regarde le code. » The toolbar is `renderPreviewToolbar()` in
`src/core/preview/previewToolbar.ts` (`@implements_req` SwRS-MDOKFSTUDIO-TOOLBAR-001, -005, -134):
today a main row of four (Refresh, Edit, Export, Collapse) and four rows of three in the collapsible
group (navigation: Anchor, Back, Next; appearance: Theme, Zoom out, Zoom in; layout: Width, TOC,
Side-by-side; content: Fold, Diff, Comments). The owner's words, mapped to the buttons by function
(the owner's icons were approximate: ≡ is TOC, ⌄ is Fold, ▯▯ is Side-by-side, ☕ is the Theme
toggle showing the cream theme):

| Row | Col. 1 | Col. 2 | Col. 3 | Col. 4 |
| --- | --- | --- | --- | --- |
| 1 | Refresh | Edit | Export | Collapse |
| 2 | Anchor ("lien") | Theme ("☕") | Back | Next |
| 3 | Width ("margin") | Fold ("collapse title") | Zoom out | Zoom in |
| 4 | TOC ("table of content") | Side-by-side ("diff") | Diff ("changes") | Comments |

The round brown look is no button kind: it is the pressed state (`aria-pressed="true"`) of Diff and
Comments, which are on by default; it stays as is. To confirm with the owner.

## 2026-11-13: confirmed, into the running batch

Owner, 2026-11-13, on the mapped table: « parfait tu as compris la reorg pour passer en 4x4. passe
la dans le batch en cours ». The table above is the layout.

## 2026-11-13: waits for the batch's pause

Owner, 2026-11-13: « tu attend que le batch soit en pause. tu aurais du l'indiquer. » batch-03 runs
in direct mode, which takes no new CR while it runs; this CR joins it with `order add` once it is
paused (after the 1.8.1 release CR has ended), so it is not in 1.8.1.

## 2026-11-13: the specification's open questions

Owner, 2026-11-13: « Ok pour tout ça », on the Chief of Staff's recommendations:

1. Row names (`data-sphinx-preview-toolbar-row` and the user doc headings): `main` (row 1),
   `navigation` (Anchor, Theme, Back, Next), `view` (Width, Fold, Zoom out, Zoom in), `review`
   (TOC, Side-by-side, Diff, Comments).
2. The pending overlay moves up to sit right under the four rows, keeping today's gap (no longer
   192 px for five rows).
3. StRS-MDOKFSTUDIO-LAYOUT-003 (approved) changes: the Width button is on row 3. The owner agrees
   explicitly; `approved_by` and `approved_at` are set again.
4. SwRS-MDOKFSTUDIO-TOOLBAR-007's wrong collapsed Tab order is fixed in this change.

Same answer: this CR and `just-dev-on-fresh-checkout` form the next batch (batch-04), opened after
the owner compacts the Chief of Staff's session.
