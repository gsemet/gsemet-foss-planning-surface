# SC13: A Driver messages the steering session through the board

Child 13 of 28 of the program CR `simplify-cards-and-prompts` (folder `1-inbox/simplify-cards-and-prompts`: read its `03-change-spec.md`, `02-answers.md` answers 17-22 and `work/study-*.md`). One PR of a single stack batch, built on the previous child's branch.

### Child 13: `msg-steering` — A Driver messages the steering session through the board

- **Scope** (answer 4; answer 13; answer 22, F8):
  - New commands `chantier msg steering <kind> <text> --lease N` and `chantier inbox [--read
    <id>|all] --epoch N`, declared in `src/declare/msg.py`.
    - `<kind>` is `anomaly`, `blocked` or `note`.
    - `steering` means the batch's Foreman, or the Chief of Staff in direct mode.
    - There are no `user` or `cr:` targets.
  - One `msg@1` line per message goes to the project's `forge-journal.jsonl`, through the one
    append function. Its schema goes in `src/hub/schemas.py` and `hub/schemas.json`.
  - **Delivery.** The surface server's `events` topic carries `msg@1` lines. The steering
    session's watcher (`src/hub/watch_reads.py`, which today reads `merged@1`, `checks-red@1`
    and `wait-cleared@1`) handles them as follows:
    - it wakes its session on `anomaly` and `blocked`;
    - `note` wakes nobody: notes are listed by `inbox` and at the steering session's next told
      block.
  - **No subscriber.** When no watcher of the batch's steering session is subscribed (read from
    the watcher locks `chantier/watch-<project>/<session>.lock` and the server's subscriptions),
    `msg`:
    - still appends the line;
    - prints `not delivered: no watcher subscribed`;
    - exits non-zero.

    The Driver then uses its host means or the hand-back.
  - The Foreman's own watcher (CR-479) has never run in a real batch. Its delivery is unproved,
    and child 28 measures it.
- **Depends on:** child 12.
- **Acceptance evidence.**
  - Pytest:
    - a schema round-trip;
    - a `note` does not wake, while `anomaly` and `blocked` do;
    - `inbox --read` marks a message read;
    - with no subscribed watcher, `msg` prints the line and exits non-zero.
  - A scenario step: a Driver's `msg steering blocked …` wakes the Foreman's watcher.
  - The added `just test` seconds are stated.
- **Must not.**
  - Let the board or the server send anything to an agent itself.
  - Carry a message across projects.
  - Replace `note <cr>`.
- **Risk.**
  - The long gate is owed.
  - AGENTS.md: the journal's writers and the watcher's subscribed lines gain `msg@1`, and `msg`
    and `inbox` get their line (simplify-cards-Q7, Q22).

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

