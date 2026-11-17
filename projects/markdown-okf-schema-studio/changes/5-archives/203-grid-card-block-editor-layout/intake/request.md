# 203 — Block editor layout in a narrow grid card (#225, #226)

P1 batch 2026-10-31 (user request via the Chief of Staff). Stack of 2 ready PRs: CR 203 (base main) then CR 204 (base CR 203). Never merge.

Backlog intent (verbatim):

> # Block editor in a narrow grid card: palette covers the text box; card title editor unreadable
> 
> GitHub issues #225 and #226 (filed 2026-10-31). In a `{grid} 1 2 3 3` of `{grid-item-card}`, editing
> a card body opens the block editor inside the narrow card: the edition palette wraps onto 5-6 rows
> and covers the text box (typed characters disappear under it). Editing a card title squeezes the
> text box and the palette into the title area, so nothing is visible.
> 
> Owner decision (2026-10-31): widen the card and push its neighbours.
> - While a block editor is open in a grid card, the card gets a minimum width and pushes the other
>   cards aside, like the table-cell editor.
> - The edition palette sits ABOVE the text box, may be wider than the card, has a max height and
>   scrolls vertically.
> - The text box has a minimum width so a card TITLE editor (#226) shows its source readably.
> 
> Reproduce: the grid document in issue #225; click the body of card 2 (#225) or the title
> "2. Status projection" (#226).

## Delivery

- PR body: "Closes #225, closes #226". Ready PR, base main. Branch
  `change-requests/203-grid-card-block-editor-layout`.
- Proof: unit tests; headless visual test on the issue's exact grid document (card body and card
  title); before/after screenshots on that document in the cream AND dark themes, in the PR body.
- Requirements: update the block-editor layout SwRS (palette placement, text box min width, card
  widening); new requirements use `--lifecycle proposed`. Locked APPROVED StRS are not edited.
- CI: normal CI green. The heavy run goes on the top PR of the stack (CR 204), not here, unless the
  Foreman asks.
- CR 204 (#227, blur stuck) stacks on this branch; push as soon as round 1 is approved so CR 204 can
  rebase onto it.
