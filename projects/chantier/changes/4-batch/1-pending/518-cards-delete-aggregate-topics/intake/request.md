# Delete the aggregate help topics that only print other pages again

Asked by the owner, 2026-11-27, verbatim: « ouvre un batch et lance ces 7 CR » (open a batch and launch these 7 CRs). Part of the card cleanup, plan steps 1 to 3.

Source files, in the planning folder, under `2-backlog/P1/card-inventory-open-rows/`: `work/fable-review-plan.md` (the plan), `work/fable-review-verdicts.md` (one verdict per file), `02-answers.md` (the owner's decisions, card-cleanup-Q1 to Q5), `intake/owner-cleanup-2026-11-27.md` (the owner's words). The plan is a proposal: its facts are checked against the base before they are used, and its "exists?" claims about what the CLI already prints are not verified.

## Wanted (plan section 6, item 2)

Delete from `skills/chantier/references/topics.json` the aggregate names: names that add no text and only print other topics' pages again (verdicts section C, kind "aggregate", 67 at the plan's base; recount after the page deletions of this batch). Fix every CLI string, card, page, host row, doc and test that names one: the CLI's source names at least lease, watcher, board, stack, stack-merge, refused-push and merge. `refused-push` and `stack` stay as names and become real pages. For each other pointer: name the page that fits. A pointer that truly needs several pages is settled in the specification (name them, or keep that one name as a real page), never by a second copy of a text.

The owner's words behind it: one card per theme, and progressive disclosure organised well enough for the number of pages.

Depends on the two page deletions.

Proof: no CLI string, card or page names a deleted name, held by a test; `help` lists none of them; `just check` passes.
