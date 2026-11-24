# SC18: Role data and a `just` check of the wrappers

Child 18 of 28 of the program CR `simplify-cards-and-prompts` (folder `1-inbox/simplify-cards-and-prompts`: read its `03-change-spec.md`, `02-answers.md` answers 17-22 and `work/study-*.md`). One PR of a single stack batch, built on the previous child's branch.

### Child 18: `roles-data-check` — Role data and a `just` check of the wrappers

- **Scope** (answer 12; answer 22: F9, Q3; study-fable 4.7):
  - New `skills/chantier/roles.yaml`. Per role, it holds:
    - name;
    - kind: `steering`, `driver`, `worker`, `review-step` or `critic`;
    - started by;
    - tools;
    - writes: `none`, `worktree` or `cr-folder`;
    - reply format;
    - card file;
    - first line;
    - description;
    - host specifics.

    It covers all 18 roles.
  - `brief` (child 10) and `help --for` (child 7) read it in place of their current tables, with
    the same output.
  - New `just roles` target running a new script, `scripts/roles_check.py`. It is not a CLI
    command and writes nothing in the plugin. It checks that each wrapper in `agents/` and
    `com.github.copilot/agents/` agrees with the data (name, description, tools, first line),
    that both hosts' bodies are identical, and that each card and reply format exists. A
    `--write` option prints the expected wrapper and writes nothing.
  - The wrappers stay hand-written (Q3).
- **Depends on:** child 17.
- **Acceptance evidence.**
  - `just roles` passes on the committed wrappers and fails on a prepared mismatch.
  - `brief`'s bytes are unchanged for each role.
  - It replaces the "bodies identical" half of `tests/test_plugin_files.py`.
  - The added `just test` seconds are stated.
- **Must not.**
  - Add a `roles:` key to a project's `chantier.yaml`. That key collides with
    `src/playbook/config.py:35`, and project roles are out of scope.
  - Write wrappers.
  - Add, remove or rename a role.
- **Risk.** The long gate is owed. No AGENTS.md change: the wrappers stay hand-written, and child
  9 already names `roles.yaml`.

### Common to children 19 to 23: the new card set, unloaded

Children 19 to 23 write the target card set in `skills/chantier/cards-next/`. That folder
mirrors the target layout of `references/`, and nothing loads it: no manifest, no CLI line, no
`SKILL.md` or wrapper names it. Child 24 swaps it in.

What a card holds:
- the role's goal;
- what the role owns;
- its own nevers, five as a target. The cap gives way before a rule that protects the user or
  the repository (F5);
- how the role ends;
- its reply format.

A card holds nothing that the floor, a topic, a refusal, a `next:` line or `--help` already
holds.

Card budgets, in LF bytes (study-fable 4.2), as targets (Q4):

| Card | Target |
| --- | --- |
| Chief of Staff | 6 KB |
| Griller | 4 KB |
| Foreman | 4 KB |
| CR driver, stack driver | 4 KB each |
| Release driver | 3 KB |
| QA driver | 2 KB |
| Verifier | 3 KB |
| Inspector | 2 KB |
| Other workers and critics | 1.5 KB each |
| Board Griller | 2 KB |
| Floor | 1.2 KB |
| A topic | 1.5 KB |

A card above its target is listed in its PR's Known gaps with its size. Only the owner raises a
target.

Rare cases become topic files in `cards-next/topics/`, listed in `cards-next/topics.json`.
Answer 10's rare rules carry `review_by` set to the next minor version.

Each child's evidence:
- the per-role byte figures of `brief <role> --cards skills/chantier/cards-next`, set beside the
  old start readings;
- `just quiz <role> --cards skills/chantier/cards-next` for each of its roles, against the
  baseline of child 6, under F4's pass rule;
- a row list of the old rules the family covers, as a first draft for child 25.

Each child records a typed merge wait on child 28, and carries the Known gap "real run not done
(child 28)".

Long gate: these children change only a folder nothing loads, but they are card changes, so
`just scenario (ubuntu-latest)` is owed.

None of these children edits `references/`, the CLI or the hook.

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

