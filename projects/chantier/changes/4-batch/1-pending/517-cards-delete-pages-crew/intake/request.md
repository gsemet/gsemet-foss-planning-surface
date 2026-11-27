# Delete the dead help pages of the Foreman, Driver and host side

Asked by the owner, 2026-11-27, verbatim: « ouvre un batch et lance ces 7 CR » (open a batch and launch these 7 CRs). Part of the card cleanup, plan steps 1 to 3.

Source files, in the planning folder, under `2-backlog/P1/card-inventory-open-rows/`: `work/fable-review-plan.md` (the plan), `work/fable-review-verdicts.md` (one verdict per file), `02-answers.md` (the owner's decisions, card-cleanup-Q1 to Q5), `intake/owner-cleanup-2026-11-27.md` (the owner's words). The plan is a proposal: its facts are checked against the base before they are used, and its "exists?" claims about what the CLI already prints are not verified.

## Wanted (plan section 6, item 1, second half; card-cleanup-Q1)

Delete these 32 pages of `skills/chantier/references/topics/`, each marked delete in the verdicts, with their entries in `references/topics.json`, and fix every pointer to them (cards, other pages, CLI strings, host rows, tests, docs and eval links):

- host notes: host-allow-extra, host-allow-not-add, host-allow-rules, host-allow-rules-copilot, host-auto-mode, host-auto-mode-steering, host-auto-mode-trials, host-claude-only, host-compact-copilot, host-configuration, host-configuration-copilot, host-for-you, host-for-you-sessions, host-foreman-worktree, host-reuse-foreman, host-sessions-copilot, host-sessions-more, host-surfaces, host-write-guard, host-write-guard-shell
- stack: merge-stack-gitlab, stack-run
- release: release-thread
- direct mode: direct-mode-epoch-p2, direct-mode-p1, direct-mode-p3
- workers: verifier-images, worker-shell
- a Driver on its CR: checkpoints, cr-proof, matrix, pr-gitlab

The owner's decision card-cleanup-Q1: all of them are deleted now (git keeps them), and every protective rule goes to its new place first. The PR says, for each protective statement of a deleted page (verdicts section D), where it lives afterwards. Where the verdict's destination does not exist yet (a host row, a card line, a docs file), add it in its smallest form, or keep the rule as a card line when it would need new CLI behaviour (a later step). The CLI's source names at least one of these pages (host-allow-not-add): fix every such string. The owner also asked that cards name no host and no forge tool, save exceptions: do not move a sentence naming one into a card; a host fact goes to a host row.

Out of scope: the pages of the Chief of Staff side (another CR), the aggregate names, joining `-pN` sets.

Proof: the diff is deletions, pointer fixes, the moved rules and tests; `help` lists no dead name; `just check` passes.