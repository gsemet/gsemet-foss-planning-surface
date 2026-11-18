# The board's drawer, Kanban priority chips and CR titles render correctly

Split from `board-design-realign` (design-Q1, the user, 2026-11-17): the quick bugs the UX QA
found (`../board-design-realign/intake/ux-qa.md`, P0), fixed first, before the full realignment:

1. The CR drawer's file list: the tree's `<span class="nm">` (`panel/tree.js:42`) also matches
   the card band rule (`cards.css:476`: negative margins, grey fill, hairline), which boxes the
   names, overlaps the icons (6 px) and misaligns the sizes; the tree's `.ind` class is also
   Triage's pill style.
2. The Kanban priority filter: `<button class="lab">` with no border reset draws the browser's
   2 px outset border; `.lab::before` adds a grey square that means nothing.
3. Front matter: `panel/markdown.js` renders it as a paragraph ("--- type: ... ---"); show it as
   a muted key/value list.
4. CR titles: `status/views.py:215` `_title()` takes "---" from a front matter, so 6 of 8 batch
   CRs are titled "---" on Batch, PRs, Home and Costs.

The user put it in the running batch (batch-24), 2026-11-17.