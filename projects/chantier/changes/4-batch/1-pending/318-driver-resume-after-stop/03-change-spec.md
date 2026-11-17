---
type: cr-change-spec
description: A Driver stopped from outside is restarted by the steering session on the batch's go, at each such stop and counting toward nothing, and the heartbeat sees it.
---

# Change Specification: a stopped Driver resumes without the user's word

## Goal

In batch-22 (2026-11-16, direct mode) three Drivers (CR-299, CR-303, CR-304) were stopped by the
host at a compaction of the steering session. The steering session tried to resume them by
`SendMessage`; Claude Code refused each with:

> Agent <id> was stopped and won't be resumed. Treat its work as cancelled; only launch a new agent if the user explicitly asks.

The steering session read that as a need for the user's word, and the batch waited on the user.

The user's decisions (`02-answers.md`):

- **driver-resume-Q1:** the batch's go already covers this. A Driver stopped from outside is
  restarted by the steering session itself, as a fresh Driver by `take <cr> --note "resume:
  <cause>"`, with no question to the user, and the restart is said in the report. The heartbeat
  detects a Driver that is still recorded but stopped, so the restart does not hang on someone
  noticing.
- **resume-stop-Q2 (counting):** a stop from outside counts neither toward `driver ended twice`
  nor toward "blocked twice": it is the host's doing. The Driver is restarted at each such stop.
- **resume-stop-Q3 (which stops):** the rule covers only a stop the steering session did not make
  itself. Its own `TaskStop` (a switch to Foreman mode, a drop, the user's stop or hold) is never
  restarted by this rule. A stop the user makes in the app is not the steering session's, so it
  is a stop from outside.
- **resume-stop-Q4 (what is detected):** the stops a compaction snapshot reports (`task_status`
  `killed`), plus the host's refusal of a message; the card and the host row say so. A trial
  records what a stop made by the user in the app leaves in the transcript.

## Evidence of the case (batch-22, Chief of Staff session `91f1382a-eacd-437e-b5a8-f9e545753a8c`)

- At `2026-11-16T20:33:02Z`, with the `compact_boundary` record (trigger `manual`), the steering
  transcript got one `attachment` record per Driver:
  `{"type":"attachment","attachment":{"type":"task_status","taskId":"a0106566b6aa3f0cb","taskType":"local_agent","description":"Driver CR-299","status":"killed",...,"canContinueAgent":true}}`,
  rendered to the session as `Task "Driver CR-299" (a0106566b6aa3f0cb) was stopped.` The same for
  `a103955deaf241307` (CR-304) and `a164f7a02355addd0` (CR-303).
- At `20:49:19Z` to `20:49:22Z`, three `SendMessage` calls got `{"success":false,"message":"Agent <id> was stopped and won't be resumed. Treat its work as cancelled; only launch a new agent if the user explicitly asks."}`.
  The `canContinueAgent: true` of the notice did not hold.
- Each stopped Driver's own transcript ends on a prompt with no answer (the record's
  `close --stopped` lines name the same agents with "its last record is a prompt with no answer
  yet"). Its transcript alone cannot tell it from a running one.
- Not yet seen: what a stop made by the user in the app leaves in the steering transcript (Q4's
  trial, below).

## What changes

### 1. The cards: the outside stop is a proven death, restarted on the go

`skills/chantier/references/foreman.md`, "A lost Driver" (it holds in a direct batch too, whose
Chief of Staff reads this card):

- **Proof of death** (today "one of two"; it becomes "one of three"): add a third proof, read at
  once, with no ping round and no message first: the host says the Driver was stopped. On Claude
  Code that is exactly two things (Q4): the stop a compaction snapshot reports (the `task_status`
  `killed` record, which the session sees as `Task "<name>" (<id>) was stopped.`, and which the
  `status` flag of section 2 reads: a CR's row in any `status`; the stack driver's and a QA
  order's `activity` line in `status --refresh` only), and the host's refusal `Agent <id> was
  stopped and won't be resumed…` of a message sent to it. Never try `SendMessage` to resume such a
  Driver: the host refuses it (proved, batch-22).
- **A new bullet, "A Driver stopped from outside"** (any Driver kind: CR, release, stack, QA
  order), next to "A host failure":
  - **Which stops (Q3):** only a stop the steering session did not make itself. Its own stop by
    the host's means (`TaskStop` on Claude Code: a switch to Foreman mode, a drop, the user's stop
    or hold, the `stop` after a `pong` with no progress for 3 hours) is never restarted by this
    rule; each of those keeps its own path. A stop the user makes in the app is from outside.
  - **Keeping its own stops apart:** the snapshot record does not say who stopped the agent, and a
    compaction may come after the steering session's own stop. So when the steering session stops
    a Driver itself and does not restart it at once by the restart path, it clears the id it
    recorded for it in the same turn (`agents set <cr> - --epoch <n>`, or the stack's or the QA
    order's own clearing as the restart path names it), after a `note <cr> "stopped: <why>"` for a
    CR. The `status` flag names only a recorded agent, so it never shows for the steering
    session's own stop; and a refusal to a message to an agent it no longer has recorded is not
    this rule.
  - **What it does:** it takes the restart path at once (`agents set <cr> - --epoch <n>`,
    `handoff <cr>`, `take <cr> --note "resume: stopped from outside: <the host's text>" --epoch
    <n>`, a new Driver, `agents set <cr> <id> --epoch <n>`; for the stack, `take stack --note …`
    as in its existing restart). It is covered by the batch's go: no ask, no question to the user,
    no wait for the user's word. The host's words "only launch a new agent if the user explicitly
    asks" are answered by that go; the card says so in one sentence.
  - **Counting (Q2):** it is the host's doing, like a death by the host: it counts neither toward
    `driver ended twice` nor toward "blocked twice" in Escalation, and it is restarted at each
    such stop, however many (no "second stop" ask, unlike a second host failure).
- **Said in the report:** the steering session's next report names each such restart: the CR,
  "stopped from outside", the time of the stop, and the new Driver's agent id. In Foreman mode
  the Foreman's report line to the Chief of Staff carries it, and the Chief of Staff gives it in
  its report to the user.
- **"A Driver that ended with no hand-back recorded"** (lines ~601-611): today, when the host
  refuses the `[foreman→driver <cr>] record your hand-back: …` message, the bullet sends the
  Driver down the restart path with `--note "resume: ended with no hand-back recorded: …"` and
  says "This counts as a silent end". Change it so that a refusal that says the Driver was stopped
  (`Agent <id> was stopped and won't be resumed…`) is the outside stop: it goes to "A Driver
  stopped from outside", with its note `resume: stopped from outside: <the host's text>`, and
  counts as nothing. Any other refusal, or no hand-back by the next wake, keeps today's rule.
- **"A silent end"** (lines ~613-616): its last sentence lists what does not count ("a death by
  the host (a new epoch, all Drivers lost at one wake) and a `context:` hand-back do not"); add
  "a Driver stopped from outside".
- **"Your means"**, the `status` bullet (lines ~153-158): add the new flag next to `Driver <id>
  ended, no hand-back recorded`: `Driver <id> stopped from outside, no hand-back recorded`
  (Claude Code only).

`skills/chantier/references/concepts.md`:

- "An agent that ends before its part is done", the causes list: add `stopped from outside:
  <the host's text>`.
- The same section's first bullet (line ~492, "Each such end is restarted **once**"): add that a
  Driver stopped from outside is restarted as foreman.md's "A Driver stopped from outside" says,
  at each such stop, not under this "once", and that such a stop counts toward nothing. Other
  agents and other causes keep "once".
- "Escalation", the row "A CR blocked twice" (line ~530): add, with the hand-backs that never
  count, that a Driver stopped from outside never counts (it is no hand-back, and it does not
  make `driver ended twice`).
- Line ~463 ("on Claude Code a message resumes a stopped agent with its context"): say that this
  holds for an agent that ended its turn, and not for one the host stopped (a `killed` task),
  which the host refuses to resume.

`skills/chantier/references/hosts/claude-code.md`, the capabilities table:

- Row "Resume a stopped subagent" (line ~615): add that a subagent the host stopped (its
  `task_status` `killed`, the notice `Task "<name>" (<id>) was stopped.`) is not resumable:
  `SendMessage` gets `Agent <id> was stopped and won't be resumed. Treat its work as cancelled;
  only launch a new agent if the user explicitly asks.`; proved, batch-22 (the three agent ids and
  the time above).
- A new row, "A background subagent is stopped from outside": what chantier detects, and nothing
  else (Q4): the stop a compaction snapshot reports (the steering transcript's `attachment` record
  `task_status` with `status: "killed"` and the agent's id as `taskId`, seen by the session as
  `Task "<name>" (<id>) was stopped.`), and the refusal of a message to it. Proved: batch-22, a
  manual compaction. Unproved, with its trial: what a stop made by the user in the app leaves in
  the steering transcript (trial: in a session with a background subagent, the user stops it in
  the app; record whether and when a `task_status` `killed` record or another record appears,
  before and after a compaction).
- Row "Stop a Driver" (`TaskStop`, line ~37): add that after its own `TaskStop` with no restart at
  once, the steering session clears the recorded id (foreman.md, "A Driver stopped from outside").

`skills/chantier/references/chief-of-staff.md`: the "Recovery" bullet (line ~1323) gets one
sentence pointing to foreman.md's "A Driver stopped from outside" for a direct batch, so the
Chief of Staff steering in direct mode restarts with no question to the user, and clears the id
after its own stop as that bullet says.

The Copilot host's reference (`hosts/copilot.md`) gets one line: an outside stop on Copilot is
unproved, and the card's rule holds when the host says the Driver was stopped. The agent files
(`agents/`, `com.github.copilot/agents/`) do not change.

### 2. The CLI: `status` flags a Driver recorded but stopped

`skills/chantier/scripts/cli/src/chantier/costs/sessions.py`: a new reader, for example
`agents_stopped(root: Path, sessions: list[str], agents: set[str]) -> dict[str, bool | None]`,
reading each steering transcript (`transcript_path(root, session)`, the main file, not the
`subagents/` folder) from its end (the existing `_lines_from_end`). For each agent asked, the
last `attachment` record whose `attachment.type` is `task_status` and whose `attachment.taskId`
is that agent decides: `status == "killed"` is stopped (True); any other status is False; none
found, or a file missing or unreadable, is None (not measured, never "stopped"). One backward
pass serves every working CR of the call.

The scan is bounded by the agents' own start, not by finding their records: a `task_status`
record is written only at a compaction of the steering session (the snapshot batch-22 shows), so a
Driver started since the last compaction has none, and a pass that stopped only "once every agent
asked has its record" would read the whole transcript at every `status` and heartbeat wake. The
reader therefore takes, for each agent asked, its start: the time (`t`) of the last `agent` event
of the batch's events log that names it (written by `agents set`, read as `_event_ages` in
`commands/activity.py` reads it). The backward pass stops at the first record whose `timestamp`
is older than the earliest start among the agents asked (a line with no `timestamp` neither
decides nor stops), or once every agent asked has its record, whichever comes first. A record
older than an agent's start never decides for it (an id is not reused, but the bound costs
nothing). An agent with no recorded start is not asked (None).

The reader does not try to tell the steering session's own stop from an outside one: the record
does not say, and the card's rule (section 1, the id cleared after its own stop) keeps an agent
the steering session stopped itself out of the agents asked.

`skills/chantier/scripts/cli/src/chantier/commands/batch_status.py`, `_cr_row`: a working CR
whose recorded agent the reader says stopped gets ` | Driver <id> stopped from outside, no
hand-back recorded`, checked before the existing `ended, no hand-back recorded` flag (the two
never show together). A plain `status` prints one row per CR (`_cr_row`, from `status` in
`batch_status.py`, lines ~271-286) and no line for the stack driver or a QA order's agent (the
`orders pending` line of `_order_lines` names an order, not its agent). So the stack driver and
each open QA order with an agent id get the flag on their `activity stack` / `activity <O-k> qa`
line only (`activity` in `commands/activity.py`, its `_targets`), which only `status --refresh`
prints: the heartbeat's wake (`status --refresh --epoch <n>`) shows it for all three kinds, a
plain `status` for a CR's Driver only. The card's "Proof of death" (section 1) says so. Like
`_ended_unrecorded`: no flag on the Copilot host (`d.host == "copilot"`), none when no steering
transcript is recorded (`foreman_uuid` raises), and `status` writes no event for it.

A flag the CLI shows is a fact, not an order: the CLI knows no role and starts nothing, and it
counts nothing for it. The card (section 1) tells the steering session what to do on it.

The flag is in the `status` text only: no new `STATUS.json` field, so the CR board pane and the
web board do not change (no screenshot rule applies).

The reader must not slow `status` noticeably on a long steering transcript (the batch-22 Chief of
Staff session's transcript is 303 MB, 303,253,068 bytes, about 85,000 lines): the PR states the
time of a plain `status` and of `status --refresh` before and after the change, on a copy of a
transcript of that size (the batch-22 file itself or one padded to it), in two cases: a Driver
started after the transcript's last `task_status` record (the scan stops at its start), and a
Driver whose `killed` record is the last one.

### 3. Out of scope

- Workers (Coder, Verifier, Inspector...) stopped inside a Driver: the Driver's existing rule
  ("An agent that ends before its part is done") holds; the new Driver restarts them from the
  recorded state.
- Detecting an outside stop by any other sign than the two of Q4 (for example a Driver's
  transcript ending on a prompt with no answer): not detected.
- Making the CLI tell the steering session's own `TaskStop` from an outside stop (for example by
  reading `TaskStop` calls in the transcript): the card's cleared id does it.
- What causes the host to stop background agents at a compaction: not chantier's; the retro's
  separate point on handing a long batch's steering to a fresh session is another CR.
- `close --stopped` and the counting of the session's other subagents at `close`: another kept
  retro point, another CR.
- A pane, board or `STATUS.json` display of the flag.
- Any change to `take` or `agents set`: the restart path is today's commands.

## Evidence that proves it

- `scenario/run_scenario.py`, beside the existing `flagged` checks (around line 3774, the
  `chief`/`sub` transcripts of the activity part):
  - write an `attachment` record `{"type":"attachment","attachment":{"type":"task_status","taskId":"agent-<one>","status":"killed"}}`
    into the steering transcript (`chief`) and check that `status` flags `<one>` with `Driver
    agent-<one> stopped from outside, no hand-back recorded`, and not with `ended, no hand-back
    recorded`;
  - append a later `task_status` record for that agent with `status: "running"`, and check the
    flag is gone (the last record decides);
  - a `killed` record for another agent id flags nothing on `<one>`;
  - a `killed` record for `<one>` whose `timestamp` is older than `<one>`'s `agent` event flags
    nothing (the scan's bound);
  - `status` writes no event for the flag (events file unchanged);
  - after `agents set <one> - --epoch 1` the row shows `no Driver recorded` and no stopped flag
    (the cleared id of the steering session's own stop, and the restart path's first step), and
    `take <one> --note "resume: stopped from outside: x" --epoch 1` is accepted with no round
    counted (the existing restart check covers the take);
  - a second stop of the new Driver (a `killed` record for its new id, then the same restart)
    is accepted the same way, with no round counted and no block.
- `just check` passes; `just test` stays within its time limit.
- The long gate: the pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (a CLI
  and cards change), and the batch's top-of-stack local `just scenario` as the project's rules
  say.
- The PR's description quotes the batch-22 evidence above (agent ids, the refusal text, the
  `task_status` record) as the source of the host reference's new rows, and names the user's
  in-app stop as an unproved row with its trial (Q4), in its Known gaps.
