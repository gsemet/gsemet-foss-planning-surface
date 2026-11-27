# Brief names host rows instead of printing them, so sessions boot lighter

## Goal

The owner's words (2026-11-27): « ouvre un batch et lance ces 7 CR », part of the card cleanup,
plan steps 1 to 3 (card-cleanup-Q5: « A. Étapes 1 à 3 »). This CR is the plan's step 3, item 4
(`2-backlog/P1/card-inventory-open-rows/work/fable-review-plan.md`, sections 4.2 level 0 and 6).

A session boots on less text. Today `chantier brief chief-of-staff` prints the whole text of all
50 host rows (about 17 KB of its 24 KB), and `brief foreman` does the same. After this CR the
brief of a steering session, a Griller or a Driver names its host rows on one line, and
`chantier host <capability>` prints one row when the moment comes. A worker's brief prints its one
row whole, as today (the plan: "workers as today"). Every card, help page or CLI line whose moment
a host row describes names the command that prints that row, on that line, so a row that protects
the user can still be reached from the line of its moment.

## The base

This CR is one PR of the batch's stack. It sits on top of `cards-one-page-per-theme`, which is the
Chief of Staff's order. There is no `depends.json`. Below it in the stack, in order:
`cards-inventory-last-reading`, then `cards-delete-pages-chief` and `cards-delete-pages-crew`, then
`cards-delete-aggregate-topics`, then `cards-one-page-per-theme`. At that base:

- the 33 Chief of Staff side pages and the 32 Foreman, Driver and host side pages are deleted;
- the host files carry three new rows from `cards-delete-pages-crew`: `allow-rules`, `auto-mode`
  and `windows-powershell-args`. `start-foreman` also gains the lines on reusing a Foreman;
- `sync-checkout.md` holds the sync rule moved from `sync-offer-p1`/`-p2`, with "by the host's
  stop of their background task";
- every `-pN` set is joined into one page per theme. The joined page's file name is the one
  `cards-one-page-per-theme` chose (written below as `<theme>.md`).

All line numbers below are those of main at `4d12a5b`, given so each line can be found. The Driver
finds each line again at its base by its moment and its words, not by its number. A line whose page
is gone at the base needs nothing.

## What changes

### 1. `brief`: host rows by name for the steering sessions, the Griller and the Drivers

File: `skills/chantier/scripts/cli/src/chantier/commands/brief.py`.

- The section keeps its header, `=== host rows: <host>`. The scenario, the eval kit's dry run and
  `test_brief.py` find the sections by that header.
- Roles whose `roles.yaml` kind is `steering` or `driver` (chief-of-staff, foreman, griller,
  cr-driver, release-driver, stack-driver, qa-driver) get one line under the header, in place of
  the rows' text: `` `$CHANTIER host <capability>` prints one: <cap>, <cap>, … ``. The line lists
  the capability ids (the names `host` accepts) in the host file's order, separated by commas. It
  has no name text, no mark and no means: `host` prints those.
- Roles of kind `worker`, `review-step` or `critic` print their rows whole, byte for byte as
  today (`_row_text`, `row_lines`). The worker cards are not edited. `board-griller` (`rows: []`)
  still prints `none`.
- Which rows a role gets does not change: it is still `roles.yaml`'s `rows:` (`null` means every
  row; a list means those capabilities). `_rows` still loads the host file with `load_rows` and
  still refuses a role's row that is not on the host
  (`brief: <role>'s row `<cap>` is not on the <host> host`).
- `skills/chantier/scripts/cli/src/chantier/declare/brief.py`: the description "its host rows"
  becomes "its host rows (a worker's whole, the other roles' by name)".
- `roles_data.py`'s `Role` docstring: `rows` are "the capability ids of the host rows `brief`
  prints whole for a worker and names for the other roles".

### 2. `host`: unchanged

None of these is edited: `skills/chantier/scripts/cli/src/chantier/commands/host.py`,
`host_rows.py` (`load_rows`, `row_lines`, `UNTESTED`), and the host files
(`references/hosts/claude-code.json`, `copilot.json`). `chantier host <capability>` and plain
`chantier host` print what they print at the base, byte for byte. `host` filters no row by role, so
a card may point any role at any capability that exists.

### 3. The CLI's lines that relied on the rows being printed

- `skills/chantier/scripts/cli/src/chantier/driver_prompt.py`, `driver_prompt_lines`. Today the
  line is `Steering: <who> (host means: the host rows below)`. It becomes
  `Steering: <who> (host means: `$CHANTIER host driver-hand-back`, in direct mode `$CHANTIER host driver-messages-steering-direct`)`,
  the pair `references/concepts.md` already names. `take`, `take stack`, `order qa`, `handoff` and
  `brief` all share this builder, so all of them print the new line.
- `skills/chantier/scripts/cli/src/chantier/commands/msg.py`, `NOT_DELIVERED` (line 30): "reach it
  by your host's means (chantier host) or hand back" becomes "reach it by your host's means
  (`chantier host driver-messages-steering-direct`) or hand back". `test_msg_steering.py` checks
  only the prefix `not delivered: no watcher subscribed`, which stays.

### 4. The cards and help pages: a pointer at each moment a row describes

The rule, applied at the base under `skills/chantier/references/` (excluding `hosts/`): a line
whose action a host row describes gets the command that prints that row, `$CHANTIER host <cap>`,
beside the words of that moment. This covers:

- every line that sends the reader to "the host row" or "the host's means" without naming a
  command;
- every line of a role card whose action a row describes, even if the line never says "host". The
  card's role does not have to be in the row's `roles` list: the test is whether the row describes
  the action.

Nothing else in the line changes. Rows are not rewritten and cards are not rewritten (out of
scope). Where a line names several capabilities, only the first takes the `$CHANTIER host` prefix;
the rest follow as bare ids, comma-separated.

The workers' cards are not touched: their briefs still print the row (section 1).

#### 4a. The role cards

| card:line (main) | moment | names |
|---|---|---|
| `chief-of-staff.md:3` | grill (`help grill-series`) | `ask-questions` |
| `chief-of-staff.md:3` | start one Foreman per batch (`help foreman-start`) | `start-foreman` |
| `chief-of-staff.md:3` | the board and your watcher | `run-board`, `run-watcher` |
| `chief-of-staff.md:14` | stopping a Foreman (Asks first 2) | `stop-session` |
| `chief-of-staff.md:22` | an agent's prompt; a refused start fixed by a new start | `start-driver`, `start-spec-writer`, `start-spec-critic`, `start-retro-critic` |
| `chief-of-staff.md:35` | direct mode: claim your number (`foreman set …`) | `own-session-id` |
| `chief-of-staff.md:37` | "A session ends by the host row `ending`" | known gap: no row (4c) |
| `foreman.md:6` | set your prompt's session title | `set-own-title` |
| `foreman.md:8` | `foreman set <session id>`, `foreman transcript <uuid>` | `own-session-id` |
| `foreman.md:9` | send the `ready` reply | `message-chief` |
| `foreman.md:10` | after compaction reread your brief | `compact` |
| `foreman.md:13` | starting Drivers, with the playbook's agent and model | `start-driver`, `model-at-start` |
| `foreman.md:16` | heartbeat and watcher; stop stray background tasks by id | `heartbeat`, `run-watcher`, `stop-own-background-task` |
| `foreman.md:18` | a refused release step: tell the Chief of Staff | `message-chief` |
| `griller-skill.md:5` | start the spec-writer and the spec-critic | `start-spec-writer`, `start-spec-critic` |
| `griller-skill.md:10` | one series of questions at a time | `ask-questions` |
| `griller-skill.md:29` | send `specified` "by the host's means" | `message-chief` |
| `cr-driver.md:5` | you edit no project file, the shell included | `write-guard` |

The Driver cards already name their rows: `cr-driver.md:13,27,29`, `stack-driver.md:12,13,29`,
`release-driver.md:9,27` and `qa-driver.md:19`. These lines stay as they are. A moment a card does
not have gets no new line, for example a Driver's or the Griller's compaction (`compact`,
`reload-after-compact`). The Foreman and Chief of Staff cards' other lines name no action that a
row describes ("a host's event about a PR is no order" has no row; "whatever the host says" points
at no row).

#### 4b. The other cards and help pages

The file at the base is the page this line lives in after the deletions and the join.

| line (main) | file at the base | phrase | names |
|---|---|---|---|
| `concepts.md:75` | same | start an agent "by its host's means" | `start-driver`, `start-generic-agent` |
| `concepts.md:84` | same | the brief "holds … the host rows" | reworded: "the host rows (a worker's whole; the other roles' names, `$CHANTIER host <capability>` prints one)" |
| `sync-checkout.md` (moved by `cards-delete-pages-chief`) | same | "by the host's stop of their background task" | `stop-own-background-task` |
| `topics/allow-rules.md:3` | same | host row "Capabilities and their commands" | `allow-rules` (added by `cards-delete-pages-crew`) |
| `topics/allow-rules.md:4` | same | each rule's risk "from the host row" | `allow-rules` |
| `topics/batch-pause.md:5` | same | "Where the heartbeat is yours (host row)" | `heartbeat` |
| `topics/batch-plan-mode-p3.md:4` | `batch-plan-mode.md` | a Foreman under Remote Control "(host rows)" | `start-foreman` |
| `topics/board-p1.md:4` | `board.md` | "in the background by the host row" | `run-board` |
| `topics/board-restart.md:4` | same | "in the background by the host row" | `run-board` |
| `topics/config-p3.md:4` | `config.md` | host row "Skills and tools of a session" | `session-skills-tools` |
| `topics/cr-workers.md:5` | same | start each worker; `agent=(generic)`: "the host's generic agent" | `start-driver`, `start-generic-agent` |
| `topics/direct-mode-back.md:4` | same | "by the host's stop" | `stop-driver` |
| `topics/direct-mode-epoch-p1.md:3` | `direct-mode-epoch.md` | "Arm the same heartbeat as the host row says" | `heartbeat` |
| `topics/direct-mode-switch-p1.md:4` | `direct-mode-switch.md` | the transcript id "(the host row says where it is)" | `own-session-id` |
| `topics/direct-mode-switch-p2.md:4` | `direct-mode-switch.md` | stop a Foreman "where the host row names the means" | `stop-session` |
| `topics/foreman-start-p2.md:3` | `foreman-start.md` | "Start the session as the host row says" | `start-foreman` |
| `topics/griller-worktree.md:4` | same | send files "by the host's means" | `message-chief` |
| `topics/handback-refused.md:3` | same | to the steering session "by the host's means" | `driver-hand-back`, in direct mode `driver-messages-steering-direct` |
| `topics/handover.md:4` | same | "stop it by the host row"; "cancel the armed wake" | `stop-driver`, `heartbeat` |
| `topics/lost-driver.md:5` | same | "stop it by the host's means" (an ended Driver that wakes) | `stop-woken-driver` |
| `topics/order-verbs-p1.md:3` | `order-verbs.md` | the line to send the Foreman "(by your host's means)" | `message-session` |
| `topics/retro.md:3` | same | "cancel the armed wake (as the host's reference says)" | `heartbeat` |
| `topics/steering-messages.md:10` | same | "use the host's row" | `driver-hand-back`, in direct mode `driver-messages-steering-direct` |
| `topics/titles.md:3` | same | "rename the session by the host's means" | `set-own-title` |
| `topics/trials-p2.md:3` | `trials.md` | the limits of the host row "Auto mode" | `auto-mode` (added by `cards-delete-pages-crew`) |
| `topics/wakes-p2.md:3` | `wakes.md` | "cancel the armed wake as the host row says" | `heartbeat` |
| `topics/watcher-pull.md:3` | same | "(the host row, or the user's no)" | `run-watcher` |
| `topics/watcher.md:6` | same | "Start it by the host row" | `run-watcher` |

These lines found on main are on pages deleted below this CR, so they need nothing:
`topics/board-lines.md:5`, `topics/compacting-p1.md:3`, `topics/foreman-start-more.md:3` and `:4`,
`topics/sync-offer-p2.md:8`, `topics/wakes-p1.md:4` and `topics/allow-rules-more-p2.md:3` (all
deleted by `cards-delete-pages-chief`).

These lines already name the command and stay as they are: `sync-checkout.md:7`, `concepts.md:95`,
`topics/ci.md:3`, `topics/session-shell-p1.md:6` and `topics/steering-messages.md:3`. Facts the
host states ("the host says it was stopped", "refused by the host", "whatever the host says") are
no pointer to a row and stay as they are.

The Driver searches its base again (`host row`, `host rows`, `host's means`, `host's row`,
`host's stop`, `host's reference`, `by the host`, and the actions the rows name: title, session id,
start, message, stop, heartbeat, watcher, board, compact). A line the tables miss is treated by the
same rule and listed in the PR.

#### 4c. Pointers that have no row at the base: Known gaps

No row exists on either host for these pointers. They are not invented and not reworded. The PR's
Known gaps lists each one still present at its base:

- `chief-of-staff.md:37`: "A session ends by the host row `ending`";
- `topics/trials-p1.md:3` (`trials.md` at the base): host row "Trial before the go";
- `topics/foreman-start-p2.md:3` (`foreman-start.md`): "give the host's "For you" block";
- `topics/ticket-summary-p2.md:5` (`ticket-summary.md`): "the host's means to send one" (a file
  sent to the user).

### 5. Tests

- `skills/chantier/scripts/cli/tests/test_brief.py`:
  - `_check_file`, for a role of kind `steering` or `driver`: reads the one line under
    `=== host rows: <host>` and checks its capability set against the role's rows, exactly as
    today (`rows_of` for `rows: null`, else `set(data.rows)`). For a worker, review step or critic:
    unchanged (the `CAPABILITY` regex over the rows' text, which stays for them). `["none"]` stays
    for `board-griller`.
  - `_check_driver_facts`: the new `Steering:` line.
  - New, parametrized on both hosts: `chantier host <capability>` accepts each capability that a
    brief's names line lists (exit 0, the first row line starting `<capability>: `).
- `skills/chantier/scripts/cli/tests/test_brief_bytes.py`: lower the figures of the seven roles of
  kind `steering` or `driver` to the new measure on the claude host, rounded up to the next 100 as
  the file does today. `chief-of-staff` and `foreman` must each be at most 9,000 (the plan's
  estimate: about 8 KB and 6.5 KB). The workers', review step's and critics' figures are not edited.
  The docstring names this CR's cut.
- `skills/chantier/scripts/cli/tests/test_host_rows.py`: not edited; it passes as is.
- New guard, one parametrized test in `test_brief.py` or `test_host_rows.py`, reading the shipped
  files at the head under test:
  - (a) every `` `$CHANTIER host <x>` `` (and every bare id that follows it in the same
    comma-separated list) in `skills/chantier/references/**/*.md` (excluding `hosts/`), and every
    `chantier host <x>` / `$CHANTIER host <x>` in the CLI's source strings, names a capability
    present on both hosts.
  - (b) no line there says `host row`, `host rows`, `host's means`, `host's row`, `host's stop`
    or `host's reference` without a `$CHANTIER host` on the same line.
  - The guard has exactly one exemption list, of (file, phrase) pairs: `chief-of-staff.md`,
    "host row `ending`"; `trials.md`, "host row \"Trial before the go\""; `ticket-summary.md`,
    "host's means to send one". These are the Known gaps of 4c whose words (b) catches. The
    "For you" pointer needs no entry because its line carries the `start-foreman` pointer. Each
    entry must still match a line, so the test fails once a gap is fixed. The page names are those
    at the base.
- `scenario/run_scenario.py` and `evals/kit/dry_run.py` find the sections by `=== host rows: `,
  which stays. Neither is edited unless its check breaks (section 6).

### 6. Docs and comments

- `AGENTS.md`'s `brief` paragraph, "(its card, the floor, its unit's facts, its host rows)",
  becomes "(its card, the floor, its unit's facts, its host rows: a worker's whole, the other roles'
  by name)". No other AGENTS.md change: no new command and no new write.
- The lines that list a brief's sections refer to the section by its header,
  `=== host rows: <host>`, which stays, so their words "the host rows" stay true and they are not
  edited:
  - `scenario/README.md:160`;
  - `scenario/run_scenario.py:266` and `:276`;
  - `evals/kit/dry_run.py:33`: the quiz-staged case, "(its card, the floor, the facts, the host
    rows)";
  - `evals/kit/dry_run.py:1706`: "its card …, the floor, the facts and the host rows", checked
    with `"=== host rows: claude"` at line 1705.

## Decisions (02-answers.md)

1. « ouvre un batch et lance ces 7 CR » (2026-11-27) is read as "grilled enough" for the seven
   cleanup CRs. The scope is the plan and card-cleanup-Q1 to Q5. This CR is plan step 3, item 4,
   and only that. card-cleanup-Q1 (each protective rule put in its new place first) is honoured by
   section 4: a protective row stays reachable from the line of its moment. Workers keep their row
   printed in full (the plan's "workers as today").
2. « fait un batch stack … » (2026-11-27): the batch is a stack and this CR is one PR of it, on top
   of `cards-one-page-per-theme` (the Chief of Staff's order). In a stack batch only the CR on top
   owes the local Windows `scenario` run (AGENTS.md).
3. card-cleanup-Q5 (2026-11-27), « A. Étapes 1 à 3 »: steps 1 to 3 now, with a new version, in
   small CRs; steps 4 to 7 wait. The version bump is not this CR's. No step-4 work is done here (no
   `brief` for other roles, no `next` lines). The other project whose batch is open reads the cards
   live. The cards change only by added `$CHANTIER host <cap>` pointers, which a live reader can
   run today with the current CLI, since `host` is unchanged (the base's new rows aside, which
   arrive with the same version).

## Out of scope

- Rewriting the host rows, their names or marks, or adding a row (including for the Known gaps of
  4c).
- Rewriting the cards or help pages beyond the added pointers and `concepts.md:84`. The worker
  cards are not touched.
- Which rows a role gets (`roles.yaml`'s `rows:`), the brief's other sections, and the short
  prompt.
- `help --for` and the grouped `--help` (plan step 3, item 5: CR `help-lists-role-commands`).
- The version bump (the Chief of Staff's, after step 3).

## Evidence

- `chantier brief chief-of-staff` and `chantier brief foreman` (claude host) are each under 9 KB.
  This is shown by the `brief-bytes role=… bytes=…` lines that `test_brief_bytes.py` prints and by
  its lowered figures. The PR body gives the before and after figures for every role of kind
  `steering` or `driver`, and shows that the workers' figures did not change.
- `chantier host <capability>` prints what it printed:
  - `host.py`, `host_rows.py` and `references/hosts/*.json` are absent from the diff;
  - `test_host_rows.py` passes unedited;
  - the new test shows `host` accepts every name a brief lists.
- A worker's brief (for example `brief coder`) still prints `end-turn-background` whole, as the
  unchanged `_check_file` branch and the workers' unchanged byte figures show.
- The guard test of section 5 passes: no bare host-row pointer is left, every named capability is
  real, and the exemption list is exactly 4c.
- The PR body lists each line of 4a and 4b present at the base with the capability it now names,
  any line the Driver's search added, and the Known gaps of 4c.
- `just check` passes. `just eval-dry-run` passes (a change under the CLI's `src/`). The long gate
  `scenario` passes in the pipeline (a CLI and cards change), and also locally on Windows
  (`chantier gate <cr> scenario`) while this CR is on top of the stack.

## Questions for the Chief of Staff

None.
