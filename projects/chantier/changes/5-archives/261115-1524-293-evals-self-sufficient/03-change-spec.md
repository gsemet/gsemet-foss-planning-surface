# The evals folder is self-sufficient: anyone can run a campaign from it

## Goal

A person who never ran an eval, with only this repository and their own GitHub account, stages and
starts `real-foreman` by following `evals/README.md`: their own sandbox (created, published,
named once), the operator's prompt printed ready to paste, the operator's session started the way
that works on Claude Desktop, every prerequisite in one list, the host's PR automations turned off
first, and the two staging lines batch-18 missed. `reset` stays as safe as it is today: it refuses
anything that is not a sandbox whose history holds the recorded base.

The scope is the request's six points as written (`02-answers.md`, answer 1: "The request's scope
stands as written; ... implementation detail is the agents'"). Hosts: Claude Code and Copilot. Forge:
GitHub only.

## What changes

### 1. The sandbox repository: named in one place, any person's

Today `REPO` is a constant in `evals/kit/sandbox.py` (and `URL` from it), a second copy in
`evals/kit/sandbox_forge.py`, and the `repository` field of `evals/kit/sandbox.json`; the README
says "the repository is a constant of the script".

- **One place names the repository** (`02-answers.md`, answer 2). A new, git-ignored file
  `evals/kit/sandbox.local.json`, `{"repository": "<owner>/<name>"}`, names a person's own
  sandbox. When it is absent, the repository is the `repository` field of `evals/kit/sandbox.json`
  (the maintainer's, `gsemet/chantier-eval-sandbox`, unchanged). One function in `sandbox.py` (for
  example `repository()`, with `url()` from it) is the only reader; `setup.py`, `judge.py`,
  `audit.py`, `merge`, `reset` and `sandbox_forge.py` take the name from it and nowhere else (the
  second constant in `sandbox_forge.py` goes). No command-line argument and no environment
  variable names the repository. Add `evals/kit/sandbox.local.json` to the root `.gitignore`, so a
  person's sandbox never dirties their checkout (setup records a dirty tree in the run record).
  `build --record` writes only `base` in `sandbox.json` and keeps its `repository` field as it is
  (today it writes `REPO`, which would copy a person's name into the committed file). A malformed
  `sandbox.local.json` (not JSON, no `repository`, not `owner/name`) is a precondition stop (exit 2)
  naming the file; never a silent fall back to the maintainer's repository.
- **Every command says which sandbox it acts on.** `reset`, `publish`, `merge` and `setup.py`
  print the repository and where it was read (`sandbox.local.json` or `sandbox.json`) on their
  first line, so a person sees before any write which repository the plan touches.
- **`reset` refuses what is not a sandbox at the recorded base's history.** New refusals, checked
  before the plan is printed, each a precondition stop (exit 2) that changes nothing, `--yes` or
  not:
  - the repository has no `main` (empty repository): "no main on <repo>: publish the base first
    (`sandbox.py publish`)";
  - the recorded base is not in `main`'s history (the base is the root commit `build` makes, so
    this is: `main` is the base or descends from it; read with a fetch of `main` into the temporary
    build repository and `git merge-base --is-ancestor <base> FETCH_HEAD`): "<repo>'s main does not
    hold the recorded base <sha>: not a chantier eval sandbox; nothing changed";
  - a branch or tag other than `main` whose history does not hold the base gets the same refusal,
    naming the ref.
  The rest of `reset` is unchanged (plan, `--yes`, the only force push, `verify`). These checks are
  what keep a misnamed real repository of the person's safe: none of them holds the base.
- **New `sandbox.py publish <owner>/<name> [--yes]`**: creates a person's sandbox and points the
  kit at it. Without `--yes` it prints the plan and changes nothing, like `reset`. The plan:
  1. if the repository does not exist: `gh repo create <owner>/<name> --public`. Public only, like
     the maintainer's (`02-answers.md`, answer 2): no option for a private one. If it exists, it
     must be public and empty (no ref at all), else refused (exit 2): publish never force-pushes
     and never touches a repository with history;
  2. build the base (refused if its SHA-1 is not `sandbox.json`'s `base`, as `reset` does) and push
     it to `refs/heads/main`, a plain push to an empty repository;
  3. check the default branch is `main` and `main` is not protected (the sandbox's `main` is
     unprotected by design; a protected one is reported, not changed);
  4. write `evals/kit/sandbox.local.json` naming it. If that file already names another
     repository, refused (exit 2), naming both: the person removes it themselves.
  Its preconditions are `reset`'s (`gh auth status`, the `workflow` scope needed to push
  `.github/workflows/`, a git credential helper for github.com). It prints the repository, the base
  and the next step (`setup.py <campaign> <workspace>`; no `reset` is needed after a publish).
  `publish` on the maintainer's name works the same way and is refused there since it is not empty.
- **`merge`** (unchanged rules): its PR-link check and its run-record check compare with the one
  repository name. **`setup.py`**: `survey`, `run_number`, the clone, the run record's `repository`
  and `issue_lines` use it.
- **`sandbox_forge.py`** answers for the repository `sandbox.py` names (the dry run's local
  sandbox), not a constant of its own.
- **Docstrings**: `sandbox.py`'s "The repository is a constant: no argument or variable changes
  it" becomes "One file names the repository (`sandbox.local.json`, else `sandbox.json`); no
  argument or variable changes it, and `reset` refuses a repository whose history does not hold the
  recorded base". `setup.py`'s and `sandbox_forge.py`'s docstrings follow.

### 2. setup.py prints the operator's prompt

`sandbox_main` already prints the `CHANTIER`, `merge` and `open` lines. It also prints, last, one
`prompt` line: the campaign's runbook prompt with `<this checkout>` replaced by the checkout's
absolute path (`ROOT`), in the platform's native spelling, ready to paste:

- `full`: `/chantier:chief-of-staff foreman Run the chantier eval campaign full: follow <ROOT>/evals/full/RUNBOOK.md.`
- `real-foreman`: `/chantier:chief-of-staff foreman Run the chantier eval campaign real-foreman in <stack|parallel|series> mode: follow <ROOT>/evals/real-foreman/RUNBOOK.md.`
- `real-direct`: `/chantier:chief-of-staff direct Run the chantier eval campaign real-direct in <stack|parallel|series> mode, in direct mode: follow <ROOT>/evals/real-direct/RUNBOOK.md.`
- `ticket-summary` and `copilot`: their runbooks have no prompt today; each gains a "Start"
  section with one, in the same form (`ticket-summary`: `/chantier:chief-of-staff Run the chantier
  eval campaign ticket-summary: follow <ROOT>/evals/ticket-summary/RUNBOOK.md.`; `copilot`, typed
  in a Copilot chat on the workspace: `Run the chantier eval campaign copilot: follow
  <ROOT>/evals/copilot/RUNBOOK.md.`), and setup prints it. The Copilot form is marked unproved in
  its runbook until the campaign's first run.

The mode stays a blank to fill, as it already is in the `open` line (`02-answers.md`, answer 2):
setup takes no `--mode`. The prompt text lives once, in `setup.py`'s `CAMPAIGNS` table; each
runbook's "Start" shows the same text with `<this checkout>` and says setup prints it filled. The
paths in the printed prompt are quoted only if they contain a space, as `merge_command()` does. The
`workspace` line setup prints is already the native spelling; the README says to use that spelling
when the app asks for the folder.

### 3. Starting the operator's session (README, "The operator", and each runbook's "Start")

Say the two ways that worked on 2026-11-15, and the trust step:

- **From New session** in the Claude Desktop app's Code tab: pick the workspace folder (its native
  spelling, backslashes on Windows: the `workspace` line setup printed), then paste the `prompt`
  line.
- **From a chantier session at the desk**: ask a Claude Desktop session (for example the one in
  this checkout) to start a new session on the workspace with the `prompt` line.
- **The trust step**: the first time, the app asks to trust the new workspace folder. It can ask
  only while the Code tab shows that session at the desk: under Remote Control it is refused. Answer
  it at the desk, then the session runs.
- On Copilot: a new chat of the Copilot app opened on the workspace, with the `prompt` line.

### 4. Prerequisites in one list (top of `evals/README.md`)

A new section "Prerequisites", right after the introduction and before "Campaigns", one list:

- this repository cloned, and the chantier plugin installed from it, the session restarted
  (`claude plugin marketplace add <this checkout>`, `claude plugin install chantier@chantier`);
- `uv` and `git`;
- `gh` logged in (`gh auth status`) with the `workflow` scope (`gh auth refresh -s workflow`) and
  git's credential helper set (`gh auth setup-git`), on an account that can push to the sandbox;
- a sandbox of your own (`sandbox.py publish <you>/<name>`, section 1), or push rights on the
  maintainer's;
- Claude Desktop, at the desk (not Remote Control) for the start and the trust step;
- the host's PR automations off (section 5).

Then the per-campaign steps in order: reset (or publish, the first time), setup, start the operator
with the printed prompt, the runbook's turns, the audit, close, the cost, the report. "Before you
start" keeps only what is specific to `claude-planted` and points to the list for the rest; no line
says the same thing twice.

### 5. Turn off the host's PR automations before and during a campaign

In the README's list and in its "A sandbox campaign" preparation, before setup, the person running
the eval:

- turns **global Auto-fix off** in Claude Desktop (Settings > Code, or Settings > Claude Code, by
  the app's version), marked **unproved**: the official documentation
  (https://code.claude.com/docs/en/desktop.md#monitor-pull-request-status) describes only the
  per-PR switch and no default for PRs opened later, and third-party reports say the global toggle
  may not reach PRs of local sessions;
- turns **auto-archive / auto-close on PR merge or close off** in the same settings, so the app does
  not archive a session when a run's PR merges.

**During the run, the operator turns Auto-fix off itself** (`02-answers.md`, answer 2): as soon as a
PR of the run appears (an `ask ready`, a hand-back, or the PR bound to its session), the operator
calls `mcp__ccd_pr__set_monitor` to turn that PR's monitor off, only on the run's own sandbox PRs:
a PR of the sandbox repository whose title starts with the run's prefix. Never on another PR, never
to arm it. It is what real-direct run 3 of 2026-11-15 did after Auto-fix events arrived on a sandbox
PR. Written in two places, the same words:

- `evals/README.md`, "A sandbox campaign", a new bullet "**Auto-fix during the run**" next to "The
  operator", and the "Before you start" Auto-fix line, which loses "That section marks the way to
  turn it off **unproved**, so this guide gives no path either" and points to the prerequisites and
  this bullet;
- each Claude sandbox runbook's "The user's turns" (`full`, `real-foreman`, `real-direct`,
  `ticket-summary` has no PR and gets none), as the first act on each new PR of the run.

The fallback by hand, when the tool is refused or absent: the person turns it off from the PR's ⋮
menu in the operator's Changes card, and the report records the refusal as a finding. `setup.py`'s
workspace `.claude/settings.local.json` for a Claude campaign that opens PRs adds the allow rule
`mcp__ccd_pr__set_monitor` (the tool was refused twice in the user's week, per the hosts card's
"Configuration"), and the README's "Nothing else is allowed there" line and `setup.py`'s docstring
name it among the rules.

**The hosts card** (`skills/chantier/references/hosts/claude-code.md`, "Auto-fix events"), kept
consistent:

- the "Turning Auto-fix off" bullet becomes: the per-PR switch is documented (the official page
  above) and seen on 2026-11-15: `mcp__ccd_pr__set_monitor`, or the PR's ⋮ menu in the Changes card;
  the global setting (Settings > Code or Settings > Claude Code) stays **unproved**, with its trial
  (turn it off, open a PR from a subagent in a local session, see whether an event arrives; record
  the labels and the date). Turning it off also loses Auto-fix for the user's own PRs.
- the "chantier never arms, disarms or unbinds the PR monitor" bullet keeps its rule for the roles
  (no card's role calls the tool during a batch) and adds one sentence: the only use is the eval
  guide's operator, who plays the user, turning the monitor off on a run's own sandbox PRs
  (`evals/README.md`).
- "During a normal batch chantier stays silent about Auto-fix" stands; its "Only the eval guide asks
  for Auto-fix off, before a real campaign" becomes "Only the eval guide turns Auto-fix off: before a
  real campaign, and on each of the run's own PRs".
- The "Configuration" note on `mcp__ccd_pr__set_monitor` ("No chantier card uses it, to arm or to
  disarm") gains the same pointer: the eval kit's workspace allows it for its operator.

### 6. Two more staging lines

- **No board left running from an earlier run**: before the start, the README's preparation says
  to stop any `chantier board` still running (its port, 8765 by default, in use made run 2's board
  fail), with the check per system: PowerShell `Get-NetTCPConnection -LocalPort 8765 -State Listen`,
  POSIX `lsof -iTCP:8765 -sTCP:LISTEN`.
- **The campaign's cost read after `close`**: the audit's cost and `cost --explain` stay where they
  are (before `close --yes`), and the report's cost figure is the one in the closed batch's record,
  `.agents/changes/5-archives/batches/batch-NN.md`, read after `close --yes` (run 2's cost rose
  from $11.47 to $11.91 between the audit and the close). The README's audit bullet and "The report"
  section, and each runbook's "Audit and report", say so.

## Decisions carried

- `02-answers.md`, answer 1: the request's scope as written, all six points, in this batch's
  parallel set before the release; implementation detail is the agents'.
- `02-answers.md`, answer 2: the operator agent turns a run's PR Auto-fix off itself with
  `mcp__ccd_pr__set_monitor`, only on the run's own sandbox PRs, written in the runbook and the
  README (section 5); `evals/kit/sandbox.local.json` names a person's sandbox (section 1); the mode
  stays a blank to fill (section 2); public sandbox only (section 1, `publish`).

## Out of scope

- A GitLab sandbox, or any forge other than GitHub; a private sandbox.
- Changing the sandbox's project (`kit/sandbox/`), its base or the frozen CRs.
- Any change to the CLI (`skills/chantier/scripts/cli/`) or to a card other than the "Auto-fix
  events" and "Configuration" lines of `hosts/claude-code.md` named in section 5; a preflight check
  or a "For you" line for Auto-fix (the card says chantier stays silent in a normal batch).
- Making setup start the operator's session, or setting Claude Desktop's settings by script.
- A `--mode` option to `setup.py`.
- Running a campaign (this CR runs in a later batch, after batch-18's evals; the main checkout does
  not change during an eval).

## Evidence

- `just check` green (it runs `sandbox.py build` as a structure test: the base is unchanged, and
  `sandbox.json` keeps the maintainer's `repository`).
- `just eval-dry-run` at the pushed head, its output in `work/verifier/evidence/` and quoted in the
  PR body (`evals/README.md`, "Changing the kit"), with new cases:
  - `other-sandbox`: a `sandbox.local.json` naming another repository (a temporary copy, never the
    real file of the checkout) flows through setup (its first line names it, the run record's
    `repository`), `merge` (a link to the maintainer's repository is refused), the judge and the
    audit, the fake forge answering for that name;
  - `reset-foreign`: a local origin whose `main` does not hold the base, and one with a branch that
    does not: `reset` and `reset --yes` refuse (exit 2), and the origin's refs are unchanged;
  - `reset-empty`: an empty origin: `reset` refuses and names `publish`;
  - `publish`: an empty origin: the plan without `--yes` changes nothing; with `--yes` `main` is at
    the base and `sandbox.local.json` (in the case's temporary kit copy) names it; a second
    `publish --yes` on the now non-empty origin is refused;
  - `setup-prompt`: setup's `prompt` line for each sandbox campaign holds the checkout's absolute
    path and the runbook's path, and nothing in angle brackets but the mode for the quick
    campaigns; the workspace's `settings.local.json` of `real-foreman` holds the
    `mcp__ccd_pr__set_monitor` rule and that of `ticket-summary` does not.
  The dry run never reads or writes the checkout's real `sandbox.local.json` (it is absent from CI
  and may be present on a person's machine; the dry run must pass either way).
- No CI job is added or changed.
- The independent review of the whole campaign path (setup, a run, the audit, the judge) by a
  reviewer that did not write it, before the merge (README, "Changing the kit").
- The card change (`hosts/claude-code.md`) passes `just scenario (ubuntu-latest)` at the PR's head
  (AGENTS.md: a change to the cards).
- A read-through by the Verifier: following only `evals/README.md` from "Prerequisites", every
  command it names to stage and start `real-foreman` exists and is spelled as the kit takes it.
- Known gaps the PR names: the request's "done when" (a person who never ran one stages and starts
  `real-foreman`) and the operator's `set_monitor` call on a run's PR are proved only by the next
  real campaign.

## Open questions for the user

None: `02-answers.md`, answer 2, settled the four left by the first draft.
