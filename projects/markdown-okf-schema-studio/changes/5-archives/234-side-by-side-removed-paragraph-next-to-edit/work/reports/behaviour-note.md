# GATE 234b: one-to-one pairing in the side-by-side diff

Round 1 implements the approved rules 1 and 2 and fixes the reported bug (before/after shots in
/private/tmp/claude-502/cr234-driver/shots/). The Inspector found one extra visible change.

## Why a new choice is needed

Rule 1 now merges "edited paragraph, blank line, new paragraph" into one hunk. Read literally, rule 2 lets each
current block keep its most similar last-commit block, so both cards would show the old paragraph on the left
(the new paragraph shown as "changed" instead of "added": a regression). To avoid it, round 1 pairs one-to-one:
a last-commit block goes to at most one current block; a block left without one is "added".

## Today (origin/main)

- Edited paragraph + new paragraph in one Myers hunk (no blank-line merge needed): two "changed" cards, both
  with the old paragraph on the left.
- Edited paragraph, blank line, new paragraph (two hunks): "changed" + "added".

## After (round 1, proposal)

- Both cases: "changed" (old paragraph on the left) + "added" (empty left).

## Edge cases to know (same in both options)

- E. Tie on similarity, e.g. a paragraph fully rewritten (no shared word) next to a removed one: the earlier
  last-commit block is kept, so the reported symptom can come back in that case.
- F. An unrelated pure removal and pure addition separated only by blank lines become one "changed" card.
- G. Rule 2 only reaches blocks that lie entirely inside one hunk; a wrapped multi-line paragraph where only some
  lines changed keeps today's behaviour (no regression, no fix). Proposed as a backlog item.

## Options

1. (recommended) Approve one-to-one pairing as built (SwRS REVIEW-009 proposed already describes it).
2. Literal rule 2 only: case "edit, blank, new paragraph" regresses to two "changed" cards.
