# Change Specification: timing and retry settings in the configuration, per host and model family

## Goal

The user wants the loops' timing in the configuration, next to the models: how often the steering
session (the Foreman, or the Chief of Staff in direct mode) wakes, the prompt cache's TTL that wake
is chosen against, and how many times a CI job failed on the infrastructure is re-run. Each has a
shipped default and can be set in `chantier.yaml`, per host and, inside a host, per model family
(Copilot) or per context (Claude Code: subagent or session), with a general value per host that
each column may override. The board's Configuration page shows them all, read-only, on a Timing
tab beside Models, a value set in `chantier.yaml` standing out from a shipped default, and the
board's "late" heartbeat mark follows the batch's steering wake.

The Driver wake is not in this CR: it is split off as its own CR (timing-Q6).

Every other wait or maximum stays where it is (02-answers, timing-Q4): the rounds limit, the
3-hour CI limit, the "no CI" minute, the 30-minute idle stop of the heartbeat (its wording changes,
not its 30 minutes: Area 3), a remote command's one re-run, the Release driver's one re-run of a
procedure step, the board's 10-second forge read.

## Decisions carried from 02-answers.md

| Answer | Carried into |
| --- | --- |
| timing-Q1: in the next batch, with batch-22's retro points, cost-receipt and board-visual-refresh | Planning |
| timing-Q2: a card per host on a Timing tab beside Models, in board-visual-refresh's style; a value set in chantier.yaml stands out from a shipped default | Area 5 |
| timing-Q3: host x model family (on Claude Code: subagent or session), a general value each column may override | The settings, Areas 1 and 2 |
| timing-Q4: only the prompt cache TTL, the wakes and the CI retries' maximum | The settings, Out of scope |
| timing-Q5: each setting once per host card, one value column per family or context; the legend beside the tabs; reference `board-visual-refresh/prototypes/01-mockups/final-config.html` | Area 5, Evidence |
| timing-Q6: the Driver wake is its own CR; no `driver_wake` key here | The settings, Out of scope |
| timing-Q7: the Timing tab is read-only | Areas 4 and 5, Out of scope |
| timing-Q8: Copilot's `cache_ttl` default `5m`, marked unproved | Shipped defaults, Area 3 |
| timing-Q9: the Copilot steering wake reads the column of the family of the model the Chief of Staff started the Foreman with, else the general value | Columns, Area 3 |
| timing-Q10: the TTL is shown, plus a `playbook` warning when a wake is longer than its column's TTL | Area 2 |
| timing-Q11: the board's "late" mark follows the batch's steering wake | Area 4, Area 5 |
| timing-Q12: CI re-runs stay re-runs of a job failed on the infrastructure; the caption says so | Area 3, Area 5 |
| timing-Q13: the strongest layer first, then within a layer the column beats the general value | Area 1 (resolution) |
| timing-Q14: the idle stop is 30 minutes or more with no Driver, whatever the wake; the wake that sees it ends the heartbeat | Area 3 |
| timing-Q15: a wake over 60 minutes refused on Claude Code, a duration not in whole minutes refused on Copilot, each with a trial in the host reference | Durations, Area 1, Area 3 |
| timing-Q16: a setting a column never reads shows "not used" on the tab, and is refused under that column in chantier.yaml with its line | Columns, Area 1, Area 5 |

## The three settings

| Key | Meaning | Value | Who reads it |
| --- | --- | --- | --- |
| `steering_wake` | the interval of the steering session's heartbeat wake | a duration | the Foreman; the Chief of Staff in direct mode; on Copilot the Chief of Staff, which arms `/every` |
| `cache_ttl` | the prompt cache's time to live in that column: what the wake is chosen against | a duration | the user (shown); `playbook`'s warning |
| `ci_reruns` | the most re-runs of one CI job judged an infrastructure failure, at one head, before the Driver blocks | a whole number, 0 or more | every Driver that judges CI (CR, stack, QA, release) |

### Durations

A duration is written `<whole number><unit>`, the unit `s`, `m` or `h` (`90s`, `4m`, `1h`), and is
at least one minute. Only what is proved is accepted (timing-Q15):

- on Claude Code, a `steering_wake` over 60 minutes is refused (`hosts.claude.timing:
  "steering_wake" is at most 60 minutes on Claude Code: found "<value>"`); `cache_ttl` has no upper
  bound;
- on Copilot, every duration is in whole minutes (`/every` takes minutes): `90s` is refused
  (`hosts.copilot.timing: "<key>" is whole minutes on Copilot (<n>m or <n>h): found "<value>"`).

Any other wrong value is refused with the file and line, as the other keys are
(`hosts.claude.timing: "steering_wake" is a duration of 1 minute or more: <n>s, <n>m or <n>h, found
"<value>"`). The CLI prints a duration in minutes (`30 min`, `1 min 30 s` when not whole).

### Columns

- Claude Code (`hosts.claude.timing`): `subagent` and `session`. The steering session is a
  session: it reads the `session` column. A Driver is a subagent: it reads `subagent`.
- Copilot (`hosts.copilot.timing`): one column per model family, `claude` and `gpt`. A Driver reads
  the column of the family of the model it runs (the first word of the model's identifier:
  `claude-sonnet-5.5` is `claude`, `gpt-6.1-sol` is `gpt`); a model of another family, or one it
  cannot name, reads the host's general value. The steering wake: the Chief of Staff reads the
  column of the family of the model it started the Foreman with, else the general value (in direct
  mode no Foreman is started: the general value) (timing-Q9).
- The general value (the setting directly under `timing:`) applies to every column that does not
  set its own (resolution: Area 1).

What a column reads (timing-Q16); a setting in a "no" cell is refused under that column in
`chantier.yaml` and shown "not used" on the Timing tab:

| Host | Column | `steering_wake` | `cache_ttl` | `ci_reruns` |
| --- | --- | --- | --- | --- |
| claude | `session` | yes | yes | no (no session judges CI) |
| claude | `subagent` | no (no subagent steers) | yes | yes |
| copilot | `claude` | yes | yes | yes |
| copilot | `gpt` | yes | yes | yes |

The refusal: `<file>:<line>: hosts.claude.timing.subagent: "steering_wake" is not read by the
subagent column: set it under session, or as the general value`. A general value is accepted for
every setting (some column of the host reads each).

### The shape in chantier.yaml

```yaml
hosts:
  claude:
    timing:
      ci_reruns: 1            # general: every column that reads it
      session:
        steering_wake: 20m    # this column only
        cache_ttl: 1h
      subagent:
        cache_ttl: 5m
  copilot:
    timing:
      steering_wake: 4m
      gpt:
        ci_reruns: 2
```

A key under `timing:` is either one of the three settings or one of the host's columns; anything
else is refused (`host "claude": timing: unknown key "<key>": one of steering_wake, cache_ttl,
ci_reruns, subagent, session`). `driver_wake` is an unknown key like any other. A plain `default`,
`~` or `null` takes a value back to the weaker layers and, at the bottom, to the shipped default.

### Shipped defaults (today's behaviour, unchanged)

In `config/chantier.defaults.yml`:

| Host | Setting | General | Column overrides | Source |
| --- | --- | --- | --- | --- |
| claude | `steering_wake` | `30m` | | today's `ScheduleWakeup` 1800 s, `hosts/claude-code.md`, "Heartbeat" |
| claude | `cache_ttl` | `5m` | `session: 1h` | measured once, 2026-11-17, one account; unproved in general: the session transcript's usage showed `cache_creation.ephemeral_1h_input_tokens` only, a subagent's `ephemeral_5m_input_tokens` only; the row and its trial in `hosts/claude-code.md` (Area 3) |
| claude | `ci_reruns` | `1` | | today's "an infrastructure failure gets one re-run", `driver.md` |
| copilot | `steering_wake` | `4m` | | today's `/every 4m`, `hosts/copilot.md`, "Heartbeat" |
| copilot | `cache_ttl` | `5m` | | unproved (timing-Q8): the row and its trial in `hosts/copilot.md` (Area 3) |
| copilot | `ci_reruns` | `1` | | as Claude Code |

The defaults go through the same check as a user file, the "not used" refusals included: the
Claude Code `steering_wake` is a general value, which only the `session` column reads. The defaults
file's comment header names the timing block and that the values are what the cards did before this
CR. The test that keeps the defaults equal to the agent files reads the roles only; it is left as it
is.

## What changes

### Area 1: reading and checking (`playbook/config.py`, `playbook/layers.py`)

- `config._host`: a host's keys are `roles` and `timing` (the message becomes `one of roles,
  timing`). A new `_timing(host, node, kline, bad)` checks the block: each key a setting or a
  column of that host (`TIMING_COLUMNS = {"claude": ("subagent", "session"), "copilot": ("claude",
  "gpt")}` beside `HOST_FILES`), each column holding only settings it reads (`TIMING_READS`, the
  table above), each value of its kind (a duration within the host's bounds, a whole number 0 or
  more for `ci_reruns`), a reset accepted where its key is. Each refusal names the file and line.
  The shipped defaults go through the same check (`read_defaults`).
- `layers.py`: a new `load_timing(repo, roles_by_host, defaults)` returns, for each host and each
  column, every setting the column reads, its value and the label of the layer behind it
  (`defaults`, `surface`, `surface project`, `repository`), and, for a setting the column does not
  read, `None` (shown "not used"). Resolution (timing-Q13): the layers are searched from the
  strongest down to the defaults; the first layer that sets the column's own value or the host's
  general value gives the value, and within that layer the column's value beats the general one.
  So a user's general `cache_ttl: 10m` gives `10m` to the Claude Code `session` column, above the
  shipped `session: 1h`. Unlike `load`, it answers with the defaults alone when no user file is
  present: the timing always has a value. A problem in a user layer is returned as the other keys'
  problems are, and `playbook` and `open` refuse on it as they do now.

### Area 2: the record and the prints (`commands/opening.py`, `core/records.py`, `playbook/lines.py`, `commands/rules.py`, `commands/facts.py`)

- `open` records the resolved timing of the batch's host in a new `BatchRecord.timing` field, next
  to `playbook`, whatever user files exist: a running batch keeps the timing it opened with, like
  its team ("applies at the next batch"). `brief.md` gets one line, `- Timing: <the timing lines>`.
- A batch record with no `timing` (opened before this change) reads as the shipped defaults of the
  running plugin; nothing is migrated.
- `playbook/lines.py`: a new `timing_lines(timing, host)` prints one line per column of the host,
  each with the settings that column reads:

  ```text
  timing: Claude Code session: steering wake 30 min, cache TTL 60 min
  timing: Claude Code subagent: cache TTL 5 min, CI re-runs 1
  ```

  ```text
  timing: Copilot claude models: steering wake 4 min, cache TTL 5 min, CI re-runs 1
  timing: Copilot gpt models: steering wake 4 min, cache TTL 5 min, CI re-runs 1
  timing: Copilot other models: steering wake 4 min, cache TTL 5 min, CI re-runs 1
  ```

  (the last line: the general values, read by a model of no named family and by the steering wake
  when the Foreman's model is not known). Each value a user layer set is followed by its layer in
  brackets, as the role lines do (`steering wake 20 min [surface project]`); a value from the
  defaults has no label.
- The TTL warning (timing-Q10): after the lines, for each column whose `steering_wake` is longer
  than its `cache_ttl`, one line: `timing: Claude Code session: steering wake 90 min is above the
  cache TTL 60 min: each wake starts cold`. A warning, not a refusal; no value is derived from the
  TTL. With the shipped defaults no warning prints.
- Printed by: `playbook` (now, for the detected host, warnings included), `playbook --batch
  <batch>` (the recorded timing, warnings included) and `take`, `round` and `handoff` for a CR, and
  `take stack` (`cr_facts` in `commands/facts.py`, after `ci_lines`, and the stack's own take
  output; the lines only). `concepts.md`'s line limits already exempt these commands.

### Area 3: the cards

All edits on both hosts' text where a card names the host; the agent files (`agents/`,
`com.github.copilot/agents/`) are not touched (no contract lives there).

- `skills/chantier/references/hosts/claude-code.md`, "Heartbeat": "Each wake is scheduled with
  `ScheduleWakeup`, 30 minutes (1800 seconds) after the last" becomes: the steering wake of the
  `timing: Claude Code session:` line of `playbook --batch <batch>`, in seconds, after the last
  (30 minutes, 1800 seconds, by default). The idle stop (timing-Q14): "on a wake where no Driver of
  any kind (CR, stack, QA, release) has run since the last wake" becomes "on the first wake that
  sees no Driver of any kind (CR, stack, QA, release) run for 30 minutes or more, whatever the
  wake's interval".
- `skills/chantier/references/hosts/claude-code.md`, the "Tools" table, two new rows:
  - "Prompt cache TTL (the `cache_ttl` defaults)": a session's cache writes are 1-hour
    (`cache_creation.ephemeral_1h_input_tokens` in its transcript's usage), a subagent's 5-minute
    (`ephemeral_5m_input_tokens`); mark: "measured once, 2026-11-17, one account; unproved in
    general. Trial: on another account, or after a host update, one session and one subagent each
    write the cache, and their transcripts' `cache_creation` fields show the same split; record the
    date and the account's kind".
  - "Steering wake bound (60 minutes)": the CLI refuses a `steering_wake` over 60 minutes; proved:
    30 minutes (real-direct run 1, 2026-11-12); unproved: any other value up to 60. Trial: a batch
    with `session: steering_wake: 60m` whose Foreman's transcript shows a `ScheduleWakeup` of 3600
    seconds and a wake about an hour later; then one over 60 minutes, to learn whether the host
    accepts it, before the bound moves.
- `skills/chantier/references/hosts/copilot.md`, "Heartbeat": the Chief of Staff sends `/every
  <steering wake> chantier status --refresh --batch <batch> --epoch <n>`, the wake read from the
  batch's `timing: Copilot <family> models:` line for the family of the model it started the
  Foreman with, else from `timing: Copilot other models:` (timing-Q9), written in `/every`'s form
  (`4m` by default); in direct mode, from `timing: Copilot other models:`. The idle stop: "when
  every Driver has ended for 30 minutes" becomes "on the first wake that sees no Driver run for 30
  minutes or more, whatever the wake's interval" (timing-Q14).
- `skills/chantier/references/hosts/copilot.md`, its table of tools, two new rows:
  - "Prompt cache TTL (the `cache_ttl` default, `5m`)": unproved (timing-Q8). Trial: a Copilot
    session's record that shows how long its prompt cache keeps a prefix (a cached read after a
    pause of known length, and a cold one after a longer pause); record the date and the models.
  - "`/every` in whole minutes": the CLI refuses a Copilot duration that is not whole minutes;
    proved: `/every 4m` (the heartbeat today); unproved: another value. Trial: `/every` armed with a
    configured value other than 4 minutes, its wakes arriving at that interval; then a form in
    seconds, to learn whether `/every` takes it, before the rule moves.
- `skills/chantier/references/foreman.md`, "Heartbeat": "(every 30 minutes, and who arms it)"
  becomes "(at the steering wake of the batch's `timing:` line, and who arms it)". The idle stop
  (timing-Q14): "on a wake where no Driver of any kind (CR, stack, QA, release) has run since the
  last wake and no order is undone: every Driver has ended, ready or blocked, for 30 minutes at
  least" becomes "on the first wake that sees no Driver of any kind (CR, stack, QA, release) run
  for 30 minutes or more, whatever the wake's interval, and no order undone: every Driver has
  ended, ready or blocked, for 30 minutes at least". The 30 minutes do not follow the wake.
- `skills/chantier/references/chief-of-staff.md`:
  - the routing table (beside the rows for `hosts.<host>.roles` and `ci: beside_gate`): a new row
    for "wake the Foreman every X", "the cache TTL", "CI re-runs", "timing": `hosts.<host>.timing`
    in `chantier.yaml`, edited only on the user's word, then `$CHANTIER playbook` to show it (and
    its warnings); it counts from the next batch;
  - the Copilot arming text near line 1239 reads the wake as `hosts/copilot.md` now says, and its
    "because every Driver has ended for 30 minutes" follows the idle stop's new wording;
  - the plan's "Team" line also quotes the `timing:` lines, as printed, and any TTL warning.
- `skills/chantier/references/driver.md`, the CI bullet and its uses (timing-Q12: the rule stays a
  re-run of a job failed on the infrastructure; a red job that is the CR's goes to a round at once,
  as today): "an infrastructure failure gets one re-run" becomes "an infrastructure failure gets at
  most the CI re-runs of your `timing:` line (1 by default; 0: none), each at the same head"; "a
  failure the CR does not touch that passes on its re-run is a flake" becomes "passes on a re-run";
  the "one re-run, or a note" of the beside-the-gate outcomes and the "one re-run for an
  infrastructure failure" of "Heavy CI on a head" follow. Once the re-runs are used up and the job
  is still red on the infrastructure, the Driver ends with `handback <cr> blocked infra: CI <job>
  red on the infrastructure after <n> re-runs` (the stack driver: `[stack→foreman] anomaly <cr>
  infra: …`), as for a remote command today. The remote command's one re-run (the paragraph near
  line 252) and the Release driver's "On the infrastructure: one re-run" stay, and the sentence
  that tells them apart names the CI rule's limit as the `timing:` line's.
- The column a Driver reads: `driver.md` says once, where the CI bullet starts: on Claude Code the
  `subagent` line; on Copilot the line of your model's family, else `other models`.
- `skills/chantier/references/concepts.md`, "Escalation", the "A CR blocked twice" row (line 530):
  "`infra:` after its one re-run" becomes "`infra:` after its re-runs".
- `skills/chantier/references/concepts.md`, "Starting an agent": the configuration's list of what
  the CLI prints gains "and `hosts.<host>.timing`, which the CLI prints as `timing:` lines". Rule 8
  ("No `sleep`, no polling loop") is unchanged.

### Area 4: the board's server (`playbook/edit.py`, `board/config_api.py`, `board/state.py`)

- `edit.config_view` adds `timing`: for each host, its columns (id and the words the page shows:
  `Subagent`, `Session`, `Claude models`, `GPT models`), and for each of the three settings, per
  column, either the value that applies, the layer behind it (and its file) and whether it is the
  shipped default, or `not_used` (timing-Q16); plus the general value and its layer.
- `edit._flat` leaves out every `hosts.<host>.timing` leaf, so the timing does not show twice (in
  the Others table).
- No write (timing-Q7): `edit_surface_file` and the `PUT` route stay as they are (agent and model
  only); `AGENTS.md`'s line on what the board edits is unchanged.
- The "late" mark (timing-Q11): `board/state.py`'s `_batch` adds `steering_wake_min`, the batch's
  steering wake in minutes, read from `BatchRecord.timing` (the shipped defaults of the running
  plugin when the record has none): on Claude Code the `session` column's; on Copilot see open
  question 1. It is a board field only, not a `STATUS.json` field (`status/views.py` is not
  touched), so the pane does not change.

### Area 5: the Configuration page and the late mark (`board/web/js/views/config.js`, `board/web/css/views/config.css`, `board/web/js/model/semantics.js`, `board/web/js/i18n/*`)

- Two tabs under the title: Models (today's page, unchanged in content) and Timing. The legend
  sits on the tabs' line, on the right: a grey pill "shipped default", a teal pill with a dot "set
  in chantier.yaml". The tab is kept in the view's state (and its URL fragment, as the router
  keeps other view state), so a refresh stays on it.
- Timing, read-only: one card per host, side by side (two columns, stacking on a narrow window).
  Each card: the host's name, then a header row (`Setting`, then one column per column id), then
  one row per setting, each setting once: its name and one line saying what it is, then one value
  pill per column. A value from the defaults is grey; a value a user layer set is teal with a dot,
  and its title (hover) names the layer and file that set it (`surface project:
  projects/chantier/chantier.yaml`). A cell the column never reads shows "not used", muted, with no
  pill (timing-Q16). Words: "Steering wake: how often the Foreman or Chief of Staff wakes while it
  waits"; "Prompt cache TTL: the wake stays under it, to keep the cache warm"; "CI re-runs max:
  re-runs of a CI job failed on the infrastructure" (timing-Q12). No field, no button.
- The look is `board-visual-refresh/prototypes/01-mockups/final-config.html` (its `.ttabs`, `.tleg`, `.tcards`,
  `.hcard`, `.trow`, `.tv` and `.tv.set`); the values in that mock-up are illustrative, the page
  shows the configuration's, and the mock-up's Driver wake row is not drawn (timing-Q6).
- `semantics.js`: `HEARTBEAT_LATE_MIN = 15` goes; `heartbeat(batch, nowIso)` marks late when the
  minutes since the last wake exceed `batch.steering_wake_min` plus a margin of 5 minutes
  (`HEARTBEAT_MARGIN_MIN = 5`): 35 minutes on Claude Code and 9 on Copilot by default.
- English and French strings, as the page's other strings are.

### Area 6: the docs

- `docs/agents-and-models.md`, "The file's keys": the `hosts.<host>.timing` block, its settings,
  columns, what each column reads, units and bounds, defaults and the resolution order; "The
  layers": `timing: default` and a setting's `default`.
- `docs/hosts.md`'s heartbeat table: the interval is the configured steering wake (30 minutes and
  4 minutes by default); the idle stop is 30 minutes with no Driver, whatever the wake.
- `docs/use-cases-foreman.md` near line 178: "every four minutes" becomes "at the configured
  steering wake (four minutes by default)".

## Out of scope

- The Driver wake (`driver_wake`): split off as its own CR (timing-Q6). This CR adds no Driver
  timer and no exception to rule 8; the mock-up's Driver wake row is not built.
- A Timing editor (timing-Q7): the tab is read-only; values are set in `chantier.yaml` by hand or by
  the Chief of Staff on the user's word.
- Every wait and maximum not named above (timing-Q4): `max_rounds`, the 3-hour CI limit, the "no
  CI" minute, the idle stop's 30 minutes, the remote command's re-run, the Release driver's step
  re-run, the board's forge read every 10 s, the gate queue.
- The cost code: it prices the 5-minute and 1-hour cache writes from the transcripts, not from
  `cache_ttl`.
- The pane and `STATUS.json`: no field added.
- The agent files: no contract moves into them.

## Planning

- In the next batch with batch-22's retro points, cost-receipt and board-visual-refresh
  (timing-Q1).
- board-visual-refresh restyles the same Configuration page and its approved reference
  (`final-config.html`) is this CR's Timing tab. This CR builds the tab (data, route, view) in that
  look; board-visual-refresh restyles the Models tab and the rest. They share `config.js` and
  `config.css`: no `depends.json` for a shared file; the one that lands second rebases onto the
  other.

## Evidence

- `just check` green on Linux, macOS and Windows; `just test` within its budget.
- Tests (`skills/chantier/scripts/cli/tests/`, parametrized, in-process, added to
  `test_playbook_config.py` and `test_playbook_layers.py`):
  - the refusals, each with its file and line: an unknown key under `timing` (`driver_wake`
    among them), a column of the other host (`gpt` under `claude`), a setting under a column that
    is not one, a setting under a column that does not read it (`steering_wake` under `subagent`,
    `ci_reruns` under `session`), a duration under one minute, a duration with no unit, a Claude
    Code `steering_wake` of `61m`, a Copilot `90s`, a negative or fractional `ci_reruns`;
  - the resolution: a column's value above the general one in the same layer; a general value in a
    stronger layer above a column value in a weaker one (a user's general `cache_ttl` beats the
    shipped `session: 1h`); a reset taking a value back to the shipped default; no user file at all
    giving the shipped defaults, labelled `defaults`; a column's unread setting returned as "not
    used";
  - the TTL warning: printed when a column's `steering_wake` exceeds its `cache_ttl`, absent with
    the shipped defaults;
  - `config_view`'s `timing` for both hosts, its `not_used` cells, and `_flat` leaving the timing
    out; the board state's `steering_wake_min` from a recorded timing and from a record with none.
- `just scenario`: a step that writes `hosts.claude.timing.session.steering_wake: 20m` and
  `hosts.claude.timing.session.cache_ttl: 1h` in the planning surface's project file, checks
  `playbook` prints the `timing:` lines with `[surface project]` on the set values and no warning,
  opens a batch, checks `brief.md`'s Timing line and `playbook --batch` and `take <cr>` print the
  recorded lines, then changes the file and checks the running batch still prints the old values.
- The board: `GET /api/p/<id>/config` returns `timing`; the Timing tab rendered from the
  scenario's state, with a "not used" cell, screenshotted at the PR's head and set beside
  `final-config.html` in the PR's Deliverables, at the same window width (1680 px); the Batch view's
  heartbeat not late at 20 minutes on a Claude Code batch with the default wake, late at 36.
- The cards: a grep shows no "1800 seconds", "every 30 minutes" in the heartbeat, `/every 4m`,
  "one re-run" for a CI job, "`infra:` after its one re-run" or "has run since the last wake" left in
  `skills/`, and no `driver_wake` anywhere; `hosts/claude-code.md` holds the cache TTL and the
  60-minute rows with their marks and trials, `hosts/copilot.md` the cache TTL and whole-minutes
  rows with theirs; `just check`'s card tests pass.
- Unproved until a real batch: a Foreman on Claude Code scheduling its wake at a configured value
  other than 30 minutes (its transcript's `ScheduleWakeup` delay); on Copilot, the Chief of Staff's
  `/every` at a configured value; the idle stop on the first wake past 30 minutes with no Driver,
  with a wake shorter than 30 minutes.

## Open questions

None. The Chief of Staff settled the last one (2026-11-17) as recommended: on Copilot the board takes the longest steering wake among the host's columns and its general value, so the late mark is never shown too early; no record of the Foreman's model is added. The margin stays one wake plus 5 minutes.
