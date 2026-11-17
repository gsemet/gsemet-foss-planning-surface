# Change Specification: `close` judges only the batch's own agents

## Goal

`close` refused batch-22 until the user declared 13 subagents stopped (`--stopped`), though every
CR was merged and every batch agent had been cleared with `agents set <cr> -`: it read every
subagent transcript of the steering session tree (the Chief of Staff's grill, spec and critic
subagents, Drivers already replaced) and refused on each one that read as running. The user's
rule: closing must not need their word for agents chantier itself replaced. From now on only the
agents the batch recorded and still holds (each `agents set` id not cleared, and the current
Foreman) can block `close`; the session's other subagents and the replaced Foremans are listed
apart, as information, never as blockers, and need no word of the user.

## Decisions carried (from `02-answers.md`)

- close-agents-Q1: only the agents the batch recorded (`agents set`) and still holds block
  `close`; the session's other subagents (grill, spec, critics, Drivers already replaced) are
  listed apart, with no word of the user needed. It changes a CLI refusal (what blocks `close`):
  the spec critic reviews this specification.
- close-agents-Q2: the current Foreman's main transcript (the last recorded) still blocks; the
  earlier, replaced Foremans' main transcripts are listed apart.
- close-agents-Q3: a held Driver's own subagents are listed apart when the Driver has ended.
- close-agents-Q4: a held agent with no transcript found is refused as `cannot be read`, the
  refusal naming `agents set <cr> - --epoch <n>` as the way out.
- close-agents-Q5: the cards say the steering session offers or runs `close` only after its retro
  critic has handed back; the CLI does not change for it (the pending `auto-pause-last-merge`
  follows the same line).
- close-agents-Q6: when other subagents are listed at a passing `close`, the heading line says
  these agents' calls are counted only up to now in the final cost.
- close-agents-Q7: only the other subagents still running or unreadable are listed; ended ones are
  not listed.

## Definitions

- **The steering sessions:** the sessions `close` reads today: `foreman_transcripts` (or the
  single `foreman_transcript`), in their recorded order. The scan is not widened: the Chief of
  Staff's sessions that are not steering sessions are not read. A steering session also listed in
  `chief_sessions(d)` (a direct batch) only has its main file skipped, as today; its subagents are
  read as for any steering session (`rails.py`, `running`; `costs/sessions.py`,
  `transcript_endings`).
- **The current Foreman:** the last session of `foreman_transcripts` (or `foreman_transcript`).
  Its main transcript is held (close-agents-Q2), unless its main file is skipped as a Chief of
  Staff session (direct batch), as today. Every earlier session of the list is a **replaced
  Foreman**: its main transcript is never a cause, and is listed apart (below).
- **A held agent:** the current Foreman (its main transcript), and each agent id the batch's
  record holds at the time of `close`, as `agents set` wrote it and no later `agents set <x> -`
  cleared it: each CR's `agent` (`CrEntry.agent`), each QA order's `agent` (`OrderRecord.agent`),
  and `stack_agent`. An id cleared with `-` is not held. A recorded `stack_agent` is also a
  record cause (`rails.py`, `running`): it always refuses, whatever its transcript reads,
  `--stopped` never passes it, and the way out is `agents set stack - --epoch <n>`.
  An id is matched to a transcript by the subagent file stem `agent-<id>.jsonl` under any
  steering session's `subagents/`; a recorded value that already starts with `agent-` matches the
  stem itself (the same two spellings `--stopped` takes today, see `_declared` in `rails.py`).
- **Another transcript:** any `subagents/agent-*.jsonl` of the steering sessions whose stem is not
  a held agent's, and the main transcript of each replaced Foreman. A held Driver's own subagents
  (their `.meta.json` naming the Driver as `parentAgentId`) are other transcripts too
  (close-agents-Q3): never a cause by themselves; when the Driver has ended they are listed apart,
  and while it still runs the Driver itself refuses.

## What changes

### CLI: `skills/chantier/scripts/cli/src/chantier/rails.py`

- `running(repo, d)` keeps its record causes unchanged: a CR not merged or cancelled, an open
  order, a recorded `stack_agent` (`stack agent <id> is recorded`). The Copilot branch (session
  file written in the last 5 minutes, or `not measured`) is unchanged.
- On Claude, the transcripts are split in two:
  - the held agents' transcripts (the current Foreman's main one and each held id's): each is
    judged by `transcript_state` as today; `running` or `unreadable` is a cause and refuses, with
    the same cause text (`Ending.text()`: `transcript <session> agent-<id> still runs: <cause>
    (<path>)`, `transcript <session> still runs: ...` for the Foreman, or `... cannot be read:
    <reason> (<path>)`);
  - a held id (a CR's or a QA order's `agent`) with no `agent-<id>.jsonl` under any steering
    session's `subagents/` (a Driver started from another session of the user's, a mistyped id) is
    a held agent that cannot be read (close-agents-Q4): it refuses as `cannot be read`, and its
    cause names the way out, for example `transcript of agent-<id> (<cr>) cannot be read: no
    transcript found; if it is not running, clear it: agents set <cr> - --epoch <n>` (`<cr>` the
    CR's slug or the order's `O-k`; `<n>` stays a placeholder). The exact wording is the
    Driver's, kept to these facts. A recorded stack agent stays a record cause only;
  - every other transcript: never a cause. `close` reads its state only to list it apart
    (below).
- `check_idle(repo, d, stopped)` refuses only on the record causes and the held agents' causes.
  `STOPPED_HINT` is appended only when a held agent reads as running and is not declared.
- `_declared` (`close --stopped NAME`): a name is accepted only when it is a held agent that reads
  as running: a held id (stem or bare id) or the current Foreman's session id. New refusal, exit
  2, when the name is another transcript (a subagent that is not held, or a replaced Foreman's
  session id): `close --stopped <name>: not an agent <batch> holds; it does not block close, drop
  the flag. Nothing was deleted.` The existing refusals keep their text, with the list after
  `still running:` now naming only the held agents that read as running: unknown name (`no
  transcript of <batch> by that name; still running: ...`), ended (`its transcript shows it ended;
  drop the flag`), cannot be read (`its transcript cannot be read (<path>), and the flag covers
  only an agent that reads as running`); a held id with no transcript is refused as cannot be
  read.
- Docstrings of `running`, `_declared`, `check_idle` say the new rule.

### CLI: `skills/chantier/scripts/cli/src/chantier/costs/sessions.py`

- `transcript_endings` (or a new reader beside it) gives what `rails.py` needs: the held agents'
  `Ending`s (with a missing held id as `unreadable`) and the other transcripts' `Ending`s, read
  once. The reader of one transcript (`transcript_state`) does not change. How the split is coded
  is the Driver's choice.

### CLI: `skills/chantier/scripts/cli/src/chantier/commands/closing.py`

- `close` (with and without `--yes`, on a paused batch that passes) prints, after the "declared
  stopped" lines and before the final cost, one line per other transcript that reads as running or
  cannot be read (close-agents-Q7), under one heading line that says they are not judged, need no
  word, and that their calls are counted only up to now (close-agents-Q6), for example:
  `not agents of <batch>, not judged (no word needed; their calls are counted only up to now): <n>`
  then, per transcript,
  `- transcript <session> agent-<id> still runs: <cause> (<path>)` (or `cannot be read: ...`; a
  replaced Foreman as `transcript <session> ...`).
  Other transcripts that ended are not listed. When there are none, the heading is not printed.
  The exact wording is the Driver's, kept to these facts: the label, the state, the cause, the
  path, and the heading's three points.
- When `close` refuses (a held agent or a record cause), the refusal's message does not list the
  other transcripts.
- Nothing about the other transcripts is written to the record: `stopped_agents` in
  `batch-NN.json` and its line under Cost in `batch-NN.md` keep only the `--stopped` declarations,
  as today (`history.stopped_agents`, `history.close_markdown`, `close_archive.py`). The pricing
  is unchanged: it counts what the transcripts hold at the time of `close`.
- `close`'s docstring says the new rule.

### CLI: `skills/chantier/scripts/cli/src/chantier/declare/closing.py`

- The `close` help: refused while anything of the batch runs (a held agent, the current Foreman
  included, whose transcript shows it still runs, or that cannot be read); the session's other
  subagents and replaced Foremans are listed, never a block; `--stopped NAME` passes a held agent
  that stopped without its hand-back, on the user's word.
- The `--stopped` help: an agent the batch holds (`agents set`, or the current Foreman's session
  id) whose transcript reads as running; it never passes a recorded stack agent, which always
  refuses: clear it with `agents set stack -`.

### Cards (`skills/chantier/references/`)

- `concepts.md`, the **Batch** entry (lines 169-176 today): `close` refuses on "an agent the batch
  holds (`agents set`, not cleared with `-`, or the current Foreman), whose transcript shows it
  still runs or cannot be read" instead of "an agent of the Foreman"; a held id with no transcript
  cannot be read, and the way out is `agents set <cr> - --epoch <n>`; the session's other
  subagents (grill, spec, critics, Drivers already replaced, a Driver's own subagents) and the
  replaced Foremans are listed apart when still running or unreadable, and never block;
  `--stopped` takes only a held agent. The steering session offers or runs `close` only after its
  retro critic has handed back (close-agents-Q5).
- `chief-of-staff.md`, **Closing** (lines 1290-1322 today):
  - the same rule for what refuses; the listed other transcripts need no question to the user and
    no `--stopped`; ask the user for `--stopped` only for a held agent the refusal names (its
    `agent-<id>` stem, or the current Foreman's session id); drop "or an earlier Foreman's session
    id" from the names `--stopped` takes;
  - a held agent the refusal says cannot be read with no transcript found: tell the user, and
    clear it with `agents set <cr> - --epoch <n>` only once it is known not to run (a Driver of
    another session of the user's: on the user's word); never `--stopped`;
  - close-agents-Q5: offer or run `close` (the check or `--yes`) only after the steering
    session's retro critic has handed back: in Foreman mode after the Foreman's `final` (which
    comes after its critic's reply, `foreman.md`); in direct mode after your own retro critic of
    the pause has handed back. A retro critic still running is not judged by `close`, so this
    card rule is what keeps its calls in the final cost.
- `chief-of-staff.md`, **Recovery** (lines 1323-1332 today): state the rule once, for any Driver
  whose id was cleared with `agents set <cr> -` (an app restart, a Driver stopped from outside, a
  context restart) and for a Foreman replaced by a new one: it is never a blocker at `close`, and
  needs no `--stopped`. Drop "that is the case for `close --stopped`" for those Drivers and for the
  old Foreman's own session. The pending P1 CR `driver-resume-after-stop` edits the same bullet:
  whichever of the two merges second rebases onto the other's Recovery text and keeps both rules.
- The pending P1 CR `auto-pause-last-merge` edits the same Closing and "The pause" text, and says
  "the close is offered after `final`, never before (the Foreman's retro critic must have ended
  for `close` to pass)". Whichever of the two merges second keeps both: the close offered after
  `final`, and, from this CR, the reason given as the card's rule (the retro critic must have
  handed back), since a running retro critic no longer refuses `close`.
- `foreman.md` needs no change (line 26 and "The retro critic", which waits for the critic's
  reply before `pause` and `final`, stay true); the Driver checks it.
- No agent file (`agents/`, `com.github.copilot/agents/`) changes.

### Docs

- `docs/planning-folder.md` (lines 78-81), `docs/use-cases-foreman.md` (line 114),
  `docs/tutorial-claude-code.md` (line 190): "an agent whose transcript shows it still runs"
  becomes an agent of the batch (one it recorded and still holds, or the current Foreman); the
  session's other subagents and replaced Foremans are listed, not a block.
- `scenario/README.md` (lines 306-314): the close steps as below.

## Out of scope

- Copilot: its session-file rule (5 minutes, `not measured`) is unchanged; it has no per-agent
  reading.
- The reader of one transcript (`transcript_state`, what ends and what runs) is unchanged.
- The record causes (CR not merged or cancelled, open order, recorded stack agent) are unchanged.
- The "no Foreman transcript recorded" and "nothing priced" refusals are unchanged.
- The CLI does not detect a running retro critic (close-agents-Q5): it is another transcript like
  any.
- `pause`, `status` and the board are unchanged; the `ended, no hand-back recorded` row of
  `status` stays.
- No new command and no automatic clearing of a merged CR's `agent` at `order merged`.

## Evidence

- `just check` passes (Linux, macOS, Windows).
- The CLI changes: `just scenario` green on the pipeline's `just scenario (ubuntu-latest)` job at
  the PR's head, and locally on Windows per the project's rules when this CR is on top of the
  stack. No `hooks/` or `types/` change, so no `just mod`.
- Scenario, `close_refusals` and `close_batch` in `scenario/run_scenario.py` (the subagents under
  `uuid-foreman/subagents/`; the steps that use `--stopped` today on unrecorded subagents first
  record them with `agents set`), each with and without `--yes` where it refuses:
  1. a held agent (a CR's `agent` set to its id) whose transcript reads as running refuses, naming
     it, its cause and its file, with the `--stopped` hint;
  2. the same transcript once the CR's agent is cleared (`agents set <cr> - --epoch <n>`, or the
     record edited the same way): `close` passes, prints the final cost, and lists the agent under
     the heading, which says they are not judged and their calls are counted only up to now;
     nothing is declared stopped and `stopped_agents` is absent from the record after `--yes`;
  3. a subagent never recorded (a grill or spec subagent) that reads as running, and one whose last
     line is cut JSON: neither refuses; both are listed apart; an ended unrecorded subagent is not
     listed, and with only ended ones the heading is not printed;
  4. a held QA order agent (`O-k` done, `agent` still set) that reads as running refuses;
  5. the current Foreman's main transcript (the last of two recorded, `foreman transcript` run
     twice) reading as running refuses; the earlier Foreman's main transcript reading as running
     does not refuse and is listed apart; `--stopped <earlier session id>` is refused with `not an
     agent <batch> holds`; `--stopped <current session id>` passes the current one;
  6. a held Driver whose transcript ended, with one subagent of its own (`.meta.json` naming it as
     `parentAgentId`) reading as running: `close` passes and lists the child apart;
  7. a held id with no transcript file refuses as `cannot be read`, its cause naming `agents set
     <cr> - --epoch <n>`; `--stopped` of that id is refused; after `agents set <cr> -` it passes;
  8. `--stopped` of a held running agent passes it (stem and bare id), says "declared stopped" and
     keeps it in `stopped_agents` with `--yes`, as today;
  9. `--stopped` of a non-held subagent is refused with `not an agent <batch> holds`; of an
     unknown name, refused with `still running:` naming only held running agents; of a held ended
     agent and of a held unreadable one, refused as today;
  10. two held running agents with one declared: refuses on the other;
  11. a held agent's transcript cut JSON refuses as `cannot be read`, and `--stopped` does not
      pass it;
  12. the existing record-cause refusals (CR ready, open order, stack agent) and the Copilot steps
      still pass unchanged.
- `tests/`: no new test file is needed; if the Driver adds a check of the split, it goes in an
  existing parametrized test (`skills/chantier/scripts/cli/tests/test_transcript_end.py`), within
  the `just test` time bound.

## Open questions

None.
