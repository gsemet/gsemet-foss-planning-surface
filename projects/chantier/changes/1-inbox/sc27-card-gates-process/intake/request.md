# SC27: The retro ladder, the approval reminder, the measure's place

Child 27 of 28 of the program CR `simplify-cards-and-prompts` (folder `1-inbox/simplify-cards-and-prompts`: read its `03-change-spec.md`, `02-answers.md` answers 17-22 and `work/study-*.md`). One PR of a single stack batch, built on the previous child's branch.

### Child 27: `card-gates-process` — The retro ladder, the approval reminder, the measure's place

- **Scope** (answer 9: M5, M6, M10, M11, M14, M7's place in the release; F13):
  - **M5.** The Retro critic's card asks each point for `home:`, `count:` and `why not code:`,
    and drops a point that lacks them. `chantier validate` checks those fields in a `retro.md`,
    read-only.
  - **M6 and F13.** The Inspector's card checks that a card diff quotes the measure line (a key
    and count from the behaviour results), or carries the owner's line. That line must quote the
    user's words as recorded in the CR's `02-answers.md`.
  - **M10.** A new `evals/results/behaviour-accepted.md` lists accepted stumbling, re-asked when
    its rate doubles. After each release retro, the Chief of Staff files the S-list of each
    measure, or answers it there.
  - **M11, as a reminder (F13).** A step of `.github/workflows/ci.yml`, in a job on
    `ubuntu-latest`, on `pull_request` only, since a push event has no body.
    - Trigger: the PR touches `references/floor.md` or `references/budgets.json`.
    - Without "Floor change approved: <user>, <date>" or "Budget change approved: <user>,
      <date>" in the body, it prints a warning annotation. It does not fail the job.
    - Its environment: GitHub's runner, with the PR's body read from the event payload and no
      local cache.
  - **M7.** "Before a release: the claims" in `evals/README.md`, and `docs/release-process.md`,
    list `just behaviour` for the version. The measure must be newer than the last card change,
    with its regressions answered, or the claims file must say "no measure: <reason>".
- **Depends on:** child 26.
- **Acceptance evidence:**
  - pytest of `validate` on a prepared `retro.md`, with the fields present and missing;
  - the CI step proved on a throwaway PR (opened, shown, closed unmerged): a touch of
    `budgets.json` without the line shows the warning;
  - a typed merge wait on child 28;
  - the added `just test` seconds are stated.
- **Must not.**
  - Let a Driver write the owner's approval line.
  - Make the CI step fail a job.
- **Risk.**
  - The long gate is owed (cards).
  - A CI job change, proved by its first run.
  - Opening and closing the throwaway PR is a forge write. The Driver does it and records the
    PR's link.

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

