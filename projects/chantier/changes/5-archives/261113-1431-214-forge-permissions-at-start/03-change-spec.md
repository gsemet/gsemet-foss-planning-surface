# Change Specification: forge permissions checked at the start

## Goal

When the Chief of Staff starts (its first turn of a session) and again at step 1 of "Starting a
batch", it checks that the batch's forge operations will go through, both on the host side (would
the commands the agents run be allowed as they write them?) and on the forge side (can the
logged-in account do what the batch needs, on GitHub, or on GitLab when the project's remote is
there?). It tells the user what is missing at the first turn, before any go, with the exact rules to
add and the forge right that is missing. It does not wait for a Driver to be refused in the middle of
the night. A missing right is a warning and never blocks.

The rights checked include the force push of a CR's branches after a rebase (a Driver's, the stack
driver's restack, the steering session's route), the PR edits (`gh pr edit --base`, `--body-file`,
`gh pr ready [--undo]`), the stack on the forge, and the release's publication (`gh release
create`).

## Origin and evidence of the problem

- Batch-15 (night of 2026-11-12 to 13): auto mode's classifier refused to the stack driver its 14
  `--force-with-lease` pushes of `chantier/batch-15/*` branches. It then refused the Chief of
  Staff's own run of them, a PowerShell loop. The stack waited for the user's word in the morning
  (ask A-17).
- Also refused in batch-15: `gh pr edit --base` on a PR, the stack's update on the forge (a `gh api
  .../stacks` call carried in a message; ask A-22), and `gh release create v0.9.0` after `just tag`
  passed (ask A-24; the Chief of Staff ran it on the user's word). Source:
  `.agents/changes/5-archives/261113-1149-213-stack-merges-in-one-go/retro.md`, points 16, 19 and 22.
- `preflight` P10 says "19 of 19 recommended allow rules not found as written" on the user's
  machine. Yet `~/.claude/settings.json` holds equivalent rules in another form, for instance
  `PowerShell(git push --force-with-lease=chantier/* origin *chantier/*)`. The warning is always
  on, so nobody hears it.
- P9 checks only that `gh` / `glab` is logged in.

## Decisions carried from `02-answers.md`

| # | Decision | Where in this spec |
| --- | --- | --- |
| D1 | At its start the Chief of Staff checks the forge permissions the batch needs: on GitHub, or on GitLab for a GitLab project | Areas 1, 2, 3 |
| D2 | A missing right **warns, never blocks**: the Chief of Staff tells the user that the permissions may stop the batch from running unattended, and advises what to allow | Areas 1, 3 |
| D3 | On Claude Code the alert says in detail that auto mode's classifier refuses some force pushes, and that these come with rebases (a Driver after a rebase, the stack driver's restack) | Areas 1, 4 |
| D4 | The general rule is for every host: **a CR's branches must be force-pushable at all times**. It goes in the cards every host reads | Area 5 |
| D5 | How to do it on Claude Code (the allow rules, and forms that match what the agents actually run) goes in `hosts/claude-code.md` | Area 4 |
| D6 | (Joined 2026-11-13) The start check names the release's publication (`gh release create`) among the rights the batch needs. The cards say whether the publication is allowed by a named permission rule or run by the user | Areas 1, 4, 6 |
| D7 | (Retro, in scope by the Chief of Staff's prompt) P10 judges whether a rule is equivalent, not whether it is the same string | Area 1 |

## Choices made here (nothing the user sees changes because of them)

- **P10 judges by sample commands.** P10 no longer compares rule strings. It holds the commands
  the cards make the agents write, filled with realistic values, and asks whether some allow rule
  of the user's settings matches each one, using Claude Code's documented matching. This is how it
  "judges equivalence" (D7): any rule that lets the command through counts, whatever its form.
- **The forge side stays in the card (P9), not in the CLI.** The agents do the forge work
  (AGENTS.md, "The CLI's scope"); no measured token cost asks for a new CLI tool. The Chief of
  Staff runs a few read-only `gh` / `glab` commands, the same way it runs P9 today.
- **The stack on the forge gets no `gh api` allow rule.** A direct `gh api` rule would allow any
  API write. The stack is changed only by the means the cards name: `$CHANTIER forge-stack`
  (covered by the CLI rule) or the `gh stack` extension (a rule of its own, below).
- **The recommended force-push rules are narrowed to `chantier/` branches.** The user's own
  settings already have that shape, and it carries less risk than `git push
  --force-with-lease*`, which covers any branch. A user who already has the broad rules keeps a
  `P10 ok`, because the broad rules match the samples too.

## What changes

### Area 1: preflight P10 (CLI), `skills/chantier/scripts/cli/src/chantier/commands.py`

Today `_ALLOW_COMMANDS`, `RECOMMENDED_ALLOW`, `_allowed_rules()` and the P10 block of `preflight()`
(about lines 173 to 300) compare strings.

1. **Sample commands.** Add a table of sample commands. Each sample is the form a card names
   (Area 5 fixes these forms), filled with realistic values: the project's remote name (the
   remote of the default branch, else `origin`), a branch `chantier/batch-01/cr-101-example`, a
   worktree path, a 40-hex sha, a PR number, a version `v1.2.3`. Each sample is tied to the
   recommended rule that covers it and to a group. Each one is checked in its `Bash(…)` form, and
   also in its `PowerShell(…)` form on Windows (as today: on POSIX only the Bash forms):

   | Group | Sample (the form agents write) | Recommended rule |
   | --- | --- | --- |
   | always | `git push -u <remote> <branch>` | `git push -u origin chantier/*` |
   | always | `git -C <worktree> push -u <remote> <branch>` | `git -C * push -u origin chantier/*` |
   | always | `git push --force-with-lease -u <remote> <branch>` | `git push --force-with-lease -u origin chantier/*` |
   | always | `git -C <worktree> push --force-with-lease -u <remote> <branch>` | `git -C * push --force-with-lease -u origin chantier/*` |
   | always | `git push --force-with-lease=<branch>:<sha> <remote> <sha>:refs/heads/<branch>` (the steering session's route) | `git push --force-with-lease=chantier/* origin *chantier/*` |
   | always | `uv run --script <path>/chantier.py status` | `uv run --script *chantier.py *` |
   | always | `SendMessage` (a bare tool) | `SendMessage` |
   | GitHub | `gh pr create --draft --body-file <f>`; `gh pr edit <n> --body-file <f>`; `gh pr edit <n> --base <b>`; `gh pr ready <n>`; `gh pr ready <n> --undo`; `gh pr checks <n>`; `gh pr view <n>` | `gh pr create*`, `gh pr edit*`, `gh pr ready*`, `gh pr checks*`, `gh pr view*` |
   | GitHub, the `gh stack` extension installed (`gh extension list` names `gh-stack`) | `gh stack <subcommand>` | `gh stack*` |
   | GitHub, the project's rules name `gh release create` | `gh release create v1.2.3 --title v1.2.3 --verify-tag --notes-file <f>` | `gh release create*` |
   | GitLab | `glab mr create --draft …`; `glab mr update <n> …`; `glab mr view <n>`; `glab ci status` | `glab mr create*`, `glab mr update*`, `glab mr view*`, `glab ci status*` |
   | GitLab, the project's rules name `glab release create` | `glab release create v1.2.3 …` | `glab release create*` |

   The forge groups follow the remote's host: a `github.com` or GitHub Enterprise remote gets the
   GitHub groups, `gitlab` in the host gets the GitLab groups, and an unknown host gets both, as
   today's list does. "The project's rules name" is a plain text search in what `$CHANTIER rules`
   lists (the instruction file and the files it links). A sample whose group does not apply is
   not checked and not reported.
2. **Matching, as Claude Code documents it** (`hosts/claude-code.md`, "How rules match"):
   - `Tool(pattern)`: `*` matches any text, anywhere;
   - `cmd *` (with a space) also matches the bare `cmd`;
   - the legacy suffix `:*` reads as ` *`;
   - PowerShell matching is case-insensitive;
   - a bare tool name (`SendMessage`) matches all its uses.

   An allow rule covers a sample when it matches the sample. A rule that auto mode drops on entry
   does not count: `Bash`, `Bash(*)`, `PowerShell`, `PowerShell(*)`, interpreter wildcards, and
   package-manager run commands (`uv run *`). These are the documented rules, listed in "What not to
   add". A sample matched by a `deny` or `ask` rule of the three files is reported as such, since
   deny > ask > allow. The three files are those read today (`_SETTINGS_SHOWN`).
3. **Output** (still one line, still `warn` and never `FAIL`):
   - `P10 ok   the commands chantier's agents run are allowed by your settings[ (unreadable: …)]`
   - `P10 warn <k> of <n> commands chantier's agents run are not allowed by your settings
     (<files>): <sample> (add <rule>); …[; denied: <sample> by <rule>]; the block is in
     hosts/claude-code.md, "Allow rules"`

   The rule to add uses the project's remote name in place of `origin` when they differ. Each
   missing sample is named once (its Bash form on POSIX; on Windows the PowerShell form is named
   when only that one is missing). A rule that covers several missing samples is named once.
4. `RECOMMENDED_ALLOW` stays the full recommended list, in the table order of `hosts/claude-code.md`
   (the Bash and PowerShell forms of each rule, then `SendMessage`). The structure test still
   compares it with the JSON block. The help line in `cli.py:35` stays true ("P10 only warns").
5. A sample command and its matching are plain data and a small function. They use no dependency,
   and they behave the same on POSIX and Windows.

### Area 2: P9, the forge side (Chief of Staff's own check), `references/chief-of-staff.md`

"The project" (first turn, around line 71) and "Starting a batch" step 1 (around line 244) now say
that P9 covers what follows. Both run it the same way, read-only, with each command alone (rule 9).
On Windows PowerShell 5.1, the commands print `--json` and read the JSON, with no `--jq` or
`--template` expression that holds spaces (`hosts/claude-code.md`, "Windows PowerShell 5.1"). A
not-logged-in CLI still fails P9 for a batch, as today. Everything else here only warns.

**GitHub:**

1. Logged in: `gh auth status` (as today). Its `Token scopes:` line: `repo` (or a fine-grained
   token, for which no scopes are printed, said as "unknown: a fine-grained token, see its
   permissions") and `workflow`. A missing `workflow` is named only as "needed by a CR that
   touches `.github/workflows/`". At step 1, the Chief of Staff names the CRs of the plan that do.
2. The right to push: `gh repo view --json viewerPermission,defaultBranchRef`. `WRITE`,
   `MAINTAIN` and `ADMIN` can push, edit PRs and publish a release. `READ` and `TRIAGE` cannot:
   the Chief of Staff says so.
3. The branch rules over `chantier/` branches: `gh api repos/<owner>/<repo>/rules/branches/<a
   chantier/ branch name>` (the rulesets that would apply to such a branch; the name need not
   exist). A rule of type `non_fast_forward` refuses the force push, `update` refuses the push,
   and `creation` refuses a new branch: each is named with its ruleset. The legacy branch
   protection of a pattern that matches `chantier/` is read only when the account is `ADMIN`.
   Otherwise it is said as "not readable with your rights". **Unproved:** whether the endpoint
   takes the `/` of the branch name raw or as `%2F`. Trial: run it on this repository with a
   `chantier/x/y` name, and keep the form that answers.

**GitLab** (the remote's host is GitLab), all **unproved**. Trial: one run on a GitLab project.

1. Logged in: `glab auth status` (as today), and the token's scopes if it prints them (`api` is
   needed).
2. The access level: `glab api projects/<url-encoded path>`, `permissions.project_access` or
   `group_access`, `access_level` 30 (Developer) or more to push, open MRs and create a release.
3. The protected branches: `glab api projects/<url-encoded path>/protected_branches`. A name or
   wildcard that matches a `chantier/` branch with `allow_force_push: false` refuses the force
   push. `push_access_levels` above the account's level refuses the push.

**What the user hears** (D2, D3): one short block in the first message, after the P5/P10 lines and
in the same message. It holds:

- what may stop the batch from running unattended, each line with what to change. A forge right
  is said in the forge's own words, for instance "a ruleset `protect-all` refuses force pushes on
  `chantier/*`: allow them for `chantier/**`, or exclude that pattern". The missing host rules come
  from the "Allow rules to add" block, with exactly the rules P10 named.
- on Claude Code, the sentence of Area 4 on why force pushes matter.
- the release's publication (D6), when the project's release procedure runs it: named either as
  allowed (the rule is there and the account can publish) or as "the publication is yours: you
  will be asked to run `<the command>`".

Nothing blocks the user's request. At step 1 the same check runs again, and the batch starts
whatever it says (D2). The plan's message repeats only what is still missing.

### Area 3: other places that state the first-turn check

- `references/session-start.md:31`: "(P5, P9, P10)" stays. Add that P9 now holds the forge's
  rights and branch rules.
- `references/init.md:80-81`: same wording update (P9 gives the missing forge rights too).
- `references/hosts/copilot.md`, "Configuration": P9's forge side runs on Copilot as on Claude Code
  (it is the card's check). P10 still does not run there, and no host rule is recorded. Add one
  line: a refusal of a force push on Copilot is reported like any refusal (rule 7), and the
  general rule of Area 5 holds.

### Area 4: `references/hosts/claude-code.md`, "Configuration"

- "Who reads it, when" (line 118): P10 now checks the commands, not the strings.
- "Allow rules":
  - Replace the table and the JSON block with the recommended rules of Area 1, in Area 1's order.
    Each Bash rule has its PowerShell twin, and `SendMessage` comes last. Each row keeps "chantier's
    use", "Risk accepted" and "Mark". New rows:
    - `gh pr edit*` (a Driver's body and the stack driver's retarget `--base`; refused in
      batch-15; risk: any edit of any PR `gh` can reach);
    - `gh pr ready*` (risk: a PR turned ready, or back to draft);
    - `gh pr view*` (read-only);
    - `gh stack*` (only with the extension; risk: any operation of the extension; **unproved**
      rule form for an extension);
    - `gh release create*` / `glab release create*` (the release's publication, only when the
      project's release procedure runs it; risk: a release published on any repository the
      CLI can reach; the CLI's `release go` still gates the step);
    - `glab mr update*`, `glab mr view*`.

    The force-push rows name their `chantier/` scope and the steering session's route form.
  - Say in a line that P10 accepts any rule that matches the same commands, so a narrower or
    different rule of the user's counts. Give the user's form as the example
    (`PowerShell(git push --force-with-lease=chantier/* origin *chantier/*)`).
- "Auto mode": add the batch-15 evidence. The classifier refused lease-protected force pushes of
  `chantier/` branches to the stack driver and then to the steering session itself (a PowerShell
  loop), and it refused `gh pr edit --base`, a stack update through `gh api`, and `gh release
  create`. An allow rule resolves a matching command before the classifier (already documented
  here); a loop, a script or a chain matches no prefix rule, so the classifier judges it alone.
  The text "the steering session's own push went through (proved by use, 2026-11-11)" stays, with
  "not always: refused on 2026-11-13 as a loop" added.
- The alert sentence of D3, written once here and used by the Chief of Staff: "Auto mode's
  classifier refuses some force pushes. They come with every rebase: a Driver's push after a
  rebase, and the stack driver's restack of every PR above a change. Without the rules below, an
  unattended batch waits for you at the first one."
- "Allow rules to add" (line 586): **Paste** is the rules P10 named (with the project's remote
  name). **You should see**: `P10 ok`, or a P10 line that no longer names them.

### Area 5: the general rule and the push forms, all hosts

- `references/concepts.md`, rule 8 (Git). Add: **a CR's branches must be force-pushable at all
  times**: a rebase is pushed with `--force-with-lease`, and the host and the forge must let it
  through (the Chief of Staff checks both at its start). Fix the push forms the samples of Area 1
  test, one command per branch, never a loop, a script or a chain:
  - plain: `git push -u <remote> <branch>`, or `git -C <worktree> push -u <remote> <branch>`;
  - after a rewrite: `git push --force-with-lease -u <remote> <branch>`, or the same with `git -C
    <worktree>`;
  - the steering session's route: `git push --force-with-lease=<branch>:<expected> <remote> <local
    sha>:refs/heads/<branch>`.
- `references/driver.md`, Push (line 71-72): already the form above. The stack driver (lines 300
  to 360: restack, partial merge, insertion) now says "push each one with the Push bullet's
  rewrite form, one command per branch".
- `references/chief-of-staff.md`, "A refused force push", step 3 (line 456): "one command per
  branch, never a loop or a script, even for a whole restack".
- The agent files (`agents/`, `com.github.copilot/agents/`) are not changed: the rule lives in the
  cards.

### Area 6: the release's publication, `references/driver.md` (Release driver) and `references/chief-of-staff.md`

- Release driver ("A release merged … go on through the procedure"): the publication step (for
  this project, `CONTRIBUTING.md` "Release" step 5, `gh release create … --verify-tag
  --notes-file …`) is run by the Release driver after `release go` answers `go`, when the host
  allows it by the named rule of `hosts/claude-code.md`. When the host refuses it, the Release
  driver reports the refusal with its exact text (rule 7) as `handback blocked approval: publish:
  <the exact command>`, and nothing else is tried. The steering session then gives the user the
  exact command as a **For you** line ("the publication is yours"). It never runs the command
  itself without the user's word (as with A-24).
- Chief of Staff (Area 2): at the start, it says which of the two applies for this batch. "The
  rule is there" means the Release driver publishes. "It is not there" means the publication is
  the user's step, and the user is told now and not at the end.

### Area 7: docs

- `docs/tutorial-claude-code.md:121-129`: the preflight checks the forge's rights and branch rules,
  and the allow rules by what they let through, not by their text.
- No other doc names P10's text.

## Out of scope

- Writing the user's settings, or changing a ruleset or a protected branch: chantier never does
  either. The user does, from the advice.
- Blocking a batch on a missing right (D2).
- A rule for `gh pr merge`, for the deletion of refs, or for `Agent(...)`: they stay as "What stays
  refused" and "What not to add" say.
- A `gh api` allow rule, and any change to `forge-stack` (its insert or rebuild is another CR,
  retro point 19).
- Rules on tags (a tag ruleset refusing `just tag`), signed-commit rules, and fine-grained token
  permissions in detail: each is said as unknown when met, never checked.
- Copilot's permission configuration (none recorded; unchanged).

## Evidence

**Checks** (`just check` on Linux, macOS and Windows; `tests/test_structure.py`, kept few):

1. Update `test_the_allow_rules_json_block_lists_exactly_what_preflight_checks`. It still compares
   the JSON block with `RECOMMENDED_ALLOW`. Add an assertion that each sample is matched by its
   own recommended rule, in both forms. This is the self-consistency of Area 1.
2. Update `test_preflight_warns_on_missing_allow_rules_and_never_fails_on_them`:
   - with no settings, `P10 warn` names `SendMessage` and a force-push rule;
   - with the user's equivalent forms only (`Bash/PowerShell(git push --force-with-lease -u origin
     chantier/*)`, `…(git push --force-with-lease=chantier/* origin *chantier/*)`), those samples
     are no longer named, while the `-C` force-push sample still is: equivalence is judged;
   - a `PowerShell(*)` / `Bash(*)` rule alone does not give `P10 ok`;
   - a `deny` rule matching a force-push sample is named as denied;
   - the full `RECOMMENDED_ALLOW` gives `P10 ok`;
   - Copilot gives no P10 line; preflight's exit code is 0 in every case.

**Scenario** (`just scenario`, needed since the CLI and the cards change):
`scenario/run_scenario.py:548-551` checks the old rule string
`Bash(git push --force-with-lease*)`. It becomes: `P10 warn` names `git push --force-with-lease -u
origin chantier/*` (the new rule). Add one step: a home `settings.json` holding the user's
equivalent forms (as in check 2) gives a P10 line that does not name the force-push forms they
cover. The existing `P10 ok` step with `RECOMMENDED_ALLOW` stays.

**By hand, on this machine, recorded in the PR:**

- `$CHANTIER preflight` in the main checkout with the user's real `~/.claude/settings.json`: P10 no
  longer says "19 of 19". It names only what the six existing rules do not cover. Paste the line.
- The GitHub P9 commands of Area 2, run on `gsemet/chantier`: their output (viewer permission,
  token scopes, the rules for a `chantier/x/y` branch), and the form of the rules endpoint that
  answered (the trial of Area 2).
- GitLab: stays **unproved**, marked so in the card with its trial.

## Self-containment for the Driver

Files to change:

- `skills/chantier/scripts/cli/src/chantier/commands.py` (P10)
- `skills/chantier/scripts/cli/tests/test_structure.py`
- `scenario/run_scenario.py`
- `skills/chantier/references/chief-of-staff.md`
- `skills/chantier/references/concepts.md`
- `skills/chantier/references/driver.md`
- `skills/chantier/references/session-start.md`
- `skills/chantier/references/init.md`
- `skills/chantier/references/hosts/claude-code.md`
- `skills/chantier/references/hosts/copilot.md`
- `docs/tutorial-claude-code.md`

No change to `hooks/` or `types/`, so `just mod` is not needed. No version edit. The CLI stays
dependency-free and portable.

## Open questions

None. Every choice left open by the answers changes nothing the user sees, or follows from D2 and
D6 as written above.
