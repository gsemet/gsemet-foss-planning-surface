# Permissions per capability: each capability's commands known, tried and warned before the go

## Goal

chantier must deliver a stack in many kinds of runs: a native stack made and rebuilt at night, a
release run on the user's grant, a fix merged on a grant, force pushes after every rebase. Each
capability chantier offers works end to end under the host's permission check, or the user knows
before the go why it may stop. The user (2026-11-14): "chantier doit être capable et flexible
pour livrer une stack dans une variété de cas, et donc il faut donner au skill et au CLI les
outils et instructions pour qu'il le fasse. Le classifier doit empêcher des cas non prévus, mais
si chantier prévoit des stacks dynamiques, des releases autonomes, … il faut que tout fonctionne
bien."

So:

- one table of each capability and the exact commands its agents run, in the host reference and
  in P10's samples;
- preflight checks the allow rules of the capabilities this batch will use (not one fixed set),
  and the Chief of Staff offers to add exactly those; the release rules only when the user grants
  a release to run on its own;
- before the go, one harmless trial per used capability, in the session's permission mode, its
  result recorded;
- the forge's capabilities probed before the go (the stacks API, the default branch's rules);
- a missing rule or a forge problem is a **strong warning**, never a failure, and it explains why
  the capability may stop: the auto-mode classifier judges each command at run time, and in a
  remote session nobody may be there to answer a prompt;
- every refusal recorded with its exact command and text, so the next table fixes it.

Why (batch-17): the Drivers' force pushes (`git -C <worktree> push --force-with-lease …`) were
refused; P10 had warned, nobody acted. CR-238 makes the Chief of Staff ask and add the missing
rules, but from one fixed set, and it keeps `gh release create` out of it: a release granted to run
on its own (`order grant … releases=N`) would stop at the host's prompt at night.

## Ordering, and what this CR changes on top of CR-238

This CR joins batch-17's stack, after CR-238 (allow-rules-ask, PR #176, not merged): its
`depends.json` is `{"after": ["allow-rules-ask"]}` (the Chief of Staff writes it; this spec
writes nothing else). It lands on CR-238's head and on CR-221's reworked CLI, and meets the same
targets: `ruff`, `mypy --strict`, files at most 400 lines, functions at most 50 lines.

The file names and line numbers below are those of CR-238's head (`3a96b35`, worktree
`chantier.worktrees/batch-17-CR-238`). The Driver finds them again once CR-238 is merged.

What CR-238 settled and this CR **keeps**:

- the Chief of Staff's question "add these rules to `~/.claude/settings.json`?", the write on the
  yes (merge, never replace or remove), the refused-edit fallback ("Allow rules to add" command
  line), and the single settings-write exception of `AGENTS.md`;
- P10 warn-only: it never fails preflight and never blocks the go. `chief-of-staff.md`'s "warns
  and never fails" (step 1, line 391) stays. The critic's call to make a missing rule a failure is
  dropped by the user (answer 2): this CR does **not** reverse CR-238 there;
- the release rules stay out of the **base** recommended set and out of the pasteable JSON block.

What this CR **changes** on top of CR-238:

- P10's one fixed sample set becomes sets per capability; preflight checks only the capabilities
  the batch will use, and names those it did not check.
- The release rules come back, but only in the capability "a release on its own", offered only
  when the user grants it. This is a partial reversal of CR-238's "no `gh release create` rule, by
  design" (CR-238 spec, section 2, the sentence under the table; `hosts/claude-code.md` lines
  200–202): the sentence becomes "no release rule in the base set, by design; offered only with a
  grant". An unplanned release still meets the host's prompt, as CR-238 wanted.
- The P10 warning becomes stronger: its text explains the classifier and the remote session, and
  the Chief of Staff says it first among the configuration lines.
- New: one harmless trial per used capability before the go; forge probes of the stacks API and of
  the default branch's rules in P9; refusals recorded for the table.

## What changes

### 1. The capabilities

| Capability | Used when | Commands its agents run (exact forms) |
| --- | --- | --- |
| Every batch | always | `$CHANTIER …` (dev: `uv run --locked --project <checkout> chantier …`; plugin: `uvx --from <plugin> chantier …`); a Driver's push `git push -u <remote> chantier/…` and `git -C <worktree> push -u <remote> chantier/…`; the force push after a rebase `git [-C <worktree>] push --force-with-lease -u <remote> chantier/…`; the steering session's route `git push --force-with-lease=<branch>:<sha> <remote> <sha>:refs/heads/<branch>`; on GitHub `gh pr create|edit|ready|checks|view …` (with `gh pr edit --base` and `gh pr ready --undo`); on GitLab `glab mr create|update|view …`, `glab ci status`; `SendMessage` |
| A stack | `--mode stack` (or `order mode --note stack`) | the above, plus the native stack: `gh stack …` when the user took the `gh stack` extension, else `$CHANTIER forge-stack create|rebuild|show` (covered by the `chantier` rule; it calls the stacks API itself) |
| A release on its own | `--autonomous-releases N` at `open`, or `order grant <release-cr> --note "releases=<n>…"` | the merge of the release PR by the steering session (`gh pr merge <pr> --<the project's method>`, `glab mr merge …`), the tag push (`git push <remote> v1.2.3`), the publication (`gh release create v1.2.3 …`, `glab release create v1.2.3 …`), and what the project's procedure names (for chantier: `just tag`, `uv run --script scripts/release_notes.py …`) |
| Fixes on a grant | `--grant-fixes` at `open`, or `order grant … fixes=on` | the merge of a fix PR by the steering session (`gh pr merge …`, `glab mr merge …`) |

The capability "every batch" keeps exactly CR-238's sample rows. The other three add rows.

### 2. The CLI: `skills/chantier/scripts/cli/src/chantier/commands/permissions.py`

- `SAMPLES` (lines 32–72) gains the capability of each row. A row becomes
  `(capability, forge, command, rule)`: `capability` one of `batch`, `stack`, `release`, `fixes`;
  `forge` one of `any`, `github`, `gitlab`, `gh-stack`, `dev`, `plugin` (today's group values
  move there unchanged). Existing rows take `batch`. The `gh-stack` row (`gh stack view`) takes
  `stack`. New rows, in the host table's order:
  - `("release", "github", "gh pr merge 12 --rebase", "gh pr merge*")`,
    `("release", "gitlab", "glab mr merge 12 --rebase", "glab mr merge*")`;
  - `("release", "any", "git push origin v1.2.3", "git push origin v*")`;
  - `("release", "github", "gh release create v1.2.3 --verify-tag --notes-file /tmp/notes.md",
    "gh release create*")`, `("release", "gitlab", "glab release create v1.2.3 --notes-file
    /tmp/notes.md", "glab release create*")`;
  - `("fixes", "github", "gh pr merge 12 --rebase", "gh pr merge*")`,
    `("fixes", "gitlab", "glab mr merge 12 --rebase", "glab mr merge*")`.
  ` origin ` keeps standing for the project's remote name. The comment above `SAMPLES` says the
  order is the host card's capability table's.
- `RECOMMENDED_ALLOW` (lines 76–83): built from the `batch` and `stack` rows only, so it keeps
  CR-238's content (no `release create`, no `pr merge`, no tag rule) and keeps equalling the
  pasteable JSON block. A new `GRANT_ALLOW` (the same shape) holds the rules of the `release` and
  `fixes` rows; it is listed in the host card's table, not in the JSON block.
- `_sample_groups` (lines 156–176) becomes the selection of rows: the `forge` rule as today (the
  remote's host; neither forge: both; `dev` or `plugin`), and the capabilities asked. The
  `gh-stack` row applies only to the capability `stack` and only when the extension is installed
  (the detection of lines 167–175 stays).
- `commands_not_allowed` (lines 192–230) takes the set of capabilities and returns its counts,
  additions, denied rules and unreadable files **per capability**. `SendMessage` stays in `batch`.

### 3. The CLI: `commands/preflight.py`

- `preflight` gets three options, named as `open`'s (opening.py lines 321–348) so the Chief of
  Staff passes the same words: `--mode parallel|series|stack`, `--autonomous-releases N` (N > 0
  adds `release`), `--grant-fixes` (adds `fixes`). `--mode stack` adds `stack`. With none of them
  (the first turn of a session, `init`), only `batch` is checked.
- `_check_allow` (lines 178–190) prints one P10 line per checked capability, the base first, in
  the table's order:
  - `P10 ok   <capability>: the commands its agents run are allowed by your settings`;
  - `P10 warn <capability>: <n> of <m> commands its agents run are not allowed by your settings
    (<files>): <samples> (add <rules>)…; denied: …; <explanation>; the rules are in
    hosts/claude-code.md, "Capabilities and their commands"`.
  - `<explanation>` is the strong warning of answer 2, one sentence, the same on each warn line:
    "the host's auto-mode classifier judges each command at run time, and in a remote session
    (Remote Control) nobody may be there to answer its prompt: <capability> may stop at the first
    one".
  - With no capability option, one more line after the base: `P10 ok   not checked here: a stack,
    a release on its own, fixes on a grant (checked at the go when the batch uses them)`.
  - P10 stays `warn=True`: exit 0, "preflight passed" unchanged. The `register` help (line 229)
    keeps "(P10 only warns)".
- The CLI runs **no trial** and **no forge probe**: a command run by the CLI is a child process,
  which the host's permission check never sees, so it would prove nothing. The trials and the
  probes are the Chief of Staff's own tool calls (sections 5 and 6). The CLI gets no new command
  and writes nothing new (`AGENTS.md`: new CLI tools only from measured token cost).

### 4. `skills/chantier/references/hosts/claude-code.md`

- **New subsection "Capabilities and their commands"**, under "Allow rules" (after line 202). The
  table of section 1, one row per capability, with the columns: Capability; Used when; Commands
  its agents run; Rules (the `Bash(…)`/`PowerShell(…)` forms, as P10 prints them); Trial before
  the go (section 5); Mark. It is the one table: P10's `SAMPLES` follow its order, and a test
  compares them (section 9). The rows `release` and `fixes` carry their risk ("any merge of any PR
  `gh` can reach"; "any release on any repository `gh` can reach"; "a push of any `v*` tag") and
  the line "offered only when the user grants it: without a grant, the host's prompt and its
  classifier keep guarding these commands".
- **The existing "Allow rules" table (lines 176–195)** keeps the base rows. The paragraph of lines
  200–202 ("There is no `gh release create` … rule, by design …") becomes: "The base set holds no
  release, merge or tag rule, by design: a release is rare, public and irreversible, and the host's
  check is a second guard at publication. When the user grants a release to run on its own, or
  fixes to merge on a grant, the Chief of Staff offers the rules of that capability
  ("Capabilities and their commands"), and only then."
- **The JSON block (lines 207–249)** is unchanged: it equals `RECOMMENDED_ALLOW`.
- **"Auto mode" (lines 291–315)** gains, after line 311, what the trials can and cannot prove
  (the request's last point):
  - an allow rule resolves a matching command at once, before the classifier (documented): a trial
    that runs where P10 says a rule matches proves the host honours that rule's form, which settles
    the unproved rows (`uv run … chantier *`, `uvx --from * chantier *`, `gh stack*`);
  - the host offers no way to try a rule ahead for the commands with no harmless form
    (`gh release create`, `gh pr merge`, `gh pr edit --base`, `SendMessage`): auto mode's
    classifier judges them at run time. Their only check before the go is P10's rule match;
  - a harmless form the classifier lets through with no rule proves nothing for the real
    command: the classifier judges each command on its own;
  - a trial runs in the Chief of Staff's session; the classifier blocks destructive git in
    subagents (line 302), so a trial that passes there with no rule says nothing about a Driver.
- **The alert sentence (lines 312–315)** gains the remote session: "… an unattended batch waits
  for you at the first one, and in a remote session nobody may be there to answer."

### 5. The trials: `skills/chantier/references/chief-of-staff.md`

"Starting a batch", step 1 (lines 388–406), after the preflight with the batch's options:

- **One harmless trial per used capability**, run by you, each command alone (rule 9), in this
  session's permission mode, before the go, with the user there. The trial forms (the host table's
  column "Trial before the go"):
  - every batch: the `$CHANTIER preflight` you just ran (the `chantier` rule); `git -C <main
    checkout> push --force-with-lease -u <remote> chantier/preflight-trial --dry-run` (the `-C`
    force-push rule; the trailing `--dry-run` keeps the command under the rule's `*`); on GitHub
    `gh pr view --json number`, on GitLab `glab mr view`;
  - a stack with the extension: `gh stack view`; with `forge-stack`: the stacks API probe of P9
    (section 6);
  - a release on its own: `git push <remote> v0.0.0-preflight-trial --dry-run` (the tag rule);
    `gh release create` and the merge have no harmless form: "no trial: P10's rule check only";
  - fixes on a grant: no harmless form: "no trial: P10's rule check only".
- **What a trial proves:** that the host let the command run. The command's own error (no such
  branch, no PR for this branch) is a pass: the trial tests the permission, not the command. A
  denial, a prompt or a classifier refusal is a refusal. Say the limits of the host card's "Auto
  mode" when a trial passes where P10 named a missing rule.
- **A refusal at the trial** is said at once, with the command and the host's exact text (rule 7),
  in the same strong warning as P10's (the classifier, the remote session), with the rules P10
  named for that capability in the question of "The project". It never blocks the go: the user
  decides.
- **Recorded:** after `open`, a section "Permission trials" in the batch's `brief.md`, one line
  per trial: `<capability>: <command> -> ran | refused: <exact text> | no trial: P10's rule check
  only`, with the P10 line of each capability. Before a batch (a first turn), the result is told,
  not recorded.
- Each trial writes nothing: a `--dry-run` push of a branch or tag that does not exist fails on
  the refspec before reaching the remote. The Driver proves each form once by hand (section
  "Evidence").

### 6. The forge's probes: `chief-of-staff.md`, "Forge permissions (P9)" (lines 336–382)

The probes stay warnings, as P9 is today ("Everything below only **warns**", line 341, unchanged;
answer 4). New items, run at step 1 for the capabilities the batch uses, read-only, each command
alone, `--json` on Windows PowerShell 5.1:

**GitHub:**

4. A stack (made by `forge-stack` or by the extension): the stacks API,
   `gh api repos/<owner>/<repo>/stacks -X GET -F per_page=1`. A 404 or 403 means no native stack
   on this repository: warn that `forge-stack create` or the extension will fail there, and that
   the stack then stays a chain. `forge_stack.py` calls this API only at create (`_make`, line 119;
   `_stacks`, lines 131–135): this probe moves the discovery to the go.
5. A merge by the steering session (a release on its own, fixes on a grant), and a stack (merged by
   the user in one action): the default branch's rules,
   `gh api repos/<owner>/<repo>/rules/branches/<default branch>`, and the methods,
   `gh repo view --json mergeCommitAllowed,rebaseMergeAllowed,squashMergeAllowed`. Warn on:
   - a `pull_request` rule with required approving reviews: a steering session's merge of its own
     account's PR waits for a review it cannot give (the grant's merge stops);
   - a `required_status_checks` rule: the merge waits for those checks (said, not a problem);
   - a `merge_queue` rule: a merge enqueues instead of merging, and a stack's one-action merge may
     not apply;
   - the project's merge method (its rules, for instance "merge by rebase") not among the allowed
     methods.
   The legacy branch protection is read as item 3 says (an `ADMIN` account only).

**GitLab** (unproved, as the section's other GitLab items):

4. No native stack: nothing to probe (a stack stays a chain).
5. `glab api projects/<url-encoded path>`: `merge_method`, `approvals_before_merge` (or the
   approval rules), merge trains; `projects/<path>/protected_branches/<default branch>`:
   `merge_access_levels` above the account's level refuses the merge.

"What the user hears" (lines 368–380): the forge's warnings go in the same block, each with what
to change in the forge's own words. The release line (lines 376–380) changes: without a grant, as
CR-238 says (the publication stays asked by the host); with a grant, the publication is a command
of the capability "a release on its own", its rules are offered (section 7), and when they are not
added, the strong warning says the release may stop at publication with nobody to answer.

### 7. The question per capability: `chief-of-staff.md`

- **"The project", the allow rules (lines 83–105).** At a first turn the question covers the
  capability "every batch" only. Add: "At the go, the question covers the capabilities the batch
  uses, with what is still missing; at a grant given later (`order grant`), it covers that
  capability." The rules of `release` and `fixes` are offered only when the user granted them
  (answer 5): never at a first turn, never for a batch without the grant. "Asked once per session"
  becomes "asked once per session per capability". "On a no" says, per capability, what will stop:
  for `release`, "the release will stop at the merge or the publication and wait for you"; for
  `fixes`, "the fix's merge will wait for you".
- **The strong warning.** A P10 warn line or a refused trial is said first among the
  configuration lines, with its explanation in the user's language (the classifier, the remote
  session), and with what the capability will do without the rules. It never blocks the go.
- **Step 1 (lines 388–394).** "`$CHANTIER preflight`" becomes "`$CHANTIER preflight` with the
  batch's options (`--mode`, `--autonomous-releases`, `--grant-fixes`, as `open` will get them)",
  then the trials (section 5), then P9 with the probes (section 6). The rest of the P10 sentence
  stays ("warns and never fails … P10 never blocks the go").
- **"auto" during a release (lines 1003–1014)**, between steps 2 and 3: run `$CHANTIER preflight
  --autonomous-releases 1`, P9's probe 5 and the release trial; ask the question for the release
  rules still missing, act on the answer, then `order grant`. The same for a later
  `order grant … fixes=on` with `--grant-fixes`. The grant itself never waits for the rules: the
  user's word is the grant.
- **The project's own procedure.** For a release on its own, read the project's release procedure
  and name each command it runs that no table row covers (for chantier, `just tag`), as one line:
  "`<command>` is the project's own: no rule is offered for it; it may meet the host's prompt".
  No rule is offered for it (see open point 2).

### 8. Refusals recorded for the table

- `chief-of-staff.md` ("While it runs", the `refused <cr> <text>` line 555–557, and "A refused
  force push") and `foreman.md` (line 190's `refused <cr> <text>`, line 273–280's push route):
  the steering session records each refusal at once,
  `$CHANTIER note <cr> "refused: <the exact command> -> <the host's exact text>"`.
- The batch retro (`foreman.md` line 25 and its tag rule, line 36; in direct mode the Chief of
  Staff's) gives one line per distinct refused command:
  `- [chantier] refused \`<command>\` (<capability>): <the table row or rule to fix>`. The
  systematic retro offers it as an inbox item, so the next table fixes it.

### 9. Copilot: `skills/chantier/references/hosts/copilot.md`, "Configuration" (lines 50–59)

What applies there:

- the capability table is the cards' commands, the same on both hosts: it is read from
  `hosts/claude-code.md`; its rules are Claude Code's;
- P10 does not run (unchanged), and no rule is recommended until a Copilot trial records one;
- the trials run as on Claude Code (the Chief of Staff's own calls, one per used capability), and
  a refusal is told and recorded with its exact text, as in sections 5 and 8; **unproved** until a
  Copilot batch runs them;
- P9's forge probes (section 6) are the card's and run unchanged.

The agent files (`agents/`, `com.github.copilot/agents/`) change only if their body names P10 or
a release rule; today none does. If one does, both change together with identical bodies.

### 10. Other cards and docs

- `skills/chantier/references/session-start.md` line 31: P10's warning per capability, the base
  only at a first turn.
- `skills/chantier/references/init.md` lines 80–88: the tour checks the base capability; it names
  the others as checked at the go. No trial at `init`.
- `skills/chantier/references/driver.md` lines 565–574 (the publication step): "when the host lets
  it through (no rule is recommended for it, by design …)" becomes "when the host lets it through
  (its rule is offered only under a release grant; without it the host asks or its classifier
  judges)". The refusal path is unchanged.
- `docs/tutorial-claude-code.md`: the P10 lines CR-238 rewrote say the check is per capability.
  The Driver greps `P10`, `release create`, "by design" over `docs/`, `README.md`, `scenario/`
  and the cards, and updates what it finds.

### 11. Tests and scenario

Tests stay few (`AGENTS.md`); the existing ones in `skills/chantier/scripts/cli/tests/test_cli_runs.py`
gain assertions, no new function:

- the JSON block test (around line 228): still equals `RECOMMENDED_ALLOW`, still no
  `release create` (line 234 stays); add: the rules of the host card's "Capabilities and their
  commands" table equal the rules of `SAMPLES`, in order.
- the P10 test (lines 240–311): with `RECOMMENDED_ALLOW` in the settings on a GitHub remote,
  `preflight` prints `P10 ok` for the base and the "not checked here" line;
  `preflight --autonomous-releases 1` prints a `P10 warn` line for the release capability that
  names `gh release create*` and `gh pr merge*` and holds the words "classifier" and "Remote
  Control"; exit 0 in both.
- `scenario/run_scenario.py` (lines 545–573): one check in the same step: `preflight
  --autonomous-releases 1` warns with the release rules and still passes; plain `preflight` names
  no release rule (CR-238's check, line 553, stays).

## Out of scope

- Making a missing rule or a forge problem a preflight failure (dropped, answer 2).
- Any change to a forge setting, and any rule outside the table (the project's procedure commands
  such as `just tag`: named only, see open point 2).
- The CLI running trials or probes (they would bypass the host's check), or a new CLI command.
- The eval kit (`evals/kit/setup.py`'s sandbox rules), as CR-238 left it.
- A grant given without the rules: the grant stays the user's word; the rules are offered, not
  required.

## Evidence

- `just check` passes on Linux, macOS and Windows (`ruff`, `mypy --strict`, files at most 400
  lines, functions at most 50).
- `just scenario` passes, with the check of section 11.
- By hand on this repository, the outputs in the PR's Deliverables: `preflight`,
  `preflight --mode stack`, `preflight --autonomous-releases 1 --grant-fixes`, each printing its
  P10 lines.
- By hand, each trial form of section 5, run once in a Claude Code session: the host's answer
  recorded, and `git status`, `git ls-remote <remote> 'refs/heads/chantier/preflight-trial'
  'refs/tags/v0.0.0-preflight-trial'` showing that nothing was written locally or on the remote.
- By hand, P9's probes 4 and 5 on this repository (GitHub), their output in Deliverables.
- In a real session (the PR's Known gaps names it until done): a Chief of Staff at a go with a
  release grant runs the trials, warns with the classifier and remote explanation, asks the
  question for the release rules, and records "Permission trials" in `brief.md`.

## Open points (each with the default this specification takes)

1. **Trials for a Driver's view.** A trial runs in the Chief of Staff's session; the classifier
   treats subagents differently ("Git Destructive"). Default: no subagent is started for the
   trials; the limit is said (section 4, "Auto mode"). The other option, one short subagent that
   runs the force-push trial, costs an agent start at every go.
2. **The project's own release commands** (`just tag`, a release script). Default: named in one
   line, no rule offered, since CR-238's settings-write exception covers only the rules P10 named.
   Offering them would widen that exception in `AGENTS.md`.
3. **The tag rule's form.** Default: `git push <remote> v*`, the common `v` prefix. A project whose
   tags differ is not covered by it and gets the strong warning.
4. **The P10 output shape.** Default: one line per checked capability, all with the `P10` tag. One
   single line holding every capability was the other option.
