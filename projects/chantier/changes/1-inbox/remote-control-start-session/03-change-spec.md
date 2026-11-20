# Sessions start from Remote Control with no cwd

Change Specification, written 2026-11-20 from `intake/request.md`, `01-intent.md` and
`02-answers.md`. No issue.

## Goal

In the user's terms: "comment faire en sorte que la creation de sous session fonctionne toujours
même depuis remote", and "pour controller comment lancer les evals meme en remote". The Claude
Code host reference, the cards and the docs say how a session driven by Remote Control starts
another session (a Foreman, a Griller, an eval's operator) so that it works: with no `cwd` and no
`preset`, in its own folder. The evals can then be launched from the phone, Foreman campaigns
included.

## The facts this change writes down (01-intent.md, 2026-11-20, Battlestation)

- Remote Control refuses a start **in another place**, not a start: `start_session` with `cwd`
  (the planning surface; the eval root) or with a saved `preset` ("Battle Station") is refused with
  "The user is working over Remote Control, and this turn can't start that session".
- `start_session` with no `cwd`, `use_worktree: false`, starts, in the steering session's own
  folder (its main checkout: `--git-dir` equals `--git-common-dir`). Seen: the Studio's two
  Grillers and its batch-07 Foreman (Sonnet 5.5, effort medium), which claimed its batch and
  started a Driver; chantier's session `local_9ef60aad-22ce-4ab4-9dd6-80cf84213736`.
- That session then called `mcp__ccd_directory__change_directory` into
  `C:\Users\gaeta\Projets\chantier-eval` (inside the trusted `Projets` tree): granted with no
  question (auto mode, trusted folder); its next turn ran there (`pwd`).
- After the move its context still held the `AGENTS.md` of the folder it started in (chantier's):
  a move does not reload project instructions.
- The Chief of Staff's `clear_session` of that other session was denied by the auto mode
  classifier, and not retried.

## Decisions carried (02-answers.md)

1. **No-argument mode unchanged.** With no argument, a batch planned under the Remote Control
   notice stays **direct**; Foreman at the desk. The docs only stop saying that a Foreman cannot
   start there. A forced `foreman` under Remote Control now **starts a new Foreman with no `cwd`**
   (in the Chief of Staff's own folder), not only reuses the last one; the reuse stays offered as
   at the desk ("Reusing the last Foreman").
2. **The eval operator from the phone.** The route that works today: the steering session starts
   the operator with no `cwd`; the operator moves itself into the workspace with
   `change_directory` (no question inside the trusted tree) and runs its campaign from its next
   turn on. Isolation (the operator must not keep chantier's `AGENTS.md`) is settled by the trial
   below, its routes tried in answer 2's order, each recorded proved or not. No route depends on
   the Chief of Staff clearing another session, nor on asking another session to do what was
   denied.
3. **Foreman campaigns from the phone** (`real-foreman`, `full`): yes. The operator, once in the
   workspace, starts the Foreman with no `cwd`, so the Foreman lands on the workspace's main
   checkout. The evals README ("Prerequisites", "The operator", "Starting the Foreman" in "The
   host's limits") and the runbooks stop requiring the desk for this.
4. **Proof before the PR is ready:** the Studio's trial and the Chief of Staff's trials are
   quoted; the route of answer 2 is tried for real on this machine, from Remote Control (a start
   with no `cwd`, the move, the isolation check), its output in the evidence. The first eval run
   from the phone proves the campaigns end to end.

## What changes

### 1. `skills/chantier/references/hosts/claude-code.md`

- **The rule, stated once** (a short paragraph under "Classes of session", or a Tools row; the
  Driver picks the place): from a session driven by Remote Control, every session start
  (Foreman, Griller, operator) is `mcp__ccd_session__start_session` with **no `cwd` and no
  `preset`**, `use_worktree: false`; the new session lands in the steering session's own folder,
  which must be a main checkout (`git rev-parse --git-dir` equals `--git-common-dir`; a worktree
  session is unfit, as the worktree row says). The planning folder and everything else outside
  that folder reach the started session by absolute paths in its prompt: the CLI line (`$CHANTIER`
  already carries `--project <absolute folder>` on a surface, `session-start.md`), `Repository:`,
  `<skill>`, the brief's path. At the desk the same start works and stays the default; a `cwd` is
  never needed by chantier (no card names one today). Marked proved 2026-11-20 (the facts above,
  quoted with sessions and dates).
- **"Start the Foreman's session" row** (Tools): add "no `cwd`, no `preset`" to the call, and the
  mark "from Remote Control: proved 2026-11-20 (the Studio's batch-07 Foreman)".
- **A start from a session that moved** (new Tools row or a line under the rule): a session
  started with no `cwd` may move with `mcp__ccd_directory__change_directory` into a folder inside a
  trusted folder, with no question (proved 2026-11-20); the move does not reload project
  instructions (proved, same session); clearing another session from the Chief of Staff
  (`clear_session` on another id) is denied by the auto mode classifier (seen 2026-11-20): no
  chantier route uses it, nor asks another session to do it. What the trial of section 5 records
  (the self-clear, the folder of a start made by a moved session) goes in this row with its mark.
- **Classes of session, row "Desktop, driven by Remote Control"**: "Can start a session" becomes
  "yes, with no `cwd` and no `preset`, in its own folder; a start with `cwd` or `preset` is
  refused (proved 2026-11-20)"; "Fit for a Foreman" becomes "yes, on a main checkout: it starts a
  new Foreman in its own folder, or reuses the last one". The paragraph after the table that says
  "The refusal on a Remote Control session to start a session: proved in use" is rewritten to the
  new finding: what was proved in use was the refusal of a start with `cwd` (or `preset`).
- **The sentence "With no argument the Chief of Staff's batches are direct in the Remote Control
  row..."** stays (answer 1).
- **"A Chief of Staff and Grillers in remote" paragraph** (the 2026-11-10 finding): keep what is
  proved (batch-06: a session the user creates from the remote client's "Remote Control" entry
  lands in a worktree), and add what changed: a session started *by* a Chief of Staff driven by
  Remote Control, with no `cwd`, lands on that Chief of Staff's main checkout (proved 2026-11-20).
  So the Chief of Staff still starts locally (desktop, no worktree) and is put in remote; from
  there it can start a Foreman, and a Griller session on the user's word, in its own folder; a
  Griller in a never-merged worktree is no longer the only remote way. The "nested sessions are a
  problem in remote" clause goes, replaced by the proved rule.
- **"The trial that settles a new Foreman from a remote client"**: marked settled by the
  2026-11-20 trials for a Foreman started by the Chief of Staff (no `cwd`); what stays unproved is
  a session the user creates from the remote client's own New session on a chosen folder (answer
  2's second route), with its trial.
- **Surfaces and options table**: row "Switch to Foreman mode", Remote Control column: "yes: a
  new Foreman with no `cwd`, or a reused one", mark proved 2026-11-20; row "A host feature
  (scheduled wake, start a session, a monitor)", Remote Control column: "`start_session` with no
  `cwd` and no `preset` works; with either, refused", mark proved 2026-11-20. The paragraph above
  the table ("a forced `foreman` is the user's way") stays.
- **Row "Trust of a workspace inside a trusted folder"**: add the proved part: a
  `change_directory` into a folder inside the trusted tree asks nothing (2026-11-20); the start
  of a session *on* such a folder from the phone stays as marked until its trial.
- **"For you" blocks**: "A new Foreman, from a remote client" becomes "nothing for the user:
  the Chief of Staff starts it with no `cwd`, as at the desk" (proved), with the cost line kept
  (the Chief of Staff's session must be on the main checkout). "A Chief of Staff and Grillers in
  remote" is aligned with the rewritten paragraph above.
- **"Reusing the last Foreman"**: no change, except that it no longer reads as the only Remote
  Control way.

### 2. `skills/chantier/references/chief-of-staff.md`

- "Starting a batch", step 2, bullet "No argument": unchanged (direct under the notice, answer 1).
- Bullet "A forced `foreman` where no Foreman can start": drop "Remote Control with no Foreman to
  reuse" from the refused cases (a terminal, VS Code stay); say that under Remote Control a forced
  `foreman` starts a new Foreman in this session's own folder, as the host's reference says, or
  reuses the last one, as at the desk; this session must be fit for a Foreman (main checkout).
- Step 4's "Where the host refuses to start a session" sentence stays; it now only meets the
  cases the host's reference still refuses.
- "Switching to Foreman mode": "on Remote Control the switch needs a Foreman to reuse, else it is
  refused" goes; the switch under Remote Control starts a new Foreman or reuses one, like at the
  desk.
- The "Offering options" table row "Switch to Foreman mode" and refusals row A (a Griller "or a
  fork of this session on Remote Control") are kept true: a Griller session stays the user's step
  (unchanged; see Out of scope).
- The card names no host tool and no `cwd`: it says "as your host's reference says" (the test
  `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` in
  `skills/chantier/scripts/cli/tests/test_plugin_files.py` refuses `start_session` in a card).

### 3. Other cards and the skill

- `skills/chantier/references/session-start.md` (the mode line, line ~208; the remote fork line,
  line ~226) and `skills/chantier/references/init.md` (line ~47, "Direct mode is used where the
  session is under Remote Control..."): true as written after answer 1. The Driver re-reads them
  and changes only a sentence that says a session cannot start under Remote Control; none is
  expected. Settled by the Chief of Staff (2026-11-20, the user asks no questions).
- `skills/chief-of-staff/SKILL.md` description ("Foreman at the desktop, direct under Remote
  Control or where no Foreman can start"): true after answer 1; unchanged unless the Driver finds
  it says a Foreman cannot start under Remote Control.
- `skills/chantier/references/hosts/copilot.md`: unchanged (no Remote Control on Copilot).

### 4. Docs

Each says, in its own words, the rule of section 1 and answer 1; none keeps "a remote session
cannot start another session", "cannot start a Foreman under Remote Control" or "a forced
`foreman` is refused under Remote Control":

- `docs/planning-modes.md`, "Remote"; `docs/planning-modes-texts.md` (the Remote panel and the
  description paragraph); `docs/planning-modes.svg` (its `<desc>` and the Remote panel's text
  lines, kept identical to the texts file, the line widths within the panel). Settled by the Chief
  of Staff (2026-11-20, the user asks no questions): the SVG is in scope because the texts file
  is its source.
- `README.md` (the paragraph before the planning-modes figure) and `docs/use-cases.md` (the
  remote steps, item 1 to 4): the same finding and rule as the host reference's rewritten
  paragraph.
- `docs/use-cases-foreman.md` (line ~12) and `docs/use-cases-direct.md` (line ~11 stays true; the
  "Switch to Foreman mode" answer at line ~107 loses "needs a Foreman to reuse, else it is
  refused"). `docs/use-cases-foreman.md` is added to the scope list of 02-answers.md: settled by
  the Chief of Staff (2026-11-20, the user asks no questions), it repeats the old rule.
- `docs/hosts.md` (direct mode paragraph): direct stays the no-argument mode under Remote
  Control; one sentence that a forced `foreman` there starts the Foreman in the Chief of Staff's
  folder.
- `docs/tutorial-claude-code.md` (lines ~9, ~70, ~143): "Foreman mode starts the Foreman as a
  nested session, which only the Desktop app can do" stays; the no-argument rule stays; no
  sentence says Remote Control cannot start the Foreman.
- `evals/README.md`: "Prerequisites" (drop "A Foreman campaign still needs the desk ... only the
  campaigns with no Foreman start from the phone"); "The operator" (add the phone route of answer
  2 as the way away from the desk, for every campaign, written to the trial's result: the
  steering session starts the operator with no `cwd`, the operator's first step is
  `change_directory` into the workspace, then the isolation step the trial proved; the old "from
  the phone, start a new Code session on the workspace folder" stays as the second route with its
  mark); "The host's limits", "Starting the Foreman" (the sentence quoting the classes row
  "Desktop, driven by Remote Control" as forbidding a start goes; the operator starts the Foreman
  with no `cwd`, on the workspace's main checkout). The 10-message limit text stays. The trial
  paragraph names the first eval run from the phone as the end-to-end proof (answer 4).
- `evals/full/RUNBOOK.md` and `evals/real-foreman/RUNBOOK.md`, "Start": "(not under Remote
  Control)" and "This campaign needs the desk, to start the Foreman and type the go" go; the
  start from the phone is the evals README's route. `evals/real-foreman/RUNBOOK.md` is added to
  the scope: settled by the Chief of Staff (2026-11-20, the user asks no questions), answer 3
  names `real-foreman` and its runbook says the same. The go is typed by the user (or played by
  the operator, as each runbook already says) in the operator's session, from the phone or the
  desk alike. `evals/real-direct/RUNBOOK.md` and `evals/ticket-summary/RUNBOOK.md` point to "The
  operator" already: unchanged.

### 5. The trial on this machine (answer 4), and who runs it

A Driver is a subagent: it has no session tools (`start_session`, `change_directory`,
`clear_session`) and no Remote Control. Settled by the Chief of Staff (2026-11-20, the user asks
no questions):

1. The Driver writes sections 1 to 4 except the eval operator's isolation step, then writes the
   protocol below into the CR's folder as `evidence/remote-control-trial.md`, each step with
   `Result: pending`. It opens its PR as a draft and hands back `hand-back PR in draft <link>
   Remote Control trial pending: <absolute path of the file>`. The PR is not ready before the
   trial.
2. The Chief of Staff runs the trial from its own session while the user drives it from the phone
   (Remote Control notice present), on this machine, in a throwaway folder
   `<eval root>/rc-trial-<yyyymmdd>` (the eval root of `evals/kit/eval-root.local.json`), never in
   chantier's main checkout and never in a campaign's workspace. It writes each step's output and
   `Result: proved | not proved | not tried (<why>)` into the evidence file, with the date and
   the session ids.
3. The CR is resumed (a `take` with a note naming the file); the Driver writes the isolation step
   and the operator route into the evals README and the host reference to match the result, then
   readies the PR. A route not proved is written as not proved, with what was seen; nothing claims
   more than the file holds.

The protocol (`evidence/remote-control-trial.md`):

- **Setup.** In the throwaway folder, an `AGENTS.md` with one canary line (for example
  `Canary: rc-trial-<yyyymmdd>`), and no other instruction.
- **A. Start with no `cwd`.** From the Chief of Staff's session under Remote Control:
  `start_session` with no `cwd`, no `preset`, `use_worktree: false`, a prompt that asks for `pwd`,
  `git rev-parse --git-dir --git-common-dir --show-toplevel`, then the next steps. Expected:
  chantier's main checkout. Quote the output.
- **B. The move.** The started session calls `change_directory` to the throwaway folder; its
  next turn runs `pwd`. Expected: granted with no question, `pwd` the folder.
- **C. Isolation, in answer 2's order; stop at the first proved, record the rest "not tried":**
  - **C1. Self-clear.** The started session clears its own context (`clear_session` with
    `self`), as its prompt asked from the start (not a request sent after any refusal). The Chief
    of Staff then sends it one message asking whether its context holds the canary line and
    whether it holds chantier's `AGENTS.md` (for example its `## chantier` planning line), and,
    where the host's transcript file of that session is found, searches it after the clear for
    both. Proved when the canary is there and chantier's `AGENTS.md` is not. A self-clear the
    classifier refuses is "not proved", not retried, routed nowhere else.
  - **C2. The phone's New session.** The user, from the phone's own New session, opens a session
    on the throwaway folder, the Chief of Staff having given the folder (its native spelling) and
    a `prompt` line asking for the same `git rev-parse` and the canary question. Proved when the
    session is on the folder's own checkout (not a worktree; the folder is `git init`-ed for this
    step) and holds the canary only.
  - **C3. A neutral steering folder.** A steering session started at the desk in the eval root
    itself, put in Remote Control, starts a session with no `cwd`; that session lands in the eval
    root, moves with `change_directory` and answers the canary question. Proved when it holds no
    chantier `AGENTS.md`. This route needs the user at the desk once; the evidence says so.
- **D. A start from the moved session** (answer 3). The session that passed C (C1's, C2's or C3's)
  starts one throwaway session with no `cwd` whose prompt runs `git rev-parse --show-toplevel` and
  stops. Proved when it lands in the throwaway folder (the folder the Foreman of a campaign would
  land in). Not proved: the evals README and the runbooks say so, and the Foreman campaigns'
  phone route is written as unproved with what was seen.
- **Cleanup.** The throwaway sessions stopped by the user or by their own end; the throwaway
  folder removed by the Chief of Staff.

## Out of scope

- The no-argument mode (answer 1: unchanged).
- Who starts a Griller: a Griller session stays the user's step in the cards (`chief-of-staff.md`,
  refusals row A); the host reference only records that a start with no `cwd` works for one.
- Any CLI change: no command, no preflight check, no test of the CLI. `preflight.py`'s Remote
  Control warning (line ~179) is unchanged.
- Copilot (`hosts/copilot.md`, `com.github.copilot/`), the agents files, `hooks/`, `types/`.
- A route that uses the Chief of Staff's clear (or stop) of another session, or asks another
  session to do what was denied.
- The first eval from the phone itself (it proves the campaigns end to end, after this CR).
- The one-line message to the Studio's Chief of Staff: the Chief of Staff sends it once the PR is
  merged (its request), not the Driver.
- Release notes and versions (the release's own work).

## Host matrix

| Cell | Before | After |
| --- | --- | --- |
| Claude Desktop, typed, no argument | Foreman, started by `start_session` | same (no `cwd`, as always) |
| Claude Desktop, Remote Control, no argument | direct | direct (answer 1) |
| Claude Desktop, Remote Control, forced `foreman`, a Foreman to reuse | reuse | a new Foreman with no `cwd`, or the reuse |
| Claude Desktop, Remote Control, forced `foreman`, none to reuse | refused | a new Foreman with no `cwd` |
| Claude Desktop, Remote Control, eval operator | phone's New session (unproved), no Foreman campaign | start with no `cwd` + `change_directory` + the isolation step the trial proved; Foreman campaigns too |
| Terminal, VS Code | direct; forced `foreman` refused | unchanged |
| Copilot | per `hosts/copilot.md` | unchanged |

## Evidence

- `evidence/remote-control-trial.md` in the CR's folder, filled as section 5 says, quoted in the
  PR's Deliverables; the 2026-11-20 facts above quoted in the PR body.
- A search of the shipped files at the PR's head, its command and empty output in the PR: no
  match for `Can start a session | no`, `refused, the message must be typed`, `cannot start
  another session`, `needs the desk, to start the Foreman`, `needs a Foreman to reuse, else it is
  refused` in `skills/`, `docs/`, `evals/`, `README.md` (the search reads the repository's files
  as they ship, not a copy).
- `just check` green in the worktree at the rebased head (the existing
  `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` reads the shipped cards and
  keeps host tools out of them; no new test: the change is prose, and the project's tests check
  structure and the CLI's refusals).
- **Long gate, per the project's `AGENTS.md`:** the change touches the cards
  (`skills/chantier/references/`), so the pipeline's `just scenario (ubuntu-latest)` job is green
  at the PR's head before the PR is ready; a docs-and-eval-README change alone would owe none, but
  the cards make it owed. `just eval-dry-run` is not owed (nothing under the CLI's `src/` or
  `evals/kit/`); `just mod` is not owed (nothing under `hooks/` or `types/`). Windows coverage: if
  this CR is the top of its batch's stack, it also passes `just scenario` locally (`chantier
  gate`) at its head before the user merges.

## Open questions

None: the user asks no more questions; the points the answers left open are settled above and
marked "Settled by the Chief of Staff (2026-11-20, the user asks no questions)".
