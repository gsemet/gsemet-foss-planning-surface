# A `+++` line inside a MyST directive or container crashes the MyST render

Type: bug · Priority: P2 · Filed 2026-11-01 from CR 223 reviews (round 2 and round 3)

## Today

`+++` (the MyST block break) inside a directive or a quoted block throws, and the whole document
fails to render:
- `renderMyst(":::{note}\na\n+++\nb\n:::")` throws `TypeError: Cannot read properties of undefined
  (reading 'length')` in `mdast-util-to-hast/lib/state.js:487`. `+++ {"a": 1}` throws the same way.
- A quoted `> +++` and a list item `- +++` throw too; so do `> [!NOTE]\n> a\n- +++` and
  `> [!NOTE]\n> a\n> +++`.
- All of these also fail on `origin/main` before CR 223. CR 223 only fixed the lazy-line path after an
  alert (`lazyLineAsText` in `src/core/syntax/blockQuoteRange.ts` now escapes a leading `+++`).
- Unquoted `+++` after a blank line is a valid block break and works.

## Expected

A `+++` line in a directive, container, quote or list item never throws. Either render it as text
(as GitHub does inside an alert) or as a block break, and pick one rule for all containers.
Open point: which rule for `:::{note}` bodies (details to confirm with the owner).

Proof: a render unit test per input above fails before the fix and passes after; a GitHub comparison
for the quote and list cases.
