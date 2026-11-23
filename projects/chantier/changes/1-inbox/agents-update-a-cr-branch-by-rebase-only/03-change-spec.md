# Agents update a CR branch by rebase only

Short name: `rebase-only`. From the owner's word of 2026-11-23, relayed by the Chief of Staff of
markdown-okf-schema-studio. No issue.

## Goal

The PRs chantier delivers never hold a merge commit, in any project, and in a stack too (a CR
updated on the CR below). The agents that move a CR's branch (the CR Driver, the Release driver,
the stack driver and the Conflict resolver) update it by rebase only: a local rebase and a
protected force-push of the CR's own branch, or the forge's rebase action. Never a plain merge of
the base (or of any other branch) into the CR's branch, and never the forge's "Update branch"
merge button. This holds on GitHub and GitLab alike. A branch that already holds a merge commit is
rebased by its Driver itself. `ship` refuses a branch that holds a merge commit and says to
rebase. No `chantier.yaml` key and no project exception for now.

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

## What changes

### 1. The CLI: `ship` refuses a merge commit among the CR's own commits

File: `skills/chantier/scripts/cli/src/chantier/commands/delivery.py`, function `ship`.

- After the head is read (`head = git("rev-parse", "HEAD", cwd=wt)`) and before the forge read
  (`read_state`), the chain check (`refuse_off_chain`) and any write, `ship` checks the CR's own
  commits for a merge commit. A new helper (in `commands/delivery.py`, or beside `_merges` in
  `commands/crs.py`, reusing it) does the check:
  - The lower bound is the base the head sits on, as `commands/carry.py`'s `head_base(repo, d, c,
    wt, head)` already finds it (the nearest base: start base, the PR's base, the planned place,
    the default branch, the batch's other CRs' branches). So in a stack, the range is the CR's own
    commits above the CR below, and a merge commit in a lower CR's branch is that lower CR's
    refusal, not this one's.
  - When `head_base` finds none, the lower bound is `<remote>/<default branch>` (from
    `repo.config`), so a branch that merged an older tip of the default branch is still checked.
  - The check is `git rev-list --merges <lower>..<head>` (as `_merges` runs it). A non-empty list
    is a refusal.
  - When git cannot read the lower bound (no base found and `<remote>/<default branch>` cannot be
    read), `ship` refuses too, naming it: never read as "no merge commit".
- The refusal: exit 2 (`EXIT_PRECONDITION`), nothing recorded (no `ship` event, no `carry`
  event, no change to the CR's record), and no forge read. Its message names the CR, the head
  (seven characters), the merge commit(s) (seven characters, the first one at least) and the base,
  and says what to do, for instance:
  `CR-12: abc1234 holds a merge commit (def5678) above origin/main: chantier's PRs hold none;
  rebase onto main (git -C <worktree> rebase <base>), push with --force-with-lease, and ship
  again`.
  The unreadable-base form: `CR-12: cannot check abc1234 for a merge commit: origin/main cannot
  be read: fetch it and ship again`.
- No flag skips it: `--conflict` does not, and no `chantier.yaml` key exists for it. Every kind
  of CR is checked (a release CR and a fix CR included).
- The `ship` docstring says it (one more refusal next to the foreign-CR one and the chain one).
- Nothing else in the CLI changes: `gate`, `handback`, `stack --out-of-draft`, `forge-stack` and
  the carry keep their current behaviour (the carry already refuses a judged head that holds a
  merge commit: `a merge commit in <sha7>'s commits`, so a rebase that removes a merge commit is
  gated and verified again, as any carry refused).

### 2. The cards

Each card says it once, in its own words, pointing at the rule rather than repeating it.

- `skills/chantier/references/concepts.md`, rule 8 (**Git**): add the rule. A CR's branch is
  updated by rebase only (a local `git rebase <base>`, never with `--rebase-merges`, then the
  rewrite push `--force-with-lease` of the CR's own branch; or the forge's rebase action:
  `gh pr update-branch --rebase`, GitLab's `glab mr rebase`). Never a merge into it: no `git
  merge`, no `git pull` without `--rebase`, no `gh pr update-branch` without `--rebase`, never the
  forge's "Update branch" merge button. In a stack, the same on the CR below. The PRs chantier
  delivers hold no merge commit; `ship` refuses one, and the branch's Driver removes it by a
  rebase. The project's own rules still rank above the cards, but this CR adds no exception
  (Q4).
- `skills/chantier/references/concepts.md`, the `$CHANTIER` paragraph's exit 2 list (around "Exit
  codes: 0 ok, 1 usage, 2 precondition"): add `ship` of a branch holding a merge commit among the
  exit-2 cases.
- `skills/chantier/references/driver.md`:
  - "Means: rebase and push", first bullet: the rebase is the only way the branch takes its base
    (rule 8); a plain `git rebase <base>` linearizes any merge commit away; never `--rebase-merges`.
    When the forge's rebase action was used (`gh pr update-branch --rebase`, `glab mr rebase`),
    the worktree takes the PR's new head before any other step (`git -C <worktree> fetch <remote>
    <branch>`, then `git -C <worktree> rebase <remote>/<branch>`), and `ship` follows as after any
    rebase.
  - "Means: carries, conflicts and the early push": one bullet for the new refusal: `ship` refused
    `holds a merge commit`: rebase the branch onto the base the refusal names (`git -C <worktree>
    rebase <base>`), with a `conflict-resolver` on a conflict, push with `--force-with-lease`, and
    `ship` again (with `--conflict` when a conflict was resolved, by the `ship --conflict` rule).
    The pass and verdict judged at the head with the merge commit do not carry (the carry refuses
    it): the long gate and a `verifier` run again, as for any carry refused.
  - "Stack driver", "Who moves a branch" and the paragraph "Order the stack's CRs ...": each CR is
    rebased on the one under it, never merged with it (rule 8); a branch whose `ship` is refused
    `holds a merge commit` is rebased like any other move.
  - The Release driver section needs no line of its own: "Means: rebase and push" covers it.
- `skills/chantier/references/conflict-resolver.md`, "Your part": the rebase stays a rebase: never
  resolve by merging the base in (`git merge`, `git pull` without `--rebase`), never
  `--rebase-merges`; a merge commit left in the branch is the Driver's `ship` refusal.
- `skills/chantier/references/hosts/claude-code.md`, "Auto-fix events": unchanged in substance;
  it already says "never by the merge of the base branch the event asks for" and points at rule 8,
  which now states it. Change it only if the pointer's wording no longer matches rule 8.
- `skills/chantier/references/foreman.md` (the host event "merge the base branch in" is not an
  order): unchanged.

### 3. The agent files, both hosts together

The role's contract stays in the cards (AGENTS.md); the agent files carry it in their
`description:` line only, and each pair stays identical between hosts (body and the shared part of
the description):

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
- The project side in markdown-okf-schema-studio (its guideline and its git-only CI check): a CR
  of that project's batch-09.
- A refusal in `gate`, `handback`, `stack --out-of-draft` or `forge-stack`: only `ship` checks
  (Q5).
- The forge's merge method of the PR itself (the user merges by rebase, as each project says):
  unchanged.
- Any change to the Foreman's or the Chief of Staff's handling of a host's "merge the base in"
  event beyond rule 8's wording.

## Evidence

- Unit test, in-process, on a prepared repository, in
  `skills/chantier/scripts/cli/tests/test_carry_ship.py` (one parametrized test, using the
  existing `stack` fixture, `commit` and `git_at` from `test_gate_carry.py`, and the stubbed
  `delivery.read_state`), cases:
  - a CR on the default branch whose branch merged `main` (`git merge --no-ff`): `ship` exits 2,
    the message names the merge commit and says to rebase, and `events.jsonl` gains no `ship`
    event and the CR's record no `pr` / `head` change;
  - a stack CR whose branch merged the CR below's branch: refused the same way;
  - a stack CR above a CR whose own branch holds a merge commit, the upper CR rebased cleanly on
    it: the upper CR's `ship` is not refused for the lower CR's merge (the range starts at the
    CR below);
  - after `git rebase <base>` of the first case's branch: `ship` records the PR (exit 0);
  - `ship --conflict` on a branch with a merge commit: refused too (no flag skips it).
  Keep the test within `just test`'s time budget (AGENTS.md).
- The test of `carry_check` (`test_gate_carry.py`, case "d: a merge commit") stays green
  unchanged.
- Scenario (`scenario/run_scenario.py`): one check next to the CR-101 `ship` checks: a merge
  commit added to the CR's branch makes `ship` exit 2 with the rebase line and record nothing;
  the branch reset to its head before (the scenario stands for the Driver's rebase), `ship`
  records as before. Add one line for it to `scenario/README.md`'s list of `ship` refusals.
- Cards and agent files: `just check` passes (it holds the structure tests, among them the check
  that each role's agent file is the same on both hosts, `test_plugin_files.py` and
  `test_startup_manifest.py` reading the shipped files at the head under test).
- Gates by AGENTS.md: `just check` and `just eval-dry-run` in the worktree at the rebased head
  before the first push (the change is under the CLI's `src/`), and the long gate
  `just scenario (ubuntu-latest)` green at the PR's head (a change to the CLI and the cards). No
  `hooks/` or `types/` change, so no `just mod`.

## Open questions

None: the answers settle the behaviour. The forge's rebase action and how the worktree follows it
(section 2, `driver.md`) are carried from the intent's "or the forge's rebase action"; the
commands named there are the agents' means, left to the Driver to adjust if a forge's CLI names
them otherwise.
