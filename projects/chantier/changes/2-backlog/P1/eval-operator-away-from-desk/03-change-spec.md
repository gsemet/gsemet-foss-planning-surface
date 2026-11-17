# Change Specification: evals that start away from the desk

## Goal

The user can start a Claude eval campaign's operator session when away from the desk (from the
phone, under Remote Control), without the Claude Desktop app stopping to ask for trust in a new
folder. The user picks one eval root folder and trusts it once, at the desk. Every run then puts
its workspace inside that folder, so no run asks for trust again. Only the user grants trust:
chantier never edits a trust or security setting (`02-answers.md`, eval-away-Q1).

Why: v0.11.0 shipped with every claim `not exercised` because its two chosen campaigns
(`real-direct` in stack mode, `real-foreman` in parallel mode) could not start. A new workspace
folder needs the app's trust step, and the app shows that step only at the desk, never under
Remote Control (`intake/request.md`; batch-22's retro;
`evals/results/claims-v0.11.0.md`).

## Decisions carried

- **eval-away-Q1 (2026-11-17, the user's choice):** there is one eval root folder, which the user
  trusts once at the desk. Every run creates its workspace inside it, so no run asks for a new
  trust. The trust is the user's act. chantier (the CLI, the eval kit, the cards, the agents)
  never writes, edits or automates a trust or security setting of the host.
- The request's other option, a release CR that waits for the campaigns' reports, was not chosen.
  It is out of scope (below).

## What changes

### 1. The eval root, in `evals/README.md`

- **Prerequisites** (the list that starts "What a person needs to run a campaign"): the item
  "Claude Desktop, at the desk (not under Remote Control), for the start and its trust step"
  changes. It now names the **eval root**: one folder outside this repository, for example
  `../chantier-eval/` (the example the README already uses). The user trusts it once in Claude
  Desktop, at the desk, by opening a Code session on that folder and answering the app's trust
  question. That is the only step that needs the desk. The item says chantier never grants or
  edits that trust.
- **"A sandbox campaign", Preparation, step 4 (`setup.py`):** `<workspace>` is a new folder
  **inside the eval root**, for example `<eval root>/<campaign>-<date>`. The text says why: a
  workspace inside the trusted root inherits the root's trust (see the proof below), so the
  operator's session can start from Remote Control.
- **"The operator"** (the bullet that starts "**The operator** is a new Code session"): the
  **trust step** paragraph changes. A workspace inside the trusted eval root does not ask for
  trust. A workspace outside it still asks, and only at the desk, as the README says today. The
  bullet adds a third way to start the operator, next to the two that "worked on 2026-11-15":
  **away from the desk**. From the phone, under Remote Control, the user starts a new Code
  session on the workspace folder and pastes the `prompt` line. The README already says the user
  can do this from a phone ("The host's limits", "Starting the Foreman": "From a phone, the user
  starts the session and pastes the Foreman's prompt"). Until the trial below reports, this way is
  marked **unproved**, in the same words the README uses for its other unproved points.
- **The staged campaign** ("The steps", step 1, "Stage the workspace next to this checkout"): the
  example path is in the eval root too, so `claude-planted` gets the same benefit. Its setup
  (`main()` in `evals/kit/setup.py`) is otherwise unchanged.
- **"The host's limits"**, "Starting the Foreman": the paragraph also says that the trusted eval
  root removes only the trust step. It does not lift the host's rule that a session started or
  driven under Remote Control cannot start another session. See the open question on
  `real-foreman` and `full` below, and the hosts card's "Classes of session" table, row "Desktop,
  driven by Remote Control".

### 2. The runbooks

Each Claude sandbox runbook has a "Start" paragraph that says "The app asks to trust the new
folder, and can ask only at the desk, not under Remote Control (the evals README, \"The
operator\")". In each one, that sentence becomes: a workspace inside the trusted eval root does
not ask; one outside it asks, and only at the desk. The paragraph points to the evals README,
"The operator", for the away-from-the-desk start. The runbooks (paths before `evals-rework`; see
section 5):

- `evals/real-direct/RUNBOOK.md` (lines 26-30)
- `evals/real-foreman/RUNBOOK.md` (lines 33-38)
- `evals/full/RUNBOOK.md` (lines 36-41)
- `evals/ticket-summary/RUNBOOK.md` (lines 18-23)

Each runbook's Setup row (`uv run --no-project python evals/kit/setup.py <campaign> <workspace>`)
names the workspace as one inside the eval root. `evals/copilot/RUNBOOK.md` and
`evals/claude-planted/RUNBOOK.md` change only if they name a workspace path or a trust step
(the Driver checks).

### 3. `evals/kit/setup.py`

- The module docstring and the summary that `sandbox_main()` prints say that the workspace is
  meant to be inside the user's trusted eval root. The `workspace` line is still printed in the
  platform's own spelling.
- Setup never writes, reads or changes any host trust or security setting. That includes the
  app's or the CLI's trust records: `~/.claude.json` and the Claude Desktop app's own settings.
  The workspace's `.claude/settings.local.json` keeps exactly the allow rules `write_settings()`
  writes today, and nothing is added for trust.
- How setup knows the eval root, and whether it refuses or only warns about a workspace outside
  it, is open (question 1). The Driver implements the user's answer. If that answer adds a
  refusal or a warning, it gets a case in `evals/kit/dry_run.py` (next to `setup-prompt`) and its
  line in the README's kit table (`kit/setup.py` row).

### 4. The hosts card, `skills/chantier/references/hosts/claude-code.md`

Add one row to the host facts table (near "Preflight P2" and "Run the board"): **"Trust of a
workspace inside a trusted folder"**. Its value: a folder the user has trusted once in Claude
Desktop at the desk covers every new folder created inside it later, so a session started on such
a folder from Remote Control does not ask for trust. Its mark: **unproved**, with the trial in
the evidence below. The README's text and this row say the same thing. When the trial reports,
the row is marked proved or not from it (Evidence, "On Pass" and "On Fail"), with the date and the
machine, as the card's other rows are.

This edit changes a card. Under `AGENTS.md`, that puts the CR under the `just scenario`
(ubuntu-latest) gate before its PR. The card has no copy for Copilot (only the agent files are
per host), and Copilot's own trust behaviour is not changed.

### 5. Order with the pending CR `1-inbox/evals-rework`

`evals-rework` touches the same text. It moves `evals/full/RUNBOOK.md`,
`evals/real-foreman/RUNBOOK.md` and `evals/real-direct/RUNBOOK.md` to `evals/claude-full/`,
`evals/claude-real-foreman/` and `evals/claude-real-direct/`, deletes
`evals/ticket-summary/RUNBOOK.md` (with its kit), renames the result reports to
`results/<YYYY-MM-DD-HH-MM>-<campaign>...md`, and rewrites the same README Prerequisites item
(Claude Desktop's items become a group marked "On Claude Desktop") and "The operator" bullet (each
part says which host it holds for). Neither CR waits for the other. Whichever merges second
carries the other's edit:

- **If `evals-rework` merges first,** this CR makes its runbook edits (section 2) in
  `evals/claude-full/RUNBOOK.md`, `evals/claude-real-foreman/RUNBOOK.md` and
  `evals/claude-real-direct/RUNBOOK.md`, and drops the `evals/ticket-summary/RUNBOOK.md` edit,
  since that file is gone. It puts the eval root in the "On Claude Desktop" group of
  Prerequisites, and writes its "The operator" changes as Claude Desktop's, in that bullet's
  host-labelled form. Its setup examples and the trial use the campaign's new name
  (`claude-real-direct`), and the trial's report (Evidence) takes the new report naming.
- **If this CR merges first,** `evals-rework` carries this CR's eval-root text onto the renamed
  runbooks and into the host-labelled Prerequisites and "The operator". It drops only the
  `ticket-summary` runbook's eval-root text, with that file.

The Driver of the CR that merges second reads the other's merged text at its rebase and says, in
its PR body, which of the two cases it is.

## Out of scope

- Any change that grants, edits or automates trust: no write to `~/.claude.json`, to the
  Desktop app's settings or to any host security setting, and no instruction to an agent to do
  so (eval-away-Q1).
- Making the release CR wait for the campaigns' reports (the request's alternative, not chosen).
- Lifting the host's refusal to start a session from a session driven under Remote Control (the
  Foreman's start). That is the host's rule, and no setting changes it (README, "The host's
  limits").
- The Copilot app's trust (the `copilot` campaign).
- Completing `evals/results/claims-v0.11.0.md`. Its campaigns run under the existing process.
- The CLI (`skills/chantier/scripts/cli/`), the scenario and the agents: none changes.

## Evidence

- `just check` passes on Linux, macOS and Windows.
- `just eval-dry-run` passes at the pushed head, because the CR changes `evals/kit/`. Its output
  is the Verifier's evidence (`work/verifier/evidence/`), quoted in the PR body. If setup gains a
  refusal or a warning (question 1), the dry run has a case that proves it: a workspace outside
  the root is refused or warned about, and nothing is created.
- `just scenario` (ubuntu-latest) is green at the PR's head, because the hosts card changes.
- An independent review of the whole campaign path (setup, a run, the audit, the judge) before
  the merge, by a reviewer that did not write the change (README, "Changing the kit").
- **The trial that proves the trust inheritance (the user's, after the merge; no CI can run it):**
  1. At the desk, the user opens a Claude Desktop Code session on the eval root and answers the
     trust question.
  2. Away from the desk, after `sandbox.py reset --yes` and `setup.py real-direct <eval
     root>/real-direct-<date>`, the user starts a new Code session on that workspace from the
     phone under Remote Control and pastes the `prompt` line.
  3. **Pass:** no trust question, and the operator runs `$CHANTIER preflight --direct`.
     **Fail:** the app asks for trust or refuses to start. The run's report then records the
     failure as a finding.

  The first `real-direct` run after the merge is that trial. Its report
  (`evals/results/real-direct-<date>-run<n>.md`, or its name in the new report naming if
  `evals-rework` merged first, section 5) says which way it went.
  - **On Pass:** the hosts card row is marked proved, and the README's "unproved" goes.
  - **On Fail:** the PR that carries the trial's report also withdraws the eval-root start. The
    hosts card row records what was seen. The README's Prerequisites item, its setup step, "The
    operator" bullet and "The host's limits" paragraph, and each runbook's "Start" paragraph and
    Setup row, no longer say that a workspace inside the eval root skips the trust step, and no
    longer offer the away-from-the-desk start. They say again that the app asks to trust each new
    workspace, and only at the desk, as they said before this CR.

## Open questions

1. **How setup knows the eval root, and what it does with a workspace outside it.** The answer
   fixes the root and that every run's workspace goes inside it. It does not say whether setup
   enforces this. The options:
   (a) Documentation only: setup is unchanged apart from its text.
   (b) The user names the root once in a git-ignored local file, like
   `evals/kit/sandbox.local.json` (for example `evals/kit/eval-root.local.json`), and setup
   refuses a workspace outside it.
   (c) The same file, but setup only warns.
   (d) Setup takes the run's name and creates the workspace inside the named root itself.
   Recommended: (b). It keeps the guarantee that no run asks for trust, and it follows the kit's
   existing pattern for a person's own settings.
2. **Which campaigns can start away from the desk.** The operator starts the Foreman's session
   with `mcp__ccd_session__start_session`. The hosts card says a session driven under Remote
   Control cannot start a session ("refused, the message must be typed in the desktop app"). The
   README says the same of the Foreman ("needs a line typed in the desktop app"). The trusted root
   removes the trust step only, so a Foreman campaign (`real-foreman`, `full`) started from the
   phone may still stop at the Foreman's start. Should this CR say plainly that only the campaigns
   with no Foreman (`real-direct`, and `claude-planted`'s operator) start away from the desk, and
   the Foreman campaigns still need the desk for the Foreman's start? Or is the operator
   session's own start from the phone expected to be enough, so that the trial should also try
   `real-foreman` and record what the host does?
3. **Does a session started from the phone land on the main checkout of the workspace?** The
   README's away-from-the-desk start assumes the new Code session opens on the workspace folder
   itself. Under Remote Control, the app may start the session in a worktree of that folder, or
   on another folder than the one picked. Should the trial also check, at step 3, that the
   operator's session runs in the workspace's main checkout (its `git rev-parse --show-toplevel`
   is the workspace), and record a Fail if not?
