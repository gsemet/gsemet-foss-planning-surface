# Change Specification: evals that start away from the desk

## Goal

The user can start a Claude eval campaign's operator session when away from the desk (from the
phone, under Remote Control), without the Claude Desktop app stopping to ask for trust in a new
folder. The user picks one eval root folder and trusts it once, at the desk. Every run then puts
its workspace inside that folder, so no run asks for trust again. Only the user grants trust:
chantier never edits a trust or security setting (`02-answers.md`, eval-away-Q1).

This holds for the campaigns with no Foreman. A Foreman campaign still needs the desk, to start
the Foreman and type the go (eval-away-Q3).

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
- **eval-away-Q2 (2026-11-17):** a git-ignored local file names the eval root
  (`evals/kit/eval-root.local.json`). Setup refuses a workspace outside it.
- **eval-away-Q3 (2026-11-17):** only the campaigns with no Foreman start away from the desk. The
  README, its Prerequisites and the Foreman campaigns' runbooks say plainly that a Foreman
  campaign still needs the desk, to start the Foreman and type the go.
- **eval-away-Q4 (2026-11-17):** the trial checks that the session started from the phone is on
  the workspace's main checkout: `git rev-parse --git-dir` equals `git rev-parse
  --git-common-dir`, and `git rev-parse --show-toplevel` is the workspace. Anything else is a
  Fail. The trial also records how the session was created from the phone.
- The request's other option, a release CR that waits for the campaigns' reports, was not chosen.
  It is out of scope (below).

## Which campaigns start away from the desk

From `CAMPAIGNS` in `evals/kit/setup.py`:

| Campaign | Foreman | Away from the desk |
|---|---|---|
| `real-direct` | no | yes |
| `ticket-summary` | no | yes |
| `claude-planted` | no | yes (its operator) |
| `real-foreman` | yes | no: the desk, to start the Foreman and type the go |
| `full` | yes | no: the desk, to start the Foreman and type the go |
| `copilot` | - | out of scope (the Copilot app's trust) |

The reason, said in the README: the operator starts the Foreman's session with
`mcp__ccd_session__start_session`, and the hosts card ("Classes of session", row "Desktop, driven
by Remote Control") says a session driven under Remote Control cannot start a session. The
trusted eval root removes the trust step only.

## What changes

### 1. The eval root file and `evals/kit/setup.py`

- **The file.** `evals/kit/eval-root.local.json`, written by the user, never by the kit. It names
  one absolute folder, outside this repository, for example `{"root": "C:/Users/<user>/chantier-eval"}`
  (the README's example `../chantier-eval/`, written absolute). It follows the pattern of
  `evals/kit/sandbox.local.json` (`sandbox.py`, `LOCAL`): a module-level path constant in the kit
  (so the dry run can point it at a temporary file, as it does for `sandbox.LOCAL`), one reader,
  and a malformed file stops setup with a message naming the file; it never falls back.
- **`.gitignore`** (the repository's root one): add `evals/kit/eval-root.local.json` next to
  `evals/kit/sandbox.local.json` (line 223 today).
- **The refusal.** In the `__main__` block of `setup.py`, before `sandbox_main()` or `main()` is
  called, so it covers every campaign: setup reads the root, resolves both paths, and refuses
  when the workspace (`sys.argv[2]`, resolved) is not a folder strictly inside the root. The
  message names the workspace, the root and the file it was read from, and says the workspace
  must be inside the trusted eval root. Nothing is created or changed on a refusal: no folder, no
  sandbox reset, no push. The refusal exits with the kit's precondition code (`sandbox.Stop` with
  `sandbox.PRECONDITION`, as setup's other refusals).
- **With no file**: setup refuses, names the file and shows the line to
  write in it. Nothing is created.
- **The text.** The module docstring and the summary `sandbox_main()` prints say that the
  workspace is inside the user's trusted eval root, and the first lines name the root and the
  file it was read from (as `sandbox.announce()` names `sandbox.local.json`). The `workspace` line
  is still printed in the platform's own spelling.
- **No trust write.** Setup never writes, reads or changes any host trust or security setting.
  That includes the app's or the CLI's trust records: `~/.claude.json` and the Claude Desktop
  app's own settings. The workspace's `.claude/settings.local.json` keeps exactly the allow rules
  `write_settings()` writes today, and nothing is added for trust. The eval root file holds the
  path only; it grants nothing.

### 2. `evals/kit/dry_run.py`

- Every case that runs setup points the kit's eval-root constant at a temporary
  `eval-root.local.json` naming the case's temporary root, and makes its workspace inside it,
  never reading the checkout's real file (as the cases do for `sandbox.LOCAL`, line 145).
- A new case next to `setup-prompt`, `eval-root`, listed in the module docstring's case list:
  (a) a workspace outside the root is refused with the kit's precondition exit code, the message
  names the root and the file, and nothing is created at the workspace path; (b) with the file
  absent, setup is refused the same way; (c) a malformed file is
  refused, naming the file; (d) a workspace inside the root goes through, and its
  `.claude/settings.local.json` holds the same allow rules as before this CR and no trust entry.
- The README's kit table (`kit/setup.py` row, and `kit/dry_run.py` if it lists cases) names the
  refusal and the new case.

### 3. `evals/README.md`

- **Prerequisites** (the list that starts "What a person needs to run a campaign"): the item
  "Claude Desktop, at the desk (not under Remote Control), for the start and its trust step"
  changes. It now names the **eval root**: one folder outside this repository, named in
  `evals/kit/eval-root.local.json`. The user trusts it once in Claude Desktop, at the desk, by
  opening a Code session on that folder and answering the app's trust question. chantier never
  grants or edits that trust. The item says plainly, as its own sentence, that a Foreman campaign
  (`real-foreman`, `full`) still needs the desk, to start the Foreman and type the go; only the
  campaigns with no Foreman start from the phone.
- **"A sandbox campaign", Preparation, step 4 (`setup.py`):** `<workspace>` is a new folder
  **inside the eval root**, for example `<eval root>/<campaign>-<date>`, and setup refuses any
  other. The text says why: a workspace inside the trusted root does not ask for trust (unproved
  until the trial reports, below), so the operator's session can start from Remote Control.
- **"The operator"** (the bullet that starts "**The operator** is a new Code session"): the
  **trust step** paragraph changes. A workspace inside the trusted eval root does not ask for
  trust. The bullet adds a third way to start the operator, next to the two that "worked on
  2026-11-15": **away from the desk**, for a campaign with no Foreman only. From the phone, under
  Remote Control, the user starts a new Code session on the workspace folder and pastes the
  `prompt` line. The session must be on the workspace's main checkout, not a worktree of it.
  Until the trial below reports, this way is marked **unproved**, in the same words the README
  uses for its other unproved points. The bullet says again that a Foreman campaign is started at
  the desk.
- **The staged campaign** ("The steps", step 1, "Stage the workspace next to this checkout"): the
  example path is in the eval root, since setup now refuses any other. Its setup (`main()` in
  `evals/kit/setup.py`) is otherwise unchanged.
- **"The host's limits"**, "Starting the Foreman": the paragraph says that the trusted eval root
  removes only the trust step. It does not lift the host's rule that a session started or driven
  under Remote Control cannot start another session, so a Foreman campaign needs the desk to start
  the Foreman and type the go. It points to the hosts card's "Classes of session" table, row
  "Desktop, driven by Remote Control".

### 4. The runbooks

Each Claude sandbox runbook has a "Start" paragraph that says "The app asks to trust the new
folder, and can ask only at the desk, not under Remote Control (the evals README, \"The
operator\")". In each one, that sentence becomes: the workspace is inside the trusted eval root,
so the app does not ask (setup refuses a workspace outside it). Each runbook's Setup row
(`uv run --no-project python evals/kit/setup.py <campaign> <workspace>`) names the workspace as
one inside the eval root. Then, per runbook (paths before `evals-rework`; see section 6):

- `evals/real-direct/RUNBOOK.md` (lines 26-30) and `evals/ticket-summary/RUNBOOK.md` (lines
  18-23): the "Start" paragraph points to the evals README, "The operator", for the start from the
  phone.
- `evals/real-foreman/RUNBOOK.md` (lines 33-38) and `evals/full/RUNBOOK.md` (lines 36-41): the
  "Start" paragraph says plainly that this campaign needs the desk, to start the Foreman and type
  the go, and that the eval root does not change that (README, "The host's limits").

`evals/copilot/RUNBOOK.md` and `evals/claude-planted/RUNBOOK.md` change only if they name a
workspace path or a trust step (the Driver checks); a workspace path they name moves inside the
eval root, since setup refuses any other.

### 5. The hosts card, `skills/chantier/references/hosts/claude-code.md`

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

### 6. Order with the pending CR `1-inbox/evals-rework`

`evals-rework` touches the same text. It moves `evals/full/RUNBOOK.md`,
`evals/real-foreman/RUNBOOK.md` and `evals/real-direct/RUNBOOK.md` to `evals/claude-full/`,
`evals/claude-real-foreman/` and `evals/claude-real-direct/`, deletes
`evals/ticket-summary/RUNBOOK.md` (with its kit), renames the result reports to
`results/<YYYY-MM-DD-HH-MM>-<campaign>...md`, and rewrites the same README Prerequisites item
(Claude Desktop's items become a group marked "On Claude Desktop") and "The operator" bullet (each
part says which host it holds for). Neither CR waits for the other. Whichever merges second
carries the other's edit:

- **If `evals-rework` merges first,** this CR makes its runbook edits (section 4) in
  `evals/claude-full/RUNBOOK.md`, `evals/claude-real-foreman/RUNBOOK.md` and
  `evals/claude-real-direct/RUNBOOK.md`, and drops the `evals/ticket-summary/RUNBOOK.md` edit and
  the `ticket-summary` row of the campaign table, since that campaign is gone. It puts the eval
  root and the Foreman campaigns' desk sentence in the "On Claude Desktop" group of
  Prerequisites, and writes its "The operator" changes as Claude Desktop's, in that bullet's
  host-labelled form. Its setup examples, the dry run and the trial use the campaigns' new names
  (`claude-real-direct`), and the trial's report (Evidence) takes the new report naming.
- **If this CR merges first,** `evals-rework` carries this CR's eval-root text and setup's refusal
  onto the renamed runbooks and campaigns and into the host-labelled Prerequisites and "The
  operator". It drops only the `ticket-summary` runbook's eval-root text, with that file.

The Driver of the CR that merges second reads the other's merged text at its rebase and says, in
its PR body, which of the two cases it is.

## Out of scope

- Any change that grants, edits or automates trust: no write to `~/.claude.json`, to the
  Desktop app's settings or to any host security setting, and no instruction to an agent to do
  so (eval-away-Q1).
- Making the release CR wait for the campaigns' reports (the request's alternative, not chosen).
- Starting a Foreman campaign away from the desk, and lifting the host's refusal to start a
  session from a session driven under Remote Control. That is the host's rule, and no setting
  changes it (README, "The host's limits"; eval-away-Q3).
- The Copilot app's trust (the `copilot` campaign).
- Completing `evals/results/claims-v0.11.0.md`. Its campaigns run under the existing process.
- The CLI (`skills/chantier/scripts/cli/`), the scenario and the agents: none changes.

## Evidence

- `just check` passes on Linux, macOS and Windows.
- `just eval-dry-run` passes at the pushed head, because the CR changes `evals/kit/`, with the
  new `eval-root` case (section 2) green. Its output is the Verifier's evidence
  (`work/verifier/evidence/`), quoted in the PR body.
- `just scenario` (ubuntu-latest) is green at the PR's head, because the hosts card changes.
- An independent review of the whole campaign path (setup, a run, the audit, the judge) before
  the merge, by a reviewer that did not write the change (README, "Changing the kit").
- **The trial that proves the trust inheritance (the user's, after the merge; no CI can run it):**
  1. At the desk, the user writes `evals/kit/eval-root.local.json`, opens a Claude Desktop Code
     session on the eval root and answers the trust question.
  2. Away from the desk, after `sandbox.py reset --yes` and `setup.py real-direct <eval
     root>/real-direct-<date>`, the user starts a new Code session on that workspace from the
     phone under Remote Control and pastes the `prompt` line.
  3. Before `preflight`, the operator runs, in its session, `git rev-parse --git-dir`, `git
     rev-parse --git-common-dir` and `git rev-parse --show-toplevel`, and the report quotes their
     output.
  4. **Pass:** no trust question; the session is on the workspace's main checkout (the first two
     outputs are the same folder, and the top level is the workspace); and the operator runs
     `$CHANTIER preflight --direct`. **Fail:** anything else: the app asks for trust or refuses
     to start, the session is in a worktree of the workspace, or its top level is another folder.
     The run's report records the failure as a finding.
  5. The report records how the session was created from the phone: the app (Claude mobile app
     or browser), the screen and the choices made (folder picked, worktree option if any), in the
     user's words.

  The first `real-direct` run after the merge is that trial. Its report
  (`evals/results/real-direct-<date>-run<n>.md`, or its name in the new report naming if
  `evals-rework` merged first, section 6) says which way it went.
  - **On Pass:** the hosts card row is marked proved, and the README's "unproved" goes.
  - **On Fail:** the PR that carries the trial's report also withdraws the away-from-the-desk
    start. The hosts card row records what was seen. The README's Prerequisites item, its setup
    step, "The operator" bullet and "The host's limits" paragraph, and each runbook's "Start"
    paragraph, no longer say that a workspace inside the eval root skips the trust step, and no
    longer offer the away-from-the-desk start. They say again that the app asks to trust each new
    workspace, and only at the desk, as they said before this CR. Whether setup keeps refusing a
    workspace outside the root is that PR's question for the user.

## Open questions

None. The Chief of Staff settled the last one (2026-11-17), as the user's answer to eval-away-Q2
leads: with no `eval-root.local.json`, setup refuses, naming the file and the line to write in
it; nothing is created (no fallback, and no run asks for trust).
