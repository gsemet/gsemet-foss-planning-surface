# Own CR branches: rebase and force-with-lease pre-authorized

Short name: `own-branch-push`. For the running batch batch-31.

## Goal

The user's words (2026-11-23, markdown-okf-schema-studio batch-09, stack mode): a rebase of a
CR's own branch and its push with `--force-with-lease` are the normal flow of a stack (a dev
branch, not protected) and must not reach the user, in any new session. In that batch the stack
driver's `git rebase` of the CR-470 worktree onto CR-471, then its `push --force-with-lease`, were
refused by Claude Code's auto-mode classifier ("Destructive or Unwanted Actions"); the question
climbed Driver, Foreman, Chief of Staff, user, and the batch waited on it.

Three parts, forge-neutral (GitHub and GitLab; on both the forge's protected branches are the
guard against a push to a branch that must not move):

1. A durable grant, once per machine: preflight's P10 names the allow rules for a local
   `git rebase` and for `git push --force-with-lease origin chantier/*`, and the Chief of Staff
   adds them to `~/.claude/settings.json` on the user's yes.
2. The Chief of Staff answers a refused force push of a `chantier/*` branch itself; only a push
   to a protected or non-chantier branch goes to the user.
3. A Driver's prompt names the action and its scope, so the host's classifier, which judges a
   command with the conversation as context, sees that the rebase and the push are in scope.

## Decisions carried (02-answers.md)

- Q1 (B): the covered set is **any `chantier/*` branch**, not only the running batch's
  `chantier/<batch>/*`; never the default branch, never a protected branch, never a plain
  `--force`.
- Q2 (A): the durable grant is the local `git rebase` and `git push --force-with-lease origin
  chantier/*`, named by preflight's P10 and added on the user's yes, once per machine.
- Q3 (A, widened by Q1): for a covered branch the Chief of Staff answers the Foreman itself; only
  a push to a protected or non-chantier branch goes to the user.
- Q4 (A): the Driver's brief names the action and its scope.
- Q5 (A): specified for the running batch batch-31.
- Q6 (A): a host refusal that remains (the host refuses the Chief of Staff's own push of a
  covered branch) keeps today's single question to the user, and the push goes on their yes.
- Q7 (A): a `chantier/*` branch that `handoff` ties to no CR of the batch stays a hard refusal
  with no question to the user, as today.

## What changes

### 1. The durable grant: P10 names the rebase rules

The push rules already exist: `git push --force-with-lease -u origin chantier/*`, its `git -C *`
form and the two steering-route forms are in P10's samples and in the host card's tables (they
match the Q2 command; the Drivers' form carries `-u`). What is missing is the local rebase.

- `skills/chantier/scripts/cli/src/chantier/commands/allow_samples.py`, `SAMPLES`: add, in the
  capability `batch`, forge `any`, right after the six `git push` samples (before the `dev`
  rows), the rebase forms the cards make the agents write, each tied to its rule:
  - `git rebase origin/main` -> `git rebase *`
  - `git -C {_TREE} rebase origin/main` -> `git -C * rebase *`
  - `git -C {_TREE} rebase --onto chantier/batch-01/cr-100-base {_SHA}` -> `git -C * rebase *`
    (the stack driver's and a dropped CR's `rebase --onto`, `driver.md` lines ~944, ~1296)
  - `git -C {_TREE} rebase --continue` -> `git -C * rebase *` (the conflict-resolver's step)
  - `git -C {_TREE} rebase --abort` -> `git -C * rebase *`
  The rules hold no branch: a rebase is local and rewrites only the local branch checked out in
  that worktree; nothing reaches the forge until a push, which the push rules scope to
  `chantier/*`. `RECOMMENDED_ALLOW` and the pasteable block then hold
  `Bash(git rebase *)`, `PowerShell(git rebase *)`, `Bash(git -C * rebase *)`,
  `PowerShell(git -C * rebase *)`, in that place.
- `skills/chantier/references/hosts/claude-code.md`, "Allow rules":
  - the rule table: two rows after the `git -C * push --force-with-lease=…` row:
    `Bash(git rebase *)` and `PowerShell(…)` (use: a Driver's rebase onto its base, the stack
    driver's restack, a conflict-resolver's `--continue`; risk: a local rebase of whatever branch
    is checked out, in the current folder; nothing is pushed by it; mark: documented (rule form);
    the classifier on a subagent's matching command **unproved**: refused without a rule in
    markdown-okf-schema-studio batch-09, 2026-11-23, with "Destructive or Unwanted Actions"), and
    `Bash(git -C * rebase *)` and `PowerShell(…)` (the same with `git -C <worktree>`; risk: as
    above in any repository the `-C` path names, and the middle `*` matches any text before
    ` rebase `, so a command that holds the word `rebase` as a later argument matches too; same
    mark);
  - the pasteable JSON block: the four rules, in the same place;
  - "Capabilities and their commands", row "Every batch": the commands column names the rebase
    forms (`git [-C <worktree>] rebase <base>`, `--onto`, `--continue`, `--abort`), the rules
    column lists `git rebase *` and `git -C * rebase *` right after the six push rules (the test
    compares this column with `SAMPLES`), the trial column adds nothing (a rebase has no harmless
    remote form), and the mark column names the rebase refusal of 2026-11-23.
  - "Auto mode": one bullet line recording the 2026-11-23 refusal of the stack driver's rebase and
    force-with-lease (no rule set for the rebase), and that whether the classifier passes a
    subagent's command its allow rule matches stays **unproved** (batch-23's case stands).
- `skills/chantier/references/chief-of-staff.md`, "The allow rules (P10, Claude Code)":
  - "The question": the list names the rebase rules with their risk like any other rule P10 names;
    the question says once that the grant is "rebase and force-with-lease of chantier's own
    branches, once per machine".
  - "On a no", the "every batch" sentence: also a Driver's rebase may stop on the host's prompt or
    classifier, and goes up as a refusal (concepts rule 7).
- No change to `commands/permissions.py`'s logic: it counts the new samples like the others (a
  missing rebase rule is one more command in P10's `every batch:` warn line; never a failure).
- Copilot: P10 does not run there (unchanged); nothing is added to `hosts/copilot.md`.

### 2. The Chief of Staff answers a covered push; the user gets only the rest

The ladder of `foreman.md`, "A Driver's refused force push", already lets the Foreman, then the
Chief of Staff, judge and run a legitimate push without the user. Changes:

- `skills/chantier/references/foreman.md`, "A Driver's refused force push", step 2, the check:
  - The branch is covered when it matches `chantier/*`, is not the project's default branch and
    the push is `--force-with-lease` (never a plain `--force`). It replaces "the branch is
    `chantier/<batch>/<cr>-<slug>`": a CR branch whose name holds another batch (a CR carried from
    an earlier batch keeps its branch) is covered.
  - The CR is still read from the branch's last segment (`cr-115-…` is `CR-115`) and tied by
    `$CHANTIER handoff <cr>`, whose `worktree: … branch <branch>` line must give exactly the
    branch; the judgement (base an ancestor, the remote's commits kept, the gate check and its
    skips) is unchanged.
  - A **non-chantier branch or the default branch** is no longer a hard refusal with no user
    question: push nothing and send it to the user: the Foreman by `$CHANTIER asks "<the CR,
    number and slug>: push <branch> <expected> <local>: not a chantier branch"` (the step 5
    channel, relayed by the Chief of Staff); in direct mode the Chief of Staff asks it directly.
    The text "the user's yes must not push such a branch" (chief-of-staff.md) goes.
  - A `chantier/*` branch that `handoff` ties to no CR of the batch (Q7): the hard refusal of
    today, unchanged: push nothing, take the CR back with `push: push refused <branch>: not a
    branch of this batch`, no hop and no user question.
- **A protected branch.** No session reads the forge's branch protection (no `gh api` or `glab
  api` rule is added). A push the forge rejects as protected (git's remote rejection, for instance
  `protected branch hook declined` on GitHub, `You are not allowed to force push code to a
  protected branch` on GitLab) is not a failed lease: the session that ran it records
  `$CHANTIER note <cr> "push rejected by the forge <branch>: <git's text>"`, never retries, and it
  goes to the user: the Foreman sends `[foreman→chief-of-staff] push failed <branch> <git's
  text>`, the Chief of Staff tells the user at once (as a failed push today) with git's text and
  that the branch is protected on the forge. `foreman.md` step 7 and `chief-of-staff.md`'s "A
  failed lease" bullet name this case beside the failed lease.
- `skills/chantier/references/chief-of-staff.md`, "A refused force push":
  - the opening sentence: a push of a covered branch (`chantier/*`, not the default, not
    protected, with a lease) is answered by you, never a question for the user; only a
    non-chantier or default branch, a forge's protected-branch rejection, a doubt of the
    judgement and a host refusal of your own push (Q6) reach the user;
  - "A hard check that fails": a branch `handoff` ties to no CR of the batch keeps today's
    refusal (Q7); the non-chantier and default-branch case becomes the user question
    above (the CR, the branch, the shas, the exact command you would run on a yes); on the
    user's go, `$CHANTIER note <cr> "push on the user's go at <local sha7> for <branch>"`, then
    the route form once (the host may ask the user itself: no rule covers it); on a no,
    `push refused <branch>: <the user's reason>`;
  - "Not legitimate" (the checks pass, the judgement disagrees) still goes to the user, unchanged:
    it is a doubt on the work, not an authorization;
  - "The host refuses your push" (Q6): unchanged: record the `refused:` note, ask the user the
    one question it names today, and on the yes run that command once, unchanged. The section
    says that this is the one case where a covered push reaches the user: the host left no other
    route.
  - The "On the yes" sentence of "The allow rules" ("the user is asked only when the host refuses
    you too") stays, as Q6 keeps it true.
- `skills/chantier/references/driver.md`, "Means: a force push the host refuses": the list of
  "any other `push refused`" names the new reasons (`not a chantier branch`, the user's no) and
  the forge's protected-branch rejection (handed back `blocked refused <git's text>`, to the user);
  `not a branch of this batch` keeps its meaning (a `chantier/*` branch tied to no CR, Q7).
- `skills/chantier/references/concepts.md`, rule 8: one sentence: rebasing a CR's own branch and
  pushing it with `--force-with-lease` (any `chantier/*` branch, never the default branch, never a
  protected one, never a plain `--force`) is chantier's normal flow, pre-authorized; only a push
  outside it reaches the user, and a push the host refuses even to the Chief of Staff (one
  question).

### 3. The Driver's prompt names the action and its scope

- `skills/chantier/references/concepts.md`, "The prompt" template: a new line, after `writes:`
  and before `Steering:`:
  `Rewrites: <the scope>   (a Driver's prompt, where "A Driver's prompt" says so)`.
- "A Driver's prompt" table: a new last column `Rewrites:` with `own branch` for `cr-driver` and
  `release-driver`, `batch branches` for `stack-driver`, `none` for `qa-driver` (it pushes
  nothing). The bullets under the table say the line is printed where the column is not `none`.
  The CLI reads the table (it knows no role).
- `skills/chantier/scripts/cli/src/chantier/driver_prompt.py`: `DriverRow` gains the column's
  value; `driver_prompt_lines` prints, where it is not `none`, the line between `writes:` and
  `Steering:`, filled by the CLI:
  - `own branch`: `  Rewrites: git -C <worktree> rebase onto your base, and git -C <worktree>
    push --force-with-lease -u <remote> <branch>, one command, on your own CR branch only
    (<branch>): chantier's normal flow, pre-authorized by the user (2026-11-23); never the
    default branch, a protected branch, another branch, or a plain --force.` with `<worktree>`
    and `<branch>` taken from the `worktree: <path> branch <branch>` line the command printed
    (left as `<…>` when it has none yet), and `<remote>` the project's remote as P10 fills it
    (`remote` in the project's configuration, else `origin`, else the first remote: the logic of
    `commands/permissions.py` near line 305, factored into one function both use).
  - `batch branches`: the same text for "each CR branch of the stack listed above, one command
    per branch (chantier/*)".
  The line's wording is the card's (concepts.md holds the two texts; the CLI copies them, filling
  the placeholders), so a later wording change is a card change.
- `driver.md`, "Means: rebase and push": one sentence: the `Rewrites:` line of your prompt is the
  scope; a rebase or push outside it is not yours.
- `foreman.md` and `chief-of-staff.md`: nothing new (they copy the skeleton whole, as today).

## Out of scope

- Any rule for a plain `--force`, a push to the default branch, a tag, a merge or a release.
- A read of the forge's branch protection by any session or by the CLI.
- An `Agent(...)` rule or any change to how a Driver is started in auto mode.
- The Copilot host's permissions (P10 does not run there); the brief's line is host-neutral and
  ships to both.
- The workers' prompts (the conflict-resolver's `rebase --continue` is covered by the rule, not by
  a prompt line).
- Writing to `~/.claude/settings.json` without the user's yes (unchanged: the one write, on the
  yes, of the rules P10 named).

## Host and default matrix

- Claude Code, no rebase rule in the settings: P10 warns, naming `Bash(git rebase *)` and
  `Bash(git -C * rebase *)` (plus the `PowerShell` forms on Windows) in its `every batch:` line;
  preflight still passes.
- Claude Code, the recommended block in the settings (`filled_allow()`): P10 ok.
- Claude Code, a user deny on `git rebase*`: P10's `denied:` part names it.
- Copilot: no P10; the Driver's prompt still holds the `Rewrites:` line.
- Foreman mode and direct mode: the check and its answers as section 2 says, in both.
- Remote: `origin` by default; a configured `remote` fills the `Rewrites:` line and P10 alike.

## Evidence

Checks (`just test`, in-process, reading the shipped files at the head under test):

- `tests/test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks`
  passes unchanged in its body: it reads the shipped `hosts/claude-code.md`, and its block, its
  capabilities row and each new sample's match against its rule (Bash and PowerShell) hold.
- `tests/test_cli_runs.py::test_preflight_warns_on_missing_allow_rules_and_never_fails_on_them`:
  add asserts that the P10 warn line names `git -C * rebase *`, that a settings file holding the
  push rules only still lists `add Bash(git rebase *)`, and that a deny of `Bash(git rebase*)` is
  reported under `denied:`.
- `tests/test_driver_prompt.py`: the table test checks the new column's values (`none` only for
  `qa-driver`); the skeleton test (all four Drivers) asserts a `  Rewrites: ` line for change,
  release and stack, placed between `writes:` (or the last middle line) and `Steering:`, naming
  the branch the `worktree:` line printed (change, release), `--force-with-lease` and `never the
  default branch`, and none for qa; `block[-1]` stays `Note:` and `block[5]` stays the CLI line.
- A card text check, reading the shipped cards: `foreman.md`'s "A Driver's refused force push"
  holds `chantier/*` as the covered set and no longer `the user's yes must not push such a
  branch` in `chief-of-staff.md` (one parametrized test beside the existing card checks).

Scenario (`just scenario`, the long gate, required: the CR changes the CLI and the cards):

- `scenario/run_scenario.py`, the P10 step (~line 1076): the warn line also names
  `git -C * rebase *`; with `filled_allow()` written in the temporary home, `P10 ok` as today.
- The `take` step of a CR Driver: the printed skeleton holds the `Rewrites:` line with the CR's
  branch.
- `scenario/README.md`, the P10 paragraph (~line 83): names the rebase rules.

Before the first push: `just check`, and `just eval-dry-run` (the change is under the CLI's
`src/`). Windows coverage per AGENTS.md (the top CR of the batch runs the long gate locally).

## Open questions

None: Q6 and Q7 closed the two points the first version left open.
