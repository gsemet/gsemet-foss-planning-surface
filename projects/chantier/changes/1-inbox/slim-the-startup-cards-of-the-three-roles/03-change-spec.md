# Slim the startup cards of the Chief of Staff, Foreman and Driver

Short name: `slim-cards`. Base: `slim-session-start` (`slim-session-start-md-split-by-role-forg`),
which this CR waits for and rebases onto (slim-cards-Q2).

## Goal

In the owner's words (2026-11-23): the Chief of Staff, the Foreman and the Driver still read
very large cards; slim them without breaking anything: the right instruction must arrive at the
right moment, by the right means. Each big card is cut by moment of need, and each piece is an
action of `startup-manifest.json`, read when its situation arrives (slim-cards-Q1). The goal is
about half of each role's start reading, measured before and after (slim-cards-Q3). The proof
is a table of every moved rule with its action, a test that every rule is reached by an action,
and a Fable advisor reading each role's split (slim-cards-Q4).

## Where it stands (measured on `main` at f4c1bccd, 2026-11-23)

A role's **start reading** is what it reads before its first act of work, as the manifest
defines it, measured in LF bytes with each byte counted once (the union rule of
`test_startup_manifest.py`'s `_unique_startup_bytes`):

| Role | Start reading | Bytes (Claude host) |
|---|---|---|
| Chief of Staff | boot (`startup-core.md`, `host-core-*.md`, `role-core.md`, `startup-manifest.json`, `skills/chief-of-staff/SKILL.md` with its `Startup core`) + action `session-start` + action `chief-of-staff` | 363,700 |
| Foreman | boot (the cores, the manifest, `startup_sections.foreman`) + action `batch` | 275,457 |
| CR Driver | boot (the cores, the manifest, `agents/cr-driver.md`, `driver.md#Startup core`) + `driver.md`'s opening + action `cr-driver` | 22,604 |

The heavy parts: `chief-of-staff.md` is 200,336 bytes, read whole by the `chief-of-staff`
action (and by `writer`); `foreman.md` is 82,872 bytes and `concepts.md` 71,611, both read
whole by `batch`; `driver.md` is 133,540 bytes, already read by sections (CR-driver steps
`cr-driver`, `cr-driver:ship`, `cr-driver:closing`), but twenty of its sections are reached
only by a link, by no action. The `chief-of-staff` and `batch` actions also list
`hosts/claude-code.md` (97,766) and `hosts/copilot.md` (18,746) whole.

These are today's figures. The CR's **before** figures are taken again at the base, once
`slim-session-start` is merged and this CR rebased onto it (it changes `session-start.md` and the
manifest), with the same measure; the PR states both.

## What changes

The order of work is the user's: the Chief of Staff, then the Foreman, then the Driver
(slim-cards-Q2), one commit per role at least, each with its own table of moved instructions.

### Rules common to the three cuts

- **The entry cards keep their names.** `chief-of-staff.md`, `foreman.md` and `driver.md` stay
  where they are, each keeping its opening, its `Startup core` when it has one, and what its role
  needs at every moment of its work. The CLI's prompts (`driver_prompt.py`'s `Card:` line naming
  `driver.md`), the eval kit (`evals/kit/audit.py`, `evals/kit/dry_run.py`, which name
  `driver.md`), the wrappers in `agents/` and `com.github.copilot/agents/` and the manifest's
  `roles` map stay valid with no change. No file under `skills/chantier/scripts/cli/src/` or
  `evals/kit/` changes.
- **Each moved piece is a new card** beside them in `skills/chantier/references/`, named
  `<role>-<moment>.md` as `foreman-stack.md` is (for instance `chief-of-staff-grill.md`,
  `chief-of-staff-batch-start.md`, `foreman-merge.md`, `driver-trouble.md`), each with a `#` title
  and level-2 sections, so that a manifest reading can name `file#heading`.
- **Each piece is an action** in `startup-manifest.json`'s `actions`, named `<role>:<moment>`
  as `cr-driver:ship` is. An action lists every reading that moment needs, so a rule read today at
  that moment is still read at it: when a moved text was read by several actions, each of them
  lists its new place.
- **Each entry card says when each of its actions is read**: one short list of moments (as
  `driver.md`'s "Deferred:" item does today), one line per action: the moment, then the action's
  name. A moment the card does not name is a lost rule.
- **Text moves, it is not rewritten.** A moved rule keeps its words; only its links change (an
  anchor like `chief-of-staff.md#steering-a-batch-yourself` or
  `foreman.md#a-drivers-refused-force-push` names the new file). Every inbound link is updated:
  the cards, `hosts/copilot.md`, `routing.md`, `skills/chief-of-staff/SKILL.md`'s `Startup core`
  ("`chief-of-staff.md`, Starting a batch" names its new place), `docs/` and
  `evals/real-direct/RUNBOOK.md`. No rule is added, none dropped; a duplicate found is said in the
  PR, not merged away.
- **What is read at boot does not grow past the limit.** Every role reads
  `startup-manifest.json` whole at boot, and the test holds each role's boot and reload under
  12,544 bytes; the Chief of Staff's reload is at 12,515 today. The new actions grow the manifest:
  the Driver measures that growth at the base before it writes the cut and follows the answer to
  the open question 1. It never raises `limit` or `STARTUP_LIMIT` on its own.
- **No other card is cut.** `concepts.md`, `hosts/claude-code.md` and `hosts/copilot.md` keep
  their text and their place; how an action reads them is the open question 2.

### 1. The Chief of Staff (`chief-of-staff.md`)

Today read whole by `chief-of-staff` and `writer`. Target cut, by its sections (sizes in bytes):

| Moment | New action | Moves there from `chief-of-staff.md` |
|---|---|---|
| any moment of the session (stays) | `chief-of-staff` | opening, Entry points (7,628), Hard rules (3,317), The project (11,744), Handing the seat over, Subagents and the demo, Never |
| filing, moving or grilling a CR, starting the Spec-writer and the spec critic | `chief-of-staff:grill` | Backlog and grill (38,762); finer pieces by its bold items when one moment needs only part (filing and moves, the grill, the specification's steps) |
| the user's "run them" up to the Foreman's start or `open --direct` | `chief-of-staff:batch-start` | Forge permissions (P9), The trials before the go, Starting a batch with The floor (holds the Foreman's prompt: `entries.foreman.prompt_builder` names this file) |
| a batch running, its reports, its asks and its watcher | `chief-of-staff:steering` | While it runs (64,781): its status, reports, asks, watcher, cost and compaction items; Offering options and Refusals to say before they are met; with `foreman.md#A Driver's refused force push`'s new place, read today by `chief-of-staff` |
| a CR ready to merge, a merge to record, a stack, a hold or an insert | `chief-of-staff:merge` | from While it runs: the words to the user about a PR, `ready-to-merge`, the series and stack items, dropping, holding and inserting a CR |
| a batch's last CR ends, the pause, the retro, a recovery | `chief-of-staff:batch-end` | from While it runs: the pause, Closing, Recovery, Putting back |
| steering a batch yourself (direct mode) | `chief-of-staff:direct` | Steering a batch yourself (19,357), read with the Foreman's actions it names |
| a release | `chief-of-staff:release` | Releases (11,807) |

`writer` lists the piece that holds the surface writer's text instead of `chief-of-staff.md`
whole. The moments come from the card's own text; where one rule is needed at two moments, both
actions list it.

### 2. The Foreman (`foreman.md`)

Today read whole by `batch` (with `concepts.md` and both host cards). `foreman.md` keeps its
opening, Your goal (5,268), The user's boundaries (13,570) and, of Your means (52,351), what a
batch's start and every heartbeat need (the CLI's limits, orders, starting a Driver, the
heartbeat). Target cut of the rest of Your means, by its bold items:

| Moment | New action | Moves there |
|---|---|---|
| a CR handed back ready, an `order merged`, the main checkout after a merge, a merge on GitHub under the grant | `foreman:merge` | The main checkout after a merge; Merging on GitHub; the hand-back and merge items |
| a held CR, a parked CR, a mode switch | `foreman:hold` | A held CR; Parking a CR on an outside wait; A mode switch |
| a Driver lost or silent | `foreman:lost-driver` | A lost Driver |
| an early conflict check (parallel batch) | `foreman:conflict` | An early conflict check |
| a Driver's refused force push | `foreman:force-push` | A Driver's refused force push (9,085), also listed by `chief-of-staff:steering` and by the Driver's force-push action |
| the pause and its retro | `foreman:pause` | The retro critic and the pause items |

`batch` lists `foreman.md`'s remaining text instead of the whole of today's card; `batch:stack`
is unchanged.

### 3. The Driver (`driver.md`)

Already read by sections. Two changes:

- **Every section is reached by an action.** Today twenty sections are read only through a link.
  Each gets an action naming its moment (target grouping; the Fable advisor may regroup):
  `driver:restart` (a Driver started again), `driver:trouble` (a worker that fails, escalation, a
  remote command fails, a git command in the wrong place, stopping a long gate, when CI lists no
  check, CI beside the long gate), `driver:force-push` (a force push the host refuses, with
  `foreman.md`'s section's new place), `driver:conflicts` (carries, conflicts and the early push;
  CR driver: moves and conflicts), `driver:handback-other` (hand-backs out of the ordinary),
  `driver:pr-extras` (the archive in the PR, images and the look, GitLab forms), `driver:session`
  (the steering session's messages, the lease, checkpoint commits), `cr-driver:retake` (CR
  driver: re-takes), `cr-driver:matrix` (matrix probe, the board's write paths). These sections
  may move to `driver-<moment>.md` pieces or stay in `driver.md` read by section, whichever keeps
  the manifest smaller: the reading is by section in both cases.
- **The first reading shrinks.** Of the `cr-driver` action (Means: the record and the workers,
  Means: context and your folder, Means: the worktree, CR driver) and the opening, what is needed
  only at a later step moves to that step's action (`cr-driver:ship`, `cr-driver:closing`,
  `cr-driver:retake`, or a `driver:*` action). The opening's "Deferred:" list names every Driver
  action with its moment. `stack-driver`, `qa-driver` and `release-driver` keep the same shape
  (their Means sections, then their role's section last), so `_check_actions`'s assertions hold.

### 4. The tests (`skills/chantier/scripts/cli/tests/`)

- `test_startup_manifest.py`:
  - **Every rule is reached** (new test): for each of the three roles' cards (the entry cards and
    every new piece), every level-2 section is listed by at least one action or startup section,
    as `file#heading` or as the whole file; a card's opening counts as read with its entry card.
    It reads the cards and the manifest from the repository as they ship.
  - **The moved-rule table** (new data, `MOVED_RULES`, one row per row of the PR's tables): the
    rule's first words, its old place, its new `file#heading`, its action. A parametrized test
    asserts the words are in the new section (`_text`), gone from the old place, and the new
    section is listed by that action. It sits beside `MOVED_IN` and `MOVED_OUT`, which are
    updated for each phrase that moves (`ABOUT_FOREMAN` now lives in the batch-start piece).
  - **Start reading figures** (new test): it prints, per role and host,
    `start-reading role=<role> host=<host> bytes=<n>` for the three start readings defined above,
    and asserts each at or below the figure the PR reports, so a later edit cannot grow it back
    unnoticed. `CR_DRIVER_LIMITS` and `CR_DRIVER_OPENING_LIMIT` are lowered to the new figures.
  - `_wrapper_path`'s and `test_startup_manifest_measures_every_real_role_and_host`'s assertion
    on `entries.foreman` (`"prompt_builder": "chief-of-staff.md"`) names the piece that now
    holds the Foreman's prompt.
- The tests that read a card's text by its name (`test_came_back.py`, `test_event_audience.py`,
  `test_launch_modes.py`, `test_release_tag.py`, `test_stack_chain_cards.py`,
  `test_board_running_lane.py`, `test_driver_prompt.py`) keep every assertion; each one that reads
  a moved phrase reads the file where it now lives. None is dropped or loosened.

### 5. The Fable advisor

For each role, once its cut is written, an advisor on Fable (`claude-fable-5-2`) reads the old
card (at the base) against the new pieces, the manifest's actions and the entry card's list of
moments, read-only, and answers: which rule now arrives too late, too early, by the wrong means
(a link where an action is needed) or not at all, and which cut would be better. Each finding is
fixed or answered in the PR; the advisor's verdict for each role is quoted in the PR's
Deliverables. Who starts it and how its model is set is the open question 3. A Fable model not
available exactly as named is a stop, never a look-alike.

## Decisions carried

- slim-cards-Q1 (A): each big card cut by moment of need, each piece an action of
  `startup-manifest.json` read when its situation arrives (sections 1 to 3).
- slim-cards-Q2 (A): the three roles in this one CR, in the order Chief of Staff, Foreman,
  Driver, each with its own table; after `slim-session-start` (waits for its merge; rebases onto
  it).
- slim-cards-Q3 (A): each role's start reading measured before and after, aiming at about half,
  the figures in the PR.
- slim-cards-Q4 (A): a table of every moved rule with its action, a test that each rule is
  reached by at least one action, a Fable advisor reading each role's split.
- slim-cards-Q5 (A): specified for the running batch batch-31.

## Out of scope

- `session-start.md` and its split: the base CR's.
- The forge wording of the cards (`gh`, `glab` beyond the startup cards): a separate CR, per
  slim-session-start-Q3.
- Cutting `concepts.md`, the host cards, `foreman-stack.md`, `pr-template.md` or the workers'
  cards; changing what the CLI prints (`take`, `handoff`, the Driver's prompt): that is
  `driver-context-second-cut`'s.
- Any rule's meaning: no rule is changed, added or dropped.
- The version: no hand edit.

## Evidence

- **The tables**, in `pr-body.md`'s Deliverables, one per role (Chief of Staff, Foreman,
  Driver): each moved rule (its old `card#section` or bold item), its new `file#section`, its
  action, its moment. The same rows are `MOVED_RULES` in the test.
- **The figures**, in the PR: each role's start reading today (above), at the base and after, in
  bytes, with the ratio; where about half is not reached, the reason, read from the figures.
  The boot and reload bytes per role (`startup-bytes` lines) before and after, with the manifest's
  size.
- **The checks**: `just check` (the new and updated tests above) in the worktree at the rebased
  head, on Windows; CI's `just check` on Linux, macOS and Windows. The tests read the shipped
  cards and the shipped `startup-manifest.json` from the repository at the head under test; the
  only prepared texts are those already in `test_reading_union_counts_lf_bytes_and_nested_sections_once`
  and `test_reload_budget_includes_additional_whole_file_readings` (a broken input), each paired
  with the check on the shipped files.
- **The long gate**: a change to the cards passes the pipeline's `just scenario (ubuntu-latest)`
  job, green at the PR's head, before the PR is ready; when this CR is on top of batch-31's stack,
  `chantier gate <cr> scenario` locally at its head (Windows coverage). No `just eval-dry-run` is
  owed (nothing under `src/` or `evals/kit/` changes); `just mod` is not owed (no `hooks/` or
  `types/` change).
- **The Fable advisor's verdicts**, one per role, quoted in the Deliverables, with each finding's
  fix or answer.
- **Host matrix** (what each role reads depends on the host through the host cards and
  wrappers):
  - Claude Code: the start reading measured by the new test (`host=claude`); the cards exercised
    by `just scenario`; no real session run of the new cards (evidence limit: not tested in a
    real batch).
  - Copilot: the start reading measured by the new test (`host=copilot`); not exercised (untested
    in a real session).

## Open questions

1. **The manifest's growth at boot.** Every role reads `startup-manifest.json` (4,587 bytes)
   whole at boot, within the 12,544-byte startup limit; the Chief of Staff's reload is at 12,515
   today, 29 bytes under. The new actions add an estimated 2 to 3 KB. Which way: (A) raise the
   limit by the measured growth; (B) let an action name another action's readings by reference
   (one line in `role-core.md`; the four Driver actions' shared Means lines written once), with the
   limit kept, and (A) for what remains; (C) the actions move out of the boot reading (one
   actions file per role, read at its first action), the manifest's format changing (version 3).
2. **The Foreman's half.** Cutting `foreman.md` alone takes the Foreman's start reading from
   275 KB to about 215 KB (about 78 %): the rest is `concepts.md` (72 KB) and the two host cards
   (116 KB), read whole by `batch`. May the Foreman's actions read the host card of its own host
   only (the `{"claude": …, "copilot": …}` form the startup sections already use) and
   `concepts.md` and the host card by section, with no text moved in those files? Without it,
   the PR reports about 78 % for the Foreman, not half.
3. **Who runs the Fable advisor.** A Driver passes only the models the CLI prints in its `team:`
   lines, and the playbook names no advisor role. Which way: (A) the Driver runs it as an
   Inspector review step, with the user setting the Inspector's model to `claude-fable-5-2` in the
   project's `chantier.yaml` for this batch; (B) the Chief of Staff runs it, like the spec critic,
   on the PR's head, before the user's merge; (C) another way the user names.
