# Group chantier --help and list each role's commands in help

## Goal

A role finds its own commands without reading 57. `chantier --help` prints the commands in six
groups; `chantier help --for <role>` prints the role's commands before its topics; the commands
that are a second name for the same code are folded under one name, and every old name still
runs as before.

This is the card cleanup's step 3, item 5 (`2-backlog/P1/card-inventory-open-rows/work/fable-review-plan.md`,
sections 4.3 and 6), one of the seven CRs of the cleanup batch.

## Decisions this specification carries

- `02-answers.md` 1: the owner's go (« ouvre un batch et lance ces 7 CR », 2026-11-27) is taken as
  "grilled enough"; the scope is the plan and the five answers of
  `2-backlog/P1/card-inventory-open-rows/02-answers.md`. The Chief of Staff's reading of that go
  is still to confirm by the owner (question 1).
- `02-answers.md` 2: the batch is a stack. This CR shares no code with the other cleanup CRs but
  `test_help_topics.py` (step 1 deletes topics; see "Risks").
- `02-answers.md` 3 (card-cleanup-Q5, « A. Étapes 1 à 3 »): this is one of the small CRs of steps
  1 to 3; the new version is the batch's, not this CR's; steps 4 to 7 wait.
- The request's reading, to confirm by the owner (question 2): only a fold that is a second name
  for the same code belongs here. `access` folded into the refusals, `phase` set by other
  commands, and the plan's new commands (`restart`, `ci`, `pr`, steering `push` and `rebase`) are
  later steps.

## What changes

### 1. The folds: new spellings of existing commands

Twelve old names get a new spelling. Each new spelling runs the old command's own handler with
the same arguments; nothing in the handlers changes. The old names stay registered, unchanged,
with their own `--help`.

| old name (still runs) | new spelling | notes |
|---|---|---|
| `abandon <item>` | `triage <item> --abandon` | `--abandon` joins `triage`'s required one-of group (`--priority`, `--ready`, `--inbox`, `--running-batch`) |
| `restore <item> [--slug S]` | `triage <item> --restore [--slug S]` | `--slug` is accepted with `--restore` only |
| `park <cr> [--wait …] [--note …]` | `order park <cr> [--wait …] [--note …]` | records no order (O-k): it is `park`, run under `order`'s name |
| `inbox [--read SEQ\|all]` | `msg --read` (lists, as `inbox`) and `msg --read SEQ\|all` (marks, as `inbox --read`) | `--epoch` as for `inbox`; `msg steering …` unchanged (question 3) |
| `interests [--kind K] [--json]` | `journal interests [--kind K] [--json]` | a second action beside `journal add` |
| `log <cr> [--lease N]` | `handoff <cr> --log [--lease N]` | |
| `serve …` | `board serve …` | every option of `serve` |
| `webui` | `board webui` | |
| `live …` | `board live …` | |
| `login …` | `board login …` | `login`'s own `--project` (repeatable) kept |
| `logout` | `board logout` | |
| `watch …` | `board watch …` | |

`board` with no action is refused by argparse with its usage (`board serve`, `board webui`, ...);
an old line `chantier board --seat <id>` (the server's name before v0.10, see
`tests/test_command_names.py`) is refused the same way, never served.

A run by a new spelling is the old command's run in every way the CLI tells apart today, all held
by `args.cmd` or argv in `skills/chantier/scripts/cli/src/chantier/`:

- `cli.py`: the same `args.cmd` (so `FULL_OUTPUT`, the `order qa` case, the `serve` exception to
  `with_notes`, and `repo.COMMAND`, the name a refusal and a surface commit carry, are unchanged:
  `board serve` is recorded as `serve`, `triage x --abandon` as `abandon`).
- `core/remote_wire.py` `NEVER_REMOTE`, read by `clients/remote.py` (never forwarded) and
  `board/cli_run.py` `judge` (refused by the server's `cli.run` with
  `cli.run: <old name> does not run through the server`): `board serve`, `board webui`,
  `board live`, `board login`, `board logout` and `board watch` are never forwarded and refused
  there exactly as their old names. `journal interests` runs through a profile as `interests` does.
- `near_misses.py`: `--epoch N` before the command name is moved for a new spelling exactly as for
  its old name (`--epoch 3 msg --read` as `--epoch 3 inbox`, `--epoch 3 order park CR-1` as
  `--epoch 3 park CR-1`); `EPOCH_COMMANDS` stays equal to the parser's (its test,
  `test_the_epoch_commands_are_the_parsers`, is kept true).
- The board server's `cli.run` reads a new spelling as the CLI does (it parses with the same
  `normalize` and `_parser`), so `test_the_server_reads_the_same_forms_as_the_cli` covers them.

The mechanism (nested subparsers with the old `cmd` set as a default, or a rewrite of argv in
`near_misses.normalize` before parsing, or both) is the Driver's choice; the behaviour above is
the requirement and the tests below hold it.

Each new spelling's `--help` ends with the old name in its "also accepted:" epilog
(`commands/registry.py` `also_text`), and each old name's `--help` names its new spelling there.

### 2. `chantier --help` in six groups

`chantier --help` prints the usage line with `<command>` in place of today's brace of 57 names,
then the commands in six groups, in this order, each command with its help text as today. Only
commands that exist today; the plan's `restart`, `ci` and `pr` are not listed.

| group | commands |
|---|---|
| session | `preflight`, `init`, `seat`, `rules`, `playbook`, `host`, `help`, `brief`, `access` |
| backlog | `file`, `triage`, `summary`, `validate` |
| batch | `open`, `order`, `status`, `asks`, `cost`, `retro`, `close`, `cancel` |
| steering | `foreman`, `next`, `judge`, `conflicts`, `agents`, `msg`, `stack`, `forge-stack`, `pause` |
| unit | `take`, `round`, `note`, `phase`, `gate`, `push`, `ship`, `verdict`, `handback`, `handoff`, `lease`, `wait`, `release` |
| board | `board` (`serve`, `webui`, `live`, `login`, `logout`, `watch`), `sync`, `journal` |

Against the plan's table: `access`, `phase` and `release` exist today and the plan's table leaves
them out (`access` and `phase` because it folds them later); they go to session, unit and unit
(question 4). The plan's `link` is `webui` today and keeps its name.

A last block, "old names, still accepted", lists the twelve old names, one line each, with their
new spelling (`abandon <item>  = triage <item> --abandon`).

The groups live in one constant in the CLI (beside `_MODULES` in `cli.py`, or in
`commands/registry.py`), and a test holds that every name the root parser accepts is in exactly
one group or in the old-names block. The plan's "argparse groups" claim is not relied on:
argparse puts subcommands in no argument group, so the Driver formats the root help itself
(a formatter or a description built from the constant).

### 3. `help --for <role>` lists the role's commands

`skills/chantier/roles.yaml` gains one field per role, `commands`: the chantier commands the role
runs, each in the spelling the grouped help prints (a fold by its new spelling, `board watch`,
`msg --read`, `handoff --log`). The CLI still knows roles only as data
(`roles_data.py` reads the field, checks it is a non-empty list of texts and adds it to `Role`
and `FIELDS`; the header comment of `roles.yaml` names it; `scripts/roles_check.py` and the agent
files of both hosts are unchanged, since the wrappers do not carry it).

`chantier help --for <role>` prints, before today's topic lines:

    commands: take, round, note, ...

then the topic lines as today (`<topic>: <trigger>`); a role with no topic prints the commands
line, then `no topic for <role>; help lists them all`. An unknown role is refused as today.
`help` with no argument and `help <topic>` are unchanged.

The lists are written from the role's card: every chantier command the card names (as
`$CHANTIER <cmd>`, or as a backticked command the role itself runs), plus `help`, mapped to the
new spelling. A starting point, read from the cards at this base and to be checked card by card
by the Driver (a backticked word that is a step and not a command the role runs, as `conflicts`
in `cr-driver.md`'s list of topics, is left out):

| role | commands |
|---|---|
| cr-driver | take, round, note, phase, gate, push, ship, handback, handoff, lease, wait, msg, next, host, help |
| release-driver | take, note, phase, gate, push, ship, release, handback, handoff, lease, wait, msg, host, help |
| stack-driver | take, note, gate, push, ship, stack, forge-stack, handback, handoff, lease, msg, next, host, help |
| qa-driver | lease, gate, host, help |
| verifier | gate, verdict, handoff, help |
| spec-writer | summary, help |
| board-griller | summary, access, rules |
| griller | seat, access, rules, file, triage, summary, help |
| foreman | foreman, next, status, asks, judge, conflicts, agents, msg --read, take, handoff, order, gate, pause, playbook, release, retro, note, stack, forge-stack, push, board watch, host, help |
| chief-of-staff | the session, backlog, batch and board groups whole, with next, judge, conflicts, agents, msg --read, stack, forge-stack, pause, take, note, gate, push, handoff, wait, release |
| coder, conflict-resolver, debugger, inspector, investigator, spec-critic, retro-critic, demo-explorer | help |

### 4. What does not change

- No command line the CLI prints changes in this CR: every `next:` line, refusal, `brief`
  prompt and watcher line keeps the old names. So the user's allow rules keep matching (P10's
  chantier rows are `… chantier *` forms, which match any spelling anyway, `commands/allow_samples.py`),
  and the host rows (`references/hosts/*.json`), the cards, the topics, the scenario and
  `AGENTS.md` stay true as they are: every name they print still runs.
- `AGENTS.md` needs no edit: the commands it names (`serve`, `webui`, `watch`, `live`, `login`,
  `logout`, `interests`, `inbox`, ...) all still run, and its lists of commands that never run
  through a profile or the server hold for the new spellings, which are refused the same way.
  A new spelling is not a new tool, so the measured-cost rule does not apply.
- `tests/test_command_names.py` keeps forbidding the server's old command, `chantier board` used
  as the server: its `TEXT` and `WEB` patterns are narrowed to the old forms (`board` followed by
  an option or nothing) so that a text may name `chantier board serve` and the other five
  actions; its four prepared old forms stay caught, and a fifth case shows `chantier board serve`
  is not.

## Out of scope

- `access` folded into the refusals and `next <cr>`; `phase` set by `round`, `ship`, `gate` and
  `verdict`; the new commands of the plan (`restart`, `ci`, `pr body`, `pr check`, steering `push`
  and `rebase`, `preflight --add-rules`, a `forge` command); the fast-forward in `order merged`.
- Removing an old name, or a date for it.
- Changing a card, a topic, a host row, the scenario or a printed line to use a new spelling.
- `brief`'s host rows and ceilings (step 3, item 4, another CR) and the version bump (the batch's).
- Copilot's classifier and any host-specific change.

## Evidence

- The PR's Deliverables hold the output of `chantier --help`, `chantier help --for cr-driver` and
  `chantier help --for chief-of-staff`, run at the PR's head.
- A parametrized test (in `skills/chantier/scripts/cli/tests/`, in-process, fast) over the twelve
  pairs of the table in section 1: the old form and the new form parse, with the real
  `cli._parser()` after `near_misses.normalize`, to the same handler and the same argument values,
  `cmd` included; the same with `--epoch N` before the command for `park` and `inbox`; and each
  old name still runs (`main([...])` on a prepared state, or `--help` exit 0 for the six server
  commands, which must not start a server in a test).
- `clients/remote.py` and `board/cli_run.py` `judge`: `board serve` and `board watch` (with the
  four others in the same parametrization) are refused as `serve` and `watch` are, by their old
  name's text.
- A test that every name the root parser accepts is in exactly one help group or in the old-names
  block, and that `--help` prints the six group titles in order.
- `test_roles_data.py`: the shipped `roles.yaml` gives every role a non-empty `commands` list;
  each entry parses as a command of the real parser; each `$CHANTIER <cmd>` a role's card names
  (read from the shipped card at the head under test) is in that role's list, by its new spelling
  for a fold; a prepared role without `commands` is refused naming the role and the field.
- `test_help_topics.py`: `help --for <role>` prints `commands: …` first, then that role's topics
  only; the board-griller case prints its commands line then `no topic for board-griller; help
  lists them all`.
- `test_command_names.py` as in section 4.
- `just check` passes; `just roles` passes; `just test` stays within its time budget; the long
  gate `scenario` passes (a CLI change), unchanged since every name it types still runs.

## Risks

- Step 1's CRs delete topics and edit `topics.json` in the same batch: `test_help_topics.py`
  changes on both sides; in the stack the later CR rebases on the earlier one.
- `board` was the server's own name before v0.10; reviving it as a group is the plan's choice
  (section 4.3) and the request's; an old `chantier board --seat` line is refused, never run as
  the server.

## Questions for the Chief of Staff

1. The go « ouvre un batch et lance ces 7 CR » taken as "grilled enough" for this CR: confirmed by
   the owner?
2. Only the folds that are a second name for the same code (the twelve of section 1), with
   `access`, `phase` and the new commands left to later steps: confirmed?
3. `msg --read` with no value lists the unread messages (today's `inbox`) and with `SEQ|all` marks
   them read (today's `inbox --read`): is that the reading of the plan's "`inbox` into
   `msg --read`", or should `msg --read` alone mark nothing and a separate spelling list?
4. `access` in session, `phase` and `release` in unit, which the plan's table leaves out: right
   groups?
5. `help --for` lists a fold by its new spelling (`board watch`) while the cards still say the old
   name (`watch`): acceptable until a later step rewrites the cards, or should the list use the
   cards' names for now?
