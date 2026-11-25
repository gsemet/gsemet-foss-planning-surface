# SC01: Push a CR's own branch through the CLI

Child 1 of 28 of the program CR `simplify-cards-and-prompts` (folder `1-inbox/simplify-cards-and-prompts`: read its `03-change-spec.md`, `02-answers.md` answers 17-22 and `work/study-*.md`). One PR of a single stack batch, built on the previous child's branch.

### Child 1: `push-own-cr-branch` — Push a CR's own branch through the CLI

- **Scope.**
  - New command `chantier push <cr> [--lease N]`. It is declared in `src/declare/delivery.py`,
    with its handler `push` in a new `src/commands/push.py`.
  - The help text says plainly why the command exists: to declare that the operation is
    legitimate, as chantier's own update of the CR's own branch after a rebase, with the lease
    held.
  - Rails, checked before any git write. Each refusal says what to do.
    - The branch is the CR's recorded one (`CrEntry.branch`), matches `chantier/*` and is not
      the default branch (`repo.config["default_branch"]`).
    - The caller holds the lease, checked through `leases.require` then `leases.claim`
      (`src/core/leases.py`). Three leases count: the CR's own; the stack's (unit `"stack"`),
      for a CR in a stack batch's chain; and an order's, for a QA order's unit.
    - The worktree, `cr_worktree(c)`, is clean: `git status --porcelain
      --untracked-files=normal` is empty. Its HEAD is on that branch.
  - The push runs from the worktree:
    `git push --force-with-lease=<branch>:<expected> <remote> HEAD:refs/heads/<branch>`.
    - `<remote>` comes from `repo.config["remote"]`.
    - `<expected>` is the worktree's ref `refs/remotes/<remote>/<branch>`. When that ref is
      absent, the expectation is empty, so the push creates the branch only if the remote has
      none.
    - Never plain `--force`, never `--no-verify`.
  - When git refuses (a stale lease, a protected branch, a hook):
    - git's text is printed verbatim and the command exits with the external-failure code;
    - nothing is retried;
    - there is no forge read of branch protection (Q7).
  - The command records a `push` event inside `RenderedBatch`:
    `b.log("push", cr, branch=…, head=…, expected=…)`. This renews the lease, as other Driver
    commands do.
  - The same command serves GitHub and GitLab. It is git only, with no forge call.
  - Never through a profile or the server:
    - `src/core/remote_wire.py`: `push` joins `NEVER_REMOTE`.
    - `src/clients/remote.py` refuses it through a profile with a line like `GATE` ("push runs
      on the machine that holds the worktree…").
    - `src/board/cli_run.py`'s `judge` refuses it in `cli.run`.
  - `src/driver_prompt.py`, `_rewrites_line`: the push half names `$CHANTIER push <cr> --lease
    <n>`, one per CR branch in a stack. The rebase half is unchanged.
  - `src/commands/delivery.py`, `_off_worktree`: the "not pushed" line names `chantier push`.
  - `src/commands/allow_samples.py`: P10 keeps its force-push samples, because the steering
    session keeps the plain push (Q6), and adds none for `push`. Whether the user's
    `chantier *` allow rules match what agents type is unproved: study-classifier found they
    seldom match compound forms.
  - AGENTS.md changes:
    - The CLI's named git exceptions gain `push`: one `git push --force-with-lease` of a CR's
      recorded `chantier/*` branch, from its worktree, never forced, never `--no-verify`.
    - The network list gains this push.
    - `push` joins `gate` among the commands that never run through a profile.
    - The named-exceptions paragraph gives its source. First, the user's answers
      simplify-cards-Q5 (2026-11-24) and Q22. Second, study-classifier's measure: 13 classifier
      refusals of force pushes in 12 days, each one a lost Driver, and 4 questions to the user;
      83 % of the pushes were typed as compound commands that no allow rule matches.
    - The paragraph says the command states the operation's legitimacy.
    - It also says (F21) that `chantier push` is the one way a Driver publishes its branch. It
      is never run as a retry after a refused `git push`, and a refused `chantier push` is not
      followed by a raw push from the Driver. The refused-push route of answer 8 stays.
- **Depends on:** batch-31's stack top (CR-485's branch unless merged).
- **Acceptance evidence.**
  - Pytest, in a new `tests/test_push.py`: parametrized, in-process, on a prepared state with a
    bare remote.
    - Each refusal exits non-zero and runs no `git push`: branch not recorded, not `chantier/*`,
      the default branch, no lease, a stale lease, a dirty worktree, HEAD on another branch.
    - A valid call pushes, records the event and renews the lease.
    - When the remote has moved since the tracking ref, git refuses, and the command exits
      external with git's text.
    - `push` is refused through a profile and through `cli.run`.
  - A scenario step in `scenario/run_scenario.py`: a Driver rebases, then runs `push`, then
    `ship` prints no "not pushed" line. Run on GitHub and on the GitLab unit.
  - **The smoke trial in auto mode (answers 7 and 22, F3; Q2).**
    - The child's own Driver, a subagent, pushes its own CR branch five times with the
      worktree's build, in the compound form agents type. Example: `C="uv run --no-sync
      --project <worktree> chantier --project <planning>"; $C push <cr> --lease <n> 2>&1 | tail
      -3`, after a small commit or rebase each time.
    - For each try, the PR's Deliverables record the exact command text, the session's
      permission mode as the host shows it, and the host's verdict: ran, or the refusal's text.
    - The user's allow rules name the main checkout's path, so the worktree build's command is
      always judged by the classifier. That makes it the harder case, and the record says so.
    - On a refusal: record it, then try once more, alone, as a plain command. If that also
      fails, the Driver hands back blocked with the text, and the program stops for the owner.
      It is not worked around.
    - The trial is a smoke test, not the proof. The proof is the `chantier push` refusal rate,
      measured afterwards by child 5's tool on later runs.
- **Must not.**
  - Push any branch but the CR's recorded one.
  - Read or write the forge.
  - Push through a profile.
  - Add `--force` or `--no-verify`.
  - Change a card's text.
  - Run a rebase.
  - Give the steering session a lease-free form (Q6).
- **Risk.**
  - The long gate is owed (CLI and scenario).
  - AGENTS.md changes: a third git exception, a network use and the F21 sentence. Answer 7
    gives the owner's word for this subcommand, and the PR quotes it.
  - The classifier's verdict on the command text is unproved until the trial, and is only
    measured afterwards.

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

