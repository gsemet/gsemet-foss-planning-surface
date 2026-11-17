# Change Specification: timing and retry settings in the configuration, per host and model family

## Goal

The user wants the loops' timing in the configuration, next to the models: how often the steering
session (the Foreman, or the Chief of Staff in direct mode) wakes, how often a Driver wakes, the
prompt cache's TTL those waits are chosen against, and how many times a CI job failed on the
infrastructure is re-run. Each has a shipped default and can be set in `chantier.yaml`, per host
and, inside a host, per model family (Copilot) or per context (Claude Code: subagent or session),
with a general value per host that each column may override. The board's Configuration page shows
them all on a Timing tab beside Models, a value set in `chantier.yaml` standing out from a shipped
default.

Every other wait or maximum stays where it is (02-answers, timing-Q4): the rounds limit, the
3-hour CI limit, the "no CI" minute, the 30-minute idle stop of the heartbeat, a remote command's
one re-run, the Release driver's one re-run of a procedure step, the board's 10-second forge read.

## Decisions carried from 02-answers.md

| Answer | Carried into |
| --- | --- |
| timing-Q1: in the next batch, with batch-22's retro points, cost-receipt and board-visual-refresh | Planning, below |
| timing-Q2: a card per host on a Timing tab beside Models, in board-visual-refresh's style; a value set in chantier.yaml stands out from a shipped default | Area 5 |
| timing-Q3: host x model family (on Claude Code: subagent or session), a general value each column may override | Areas 1 and 2 |
| timing-Q4: only the prompt cache TTL, the wakes (steering, Driver) and the CI retries' maximum | The four settings, Area 1 |
| timing-Q5: each setting once per host card, one value column per family or context; the legend beside the tabs; reference `board-visual-refresh/mockups/final-config.html` | Area 5, Evidence |

## The four settings

| Key | Meaning | Value | Who reads it |
| --- | --- | --- | --- |
| `steering_wake` | the interval of the steering session's heartbeat wake | a duration | the Foreman; the Chief of Staff in direct mode; on Copilot the Chief of Staff, which arms `/every` |
| `driver_wake` | how long a Driver waiting on its own background work (the CI watch, the long gate) stays asleep before it wakes: see open question 1 | a duration, or `off` | every Driver that waits on CI (CR, stack, QA, release) |
| `cache_ttl` | the prompt cache's time to live in that column: what the wakes are chosen against | a duration | the user (shown); see open question 5 |
| `ci_reruns` | the most re-runs of one CI job judged an infrastructure failure, at one head, before the Driver treats it as the CR's or blocks | a whole number, 0 or more | every Driver that judges CI |

A duration is written `<whole number><unit>`, the unit `s`, `m` or `h` (`90s`, `4m`, `1h`), and is
at least one minute; the CLI prints it in minutes (`30 min`, `1 min 30 s` when not whole). A wrong
value is refused with the file and line, as the other keys are (`hosts.claude.timing:
"steering_wake" is a duration of 1 minute or more: <n>s, <n>m or <n>h, found "<value>"`).

### Columns

- Claude Code (`hosts.claude.timing`): `subagent` and `session`. The steering session is a
  session: it reads the `session` column. A Driver is a subagent: it reads `subagent`.
- Copilot (`hosts.copilot.timing`): one column per model family, `claude` and `gpt`. An agent reads
  the column of the family of the model it runs (the first word of the model's identifier:
  `claude-sonnet-5.5` is `claude`, `gpt-6.1-sol` is `gpt`); a model of another family, or one it
  cannot name, reads the host's general value. Which column the Copilot steering wake takes: open
  question 4.
- The general value (the setting directly under `timing:`) applies to every column that does not
  set its own.

### The shape in chantier.yaml

```yaml
hosts:
  claude:
    timing:
      steering_wake: 30m      # general: every column
      ci_reruns: 1
      session:
        cache_ttl: 1h         # this column only
      subagent:
        cache_ttl: 5m
  copilot:
    timing:
      steering_wake: 4m
      gpt:
        ci_reruns: 2
```

A key under `timing:` is either one of the four settings or one of the host's columns; anything
else is refused (`host "claude": timing: unknown key "<key>": one of steering_wake, driver_wake,
cache_ttl, ci_reruns, subagent, session`). The layers merge it as any other mapping (a stronger
layer's leaf replaces a weaker one's; a plain `default`, `~` or `null` takes a value back to the
weaker layers and, at the bottom, to the shipped default).

### Shipped defaults (today's behaviour, unchanged)

In `config/chantier.defaults.yml`:

| Host | Setting | General | Column overrides | Source |
| --- | --- | --- | --- | --- |
| claude | `steering_wake` | `30m` | | today's `ScheduleWakeup` 1800 s, `hosts/claude-code.md`, "Heartbeat" |
| claude | `driver_wake` | open question 1 (`off` keeps today's behaviour) | | |
| claude | `cache_ttl` | `5m` | `session: 1h`, `subagent: 5m` | measured once, 2026-11-17, one account; unproved in general: the session transcript's usage showed `cache_creation.ephemeral_1h_input_tokens` only, a subagent's `ephemeral_5m_input_tokens` only; the row and its trial in `hosts/claude-code.md` (Area 3) |
| claude | `ci_reruns` | `1` | | today's "an infrastructure failure gets one re-run", `driver.md` |
| copilot | `steering_wake` | `4m` | | today's `/every 4m`, `hosts/copilot.md`, "Heartbeat" |
| copilot | `driver_wake` | open question 1 | | |
| copilot | `cache_ttl` | open question 3 | | |
| copilot | `ci_reruns` | `1` | | as Claude Code |

The defaults file's comment header names the timing block and that the values are what the cards
did before this CR. The test that keeps the defaults equal to the agent files reads the roles
only; it is left as it is.

## What changes

### Area 1: reading and checking (`playbook/config.py`, `playbook/layers.py`)

- `config._host`: a host's keys are `roles` and `timing` (the message becomes `one of roles,
  timing`). A new `_timing(host, node, kline, bad)` checks the block: each key a setting or a
  column of that host (`TIMING_COLUMNS = {"claude": ("subagent", "session"), "copilot": ("claude",
  "gpt")}` beside `HOST_FILES`), each column holding only settings, each value of its kind
  (durations, `off` for `driver_wake` only, a whole number for `ci_reruns`), a reset accepted where
  its key is. The shipped defaults go through the same check (`read_defaults`).
- `layers.py`: a new `load_timing(repo, roles_by_host, defaults)` returns, for each host and each
  column, every setting's value and the label of the layer behind it (`defaults`, `surface`,
  `surface project`, `repository`), the column's own value first, then the host's general value,
  each searched from the strongest layer down to the defaults. Unlike `load`, it answers with the
  defaults alone when no user file is present: the timing always has a value. A problem in a user
  layer is returned as the other keys' problems are, and `playbook` and `open` refuse on it as they
  do now.

### Area 2: the record and the prints (`commands/opening.py`, `core/records.py`, `playbook/lines.py`, `commands/rules.py`, `commands/facts.py`)

- `open` records the resolved timing of the batch's host in a new `BatchRecord.timing` field, next
  to `playbook`, whatever user files exist: a running batch keeps the timing it opened with, like
  its team ("applies at the next batch"). `brief.md` gets one line, `- Timing: <the timing lines>`.
- A batch record with no `timing` (opened before this change) reads as the shipped defaults of the
  running plugin; nothing is migrated.
- `playbook/lines.py`: a new `timing_lines(timing, host)` prints one line per column of the host:

  ```text
  timing: Claude Code session: steering wake 30 min, driver wake off, cache TTL 60 min, CI re-runs 1
  timing: Claude Code subagent: steering wake 30 min, driver wake off, cache TTL 5 min, CI re-runs 1
  ```

  each value a user layer set followed by its layer in brackets, as the role lines do (`steering
  wake 20 min [surface project]`); a value from the defaults has no label.
- Printed by: `playbook` (now, for the detected host), `playbook --batch <batch>` (the recorded
  timing) and `take`, `round` and `handoff` for a CR, and `take stack` (`cr_facts` in
  `commands/facts.py`, after `ci_lines`, and the stack's own take output). `concepts.md`'s line
  limits already exempt these commands.

### Area 3: the cards

All edits on both hosts' text where a card names the host; the agent files (`agents/`,
`com.github.copilot/agents/`) are not touched (no contract lives there).

- `skills/chantier/references/hosts/claude-code.md`, "Heartbeat": "Each wake is scheduled with
  `ScheduleWakeup`, 30 minutes (1800 seconds) after the last" becomes: the steering wake of the
  `timing: Claude Code session:` line of `playbook --batch <batch>`, in seconds, after the last
  (30 minutes, 1800 seconds, by default).
- `skills/chantier/references/hosts/claude-code.md`, the "Tools" table: a new row, "Prompt cache
  TTL (the `cache_ttl` defaults)": a session's cache writes are 1-hour
  (`cache_creation.ephemeral_1h_input_tokens` in its transcript's usage), a subagent's 5-minute
  (`ephemeral_5m_input_tokens`); mark: "measured once, 2026-11-17, one account; unproved in
  general. Trial: on another account, or after a host update, one session and one subagent each
  write the cache, and their transcripts' `cache_creation` fields show the same split; record the
  date and the account's kind".
- `skills/chantier/references/hosts/copilot.md`, "Heartbeat": the Chief of Staff sends `/every
  <steering wake> chantier status --refresh --batch <batch> --epoch <n>`, the wake read from the
  batch's `timing: Copilot <column>:` line (column: open question 4), written in `/every`'s form
  (`4m` by default); the same in direct mode. The "every Driver has ended for 30 minutes" stop
  stays 30 minutes.
- `skills/chantier/references/foreman.md`, "Heartbeat": "(every 30 minutes, and who arms it)"
  becomes "(at the steering wake of the batch's `timing:` line, and who arms it)". The idle stop's
  "for 30 minutes at least" stays.
- `skills/chantier/references/chief-of-staff.md`:
  - the routing table (beside the rows for `hosts.<host>.roles` and `ci: beside_gate`): a new row
    for "wake the Foreman every X", "the cache TTL", "CI re-runs", "timing": `hosts.<host>.timing`
    in `chantier.yaml`, edited only on the user's word, then `$CHANTIER playbook` to show it; it
    counts from the next batch;
  - the Copilot arming text near line 1239 reads the wake as `hosts/copilot.md` now says;
  - the plan's "Team" line also quotes the `timing:` lines, as printed.
- `skills/chantier/references/driver.md`, the CI bullet and its uses: "an infrastructure failure
  gets one re-run" becomes "an infrastructure failure gets at most the CI re-runs of your `timing:`
  line (1 by default; 0: none), each at the same head"; "a failure the CR does not touch that
  passes on its re-run is a flake" becomes "passes on a re-run"; the "one re-run, or a note" of the
  beside-the-gate outcomes and the "one re-run for an infrastructure failure" of "Heavy CI on a
  head" follow. Once the re-runs are used up and the job is still red on the infrastructure, the
  Driver ends with `handback <cr> blocked infra: CI <job> red on the infrastructure after <n>
  re-runs` (the stack driver: `[stack→foreman] anomaly <cr> infra: …`), as for a remote command
  today. The remote command's one re-run (the paragraph near line 252) and the Release driver's
  "On the infrastructure: one re-run" stay, and the sentence that tells them apart names the CI
  rule's limit as the `timing:` line's.
- `skills/chantier/references/concepts.md`, "Escalation", the "A CR blocked twice" row (line 530):
  "`infra:` after its one re-run" becomes "`infra:` after its re-runs".
- The column a Driver reads: `driver.md` says once, where the CI bullet starts: on Claude Code
  the `subagent` column; on Copilot the column of your model's family, else the general value.
- `driver_wake`: the Driver's text follows open question 1; with `off` (the recommended default if
  the user keeps today's behaviour) no card text changes for it.
- `skills/chantier/references/concepts.md`, "Starting an agent": the configuration's list of what
  the CLI prints gains "and `hosts.<host>.timing`, which the CLI prints as `timing:` lines"; if
  open question 1 makes a Driver wake periodically, rule 8's "No `sleep`, no polling loop" names
  it as a second exception, bounded by `driver_wake`.

### Area 4: the board's server (`playbook/edit.py`, `board/config_api.py`)

- `edit.config_view` adds `timing`: for each host, its columns (id and the words the page shows:
  `Subagent`, `Session`, `Claude models`, `GPT models`), and for each of the four settings, per
  column, the value that applies, the layer behind it, and whether it is the shipped default; plus
  the general value and its layer.
- `edit._flat` leaves out every `hosts.<host>.timing` leaf, so the timing does not show twice (in
  the Others table).
- Writing: open question 2. Until it is answered yes, `edit_surface_file` and the `PUT` route stay
  as they are (agent and model only), and the Timing tab is read-only.

### Area 5: the Configuration page (`board/web/js/views/config.js`, `board/web/css/views/config.css`, `board/web/js/i18n/*`)

- Two tabs under the title: Models (today's page, unchanged in content) and Timing. The legend
  sits on the tabs' line, on the right: a grey pill "shipped default", a teal pill with a dot "set
  in chantier.yaml". The tab is kept in the view's state (and its URL fragment, as the router
  keeps other view state), so a refresh stays on it.
- Timing: one card per host, side by side (two columns, stacking on a narrow window). Each card:
  the host's name, then a header row (`Setting`, then one column per column id), then one row per
  setting, each setting once: its name and one line saying what it is, then one value pill per
  column. A value from the defaults is grey; a value a user layer set is teal with a dot, and its
  title (hover) names the layer and file that set it (`surface project:
  projects/chantier/chantier.yaml`). Words, from the reference: "Steering wake: how often the
  Foreman or Chief of Staff wakes while it waits"; "Driver wake: how long a Driver waits on CI
  before it wakes" (its final words follow open question 1); "Prompt cache TTL: the waits stay
  under it, to keep the cache warm"; "CI re-runs max: re-runs of a CI job failed on the
  infrastructure" (open question 7).
- The look is `board-visual-refresh/mockups/final-config.html` (its `.ttabs`, `.tleg`,
  `.tcards`, `.hcard`, `.trow`, `.tv` and `.tv.set`); the values in that mock-up are illustrative,
  the page shows the configuration's.
- English and French strings, as the page's other strings are.

### Area 6: the docs

- `docs/agents-and-models.md`, "The file's keys": the `hosts.<host>.timing` block, its settings,
  columns, units, and defaults; "The layers": `timing: default` and a setting's `default`.
- `docs/hosts.md`'s heartbeat table: the interval is the configured steering wake (30 minutes and
  4 minutes by default).
- `docs/use-cases-foreman.md` near line 178: "every four minutes" becomes "at the configured
  steering wake (four minutes by default)".

## Out of scope

- Every wait and maximum not named above (timing-Q4): `max_rounds`, the 3-hour CI limit, the "no
  CI" minute, the idle stop's 30 minutes, the remote command's re-run, the Release driver's
  step re-run, the board's forge read every 10 s, the gate queue.
- The cost code: it prices the 5-minute and 1-hour cache writes from the transcripts, not from
  `cache_ttl`.
- A Timing editor, unless open question 2 says so.
- The board's "late" mark on the heartbeat (`HEARTBEAT_LATE_MIN = 15` in
  `board/web/js/model/semantics.js`), unless open question 6 says so.
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
  - the refusals, each with its file and line: an unknown key under `timing`, a column of the other
    host (`gpt` under `claude`), a setting under a column that is not one, a duration under one
    minute, a duration with no unit, `off` for a setting other than `driver_wake`, a negative or
    fractional `ci_reruns`;
  - the resolution: a column's value above the general one; a general value in a stronger layer
    against a column value in a weaker one (the column value still applies to its column: column
    first, then general, each from the strongest layer down); a reset taking a value back to the
    shipped default; no user file at all giving the shipped defaults, labelled `defaults`;
  - `config_view`'s `timing` for both hosts, and `_flat` leaving the timing out.
- `just scenario`: a step that writes `hosts.claude.timing.steering_wake: 20m` and
  `hosts.claude.timing.session.cache_ttl: 1h` in the planning surface's project file, checks
  `playbook` prints both `timing:` lines with `[surface project]` on the set values, opens a batch,
  checks `brief.md`'s Timing line and `playbook --batch` and `take <cr>` print the recorded lines,
  then changes the file and checks the running batch still prints the old values.
- The board: `GET /api/p/<id>/config` returns `timing`; the Timing tab rendered from the
  scenario's state, screenshotted at the PR's head and set beside `final-config.html` in the PR's
  Deliverables, at the same window width (1680 px).
- The cards: a grep shows no "1800 seconds", "every 30 minutes" in the heartbeat, `/every 4m`,
  "one re-run" for a CI job or "`infra:` after its one re-run" left in `skills/`; `hosts/claude-code.md`
  holds the cache TTL row with its mark and trial; `just check`'s card tests pass.
- Unproved until a real batch: a Foreman on Claude Code scheduling its wake at a configured value
  other than 30 minutes (its transcript's `ScheduleWakeup` delay); on Copilot, the Chief of Staff's
  `/every` at a configured value.

## Open questions

1. **The Driver wake.** Today no Driver wakes on a timer: it ends its turn while the CI watch runs
   in a background shell and the watch's end wakes it (`driver.md`, "CI"; rule 8 forbids polling).
   What should `driver_wake` do? Recommended: a Driver waiting on CI also runs, in a second
   background shell, a single bounded wait of `driver_wake`; when that wait ends first it takes one
   look at the checks (the head first), and if CI still runs starts one more bounded wait; the
   watch keeps running. Each wake reads the Driver's cache before its 5-minute TTL ends, which
   costs less than writing the whole context again after a long CI. Shipped default: `4m` on the
   Claude Code subagent column (under its 5-minute TTL), `off` elsewhere; or `off` everywhere to
   keep today's behaviour.
2. **Does the Timing tab write?** Recommended: read-only in this CR (the values are shown, set in
   `chantier.yaml` by hand or by the Chief of Staff on your word), since the board's write
   permission in `AGENTS.md` covers only each role's agent and model. A yes extends the
   Configuration page's write (a value pill becomes a field, "inherited" takes it back) and the
   `AGENTS.md` line that bounds what the board edits.
3. **Copilot's cache TTL default.** Nothing measured says what Copilot's prompt cache keeps.
   Recommended: ship `5m` for both families, marked unproved in `hosts/copilot.md` until a Copilot
   record shows it.
4. **Which Copilot column the steering wake takes.** The Foreman chat's model is not in the
   playbook. Recommended: the Chief of Staff uses the column of the model it started the Foreman
   session with when it knows it, else the general value; in direct mode, its own model's family.
5. **What the TTL does by itself.** Recommended: shown and printed only, plus one warning line in
   `playbook` when a wake in a column is longer than that column's TTL (`timing: Claude Code
   subagent: driver wake 8 min is above the cache TTL 5 min: each wake starts cold`); no value
   derived from it.
6. **The board's "late" heartbeat mark** fires after 15 minutes while the Claude Code wake is 30
   minutes. Should it follow the batch's steering wake (late beyond one wake plus a margin)?
   Recommended: yes, in this CR, from the batch's recorded timing.
7. **"CI retries max" means the infrastructure re-runs.** The mock-up's caption says "re-runs of a
   red check before the Debugger"; today only a job failed on the infrastructure is re-run, a red
   job that is the CR's goes to a round at once. Recommended: keep that rule and word the setting
   "re-runs of a CI job failed on the infrastructure".
