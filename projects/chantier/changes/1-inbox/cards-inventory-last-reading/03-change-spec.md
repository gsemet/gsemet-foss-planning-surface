# Read the open inventory rows once more, then remove the inventory

## Goal

The owner wants the card cleanup to go fast, but without losing a rule that protects the
user. Before the cleanup's step 1 deletes pages, one agent reads the open rows of the old cards'
inventory one last time and looks for protective rules that nothing holds today. Each one it
finds goes back in one place. Then the inventory, and every test and eval-kit path that exists only
for it, is removed. A short list of protective rules replaces it, and the cleanup's later CRs cite
that list (card-cleanup-Q4, answer A).

This CR is the first step of the cleanup batch, "before step 1" in section 6 of the plan
(`2-backlog/P1/card-inventory-open-rows/work/fable-review-plan.md`). The batch is a stack
(answer 2). This CR comes before the CRs that delete pages (`cards-delete-pages-chief`,
`cards-delete-pages-crew`, `cards-delete-aggregate-topics`), because the inventory's tests pin
where each old sentence lives.

## Sources, and how far they are trusted

In the planning folder, under `2-backlog/P1/card-inventory-open-rows/`:

- `work/fable-review-plan.md`: the plan. It is a proposal, so its facts are checked against the
  base before use. Its "exists?" claims about what the CLI already prints or refuses are not
  verified.
- `work/fable-review-verdicts.md`: one verdict per file. Section D lists the protective
  statements, about 96 of them in four slices.
- `02-answers.md`: the owner's decisions card-cleanup-Q1 to Q5.
- `intake/owner-cleanup-2026-11-27.md`: the owner's words.

Measured at 4d12a5b (main when this was written): `docs/proofs/cards-inventory-open.tsv` holds
329 open rows: 62 of kind a, 139 of kind b, 1 of kind c, 112 of kind e, 11 of kind d and 4 of
kind f. The Driver counts them again at the base it branches from.

## What changes

### 1. The last reading of the open rows

- Read every row of `docs/proofs/cards-inventory-open.tsv`, one by one. CR-511 judged 267 of
  them from their wording alone, and this reading does not repeat that. For each row, read:
  - its line in `## Rows` of `docs/proofs/cards-inventory.md` (behaviour, trigger, source);
  - when the behaviour text is cut or unclear, its source line at the inventory's base,
    `git show f08cf41f2c80e2e4f7ab834adc3dc06820ae7f93:<path>`.
- The question for each row: does it state a rule that protects the user or the repository, and
  does no floor line, role card, topic page, CLI refusal or hook refusal hold that rule at the
  head today? Search the head for the rule's meaning, not only for its old wording.
- Restore each rule that passes the question in exactly one place, and add no new page:
  - the place is the floor (`skills/chantier/references/floor.md`), one line of a role card under
    `skills/chantier/references/`, or an existing page;
  - section 2's test 3 of the plan prefers the floor or a role card for a protective rule ("never
    in a guide alone");
  - never pick a page whose verdict in `fable-review-verdicts.md` is a delete verdict. The
    stack's next CRs delete those pages, and the rule would go with them.
- Each restored line is new text in the cards' plain style. No other card text is reworded.
- The PR body, under Deliverables, gives:
  - how many rows were read (the recount at the base);
  - how many were judged protective;
  - one line for each row judged protective: the row id, the rule in a few words, and where it
    lives now. That is either an existing home quoted with a short span (file, or command and
    refusal text), or "restored: <file>" for a line this CR adds.
- A row judged not protective needs no line of its own. The count covers it.

### 2. The list of protective rules

- Add one short file, `docs/protective-rules.md`. The later cleanup CRs cite it, each saying
  where every protective line of a page it deletes lives (card-cleanup-Q1).
- Content:
  - the rules of plan section 5's table;
  - the statements of verdicts section D, grouped as section 5 groups them;
  - the rules section 1 of this CR finds.
- One line per rule, each with its home and its state, which is one of:
  - `held`: by a floor line (its number), a card (file and a quoted span), a refusal (command and
    a span of its message) or a hook;
  - `restored here`: by this CR;
  - `to add`: a refusal or rule the plan proposes and no code holds yet. The line names the plan
    step that brings it.
- Every home is checked against the base, not copied from the plan. Each "exists?" and "not
  verified" claim of section D is settled by reading the code or by running the command:
  - a claim that holds becomes `held`;
  - a claim that does not hold becomes `to add`;
  - neither is assumed.
- The list follows the owner's answers where they differ from the plan's table:
  - the allow rules (card-cleanup-Q3): the user writes them, from a command the CLI builds for the
    running system and host; the CLI checks that they are in place; no agent writes the settings;
    each host has its own case;
  - a refused push or rebase (card-cleanup-Q2): the CLI checks the branch and prints the exact
    command, and the agent runs it.
  The plan's "a CLI write that can only add" and "the steering push and rebase as rails" are not
  carried over as written.
- The file names no file this CR removes. It speaks of "the old cards' inventory, removed by this
  change", so the check in Evidence finds no reference.
- The file is not a card. It sits outside `skills/`, so no brief, `help` topic or role loads it,
  and no test guards it (plan section 7 keeps the structural tests for its step 7).

### 3. The inventory and its tests are removed

- Delete:
  - `docs/proofs/cards-inventory.md`;
  - `docs/proofs/cards-inventory-open.tsv`;
  - `skills/chantier/scripts/cli/tests/test_cards_inventory.py`;
  - `skills/chantier/scripts/cli/tests/cards_inventory.py`.
- `skills/chantier/scripts/cli/tests/test_card_homes.py`:
  - drop every pin that only says where a removed card's sentence lives: the `HOMES` table with
    its topics, cards, skills and host rows, and the test parametrized on it;
  - keep the assertion that the floor's lines stand word for word in
    `skills/chantier/references/floor.md`, read at the head under test (today the `FLOOR`
    dictionary, lines 1, 3 to 7, 9 and 10). The Driver may move it next to
    `test_the_floor_is_short_lf_only_and_holds_the_ten_rules` in `test_brief.py`;
  - when section 1 or 2 changes a floor line, update the pinned text with it;
  - keep the floor within `FLOOR_BYTES` (1,200);
  - the docstring stops citing the family inventories.

### 4. The eval kit runs without the inventory

No shipped quiz case under `evals/quiz/` names an inventory row id (all 80 cases checked at
4d12a5b: their `rules` are floor rules and `J` rows). The quiz therefore loses nothing it uses.

- `evals/kit/quiz.py`:
  - remove `INVENTORY` and `inventory_rows()`;
  - `load_cases` takes as rails the `J` rows of `evals/SCORECARD.md` only, beside `floor-1` to
    `floor-10` and `R-nnn`;
  - the refusal message in `read_case` and the docstring of `load_cases` stop naming the
    inventory.
- `evals/kit/dry_run.py`: the case `quiz-row-id` is replaced by `quiz-rule-id`, updated in the
  header table, the case list and the dispatch table. In it:
  - a case whose `rules` name a `J` row of `SCORECARD.md` loads;
  - a case naming `X-9999` is still refused with exit 2;
  - the refusal names the file and the key.
- `evals/README.md`, "Cases": the list of accepted `rules` drops the inventory row id.

## Decisions carried (02-answers.md)

1. The owner's « ouvre un batch et lance ces 7 CR » counts as "grilled enough" for the seven
   cleanup CRs. Their scope is the plan and the five answers of
   `card-inventory-open-rows/02-answers.md` (the Chief of Staff's reading, to be confirmed by the
   owner).
2. The batch is a stack (« fait un batch stack »).
3. card-cleanup-Q4, answer A: an agent reads the open rows for missing protective rules, and then
   the inventory and its tests are removed. The replacement is the list of protective rules and a
   real batch on a test project. Sections 1 to 3 do this. The real batch is not part of this CR.
4. card-cleanup-Q5, answer A: first the inventory's last reading, then steps 1 to 3, with a new
   version, in small CRs; steps 4 to 7 wait. The other project with an open batch reads the cards
   live, so the moment has to fit with it. This CR's restored lines change cards that project
   reads live, so it lands in the stack as the batch plans it.
5. card-cleanup-Q1 (each protective rule placed before a page is deleted) is why the list exists
   and why section 1 never restores into a page with a delete verdict.
6. card-cleanup-Q2 and Q3 give the wording of the list's push, rebase and allow-rule rows
   (section 2).

## Out of scope

- Deleting topic pages, the aggregate names, joining `-pN` pages (the stack's next CRs).
- Rewording cards beyond the restored lines.
- Any new CLI refusal, hook or command, including the `to add` rows of the list: they stay listed
  for plan steps 4 and 5.
- Changes to `AGENTS.md`.
- The version bump. Q5 asks for one after step 3, not in this CR.
- The real batch on a test project.
- Running `just quiz` with a model: it costs money, and no case changes.

## Evidence

- The PR's Deliverables hold the count of rows read and the per-row lines of section 1. Its diff
  holds `docs/protective-rules.md`, with every line marked `held`, `restored here` or `to add`, and
  every `held` home quoting a span found at the head.
- `git grep -nE "cards-inventory|cards_inventory|inventory_rows|quiz-row-id"` at the PR's head
  prints nothing.
- `just check` passes.
- `just eval-dry-run` passes, since `evals/kit/` changes. Its `quiz-cases` and `quiz-rule-id`
  cases load the shipped cases and refuse `X-9999`.
- When a card or the floor changes (a restored line), the change owes what `AGENTS.md` asks of a
  cards change: the pipeline's `just scenario (ubuntu-latest)` job green at the PR's head. In
  this stack batch, the local Windows run is owed only by the CR on top. If a brief's byte ceiling
  in `test_brief_bytes.py` has to rise, the PR's Known gaps name it, with the before and after.

## Questions for the Chief of Staff

1. Section 2's check may find a rule of the plan's table or of section D that nothing holds today
   and that one card or floor line could hold (not a code refusal). Should this CR restore it, as
   section 1 does for the open rows? Or should the list mark it `to add`, for the CR that owns its
   family? The specification asks only for the marking.
2. The floor pin in `test_card_homes.py` covers eight of the ten floor lines today (not 2 and 8).
   Should the kept check pin all ten?
3. Two backlog specifications build on the inventory: `2-backlog/P1/512-sc26-card-gates-pytest`
   (its `rows` field and a check that each id exists in `docs/proofs/cards-inventory.md`) and
   `514-sc28-cards-real-run` (its owner lists). Once this CR lands, they no longer hold. Should
   they be marked superseded by the cleanup plan, or reworked? This CR does not touch them.
