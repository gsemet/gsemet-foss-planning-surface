# Slim the startup cards of the Chief of Staff, Foreman and Driver

Short name: `slim-cards`. Base: `slim-session-start` (`slim-session-start-md-split-by-role-forg`),
which this CR waits for and rebases onto (slim-cards-Q2). It closes the P1 item
`role-cards-still-too-big-for-a-driver-s-` (slim-cards-Q12).

## Goal

In the owner's words (2026-11-23): the Chief of Staff, the Foreman and the Driver still read
very large cards; slim them without breaking anything: the right instruction must arrive at the
right moment, by the right means. Each big card is cut by moment of need, and each piece is an
action of `startup-manifest.json`, read when its situation arrives (slim-cards-Q1). The goal is
about half of each role's start reading, measured before and after (slim-cards-Q3). The proof
is a table of every moved rule with its action, a test that every rule is reached by an action,
and a Fable reading of each role's split (slim-cards-Q4, run as slim-cards-Q9 says).

## Where it stands (measured on `main` at f4c1bccd, 2026-11-23)

A role's **start reading** is what it reads before its first act of work, as the manifest
defines it, in LF bytes, each byte counted once (the union rule of `test_startup_manifest.py`'s
`_unique_startup_bytes`):

| Role | Start reading | Bytes (Claude host) |
|---|---|---|
| Chief of Staff | boot (`startup-core.md`, `host-core-*.md`, `role-core.md`, `startup-manifest.json`, `skills/chief-of-staff/SKILL.md` with its `Startup core`) + action `session-start` + action `chief-of-staff` | 363,700 |
| Foreman | boot (the cores, the manifest, `startup_sections.foreman`) + action `batch` | 275,457 |
| CR Driver | boot (the cores, the manifest, its wrapper, `driver.md#Startup core`) + action `cr-driver` | 22,604 |
| Stack Driver | the same + action `stack-driver` | 63,522 |
| QA Driver | the same + action `qa-driver` | 33,664 |
| Release Driver | the same + action `release-driver` | 44,953 |

The four Drivers also read `driver.md`'s opening (2,475 bytes), not counted above. The heavy
parts: `chief-of-staff.md` is 200,336 bytes, read whole by `chief-of-staff` (and by `writer`);
`foreman.md` 82,872 and `concepts.md` 71,611, both read whole by `batch`; `chief-of-staff` and
`batch` list `hosts/claude-code.md` (97,766) and `hosts/copilot.md` (18,746) whole, both hosts'
cards for every host. `driver.md` (133,540) is read by sections, but 21 of its sections are
listed by no action (reached only by a link): the 17 "Means:" sections from "a Driver started
again" to "the lease" that no action names, and "CR driver: re-takes", "matrix probe", "the
board's write paths", "moves and conflicts". The manifest is 4,537 bytes; the Chief of Staff's
boot reload is 12,515 of the 12,544-byte limit.

These are today's figures. The CR's **before** figures and its cut are taken at the rebased base
(below), with the same measure; the PR states today's, the base's and the after figures.

## The base the cut is taken on

The Driver cuts the cards as they stand once `slim-session-start` is merged and every other CR of
batch-31 that edits these cards is merged or dropped, rebased onto that head: CR-465 (`driver.md`),
CR-466 (`driver.md` "Means: a rebase the host refuses", `foreman.md` "A Driver's refused rebase",
`chief-of-staff.md` "A refused rebase"), CR-467 (`chief-of-staff.md`, "Backlog and grill"), CR-468
(`chief-of-staff.md`). Every section or bold item these CRs add gets an action like the rest
(section 3's tables name where CR-466's three go); one that lands after this CR's tables were
written is added to them before the push. The tables and `MOVED_RULES` are written from that head,
never from today's `main`.

## What changes

The order of work is the user's: the Chief of Staff, then the Foreman, then the four Drivers
(slim-cards-Q2, Q12), one commit per role at least, each with its own table.

### 1. Rules common to the cuts

- **The entry cards keep their names.** `chief-of-staff.md`, `foreman.md` and `driver.md` stay,
  each keeping its opening, its `Startup core` when it has one, and what its role needs at every
  moment. The CLI's prompts (`driver_prompt.py`'s `Card:` line naming `driver.md`), the eval kit
  (`evals/kit/audit.py`, `evals/kit/dry_run.py`), the wrappers in `agents/` and
  `com.github.copilot/agents/` and the manifest's `roles` map stay valid with no change. No file
  under `skills/chantier/scripts/cli/src/` or `evals/kit/` changes.
- **Each moved piece is a new card** in `skills/chantier/references/`, named `<role>-<moment>.md`
  as `foreman-stack.md` is (for instance `chief-of-staff-grill.md`, `foreman-merge.md`,
  `driver-trouble.md`), with a `#` title and level-2 sections.
- **Each piece is an action** named `<role>:<moment>` (as `cr-driver:ship`), in
  `startup-manifest.json`'s `actions`.
- **The manifest stays small; the moments live in the entry cards** (slim-cards-Q10). Each new
  action is one short line, preferably one whole piece file (`"foreman:merge":
  ["foreman-merge.md"]`), so the manifest grows by a few bytes per action. Each entry card holds
  its role's list of moments: one line per action, the moment, then the action's name, and the
  readings it adds beyond its piece when there are some (a `concepts.md` or host section). The
  manifest's line and the card's line agree; a test holds them together (section 4). Q6's
  reference form (`@<action>`) is not used unless it saves bytes, measured; then the PR shows the
  saving. The 12,544-byte limit stays and is not raised: a cut that would pass it is redone with
  fewer, shorter action lines; if it still cannot fit, the Driver hands back blocked with the
  figures.
- **The one-host reading form.** A reading may be `{"claude": "<reading>", "copilot":
  "<reading>"}`: each host reads only its own value (the form `startup_sections.foreman` already
  uses, now allowed in `actions` too). The manifest's `paths` text says so, in one clause: "a
  reading is a file, a file#heading (a level-2 section), or {host: reading}, read by that host
  only". The tests' `_resolve` already accepts it; they check both keys are present.
- **After a compaction** (slim-cards-Q11): a role re-reads its entry action, then the action of
  the moment it is in. One sentence says it in `session-start.md`, "5. Reload" (the section the
  base keeps), and the same sentence ends each entry card's list of moments.
- **Text moves, it is not rewritten.** A moved rule keeps its words; only its links change. Every
  inbound link is updated: the cards (`chief-of-staff.md#steering-a-batch-yourself`,
  `foreman.md#a-drivers-refused-force-push` and the like), `hosts/copilot.md`, `routing.md`,
  `skills/chief-of-staff/SKILL.md`'s `Startup core` ("`chief-of-staff.md`, Starting a batch"),
  `CONTRIBUTING.md` (the references list near line 64, which names each new piece, and the link
  near line 172), `evals/README.md` (lines 157, 171 and 278 cite `chief-of-staff.md`'s rules:
  they name the piece that now holds them), `evals/real-direct/RUNBOOK.md` and `docs/`. No rule is
  added, none dropped; a duplicate found is said in the PR, not merged away.
- **No text moves in `concepts.md` or the host cards**; only how the actions read them changes
  (sections 2 and 3).

### 2. The Chief of Staff (`chief-of-staff.md`)

The `chief-of-staff` action reads only its own host's card, whole (slim-cards-Q13, in the
one-host form), instead of both. Target cut, by the card's sections:

| Moment | Action | Moves there from `chief-of-staff.md` |
|---|---|---|
| any moment of the session (stays) | `chief-of-staff` | opening, Entry points, Hard rules, The project, Handing the seat over, Subagents and the demo, Never; the list of moments |
| filing, moving or grilling a CR, starting the Spec-writer and the spec critic | `chief-of-staff:grill` | Backlog and grill (38,762, with CR-467's change); finer pieces by its bold items where one moment needs only part |
| the user's "run them" up to the Foreman's start or `open --direct` | `chief-of-staff:batch-start` | Forge permissions (P9), The trials before the go, Starting a batch with The floor (holds the Foreman's prompt: `entries.foreman.prompt_builder` names this file) |
| a batch running: status, reports, asks, the watcher | `chief-of-staff:steering` | While it runs (its status, report, ask, watcher, cost and compaction items), Offering options, Refusals to say before they are met; "A refused force push" and CR-466's "A refused rebase"; with `foreman.md`'s "A Driver's refused force push" and "A Driver's refused rebase" in their new place |
| a CR ready to merge, a merge to record, a stack, a hold, an insert | `chief-of-staff:merge` | from While it runs: the words about a PR, `ready-to-merge`, the series and stack items, dropping, holding, inserting a CR |
| a batch's last CR ends: the pause, the retro, a recovery | `chief-of-staff:batch-end` | from While it runs: the pause, Closing, Recovery, Putting back |
| steering a batch yourself (direct mode) | `chief-of-staff:direct` | Steering a batch yourself, with the Foreman's actions it names |
| a release | `chief-of-staff:release` | Releases |

`writer` names the piece that holds the surface writer's text instead of `chief-of-staff.md`
whole. CR-468's additions go with the moment their text serves. Where one rule is needed at two
moments, both actions list it.

### 3. The Foreman and the Drivers

**The Foreman** (`foreman.md`). It keeps its opening, Your goal, The user's boundaries and, of
Your means, what a batch's start and every heartbeat need (the CLI's limits, orders, starting a
Driver, the heartbeat) and the list of moments. The rest of Your means, by its bold items:

| Moment | Action | Moves there |
|---|---|---|
| a CR handed back ready, an `order merged`, the main checkout after a merge, a merge on GitHub under the grant | `foreman:merge` | The main checkout after a merge; Merging on GitHub; the hand-back and merge items |
| a held CR, a parked CR, a mode switch | `foreman:hold` | A held CR; Parking a CR on an outside wait; A mode switch |
| a Driver lost or silent | `foreman:lost-driver` | A lost Driver |
| an early conflict check (parallel batch) | `foreman:conflict` | An early conflict check |
| a Driver's refused force push or refused rebase | `foreman:refused` | A Driver's refused force push; CR-466's A Driver's refused rebase (also read by `chief-of-staff:steering` and `driver:refused`) |
| the pause and its retro | `foreman:pause` | The retro critic and the pause items |

The Foreman's actions read only its own host's card, and `concepts.md` and that host card by
section, with no text moved (slim-cards-Q7): `batch` lists `foreman.md`'s remaining text and the
sections a batch's start needs (in the one-host form for the host card); each `foreman:*` action
or its line in the list of moments names the sections its moment needs (for instance
`concepts.md#Escalation` where a trigger arises). Every section of `concepts.md` and of the host
card that `batch` reads whole at the base stays listed by at least one Foreman action, for that
host. `batch:stack` is unchanged. The Chief of Staff's actions naming `concepts.md` (`board`,
`writer`) are unchanged.

**The four Drivers** (`driver.md`; slim-cards-Q12). The cut covers the CR, stack, QA and release
Drivers; each one's first reading is measured and cut by step.

- **Every section is reached by an action.** The 21 sections no action lists today, and CR-466's
  "Means: a rebase the host refuses", each get one, moving to `driver-<moment>.md` pieces so each
  action stays one short line (target grouping; the Fable reading may regroup):
  `driver:restart` (a Driver started again), `driver:trouble` (a worker that fails, escalation, a
  remote command fails, a git command in the wrong place, stopping a long gate, when CI lists no
  check, CI beside the long gate), `driver:refused` (a force push the host refuses, a rebase the
  host refuses, with `foreman:refused`'s piece), `driver:conflicts` (carries, conflicts and the
  early push; CR driver: moves and conflicts), `driver:handback-other` (hand-backs out of the
  ordinary), `driver:pr-extras` (the archive in the PR, images and the look, GitLab forms),
  `driver:session` (the steering session's messages, the lease, checkpoint commits),
  `cr-driver:retake` (CR driver: re-takes), `cr-driver:matrix` (matrix probe, the board's write
  paths).
- **Each Driver's first reading shrinks, by step.** Of each Driver's first action (`cr-driver`,
  `stack-driver`, `qa-driver`, `release-driver`), what is needed only at a later step moves to that
  step's action: for the CR Driver `cr-driver:ship`, `cr-driver:closing` or a `driver:*` action;
  for the stack Driver, its 31,211-byte section cut by step into `stack-driver:<step>` actions
  (for instance the chain's build, the ship, the merges and drops); for the release Driver, its
  section cut likewise into `release-driver:<step>` (its "Release driver: the end" one of them);
  the QA Driver's shared Means lines move to their step like the others'. `_check_actions`'s rule
  (role section last in the first action, the rest "Means:" sections) and `_check_driver_steps`'s
  disjointness are kept, extended to the new step lines.
- **What leaves the Driver opening.** `driver.md`'s opening (before its first `##`, read by all
  four Drivers) keeps its first paragraph, the "Rules" and "A card" bullets, "Another Driver's
  section ... are not opening reads", "A rule you did not read still binds you", and the list of
  moments. The "Deferred:", "Concepts:" and "A Driver started again" bullets become lines of that
  list (no word of their rule lost: each line names the same moment and section). The
  "Specification" bullet moves to the first-step piece of each Driver that briefs workers (the CR,
  stack and QA Drivers' first actions list it). The opening stays at or under
  `CR_DRIVER_OPENING_LIMIT`, lowered to its new size.

### 4. The tests (`skills/chantier/scripts/cli/tests/`)

`test_startup_manifest.py` has 391 lines and `test_plugin_files.py` 400, the most a file may hold
(`CONTRIBUTING.md`, "File: at most 400 lines"): nothing is added to `test_plugin_files.py`, and
`test_startup_manifest.py` only changes what must (`MANIFEST_VERSION` if Q6's form is used, the
`entries.foreman` assertion's `prompt_builder` file, `MOVED_IN` and `MOVED_OUT` rows whose phrase
moves, `CR_DRIVER_LIMITS` and `CR_DRIVER_OPENING_LIMIT` lowered to the new figures), staying under
400 lines. The new checks go in two new files, each importing `_manifest`, `_resolve`, `_sections`,
`_section_span`, `_text`, `_lf_bytes` and `_unique_startup_bytes` from `test_startup_manifest.py`
(imported, not copied), each under 400 lines, reading the shipped cards and manifest from the
repository at the head under test:

- **`test_role_cards_split.py`:**
  - Every rule is reached: for each card of the three roles (the entry cards and every piece),
    every level-2 section is listed by at least one action or startup section, for each host, as
    `file#heading` or the whole file; an entry card's opening counts as read with it. For the
    Foreman, every section of `concepts.md` and of its host card that `batch` read whole at the
    base is listed by a Foreman action.
  - Entry card and manifest agree: every `<role>:<moment>` action of the manifest (`chief-of-staff:`,
    `foreman:`, `cr-driver:`, `stack-driver:`, `qa-driver:`, `release-driver:`, `driver:`) is named,
    in backticks, in its entry card's list of moments, and every action that list names exists in
    the manifest.
  - `MOVED_RULES`, one row per row of the PR's tables: the rule's first words, its old place, its
    new `file#heading`, its action. Parametrized: the words are in the new section, gone from the
    old place, and the new section is read by that action.
  - The compaction sentence (slim-cards-Q11) is in `session-start.md`'s "5. Reload" and in each
    entry card's list of moments.
  - The one-host form: every dict reading in `actions` has exactly the keys `claude` and
    `copilot`, and the manifest's `paths` text names the form.
  - The links: no card, `CONTRIBUTING.md`, `evals/README.md` or `docs/` file links an anchor of
    `chief-of-staff.md`, `foreman.md` or `driver.md` that no longer exists there.
- **`test_start_reading.py`:**
  - Prints `start-reading role=<role> host=<host> bytes=<n>` for the six start readings of the
    table above (each Driver's opening counted), and asserts each at or below the after figure the
    PR reports, so a later edit cannot grow it back unnoticed.
  - The two `STARTUP_LIMIT` constants (`test_startup_manifest.py` line 10 and
    `test_plugin_files.py` line 65) both equal the manifest's `limit`, 12,544.
- The tests that read a moved phrase in a card by its name (`test_came_back.py`,
  `test_event_audience.py`, `test_launch_modes.py`, `test_release_tag.py`,
  `test_stack_chain_cards.py`, `test_board_running_lane.py`, `test_driver_prompt.py`, and the
  checks CR-466 adds on `foreman.md`'s two refused sections) keep every assertion and read the
  file where the phrase now lives; none is dropped or loosened.

### 5. The Fable reading (slim-cards-Q9)

The Chief of Staff runs it, not the Driver: once the PR is ready, before the merge, it starts one
read-only reading per role (Chief of Staff, Foreman, Drivers) on Fable through the host's model
parameter, as it starts the spec critic. Each reading compares the old card (at the base) with the
pieces, the actions and the entry card's list of moments, and answers which rule now arrives too
late, too early, by the wrong means (a link where an action is needed) or not at all, and which
cut would be better. Its findings go back to the Driver as a round; the Driver fixes each or
answers it in the PR, and quotes each role's verdict in the Deliverables. The Driver neither
starts it nor edits `chantier.yaml` for it. Fable not available exactly as named is a stop,
never a look-alike.

## Decisions carried

- Q1 (A): each big card cut by moment of need, each piece an action read when its situation
  arrives (sections 2, 3).
- Q2 (A): the three roles in one CR, in the order Chief of Staff, Foreman, Driver, each with its
  table; after `slim-session-start`.
- Q3 (A): start reading measured before and after, aiming at about half, figures in the PR.
- Q4 (A): the moved-rule table, the reach test, a Fable reading of each role's split.
- Q5 (A): specified for batch-31.
- Q6 (B), as narrowed by Q10: the reference form only where it saves bytes; the limit stays.
- Q7 (A): the Foreman reads its own host's card, `concepts.md` and that card by section, no text
  moved (section 3).
- Q8 (A): superseded by Q9.
- Q9 (A): the Chief of Staff runs the Fable reading on the ready PR, before the merge, once per
  role; findings go back as a round (section 5).
- Q10 (A): the manifest stays small, the moments in each entry card, the limit stays (section 1).
- Q11 (A): after a compaction, the entry action then the current moment's action; one sentence in
  "5. Reload" and in each entry card (section 1).
- Q12 (A): the CR, stack, QA and release Drivers, each first reading cut by step; the P1 item
  `role-cards-still-too-big-for-a-driver-s-` closed by this CR (section 3).
- Q13 (A): the Chief of Staff reads its own host's card only, whole (section 2).

## Out of scope

- `session-start.md`'s split: the base CR's (this CR adds only the Q11 sentence to "5. Reload").
- The forge wording of the cards beyond the startup cards: a separate CR.
- Moving text in `concepts.md`, the host cards, `foreman-stack.md`, `pr-template.md` or the
  workers' cards; changing what the CLI prints: `driver-context-second-cut`'s.
- Any rule's meaning: no rule is changed, added or dropped.
- The version: no hand edit.

## Evidence

- **The tables**, in `pr-body.md`'s Deliverables, one per role (Chief of Staff, Foreman, the
  Drivers): each moved rule (its old `card#section` or bold item), its new `file#section`, its
  action, its moment; the same rows as `MOVED_RULES`.
- **The figures**, in the PR: the six start readings today, at the base and after, in bytes, with
  the ratio, and where about half is not reached the reason read from the figures; the boot and
  reload bytes per role (`startup-bytes` lines) and the manifest's size before and after.
- **The checks**: `just check` in the worktree at the rebased head, on Windows; CI's `just check`
  on Linux, macOS and Windows. The tests read the shipped cards and manifest at the head under
  test; the only prepared texts are those already in
  `test_reading_union_counts_lf_bytes_and_nested_sections_once` and
  `test_reload_budget_includes_additional_whole_file_readings`, each paired with the check on the
  shipped files.
- **The long gate**: the pipeline's `just scenario (ubuntu-latest)` green at the PR's head before
  the PR is ready; when this CR is on top of batch-31, `chantier gate <cr> scenario` locally at its
  head. No `just eval-dry-run` (nothing under `src/` or `evals/kit/` changes); no `just mod`.
- **The Fable verdicts**, one per role, quoted in the Deliverables after the Chief of Staff's
  round, with each finding's fix or answer.
- **The P1 item**: the PR names `role-cards-still-too-big-for-a-driver-s-` as closed by it, with
  the four Drivers' figures; the Chief of Staff closes the item at the merge.
- **Host matrix** (each host reads only its own host card's readings):
  - Claude Code: measured by the new tests (`host=claude`); exercised by `just scenario`; not
    tested in a real batch.
  - Copilot: measured by the new tests (`host=copilot`); untested in a real session.

## Open questions

None: slim-cards-Q6 to Q13 answered those this specification raised.
