# Own CR branches: rebase and force-with-lease pre-authorized

Short name: `own-branch-push`. For the running batch batch-31, built on CR-465
(`agents-update-a-cr-branch-by-rebase-only`, branch
`chantier/batch-31/cr-465-agents-update-a-cr-branch-by-rebase-only`): this CR's branch is rebased
onto CR-465's, and it touches the same rebase passages of the cards.

## Goal

The user's words (2026-11-23, markdown-okf-schema-studio batch-09, stack mode): a rebase of a
CR's own branch and its push with `--force-with-lease` are the normal flow of a stack (a dev
branch, not protected) and must not reach the user, in any new session. In that batch the stack
driver's `git rebase` of the CR-470 worktree onto CR-471, then its `push --force-with-lease`, were
refused by Claude Code's auto-mode classifier ("Destructive or Unwanted Actions"); the question
climbed Driver, Foreman, Chief of Staff, user, and the batch waited on it.

Three parts, forge-neutral (GitHub and GitLab; on both the forge's protected branches are the
guard against a push to a branch that must not move):

1. A durable grant, once per machine: preflight's P10 names narrow allow rules for the local
   rebase forms the cards use and for `git push --force-with-lease origin chantier/*`, and the
   Chief of Staff adds them to `~/.claude/settings.json` on the user's yes.
2. The steering sessions answer a refused rebase or force push of a covered branch themselves; a
   push of any other branch is never run, and the user is only told of it.
3. A Driver's prompt names the action and its scope, so the host's classifier, which judges a
   command with the conversation as context, may see that the rebase and the push are in scope
   (its effect is unproved; a trial is named below).

## Decisions carried (02-answers.md)

- Q1 (B): the covered set is **any `chantier/*` branch**, not only the running batch's
  `chantier/<batch>/*`; never the default branch, never a protected branch, never a plain
  `--force`.
- Q2 (A): the durable grant is the local `git rebase` and `git push --force-with-lease origin
  chantier/*`, named by preflight's P10 and added on the user's yes, once per machine. Q10 sets
  the rebase rules' width.
- Q3 (A, widened by Q1, its user part replaced by Q9): for a covered branch the Chief of Staff
  answers the Foreman itself.
- Q4 (A): the Driver's brief names the action and its scope.
- Q5 (A): specified for the running batch batch-31.
- Q6 (A): a host refusal that remains (the host refuses the Chief of Staff's own push of a
  covered branch) keeps today's single question to the user, and the push goes on their yes.
- Q7 (A): a `chantier/*` branch that `handoff` ties to no CR of the batch stays a hard refusal
  with no question to the user, as today.
- Q8 (A): a refused rebase: the steering session runs the same rebase in the Driver's worktree
  (`git -C <worktree> rebase <base>`), under the same check as a push (the branch tied by
  `handoff`); on a conflict it hands the work back to a new Driver; the user is asked only if the
  host refuses the steering session too.
- Q9 (A): a force push of a non-`chantier/*` branch or of the default branch: nothing is pushed;
  the user is told, as information, which branch was asked and by which CR; a yes does not push
  it (today's guard stays). It replaces Q3's "goes to the user" for such a push.
- Q10 (A): narrow rebase rules that name the base: `git -C * rebase origin/*`,
  `git -C * rebase --onto chantier/* *`, `git -C * rebase --continue`, `git -C * rebase --abort`,
  and the plain forms; the cards forbid `--exec` / `-x`; the risk column names what remains.
- The critic's other findings: the classifier effect is marked unproved with a trial; the
  Driver's line says "chantier's normal flow, pre-authorized by the playbook" (no user, no date);
  CR-465 is the base and its rebase forms are checked against the rules; the two passages that
  still say "asked only when the host refuses you too" are updated and name the rebase; the
  GitLab protected-branch text is marked unproved.

## What changes

### 1. The durable grant: P10 names the rebase rules

The push rules already exist: `git push --force-with-lease -u origin chantier/*`, its `git -C *`
form and the two steering-route forms are in P10's samples and in the host card (the Drivers'
form carries `-u`). What is missing is the rebase.

**The forms checked against the rules.** Every rebase command the cards write, with CR-465's
passages, and the rule that covers it (`<base>` is what `take` / `handoff` print: `origin/<default
branch>` for a CR on the default branch, the bare `chantier/…` branch of the CR under it in a
series or a stack; `facts.py`, `_ref` and `_base_of`):

| Command (card) | Rule |
| --- | --- |
| `git -C <worktree> rebase origin/main` (`driver.md` "Means: rebase and push"; CR-465's rebase onto the base) | `git -C * rebase origin/*` |
| `git -C <worktree> rebase origin/<branch>` (CR-465's GitLab fold: onto the remote branch first) | `git -C * rebase origin/*` |
| `git -C <worktree> rebase chantier/<batch>/<cr>-<slug>` (a stacked or dependent CR's base; the batch-09 refusal) | `git -C * rebase chantier/*` |
| `git -C <worktree> rebase --onto chantier/… <sha or branch>` (`driver.md` ~944, ~1296) | `git -C * rebase --onto chantier/* *` |
| `git -C <worktree> rebase --onto origin/<default branch> <branch>` (`driver.md` ~1295, the CR at the bottom after a drop) | `git -C * rebase --onto origin/* *` |
| `git -C <worktree> rebase --continue` (`conflict-resolver.md`) | `git -C * rebase --continue` |
| `git -C <worktree> rebase --abort` (`driver.md` ~796, ~1122) | `git -C * rebase --abort` |
| `git rebase origin/<branch>` (`chief-of-staff.md` ~506, the surface's checkout) | `git rebase origin/*` |

Q10's four named forms leave out two bases the cards use (`rebase chantier/…` and `--onto
origin/…`); both name the base as Q10 asks, and the first is the very command refused in
batch-09, so they are added in the same shape. Each `git -C *` rule has its plain form
(`git rebase origin/*`, `git rebase chantier/*`, `git rebase --onto chantier/* *`,
`git rebase --onto origin/* *`, `git rebase --continue`, `git rebase --abort`).

- `skills/chantier/scripts/cli/src/chantier/commands/allow_samples.py`, `SAMPLES`: in capability
  `batch`, forge `any`, right after the six `git push` samples, one sample per row of the table
  above, filled with `_TREE`, `_BRANCH` and `_SHA`, plus one sample per plain form, tied to its
  rule. `RECOMMENDED_ALLOW` and the pasteable block then hold the twelve rules, each with its
  `Bash(…)` and `PowerShell(…)` forms, in that place.
- `skills/chantier/scripts/cli/src/chantier/commands/permissions.py`, `_gap` (line ~195): the
  remote fill also replaces ` origin/` with ` <remote>/` in the command and the rule, beside
  ` origin `, so the rebase rules carry the project's remote as the push rules do.
- `skills/chantier/references/hosts/claude-code.md`, "Allow rules":
  - the rule table: rows after the `git -C * push --force-with-lease=…` row, one per rule pair
    (`Bash(…)` and `PowerShell(…)`). Use: as in the table above. Risk: a local rebase of the
    branch checked out (nothing is pushed by it) onto a branch of the remote or a `chantier/`
    branch; what remains: the trailing `*` matches any further text, so a flag added after the
    base passes too (`--exec` / `-x` runs any command: the cards forbid it, the rule does not
    enforce it); for the `git -C *` forms, any repository the path names, and the middle `*`
    matches any text before ` rebase `, so a command that holds the word `rebase` as a later
    argument matches too. Mark: documented (rule form); the classifier on a subagent's matching
    command **unproved** (the batch-23 case stands); refused with no rule set in
    markdown-okf-schema-studio batch-09, 2026-11-23, "Destructive or Unwanted Actions".
  - the pasteable JSON block: the new rules, in the same place.
  - "Capabilities and their commands", row "Every batch": the commands column names the rebase
    forms, the rules column lists the six rebase rules right after the six push rules (the test
    compares this column with `SAMPLES`), the trial column adds nothing (a rebase has no harmless
    remote form), the mark column names the 2026-11-23 refusal.
  - "Auto mode": one bullet records the 2026-11-23 refusal of the stack driver's rebase and
    force-with-lease, and the trial of part 3.
  - The start alert (the bullet "The alert the Chief of Staff gives, once, at its first turn",
    ~line 500): it names the rebase beside the force push ("some rebases and force pushes"), and
    its last sentence becomes: a refused one goes to the Foreman, then to the Chief of Staff, who
    each run a legitimate one on the Driver's own branch without asking you; you are asked only
    if the host refuses the Chief of Staff too, or when a judgement finds a push not legitimate;
    a push of a branch that is not chantier's is never run, you are told of it.
- `skills/chantier/references/chief-of-staff.md`, "The allow rules (P10, Claude Code)":
  - "The question" lists the rebase rules with their risk like any other rule P10 names, and
    says once that the grant is "rebase and force-with-lease of chantier's own branches, once
    per machine".
  - "On the yes": the sentence on a refused push names the rebase too ("a refused rebase or
    force push climbs…; the user is asked only when the host refuses you too").
  - "On a no", the "every batch" sentence: a Driver's rebase may stop on the host too, and
    climbs as section 2 says.
- Copilot: P10 does not run there (unchanged); nothing is added to `hosts/copilot.md`.

### 2. The ladder: rebase and push of a covered branch, nothing else pushed

The covered branch: it matches `chantier/*`, it is not the project's default branch, and the push
is `--force-with-lease` (never a plain `--force`). It replaces "the branch is
`chantier/<batch>/<cr>-<slug>`": a CR branch whose name holds another batch (a CR carried from an
earlier batch keeps its branch) is covered. The CR is still read from the branch's last segment
(`cr-115-…` is `CR-115`) and tied by `$CHANTIER handoff <cr>`, whose `worktree: … branch
<branch>` line must give exactly the branch.

**A. The force push** (`skills/chantier/references/foreman.md`, "A Driver's refused force push"):

- Step 2, the check: the covered-branch test above. Its judgement (base an ancestor, the
  remote's commits kept, the gate check and its skips) is unchanged.
- A covered branch that `handoff` ties to no CR of the batch (Q7): today's hard refusal,
  unchanged: push nothing, take the CR back with `push: push refused <branch>: not a branch of
  this batch`, no hop, no user question.
- A non-`chantier/*` branch or the default branch (Q9): push nothing, ever, at any step; take the
  CR back with `push: push refused <branch>: not a chantier branch`, and send
  `[foreman→chief-of-staff] push refused <branch>: not a chantier branch (<cr>)`, which the Chief
  of Staff tells the user as information (the report's shape, no question, no tip, nothing to
  answer): the branch asked and the CR that asked it. In direct mode the Chief of Staff does both.
  A user's yes does not push it.
- A protected branch: no session reads the forge's branch protection (no `gh api` or `glab api`
  rule is added). A push the forge rejects as protected (git's remote rejection: on GitHub
  `protected branch hook declined`; on GitLab `You are not allowed to force push code to a
  protected branch`, marked **unproved**) is not a failed lease: the session that ran it records
  `$CHANTIER note <cr> "push rejected by the forge <branch>: <git's text>"`, never retries; the
  Foreman sends `[foreman→chief-of-staff] push failed <branch> <git's text>`, and the Chief of
  Staff tells the user at once, with git's text and that the branch is protected on the forge.
  Step 7 names this case beside the failed lease.
- `skills/chantier/references/chief-of-staff.md`, "A refused force push":
  - the opening sentence: a push of a covered branch is answered by you, never a question for the
    user; the user is told of a non-chantier or default branch (information only) and of a
    forge's protected-branch rejection, and asked only on a doubt of the judgement or a host
    refusal of your own push (Q6);
  - "A hard check that fails": a branch tied to no CR keeps today's refusal (Q7); a
    non-chantier or default branch: push nothing, answer `push refused <branch>: not a chantier
    branch`, tell the user as information; "the user's yes must not push such a branch" stays;
  - "Not legitimate" (the checks pass, the judgement disagrees) still goes to the user, unchanged;
  - "The host refuses your push" (Q6): unchanged (the `refused:` note, the one question, the
    command run once on the yes);
  - the "Nothing is sent to yourself" bullet of direct mode (~line 1894): "A Driver's refused
    rebase or force push is judged and run by you, as above, without asking the user, and asked
    to the user only when the host refuses you too; a push of a branch that is not chantier's is
    never run, the user is told of it".
- `skills/chantier/references/driver.md`, "Means: a force push the host refuses": the opening
  names the rebase ladder (B); the list of "any other `push refused`" names `not a chantier
  branch` and the forge's protected-branch rejection (handed back `blocked refused <text>`).

**B. The rebase (Q8).** The same ladder, for a rebase the host refuses a Driver:

- `driver.md`, a new section "Means: a rebase the host refuses", beside the push's: with the
  work committed, (1) `$CHANTIER note <cr> "refused: <the exact command> -> <the host's exact
  text>"`; (2) the `next after rebase` note (the steps left, as for a push); (3)
  `$CHANTIER handback <cr> blocked waits: rebase <branch> <base>` (the `base` that `take` /
  `handoff` printed); (4) send `[driver <cr>→foreman] rebase <branch> <base>` and end. The stack
  driver sends one line per refused branch, as for its pushes. The fresh Driver reads the answer
  in its `take` note: `rebased <branch> onto <base> at <sha7>`: push (`--force-with-lease`) and go
  on; `rebase conflict <branch> onto <base>`: the rebase is stopped at the conflict in the
  worktree; start a `conflict-resolver` on it; `rebase refused <branch>: <text>`: `handback
  blocked refused <text>`.
- `foreman.md`, a new section "A Driver's refused rebase", after the push's:
  - The check, a hard refusal: the branch is covered and `handoff <cr>`'s `worktree: … branch`
    line gives exactly it, and the line's `<base>` is the `base` that `handoff` prints. Else
    rebase nothing: take the CR back with `rebase: rebase refused <branch>: <the reason>`.
  - The rule first (Claude Code), as step 3 of the push: the P10 `every batch:` line names in an
    `(add …)` part, or under `denied:`, the rebase rule of the form you will run: rebase nothing,
    note `rebase not tried: rule missing` and send the line up.
  - Run, one command: `git -C <worktree> rebase <base>` in the Driver's worktree, the worktree
    clean (a clean `git status`), after `git -C <worktree> fetch <remote>`. A clean rebase: note
    `rebased <branch> onto <base> at <sha7>` and take the CR back with that answer. A conflict:
    leave the rebase stopped (no `--abort`, no resolution), take the CR back with `rebase:
    rebase conflict <branch> onto <base>`. The steering session resolves nothing.
  - The host refuses you: `refused:` note, then `[foreman→chief-of-staff] rebase <branch>
    <base>`; wait for the answer; retry nothing, no other form.
  - This is a named exception to the Foreman's "no `git rebase`" (`foreman.md` ~line 311): only
    this command, only in a Driver's worktree, only on such a line.
- `chief-of-staff.md`, "A refused rebase", beside "A refused force push": on the Foreman's line
  (or, in direct mode, the Driver's), the same check and the same run; answers to the Foreman
  as above; the host refuses you: the `refused:` note, then one question to the user naming the
  CR, the branch, the base, each step's refusal (exact command, exact text) and the exact command
  you will run on a yes; on the yes, run it once, unchanged; on a no or a second refusal,
  `rebase refused <branch>: <text>`.
- `skills/chantier/references/routing.md`: the new lines `[driver <cr>→foreman] rebase <branch>
  <base>` and `[foreman→chief-of-staff] rebase <branch> <base>`, and the informational
  `push refused <branch>: not a chantier branch (<cr>)`.

**C. The ground rules.**

- `skills/chantier/references/concepts.md`, rule 8: rebasing a CR's own branch and pushing it with
  `--force-with-lease` (any `chantier/*` branch, never the default branch, never a protected one,
  never a plain `--force`) is chantier's normal flow, pre-authorized by the playbook; a refused one
  climbs the steering ladder; a push of another branch is never run. Never `git rebase --exec` or
  `-x`.
- `driver.md`, "Means: rebase and push", and `conflict-resolver.md`, "Your part": one sentence
  each: never `--exec` / `-x`.

### 3. The Driver's prompt names the action and its scope

- `concepts.md`, "The prompt" template: a new line after `writes:` and before `Steering:`:
  `Rewrites: <the scope>   (a Driver's prompt, where "A Driver's prompt" says so)`.
- "A Driver's prompt" table: a new last column `Rewrites:` with `own branch` for `cr-driver` and
  `release-driver`, `batch branches` for `stack-driver`, `none` for `qa-driver` (it pushes
  nothing). The bullets say the line is printed where the column is not `none`, and hold the two
  texts the CLI copies:
  - `own branch`: `Rewrites: git -C <worktree> rebase <base>, then git -C <worktree> push
    --force-with-lease -u <remote> <branch>, one command each, on your own CR branch only
    (<branch>): chantier's normal flow, pre-authorized by the playbook; never the default branch,
    a protected branch, another branch, a plain --force or a rebase --exec.`
  - `batch branches`: the same for "each CR branch of the stack listed above (chantier/*), one
    command per branch".
- `skills/chantier/scripts/cli/src/chantier/driver_prompt.py`: `DriverRow` gains the column's
  value; `driver_prompt_lines` prints the line, where it is not `none`, between `writes:` and
  `Steering:`, filled from the `worktree: <path> branch <branch> base <base>` line the command
  printed (left as `<…>` when it has none yet), `<remote>` being the project's remote as P10 fills
  it (the logic of `commands/permissions.py` ~line 305, factored into one function both use).
- `driver.md`, "Means: rebase and push": the `Rewrites:` line of your prompt is the scope; a
  rebase or push outside it is not yours.
- Its effect on the classifier is **unproved**. Trial, recorded in `hosts/claude-code.md`, "Auto
  mode", with its date and exact text: the next batch in auto mode where a Driver, with the
  `Rewrites:` line and the rules set, rebases onto a `chantier/` base and force-pushes; accepted or
  refused.

## Out of scope

- Any rule for a plain `--force`, a push to the default branch, a tag, a merge or a release.
- A read of the forge's branch protection by any session or by the CLI.
- An `Agent(...)` rule or any change to how a Driver is started in auto mode.
- The Copilot host's permissions (P10 does not run there); the prompt's line is host-neutral.
- The workers' prompts (the conflict-resolver's `rebase --continue` is covered by its rule).
- Resolving a conflict in a steering session (Q8: handed back to a new Driver).
- Writing to `~/.claude/settings.json` without the user's yes (unchanged).
- CR-465's own content (the merge-commit refusal of `ship`, the forge's rebase action).

## Host and default matrix

- Claude Code, no rebase rule in the settings: P10 warns, naming the rebase rules (plus the
  `PowerShell` forms on Windows) in its `every batch:` line; preflight still passes.
- Claude Code, the recommended block in the settings (`filled_allow()`): P10 ok.
- Claude Code, a user deny on `git -C * rebase*`: P10's `denied:` part names it.
- Copilot: no P10; the Driver's prompt still holds the `Rewrites:` line; the ladder's cards apply.
- Foreman mode and direct mode: the checks and answers of section 2, in both.
- Remote: `origin` by default; a configured `remote` fills the rules (` origin ` and ` origin/`),
  P10's commands and the `Rewrites:` line alike.

## Evidence

Checks (`just test`, in-process, reading the shipped files at the head under test):

- `tests/test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks`,
  unchanged in its body: it reads the shipped `hosts/claude-code.md`; its block, its capabilities
  row and each new sample's match against its rule (Bash and PowerShell) hold.
- `tests/test_cli_runs.py::test_preflight_warns_on_missing_allow_rules_and_never_fails_on_them`:
  add asserts that the warn line names `git -C * rebase chantier/*`; that a settings file holding
  the push rules only still lists `add Bash(git -C * rebase origin/*)`; that a deny of
  `Bash(git -C * rebase*)` shows under `denied:`; and, with a `remote: upstream` configuration,
  that the line names `git -C * rebase upstream/*`.
- A parametrized matching test (beside it): each command of the table of section 1 is matched by
  its rule, and `git -C /w rebase main`, `git -C /w rebase --root`, `git rebase -i origin/main`
  are not matched by any of the recommended rules (the narrow forms hold).
- `tests/test_driver_prompt.py`: the table test checks the new column (`none` only for
  `qa-driver`); the skeleton test asserts a `  Rewrites: ` line for change, release and stack,
  between `writes:` (or the last middle line) and `Steering:`, naming the branch the `worktree:`
  line printed (change, release), `--force-with-lease`, `pre-authorized by the playbook` and
  `never the default branch`, and none for qa; `block[-1]` stays `Note:`, `block[5]` the CLI line.
- A card text check reading the shipped cards: `foreman.md` holds the sections "A Driver's
  refused force push" and "A Driver's refused rebase"; neither `chief-of-staff.md` nor
  `hosts/claude-code.md` holds a sentence that says the user is asked only when both are refused
  without naming the rebase (the two passages fixed).

Scenario (`just scenario`, the long gate, required: the CR changes the CLI and the cards):

- `scenario/run_scenario.py`, the P10 step (~line 1076): the warn line also names
  `git -C * rebase chantier/*`; with `filled_allow()` in the temporary home, `P10 ok` as today.
- The `take` step of a CR Driver: the printed skeleton holds the `Rewrites:` line with the CR's
  branch.
- `scenario/README.md`, the P10 paragraph (~line 83): names the rebase rules.

Before the first push: rebased onto CR-465's branch (or `origin/main` once it merged), `just
check` and `just eval-dry-run` (the change is under the CLI's `src/`). Windows coverage per
AGENTS.md (the top CR of the batch runs the long gate locally).

## Open questions

None.
