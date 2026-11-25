# Host capabilities as data, `chantier host`, trial history to proofs

Child 8 of 28 of the program `simplify-cards-and-prompts` (study-fable-v2 child 3, first part).
One PR in batch-31's stack. Its base is child 7's branch (`sc07-help-topics`). Child 9
(`sc09-agents-md-role-rules`) is built on this branch.

Code read: `origin/main` at `8a960d34`. Short forms:
- `src/` means `skills/chantier/scripts/cli/src/chantier/`;
- `tests/` means `skills/chantier/scripts/cli/tests/`;
- `references/` means `skills/chantier/references/`.

## Goal

The owner's answer simplify-cards-Q13 (program answer 16): when a role uses a host function, the
CLI says in one sentence that it was never tried for real here. The history of the trials (dates,
batches, models) leaves the cards and goes to a proof file that nobody loads.

This child lays the ground for that. It turns each host card's capabilities into data, one row per
capability, with a one-word mark. It adds a command that prints a capability's row and adds the
sentence when the row is not proved. It copies every trial story into two proof files. It removes
nothing: the host cards keep their text until the swap (child 24). Child 10 then puts the rows a
role uses into that role's brief, and child 23 writes what is left of the host cards as topics.

## What changes

### 1. Two data files: `references/hosts/claude-code.json` and `references/hosts/copilot.json`

The files are new. They sit beside the two host cards, which stay unchanged. They are plain JSON,
UTF-8, LF, and read with the standard `json` module. Shape:

```json
{
  "host": "claude",
  "rows": [
    {
      "capability": "start-driver",
      "name": "Start a Driver or a worker",
      "roles": ["foreman", "chief-of-staff", "cr-driver", "stack-driver", "qa-driver", "release-driver"],
      "means": [
        "`Agent` with `subagent_type: chantier:<role>`; `run_in_background: true` for a Driver.",
        "The `model` parameter only when `$CHANTIER` printed a start value (an alias), as printed; no effort."
      ],
      "mark": "proved"
    }
  ]
}
```

- `host`: `claude` in `claude-code.json` and `copilot` in `copilot.json`. These are the values of
  `HOSTS` in `src/plugin_files.py`.
- `capability`: a kebab-case id, unique in the file. Both files hold the same set of ids, in the
  same order (see "The row set" below).
- `name`: the capability in a few words, taken from the card's "Generic" column or section title.
- `roles`: the roles that act on the capability, at least one. Each name is one of
  `plugin_roles(host)` (the 15 agent files) or `chief-of-staff`, `foreman` or `griller`. The roles
  come from the card itself: the brackets of the "Generic" column ("(Chief of Staff)", "(Foreman,
  Chief of Staff)"), else the roles whose cards use that row. This child's command does not read
  `roles`. Child 10 reads it to choose the rows a role's brief carries ("the host rows the role
  uses"). It is put here so that the data child holds all the data.
- `means`: two to four lines, each at most 160 characters. They say how this host does the thing,
  for this host only. They hold no date, no batch name, no CR id, no PR number, no machine name,
  no trial and no mark word (`proved`, `unproved`, `documented`, `untested`). The means are the
  card's means, shortened. What does not fit (the rules around a tool, its edge cases) stays in
  the card, and child 23 turns it into a host topic.
- `mark`: one word, `proved` or `untested`.

**The mark rule** (the program's "Must not"). A row is `proved` only when the card marks every
part of the row's means proved ("proved", "proved, same", or "**proved**" with a trial), for the
shipped default model where the means depend on a model. Any part marked unproved, documented,
measured once, "not recorded", "exercised", or left unmarked makes the row `untested`. Any doubt
makes it `untested`. Copilot's card says that nothing on it was re-tried and that every line is
unproved unless it says otherwise (its "Startup core"). The program says Copilot's host rows say
"untested" (its "Out of scope" and "Evidence"). So every row of `copilot.json` is `untested`.

**Splitting a card row.** A card row that gives distinct marks to distinct paths becomes one row
per path, each with its own mark. This is done only along the card's own marks, never to make a
row proved. The table below has the two splits made here (`driver-hand-back` and
`driver-messages-steering-direct`; `start-driver` and `model-at-start`).

**A capability one host lacks.** Its row in that host's file still exists. Its means say so in two
lines: what the host has instead, or "not recorded on this host", and what a role does then, as the
card says. For example, `write-guard` on Copilot says that Copilot has no hook and that the
`writes:` line is inert there. Its mark is `untested`.

### 2. The row set

These are the rows expected. The Claude Code source is a row of `hosts/claude-code.md#Tools`
unless another section is named. The Claude Code mark follows the rule above, with the card's
words as the reason. The PR lists every `proved` row with the card words it rests on (see
"Acceptance evidence"). A Driver who finds a row the table missed, or a mark the card contradicts,
adds or corrects the row and names the change in the PR. Every Copilot row is `untested`.

| capability | Claude Code source | Claude Code mark, and why | Copilot source |
| --- | --- | --- | --- |
| `start-foreman` | Start the Foreman's session | untested: "with this model: **unproved**" | Tools: Start the Foreman's session |
| `own-session-id` | Own session id and title | proved: "proved, same" | Own session id |
| `set-own-title` | Set a session's own title | untested: "the Foreman's case stays unproved" | Set the Foreman's own title; Set a session's own title |
| `skills` | The skills | untested: documented; the argument handling is unproved | The skills |
| `load-skill` | Load another skill (the router) | untested | not recorded |
| `list-sessions` | List the sessions and their state | untested | List the sessions |
| `message-session` | Message another session of the user | untested: "between two sessions of the user, unproved" | Message another session |
| `session-link` | A session's link (for the seat) | untested | not recorded |
| `start-driver` | Start a Driver or a worker (the agent, with no model passed, as the shipped defaults do) | proved: "the agent: proved, same" | Start a Driver or a worker |
| `model-at-start` | Models at an agent's start (and the model part of Start a Driver) | untested: only the `haiku` alias was proved; "the other two aliases ... unproved one by one" | Models at an agent's start |
| `start-generic-agent` | not on this host: a configured model goes through the `model` parameter (`model-at-start`) | untested | Start a generic agent |
| `model-ran-on` | not recorded | untested | The model a role ran on |
| `start-spec-writer` | Start the Spec-writer | untested | Start the Spec-writer |
| `start-spec-critic` | Start the Spec critic | untested | Start the Spec critic |
| `start-retro-critic` | Start the Retro critic | untested | Start the Retro critic |
| `message-driver` | Message a Driver | proved: "proved, same" | Message a Driver |
| `message-chief` | Message the Chief of Staff | proved: "proved, same" | Message the Chief of Staff |
| `driver-hand-back` | A Driver messages its steering session: the final report to a Foreman's Desktop session | proved: "Foreman mode: the final report as the hand-back's route is proved (batch-16, batch-18)" | A Driver's hand-back to its steering session |
| `driver-messages-steering-direct` | the same row: direct mode, from Claude Desktop or a terminal | untested: "Direct mode from Claude Desktop: unproved", "Direct mode from a terminal: unproved" | the same row: "in direct mode ... unproved" |
| `stop-driver` | Stop a Driver | proved: "proved, same" | Stop a Driver |
| `stop-woken-driver` | Stop an ended Driver that wakes again | untested: whether it ends the Driver's tasks is unproved | not recorded |
| `driver-start-folder` | A CR Driver's start folder | untested | A Driver's start folder |
| `stop-own-background-task` | Stop a background task of one's own | untested | Stop a background task of one's own |
| `name-env-holders` | Name the holders of the checkout's environment | untested: Windows "exercised", macOS and Linux "untested" | Name the holders of the checkout's environment |
| `stop-session` | Stop another session | untested | not recorded |
| `agent-ids` | Agent ids of the project | proved: "proved, same" | Agent ids of the project |
| `models` | Models | untested: "except the CR driver, the stack and release drivers and the Foreman: unproved" | Models |
| `session-skills-tools` | Skills and tools of a session | untested | Skills and tools of a session |
| `preflight-p2` | Preflight P2 | proved: "proved, same" | Preflight P2 |
| `ask-questions` | Ask the user a series of questions | untested: the figures are the user's statements, unproved | Ask the user a series of questions |
| `run-board` | Run the board | untested | Run the board |
| `board-griller` | The board's Griller | untested | The board's Griller |
| `workspace-trust` | Trust of a workspace inside a trusted folder | untested | not recorded |
| `move-session` | Move a started session to another folder | proved: "proved 2026-11-20, Battlestation (the move and the denial)"; the means hold only the move and the denial | not recorded |
| `prompt-cache-ttl` | Prompt cache TTL | untested: "measured once ... unproved in general" | Prompt cache TTL |
| `steering-wake-bound` | Steering wake bound (60 minutes) | untested: "unproved: 55 minutes, the shipped default" | `/every` in whole minutes |
| `heartbeat` | section "Heartbeat" (the loop, `ScheduleWakeup` with the wake `playbook` prints, the stop); the means name no wake value, which is `steering-wake-bound`'s | proved: the section ends "Proved: same." | section "Heartbeat" |
| `run-watcher` | Run the watcher | untested | Run the watcher |
| `watcher-session-end` | The watcher when the session ends | untested | not recorded |
| `board-session-end` | The board when the session ends | untested | The board when the session ends |
| `message-limit` | the paragraph "Limit on messages" under the table | untested: "the figure comes from the earlier card, with no dated trial" | not recorded |
| `end-turn-background` | "Surfaces and options": End a subagent's turn with nothing running in the background | proved: "proved, batch-16" | not recorded |
| `subagent-stops` | "Surfaces and options": A background subagent stops | proved: "proved, batch-18" | not recorded |
| `subagent-stopped-outside` | "Surfaces and options": A background subagent is stopped from outside | untested: the user's stop in the app is unproved | section "Sessions": "A Driver stopped from outside on Copilot is unproved" |
| `resume-subagent` | "Surfaces and options": Resume a stopped subagent | proved: "proved, batch-15", the refusal "proved, batch-22" | not recorded |
| `compact` | section "Compacting" | untested: documented and measured, the cap unproved | section "Compacting" |
| `reload-after-compact` | section "Reload after a compaction" | untested: "**Unproved** until seen in a session" | section "Reload after a compaction" |
| `write-guard` | section "The write guard" | untested: the passes are "**Unproved** until that eval reports"; the refusals are proved only by `hooks/register.test.tsx` | none: Copilot has no hook (`claude-code.md`, "The write guard", last line) |
| `griller-in-worktree` | "Sessions of one repository": a Griller in a worktree | untested | A Griller in a worktree |
| `surface-session-writes` | "Classes of session": the planning surface row, writing in the project's clone and worktrees | untested | A session in a planning surface writing in the project's clone |

That is 50 rows, 13 of them `proved` on Claude Code and none on Copilot. These sections give no
row, because no role calls a host tool from them: "Auto-fix events", "The Foreman's turn-end
notice", "A Driver's silence", "Configuration", "Classes of session" (apart from the row above),
"Surfaces and options" (apart from the four rows above), "A Foreman in a worktree asks", "Reusing
the last Foreman" and "The 'For you' block". Their stories still go to the proof file
(section 4). Child 23 decides what of them becomes a host topic.

### 3. The command `chantier host [<capability>]`

- **Declared** in a new `src/declare/host.py`, with `register(sub)` calling
  `add_command(sub, "host", "chantier.commands.host:host", "<help>", BATCH)`. Add it to the
  imports and to `_MODULES` in `src/cli.py`, and add `"host"` to `FULL_OUTPUT`: a row is useless
  cut short. Help text: "how this host does a capability, from the plugin's host rows; with no
  capability, every row". One optional positional argument, `capability`.
- **The handler**, in a new `src/commands/host.py`, `host(args) -> list[str]`.
- **The data module**, a new `src/host_rows.py`. Child 10 imports it.
  - `UNTESTED = "This path was never tried for real here."`: the one sentence, the same
    everywhere.
  - `FILES = {"claude": "claude-code.json", "copilot": "copilot.json"}`.
  - `load_rows(host: str) -> list[HostRow]` reads `skill_dir() / "references" / "hosts" /
    FILES[host]` (`skill_dir` from `src/plugin_files.py`). `HostRow` is a frozen dataclass:
    `capability`, `name`, `roles`, `means`, `mark`. A missing or unreadable file, or a row whose
    mark is neither word, raises `ChantierError(..., EXIT_PRECONDITION)` naming the file and the
    row.
  - `row_lines(row: HostRow) -> list[str]` gives the first line
    `<capability>: <name> (<mark>)`, then each means line indented by two spaces, then, for a row
    not marked `proved`, the line `  This path was never tried for real here.`
- **Which host.**
  1. When a batch resolves, that batch's record decides (`BatchRecord.host`). The batch is
     resolved with `resolve_batch(repo, args.batch, paused=True)` from `src/core/batch.py`, read
     with `read_batch`.
  2. With no batch, the session's host decides, as the CLI resolves it today: `detect_host()`
     from `src/plugin_files.py` (`CHANTIER_HOST`, then the host's own environment). A session
     whose host cannot be told gets that function's own refusal, exit 2.

  "No batch" means: no planning folder found (`Repo.find()` raises), or no `--batch`, no
  `CHANTIER_BATCH` and no running or paused batch to take. An explicit `--batch` or
  `CHANTIER_BATCH` that does not resolve is refused, as for every command. Several running
  batches with no `--batch` are refused as `resolve_batch` refuses them today: the command does
  not guess.
- **Output.** The first line names the host and where it came from: `host: claude (batch-31)` or
  `host: copilot (this session)`. Then:
  - with a capability: that row's `row_lines`;
  - with no capability: every row's `row_lines`, in file order, with one blank line between rows.

  Exit 0.
- **Unknown capability.** Exit 2 (`EXIT_USAGE`) with one line:
  ``unknown capability `<given>` on <host>: one of <id>, <id>, …``, giving every id in file order.
- **Nothing else.** The command reads only the plugin's files and the batch record. It writes
  nothing and reads no network. Through a profile (`chantier login`), it runs on the server like
  every other command. `cli.run` passes the client's host variables, so `detect_host` there sees
  the client's host. Nothing is added for that.

### 4. Two proof files: `docs/proofs/claude-code.md` and `docs/proofs/copilot.md`

Both files are new, in a new folder `docs/proofs/`.

- **Top.** A `#` title ("Claude Code: trial history", "Copilot: trial history") and one short
  paragraph. It says that no role loads the file; that it holds the trials, dates, batches, models
  and marks behind `references/hosts/<file>.json`; and that a row's mark changes only with a trial
  recorded here.
- **One `## <capability>` heading per row**, the heading text being the id alone, in the JSON's
  order. Under it:
  - a first line `Mark: proved` or `Mark: untested`, followed by the card's words that justify it;
  - then every trial, date, batch, session or agent id, model, account and proved, unproved,
    documented, measured or "Trial: …" sentence that the host card gives for that capability,
    copied in substance. Copy each source quote with its card section (and its row, for a Tools
    row).

  A capability with no story says so in one line ("No trial recorded on this host; the card's
  Startup core marks every line unproved." for most Copilot rows).
- **Then one `## Other: <section title>` heading per card section that gives no row** (the list
  at the end of section 2), holding that section's stories in the same way. On Copilot: "Known
  host issues" (the four upstream issues) and "Configuration".
- **Links.** A relative link copied from a card is rewritten so that it resolves from
  `docs/proofs/`, or turned into a code span. Planning-surface paths stay code spans.
- **Unchanged.** The host cards keep every word (program: "The host cards keep their text until
  the swap"). The proof files copy; they do not move.
- **One pointer line in `docs/hosts.md`.** It names the two proof files and `chantier host
  <capability>`. This changes a doc, not a card.

### 5. AGENTS.md

AGENTS.md gains one paragraph among the CLI's named exceptions. Put it after the `access`
paragraph, in the same form:

> `host`: read-only, it prints how the host does a capability: the row of the plugin's
> `references/hosts/<host>.json` (the batch's recorded host, else the session's), whose means end,
> on a row not marked proved, with one sentence saying the path was never tried for real here; it
> writes nothing and reads no network; built on the user's answer simplify-cards-Q13, with no
> measured cost.

No other AGENTS.md rule changes. Child 9 rewrites the role sentences.

### 6. The scenario

A new command adds a step and a coverage bullet (the program's rules).

- **`scenario/run_scenario.py`.** In the unit `parallel` (function `scenario`), right after the
  `rules` check in section 1, add a check: `host` with no batch prints `host: claude (this
  session)`. After the batch opens (section 2), add three checks:
  - `host start-driver` prints `host: claude (<batch>)` and the row with no untested sentence;
  - `host write-guard` ends with `This path was never tried for real here.`;
  - `host nope` exits 2, and its line names `start-driver`.
- **`scenario/README.md`, `## Coverage`.** Add one bullet: "`host` prints a capability's row for
  the batch's recorded host, else the session's; an untested row ends with the one sentence; an
  unknown capability lists the known ones", ending with `(unit: parallel)` and the test names of
  section 7. `tests/test_scenario_coverage.py` then checks the bullet.

### 7. Tests: a new `tests/test_host_rows.py`

The tests read the shipped files from the repository at the head under test: `PLUGIN_ROOT` and
`SKILL` from `tests/conftest.py`, never a copy. They call the CLI in process through the
`chantier` fixture. Keep them few and parametrized over the two hosts.

1. `test_every_row_has_means_and_a_one_word_mark[claude|copilot]`. Each file parses. `host`
   matches its file. The ids are unique and kebab-case. Each row has 2 to 4 means lines of at
   most 160 characters. Each mark is `proved` or `untested`. Each role name is a known role
   (`plugin_roles(host)` plus `chief-of-staff`, `foreman`, `griller`). The two files hold the
   same ids in the same order.
2. `test_every_copilot_row_is_untested`.
3. `test_means_carry_no_history[claude|copilot]`. No means line matches a date
   (`\d{4}-\d{2}-\d{2}`), `batch-\d+`, `CR-\d+`, `PR \d+`, `#\d+`, or the words `proved`,
   `unproved`, `documented`, `untested`, `trial`. This anticipates child 26's M3 on the new home
   of host means.
4. `test_every_untested_row_prints_the_sentence[claude|copilot]`. For every row: `host <id>`
   (host set with `batch_helpers.host(monkeypatch, name)`, no batch) prints the row. The output
   ends with `UNTESTED` exactly when the mark is not `proved`, and the sentence appears in no
   proved row's output.
5. `test_every_capability_is_a_heading_in_the_proof_file[claude|copilot]`. Every id has a
   `## <id>` line in `docs/proofs/<file>.md`, and the headings follow the JSON's order.
6. `test_the_proof_file_keeps_every_date_and_batch_of_the_card[claude|copilot]`. Every date
   (`\d{4}-\d{2}-\d{2}`) and every `batch-\d+` found in `references/hosts/<host card>.md`, as it
   ships, is found in the matching proof file. This is the mechanical check that the history was
   copied. Once child 24 empties the cards of dates, it holds trivially.
7. `test_an_unknown_capability_lists_the_known_ones`. `host nope` exits 2. Its one line names
   `nope`, the host and every id.
8. `test_the_batch_record_decides_the_host`. Open a batch as Copilot: `batch_helpers.host(
   monkeypatch, "copilot")`, `prepared`, then `open` as `open_batch` runs it. Then set the session
   to Claude. `host start-driver` prints `host: copilot (<batch>)` and Copilot's means with the
   sentence. With the batch's CRs ended and no batch to resolve, `host start-driver` prints
   `host: claude (this session)` and Claude's proved row. If ending the batch is costly in a
   test, use a second, batch-less repository fixture instead.
9. `test_no_host_and_no_batch_is_refused`. With `CHANTIER_HOST`, `CLAUDE_CODE_ENTRYPOINT` and
   the Copilot variables cleared and no batch, `host` exits 2 with `detect_host`'s refusal.

Test 1's role check guards child 10's input. Tests 4 to 6 are the program's four checks; tests 1,
2, 3, 8 and 9 guard the mark rule and the host resolution.

## Decisions carried

| Source | Decision | Here |
| --- | --- | --- |
| Program answer 16 (simplify-cards-Q13) | When a host function is used, the CLI says in one sentence that it was never tried for real here. The trial history leaves the cards for a proof file nobody loads | sections 3 (`UNTESTED`) and 4. The cards themselves lose the history at child 24 |
| Program, child 8: rows | One row per capability, from the "Tools" tables and the sections a role acts on (heartbeat, a Driver messaging its steering session, starting a child, ending, compacting, reloading, the write guard): the capability, two to four lines of means for this host only, and a one-word mark | sections 1 and 2 |
| Program, child 8: command | `host [<capability>]` reads the host from the batch's record, else the session's host as resolved today. It prints the matching rows. A row not `proved` ends with the same sentence | section 3 |
| Program, child 8: proofs | Every trial, date, batch, model and proved or unproved story of both host cards is copied, grouped by capability | section 4, test 6 |
| Program, child 8: must not | The host cards are not edited. No mark the cards do not hold: `proved` only where the card says proved for the shipped default model; any doubt is `untested` | the mark rule; "Out of scope" |
| Program: Copilot | Copilot roles boot through `brief`, and its host rows say "untested" | every Copilot row `untested`, test 2 |
| Program: rules for every child | A new command gets a scenario step and a coverage bullet, an AGENTS.md line with its source, and the PR states the seconds its tests add. No card text changes before child 19. No version is edited by hand | sections 5 to 7; "Acceptance evidence" |
| Program: the floor's neighbours | "An untested host path is said to be untested: the sentence in the host rows (child 8)" | `UNTESTED`, one constant, which child 10 reuses |
| Program, child 10 | The brief carries "the host rows the role uses (child 8)" | the `roles` field, and `load_rows` and `row_lines` in `src/host_rows.py` |

Judgments made here within those decisions. The Chief of Staff can see them; none needs the
owner:
- `heartbeat` is `proved`, because the card's section says "Proved: same". The unproved 55-minute
  default goes to its own row, `steering-wake-bound`, which is `untested`.
- `message-chief` is `proved` ("proved, same"). `message-session`, the general case between two
  of the user's sessions, is `untested`, as the card marks it.
- Two card rows are split along their own marks: `driver-hand-back` / `driver-messages-steering-
  direct`, and `start-driver` / `model-at-start`.

## Out of scope

- Any edit to `references/hosts/claude-code.md`, `references/hosts/copilot.md`, any other card,
  `SKILL.md`, a wrapper, `startup-manifest.json` or the four core files. Those are children 19 to
  24.
- Putting rows in a brief, or any role reading `host`. That is child 10, and child 24 for the old
  outputs.
- The host topics: what stays of the host cards apart from the rows and the history. That is
  child 23.
- Removing the history from the cards. That is child 24, when the cards are replaced.
- A `--host` flag or a `--for <role>` filter on `host`. Neither is asked for. `CHANTIER_HOST`
  already picks the host when no batch decides.
- A new trial of any host behaviour, or a changed mark beyond what the cards hold.
- A mark word other than `proved` and `untested` (no `documented`). The program fixes two words.
- Project-configured rows: the rows are the plugin's. `chantier.yaml` has no key for them.

## Host and default matrix

`host` depends on the host. It does not depend on a shipped default versus a configured value:
the rows are the plugin's own data, and no `chantier.yaml` key touches them. One line per cell:

- **Claude Code, batch recorded `claude`.** `host start-driver` prints `host: claude (<batch>)`
  and the proved row, with no sentence. Proved by the scenario step (a real `open`) and by test 4.
- **Claude Code, no batch, host from the environment** (`CHANTIER_HOST=claude`, or
  `CLAUDE_CODE_ENTRYPOINT`). `host` prints `host: claude (this session)`. Proved by the scenario
  step in section 1 and by test 8.
- **Copilot, batch recorded `copilot`** (opened with `CHANTIER_HOST=copilot`) and session on
  Claude. Copilot's row, with the sentence: the record wins. Proved by test 8.
- **Copilot, no batch, host from the environment.** Copilot's rows, each with the sentence.
  Proved by tests 2 and 4.
- **No host told and no batch.** `detect_host`'s refusal, exit 2. Proved by test 9.

No Copilot session is run: none was ever seen here (program, "Out of scope").

## Acceptance evidence

- `just check` green at the pushed head. `just eval-dry-run` green there too, since the change is
  under `src/`.
- `just scenario (ubuntu-latest)` green at the PR's head: the long gate is owed, since the CLI
  changes. The local Windows run (`chantier gate <cr> scenario`) is owed only while this CR is on
  top of the stack (the program's long-gate rule).
- The nine tests of section 7 pass. Each guarded check reads the shipped files at the head under
  test: the two JSON files, the two proof files and the two host cards. No prepared text is used.
  The only prepared input is the unknown capability `nope`, a refusal case, paired with the
  shipped id list it must print.
- The PR's Deliverables hold:
  - the output of `chantier host` with no argument on each host (`CHANTIER_HOST=claude`, then
    `copilot`, no batch);
  - the list of the 13 proved Claude Code rows, each with the card words it rests on (the third
    column of section 2's table), so the reviewer checks no mark was claimed beyond the card;
  - the seconds the new tests add to `just test`: `just test` before and after, on the same
    machine. Expected: under 2 seconds (nine tests, about 110 in-process CLI calls, no batch but
    in test 8).
- `git diff --stat` against the base shows no file under `references/` changed apart from the two
  new JSON files.

## Its place in the chain

- **Depends on:** child 7 (`sc07-help-topics`), as its base branch. Nothing of child 7's code is
  used. If child 7 added a `help` line to AGENTS.md, this child's paragraph follows it.
- **Depended on by:**
  - child 9, built on this branch;
  - child 10, which imports `load_rows`, `row_lines` and `UNTESTED` from `src/host_rows.py` and
    filters rows by `roles` for a role's brief;
  - child 23, which writes the host topics from what the cards keep beyond these rows and the
    proof files;
  - child 24, which removes the old host cards' history and links the proof files;
  - child 26, whose M3 lint the means already respect (test 3);
  - child 28, whose Copilot cell reads these rows ("untested").

## Risk

- The long gate is owed (CLI). `just mod` is not owed: no hook change.
- Shortening each card row to four lines of means is a judgment on what is the means and what is
  the rule. A rule left out of the means stays in the card until child 23 places it, and child 25's
  review checks it. Nothing is lost here, since the cards keep their text.
- A wrong `proved` would make a role trust an untried path. The mark rule, the PR's list of proved
  rows with their card words, and test 2 bound that.
- The `roles` values are child 10's input. A role missing from a row means its brief lacks that
  row. Child 10's tests (its brief per role) are where that shows.

## Open questions

None. The program's specification and its answers 16 to 22 settle the scope. The judgments above
stay within the mark rule the program fixed.
