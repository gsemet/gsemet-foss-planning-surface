# Behaviour note: the expanded toolbar no longer covers the first lines

## Today
In a pane of 380 to 440 px with the view controls expanded, the toolbar (102 x 166 px, fixed at the
top right) sits over the first two lines of the first paragraph; at 440 px it also covers the end of
a one-line h1. The content keeps only its 31 to 35 px side gutter, and nothing reserves the toolbar's
width for body text (the existing runtime only moves a first-block editor, the Start writing button
or a leading properties table). The h1 does not wrap around the toolbar: it wraps on its own.

## After (proposal)
At the top of the document, the text flows around the toolbar like text around a picture: the
runtime that already measures the toolbar (`firstClearance`) publishes its overlap (width and
height of the part of the toolbar inside the column), and an invisible right float of that size at
the start of the content makes the first lines (h1 and paragraph) end before the toolbar. Below the
toolbar the text uses the full width again. Scrolling keeps the overlay behaviour (text scrolled
under a fixed toolbar is expected). Wide panes, where the toolbar sits beside the column, do not
change (overlap 0).

## Requirements touched
- New SwRS (proposed), layout-width: "Body text keeps clear of the floating toolbar".
- SwRS-LAYOUT-011 (proposed) may gain a sentence about the new published value; LAYOUT-007
  (proposed, 40 px gap) unchanged. No approved requirement changes.

## Choices left open
1. Mechanism: float spacer at the top (proposed) vs a reserved right padding on the whole column
   (wastes 100 px all along the document) vs narrowing only the overlapped blocks.
2. Scope: any toolbar state and any width where the toolbar overlaps the column (proposed; the
   collapsed toolbar never overlaps text at 380-440 px, so it changes nothing in practice) vs
   only the expanded toolbar under 440 px as the intent words it.
3. Block boxes: a block border or background that starts beside the float (h1 underline, a note
   box or a code block if it starts that high) still runs under the toolbar; only text lines wrap.
   Proposed: accept (at 380-440 px only the h1 and first paragraph reach the toolbar's height).
4. Not combined with the existing remedies: when the first element is a first-block editor, the
   Start writing button or a leading properties table, the current inset/clearance logic applies
   and no float is added (proposed).
5. Tests: the intent says "no test"; proposed anyway: one unit test in firstClearance.test.ts on
   the published overlap (cheap, not a pixel measure), failing before, plus a headless visual
   check of the first paragraph vs the toolbar at 393 px. Owner can drop either.

## Owner answer (2026-10-31)
APPROVED as proposed, choices 1-5. Both tests kept (unit test on the published size, headless 393 px
no-overlap check). Before shot retaken without the tooltip; after shot same framing, Cream and Dark.

## Round 1 drift (Inspector, reviews/round-1-inspector.md) -> new GATE 226b
The float works for text, but boxes that form their own layout context (tables, centred figures,
code blocks, admonitions, block editor frames) beside it shrink or shift as a whole: 7 visual
scenarios regress (v66-v71 narrow table off-centre by 26 px at 900/1600 px; palette-slash v28 edit
palette covers an editor frame at 900 px). The toolbar overlaps the column up to ~1100 px in Auto and
Margin, and at every width in Full, so this is not only a narrow-pane effect.
Proposal: such boxes clear the float (start below the toolbar's reach, like LAYOUT-011 pushes a first
editor down), text keeps wrapping. Alternatives: (B) float only for panes under 600 px; (C) accept the
narrowing and update v66-v71. Also fixed without a gate: headings clear raw-HTML align images again.

## Owner answer GATE 226b (2026-10-31)
Option A: boxes near the top (tables, figures, code, notes, grids, diagrams, block-editor frames)
start below the toolbar's reach; only text wraps. Full width follows the same rule. Headings clear
raw-HTML align=left/right images again. Update v66-v71, v28 and any scenario A legitimately changes.

## Round 2 limits -> GATE 226c
Option A is implemented, but it needed two exceptions that the owner has not seen yet:
1. If the document's first block is a box (table, image, note, code), it keeps its 40 px gap
   (LAYOUT-007) and gets no float. Moving it below the toolbar broke the first-gap tests v21, v24,
   v27, v46, v47, v48 and v65. Text after that box can still run under the toolbar, as on main.
2. If a document has any aligned image, figure or table (MyST :align: or raw align=), it keeps the
   main layout: no float, and no box clears. The precise variant made the huge-document scenario v20
   time out, and without the exception boxes would clear right-aligned figures.
Proposal: accept both as known issues in LAYOUT-043. Neither changes anything compared with main.

## Owner answer GATE 226c (2026-10-31)
Both exceptions accepted as known issues in LAYOUT-043; LAYOUT-007 unchanged. P3 backlog item filed: 02-backlog/P3/narrow-toolbar-precise-aligned-float-rule.
