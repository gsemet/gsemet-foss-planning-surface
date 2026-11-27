# Join every -pN page set into one page

Asked by the owner, 2026-11-27, verbatim: « ouvre un batch et lance ces 7 CR » (open a batch and launch these 7 CRs). Part of the card cleanup, plan steps 1 to 3.

Source files, in the planning folder, under `2-backlog/P1/card-inventory-open-rows/`: `work/fable-review-plan.md` (the plan), `work/fable-review-verdicts.md` (one verdict per file), `02-answers.md` (the owner's decisions, card-cleanup-Q1 to Q5), `intake/owner-cleanup-2026-11-27.md` (the owner's words). The plan is a proposal: its facts are checked against the base before they are used, and its "exists?" claims about what the CLI already prints are not verified.

## Wanted (plan section 6, step 2, item 3)

Join every set of `-pN` pages of `skills/chantier/references/topics/` into one file (105 pages into 50 at the plan's base; recount after the deletions of this batch), update `topics.json` and every pointer, without rewording: only the part markers (such as "(part 1 of 2)" headings) go. Add a test that no file is named `-pN`. Remove the page-size target of 1,500 bytes wherever it is still written or checked (the plan found no test that enforces it; it came from earlier specifications). A page may be as long as its theme needs; the total size of the folder does not grow.

The owner's words: « deja tous ces cartes p1 p2 ... c'est beaucoup trop. il faut mettre dans une carte un theme. »

Depends on the deletions of pages and of aggregate names.

Proof: a script, quoted in the PR with its output, shows that each joined file equals its parts in order, the part headings aside; the new test; `just check` passes.
