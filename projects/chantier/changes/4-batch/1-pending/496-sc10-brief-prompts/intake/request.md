# SC10: `chantier brief` writes a role's whole prompt

Child 10 of 28 of the program CR `simplify-cards-and-prompts` (folder `1-inbox/simplify-cards-and-prompts`: read its `03-change-spec.md`, `02-answers.md` answers 17-22 and `work/study-*.md`). One PR of a single stack batch, built on the previous child's branch.

### Child 10: `brief-prompts` — `chantier brief` writes a role's whole prompt

- **Scope** (study-fable design line 3; the floor as judged above; answer 22: F1, F10, F19):
  - New `references/floor.md`, at most 1,200 LF bytes: the ten rules of "The floor", one line
    each.
  - New command `chantier brief <role> [<cr>] [--lease N] [--epoch N] [--cards <folder>]`. It is
    declared in `src/declare/brief.py`, with its handler in `src/commands/brief.py`.
  - The role's card, wrapper, first line and `writes:` value are read as data: from what
    `src/plugin_files.py` and the Driver's prompt table already read, in the form child 18 later
    puts in `roles.yaml`.
  - **Which roles.** All 18: the 15 with a wrapper, and the three that boot with no parent to run
    `brief`: the Chief of Staff, the Griller and the Foreman (F19).
  - **The brief file.** `brief` writes the prompt to the repository's git folder, at
    `chantier/briefs/<batch or "none">/<cr or "none">-<role>.md`, never published (F10). For a
    given role, version and CR facts, the file is byte-stable. It holds, in order:
    1. the role's card, whole;
    2. the floor;
    3. the facts: CLI, worktree, folder, specification, PR, rounds, notes, lease, `writes:`,
       `Rewrites:` for a Driver, `Team:`;
    4. the host rows the role uses (child 8);
    5. the line "`$CHANTIER next` says what is due; `$CHANTIER help <topic>` when a line names
       one".
  - **The short prompt** (F1). `brief` prints the prompt to pass:
    1. the role's first line, unchanged, since the wrappers check it;
    2. the `writes:` and `worktree:` lines, exactly as `driver_prompt_lines` and
       `worker_prompt_lines` print them today, because the hook reads them from the spawn prompt
       (`hooks/register.tsx`, `writesOf`, `worktreeOf`);
    3. "Read <the brief file> whole, first."
  - `--cards <folder>` builds the brief from another folder of cards. Children 19 to 23 use it to
    check their unloaded set, and child 6's quiz uses it too.
  - The facts' source for `brief` is `src/driver_prompt.py`'s `driver_prompt_lines`, plus
    `worker_prompt_lines` and `chief_prompt_lines` from `src/plugin_files.py`. Their current
    outputs in `take`, `round`, `handoff` and `order qa` stay unchanged in this child. Child 24
    switches them.
- **Depends on:** child 9.
- **Acceptance evidence.**
  - Pytest, for each of the 18 roles and both hosts:
    - the file starts with the card and holds the floor once;
    - two runs give the same bytes;
    - the printed first line equals the wrapper's `Prompt starts with:`;
    - the short prompt carries `writes:` and `worktree:`, and the hook's `writesOf` on it returns
      the same list as on `take`'s skeleton. A case in `hooks/register.test.tsx` feeds it the
      short prompt; the hook itself is not changed.
    - a Driver's brief carries the same facts as `take`'s skeleton;
    - nothing is written under the planning folder.
  - A scenario step starts a Driver from `brief cr-driver <cr>`.
  - The added `just test` seconds are stated.
- **Must not.**
  - Change the output of `take`, `round` or `handoff`.
  - Edit an existing card.
  - Write a brief in the planning folder.
  - Change the hook's logic.
- **Risk.**
  - The long gate is owed. `just mod` is owed if the hook test file changes.
  - AGENTS.md: the CLI's write list gains `chantier/briefs/` in the git folder, and `brief`
    gets its line. The role sentences are child 9's.

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

