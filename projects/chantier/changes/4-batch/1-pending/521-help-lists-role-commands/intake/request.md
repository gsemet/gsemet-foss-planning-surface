# Group chantier --help and list each role's commands in help

Asked by the owner, 2026-11-27, verbatim: « ouvre un batch et lance ces 7 CR » (open a batch and launch these 7 CRs). Part of the card cleanup, plan steps 1 to 3.

Source files, in the planning folder, under `2-backlog/P1/card-inventory-open-rows/`: `work/fable-review-plan.md` (the plan), `work/fable-review-verdicts.md` (one verdict per file), `02-answers.md` (the owner's decisions, card-cleanup-Q1 to Q5), `intake/owner-cleanup-2026-11-27.md` (the owner's words). The plan is a proposal: its facts are checked against the base before they are used, and its "exists?" claims about what the CLI already prints are not verified.

## Wanted (plan section 6, step 3, item 5; section 4.3)

1. `chantier --help` prints the commands in groups (session, backlog, batch, steering, unit, board: the table of section 4.3, with the commands that exist today only).
2. `chantier help --for <role>` lists the role's commands besides its topics. The CLI knows roles only as data.
3. The folds, each old name kept as an alias: `abandon` and `restore` under `triage`; `park` as `order park`; `inbox` as `msg --read`; `interests` under `journal`; `log` as `handoff --log`; `serve`, `webui`, `live`, `login`, `logout` and `watch` under `board`.

Chief of Staff's reading, to confirm by the owner: only a fold that is a second name for the same code belongs here. A fold that needs new behaviour (`access` folded into the refusals, `phase` set by other commands) and the new commands of the plan are later steps.

Constraints: every old name still runs; the user's existing allow rules still match the command lines the CLI prints (P10); host rows, cards, the scenario and `AGENTS.md` stay true.

Proof: the output of `--help` and of `help --for` for two roles in the PR; each old name still runs, held by a test; `just check` passes.
