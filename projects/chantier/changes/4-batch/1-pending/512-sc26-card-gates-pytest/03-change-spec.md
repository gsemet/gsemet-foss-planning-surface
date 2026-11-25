# SC26: Budgets, history lint and rule ids as pytest gates

Child 26 of 28 of the program `simplify-cards-and-prompts`. These rank above this specification:
the program's `03-change-spec.md` ("Child 26"), its `02-answers.md` answers 17 to 22, and its
`work/study-*.md`. Code and cards are named as at `origin/main` 8a960d34, with the changes the
earlier children's specifications make (children 1 to 25, in `changes/4-batch/1-pending/`).

## Goal

The rewritten cards stay small and clean. They do not slowly grow back. This happens without
anyone re-reading them. Pytest refuses five things:

- a card or a role's reading path that grows above its frozen size;
- a date, an incident or a trial story in a card;
- a rule sentence with no id, or an id with no row;
- a rule whose check does not exist;
- a test that pins a long card phrase instead of a rule id.

The rule ids become the one link between a card sentence and the inventory (child 25). They also
link it to the behaviour detectors (child 5), the quiz cases (child 6) and the checks that prove
it.

## Place in the chain

- **Stack.** batch-31 is one stack batch. This CR is a stack PR on child 25's branch
  (`cards-compare-review`). Child 27 (`card-gates-process`) stacks on it. Child 27's CI reminder
  triggers on `references/floor.md` and `references/budgets.json`, so this CR must create
  `budgets.json` at exactly that path. Child 28 (`cards-real-run`) is the top of the stack.
- **Merge.** Children 19 to 28 merge as one unit, in order, in one sitting, after child 28's
  campaign. The Driver records `$CHANTIER wait <this CR> merge <child 28's PR>`. If child 28 has
  no PR yet, it records the wait on child 28's CR with `--note "child 26 waits for this PR"` and
  names that in Known gaps. Nothing merges while the owner sleeps.
- **What this CR changes for later children.**
  - Child 27 reads `budgets.json` and `floor.md` paths only.
  - Child 28 confirms each limit at what the run read, or asks a raise with the owner's line
    (M11). This CR raises no limit by itself.

## Decisions carried (none invented)

| Source | Decision | Where |
|---|---|---|
| Answer 9 (M1, M2, M3, M4, M8, M12, M13); F2 | The scope below; hard gates in pytest | Sections 2 to 8 |
| Q4 | The gates child freezes what the rewrite reached. A card above its target keeps its reached size as its limit and goes in Known gaps | Section 2 |
| Program, child 26, "Must not" | No limit above child 24's reached size; no exemption for a floor rule | Sections 2, 4 and 7 |
| F5 | An inventory kind-a row is never `inferred` | Section 5 |
| F11, answer 22 | A typed merge wait on child 28; Known gap "real run not done (child 28)" | Handback |
| F17 | A claim this program has not proved is marked "unproved" in this spec and in the PR, never in a card | Section 4 |
| Program, "Text style" | No date, batch name or trial story in a card; enforced from this child | Section 4 |
| Program, rules for every child | A check guarding a shipped file reads it from the repository at the head under test. A prepared text is used only for a refusal case, paired with the check on the shipped file | Every test |
| sc25's check grammar | `test <path>::<name>`, `scenario <unit>`, `rail <id>`, `quiz <role>/<id>`, resolved the same way | Section 5 |
| sc05 | Detector fields: tools, roles, pattern, positive, negative. Results compare by detector name with the previous file | Section 6 |

## Hand-over checklist (every note the siblings address to child 26)

The PR copies this table. Each line ends `done: <where>` or `known gap: <why>`.

| Id | From | Owed by this CR |
|---|---|---|
| H1 | Program, Q4; sc23-Q1 | Freeze `budgets.json` at the sizes reached. This includes the six shared files that have no target: `concepts.md`, `pr-template.md`, `release-template.md`, `status-layout.md`, `routing.md`, `init.md`. Q4 answers sc23-Q1: freeze at the reached size |
| H2 | sc24, `tests/test_brief_bytes.py` | Its `BRIEF_BYTES` table becomes the `paths` section of `budgets.json` (M2), on both hosts |
| H3 | sc24, file-and-heading pins | Turn every converted card pin into an id pin, gathered in `tests/test_card_ids.py` (M13) |
| H4 | sc19, sc20, sc21, sc22, sc23 (draft ids W/D/FM/C/G/S), sc25 (X) | The inventory's rows take R ids. Each `rules.json` row lists the inventory row ids it carries |
| H5 | sc25, owner list 4 | Give every kind-a row whose check is `quote` a behaviour check (Q3) |
| H6 | sc25-Q1 | Its default (a `quote` check for kind a, in Known gaps) stops at this CR. No kind-a rule's only check may be its own id pin |
| H7 | sc05 | Move `evals/kit/detectors.json` into `rules.json` (`detector`). Repoint `evals/kit/behaviour.py`, its `--prune`, and dry-run check 4. Move check 4 (positive and negative examples) into pytest |
| H8 | sc06 | The quiz cases' `rules` take R ids in place of `floor-<n>`. `load_cases` and the dry run accept `R-nnn` present in `rules.json` |
| H9 | sc07 | Every `` `help <name>` `` in a card names a topic of `topics.json`. No file under `references/topics/` is orphaned |
| H10 | sc24, links | Make the link check permanent: recursive under `references/` and `docs/`, with anchors |
| H11 | sc08 | M3 covers `.md` files only. The host rows' JSON stays under `test_means_carry_no_history` |
| H12 | sc03 | Its M9 allow-list holds fragments of 40 characters or fewer and passes M13 unchanged (`MAX_ALLOWED = 7`) |
| H13 | sc18 | `roles.yaml` gives each role's card and owner. This CR adds no `roles lint` |
| H14 | sc21, sc23 | The "unproved" marks in topics (GitLab forms, host allow rules, Copilot claims) are M3 hits. They become "untested" |
| H15 | sc23 | Topics with `review_by` are budgeted like any topic (1.5 KB target) |
| H16 | Program, child 27 | The paths `references/floor.md` and `references/budgets.json` are fixed |
| H17 | Program, child 28 | Limits are frozen and not raised here. Child 28 confirms them or asks a raise |

## What changes, by file

Paths are relative to the repository root. `tests/` means `skills/chantier/scripts/cli/tests/`.
`references/` means `skills/chantier/references/`. A KB is 1,000 bytes with LF line endings.

### 1. Rule ids in the cards

- **The tag.** `[R-nnn]` is three digits, zero-padded. It goes after the sentence's final
  punctuation, separated by one space: `Never merge without the user's word. [R-001]`.
- **Numbering.**
  - The floor comes first: floor rule n is `R-00n` for n from 1 to 10 (`R-010` is rule 10).
  - Then the role cards, in `skills/chantier/roles.yaml` order.
  - Then any id placed in a topic or a shared file.
  - Ids are never reused (M12).
- **Which sentences must carry an id.** In every file that is a `card` of `roles.yaml`, and in
  `floor.md`, every prose sentence holding the word `never`, `must`, `only` or `always`. The match
  is case-insensitive and on whole words. These are not prose and are skipped:
  - fenced code blocks and inline code spans;
  - headings;
  - table header rows;
  - front matter.

  A bullet is one sentence or more. Sentences are split on `. `, `? ` and `! ` and at line ends
  that end a bullet. A rule written without one of the four words may carry an id too.
- **Where ids may appear.** Anywhere under `references/**/*.md`. A topic or shared file may hold
  a rule with an id (its row's `card` is that file), but carrying one there is not required (Q2).
- **One place per id.** An id appears exactly once across `references/**/*.md`. A rule repeated
  in two places keeps one place: the other copy is removed, or it points to the first by name
  without an id.
- **Wording does not change.** The Driver adds tags only. A sentence that holds one of the four
  words but is not a rule ("it only prints") gets reworded with no change of meaning, or gets an
  id with kind `format`. Each rewording is listed in the PR, before and after.

### 2. `references/budgets.json` (new) and `tests/test_card_budgets.py` (new): M1, M2

- **Format.**

  ```json
  {"schema": 1,
   "files": {"cr-driver.md": {"limit": 4000, "owner": "cr-driver", "target": 4000}, ...},
   "paths": {"cr-driver": {"claude": 9100, "copilot": 9300}, ...},
   "sum_limit": 0}
  ```

  - `files` holds every `*.md` under `references/`, recursive, keyed by its path relative to
    `references/`. `limit` is in LF bytes. `owner` is the `roles.yaml` role whose card it is, or
    `shared`, or `topic`. `target` is the program's target, or `null` for the six shared files
    without one.
  - `paths` holds, per `roles.yaml` role and per host, the measured path's limit (below).
  - `sum_limit` is the sum of the `files` limits at freeze. The test also holds it as a constant,
    `SUM_LIMIT`, so that a raise must touch two places.
- **What counts as a card's bytes.** The file's bytes with CRLF turned into LF and every
  `\s?\[R-\d{3}\]` removed. The ids are bookkeeping, and counting them would push each card above
  child 24's reached size, which the program forbids. This is Q1's default.
- **The freeze.**
  - For each file, the limit is its counted size at child 24's head, rounded up to the next 10
    bytes.
  - A file that child 25 grew above that size is handled by Q1's default: its limit is child 25's
    size, marked `"pending_owner": "<n> bytes above child 24"`. It is listed in Known gaps for the
    owner's line (M11). The test prints every pending row.
  - A file that child 25 created (a topic) gets its size at child 25's head.
  - The Driver's freeze is a throwaway script, quoted in the PR with its output. Columns: file,
    size at child 24's head, at child 25's head, at this head (ids stripped), target, limit, and
    "over target by N" where it applies.
- **The measured path (M2).**
  - For a role and a host, it is the sum of:
    - the output of `chantier brief <role>` on that host (child 10), with the `=== facts` section
      removed, because it holds state and machine paths that differ between Windows and Linux;
    - the counted bytes of each topic the card or the brief names (a `` `help <name>` `` span, or
      a link to `topics/<name>.md`), once each.
  - The limit is the figure at child 24's head, rounded up to the next 100 bytes. This is the
    `BRIEF_BYTES` figure of sc24, re-measured without facts.
  - The Copilot figures are measured the same way from the Copilot host rows. Copilot's real
    reading is untested (unproved, F17).
  - `tests/test_brief_bytes.py` (sc24) is folded into this file: its card-first assertion stays,
    and its table is removed.
- **Tests** (few, parametrized):
  - `test_every_reference_has_a_row`: the `files` keys equal the set of `*.md` under
    `references/`, both ways.
  - `test_file_within_limit[<file>]`: the counted bytes are at or below `limit`.
  - `test_sum_within_limit`: the sum of the limits is at or below `SUM_LIMIT`, and
    `SUM_LIMIT == sum_limit`.
  - `test_limits_frozen`: no limit is above its child 24 figure unless the row carries
    `pending_owner`, and no floor file row carries `pending_owner`. The child 24 figure is a table
    in the test, written once by the Driver.
  - `test_path_within_limit[<role>-<host>]`: 18 roles × 2 hosts, in-process through child 10's
    brief function.
  - `test_budget_refusals` (prepared): a card text over its limit, a `references/` file with no
    row, and a sum over `SUM_LIMIT` are each refused.

### 3. `references/rules.json` (new)

```json
{"schema": 1, "rules": [
  {"id": "R-001", "card": "floor.md", "kind": "floor", "class": "a",
   "rows": ["W-003", "FM-011"],
   "check": ["test tests/test_merge_refusal.py::test_merge_needs_the_user", "quiz foreman/floor-1-foreman-merge"],
   "detector": {"name": "merge-by-agent", "tools": ["Bash", "PowerShell"], "roles": "all",
                "pattern": "...", "positive": ["..."], "negative": ["..."]}},
  {"id": "R-044", "card": "coder.md", "kind": "inferred", "class": "b", "rows": ["W-120"],
   "check": ["quiz coder/inferable-coder-1"]},
  {"id": "R-090", "card": "foreman.md", "kind": "role", "class": "c", "rows": [],
   "check": ["scenario stack-chain"], "retired": "0.16.0, folded into a refusal"}]}
```

- `id`: `R-nnn`, unique.
- `card`: the path, relative to `references/`, of the one file holding the id. A retired row
  keeps its last card.
- `kind`:
  - `floor`: the ten floor lines;
  - `role`: a role's behaviour;
  - `format`: the shape of an output;
  - `inferred`: a rule whose only check is a quiz case.
- `class`: the inventory kind `a` to `f` of its rows (study-fable section 3). A row whose rows
  hold several kinds takes the first in the order a, c, e, d, f, b.
- `rows`: the inventory row ids of `docs/proofs/cards-inventory.md` it carries. These may be
  empty only for a rule added after child 25.
- `check`: a list in sc25's check grammar (no `quote`). It is empty only for a retired row.
- `detector`: optional (section 6).
- `retired`: optional, `<version>, <reason>` (M12).

### 4. `references/lint-allow.txt` (new) and the history lint (M3)

- **Scope.** Every `references/**/*.md`, and the bodies of the 30 wrappers
  (`agents/*.md`, `com.github.copilot/agents/*.agent.md`) after their front matter. The front
  matter holds `model:`, which is configuration and not history. Fenced code is scanned too.
- **Patterns**, case-insensitive:
  - a date `\b\d{4}-\d{2}-\d{2}\b`;
  - a batch name `\bbatch-\d+\b`;
  - a CR id `\bCR-\d+\b`;
  - a PR number `\bPR ?#?\d+\b`;
  - the words `proved`, `unproved`, `trial`, `trials`;
  - the phrase `the user's answer`;
  - a model name `\b(opus|sonnet|haiku|fable)\b`, `\bclaude-[0-9a-z]`, `\bgpt-\d`;
  - a token count `\b\d[\d,.]*\s?k?\s?tokens?\b`.
- **Fixing the hits** at this head, in this order:
  1. A host or forge path that was not tried: "unproved" becomes "untested" (answer 16 and child
     8's word). This covers sc21's GitLab forms and sc23's host allow rules and Copilot lines.
  2. History (a date, a batch, an incident): it moves to `docs/incidents.md` (child 24) or under
     `docs/proofs/`, and the card keeps the rule alone.
  3. A behaviour phrase that matches by accident ("record the user's answer"): reword it with no
     change of meaning ("the user's reply").
  4. Only what none of these fixes goes in `lint-allow.txt`.
- **`lint-allow.txt` format.** One entry per line: path (relative to the repository root), TAB,
  the exact matched text, TAB, the rule id of the sentence, TAB, the reason. `#` starts a comment
  line.
  - An entry that matches nothing fails (stale).
  - An entry whose rule id is a floor row, or whose path is `references/floor.md`, fails.
  - An entry whose id has no row in `rules.json` fails.

### 5. `tests/test_card_rules.py` (new): the registry test (M3, M4, M8, M12)

Every check reads the shipped files through `conftest.SKILL` and `conftest.PLUGIN_ROOT`.

- `test_rule_sentences_carry_ids[<card>]`: section 1's lint on each `roles.yaml` card and on
  `floor.md`.
- `test_ids_and_rows_match`:
  - every id in `references/**/*.md` has one row whose `card` is that file;
  - every row that is not retired has its id in its card, exactly once;
  - no id appears twice across the files;
  - floor rows are `R-001`…`R-010`, kind `floor`, card `floor.md`, in the floor's order.
- `test_checks_resolve`: each check resolves.
  - `test` and `scenario` resolve the way `tests/test_scenario_coverage.py` does, reusing its
    `function_names` and `unit_names` (import them, or move them to `conftest.py`).
  - `rail` resolves against the first column of `evals/SCORECARD.md`.
  - `quiz` resolves to an existing case file whose `rules` list the id.
- `test_kinds`:
  - a non-retired row that is not `inferred` has at least one non-quiz check;
  - an `inferred` row has only quiz checks, at least one;
  - a class-a row is never `inferred` (F5), and has at least one check outside
    `tests/test_card_ids.py` (H6);
  - a floor row is never `inferred` and never retired.
- `test_inventory_rows`:
  - every `rows` id exists in `docs/proofs/cards-inventory.md`, parsed with child 25's parser;
  - every inventory kind-a row homed `floor <n>` or `card <file>` is carried by exactly one row
    whose `card` matches the home.
- `test_retired`: a retired row matches `<X.Y.Z>, <reason>`. Its id is in no file.
- `test_history_lint[<file>]`: section 4 on each file, with the allow entries applied.
- `test_lint_allow_entries`: section 4's rules on `lint-allow.txt`.
- `test_detectors[<id>]`: each `detector.pattern` compiles, matches every `positive`, and matches
  no `negative`. `name` values are unique, and a detector's `tools` are tool names of `roles.yaml`
  or the hosts' rows.
- `test_help_names_resolve`: every `` `help <name>` `` in `references/**/*.md`, the wrappers and
  `skills/*/SKILL.md` is a key of `topics.json`, read with `load_topics()`.
- `test_no_orphan_topic`: every file under `references/topics/` is named in some topic's
  readings.
- `test_registry_refusals` (prepared texts, built from pieces of 40 characters or fewer). These
  cases must fail:
  - a date in a card;
  - a rule sentence with no id;
  - an id with no row;
  - a row whose id is not in its card;
  - a check naming a missing test;
  - an `inferred` class-a row;
  - a retired id still in a card;
  - a stale allow entry;
  - an allow entry on a floor id;
  - a detector matching its own negative.

### 6. The detectors move (M8)

- Each of the nine seed detectors of `evals/kit/detectors.json` (sc05) goes into the `detector`
  field of the row whose sentence states its rule. Its old id is kept as `detector.name`, so the
  measure's comparison with the previous results file still matches.
  - `merge-by-agent` goes to `R-001`.
  - `merge-not-ff` and `plain-force-push` go to `R-002`. A row holds one detector, so the second
    one goes on the floor-2 sentence of the card that states it.
  - `discard-work` and `git-stash` go to `R-005` and its card sentence, the same way.
  - `stop-by-name` goes to `R-010`.
  - `add-all`, `cd-into-changes` and `no-verify` go to the card or topic sentence that states each
    one.

  The field is `detector` (one object), as the program names it.
- A detector whose rule no sentence states is a finding. The Driver does not invent a sentence.
  It lists the detector in the PR, keeps it in a row only once a sentence exists, and otherwise
  names it in Known gaps (Q4 below).
- `evals/kit/detectors.json` is deleted.
- `evals/kit/behaviour.py`:
  - it reads the rows of `rules.json` that carry a `detector`;
  - it reports by `detector.name`, with the row's id beside it;
  - `--prune` takes as candidates the rows whose kind is not `floor`, with zero hits in both files
    (in place of `floor: null`).
- `evals/kit/dry_run.py`: check 4 of the behaviour case is removed (it is now pytest's). The
  fixture's expected output takes the new id column.
- `evals/README.md` and every other mention of `detectors.json` (`git grep detectors.json` at
  head) are updated.

### 7. The quiz and the inventory (H4, H5, H8)

- Every `floor-<n>` in the `rules` of `evals/quiz/**/*.json` becomes `R-00n` (`R-010`).
  Inventory ids and `J<n>` rails stay.
- `evals/kit/quiz.py`'s `load_cases` accepts `R-\d{3}` only when the id is a non-retired row of
  `rules.json`. It no longer accepts `floor-<n>`. The dry run's quiz case is updated the same way.
- The kind-a rows of sc25's owner list 4 (Q3): each gets a behaviour check. It is the existing
  refusal test, scenario unit, rail or quiz case that proves it, where one exists. Otherwise the
  Driver writes one quiz case in sc06's format, with no run and no spend: child 28 runs the quiz.
  The PR lists each row with its new check.
- `docs/proofs/cards-inventory.md` is not rewritten. The link is `rules.json`'s `rows`.

### 8. `tests/test_card_ids.py` (new) and `tests/test_card_pins.py` (new): M13

- **Id pins.** Every file-and-heading pin that child 24 converted is replaced by one
  parametrized test, `test_rule_in_card[<id>]`. It asserts that the id is in the card its row
  names. The scattered heading pins in the files sc24 lists (section 6, "Converted to
  file-and-heading pins") are removed. A pin on a CLI line (a refusal, a `next:` line) stays where
  it is: it pins code, not a card.
- **The pin scan, `test_no_card_phrase_pins`.**
  - It reads every `tests/**/*.py` with `ast` and collects string constants longer than 40
    characters. Docstrings are skipped. An f-string's literal parts are joined.
  - It also reads the data files under `tests/` (`*.tsv`, `*.json`, `*.txt`, `*.md`), field by
    field.
  - It fails on each one that occurs in a shipped card, with whitespace collapsed on both sides.
    A shipped card is `references/**/*.md`, a wrapper body, or `skills/*/SKILL.md`.
  - Exempt: `tests/test_card_rules.py` (the registry test), and a line marked
    `# card-pin: <reason>`. The marked lines are counted and printed, and their count must not
    exceed `MAX_PINS`, set to the count at head. A marked literal found in `floor.md` fails anyway.
  - `tests/moved_rules.tsv`, if child 24 kept it, is converted or deleted with its test.
- **`test_pin_refusal`** (prepared): a test source holding a literal longer than 40 characters
  copied from a card fails, naming it. A marked one passes and is counted.

### 9. The link check (H10)

`tests/test_plugin_files.py::test_skill_and_references_links_resolve`:

- it globs `references/**/*.md`, `docs/**/*.md`, `skills/*/SKILL.md`, `README.md`,
  `CONTRIBUTING.md` and the wrappers;
- it resolves each relative link;
- a link with an anchor also needs a heading in the target whose GitHub slug equals the anchor
  (lowercase, spaces become `-`, punctuation other than `-` and `_` dropped).

### Files touched

- New:
  - `references/budgets.json`, `references/rules.json`, `references/lint-allow.txt`;
  - `tests/test_card_budgets.py`, `tests/test_card_rules.py`, `tests/test_card_ids.py`,
    `tests/test_card_pins.py`.
- Changed:
  - every `roles.yaml` card and `floor.md` (ids, M3 fixes, rewordings);
  - topics and shared files with M3 hits or ids;
  - `docs/incidents.md` (moved history);
  - `evals/kit/behaviour.py`, `evals/kit/quiz.py`, `evals/kit/dry_run.py` and their fixtures;
  - `evals/quiz/**/*.json`, `evals/README.md`;
  - `tests/test_plugin_files.py`, `tests/test_scenario_coverage.py` (helpers shared), and the
    pin files sc24 lists.
- Removed:
  - `evals/kit/detectors.json`;
  - `tests/test_brief_bytes.py` (folded);
  - the scattered heading pins.
- Untouched: `src/`, `hooks/`, `types/`, AGENTS.md, versions.

The Driver chooses the test file names within this plan. A rename is listed in the PR.

## Out of scope

- Raising any limit, or setting the six shared files' targets: the owner's line, through child 27
  or 28 (M11).
- `roles lint` (sc18) and the host rows' history check (sc08).
- The retro ladder, the approval reminder, the measure's place in the release (child 27).
- Running the quiz or the behaviour measure, or any spend (child 28).
- Rewriting a card's meaning, or restoring rules (child 25). Only tags, M3 fixes and the
  rewordings of section 1 are allowed.
- Making the sentence-id lint mandatory in topics and shared files (Q2).
- Rewriting `docs/proofs/cards-inventory.md`.

## Host and default matrix

| | Claude Code (shipped defaults) | Copilot |
|---|---|---|
| Tests, `just check`, `just eval-dry-run` | run | the same tests (pytest has no host) |
| M2 path limits | measured from the claude host rows | measured from the copilot rows. Copilot's real reading is untested (unproved) |
| Long gate `just scenario (ubuntu-latest)` | owed | none |

## Acceptance evidence

1. `just check` passes in the worktree at the rebased head. `just eval-dry-run` passes too, since
   `evals/kit/` changes. Both commands and their final lines are quoted.
2. The long gate `just scenario (ubuntu-latest)` is green at the PR's head. The local Windows
   `chantier gate <cr> scenario` is owed only if this CR is the stack's top when it is called
   ready, which it is not while child 27 and child 28 stack on it.
3. The new tests pass on the shipped files at head. Each refusal case fails as expected, at least
   these: a card over budget, a date in a card, an id with no row, a phrase pin, an inferred
   class-a row, a stale allow entry, a retired id in a card. The PR quotes one failure line per
   case.
4. The freeze table of section 2, with every file over its target and every `pending_owner` row.
5. The rewordings (before and after), the M3 fixes with where the history went, and the allow
   entries with their reasons.
6. The detectors' new homes, and any detector with no sentence (Q4).
7. The kind-a rows of owner list 4 with their new checks (Q3).
8. **`just test` seconds.** The measurement at `origin/main` 8a960d34, on the owner's Windows
   machine under the load of parallel sessions, was:
   - the full suite in 137.35 s (2,597 passed, 20 skipped, 2 failed only because the copy had no
     `.git`). That is already above the AGENTS.md ceiling of 48.5 s (18.5 s + 30 s). The ceiling
     is open in `2-backlog/P2/test-ceiling-decision`;
   - comparable static card tests at 0.01 to 0.41 s of call time each.

   This CR's new tests are static file reads plus in-process `brief` calls, with no repository
   fixture. Their target is at most 2 s of call time together. The Driver quotes:
   - `just test` at the base and at head, on the same machine;
   - `pytest --durations=0` on the four new files;
   - the net seconds added.
9. The merge wait recorded (`$CHANTIER wait <cr> merge <child 28's PR>`), and the hand-over
   checklist closed, every line `done:` or `known gap:`.

## Risk

- The cards gain about 8 bytes per id. The count strips them (Q1), so no limit moves.
- A wrong sentence split makes the lint noisy. The refusal cases and the shipped pass pin its
  behaviour, and the rewordings are listed for review.
- Deleting `detectors.json` breaks the comparison with the 0.15.1 baseline results unless
  `detector.name` keeps the old ids. The dry run's previous-file case proves it.
- The long gate is owed: the cards change (ids, M3 fixes).

## AGENTS.md

None (program). No CLI tool and no `src/` change.

## Handback

- Validated, with Known gaps:
  - "real run not done (child 28)";
  - "do not merge: merges with children 19 to 28 as one unit, after child 28's campaign";
  - every file above its target, with its size;
  - every `pending_owner` row;
  - every detector with no sentence;
  - the AGENTS.md test ceiling already exceeded at the base (figures above).
- The typed merge wait on child 28.

## Open questions

1. **sc26-Q1 (scope): budgets against ids and child 25's growth.** The program freezes limits at
   child 24's reached sizes and forbids a limit above them. This conflicts with two things. Ids
   add bytes, and child 25 may restore lines into a card. Default:
   - the count strips `[R-nnn]` tags;
   - a file child 25 grew keeps child 25's size as its limit, marked `pending_owner`, listed in
     Known gaps, and confirmed or cut by the owner at child 28.

   The alternative is a stop: the test fails until the owner raises the limit.
2. **sc26-Q2 (scope): where ids are mandatory.** The program says "every never/must/only/always
   sentence of a card". Default: the `roles.yaml` cards and `floor.md` only. Topics and shared
   files may carry ids, but the lint does not require them. Requiring them everywhere would add
   many ids and rewordings to text that is read rarely.
3. **sc26-Q3 (risk): kind-a rules with only a quote check (sc25 owner list 4).** Default: each
   gets the existing behaviour check where one exists, or else a new quiz case, written but not
   run (no spend tonight; child 28 runs it). Until child 28 runs it, such a rule is proven only on
   paper.
4. **sc26-Q4 (scope): a detector with no rule sentence.** If no sentence in the new cards states
   what a detector catches (for example `add-all` or `cd-into-changes`, if the rewrite dropped
   them as inferable), default: the detector leaves the measure, and it is listed in Known gaps
   for the owner. The Driver writes no new card sentence for it, since that would grow a card
   above its frozen limit.
