# test(cards): inventory every rule of the old cards and restore the lost ones

## Summary

The role cards (the instructions each agent reads) were rewritten to be much shorter. Nothing showed
that no rule protecting the user or the repository was dropped on the way. This change puts every
rule of the old card set in one table, with where it lives now and how it is checked, restores what
was lost, and adds a test that keeps the table true.

## Deliverables

- `docs/proofs/cards-inventory.md` (generated): one row per old rule, the ranges that hold no rule,
  four lists for the project owner and a closed hand-over checklist.
- `test_cards_inventory.py`: every home and check resolves, every old line is covered, and a rule
  that protects the user or the repository lives only in a floor rule, a role card or a CLI refusal.
- The eval kit's quiz cases may cite an inventory row id.

## Blast radius

- **2**: a proof file, a test, the eval kit's loader and card text; a plain revert restores it.

## Autonomous decisions

- Row ids accept an optional `B` and four digits, because the existing ids must stay unchanged.

## Known gaps

None

<details><summary>Details</summary>

## Changes

- `docs/proofs/cards-inventory.md`, `skills/chantier/scripts/cli/tests/test_cards_inventory.py`:
  new.
- `evals/kit/quiz.py`, `evals/kit/dry_run.py`, `evals/README.md`: inventory row ids in `rules`.

## Impacts

No visual change.

## Test plan

- [ ] `just check`
- [ ] `just eval-dry-run`
- [ ] Review

## Internal references

CR-511 sc25-cards-compare-review

</details>
