# SC25: Read the old cards against the new; nothing important lost

Child 25 of 28 of the program `simplify-cards-and-prompts`
(`1-inbox/simplify-cards-and-prompts/03-change-spec.md`, "Child 25"). One Driver, one stack PR.

## Goal

Children 19 to 23 rewrote every role's card and child 24 swapped them in. Child 25 reads the
whole old card set and puts every rule it holds in one table. Each rule gets the place where it
now lives, or a removal the owner can see, plus a check. Child 25 restores whatever was lost and
commits the table as `docs/proofs/cards-inventory.md`. A test keeps that table true at every later
head. The owner should be able to open one file and see that nothing that protects the user or the
repository was dropped.

## Place in the chain

- **Base.** This CR is a stack PR on child 24's branch (`cards-swap`). Child 24's PR is its base,
  and the CR on top of it is child 26 (`[R-nnn]` ids and `rules.json`). Child 26's rule ids take
  this inventory's rows (program, child 26), so the row ids defined here must stay stable.
- **Merge.** Children 19 to 28 merge as one unit after child 28's campaign. Record the merge wait
  with `$CHANTIER wait <this CR> merge <child 28's PR>`. If child 28 has no PR yet, record the
  wait on child 28's CR with `--note "child 25 waits for this PR"` and name it in Known gaps. The
  Known gaps also carry "real run not done (child 28)". Nothing merges tonight.
- **The old cards.** These are the cards at child 19's base, meaning the parent of the first
  commit on the stack that touches `skills/chantier/cards-next/`. Children 19 to 23 write only
  under `cards-next/`, so child 24's parent holds the same old set. The Driver proves this with
  the command below, which must print nothing, and quotes it in the PR:

  ```
  git diff --stat <child19-base> <child24-parent> -- skills/chantier/references 'skills/*/SKILL.md'
  ```

  If it prints anything, the old set is the one at `<child24-parent>`. Name the difference in the
  PR's Deliverables.
- **The new cards.** These are the files at this CR's head, after child 24's swap.

## Decisions carried (none invented)

- **Program, child 25.** These are the inventory's columns, the list of homes, restoring before
  committing, grouped quiz cases for inferable rows, and topics with `review_by` for rare rules.
  Both Known gaps lists come from here too: every kind-a row with its home, and every row homed as
  inferable or in the incidents file.
- **Program F5.** A kind-a row's home is only the floor, the role's card or a refusal. It is never
  a topic alone and never "inferable", and no kind-a row is dropped.
- **Program F4.** On the quiz, no case may score 0/3 on the new cards if the old cards scored at
  least 1/3 on it.
- **Program answer 10.** A rare rule with no CLI trigger becomes a topic whose `review_by` is the
  next minor version: `"0.16.0"` on a 0.15.x base, otherwise the minor after the base's
  `pyproject.toml` version.
- **Program budgets.** Size targets: Chief of Staff 6 KB; Griller, Foreman, CR driver and stack
  driver 4; release driver 3; Verifier 3; QA driver 2; Inspector 2; other workers 1.5; board
  Griller 2; floor 1.2; a topic 1.5. Here 1 KB means 1,000 bytes with LF line endings. A
  restoration may add a card line only inside that card's budget. Otherwise it goes in a topic, a
  refusal or a `next:` line, or the PR's Known gaps name the overrun (program, child 25, "Must
  not").
- **Program M4 and M13.** A row's check is a pytest node, a scenario step, a rail or a quiz case,
  and a kind-a row's check is never "inferred". A test string literal is at most 40 characters.
- **Program cost.** Quiz models are paid outside the batch's `cost`, and the cap is printed before
  any spend. The batch budget is $400. Child 25's quiz runs each pass `--max-usd 10`.
- **sc19's format** (`4-batch/1-pending/505-sc19-cards-workers/03-change-spec.md`). This CR keeps
  the per-family inventories in `evidence/cards-inventory-<family>.md`, their id prefixes, their
  home words and the "child 25" check placeholder. It merges them; it does not rewrite them.
- **Owner answer, 2026-11-25** (`02-answers.md` Q1). The program's specification is the grill.
  There is no separate critic. Destination is batch-31.

## What changes

### 1. `docs/proofs/cards-inventory.md` (new, committed)

The file holds five parts, in this order. The test reads every part, so the Driver keeps the
headings exactly as written here.

**`## Base`**: one line, `base: <40-hex SHA of child 19's base>`. Then the method, in at most ten
lines: what was read, how lines were counted (each source's lines as `git show <base>:<path>`
prints them, with LF endings), and that ids are never reused.

**`## Sources`**: a table with columns `path | lines | lf_bytes | blob`, one row per old source
file at the base:

- every file under `skills/chantier/references/` (the `.md` files, the two `forges/`, the two
  `hosts/` and `startup-manifest.json`);
- the four `skills/*/SKILL.md`.

The agent wrappers (`agents/`, `com.github.copilot/agents/`) are left out, with that reason
written in the method lines: they are not removed, and `just roles` checks them. The Driver fills
the table from the base with these two commands and quotes both in the PR:

```
git ls-tree -r <base> -- skills/chantier/references 'skills/*/SKILL.md'
git show <base>:<path> | wc -l -c
```

On Windows, use Git Bash and `MSYS_NO_PATHCONV=1`.

**`## Rows`**: a table with exactly these columns:

`id | role | trigger | behaviour | source | kind | home | check`

- `id` matches `^[A-Z]{1,2}-\d{3}$` and is unique. The family prefixes are kept as the family
  inventories gave them: `W`, `D`, `FM`, `C`, `G`. Child 23's rows take `S` unless child 23's
  spec gives another prefix, which then wins. Rows this review adds take `X`. A family row's id
  stays the same when it is merged.
- `role` is the role the rule binds, or `all`.
- `trigger` is the situation or command that brings the rule into play. Use `none (rare)` for a
  rule with no CLI trigger.
- `behaviour` is one sentence in the agent's terms.
- `source` is `<path>:<line>` or `<path>:<first>-<last>`, a path listed in Sources at the base. A
  rule repeated in several cards gets one row per place, kind `f`, all with the same home.
- `kind` is one letter `a` to `f`, as in study-fable section 3:
  - a: protects the user or the repository;
  - b: inferable;
  - c: incident or retro patch;
  - d: host trial bookkeeping;
  - e: state or procedure the CLI could print;
  - f: duplicated or contradictory.
- `home` is one form of the home grammar below.
- `check` is one form of the check grammar below.

**`## No-rule lines`**: a table `source | reason`. It lists the line ranges of the old sources
that hold no rule. Each reason is one word from: `heading`, `blank`, `example`, `table-header`,
`code`, `link`, `transition`, `front-matter`. Together, Rows and No-rule lines cover every line
1..N of every Sources file. Ranges may overlap, and a line may sit both in a row and in a no-rule
range.

**`## For the owner`**: four lists, each item naming row ids.

1. Every kind-a row, with its home and check.
2. Every row homed `inferable` or `incidents`.
3. Every row homed `removed:`, which is "changed on purpose", with the decision it cites.
4. Every kind-a row whose check is `quote` only. These rows have no behaviour check yet, and the
   list is left for child 26.

**`## Hand-over checklist`**: one line per item of the checklist below. Each line starts with the
item id and ends with `done: <where>` or `known gap: <why>`.

#### Home grammar (each home must resolve at this CR's head)

| form | resolves when |
|---|---|
| `card <file>: "<span>"` | `skills/chantier/references/<file>` exists and contains `<span>`. A span is at most 40 characters and matches with whitespace collapsed. |
| `floor <n>` | `references/floor.md` has a numbered item `n`. |
| `refusal <command or hook>: "<span>"` | the span is in some `skills/chantier/scripts/cli/src/**/*.py` or in `hooks/register.tsx`. |
| `next <command>: "<span>"` | the span is in `src/**/*.py`. |
| `--help <command>: "<span>"` | the span is in `src/**/*.py`. |
| `facts: "<span>"` | the span is in `src/**/*.py` (child 10's `brief` facts). |
| `topic <name>` | `load_topics(references/topics.json)` has `<name>`. |
| `host row <id>` | `host_rows.load_rows()` has `<id>` (child 8). |
| `proof file <path>` | `<path>` exists under `docs/proofs/`. |
| `incidents: "<span>"` | the span is in `docs/incidents.md` (child 24). |
| `inferable` | the row is not kind a, and its id appears in the `rules` of a quiz case under `evals/quiz/`. |
| `removed: <decision> - <reason>` | the row is not kind a, and `<decision>` cites a recorded decision id: a program answer (`answer 8`), a child's question (`sc21-Q1`) or a child's item (`sc21 B6`). |

The family inventories write `refusal`, `next: line` and `facts` without a span. When merging,
the Driver adds the span, read from the code at the head.

#### Check grammar

| form | resolves when |
|---|---|
| `test <path>::<name>` | the test file exists under `skills/chantier/scripts/cli/tests/` and defines `<name>`. |
| `scenario <unit>` | `<unit>` is a unit name in `scenario/run_scenario.py`, read the way `test_scenario_coverage.py` reads them. |
| `rail <id>` | `evals/SCORECARD.md` has a row with that id. |
| `quiz <role>/<id>` | `evals/quiz/<role>/<id>.json` exists, and its `rules` list the row's id. |
| `quote` | the home's span resolves; the home itself is the check. A kind-a row may use it, but it is then listed in owner list 4. |

The family placeholder `child 25` is not a valid check at this head: every one is replaced.

### 2. Building the rows

- **Seeds**, all read at the base, merged into one table. Only lines that no seed covers are read
  from scratch:
  - the five family inventories: workers (sc19), drivers (sc20), foreman (sc21), chief and
    griller (sc22), host and shared (sc23), each in `evidence/` of its CR folder;
  - CR-471's `4-batch/3-done/471-slim-the-startup-cards-of-the-three-role/work/tables.md`;
  - `tests/moved_rules.tsv`;
  - `evals/SCORECARD.md`'s rails.
- **Sources no family claims.** sc19 left `review-step.md`, `concepts.md`, the templates
  (`pr-template.md`, `release-template.md`, `ticket-summary-example.md`), `startup-core.md` and
  `role-core.md` to child 23 or child 25. sc22 rows `sync-checkout.md` and `status-layout.md` only
  if no other child claims them. Whatever the Sources table lists that no family inventory covers
  is rowed here with `X` ids. The coverage test finds any gap.
- **The floor.** Each of the ten floor rules gets a row at each old place it came from. Every such
  row is kind a, homed `floor <n>`.

### 3. Restoring

A row with no home at the head is restored before the commit. Restoring is in this order:

1. a refusal that names the next command (child 3's form);
2. a `next:` line;
3. a topic in `references/topics.json` (child 7's format) plus its reading file;
4. a card line, only inside the card's budget.

A rare rule (trigger `none (rare)`) goes into a topic with `review_by` set (answer 10), or into
the incidents file if it is a story. A kind-a row is never restored into a topic alone (F5). A
restored rule is a real change to the cards or the CLI. It is listed in the PR's Deliverables, one
line per row id.

### 4. Quiz

- **Inventory row ids as rules.** Child 6's quiz loader (`evals/kit/quiz.py`, which child 6
  adds) accepts `floor-<n>` and `J<n>` in a case's `rules`. Child 25 extends that check so it
  also accepts an id that is a row of `docs/proofs/cards-inventory.md`. An unknown id still exits
  2. One `evals/kit/dry_run.py` case, `quiz-row-id`, checks both: a known row id loads and an
  unknown one exits 2. This is why `just eval-dry-run` is owed.
- **Grouped cases.** The inferable rows are grouped by role and situation into cases
  `evals/quiz/<role>/inf-<n>.json`, with several row ids in `rules`. No case holds a kind-a row.
- **Cases left to child 25.** sc20 left "rows it finds uncovered". sc21 left eight candidates (see
  the checklist). sc22 left cases that had no accepted id. Each becomes a case whose `rules` name
  its row ids, or a Known gap naming why not.
- **Runs.** First `just quiz <role> --plan --max-usd 10`, which prints the cap. Then, for each
  role that has new cases:

  ```
  just quiz <role> --cards <child19-base> --max-usd 10 --save old-<role>
  just quiz <role> --max-usd 10 --against <the saved old results>
  ```

  Session roles (chief-of-staff, foreman, griller) add `--model`. The second run exits 0, which
  means F4 holds. Both result files are quoted in the PR.
- **No headless CLI.** If the Driver cannot start a headless host CLI, it hands back with the
  exact commands, and the Chief of Staff runs them. This is not a gap the Driver works around.

### 5. `evals/SCORECARD.md`

Reconcile rails J11 (the refused force-push ladder) and J22 (the steering session never codes,
commits, pushes, rebases or creates a worktree, with its exceptions) with the new cards' wording
(sc22's hand-over). Ids stay the same and the "from" column is not rewritten. If a rail's
behaviour changed rather than its wording, add a row and keep the old one with the change
recorded, following the file's own rule ("never reused, never renumbered"). Also check the
duplicate J29 row as part of this review. If both rows are distinct rails, name the duplicate in
Known gaps; never renumber.

### 6. `skills/chantier/scripts/cli/tests/test_cards_inventory.py` (new)

The test reads the shipped `docs/proofs/cards-inventory.md` at the head under test, through
`conftest.PLUGIN_ROOT`, and checks:

- `test_schema`: the five headings exist; ids are unique and match the regex; kind is `a`-`f`;
  no cell is empty; `base:` is 40 hex characters.
- `test_homes_resolve`: every home resolves under the grammar above.
- `test_kind_a_homes`: no kind-a row is homed `topic`, `inferable`, `removed:`, `incidents`,
  `proof file`, `host row`, `--help` or `facts`. Only `floor`, `card` and `refusal` pass (F5).
- `test_checks_resolve`: every check resolves under the grammar above, and none is `child 25`.
- `test_rare_rules`: a `none (rare)` row is homed in a topic that has `review_by`, or in
  `incidents`.
- `test_coverage`: for each Sources row, the union of Rows and No-rule lines ranges covers
  1..`lines`, and no range points past `lines` or at a path not in Sources.
- `test_owner_lists`: list 1 names every kind-a row, list 2 every `inferable` and `incidents`
  row, list 3 every `removed:` row, and list 4 every kind-a `quote` row.
- `test_checklist_closed`: every checklist line ends in `done:` or `known gap:`.
- `test_refusals` (parametrized): prepared inventory texts, built in the test from short pieces
  (M13), each break one rule above and must be refused. Cases: a duplicate id; a kind-a row homed
  as a topic; a kind-a row homed `inferable`; a home naming a missing topic; a check naming a
  missing test; an uncovered line. Prepared texts are used only for these refusal cases. The
  checks above all read the shipped file.

The parser is a small function inside the test file, with no new module under `src/`. It reads
Markdown tables by splitting on `|`.

The test cannot prove the Sources table against the base commit, because CI checks out at depth
1. That proof is the Driver's commands quoted in the PR (section 1). The test proves the table is
complete and consistent at every head.

### 7. Files touched

- New: `docs/proofs/cards-inventory.md`, `skills/chantier/scripts/cli/tests/test_cards_inventory.py`,
  `evals/quiz/<role>/inf-<n>.json` and the other new cases.
- Edited:
  - `evals/kit/quiz.py` (row ids);
  - `evals/kit/dry_run.py` (one case);
  - `evals/SCORECARD.md` (J11, J22);
  - whatever restorations touch (`references/topics.json` and topic files, cards within budget,
    `src/` refusals and `next:` lines).
- The planning folder: the per-family inventories stay where they are, unedited.

## Hand-over checklist (every note addressed to child 25)

Each item gets one line in the inventory's `## Hand-over checklist`, closed `done:` or
`known gap:`.

| id | from | item |
|---|---|---|
| P1 | program, answer 10 | Rare rules with no CLI trigger are topics with `review_by` the next minor. |
| P2 | program, pending `1-inbox/driver-card-leads-left-by-role-cards-sti` | Check child 20's three leads, which are item sc20-L. |
| P3 | program, F5 | No kind-a row in a topic alone or inferable; none dropped. |
| P4 | program, child 25 | Inferable rows are grouped into quiz cases that pass F4. |
| P5 | program, close-behind | The Foreman's chat obeys only stop and hold (Foreman card). Tracker approval is in the Chief of Staff's card. The untested host path is in the host rows. Each has a row with that home. |
| P6 | program, child 10 | Each of the ten floor rules has a row at every old place it came from. |
| sc03 | `489-…` | Rows homed as refusals cite the refusal's message start. |
| sc06 | `492-…` | Grouped cases for inferable rows; quiz `rules` accept row ids (section 4). |
| sc07 | `493-…` | Topic homes, with `review_by` set for rare rules. |
| sc08 | `494-…` | A rule left out of the host-row means stays in its card until child 23. Check that it now has a home. |
| sc09-Q2 | `495-…` | `CONTRIBUTING.md:100` ("The CLI knows no role…") is aligned with the new cards, in child 24 or here. Check only, as recorded in sc09. If child 24 did not align it, align it here with the wording sc09 recorded; do not re-ask. |
| sc13 | `499-…` | The old "a Driver tells its steering session" rules are found again through `msg` and `inbox`. |
| sc15 | `501-…` | Each rule of `foreman-conflict.md` is found again in `conflicts`, its output or its refusals. |
| sc19-S | sc19 | Row the sources sc19 left out (section 2). |
| sc20-U | sc20 | Write cases for rows found uncovered. |
| sc20-Q2 | sc20 | A new worktree per release attempt replaces `git reset --hard`. Row it `removed: sc20-Q2` for the old rule and give the new rule its home. |
| sc20-L | sc20, section 4 | Three leads: the typed `pipeline` wait in `release-driver.md`; read a guideline by section; wait only in a background shell, in `cr-driver.md`, `stack-driver.md` and topic `ci`, with "Monitor from a subagent is unproved". |
| sc21-B1b | sc21 | The icon rule is gone: `removed: sc21 B1b`. |
| sc21-B1e | sc21 | If `judge` does not carry the image-replaced note, that is a Known gap. |
| sc21-B6 | sc21 | The third chat case (the user's line allowing a refused action) is dropped: `removed: answer 8`. |
| sc21-Q1 | sc21 | The worktree override is dropped: `removed: sc21-Q1`. |
| sc21-C | sc21 | Quiz-case candidates: chat obeys only stop/hold; a note does not wake; judge then send, no merge; the `--no-gate` check; no release merged without the grant; a refused push of a non-`chantier/*` branch; a session in a worktree; `next` against a refusal. |
| sc22-B | sc22 | Its rows whose behaviour changes on purpose, answer 8 items 3 and 4 included, go into owner list 3. |
| sc22-J | sc22 | Reconcile J11 and J22 (section 5). |
| sc22-C | sc22 | Cases left out for lack of an accepted id: write them now that row ids are accepted. |
| sc22-S | sc22 | `sync-checkout.md` and `status-layout.md` each have rows, from sc22 or here. |
| sc22-D | sc22 | "The floor" for delivery time is topic `delivery-time`. Its rows point there, not at `floor.md`. |
| sc23 | child 23's spec at the base | Every note to child 25 in `03-change-spec.md` of `sc23-cards-host-and-shared`, one line each. |
| sc24 | child 24's spec at the base | Every note to child 25 in `03-change-spec.md` of `sc24-cards-swap`, one line each. The stories moved to `docs/incidents.md` give `incidents:` homes. |

Child 23 and child 24 were being specified when this spec was written. The Driver reads their
specs at its base and adds their notes as lines `sc23-<n>` and `sc24-<n>`.

## Out of scope

- Rule ids `[R-nnn]` and `rules.json` belong to child 26. This CR only keeps row ids stable for
  it.
- Behaviour checks for the kind-a rows in owner list 4 are left for child 26.
- Child 28's real-run campaign and the stack's merge.
- Rewriting a card beyond restoring rows, re-arguing a family's decisions, and changing a budget.
- The agent wrappers, which `just roles` checks.
- A new CLI command, and a new script under `scripts/`.
- The board Griller's budget (sc19-Q1) and sc22-Q1 and sc22-Q2, which belong to their children.

## Acceptance evidence (in the PR)

1. `git diff --stat <child19-base> <child24-parent> -- …` prints nothing, or the difference is
   named.
2. The `git ls-tree` and `wc -l -c` output that the Sources table copies.
3. `test_cards_inventory.py` passes on the shipped file, and each refusal case fails as expected.
4. Every row has a home and a check that resolve. No kind-a row is in a topic, inferable or
   removed. The four owner lists, plus Known gaps that repeat lists 1 and 2 (program).
5. Restorations, one line per row id and file. Each card's size against its budget, as LF bytes
   at the head. Any overrun named in Known gaps.
6. The quiz `--plan` output with the cap, both runs' result files, and the exit 0 of
   `--against` (F4). Or the hand-back to the Chief of Staff with the exact commands.
7. `just check` at the pushed head, and `just eval-dry-run` (`evals/kit/` changes).
8. The long gate `just scenario (ubuntu-latest)` green at the PR's head if any topic, refusal,
   `next:` line or card line is added. The local Windows `chantier gate <cr> scenario` is owed
   only while this CR is the stack's top.
9. The merge wait recorded, and the Known gap "real run not done (child 28)".
10. The seconds `test_cards_inventory.py` adds to `just test`, measured on the Driver's machine
    as two runs of `just test` before and after, with both times quoted. The expected cost is
    about 1 to 1.5 s. A cost above 3 s is a Known gap.

## `just test` seconds

About 1 to 1.5 s expected: one parse of the inventory, one scan of `src/**/*.py` for spans (read
once and cached in the module), and six small refusal cases. The measured figure goes in the PR
(evidence 10).

## Handback

The Driver's ready line names:

- the PR;
- the row count by kind;
- the number of restorations;
- the owner lists' sizes;
- the quiz result (F4 held, or handed back for the Chief of Staff to run);
- the measured seconds;
- the Known gaps.

## Risk

- **Size.** The inventory may run to thousands of rows and hundreds of KB. It is a proof file
  that no agent loads, so it costs repository size, not tokens. See Q3.
- **Gates.** Restorations change the cards or the CLI, so the long gate is owed. A `src/` change
  also owes `just eval-dry-run`, which `evals/kit/` already owes.
- **Brittle spans.** A later edit of a card or message breaks a `card` or `refusal` span. That
  is intended: the test then names the row whose home moved.
- **Quiz spend.** Capped at $10 per run and printed first, outside the batch's `cost`.

## AGENTS.md

None. `docs/proofs/` is a docs folder, and the test and quiz changes follow the existing rules.

## Open questions

- **sc25-Q1 (risk).** Until child 26 adds behaviour checks, may a kind-a row be checked by
  `quote` alone, meaning the test proves only that the rule's text is still in its card, floor or
  refusal? Default: yes, with every such row in owner list 4 and in Known gaps for child 26.
- **sc25-Q2 (scope).** If the review finds an old rule that is gone with no recorded decision,
  and it is not kind a, may the Driver home it `removed:` on its own judgement? Default: no. It
  restores the rule (section 3) and lists it. Only a row with a recorded decision id may be
  `removed:`.
- **sc25-Q3 (risk).** If the inventory exceeds 500 KB, should it still be one committed file?
  Default: yes, one file, its size named in the PR.
