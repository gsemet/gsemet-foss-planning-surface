# Split the SwRS BLOCK-258 requirement

Type: docs / requirements · Priority: P3 · Filed 2026-11-01 from CR 221 and CR 217 reviews

## Today

`requirements/tiers/swrs/block-editing/SwRS-MDOKFSTUDIO-BLOCK-258.md` (status `proposed`) grew over
several CRs. It now holds:
- the click mapping on a card title;
- the one-line editor rule (Enter commits a one-line card editor) with its key table;
- the linked-title union (a `:link:` card keeps a source mapping, CR 217).

The guideline says one SwRS is one observable behaviour. CR 221 reviewers (round 1 finding 3, round 3
point 2) said a split could be considered before approval. Related open items: grid-card-title-and-options,
block-258-done-e2e (they touch the same file).

## Expected

Separate SwRS for the click mapping, the one-line editor key rule and table, and the linked-title
rule; fix cross-references and tests' `@tests_req` tags. Do it before BLOCK-258 is approved.

Proof: the requirements validation passes; each new SwRS has its own scenario table and test link.
