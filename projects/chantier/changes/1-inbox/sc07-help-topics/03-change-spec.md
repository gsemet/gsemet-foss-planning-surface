# SC07: `chantier help <topic>` carries the rare cases

Child 7 of 28 of the program CR `simplify-cards-and-prompts` (its `03-change-spec.md`, "Child 7",
and its `02-answers.md` answers 10, 13, 17 to 22 rank above this file). One Driver, one PR, in the
running stack batch (batch-31). Code read: `origin/main` at `8a960d34`, plus the specifications of
children 1 and 3 (`4-batch/1-pending/487-sc01-push-own-cr-branch`,
`489-sc03-refusals-name-next-step`), which sit below this child in the stack. Short forms:

- `src/` is `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` is `skills/chantier/scripts/cli/tests/`;
- `references/` is `skills/chantier/references/`.

## Goal

The owner's words (answers 1, 17, 18): progressive disclosure as far as it goes; a model that
stumbles runs `--help` or `help <topic>`, and what a role needs at a rare moment comes from a help
topic that a refusal, a `next:` line or a state line names. Today the 33 pieces of `references/`
exist as files, each reached only through a manifest action the role must remember
(study-fable-v2, section 4.3: "no `help` command, no refusal or state line that names a piece").
This child builds the carrier: a topic index, a `help` command that prints a topic whole, and
`help <topic>` named in the CLI lines where a rare case starts. It only adds: no card text
changes, the manifest and every piece stay, and every role keeps working on the old cards.

## Place in the chain

- **Base:** child 6's branch (`situation-quiz`), the previous CR of the stack. Children 1 to 6
  are below it: child 1's `chantier push` and its refusals (`src/commands/push.py`) and child 3's
  completed refusal tails in `src/core/leases.py` are in the base and are edited on top here.
- **It relies on:** child 1 (the push refusals it names a topic in); child 3 (its M9 gate reads the
  command names from the parser, so a `` `help lease` `` span counts as a command once `help` is
  registered, with no edit to that gate).
- **What depends on it:**
  - child 8 (`host-rows-and-proofs`) builds on this branch;
  - child 5's measure counts `help <topic>` reads by topic (it reads transcripts; no code link);
  - child 9 rewrites the AGENTS.md role sentences and names `help --for` as a reader of role data;
  - child 10's brief ends with the line "`$CHANTIER help <topic>` when a line names one";
  - child 18 switches `help --for`'s role list to `skills/chantier/roles.yaml`, with the same
    output;
  - children 19 to 23 write the new topics in `skills/chantier/cards-next/topics/` and the final
    `cards-next/topics.json` (child 23), in the format this child sets; child 24 swaps it in place
    of this child's `references/topics.json` and repoints its readings;
  - child 25 homes inventory rows in topics and sets `review_by` on answer 10's rare ones.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Answer 18 (simplify-cards-Q18) | `help <topic>` is one of the tools that land first, before any card is rewritten | the whole CR |
| Answer 17 | A removed rule must be easy to find again: a topic, a refusal or a `next:` line | the topics index, the named lines |
| Answer 10 (Q10) | A rare incident rule with no CLI trigger is kept as a topic for one release, its reads measured | `review_by` in the format (section 1); no topic of this child carries it (section 1, "review_by") |
| Answer 13 (Q15) | In direct mode the Chief of Staff gets the Foreman's card and tools | the Foreman's topics also serve `chief-of-staff` (section 1) |
| Answer 8 (Q5b), answer 22 F3 | The refused-push route stays for good | the `refused-push` topic, named by `chantier push`'s git refusal |
| Answer 22, F20 | The PR states the seconds its tests add to `just test`, measured before and after on the same machine | Evidence |
| Answer 22, F17 | A claim this program has not proved is marked unproved | Risk |
| Program child 7, Scope | `references/topics.json` (readings, roles, trigger, `review_by`); every manifest action that is a piece or a rare-case section becomes a topic pointing at today's file; `chantier help [<topic>] [--for <role>]` in a new `src/declare/help.py`; topics named in the lease refusals, the push refusals, `restack owed:`, `handed back:` and the watcher's end lines | sections 1 to 4 |
| Program child 7, Must not | No manifest or piece removed, no card text changed, no network read | Out of scope |
| Program child 7, Risk | Long gate owed; AGENTS.md gains a line for `help` (simplify-cards-Q18) | Gates, section 6 |
| Program rules | A new command adds a scenario step and its coverage bullet; `just check` and `just eval-dry-run` before the first push; no version edited by hand | sections 5, Gates |

## What changes

### 1. The topic index: new `references/topics.json`

One JSON file, read by the CLI and the tests:

```json
{
"version": 1,
"paths": "relative to this folder; a reading: file, file#heading (a level-2 heading of that file), or {\"claude\": ..., \"copilot\": ...} (that host only)",
"topics": {
  "lease": {
    "readings": ["driver-session.md#Means: the lease"],
    "roles": ["cr-driver", "stack-driver", "qa-driver", "release-driver", "foreman", "chief-of-staff"],
    "trigger": "a `--lease` refusal, `claim lost`, a lease `not confirmed`, a wait over 3 minutes"
  }
}
}
```

- **Readings** take the manifest's reading forms (`startup-manifest.json`, its `paths` key): a
  file, `file#heading` (the level-2 heading `## <heading>`, its section running to the next
  heading of level 1 or 2), or a `{"claude": …, "copilot": …}` map. The `@action` form is not
  allowed: a topic names its files directly, so it survives the manifest's removal (child 24).
- **Roles** are names from the manifest's `roles` map (today's role list; child 18 moves it to
  `roles.yaml`). The CLI knows them only as this data.
- **Trigger**: one short phrase, the refusal, line or moment that sends a role there. Where a CLI
  line names the topic, the trigger quotes that line's start in backticks.
- **`review_by`** (optional): a version `X.Y.Z`, for answer 10's rare topics. No topic of this
  child carries it: every topic here points at a piece or a section the manifest still loads, not
  at a rare incident rule cut from a card; those come with the rewrite and the review (children 19
  to 25), which set it to the next minor version. The format, the loader and a test accept it now.
- **Which actions become topics.** Each action of `startup-manifest.json` that reads a piece (a
  file `driver-*.md`, `foreman-*.md`, `stack-driver-*.md`, `release-driver-*.md` or
  `chief-of-staff-*.md`, but `chief-of-staff-any.md`, which the Chief of Staff's own start reads)
  or a rare-case section. A topic keeps the action's piece and section readings and drops the
  readings a role already holds at its start or through its own card: the `@driver:*` references
  (a Driver's common means), whole shared cards (`concepts.md`, `foreman.md`, `driver.md`, the host
  cards). Not topics: the role and boot actions (`route`, `reload`, `session-start`, `grill`,
  `status`, the worker card actions, `cr-driver`, `stack-driver`, `qa-driver`, `release-driver`,
  `cr-driver:ship`, `cr-driver:closing`, `driver:brief`, `driver:start`, `driver:ship`,
  `driver:end`, `batch`, `foreman:reference`, `host`, `chief-of-staff`), and the templates
  (`deliver`, `release`), read at a common step.
- **The topics**, in this order (the file's order is the listing's order). `D` stands for the four
  Driver roles `cr-driver`, `stack-driver`, `qa-driver`, `release-driver`; `F` for `foreman` and
  `chief-of-staff` (answer 13: direct mode). The Driver words each trigger from the file's title and
  first lines, at most about 100 characters; the table gives its substance.

| Topic | Readings | Roles | Trigger (substance) | From action |
| --- | --- | --- | --- | --- |
| `lease` | `driver-session.md#Means: the lease` | D, F | a `--lease` refusal, `claim lost`, a lease `not confirmed`, a wait over 3 minutes | `driver:session` |
| `checkpoints` | `driver-session.md#Means: checkpoint commits` | D | a checkpoint commit | `driver:session` |
| `steering-messages` | `driver-session.md#Means: the steering session's messages` | D | a message from or to the steering session | `driver:session` |
| `restart` | `driver.md#Means: a Driver started again` | D | a `take` note `resume:`, `rebase:` or `context:` | `driver:restart` |
| `trouble` | `driver-trouble.md` | D | a worker fails, an escalation, a remote command fails, CI beside the long gate, a gate to stop | `driver:trouble` |
| `conflicts` | `driver-conflicts.md` | D | a `ship` refused `holds a merge commit`, a carry, a conflict, the early push | `driver:conflicts` |
| `handback-other` | `driver-handback-other.md` | D | a hand-back out of the ordinary | `driver:handback-other` |
| `pr-extras` | `driver-pr-extras.md` | D | `archive: in the PR at <path>`, images, GitLab forms | `driver:pr-extras` |
| `refused-push` | `driver-refused.md`, `foreman-refused.md` | D, F | a force push or rebase the host refuses; `` `push <cr>: git refused the push` `` | `driver:refused` |
| `retake` | `driver-retake.md` | `cr-driver` | a first `take` that shows a `PR:` link | `cr-driver:retake` |
| `matrix` | `driver-matrix.md` | `cr-driver` | a matrix probe; the board's write paths | `cr-driver:matrix` |
| `stack-restack` | `stack-driver-restack.md` | `stack-driver` | the restack pass after a merge | `stack-driver:restack` |
| `stack-make` | `stack-driver-make.md` | `stack-driver` | making the stack, the five checks | `stack-driver:make` |
| `stack-joins` | `stack-driver-joins.md` | `stack-driver` | a join, a draft turning ready, a merge, a deadline | `stack-driver:joins` |
| `stack-changes` | `stack-driver-changes.md` | `stack-driver` | an insertion, a drop, a hold, a park, a conflict, heavy CI | `stack-driver:changes` |
| `release-notes` | `release-driver-notes.md` | `release-driver` | the notes, the drafts, the PR body | `release-driver:notes` |
| `release-ship` | `release-driver-ship.md` | `release-driver` | the release PR | `release-driver:ship` |
| `release-merged` | `release-driver-merged.md` | `release-driver` | after the release's merge | `release-driver:merged` |
| `release-end` | `release-driver-end.md` | `release-driver` | the release Driver's end | `release-driver:end` |
| `stack` | `foreman-stack.md` | F | a stack batch | `batch:stack` |
| `stack-merge` | `foreman-stack.md#After a merge` | F | `` `restack owed:` `` | section of `batch:stack` |
| `merge` | `foreman-merge.md` | F | a `` `handed back:` `` line, `order merged`, the main checkout after a merge | `foreman:merge` |
| `hold` | `foreman-hold.md` | F | `order hold`, `order unhold`, a park, a mode switch | `foreman:hold` |
| `lost-driver` | `foreman-lost-driver.md`, `concepts.md#Escalation` | F | a Driver that ended with no hand-back | `foreman:lost-driver` |
| `conflict-check` | `foreman-conflict.md` | F | an early conflict check (parallel batch) | `foreman:conflict` |
| `release` | `foreman-release.md` | F | a release CR in the batch | `foreman:release` |
| `retro` | `foreman-pause.md` | F | the retro critic at a pause | `foreman:pause` |
| `grill` | `chief-of-staff-grill.md`, `chief-of-staff-writer.md` | `chief-of-staff` | the backlog and a grill | `chief-of-staff:grill` |
| `batch-start` | `chief-of-staff-batch-start.md` | `chief-of-staff` | the trials before the go, starting a batch | `chief-of-staff:batch-start` |
| `steering` | `chief-of-staff-steering.md`, `foreman-refused.md` | `chief-of-staff` | a running batch | `chief-of-staff:steering` |
| `ready-to-merge` | `chief-of-staff-merge.md` | `chief-of-staff` | a PR ready to merge, a merge, a stack | `chief-of-staff:merge` |
| `batch-end` | `chief-of-staff-batch-end.md` | `chief-of-staff` | the pause, the end of a batch | `chief-of-staff:batch-end` |
| `direct` | `chief-of-staff-direct.md` | `chief-of-staff` | steering a batch yourself (direct mode) | `chief-of-staff:direct` |
| `release-procedure` | `chief-of-staff-release.md` | `chief-of-staff` | a release to plan, the project's procedure | `chief-of-staff:release` |
| `writer` | `chief-of-staff-writer.md` | `chief-of-staff` | a refused write naming no running writer | `writer` |
| `watcher` | `session-start-chief-of-staff.md#The watcher` | `chief-of-staff` | a watcher's end line (`` `watch: no event` ``, no seat, no key) | section of `board` |
| `board` | `session-start-chief-of-staff.md#The board` | `chief-of-staff` | the board did not start, refused a key or a watcher | section of `board` |
| `sync` | `sync-checkout.md` | `chief-of-staff`, `foreman` | a sync of the main checkout after a merge | `sync` |

The two `session-start-chief-of-staff.md` sections and `stack-merge` are rare-case sections that a
CLI line of section 3 names; they are added so that every named topic exists.

### 2. The command: `chantier help [<topic>] [--for <role>] [--host claude|copilot]`

- **Declared** in a new `src/declare/help.py`: `register(sub)` calls
  `add_command(sub, "help", "chantier.commands.help:show", HELP, NO_BATCH)` (`NO_BATCH` from
  `src/commands/registry.py`), with a positional `topic` (`nargs="?"`), `--for` (`dest="role"`)
  and `--host` (`choices=["claude", "copilot"]`, default: the detected host, as `playbook` does
  with `plugin_files.detect_host`). `HELP`, in substance: "print a help topic whole, the rare case
  a refusal or a line named; with no topic, list them; --for lists one role's; reads only the
  plugin's cards, needs no batch and no project".
- **Wired** in `src/cli.py`: `help` joins the `from chantier.declare import (…)` list and
  `_MODULES`, and `FULL_OUTPUT` (a topic or the list is useless cut at ten lines).
- **Handler** in a new `src/commands/help.py`:
  - `load_topics(path: Path | None = None) -> dict[str, Topic]` reads
    `plugin_files.skill_dir() / "references" / "topics.json"` (a `path` for the tests' prepared
    cases), checks the shape (`version` 1, each topic with a non-empty `readings` list of the three
    forms, a non-empty `roles` list, a non-empty `trigger`, `review_by` absent or `X.Y.Z`) and
    raises `ChantierError(..., EXIT_PRECONDITION)` naming the topic and the problem otherwise.
  - `section(path, heading) -> str`: the LF text from the line `## <heading>` to the next heading
    of level 1 or 2 (the same span as `tests/test_startup_manifest.py`'s `_section_span`); a
    missing heading raises `ChantierError` naming file and heading.
  - `show(args)`:
    - **no topic, no `--for`**: a first line `topics: <n>; help <topic> prints one, help --for
      <role> lists a role's`, then one line per topic in the file's order:
      `<name>: <trigger> (<roles, comma-separated>)`. Exit 0.
    - **`--for <role>`, no topic**: one line per topic whose `roles` holds the role,
      `<name>: <trigger>`. A role in the manifest's `roles` map that no topic serves (a worker):
      one line `no topic for <role>; help lists them all`, exit 0. A role not in that map:
      `ChantierError("no role <role>; roles: <the map's names>", EXIT_USAGE)`.
    - **a topic**: a first line `topic <name>: <trigger> (<roles>)`, then for each reading, in
      order, a line `--- references/<file>[#<heading>] ---` and the reading's text whole (the file,
      or its section; a host map resolved for `--host`). Exit 0.
    - **an unknown topic**: `ChantierError`, exit `EXIT_USAGE` (1), `no topic <name>`, then, when
      `difflib.get_close_matches` finds one or more among the names, `; did you mean help <a>[ or
      help <b>]?`, and `; help lists them all`.
    - **a topic and `--for` together**: `ChantierError("help takes a topic or --for, not both",
      EXIT_USAGE)`.
  - It calls no `Repo.find()`, reads no batch, no planning folder, no git and no network: only
    `references/` (and the manifest's `roles` map for `--for`). It runs from any folder, inside a
    project or not.
- **Never through a profile.** `src/core/remote_wire.py`: `"help"` joins `NEVER_REMOTE`, so
  `clients/remote.py`'s `forward` returns before any profile lookup and the command runs where it
  is typed, on the cards of the plugin the agent itself loaded; `board/cli_run.py`'s `judge`
  then refuses it through `cli.run` (`cli.run: help does not run through the server`) with no
  edit. (Open question 1.)

### 3. The CLI lines that name a topic

The form is always a backticked `` `help <topic>` ``, so the gate of section 4 finds it and child
3's M9 gate reads `help` as a command. Every edit adds text and keeps the existing words and their
order; exit codes and conditions do not move. Before pushing, the Driver greps `tests/` and
`scenario/run_scenario.py` for each changed literal and updates an exact-match check to the new
text, never loosening it.

- **Lease refusals, `src/core/leases.py`** (as child 3 left them): append `` (`help lease`) `` at
  the very end of the message (after child 3's tail and after `_late_ship_tail` when it is added)
  in: `check_free`'s two refusals (held; not confirmed), `require`'s and `claim`'s missing-lease
  refusal, and `lost` (`claim lost: …; stop now: nothing recorded (`help lease`)`). Not in
  `lease_of`'s unknown unit refusals nor the two test-seam refusals (`ttl_seconds`,
  `minute_seconds`): no topic is about them.
- **Push refusals, `src/commands/push.py`** (child 1): append `` (`help lease`) `` to the refusal
  `push needs a held lease; <unit> has none`, and `` (`help refused-push`) `` to the chantier line
  that precedes git's verbatim text, `push <cr>: git refused the push of <branch>; nothing
  recorded`. The lease refusals that `push` raises through `leases.require` and `leases.claim`
  carry `help lease` from the previous bullet. Its other rails (no branch recorded, not a
  `chantier/*` branch, the default branch, worktree missing or dirty, HEAD not on the branch) name
  no topic: no rare-case section covers them.
- **`restack owed:`, `src/commands/orders_merged.py`, `restack_line`**: append
  `` (`help stack-merge`) `` to both forms (with a stack driver recorded; with none). Update
  `tests/test_restack_line.py`'s two expected strings.
- **`handed back:`, `src/status/ready_line.py`, `_line`**: append a last segment
  `` | `help merge` `` after every other segment (after the long gate's segment when there is one).
  `tests/test_ready_line.py` asserts by `startswith` and stays true; add the tail to one case.
- **The watcher's end lines, `src/hub/watch_lines.py`**: insert `` (`help <topic>`) `` immediately
  before the first `: for the Chief of Staff` of each line below, so the command the line ends with
  stays last (the Chief of Staff runs it as printed) and every prefix the tests and the cards
  quote stays true (`no event for <name> in 2 h; ended`, `did not start within 20 s`, `refused the
  key`):
  - `` `help watcher` ``: `NO_KEY`, `NO_SEAT`, `NO_TRANSCRIPT`, `UNREADABLE_SEAT`, `IDLE_END`;
  - `` `help board` ``: `NOT_STARTED`, `BAD_KEY`, `REFUSED`, `NOT_SERVED`.

  Not changed: `EVENTS_END` (`watch: <name> still running: for the Chief of Staff, start again …`):
  it is the common restart, which the Chief of Staff's card names in its Entry points as
  `still running: …`, and any insertion would split that quoted text (open question 2);
  `SEAT_LINE`, `STREAM_TOLD` (no end, or nothing to do); the Foreman's lines (`FOREMAN_*`): the
  Foreman's watcher is a bullet of its own card, no section a topic can point at.

### 4. Tests: new `tests/test_help_topics.py`, few and parametrized

Every check below reads the shipped files from the repository at the head under test
(`conftest.SKILL / "references"`, the package's own `src/`), never a copy:

- **Every topic resolves, on both hosts** (parametrized `host` in `claude`, `copilot`): through
  `chantier.commands.help.load_topics()` on the shipped `topics.json`, each reading's file exists
  under `references/`, each `#heading` is a level-2 heading of it with a non-empty section, each
  role is in the manifest's `roles` map, each trigger is non-empty, and `review_by`, when present,
  is `X.Y.Z`.
- **Every piece has a topic**: every file of `references/` matching the piece pattern of section 1
  (`chief-of-staff-any.md` excepted) is named, whole or by a section, in some topic's readings. A
  piece added later without a topic fails it.
- **Every named topic exists**: a regex scan (`` `help ([a-z][a-z0-9-]*)` ``) of the text of every
  `*.py` under `src/` collects the names; each is a key of `topics.json`. The scan must find at
  least `MIN_NAMED` occurrences (the count at the head, which the Driver sets: 5 lease refusals, 2
  push, 2 restack, 1 handed back, 9 watcher lines, as written), so a broken scan cannot pass empty.
- **`help --for <role>` lists only that role's topics** (parametrized: `cr-driver`,
  `stack-driver`, `foreman`, `chief-of-staff`, and `coder` for the "no topic" line): in-process
  through `chantier.cli.main`, the listed names equal the set of topics whose `roles` holds the
  role; an unknown role exits 1 naming the roles.
- **`help lease` prints the section whole**: in-process, from a temporary folder with no project
  (so no batch and no `Repo`), exit 0, the first line `topic lease: …`, and the output holds the
  LF text of `driver-session.md`'s `## Means: the lease` section, read from the shipped file, and
  not the next section's heading. Plus: an unknown near name (`leas`) exits 1 with `did you mean
  help lease`; a topic with `--for` exits 1.
- **`help` stays local**: `"help"` is in `remote_wire.NEVER_REMOTE`, and `cli_run.judge` refuses
  it (one case added to the existing parametrized refusal test if there is one, else here).
- **Prepared cases, only where the shipped file cannot hold the case**, each named as prepared in
  its test id and paired with the shipped-file checks above: a `topics.json` with an `@action`
  reading, a missing heading and a bad `review_by` (each refused by `load_topics`), and one host
  map reading (resolved per `--host`), all written to `tmp_path`.
- **Behavioural assertions on the named lines**, by extending existing tests, each asserting the
  short `` `help <topic>` `` span, never a phrase: the missing-lease case of `tests/test_leases.py`
  (`help lease`), child 1's push refusal tests (`help lease`, `help refused-push`),
  `tests/test_restack_line.py`, `tests/test_ready_line.py`, and one of `tests/test_watch_stream.py`
  or `tests/test_watch_board.py` for an end line (`help watcher`, `help board`).

### 5. Scenario (`scenario/run_scenario.py`, `scenario/README.md`)

- In the `parallel` unit's section 1, right after the `rules` step (the line
  `_, out = w.chantier("rules")`), before the batch opens: `w.chantier("help", "lease")`, checked
  as "`help lease` prints the lease section whole, with no batch": exit 0, the first line starts
  `topic lease:`, and the output holds `claim lost` and the section's heading line read from
  `SKILL / "references" / "driver-session.md"`.
- `scenario/README.md`, "## Coverage": one bullet, `- help topics (unit: parallel): ``help lease``
  prints a topic whole with no batch; every topic resolves on both hosts and every topic a CLI line
  names exists in pytest (test: test_help_topics.py::<the resolution test>)`, so that
  `tests/test_scenario_coverage.py` passes.
- The two scenario reconstructions of `EVENTS_END` (around lines 2479 and 11194) do not change
  (section 3). Any scenario check of a changed lease, restack, handed-back or watcher literal is
  updated to the new text.

### 6. AGENTS.md

Edit the repository's root `AGENTS.md`, as child 1 left it:

- **The named-exceptions paragraph** gains, beside `access` and `live`, in the same style: "`help`:
  read-only, it prints a help topic whole from the plugin's own cards (`references/topics.json`
  names each topic's readings, the roles it serves and the line that names it), lists the topics,
  or one role's with `--for`, reading roles only as that data; it needs no batch and no project,
  writes nothing, reads no network and never runs through a profile; the CLI names a topic in a
  refusal or a line where a rare case starts; built on the user's answer simplify-cards-Q18
  (2026-11-24), with no measured cost."
- **Profiles:** `help` joins the commands that run where they are typed: the `cli.run` list ("any
  but `serve`, `webui`, `watch`, `live`, `login`, `logout` and `gate`", with child 1's `push`) and
  the `login` paragraph ("every command for those projects but `serve`, `watch`, `webui`, `live`,
  `login` and `logout`"), kept true with section 2's `NEVER_REMOTE`.
- No other rule changes. The sentence "The CLI knows no role" stays as is (child 9 rewrites it and
  names `help --for` there); `help` reads role names as data from the cards folder, so it stays
  true.

## Out of scope

- Removing the manifest, a piece or a role's start reading; any card text, `SKILL.md` or wrapper
  (the moments lists that the topics will replace shrink in children 19 to 24).
- Topic files of their own (`cards-next/topics/`), topic budgets (1.5 KB), `review_by` values and
  the deletion of never-read topics (children 19 to 25, and a later CR).
- `roles.yaml` (child 18); `brief`'s closing line (child 10); `next:` lines (child 12).
- A topic for the Foreman's watcher, `EVENTS_END`, the `batch:` line's `rules:` pointer, or
  refusals outside the files of section 3 (other rails, the hook's write guard).
- Counting topic reads (child 5's transcript measure); any CLI-side log of `help` calls.
- `docs/` (child 24 fixes the docs links; a docs sentence on `help` is not owed here).
- Any network read, any forge call, any write.

## Gates and evidence

- `just test` green with the new file and the extended assertions. The PR states under
  Deliverables the seconds its tests add to `just test`, measured before and after on the same
  machine (expected under 1 s: one JSON load, a regex over `src/`'s text, a handful of in-process
  calls).
- `just check` and `just eval-dry-run` (a change under `src/`) in the worktree at the rebased head
  before the first push.
- The long gate `just scenario (ubuntu-latest)` green at the PR's head (the CLI and the scenario
  change). The local Windows `chantier gate <cr> scenario` is owed only while this CR is the
  stack's top; it moves to the CR that joins above it.
- The PR's Deliverables quote, as printed: `help` (the list's first lines), `help --for
  cr-driver`, and the first lines of `help lease`.
- Checks that guard shipped files (`topics.json`, the cards, the CLI's sources) read them from the
  repository at the head under test; the prepared texts of section 4 cover only refusals and the
  host map no shipped topic holds, each paired with a shipped-file check.
- No host or default matrix: no topic of this child has a host-dependent reading, and nothing
  depends on a configured value; the host-map branch is covered by the both-host resolution test
  and the one prepared case.
- No `just mod` (no change to `hooks/` or `types/`); no journal type.

## Risk

- Tests and the scenario read the lines this child extends: covered by appending only, by the
  insertion point chosen for the watcher lines, and by the Driver's grep of each literal.
- A topic pointing at a heading a later card edit renames: the resolution test fails at once,
  until the swap (child 24) repoints the readings.
- Whether a role reads a topic when a line names it is **unproved**: child 5 counts `help` reads,
  child 28 measures them on the new cards.
- `--for chief-of-staff` lists the Foreman's topics too (answer 13): a longer list for the Chief of
  Staff outside direct mode, accepted.

## Open questions

1. sc07-Q1: `help` reads only the plugin's cards, so this spec makes it run where it is typed,
   never through a profile (it joins `NEVER_REMOTE`; the server's `cli.run` then refuses it), so a
   role reads the cards of the plugin it loaded, not the server's build. The alternative forwards it
   like any command and prints the server's cards. Keep it local (default)?
2. sc07-Q2: The watcher's common restart line (`EVENTS_END`, `still running: for the Chief of
   Staff, …`) names no topic here, because any insertion splits the text the Chief of Staff's card
   quotes and the tests read; the other nine end lines for the Chief of Staff name `help watcher`
   or `help board`. Leave `EVENTS_END` unchanged (default), or insert the topic and update the
   tests and scenario that quote it?
