# Delete the dead help pages of the Chief of Staff side

Asked by the owner, 2026-11-27, verbatim: « ouvre un batch et lance ces 7 CR » (open a batch and launch these 7 CRs). Part of the card cleanup, plan steps 1 to 3.

Source files, in the planning folder, under `2-backlog/P1/card-inventory-open-rows/`: `work/fable-review-plan.md` (the plan), `work/fable-review-verdicts.md` (one verdict per file), `02-answers.md` (the owner's decisions, card-cleanup-Q1 to Q5), `intake/owner-cleanup-2026-11-27.md` (the owner's words). The plan is a proposal: its facts are checked against the base before they are used, and its "exists?" claims about what the CLI already prints are not verified.

## Wanted (plan section 6, item 1, first half; card-cleanup-Q1)

Delete these 33 pages of `skills/chantier/references/topics/`, each marked delete in the verdicts, with their entries in `references/topics.json`, and fix every pointer to them (cards, other pages, CLI strings, host rows, tests, docs and eval links):

- session, seat, board, watcher: board-lines, board-p2, compacting-p1, compacting-p2, cost, first-turn-p2, options, pr-template-own, session-start-surface-p2, sync-offer-p1, sync-offer-p2, watcher-board-p2, watcher-events-p2, watcher-lines-p1
- starting a batch: allow-rules-more-p2, config-p2, foreman-start-more, forge-permissions-gitlab
- ending a batch: batch-close-p2, batch-close-stopped-p2, demo-p2, retro-lines
- grill and tickets: grill-example, grill-specify-p2, griller-cost, ticket-summary-post-p1
- merge and asks: asks, ready-asks
- steering: orders-queue, qa-order, wakes-p1
- refused push: refused-forge-chain, refused-push-chief-more-p2

The owner's decision card-cleanup-Q1: all of them are deleted now (git keeps them), and every protective rule goes to its new place first. Verdicts section D lists protective statements; among these pages it names at least asks, orders-queue, demo-p2, board-lines, ticket-summary-post-p1, refused-forge-chain, refused-push-chief-more-p2 and watcher-board-p2. The PR says, for each protective statement of a deleted page, where it lives afterwards. Where the verdict's destination does not exist yet (a CLI line, a host row, a card line), add it in its smallest form, or keep the rule as a card line when it would need new CLI behaviour (a later step). A page that turns out to hold something still needed: move that into its new home, and say so in the PR.

Out of scope: the pages of the Foreman, Driver and host side (another CR), the aggregate names, joining `-pN` sets.

Proof: the diff is deletions, pointer fixes, the moved rules and tests; `help` lists no dead name; `just check` passes.