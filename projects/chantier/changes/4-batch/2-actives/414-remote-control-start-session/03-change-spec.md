# Sessions start from Remote Control with no cwd

Change Specification, written 2026-11-20 from `intake/request.md`, `01-intent.md` and
`02-answers.md`, revised the same day with the spec critic's seven findings, as the Chief of Staff
settled them. No issue.

This CR is **part A** of the request: the rule for starting the Foreman and Grillers from Remote
Control. **Part B**, starting an eval's operator from the phone (`evals/README.md`, the `full` and
`real-foreman` runbooks, the real trial from the phone, and the self-clear), leaves this CR. The
Chief of Staff files it as its own CR. Settled by the Chief of Staff (2026-11-20, the user asks no
questions; critic findings 3, 4 and 6).

## Goal

In the user's terms: "comment faire en sorte que la creation de sous session fonctionne toujours
même depuis remote". The Claude Code host reference, the cards and the docs say how a session
driven by Remote Control starts another session (a Foreman, a Griller) so that it works: with no
`cwd` and no `preset`, in the steering session's own folder.

## The facts this change writes down (01-intent.md, 2026-11-20, Battlestation)

- Remote Control refuses a start **in another place**, not every start: `start_session` with a
  `cwd` (the planning surface; the eval root) or with a saved `preset` ("Battle Station") is
  refused with "The user is working over Remote Control, and this turn can't start that session".
- `start_session` with no `cwd` and `use_worktree: false` starts the session in the steering
  session's own folder, its main checkout (`--git-dir` equals `--git-common-dir`). This was seen
  in both setups below.
- A session started with no `cwd` can move with `mcp__ccd_directory__change_directory` into a
  folder inside the trusted `Projets` tree with no question asked (auto mode, trusted folder); its
  next turn runs there (`pwd`). The move does not reload project instructions: the session keeps
  the `AGENTS.md` of the folder it started in.
- The Chief of Staff's `clear_session` of another session was denied by the auto mode classifier,
  and not retried.

**The two setups of the steering session's folder, both seen in use.** Settled by the Chief of
Staff (2026-11-20, the user asks no questions; critic finding 1).

1. **The planning surface's checkout** (the documented external mode, `session-start.md`).
2. **The project's main checkout, with the planning surface added as a working directory.** Seen
   twice:
   - The Studio's Chief of Staff ran in the Studio's main checkout. Its batch-07 Foreman (Sonnet
     5.5, effort medium), started with no `cwd`, landed there, passed its worktree check, claimed
     its batch, wrote to the surface by absolute paths and started a Driver. Two Grillers were
     started the same way.
   - chantier's own Chief of Staff runs in `C:\Users\gaeta\Projets\chantier` with the surface
     added. Its batch-29 Foreman landed in `C:\Users\gaeta\Projets\chantier`, and session
     `local_9ef60aad-22ce-4ab4-9dd6-80cf84213736` was started there too.

In both setups the started session lands in the steering session's own folder. Everything outside
that folder reaches it by absolute paths in its prompt:

- on a surface, `$CHANTIER` already carries `--project <absolute folder>` (`session-start.md`,
  section 2);
- the Foreman's prompt already gives `Repository:` and `<skill>` as absolute paths
  (`chief-of-staff.md`, "Starting a batch", step 4).

## Decisions carried (02-answers.md)

1. **The mode with no argument does not change.** With no argument, a batch planned under the
   Remote Control notice stays **direct**; it is Foreman at the desk. The docs only stop saying
   that a Foreman cannot start under Remote Control. A forced `foreman` under Remote Control now
   **starts a new Foreman with no `cwd`**, in the Chief of Staff's own folder, instead of only
   reusing the last one. Reusing it stays offered, as at the desk ("Reusing the last Foreman").
2. **The eval operator from the phone:** moves to part B. Part A only records the move with
   `change_directory` as proved (the facts above), not the operator's route.
3. **Foreman campaigns from the phone:** moves to part B.
4. **Proof before the PR is ready.** For part A, the Chief of Staff's trials and the Studio's trial
   of 01-intent.md are the "trial here". The PR quotes them. Part A needs no new trial and no
   draft PR to resume later. Part B carries the real trial from the phone. Settled by the Chief of
   Staff (2026-11-20, the user asks no questions; critic finding 3).

## What changes

### 1. `skills/chantier/references/hosts/claude-code.md`

- **State the rule once**, either as a short paragraph under "Classes of session" or as a Tools
  row; the Driver picks the place.
  - From a session driven by Remote Control, every session start (Foreman, Griller) is
    `mcp__ccd_session__start_session` with **no `cwd` and no `preset`** and `use_worktree: false`.
  - The new session lands in the steering session's own folder. That folder must be a main
    checkout: either the surface's checkout, or the project's main checkout with the surface added
    as a working directory (the two setups above). A worktree session is unfit, as the worktree row
    says.
  - What lies outside that folder reaches the new session by absolute paths in its prompt.
  - At the desk the same start works and stays the default. No card names a `cwd` today, and
    chantier never needs one.
  - Mark it proved 2026-11-20, quoting the sessions and dates above.
- **"Start the Foreman's session" row** (Tools): add "no `cwd`, no `preset`" to the call, and the
  mark "from Remote Control: proved 2026-11-20 (the Studio's batch-07 Foreman)".
- **The move.** A session started with no `cwd` may move with
  `mcp__ccd_directory__change_directory` into a folder inside a trusted folder, with no question
  asked; the move does not reload project instructions. Both are proved 2026-11-20 (01-intent.md).
  Record this in the "Trust of a workspace inside a trusted folder" row, or in a line under the
  rule. Two more facts go with it:
  - Clearing another session from the Chief of Staff (`clear_session` on another id) is denied by
    the auto mode classifier (seen 2026-11-20). No chantier route uses it.
  - What is not recorded here: the operator's route, the self-clear, and where a session started by
    a moved session lands. All three are part B's.
- **Classes of session, row "Desktop, driven by Remote Control":**
  - "Can start a session" becomes "yes, with no `cwd` and no `preset`, in its own folder; a start
    with `cwd` or `preset` is refused (proved 2026-11-20)".
  - "Fit for a Foreman" becomes "yes, on a main checkout: it starts a new Foreman in its own
    folder, or reuses the last one".
  - The paragraph after the table says "The refusal on a Remote Control session to start a session:
    proved in use". Rewrite it: what was proved in use was the refusal of a start with a `cwd` (or a
    `preset`).
- **Classes of session, row "Session in a planning surface":** make it true for both setups.
  - The surface's checkout (as today).
  - Or the project's main checkout with the surface added as a working directory: the
    sessions run there, write the planning folder by absolute paths, and a session started with
    no `cwd` lands there (proved 2026-11-20, the Studio's batch-07 Foreman and chantier's
    batch-29 Foreman).
  - Who plans where does not change.
- **The sentence "With no argument the Chief of Staff's batches are direct in the Remote Control
  row..."** stays (answer 1).
- **The paragraph "A Chief of Staff and Grillers in remote"** (the 2026-11-10 finding):
  - Keep what is proved: batch-06 showed that a session the user creates from the remote client's
    "Remote Control" entry lands in a worktree.
  - Add what changed: a session started *by* a Chief of Staff driven by Remote Control, with no
    `cwd`, lands on that Chief of Staff's main checkout (proved 2026-11-20).
  - So the Chief of Staff still starts locally (desktop, no worktree) and is then put in remote.
    From there it can start a Foreman in its own folder, and a Griller session on the user's word.
    A Griller in a never-merged worktree is no longer the only way to have a Griller in remote.
  - The clause "nested sessions are a problem in remote too" goes, replaced by the proved rule.
- **"The trial that settles a new Foreman from a remote client":** mark it settled by the
  2026-11-20 trials for a Foreman started by the Chief of Staff with no `cwd`. A session the user
  creates from the remote client's own New session on a chosen folder stays unproved, with its
  trial (part B tries it).
- **Surfaces and options table:**
  - Row "Switch to Foreman mode", Remote Control column: "yes: a new Foreman with no `cwd`, or a
    reused one", marked proved 2026-11-20.
  - Row "A host feature (scheduled wake, start a session, a monitor)", Remote Control column:
    "`start_session` with no `cwd` and no `preset` works; with either, it is refused", marked proved
    2026-11-20.
- **"For you" blocks:**
  - "A new Foreman, from a remote client" becomes "nothing for the user: the Chief of Staff starts
    it with no `cwd`, as at the desk" (proved). Keep the cost line: the Chief of Staff's session
    must be on a main checkout.
  - "A Chief of Staff and Grillers in remote" follows the rewritten paragraph above.
- **"Reusing the last Foreman":** no change, except that it no longer reads as the only way under
  Remote Control.

### 2. `skills/chantier/references/chief-of-staff.md`

- "Starting a batch", step 2, bullet "No argument": unchanged (direct under the notice, answer 1).
- Bullet "A forced `foreman` where no Foreman can start":
  - drop "Remote Control with no Foreman to reuse" from the refused cases; a terminal and VS Code
    stay refused;
  - say that under Remote Control a forced `foreman` starts a new Foreman in this session's own
    folder, as the host's reference says, or reuses the last one, as at the desk;
  - this session must be fit for a Foreman (a main checkout).
- Step 4's sentence "Where the host refuses to start a session" stays; it now only covers the cases
  the host's reference still refuses.
- "Switching to Foreman mode": "on Remote Control the switch needs a Foreman to reuse, else it is
  refused" goes. Under Remote Control the switch starts a new Foreman or reuses one, as at the desk.
- Refusals row A ("a Griller session, or a fork of this session on Remote Control") stays true: a
  Griller session stays the user's step (see Out of scope).
- The card names no host tool and no `cwd`; it says "as your host's reference says". The test
  `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` in
  `skills/chantier/scripts/cli/tests/test_plugin_files.py` refuses `start_session` in a card.

### 3. `skills/chantier/references/session-start.md` and the other cards

- `session-start.md`, section 1, the bullet "With a planning surface, 'the main checkout' is the
  surface's checkout...": make it true for the second setup too. The main checkout is the
  surface's checkout, or the project's main checkout with the surface added as a working directory.
  In both, the planning folder is the surface's project folder, written by absolute paths, and the
  project's clone of `checkout.yml` hosts no session.
- The pointer line stays exactly as it is: a session started alone in the project, without the
  surface added, still says "this project plans in the surface at <url>; start the session there"
  and plans nothing in the project. Who plans where does not change. The Driver words how a session
  tells the two cases apart: the surface added as a working directory, and `$CHANTIER` given
  `--project` in it. Settled by the Chief of Staff (2026-11-20, the user asks no questions; critic
  finding 1).
- `session-start.md`'s mode line (around line 208) and its remote fork line (around line 226), and
  `init.md` (around line 47): already true after answer 1. The Driver re-reads them and changes only
  a sentence that says a session cannot start under Remote Control. None is expected.
- `skills/chief-of-staff/SKILL.md` (its description): true after answer 1; unchanged.
- `skills/chantier/references/hosts/copilot.md`: unchanged.

### 4. Docs

Each doc says, in its own words, the rule of section 1 and answer 1. None keeps "a remote session
cannot start outside a worktree", "nested sessions are a problem", or "a forced `foreman` is
refused under Remote Control / needs a Foreman to reuse".

- `docs/planning-modes.md`, "Remote".
- `docs/planning-modes-texts.md`: the Remote panel and the description paragraph.
- `docs/planning-modes.svg`: its `<desc>` and the Remote panel's text lines, kept identical to the
  texts file, with line widths that fit the panel. The SVG is in scope because the texts file is
  its source.
- `README.md` (the paragraph before the planning-modes figure) and `docs/use-cases.md` (the remote
  steps, items 1 to 4): the same finding and rule as the host reference's rewritten paragraph.
- `docs/use-cases-direct.md`:
  - line 87: "a Remote Control session with no Foreman to reuse" becomes "a Remote Control
    session";
  - line 107: "Switch to Foreman mode" loses "needs a Foreman to reuse, else it is refused".
- `docs/use-cases-foreman.md`, line 12: under Remote Control, a forced `foreman` starts the Foreman
  in the Chief of Staff's folder. The no-argument mode stays direct there.
- `docs/hosts.md`, the direct mode paragraph: direct stays the no-argument mode under Remote
  Control. Add one sentence: a forced `foreman` there starts the Foreman in the Chief of Staff's
  folder. Line 16 is about the terminal and VS Code and stays.
- `docs/tutorial-claude-code.md`: no sentence there says Remote Control cannot start the Foreman.
  The Driver re-reads it (lines 9, 70, 143, 250) and changes nothing that is still true.

## Out of scope

- Part B: the eval operator from the phone, which the Chief of Staff files as its own CR. It covers
  answers 2, 3 and 4's real trial from the phone, critic findings 2, 4 and 6, `evals/README.md`,
  `evals/full/RUNBOOK.md`, `evals/real-foreman/RUNBOOK.md`, the trial file, and the host reference
  rows for the self-clear and the operator route.
- The mode with no argument (answer 1: unchanged).
- Who starts a Griller: a Griller session stays the user's step in the cards (`chief-of-staff.md`,
  refusals row A). The host reference only records that a start with no `cwd` works for one.
- Who plans where: the pointer line and the in-project versus external modes are unchanged.
- Any CLI change, `hooks/`, `types/`, Copilot, and the agents files.
- Any route that uses the Chief of Staff's clear or stop of another session, or asks another
  session to do what was denied.
- After this merges, the Chief of Staff:
  - fixes line 216 of batch-takeover's specification to "starts a new Foreman with no `cwd`, or
    reuses one";
  - re-reads evals-rework before it is taken;
  - tells the Studio's Chief of Staff in one line (its request).

  None of this is the Driver's work. Settled by the Chief of Staff (2026-11-20, the user asks no
  questions; critic finding 7).
- Release notes and versions.

## Host matrix

| Cell | Before | After |
| --- | --- | --- |
| Claude Desktop, typed, no argument | Foreman, started by `start_session` | same (no `cwd`, as always) |
| Claude Desktop, Remote Control, no argument | direct | direct (answer 1) |
| Claude Desktop, Remote Control, forced `foreman`, a Foreman to reuse | reuse | a new Foreman with no `cwd`, or the reuse |
| Claude Desktop, Remote Control, forced `foreman`, none to reuse | refused | a new Foreman with no `cwd` |
| Steering folder: the surface's checkout | documented | unchanged |
| Steering folder: the project's main checkout, surface added | not described | described in `session-start.md` and the hosts card; the Foreman lands there |
| Terminal, VS Code | direct; forced `foreman` refused | unchanged |
| Copilot | per `hosts/copilot.md` | unchanged |

## Evidence

- **The 2026-11-20 facts above**, quoted in the PR body with their sessions: the Studio's trial and
  the Chief of Staff's trials of 01-intent.md, plus the batch-29 Foreman's landing folder. No new
  trial.
- **A search of the shipped files.** Each pattern below matches at today's base (`d7b5a019`) and
  must return nothing at the PR's head. Run it with
  `grep -rnF "<pattern>" skills docs README.md --include=*.md --include=*.svg`, on the repository's
  files as they ship, not a copy, and put the command and its output at the base and at the head in
  the PR. Settled by the Chief of Staff (2026-11-20, the user asks no questions; critic finding 5).

  The list, run at the base on 2026-11-20 (files this CR owns only; `evals/` is part B's):

  | Pattern | Matches at the base |
  | --- | --- |
  | `no: refused, the message must be typed` | `skills/chantier/references/hosts/claude-code.md:582` |
  | `Foreman to reuse, else` | `skills/chantier/references/chief-of-staff.md:1841`, `docs/use-cases-direct.md:107` |
  | `Remote Control with no Foreman to reuse` | `skills/chantier/references/chief-of-staff.md:872` |
  | `with no Foreman to reuse` | `chief-of-staff.md:872`, `docs/use-cases-direct.md:87` |
  | `nested sessions are a problem` | `skills/chantier/references/hosts/claude-code.md:608` |
  | `cannot start outside a worktree` | `docs/planning-modes-texts.md:3,32`, `docs/planning-modes.svg:3,38`, `docs/use-cases.md:119` |
  | `only by reusing a Foreman` | `skills/chantier/references/hosts/claude-code.md:646` |
  | ``start_session` is refused (classes table)`` | `skills/chantier/references/hosts/claude-code.md:655` |
  | `start a session: proved in use` | `skills/chantier/references/hosts/claude-code.md:596` |

  Some old wordings wrap across lines and need a reading check named in the PR: `README.md` lines
  76–78 ("a remote session cannot start / outside a worktree") and `docs/planning-modes.md` lines
  152–157 ("a remote session cannot be / started outside a worktree", "nested sessions are / a
  problem").
- **`just check`** green in the worktree at the rebased head. The existing
  `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` reads the shipped cards and
  keeps host tools out of them. No new test: the change is prose, and the project's tests check
  structure and the CLI's refusals.

## Gates (the project's `AGENTS.md`)

- **`just check`** before the hand-back. The Driver runs it in the worktree at the rebased head it
  pushes, before the first push.
- **Long gate:** this CR changes the cards (`skills/chantier/references/`), so the pipeline's
  `just scenario (ubuntu-latest)` job must be green at the PR's head before the PR is ready. A
  change to the docs alone would owe none; the cards make it owed.
- **Windows coverage:** if this CR is on top of its batch's stack, it also passes `just scenario`
  locally (`chantier gate`) at its head before the user merges. When a CR joins on top of it, the
  local run moves to that CR.
- **Not owed:** `just eval-dry-run` (nothing under the CLI's `src/` or `evals/kit/`) and `just mod`
  (nothing under `hooks/` or `types/`).

## Open questions

None. The user asks no more questions. Each point the answers and the critic left open is settled
above and marked "Settled by the Chief of Staff (2026-11-20, the user asks no questions)".
