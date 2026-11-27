# Brief prints host rows by name only, so sessions boot lighter

## Goal

The owner's words (2026-11-27): « ouvre un batch et lance ces 7 CR », part of the card cleanup,
plan steps 1 to 3 (card-cleanup-Q5: « A. Étapes 1 à 3 »). This CR is the plan's step 3, item 4
(`2-backlog/P1/card-inventory-open-rows/work/fable-review-plan.md`, sections 4.2 level 0 and 6).

A session boots on less text. Today `chantier brief chief-of-staff` prints the whole text of all
50 host rows (about 17 KB of its 24 KB) and `brief foreman` the same. After this CR a brief names
its host rows on one line, and `chantier host <capability>` prints one row when the moment comes.
Every card, help page or CLI line that counted on a row's text being in the brief names the
command that prints it, at that moment.

## What changes

### 1. `brief`: the host rows by name only

File: `skills/chantier/scripts/cli/src/chantier/commands/brief.py`.

- The section keeps its header, `=== host rows: <host>` (the scenario, the eval kit's dry run and
  `test_brief.py` find the sections by it). Below it, one line in place of the rows' text:
  `` `$CHANTIER host <capability>` prints one: <cap>, <cap>, … `` with the capability ids (the
  names `host` accepts), in the host file's order, comma-separated. No name text, no mark, no
  means: `host` prints those.
- Which rows a role gets does not change: `roles.yaml`'s `rows:` (`null`: every row; a list: those
  capabilities). `_rows` still loads the host file with `load_rows` and still refuses a role's
  row that is not on the host (`brief: <role>'s row `<cap>` is not on the <host> host`). A role
  with no row (`board-griller`, `rows: []`) still prints `none`.
- This applies to every role (the request: "`chantier brief` prints the host rows of a role by
  name only"); see question 1.
- `_row_text` and the `row_lines` import go from `brief.py` if nothing else there uses them.
- `skills/chantier/scripts/cli/src/chantier/declare/brief.py`: the description says "the names of
  its host rows" in place of "its host rows".
- `roles_data.py`'s `Role` docstring: `rows` are "the capability ids of the host rows `brief`
  names".

### 2. `host`: unchanged

`skills/chantier/scripts/cli/src/chantier/commands/host.py`, `host_rows.py` (`load_rows`,
`row_lines`, `UNTESTED`) and the two host files (`references/hosts/claude-code.json`,
`copilot.json`) are not edited. `chantier host <capability>` and plain `chantier host` print what
they print today, byte for byte.

### 3. The Driver's `Steering:` fact

File: `skills/chantier/scripts/cli/src/chantier/driver_prompt.py`, `driver_prompt_lines`. Today:
`Steering: <who> (host means: the host rows below)`. It becomes:
`Steering: <who> (host means: `$CHANTIER host driver-hand-back`, in direct mode `$CHANTIER host driver-messages-steering-direct`)`,
the same pair `references/concepts.md` already names. `take`, `take stack`, `order qa` and
`handoff`, which share this builder, print the new line too.

### 4. The cards and help pages that relied on the row in the brief

Rule, applied at the CR's base (the files that exist there; a page another CR of the batch deleted
below this one needs nothing): every line under `skills/chantier/references/` (but `hosts/`) that
sends the reader to a host row or "the host's means" with no command gets
`` `$CHANTIER host <capability>` `` beside that phrase, at the moment the line describes, and
nothing else in the line changes. Rows are not rewritten and cards are not rewritten (out of
scope). The list found on main at 4d12a5b, with the capability each one names:

| file:line (main 4d12a5b) | phrase | names |
|---|---|---|
| `concepts.md:75` | "by its host's means" (start an agent) | `start-driver`, `start-generic-agent` |
| `concepts.md:84` | brief "holds … the host rows" | reworded: "the names of its host rows (`$CHANTIER host <capability>` prints one)" |
| `griller-skill.md:29` | send `specified` "by the host's means" | `message-chief` |
| `topics/batch-pause.md:5` | "Where the heartbeat is yours (host row)" | `heartbeat` |
| `topics/batch-plan-mode-p3.md:4` | Foreman under Remote Control "(host rows)" | `start-foreman` |
| `topics/board-lines.md:5` | "stops it by the host row" | `run-board` |
| `topics/board-p1.md:4` | "in the background by the host row" | `run-board` |
| `topics/board-restart.md:4` | "in the background by the host row" | `run-board` |
| `topics/compacting-p1.md:3` | "if its host row names one" | `compact` |
| `topics/config-p3.md:4` | host row "Skills and tools of a session" | `session-skills-tools` |
| `topics/direct-mode-back.md:4` | "by the host's stop" | `stop-driver` |
| `topics/direct-mode-epoch-p1.md:3` | "Arm the same heartbeat as the host row says" | `heartbeat` |
| `topics/direct-mode-switch-p1.md:4` | transcript id "(the host row says where it is)" | `own-session-id` |
| `topics/direct-mode-switch-p2.md:5` | "where the host row names the means" (stop a Foreman) | `stop-session` |
| `topics/foreman-start-more.md:3` | "arm the heartbeat if the host row says you do" | `heartbeat` |
| `topics/foreman-start-more.md:4` | "The host row says how the prompt reaches an idle or closed session" | `start-foreman` |
| `topics/foreman-start-p2.md:3` | "Start the session as the host row says" | `start-foreman` |
| `topics/griller-worktree.md:4` | send files "by the host's means" | `message-chief` |
| `topics/handback-refused.md:3` | to the steering session "by the host's means" | `driver-hand-back`, in direct mode `driver-messages-steering-direct` |
| `topics/handover.md:4` | "stop it by the host row" | `stop-driver` |
| `topics/lost-driver.md:5` | "stop it by the host's means" (an ended Driver that wakes) | `stop-woken-driver` |
| `topics/steering-messages.md:10` | "use the host's row" | `driver-hand-back`, in direct mode `driver-messages-steering-direct` |
| `topics/sync-offer-p2.md:8` | "by the host's stop of their background shell" | `stop-own-background-task` |
| `topics/titles.md:3` | "rename the session by the host's means" | `set-own-title` |
| `topics/wakes-p1.md:4` | "the host row who arms it" | `heartbeat` |
| `topics/wakes-p2.md:3` | "cancel the armed wake as the host row says" | `heartbeat` |
| `topics/watcher-pull.md:3` | "(the host row, or the user's no)" | `run-watcher` |
| `topics/watcher.md:6` | "Start it by the host row" | `run-watcher` |

Lines already naming the command (`cr-driver.md:13,27,29`, `stack-driver.md:12,13,29`,
`release-driver.md:9,27`, `qa-driver.md:19`, `sync-checkout.md:7`, `topics/ci.md:3`,
`topics/session-shell-p1.md:6`, `topics/steering-messages.md:3`, `concepts.md:95`) stay as they
are. The Driver searches its base again (`host row`, `host rows`, `host's means`, `host's row`,
`host's stop`, `by the host`) and treats a line the table misses by the same rule.

Pointers to a row that does not exist on either host (no capability to name) are not invented
and not reworded: `chief-of-staff.md:37` (host row `ending`), `topics/allow-rules.md:3,4`
("Capabilities and their commands", "from the host row"), `topics/allow-rules-more-p2.md:3`
("Allow rules to add"), `topics/trials-p1.md:3` ("Trial before the go"), `topics/trials-p2.md:3`
("Auto mode"), and `topics/foreman-start-p2.md:3`'s "For you" block. The PR's Known gaps lists the
ones still present at its base (question 2).

### 5. The worker cards: the one protective row at its moment

Ten worker roles' briefs carry only `end-turn-background` (proved: the host asks a subagent for
its hand-back at once and a background shell's end wakes it). With names only, the row's text is
no longer read at boot, so each of those cards names it at its end: `coder.md`,
`conflict-resolver.md`, `debugger.md`, `inspector.md`, `investigator.md`, `verifier.md`,
`spec-writer.md`, `spec-critic.md`, `retro-critic.md`, `demo-explorer.md` get, on their reply
line, one clause: "with nothing running in the background (`$CHANTIER host end-turn-background`)".
`griller-skill.md` (the Griller's rows: `start-spec-critic`, `end-turn-background`, `compact`,
`reload-after-compact`) names `start-spec-critic` where it starts the Spec critic, and `compact`
and `reload-after-compact` where it compacts, if it has such a line; a moment the card does not
have gets no new line. The Drivers' cards already name their rows (above); their
`start-driver`, `start-generic-agent`, `compact` and `write-guard` moments are in the
`cr-workers`, `compacting-*` and write-guard pages, which the section 4 rule covers. No agent file
(`agents/`, `com.github.copilot/agents/`) changes.

### 6. Tests

- `skills/chantier/scripts/cli/tests/test_brief.py`:
  - `_check_file`: reads the one line under `=== host rows: <host>` and checks its capability set
    against the role's rows exactly as today (`rows_of` for `rows: null`, else `set(data.rows)`;
    `["none"]` for `board-griller`); the `CAPABILITY` regex over the rows' text goes.
  - `_check_driver_facts`: the new `Steering:` line.
  - New, parametrized on both hosts: each capability a role's brief names is accepted by
    `chantier host <capability>` (exit 0, its first row line starting `<capability>: `).
- `skills/chantier/scripts/cli/tests/test_brief_bytes.py`: every figure lowered to the new measure
  on the claude host, rounded up to the next 100, as the file does today; `chief-of-staff` and
  `foreman` each at most 9,000 (the plan's estimate: about 8 KB and 6.5 KB). The docstring names
  this CR's cut.
- `skills/chantier/scripts/cli/tests/test_host_rows.py`: not edited; it passes as is.
- New guard (in `test_brief.py` or `test_host_rows.py`), reading the shipped files at the head
  under test: every `` `$CHANTIER host <x>` `` in `skills/chantier/references/**/*.md` (but
  `hosts/`) and in the CLI's source strings names a capability present on both hosts; and no line
  there says "the host rows below", "as the host row says", "by the host row", "the host row
  says", "(host row)", "(host rows)" or "by the host's means" without a `$CHANTIER host` on the
  same line. Few lines, one parametrized test.
- `scenario/run_scenario.py` and `evals/kit/dry_run.py` find the sections by `=== host rows: `,
  which stays; their wording "the host rows" stays true (the section still names them). Neither
  is edited unless its check breaks.

### 7. Docs

`scenario/README.md:160` and any doc that says the brief "holds the host rows" say it names them.
AGENTS.md's `brief` paragraph says "(its card, the floor, its unit's facts, its host rows)":
it becomes "its host rows' names". No other AGENTS.md change: no new command, no new write.

## Decisions (02-answers.md)

1. « ouvre un batch et lance ces 7 CR » (2026-11-27), read as "grilled enough" for the seven
   cleanup CRs, scope the plan and card-cleanup-Q1 to Q5: this CR is plan step 3, item 4, and only
   that. card-cleanup-Q1 (each protective rule put in its new place first) is honoured by
   sections 4 and 5: no protective row leaves a moment without the command that prints it.
2. « fait un batch stack … » (2026-11-27): the batch is a stack; this CR is one PR of it.
   Section 4's rule works at whatever base the stack gives it (question 3).
3. card-cleanup-Q5 (2026-11-27), « A. Étapes 1 à 3 »: steps 1 to 3 now, with a new version, in
   small CRs; steps 4 to 7 wait. The version bump is not this CR's; no step-4 work (`brief` for
   the remaining roles, `next` lines) is done here. The other project whose batch is open reads
   the cards live: the cards change only by added `$CHANTIER host <cap>` pointers, which a live
   reader with the current CLI can run today, since `host` is unchanged.

## Out of scope

- Rewriting the host rows, their names or marks, or adding a row (the dead pointers of section 4
  included).
- Rewriting the cards or help pages beyond the added pointers and `concepts.md:84`.
- Which rows a role gets (`roles.yaml`'s `rows:`), the brief's other sections, the short prompt.
- `help --for` and the grouped `--help` (plan step 3, item 5: CR `help-lists-role-commands`).
- The version bump (Chief of Staff's, after step 3).

## Evidence

- `chantier brief chief-of-staff` and `chantier brief foreman` (claude host) each under 9 KB,
  shown by `test_brief_bytes.py`'s printed `brief-bytes role=… bytes=…` lines and its lowered
  figures; the before and after figures in the PR body.
- `chantier host <capability>` prints what it printed: `host.py`, `host_rows.py` and
  `references/hosts/*.json` absent from the diff, `test_host_rows.py` green unedited, and the new
  test showing every name a brief lists is accepted by `host`.
- The guard test of section 6 green: no bare host-row pointer left, every named capability real.
- The PR body lists, for each line of section 4's table present at the base, the capability it
  now names, and the dead pointers left as Known gaps.
- `just check` passes; `just eval-dry-run` passes (a change under the CLI's `src/`); the long gate
  `scenario` passes (a CLI and cards change).

## Questions for the Chief of Staff

1. Workers. The request says every role's brief prints names only; the plan's targets say
   "workers as today". This spec cuts the workers' one row too and adds the
   `$CHANTIER host end-turn-background` clause to ten worker cards (section 5). Keep that, or
   leave the workers' briefs printing their one row whole (no worker card touched)?
2. Dead pointers. Six lines point to a host row that exists on neither host (`ending`,
   "Capabilities and their commands", "Allow rules to add", "Trial before the go", "Auto mode",
   the "For you" block). This spec leaves them and lists them as Known gaps. Should this CR
   instead name the nearest existing row (for `ending`: `watcher-session-end` and
   `board-session-end`?), or leave them to the step-1 deletions and step 4?
3. Stack order. This CR has no `depends.json`. Its pointers touch `-pN` pages that
   `cards-one-page-per-theme` joins and pages that `cards-delete-pages-chief` and
   `cards-delete-pages-crew` delete. Placing it after `cards-one-page-per-theme` would spare a
   conflict on every joined page; should the Chief of Staff add
   `{"after": ["cards-one-page-per-theme"]}`?
