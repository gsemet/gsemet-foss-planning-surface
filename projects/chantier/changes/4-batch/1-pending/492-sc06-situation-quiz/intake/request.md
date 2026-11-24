# SC06: A cheap quiz of a role's boot on one situation

Child 6 of 28 of the program CR `simplify-cards-and-prompts` (folder `1-inbox/simplify-cards-and-prompts`: read its `03-change-spec.md`, `02-answers.md` answers 17-22 and `work/study-*.md`). One PR of a single stack batch, built on the previous child's branch.

### Child 6: `situation-quiz` — A cheap quiz of a role's boot on one situation

- **Scope** (answer 14's quiz; answer 22, F4):
  - New `evals/kit/quiz.py` and `just quiz <role> [--cards <git ref or folder>] [--case <id>]`.
    For one case, the quiz:
    1. builds the role's boot text from the cards given;
    2. adds one situation and asks "what do you do next";
    3. runs it three times on the role's model as the shipped playbook gives it
       (`config/chantier.defaults.yml`);
    4. has a judge read each reply against the case's expected behaviour;
    5. prints the pass counts per case and per role.
  - **The runner** uses the headless host CLI with the board Griller's proved flags
    (`src/board/griller_host.py`: `--setting-sources ""`, `--plugin-dir`,
    `--strict-mcp-config`). The user's settings, hooks and MCP servers therefore stay out.
  - **The judge** is new, `evals/kit/quiz_judge.py`. The existing `evals/kit/judge.py` runs
    hidden pytest files and reads no reply. The new judge:
    - uses one named model, not the role's own, set as a constant in the file;
    - reads the reply and the expected behaviour;
    - answers pass or fail with one line of reason.
  - **The spend cap.** Before any model call, the quiz prints the planned number of runs and the
    estimated spend, and stops if the estimate exceeds `--max-usd` (default 10). The batch's
    `cost` does not see this spend.
  - **Cases** live in `evals/quiz/<role>/<id>.json`. Each holds: id, role, situation, expected
    behaviour, and the rule it proves. The rule is the floor rule's number for now; an `R-nnn`
    id from child 26.
    - Seed: one case per floor rule for the roles it binds, plus one per rail of
      `evals/SCORECARD.md` of kind judgement that names a role.
    - Rows judged "inferable" in child 25 are grouped, several per case.
  - **Pass rule (F4).** A new card set passes when no case scores 0 of 3 that the old cards
    passed.
  - **Boot text by stage:**
    - Before child 24: for the old cards, the role's declared start reading (the files
      `tests/test_start_reading.py` resolves). For a folder of new cards, the output of
      `chantier brief <role> --cards <folder>` (child 10).
    - After child 24: `chantier brief <role>`.
  - **The baseline:** the quiz on the old cards at the stack's base. The result file is named by
    the convention of `evals/results/`.
- **Depends on:** child 5.
- **Acceptance evidence.**
  - `just eval-dry-run` runs the quiz's plumbing with no model: a staged reply and a staged
    verdict.
  - The spend cap's refusal is tested.
  - The baseline file is committed with its pass counts and its spend.
- **Must not.**
  - Run in CI.
  - Spend on a model in `just check`.
  - Judge with the role's own model.
  - Load the user's settings, hooks or MCP servers.
- **Risk.**
  - The long gate is owed only if a change falls outside `evals/`; the `justfile` target is
    outside it.
  - `just eval-dry-run` is owed.
  - Model cost falls on the user's machine, capped and printed.
  - Whether a Driver subagent may start a headless host CLI in auto mode is unproved. A refusal
    is not worked around: the Driver hands back with the plumbing and the cases, and the
    baseline is run by the Chief of Staff.

---
Program context (copied):

## Order

Four steps, as answer 18 sets them. Answer 20 allows a step to be cut into chained CRs.

1. **Tools first** (children 1 to 18). Each tools child only adds things: commands, flags, lines,
   files and data. It removes no output the current cards rely on, and it changes no text in an
   existing card. Every intermediate `main` keeps working with the old cards. The push subcommand
   comes first, and its smoke trial in auto mode runs before any card is cut (answers 7 and 22).
2. **The total rewrite** (children 19 to 24):
   - Five family CRs write the whole new card set in a folder nothing loads.
   - One swap CR switches the CLI and the hook to the new set, removes the old set and converts
     the tests.
   - This is one target state, reached in one pass of chained CRs. No family runs on new cards
     before the others (answers 14, 17, F2).
3. **The read-and-compare review** (child 25).
4. **The gates and the measure** (children 26 to 28): the pytest and process gates of answer 9,
   then the sandbox campaign on the new cards (F6).

**The merge rule (answers 14 and 22: F2, F11, Q8):**
- Nothing merges while the owner sleeps. Each child is presented as ready, and the owner merges.
- Children 1 to 18 keep the old cards working. Each may merge, in order, once the owner says so.
- Children 19 to 28 (the family CRs, the swap, the review, the gates and the real run) merge as
  one unit:
  - in one sitting, in order;
  - with no chantier session started in between, since the plugin is read live from the main
    checkout;
  - and only after child 28's campaign has passed on the stack's top worktree.
- Each of children 19 to 27 records a typed merge wait on child 28:
  `$CHANTIER wait <cr> merge <child 28's PR>`, so the `handed back:` line prints
  `do not merge: waits for …`.
- Each of children 19 to 27 is handed back validated, with the Known gap "real run not done (child
  28)" until child 28's results are in.

How study-fable-v2 section 6 is regrouped (answer 18):

| Study child | Here |
| --- | --- |
| 1. Measure the new cards for real | child 5 (the tool), child 28 (the run) |
| 2. The carrier for the pieces | child 7 |
| 3. The host card out of the start | child 8 (data, proofs), child 10 (host rows in `brief`), child 23 (cards) |
| 4. Quick cuts | child 17 (launcher), child 11 (`status --since`), child 24 (`handoff` without the worker lines; `driver:refused` without the Foreman's piece) |
| 5. The tools | children 10 to 16 |
| 6. Refusals | children 2, 3, 4 |
| 7. The rewrite, by family | children 19 to 24. Families are written separately but swapped as one (answer 17 replaces the `cards:` key) |
| 8. Roles as data | child 18 (narrowed by F9) |
| 9. Removal | child 24 |

## Rules for every child

- **Base.** In a stack batch, each child's base is the previous child's branch. Child 1's base is
  batch-31's stack top when it joins: CR-485's branch, unless CR-485 has merged (F16).
- **Before the first push.** Run `just check`. A change under `src/` or `evals/kit/` also runs
  `just eval-dry-run` (AGENTS.md).
- **Long gate.**
  - A child that changes the CLI, the cards or the scenario passes `just scenario
    (ubuntu-latest)`, green at its PR's head.
  - In this stack only the CR on top owes the local Windows run, `chantier gate <cr> scenario`.
    When a child joins on top, that run moves to it.
  - A child that changes only `evals/` or `docs/` owes no long gate.
- **Hook changes.** A child that changes `hooks/` runs `just mod` itself before its PR. One that
  cannot stops and says so.
- **New commands.** A new command adds a step to `scenario/run_scenario.py` and its coverage
  bullet (`tests/test_scenario_coverage.py`).
- **`just test` time (F20).** Each child states in its PR, under Deliverables, the seconds its
  tests add to `just test`, measured before and after on the same machine. The ceiling is still
  open (`2-backlog/P2/test-ceiling-decision`).
- **Journal types.** A new journal type regenerates `hub/schemas.json` with `just journal-schemas`.
- **AGENTS.md lines.** Each new CLI tool adds its line to AGENTS.md's named exceptions, with its
  source: the measure (figures from study-behaviour or study-classifier) or the user's answer
  (simplify-cards-Q…). AGENTS.md does the same today for `wait`, `access` and `live`.
- **Card text.** No child before 19 edits an existing card's text. Children 19 to 23 write only
  the new, unloaded set.
- **Versions.** No child edits a version by hand.
- **Text style.** Repository text is in English. No date, batch name or trial story goes in a
  card (M3, enforced from child 26).
- **Unproved claims.** A claim about the host, a tool version or the classifier that this program
  has not proved is marked "unproved" in the child's specification and in its PR (F17).

