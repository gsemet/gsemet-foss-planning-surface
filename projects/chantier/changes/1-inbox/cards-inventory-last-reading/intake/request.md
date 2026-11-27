# Read the open inventory rows once more, then remove the inventory

Asked by the owner, 2026-11-27, verbatim: « ouvre un batch et lance ces 7 CR » (open a batch and launch these 7 CRs). Part of the card cleanup, plan steps 1 to 3.

Source files, in the planning folder, under `2-backlog/P1/card-inventory-open-rows/`: `work/fable-review-plan.md` (the plan), `work/fable-review-verdicts.md` (one verdict per file), `02-answers.md` (the owner's decisions, card-cleanup-Q1 to Q5), `intake/owner-cleanup-2026-11-27.md` (the owner's words). The plan is a proposal: its facts are checked against the base before they are used, and its "exists?" claims about what the CLI already prints are not verified.

## Wanted (plan section 6, "before step 1"; card-cleanup-Q4 and Q5)

1. Read the open rows of `docs/proofs/cards-inventory-open.tsv` (329 at CR-511's hand-back; recount at the base), with their text in `docs/proofs/cards-inventory.md`, for rules that protect the user or the repository and that no floor line, role card, topic page, CLI or hook refusal holds today. Restore each such rule in one place (the floor, a role card line or an existing page; no new page). The PR says how many rows were read, and for each row judged protective where its rule now lives.
2. Remove the inventory and what exists only for it: `docs/proofs/cards-inventory.md` (1.48 MB), `cards-inventory-open.tsv`, `skills/chantier/scripts/cli/tests/test_cards_inventory.py` and `cards_inventory.py`. The owner's answer speaks of its three tests: `test_card_homes.py` also pins where sentences of the removed cards live; keep any assertion that protects a rule today (the floor's lines, for instance) and drop what only pins a sentence's home.
3. The eval kit reads the inventory (`evals/kit/quiz.py`, `evals/kit/dry_run.py`, `evals/README.md`): the quiz cases keep working without it.
4. The replacement the owner chose is the list of protective rules and a real batch on a test project. Commit the list (plan section 5 and verdicts section D, checked against the base) as one short file the later CRs cite. The real batch is not part of this CR.

Out of scope: deleting topic pages (the next CRs), rewording cards.

Proof: the list of rules restored with their homes; no reference to the removed files left; `just check`, and `just eval-dry-run` since `evals/kit/` changes.