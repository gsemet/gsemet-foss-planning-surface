# Block editor in a narrow grid card: palette covers the text box; card title editor unreadable

GitHub issues #225 and #226 (filed 2026-10-31). In a `{grid} 1 2 3 3` of `{grid-item-card}`, editing
a card body opens the block editor inside the narrow card: the edition palette wraps onto 5-6 rows
and covers the text box (typed characters disappear under it). Editing a card title squeezes the
text box and the palette into the title area, so nothing is visible.

Owner decision (2026-10-31): widen the card and push its neighbours.
- While a block editor is open in a grid card, the card gets a minimum width and pushes the other
  cards aside, like the table-cell editor.
- The edition palette sits ABOVE the text box, may be wider than the card, has a max height and
  scrolls vertically.
- The text box has a minimum width so a card TITLE editor (#226) shows its source readably.

Reproduce: the grid document in issue #225; click the body of card 2 (#225) or the title
"2. Status projection" (#226).
