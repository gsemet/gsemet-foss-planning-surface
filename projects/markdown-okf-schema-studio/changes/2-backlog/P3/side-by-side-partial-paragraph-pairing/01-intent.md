# Side-by-side pairing for a wrapped paragraph where only some lines changed

Type: fix · Priority: P3 · Filed 2026-11-01 from GATE 234b (owner-accepted edge case)

## Today

The side-by-side diff pairs a current block with its most similar last-commit block, one to one, only when the block
lies entirely inside one line-diff hunk (`src/page/modules/sideBySide.ts`, render). A wrapped paragraph where only some
lines changed is only partly inside the hunk, so it keeps the older behaviour. Next to a removed paragraph it can still be
paired with the wrong last-commit block.

Two other accepted edge cases are related:
- A fully rewritten paragraph (no shared word) next to a removed one: the similarity tie keeps the earlier block.
- An unrelated removal and addition with only blank lines between them become one "changed" card.

## Expected

Pair by block span rather than hunk span, so that a partly changed wrapped paragraph gets the same one-to-one,
similarity-based pairing.

Proof: unit tests in test/page/sideBySideCards.test.ts with a wrapped paragraph where one line changed, next to a
removed paragraph.
