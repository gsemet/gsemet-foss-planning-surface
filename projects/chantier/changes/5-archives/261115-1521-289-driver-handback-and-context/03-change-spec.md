# Change Specification: a Driver always hands back, within its context

No issue.

## Goal

From the study of batch-18's real runs (2026-11-15), judged by the retro-critic. The batch-18 retro
says Drivers ended without a recorded hand-back 4 times (CR-257, CR-259, CR-262, CR-263), and ran
out of context twice (CR-262, CR-266). In the eval, Drivers peaked at 85k to 97k tokens. The
request asks for two things:

1. Detect "a Driver ended, and no hand-back was recorded". The transcript-end reading of the
   `close-sees-finished-agent` CR can serve.
2. Keep a Driver's context bounded.

Decisions (`02-answers.md`, 2026-11-15): the request's scope stands as written. The user planned
this CR with 18 others in one parallel batch before the release ("oui planifie les 19"). No
behaviour question was left open, and implementation detail is the agents'. The points the
request leaves open take this specification's defaults, listed at the end.

## The measure (done while writing this specification)

Source: batch-18's Foreman session, `C:/Users/gaeta/.claude/projects/C--Users-gaeta-Projets-chantier/446cff2e-8291-4f73-9ff0-f19c29743e6e.jsonl`,
and its Drivers' `subagents/agent-<id>.jsonl` beside it. Also used: the batch record
`.agents/changes/4-batch/events.jsonl` and the two eval audits named in `intake/request.md`.

Method, which the Verifier repeats:

- For a Driver: list each `assistant` record's `tool_use` items (name, input) and `text` items, and
  each `user` record's text.
- A turn end is an assistant `text` followed by a `user` text (a notification, a message or the
  host's `[handback-send-enforce]`).
- The prompt size is computed the way `costs.sessions._line_context` computes it. A compaction is
  a `system` record with `subtype` `compact_boundary`.
- For the Foreman: read the `<task-notification>` texts and the `SendMessage` calls at the times
  below.

### 1. Of the six "no recorded hand-back" interventions, four were not ends

Four times, the Foreman sent a Driver a message saying the Driver had ended with no hand-back.
Each time the Driver had ended its turn while its own long gate or CI watch ran in a background
shell, as `driver.md` allows. The host had told the Foreman so in the notification just before:
`Agent "<name>" is waiting on its own background work`, with the note "This agent stopped with
background work of its own still running. It may resume on its own when that work completes…;
the result below may be interim."

| CR | Driver | Turn end | Host notification | Foreman's message |
| --- | --- | --- | --- | --- |
| CR-263 | `afa8f5839de908336` | 2026-11-14 21:57:44 "Next I wait for the local gate" | 21:57:46 waiting on its own background work | "Your turn ended while waiting, which is not a hand-back" |
| CR-257 | `a41fb231abed92f69` | 22:01:34 "CI at c6ec311 is green. I'm waiting for the local gate." | 22:01:36, same | same |
| CR-259 | `ae0bbdc1c2ed83668` | 23:14:23 "…so I'm waiting for the gate to finish" | 23:14:24, same | same |
| CR-262 | `a6a4eb93596c562ba` | 2026-11-15 02:12:33 "CI is green at 63a6138. I'm waiting for the long gate." | 02:12:34, same | "Your turn ended with no hand-back and CR-262 is still working" |

The host has a second notification, `Agent "<name>" finished` ("fires each time this agent stops
with no live background children of its own"). Its result says where the `SubagentHandback`
report went. The two notifications are told apart by their summary.

### 2. Two Drivers called the host's hand-back before `$CHANTIER handback`

| CR | Driver | What happened | How it was repaired |
| --- | --- | --- | --- |
| CR-263 | `a2c1f342e038708e6` | `SubagentHandback` at about 01:55:50 with no `$CHANTIER handback` before it | At 01:55:55 the Foreman's `status` showed CR-263 `working`. It resumed the Driver with `SendMessage` at 01:55:59, and the Driver ran `handback CR-263 ready …` at 01:56:08. |
| CR-262 | `ae6e32e6270cf2ba5` | `SubagentHandback` at 02:52:10 with no `$CHANTIER handback` | The Foreman ran `agents set 262 -` (02:52:15) and resumed the Driver at 02:52:22 ("your hand-back isn't recorded"). The Driver recorded it at 02:52:28. |

Both repairs were a resume by message, and both took under 10 seconds. Both were found by chance:
the Foreman compared the Driver's report with `status`. Nothing in the CLI points at it.

In every Driver transcript of batch-18 that ended, the last `tool_use` is `SubagentHandback`. A
record written after it (a later background notification, a short text) does not change that. A
Driver resumed after its hand-back adds new tool calls after it.

### 3. No Driver ran out of context

| CR | Driver | Peak prompt | Compactions | How it really ended |
| --- | --- | --- | --- | --- |
| CR-262 | `a6a4eb93596c562ba` | 99,239 | 0 | At 02:50:12 it sent the description pass back to its Verifier `af15bfb16c59e3a17` by `SendMessage`. It ended its turn at 96,069 tokens ("I'm waiting for that reply"), and the host asked for its hand-back (`[handback-send-enforce]`). It handed back `blocked context: host asked the hand-back at 95000 tokens`, the wording `driver.md` gives that case. The real cause was the message to a worker, which `driver.md` forbids ("A worker is never resumed by a message to its agent"). |
| CR-266 | `ac3061ac821af857f` | 116,972 | 0 | It recorded `handback CR-266 ready … draft on <CR-265's branch>: waits for CR-265` (04:37:56). The next Driver (`aa8848ec33e234b07`, 04:41:53) came from the take `rebase: stacked on CR-262`, not from a context restart. |

The highest Driver peaks measured:

- batch-18: 119,401 (CR-263, `afa8f5839de908336`; its last two calls came after its hand-back);
- eval `real-direct` 2026-11-15: 123,512 (CR-101, 171 calls);
- eval `real-foreman` 2026-11-15: 97,774 (CR-104).

No Driver compacted in batch-18 or in either eval run, and all of them stayed under the
130,000-token threshold of `driver.md`. The measured first compaction is at about 162,000
(`hosts/claude-code.md`, "Compacting"). **The threshold stays 130,000.**

The "ran out of context twice" in the retro is a misreading. CR-262's `context:` label hid a
turn that ended early. CR-266 never stopped for its context.

### What this means for the change

- The detection the request asks for is needed for the two cases of point 2.
- The Foreman must stop reading "waiting on its own background work" as an end (point 1).
- A turn that ends early must stop being recorded as a context end (point 3).
- The context rule itself holds, and only its wording for the host's early ask changes.

## What changes

### 1. CLI: `status` flags a working CR whose Driver ended with no hand-back recorded

The flag reads the end of the Driver's transcript.

`skills/chantier/scripts/cli/src/chantier/costs/sessions.py`, beside `agent_context`: add a reader
of an agent's end, for example `agent_handed_back(root, sessions, agent) -> bool | None`.

- It finds `subagents/agent-<agent>.jsonl` beside each steering transcript, as `agent_context`
  does.
- It reads the file from its end in growing chunks, as `_tail_context` does, never the whole of
  it, until it finds the last `assistant` record that carries a `tool_use` item.
- It returns `True` when that item's `name` is `SubagentHandback`, and `False` when it is another
  tool.
- It returns `None` when no file is found, the file cannot be read, or no tool call is in it.
  `None` is "not measured", never "ended".
- An unreadable line is skipped, as `_line_context` skips it.

`skills/chantier/scripts/cli/src/chantier/commands/batch_status.py`, `_cr_row`: for a CR in
`working` with an `agent` recorded, on a batch whose `host` is not `copilot`, read that agent's
end with the steering sessions `context_line` uses (`foreman_uuid(d)`; no sessions, no flag).
When the reader returns `True`, append to the row, after the `no Driver recorded` check's place:

` | Driver <agent> ended, no hand-back recorded`

`<agent>` is the id as recorded.

- No other row changes. A `ready`, `blocked`, `queued`, `merged` or `cancelled` CR is not read.
  Neither is a working CR with no agent (it keeps `no Driver recorded`).
- The flag shows on every `status` call, with or without `--refresh`.
- `status` writes nothing more: no event, no field in `batch.json`, `STATUS.json` or `STATUS.md`.
  The board and the CR board pane do not change, so the screenshot rule of `AGENTS.md` does not
  apply.
- Copilot: no flag. Copilot keeps no per-agent record ("Copilot gives no per-agent record", as
  `context_line` says).
- The CLI states the fact and judges nothing: the card says what to do with it.

**Coordination with `close-sees-finished-agent`** (same batch, parallel). That CR reads the same
transcript end for `close` and `pause` (`rails.py`, `running()`). There is to be one reader of a
transcript's end in the CLI. The two CRs are not ordered (no `depends.json`), and whichever CR
lands second rebases and reuses the first one's reader. If that reader returns more than this CR
needs (for example "running", "ended" or "unreadable"), this CR's "ended" is its "the last tool
call is `SubagentHandback`". The second CR does not keep a copy of the reader.

### 2. Card: `skills/chantier/references/foreman.md`

Keep the card's voice and wrap at its width (about 100 characters). Direct mode needs no separate
edit: `chief-of-staff.md`, "Steering a batch yourself", already sends the Chief of Staff to this
card.

a. "Your means", the `$CHANTIER status` bullet (line ~149-153): after `a CR with no agent recorded
   shows no Driver recorded in its row`, add: a working CR whose recorded Driver called the host's
   hand-back with no `handback` recorded shows `Driver <id> ended, no hand-back recorded` (Claude
   Code only).

b. The same section, the sentence on `agents set` (line ~163-164, "`-` when it ended, with its
   hand-back or without, before the CR's next `take`"). Make it say: when a Driver ends, read its
   row in `status` before `agents set <cr> -`. A row showing `ended, no hand-back recorded` takes
   bullet (d) first, with the id still recorded (the flag reads it).

c. The host's notifications (a new bullet in "A lost Driver", before "Suspect"). A Driver that
   ends its turn while its own background work runs (the long gate, a CI watch) has not ended.
   On Claude Code the host says `Agent "<name>" is waiting on its own background work`. Send it
   no message and no ping, and do not run `agents set -`. It wakes on its own when that work
   ends, and the heartbeat's `activity` line covers it (`gate running`, `gate queued`, an age).
   Only `Agent "<name>" finished`, or a host refusal, is an end.

d. A new bullet in "A lost Driver", after "A host failure": **A Driver that ended with no
   hand-back recorded** (the `status` flag, or a `[driver <cr>→foreman] hand-back …` report while
   `status` still shows the CR `working`).
   - Resume it once by the host's means (`SendMessage` on Claude Code, `write_agent` on Copilot):
     `[foreman→driver <cr>] record your hand-back: $CHANTIER handback <cr> as your report says,
     then the host's hand-back with the line it prints`.
   - Keep or set again its id (`agents set <cr> <id> --epoch <n>`), so the log shows the resume.
   - When the CLI records its hand-back, handle it as any hand-back.
   - When it does not record one by the next heartbeat wake, or the host refuses the message:
     `agents set <cr> - --epoch <n>`, then the restart path with `--note "resume: ended with no
     hand-back recorded: <its report's first line>"`. This counts as a silent end ("A silent
     end"). A resume that records the hand-back counts as nothing.
   - Never record the hand-back yourself: `handback` is the Driver's.

e. "A hand-back `blocked context: …`" (line ~543-547): "(the Driver's context ran out)" becomes
   "(the Driver's context reached the threshold, or the host asked its hand-back early: its text
   says which)".
   - The restart is unchanged.
   - In a report or a retro, a `context: host asked the hand-back …` is named "a turn ended
     early", with what the Driver waited for, never "out of context".
   - The "second `context:`" ask counts only real context ends (no `host asked the hand-back` in
     the text).

### 3. Card: `skills/chantier/references/driver.md`

a. "Your means", the "Your end:" bullet (line ~410). At its start, before the `ready` details, put
   the order of the end in one sentence:
   - first `$CHANTIER handback <cr> …`;
   - once the CLI accepted it, the host's hand-back, whose first line is the line `handback`
     printed (`[driver <cr>→foreman] hand-back …`), unchanged;
   - a hand-back the CLI refused is never followed by the host's hand-back until a `handback`
     (ready or blocked) is accepted;
   - a report sent with no recorded hand-back leaves the CR `working`, and the steering session
     resumes you to record it.

   Move here, from the Context bullet (line ~134), the sentence "Never call the host's hand-back
   with no `$CHANTIER handback` first", so that it appears once.

b. The Context bullet (line ~119-135), the sentence on the host's early ask. The text becomes
   `handback <cr> blocked context: host asked the hand-back at <n> tokens while waiting for <what>:
   <where it stopped, what is next>`. `<what>` is what the turn waited for (a worker's reply, the
   gate, CI). Add: a turn that ended to wait for a worker's reply had broken "a worker is never
   resumed by a message".
   - Keep the text `` `context: <where it stopped `` in `driver.md`: the scenario's card check
     looks for it (`scenario/run_scenario.py`, grep `context: <where it stopped`).
   - The 130,000 threshold and its reason do not change.

c. "CR driver", the description pass (line ~550-552): "(`NOT VERIFIED` is fixed in the
   description, then checked again)" becomes "(`NOT VERIFIED` is fixed in the description, then
   checked again by a new short `verifier` start, never a message to the Verifier that replied)".
   This is the CR-262 case of the measure.

d. The CI wait (the Context bullet's "The one turn end that waits is the long CI wait…"): add that
   ending the turn while your own long gate or CI watch runs in a background shell is allowed and
   needs no message. The host tells the steering session that you are waiting on your own work.

### 4. Card: `skills/chantier/references/hosts/claude-code.md`

In the capabilities table (line ~550-563):

- The row "Resume a stopped subagent": "chantier uses it only for the `taken back:` note of
  `foreman.md`" becomes "for the `taken back:` note and the `record your hand-back` note of
  `foreman.md`". Add to its mark: proved, batch-18, twice (`a2c1f342e038708e6` and
  `ae6e32e6270cf2ba5` recorded their hand-back within 10 seconds of the message).
- A new row, "A background subagent stops":
  - `<task-notification>` summary `Agent "<name>" is waiting on its own background work`: the
    agent stopped with background work of its own running. It resumes when that work reports, so
    it has not ended.
  - `Agent "<name>" finished`: the agent stopped with no live background child. Its
    `SubagentHandback` report arrives as a message.
  - Mark: proved, batch-18, Foreman session `446cff2e-8291-4f73-9ff0-f19c29743e6e` (the four
    cases of the measure, point 1).
- A sentence by the "Compacting" section's measured line: Drivers of batch-18 and of both eval
  runs of 2026-11-15 peaked at 80k to 124k with no compaction.

### Not changed

- The agent files (`agents/`, `com.github.copilot/agents/`): the contract lives in the cards.
- `hosts/copilot.md`: the flag is Claude Code only, and `foreman.md`'s bullet (d) already names
  `write_agent`.
- `worker.md`.

## Out of scope

- The 130,000 threshold, the agents' `autoCompactWindow`, their model, and the Driver's opening
  reads: the measure shows no Driver near a compaction (default O3).
- A new hand-back reason word (for example `ended:`) for the host's early ask. That would change
  the CLI's `handback`, J24's list of words and both cards (default O2).
- Blocking the host's hand-back itself. A plugin hook that refuses a Driver's stop is out of
  scope: `hooks/` holds the pane's module only, and the CLI messages no agent and knows no role.
- `close` and `pause`'s quiet check (`rails.py`, `running()`, `QUIET_SECONDS`): that is
  `close-sees-finished-agent`.
- The stack driver and a QA order's driver: the flag reads CR rows only, release CRs included.
- `STATUS.json`, `STATUS.md`, the board and the CR board pane.
- Copilot: no per-agent record to read.

## Evidence

### `just check` and `just test`

`just check` passes on Linux, macOS and Windows (CI on the PR). The tests stay within the time
budget of `AGENTS.md`.

Add one parametrized unit test in `skills/chantier/scripts/cli/tests/test_cost_reading.py` (or the
test file that holds `agent_context`'s tests) for the reader, on files written in `tmp_path`. The
cases and the result each one expects:

| File | Expected |
| --- | --- |
| Last tool call `SubagentHandback`, then a later text record | `True` |
| Last tool call `PowerShell` with no result | `False` |
| `SubagentHandback`, then a resumed turn with a `PowerShell` call | `False` |
| A transcript larger than one read chunk whose last tool call is `SubagentHandback` | `True` |
| A missing file | `None` |
| A file with no tool call | `None` |

### `just scenario`

`just scenario` passes for `--forge github` and `--forge gitlab`. As `AGENTS.md` asks for a change
to the CLI and the cards, the pipeline's `just scenario (ubuntu-latest)` job is green at the PR's
head.

Extend `scenario/run_scenario.py`, `driver_liveness`, next to the check "status flags a working CR
with no Driver recorded" (about line 3477). Use that section's `sub` folder and the first CR with
its agent recorded. Each step has its own `check(...)`:

1. Write `agent-agent-<one>.jsonl` whose last assistant record carries a `tool_use` named
   `SubagentHandback`. `status` → the CR's row contains `Driver agent-<one> ended, no hand-back
   recorded`.
2. Append an assistant record with a `tool_use` named `PowerShell`. `status` → no flag.
3. With the `SubagentHandback` file back, run the Driver's `handback <one> blocked question: x`.
   `status` → the row shows `blocked`, with no flag.
4. A working CR with no agent recorded keeps `no Driver recorded` and gets no flag.
5. `status` writes nothing: `events.jsonl` has no new line from the `status` calls of steps 1 and
   2.

The resume of bullet 2d, and the Foreman's reading of the host's notifications, are behaviour
between agents. The scenario runs no agents, so it does not prove them. The next real batch is
where they are seen.

### The Verifier

- It quotes, with `git grep -n` at the pushed head:
  - `ended, no hand-back recorded` in `batch_status.py` and `foreman.md`;
  - `waiting on its own background work` in `foreman.md` and `hosts/claude-code.md`;
  - `record your hand-back` in `foreman.md` and `hosts/claude-code.md`;
  - `while waiting for <what>` and `a new short \`verifier\` start` in `driver.md`;
  - `130,000` still in `driver.md`.
- `git grep -n "Never call the host's hand-back"` under `skills/` finds it once.
- It repeats the measure's method on the Foreman session named there, and finds the times and
  peaks of the three tables. A later cleanup may have removed the transcripts. In that case
  `verify.md` says so and carries the figures from this specification.
- `git diff --stat <base>..HEAD` lists only `costs/sessions.py`, `commands/batch_status.py`, the
  test file, `scenario/run_scenario.py`, `foreman.md`, `driver.md`, `hosts/claude-code.md`, and
  the CR's archive when the project asks for it.

### Known gaps the PR names

- Two things are not seen in a real batch yet. One is the Foreman leaving a Driver alone on
  "waiting on its own background work". The other is resuming a Driver flagged `ended, no
  hand-back recorded`. Both are proved when a later batch shows them in its Foreman transcript.
- The flag reads Claude Code's transcript format (`SubagentHandback` as a `tool_use` name). A
  host update that renames the tool makes the flag silent, never wrong.

## Open points, with the default taken

None of these is a behaviour question the answers leave open: the answers keep the request's
scope and give implementation detail to the agents. The Chief of Staff may still take O1 to the
user, because it widens the use of a resume by message.

- **O1. What the steering session does with a Driver that ended with no hand-back recorded.**
  Default: resume it once by message to record its hand-back, and take the restart path (a silent
  end) only when that fails. Both batch-18 cases were repaired this way in seconds. A new Driver
  costs a fresh context of about 20k to 30k tokens, and counts a silent end the Driver did not
  really have. The resume reuses the host means `foreman.md` already uses for `taken back:`.
- **O2. The host's early ask keeps the `context:` word.** Default: keep it, with `while waiting
  for <what>` in the text, and the Foreman naming it "a turn ended early". This follows CR-236's
  O2: the `context:` route already restarts a fresh Driver from the record with no ask. A new
  word would change the CLI, the eval's J24 and both cards.
- **O3. The context threshold and the Driver's reads.** Default: no change. No Driver compacted
  in batch-18 or in either eval run. The highest peak was 123,512, under 130,000, and the first
  compaction measured is at about 162,000.
