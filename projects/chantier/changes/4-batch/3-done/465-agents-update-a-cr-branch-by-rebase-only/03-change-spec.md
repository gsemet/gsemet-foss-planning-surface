# Agents update a CR branch by rebase only

Short name: `rebase-only`. From the owner's word of 2026-11-23, relayed by the Chief of Staff of
markdown-okf-schema-studio. No issue.

## Goal

The PRs chantier delivers never hold a merge commit, in any project, and in a stack too (a CR
updated on the CR below). The agents that move a CR's branch (the CR Driver, the Release driver,
the stack driver and the Conflict resolver) update it by rebase only. Their means is a local
rebase and the protected force-push of the CR's own branch. The forge's rebase action is allowed
but unproved. They never merge the base (or any other branch) into the CR's branch, and never use
the forge's "Update branch" merge button. This holds on GitHub and GitLab alike. A branch that
already holds a merge commit, a GitLab fold included, is rebased by its Driver itself. `ship`
refuses a branch that holds a merge commit and says to rebase. No `chantier.yaml` key and no
project exception for now.

Why: in markdown-okf-schema-studio batch-07, merge commits landed twice in PR branches (#458,
#462); each cost a rebase round.

## Decisions carried from the grill (`02-answers.md`)

- Q1 then Q4: no project key and no project exception for now. In the PRs chantier delivers there
  is never a merge commit; when one appears, the branch is rebased. (Q4 replaces Q1's exception
  part: a project that would prefer merges is not handled by this CR.)
- Q2 A: a branch that already holds a merge commit is rebased by its Driver itself, then pushed
  with the protected force-push of its own branch (`git -C <worktree> push --force-with-lease -u
  <remote> <branch>`).
- Q3 A: in a stack, a CR is updated on the CR below by rebase only, too.
- Q5 A: `ship` refuses a branch that holds a merge commit and says to rebase.
- Q7 A: a GitLab fold. The folded CR's Driver rebases its branch onto its base, which linearizes
  the fold, then pushes with `--force-with-lease`, ships and judges again. The `folded:`
  procedure in `driver.md` says so.
- Q8 A: the agents' means is the local rebase plus `--force-with-lease`. The forge's rebase action
  is allowed but marked unproved, with a trial named, and its commands are not stated as fact.
- The critic's other findings, recorded after Q8 and carried below:
  - the new check runs `git rev-list --merges` with `check=True`, so a git failure is the
    unreadable-base refusal (`_merges` is not reused as it stands);
  - the unit test adds the fallback-base case and the unreadable-base case;
  - the scenario line goes in the `ship` item of `scenario/README.md`.

## What changes

### 1. The CLI: `ship` refuses a merge commit among the CR's own commits

File: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py`, function `ship`.

- **When it runs.** After the head is read (`head = git("rev-parse", "HEAD", cwd=wt)`), `ship`
  checks the CR's own commits for a merge commit. This comes before the forge read
  (`read_state`), before the chain check (`refuse_off_chain`) and before any write. A new helper
  does the check, in `commands/delivery.py` or in `commands/crs.py`.
- **The lower end of the range: the base the head sits on.** It is found as
  `commands/carry.py`'s `head_base(repo, d, c, wt, head)` finds it today. The candidates are the
  start base, the PR's base, the planned place, the default branch and the batch's other CRs'
  branches; the nearest wins. In a stack, the range is therefore the CR's own commits above the
  CR below. A merge commit in a lower CR's branch is that lower CR's refusal, not this one's.
- **When `head_base` finds no base.** The lower end is `<remote>/<default branch>`, from
  `repo.config` (this is the fallback base). A branch that merged an older tip of the default
  branch is therefore still checked.
- **The check.** It runs `git rev-list --merges <lower>..<head>` with `check=True` (the
  `chantier.core.git.git` helper's default). Today's `_merges` is not reused as it stands: it
  runs with `check=False`, which would read a git failure as "no merge commit".
  - A non-empty list is a refusal.
  - A git failure is the unreadable-base refusal (below). It is never read as "no merge commit".
- **The refusal.**
  - It exits 2 (`EXIT_PRECONDITION`) and records nothing: no `ship` event, no `carry` event, no
    change to the CR's record. The forge is not read.
  - Its message names the CR, the head (seven characters), the merge commit (seven characters;
    the first one when there are several) and the base. It says what to do, for instance:
    `CR-12: abc1234 holds a merge commit (def5678) above origin/main: chantier's PRs hold none;
    rebase onto main (git -C <worktree> rebase <base>), push with --force-with-lease, and ship
    again`.
  - The unreadable-base form says which ref git could not read, with git's first line, for
    instance: `CR-12: cannot check abc1234 for a merge commit: git could not read
    origin/main..abc1234: <git's first line>; fetch and ship again`.
- **No flag skips it.** `--conflict` does not, and no `chantier.yaml` key exists for it. Every
  kind of CR is checked, a release CR and a fix CR included.
- The `ship` docstring names this refusal next to the foreign-CR refusal and the chain refusal.
- **Nothing else in the CLI changes.** `gate`, `handback`, `stack --out-of-draft`, `forge-stack`
  and the carry keep their current behaviour. The carry already refuses a judged head that holds
  a merge commit (`a merge commit in <sha7>'s commits`). So a rebase that removes a merge commit
  is gated and verified again, as for any carry refused.

### 2. The cards

Each card says it once, in its own words, and points at rule 8 rather than repeating it.

- **`skills/chantier/references/concepts.md`, rule 8 (Git):** add the rule.
  - A CR's branch is updated by rebase only: a local `git rebase <base>`, never with
    `--rebase-merges`, then the rewrite push `--force-with-lease` of the CR's own branch.
  - The forge's rebase action is allowed and unproved (below). Rule 8 names no command for it.
  - Never a merge into the branch: no `git merge`, no `git pull` without `--rebase`, never the
    forge's "Update branch" merge button. In a stack, the same holds for the CR below.
  - The PRs chantier delivers hold no merge commit. `ship` refuses one, and the branch's Driver
    removes it by a rebase.
  - The project's own rules still rank above the cards, but this CR adds no exception (Q4).
- **`concepts.md`, the exit-2 list** (the `$CHANTIER` paragraph, "Exit codes: 0 ok, 1 usage, 2
  precondition"): add `ship` of a branch holding a merge commit, or one whose merge commits git
  cannot check.
- **`skills/chantier/references/driver.md`:**
  - **"Means: rebase and push", first bullet.** The local rebase is the means of taking the base
    (rule 8). A plain `git rebase <base>` linearizes any merge commit away; never use
    `--rebase-merges`.
  - **The forge's rebase action, in the same bullet.** It is allowed, and marked: "Unproved;
    trial: a Driver uses the forge's rebase action on one CR's PR, on GitHub and on GitLab, and
    the PR's head afterwards holds no merge commit (`git rev-list --merges <base>..<head>` is
    empty). Then the worktree takes that head, and `ship` records it with no refusal and no
    `off:` line about the head." The card names no command for that action as fact. The Driver
    reads the forge CLI's help for it. After such an action, the worktree takes the PR's new head
    before any other step, by fetch then rebase onto the remote branch, never by a merge. `ship`
    follows, as after any rebase.
  - **"Means: carries, conflicts and the early push", one bullet for the new refusal.** When
    `ship` refuses `holds a merge commit`:
    - rebase the branch onto the base the refusal names (`git -C <worktree> rebase <base>`), with a
      `conflict-resolver` on a conflict;
    - push with `--force-with-lease`, and `ship` again (with `--conflict` when a conflict was
      resolved, by the `ship --conflict` rule);
    - the pass and the verdict judged at the head with the merge commit do not carry (the carry
      refuses it), so the long gate and a `verifier` run again, as for any carry refused.

    A `ship` refused `cannot check ... for a merge commit`: fetch and `ship` again. When it is
    refused again, it is a `blocked` line, never worked around.
  - **"CR driver: re-takes", the `folded:` paragraph (Q7).** It currently says to bring the
    forge's branch in with `git -C <worktree> merge --ff-only origin/<branch>`. Replace that with
    a rebase:
    - `git -C <worktree> fetch`, then `git -C <worktree> rebase origin/<branch>`. The worktree's
      commits are all in the forge's branch, so this takes the forge's head and makes no merge.
    - Then `git -C <worktree> rebase <base>` (the base `take` printed). This linearizes the fold's
      merge commit, and a conflict goes to a `conflict-resolver`.
    - Push with `--force-with-lease`, and `ship` (with `--conflict` when a conflict was
      resolved).
    - The rest stays: `pr-body.md` names the folded CR's change and its merged MR, and the move
      is judged again (`verifier` given the move, `inspector` on it, the long gate and CI at the
      new head, the description pass).
    - "Never `git reset --hard`" stays. The paragraph's "Unproved; trial: one run on a GitLab
      project" stays.
  - **"Stack driver"**, both "Who moves a branch" and the paragraph "Order the stack's CRs ...":
    each CR is rebased on the one under it, never merged with it (rule 8). A branch whose `ship`
    is refused `holds a merge commit` is rebased like any other move.
  - The Release driver section needs no line of its own: "Means: rebase and push" covers it.
- **`skills/chantier/references/conflict-resolver.md`, "Your part":** the rebase stays a rebase.
  Never resolve by merging the base in (`git merge`, `git pull` without `--rebase`), and never use
  `--rebase-merges`. A merge commit left in the branch shows up as the Driver's `ship` refusal.
- **`skills/chantier/references/hosts/claude-code.md`, "Auto-fix events":** unchanged in
  substance. It already says "never by the merge of the base branch the event asks for" and points
  at rule 8, which now states the rule. Change it only if the pointer's wording no longer matches
  rule 8.
- **`skills/chantier/references/foreman.md`:** unchanged. Its rule already says a host event that
  asks to merge the base branch in is not an order.

### 3. The agent files, both hosts together

The role's contract stays in the cards (AGENTS.md). The agent files carry the rule in their
`description:` line only. Each pair stays the same on both hosts: the body, and the shared part of
the description.

- `agents/cr-driver.md` and `com.github.copilot/agents/chantier-cr-driver.agent.md`: "Drives one
  chantier change request through rounds, ship, CI and hand-back, updating its branch by rebase
  only. ..."
- `agents/release-driver.md` and `com.github.copilot/agents/chantier-release-driver.agent.md`:
  add "updates its branch by rebase only" to the description.
- `agents/stack-driver.md` and `com.github.copilot/agents/chantier-stack-driver.agent.md`:
  "Orders, restacks by rebase only and ships a chantier stack of pull requests, ..."
- `agents/conflict-resolver.md` and
  `com.github.copilot/agents/chantier-conflict-resolver.agent.md`: "Rebases one chantier CR branch
  (never a merge) and resolves its conflicts, keeping both intents. ..."

The `Prompt starts with:` part of each description is unchanged.

## Out of scope

- A `chantier.yaml` key or any project exception allowing merges (Q4: not for now).
- The project side in markdown-okf-schema-studio (its guideline and its git-only CI check): that
  is a CR of that project's batch-09.
- A refusal in `gate`, `handback`, `stack --out-of-draft` or `forge-stack`: only `ship` checks
  (Q5).
- Running the forge rebase action's trial: the cards name the trial, and this CR does not run it.
- The forge's merge method of the PR itself, which the user chooses as each project says:
  unchanged.
- Any change to how the Foreman or the Chief of Staff handles a host's "merge the base in" event,
  beyond rule 8's wording.

## Evidence

- **Unit test.** One parametrized test in
  `skills/chantier/scripts/cli/tests/test_carry_ship.py`, in-process on a prepared repository. It
  uses the existing `stack` fixture, `commit` and `git_at` from `test_gate_carry.py`, and the
  stubbed `delivery.read_state`. Each refusal case asserts all three of:
  - exit 2;
  - the message's words;
  - nothing recorded: no new `ship` event in `events.jsonl`, and no `pr` or `head` change in the
    CR's record.

  The cases:
  - **The default branch merged in.** A CR whose branch merged `main` (`git merge --no-ff`) is
    refused. The message names the merge commit and says to rebase.
  - **The CR below merged in.** A stack CR whose branch merged the CR below's branch is refused
    the same way.
  - **A merge commit only in the CR below.** The CR below's branch holds a merge commit, and the
    upper CR is rebased cleanly on it. The upper CR's `ship` is not refused for the lower CR's
    merge: the range starts at the CR below.
  - **The fallback base.** None of `head_base`'s candidate tips is an ancestor of the head: for
    instance, the branch merged an older `main` tip and `origin/main` moved on since, while the
    start base and the other CRs' branches are not under it. `ship` still finds the merge commit
    above `origin/main` and refuses.
  - **An unreadable base.** `head_base` finds no base and `origin/main` cannot be read (the ref
    deleted). `ship` refuses with the `cannot check` message. It never records the PR as if there
    were no merge commit.
  - **After a rebase.** After `git rebase <base>` of the first case's branch, `ship` records the
    PR (exit 0).
  - **`--conflict`.** `ship --conflict` on a branch with a merge commit is refused too: no flag
    skips the check.

  Keep the test within `just test`'s time budget (AGENTS.md).
- **The existing carry test.** `carry_check`'s test (`test_gate_carry.py`, case "d: a merge
  commit") stays green unchanged.
- **Scenario check** (`scenario/run_scenario.py`). One check sits next to the CR-101 `ship`
  checks. A merge commit added to the CR's branch makes `ship` exit 2 with the rebase line and
  record nothing. With the branch reset to its earlier head (the scenario stands in for the
  Driver's rebase), `ship` records as before.
- **`scenario/README.md`.** In the `ship` item (near line 109, "`ship` reporting what is off
  (uncommitted changes, a head not pushed, no long gate at it)"), add that `ship` refuses a
  branch holding a merge commit among the CR's own commits, and records nothing.
- **Cards and agent files.** `just check` passes. It holds the structure tests, among them the
  checks on the agent files of both hosts (`test_plugin_files.py`, `test_startup_manifest.py`),
  which read the shipped files at the head under test.
- **Gates (AGENTS.md).**
  - In the worktree, at the rebased head, before the first push: `just check` and
    `just eval-dry-run` (the change is under the CLI's `src/`).
  - At the PR's head: the long gate `just scenario (ubuntu-latest)` green (the change touches the
    CLI and the cards).
  - No `hooks/` or `types/` change, so no `just mod`.

## Open questions

None. The answers through Q8, and the critic's findings recorded after them, settle the
behaviour.
