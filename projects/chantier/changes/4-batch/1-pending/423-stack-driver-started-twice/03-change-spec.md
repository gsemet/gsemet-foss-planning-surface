# A Driver's only send to a Desktop Foreman is its final report

Change Specification, written 2026-11-20 from `intake/request.md` and `02-answers.md` (no
`01-intent.md`; the user asks no questions, the Chief of Staff settled the open points). No issue.
Priority P2. One batch CR, at most 3 rounds. Cards only: no CLI change, no agent file change.

## Goal

In the request's terms: a second stack Driver was started on a CR 25 minutes before the first
one's hand-back arrived, because the Foreman read the first one's silence as a lost Driver. On
Claude Desktop a subagent Driver cannot message its Foreman before its end: its hand-back reaches
the Foreman only as its final report. `hosts/claude-code.md` says the opposite ("`SendMessage` to
`main`", proved). Correct that row, write in a Driver's `Steering:` line what a subagent really
sends, and tell the Foreman what a Driver's silence means on this host, so that it does not start
a second Driver on silence.

## The facts this change writes down

- **Seen, Studio batch-06, 2026-11-20** (its retro,
  `projects/markdown-okf-schema-studio/changes/5-archives/batches/batch-06.md` in the planning
  surface, the `[chantier]` point): a subagent Driver cannot `SendMessage` a Claude Desktop
  Foreman session (id `local_…`); its hand-back reached the Foreman only as its final report; a
  second stack Driver was started 25 minutes before that report arrived. The host's exact text
  for the failed send was not recorded: the card must not quote one.
- **Already in `hosts/claude-code.md`, proved:** the host asks an ending subagent for its
  hand-back (`SubagentHandback`, batch-16); the report arrives in the steering session as a
  message with the notice `Agent "<name>" finished` (batch-18); `Agent "<name>" is waiting on its
  own background work` is not an end (batch-18); a steering session's `SendMessage` to a Driver's
  agent id reaches it and resumes it (batch-15, batch-18).
- **In the CLI, unchanged** (`skills/chantier/scripts/cli/src/chantier/commands/activity.py`,
  `activity()`): the `activity <cr>|stack|O-k qa` line of `status --refresh` gives the age of the
  most recent of the unit's last event and the last write of the session records of its own
  agents, or `gate running`, `gate queued`. A Driver that works, or that a message woke, writes
  its record, with no message to anyone.

## Decisions carried (02-answers.md)

Each is: Settled by the Chief of Staff (2026-11-20, the user asks no questions).

1. The row cites the Studio batch-06 retro and its date, and names the recording of the host's
   exact text as a trial.
2. The row and the `Steering:` text hold for every Driver (CR, stack, release, QA).
3. Foreman mode is the corrected case. Direct mode from Claude Desktop gets the same means,
   unproved. Direct mode from a terminal or VS Code keeps `SendMessage` to `main`, unproved.
4. A line due before the end (`anomaly`, `push`): an `anomaly` is a `$CHANTIER note` on its CR
   when it happens; every such line is in the final report, under the hand-back line.
5. The `ping`: no `pong` can come; the Foreman still pings a suspect and reads the proof of life
   in the `activity` age at the next wake. Unproved, with its trial.
6. Host facts in `hosts/claude-code.md` only; two short pointers in the generic cards
   (`foreman.md`, `driver.md`), with no host tool named.
7. No CLI change: the skeleton's `Steering:` placeholder and the row's label stay.
8. No agent file change on either host.
9. `hosts/copilot.md` unchanged.
10. No new refusal of a second stack driver.

## What changes

### 1. `skills/chantier/references/hosts/claude-code.md`, "Tools": the row

The row `A Driver messages its steering session (the Foreman; in direct mode the Chief of Staff,
which is `main` there)` (today: `SendMessage` to `main`, "proved, same; in direct mode the same
mechanism, unproved until a direct batch runs"). **Keep its first cell's opening words `A Driver
messages its steering session` unchanged**: the CLI's skeleton names the row by them
(`driver_prompt.py`, `driver_prompt_lines`). Rewrite its two other cells to say:

- **The means, for a steering session of Claude Desktop (a session id `local_…`: every Foreman,
  and the Chief of Staff of a direct batch run from Claude Desktop):** the Driver's final report
  only, the host's hand-back (`SubagentHandback`), once, at its end. Before its end a background
  subagent has no means to reach that session: `SendMessage` to `main` does not reach it.
- **The `Steering:` line, written out** (what the parent copies into each Driver's prompt, with
  its own session id and "the Chief of Staff" in place of "the Foreman" in a direct batch). The
  wording may be tightened; every element is required:

  ```text
  Steering: the Foreman (session <id>, for the record). Nothing reaches it before your end: send no message. Your one send is your final report (the host's hand-back): its first line is your hand-back line, then every other line due (`anomaly`, `push`), one per line, as the cards word them. Record an `anomaly` when it happens: `$CHANTIER note <cr> "anomaly: <text>"`. A `ping` needs no answer: go on.
  ```

- **The means, for a direct batch run from a terminal or VS Code:** `SendMessage` to `main`, and
  the `Steering:` line names it.
- **The mark.** Foreman mode: the final report as the hand-back's route is proved (batch-16,
  batch-18, the rows below it); that no message reaches a Desktop Foreman before it: seen,
  Studio's batch-06, 2026-11-20 (its retro), the host's exact text not recorded. Trial: in the
  next Foreman batch, a Driver's transcript shows what a `SendMessage` to `main` returns; record
  the text and the date. The former "proved, same" is removed. Direct mode from Claude Desktop:
  unproved, same trial in a direct batch. Direct mode from a terminal: unproved; trial: the first
  direct batch run there, a Driver's `anomaly` line arriving before its hand-back.

Leave the rows `Message a Driver`, `Message the Chief of Staff`, `Resume a stopped subagent`, the
allow rules (`SendMessage` stays: the Foreman messages its Drivers and the Chief of Staff) and
the "Limit on messages" paragraph as they are.

### 2. `skills/chantier/references/hosts/claude-code.md`: a new section, "A Driver's silence"

A short section (place it after "The Foreman's turn-end notice", or as rows under "Surfaces and
options" next to `A background subagent stops`; the Driver chooses the place that reads best),
for the steering session, saying:

- Between its start and its final report a Driver sends nothing to a Claude Desktop steering
  session. Silence is no sign of a lost Driver, however long, and no reason to start another.
- A Driver's life is read from two things only: the `activity` line of `$CHANTIER status
  --refresh` (an age, `gate running`, `gate queued`), and the host's notices (the rows `A
  background subagent stops` and `A background subagent is stopped from outside`). `Agent
  "<name>" is waiting on its own background work` is not an end.
- An `anomaly` comes as a note on the CR (`$CHANTIER status --notes`) and again in the Driver's
  final report; handle it when the report arrives, as the card says for the line.
- **The `ping`.** No `pong` can come. A `ping` to a suspect is still sent (it wakes a waiting
  Driver). At the next wake, the proof of life is that unit's `activity` age, younger than the
  ping. An age older than the ping, with no `gate running` and no `gate queued`, is the missing
  `pong` of `foreman.md`'s proof of death. **Unproved**; trial: in a Foreman batch, ping a
  Driver that waits on its own background work, and read at the next `status --refresh` an
  `activity` age younger than the ping; record the batch and the date.
- A second Driver for a unit (a CR, the stack, a QA order) is started only by the restart path
  of `foreman.md`, after one of its proofs of death or the first one's final report: never on
  silence alone. For the stack: `agents set stack -` only once the stack driver's report arrived
  or a proof of death holds.
- One line of where it was seen: Studio's batch-06, 2026-11-20, a second stack Driver started 25
  minutes before the first one's hand-back arrived.

### 3. `skills/chantier/references/foreman.md`, "A lost Driver", "Proof of death"

One pointer, no host tool named. In the second proof (`a [foreman→driver <cr>] ping to a suspect
gets no pong by the next wake`), add that on a host whose reference says a Driver cannot answer
before its end, the sign that reference names stands in place of the `pong` (for Claude Code:
[its reference](hosts/claude-code.md), "A Driver's silence", linked as the card links its host's
reference elsewhere). Nothing else in "A lost Driver" changes: "Suspect", "A `pong` proves a
Driver alive, not that it moves" (the 3 hours with no new round, head or note), the restart path
and "A silent end" stay.

### 4. `skills/chantier/references/driver.md`, the `ping` answer

In the bullet of the Foreman's lines (`ping`: `[driver <cr>→foreman] pong <step>`), add: when
the `Steering:` line says nothing reaches the steering session before the Driver's end, a `ping`
gets no answer and the Driver goes on. The card's opening already says every line goes by the
`Steering:` line; no other line of `driver.md` changes (the stack driver's `anomaly … sent
before the hand-back` is then the note and the report line, by its `Steering:` line).

### 5. Checks on the other cards

`concepts.md` ("A Driver's prompt holds the `Steering:` line … written out as that reference
says it") and `routing.md` (the line names) stay true and are not changed. The Driver reads both
after its edits and changes a sentence only where it has become false.

## Out of scope

- The CLI (`driver_prompt.py`, `take stack`, the lease, `status`): no change, no new refusal.
- `agents/*.md` and `com.github.copilot/agents/*.agent.md`: no change; their bodies stay
  identical.
- `hosts/copilot.md`.
- The Studio project's own batch record.
- A new means for a Driver to send before its end (a file, a journal line): none is added.

## Host matrix

One line per cell; no shipped default or configured value is involved.

- Claude Code, Foreman mode (the Foreman is a Claude Desktop `local_` session): the final report
  only; seen, Studio batch-06, 2026-11-20; the host's text to record (trial above).
- Claude Code, direct mode from Claude Desktop: the same means; unproved.
- Claude Code, direct mode from a terminal or VS Code: `SendMessage` to `main`; unproved.
- Copilot: unchanged (its row: the Driver's final answer).

## Evidence

No test is added: the change is card text, and the tests stay few. The Verifier reads the shipped
files from the repository at the head under test (not a copy):

1. `skills/chantier/references/hosts/claude-code.md` holds one row whose first cell starts `A
   Driver messages its steering session`; that row no longer reads "proved, same" for
   `SendMessage` to `main`, names the final report, cites Studio's batch-06 with its date, and
   holds the `Steering:` text with its five elements (nothing before the end; the final report;
   the hand-back line first; an `anomaly` as a note; no answer to a `ping`).
2. The same file holds "A Driver's silence" with its six points, the `ping` point marked
   unproved with its trial.
3. `foreman.md`'s proof of death and `driver.md`'s `ping` bullet hold their pointer; neither
   names a host tool.
4. A prompt check, on a prepared batch: `take stack --note why --epoch <n>` still prints `
   Steering: the Foreman <the host's means, from its reference's row "A Driver messages its
   steering session">`, and the row it names exists under that label (the existing
   `test_driver_prompt.py` covers the printed line; it is not changed).
5. `just check` passes in the worktree at the pushed head; among its tests,
   `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` and the allow-rules test of
   `test_cli_runs.py` (both read the shipped cards).

What only a real batch proves, and is named in the PR's Known gaps: the host's exact text for a
Driver's `SendMessage` to `main` under a Desktop Foreman, and the `ping` read by the `activity`
age.

## Gates (the project's `AGENTS.md`)

- `just check` in the worktree at the rebased head, before the first push.
- Cards only: no `just eval-dry-run`, no `just mod`.
- The long gate: the pipeline's `just scenario (ubuntu-latest)` job green at the PR's head (a
  change to the cards); the local `just scenario` only when this CR is on top of the stack.
- Repository text in English.

## Open questions

None: the user asks no questions (2026-11-20); the ten points are settled in `02-answers.md`.
