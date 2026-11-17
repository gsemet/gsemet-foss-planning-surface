# Change Specification: `close` judges only the batch's own agents

## Goal

`close` refused batch-22 until the user declared 13 subagents stopped (`--stopped`), though every
CR was merged and every batch agent had been cleared with `agents set <cr> -`: it read every
subagent transcript of the steering session tree (the Chief of Staff's grill, spec and critic
subagents, Drivers already replaced) and refused on each one that read as running. The user's
rule: closing must not need their word for agents chantier itself replaced. From now on only the
agents the batch recorded (`agents set`) and still holds can block `close`; the session's other
subagents are listed apart, as information, never as blockers, and need no word of the user.

## Decisions carried (from `02-answers.md`)

- close-agents-Q1: only the agents the batch recorded (`agents set`) and still holds block
  `close`; the session's other subagents (grill, spec, critics, Drivers already replaced) are
  listed apart, with no word of the user needed.
- It changes a CLI refusal (what blocks `close`): the spec critic reviews this specification.

## Definitions

- **A held agent:** an agent id the batch's record holds at the time of `close`, as `agents set`
  wrote it and no later `agents set <x> -` cleared it: each CR's `agent` (`CrEntry.agent`), each
  QA order's `agent` (`OrderRecord.agent`), and `stack_agent`. An id cleared with `-` is not held.
  A recorded `stack_agent` is also a record cause (`rails.py`, `running`): it always refuses,
  whatever its transcript reads, `--stopped` never passes it, and the way out is
  `agents set stack - --epoch <n>`.
  An id is matched to a transcript by the subagent file stem `agent-<id>.jsonl`; a recorded value
  that already starts with `agent-` matches the stem itself (the same two spellings `--stopped`
  takes today, see `_declared` in `rails.py`).
- **Another subagent:** any `subagents/agent-*.jsonl` of the steering sessions `close` reads
  today (`foreman_transcripts`, or `foreman_transcript`) whose stem is not a held agent's. A
  steering session also listed in `chief_sessions(d)` (a direct batch) only has its main file
  skipped; its subagents are read as for any steering session (`rails.py`, `running`;
  `costs/sessions.py`, `transcript_endings`). The scan is not widened: the Chief of Staff's
  sessions that are not steering sessions are not read.

## What changes

### CLI: `skills/chantier/scripts/cli/src/chantier/rails.py`

- `running(repo, d)` keeps its record causes unchanged: a CR not merged or cancelled, an open
  order, a recorded `stack_agent` (`stack agent <id> is recorded`). The Copilot branch (session
  file written in the last 5 minutes, or `not measured`) is unchanged.
- On Claude, the transcripts are split in two:
  - the held agents' transcripts: each is judged by `transcript_state` as today; `running` or
    `unreadable` is a cause and refuses, with the same cause text (`Ending.text()`: `transcript
    <session> agent-<id> still runs: <cause> (<path>)`, or `... cannot be read: <reason>
    (<path>)`);
  - every other subagent's transcript: never a cause. `close` reads its state only to list it
    apart (below).
  - the main transcripts of the Foreman sessions: see open question 1; until it is answered the
    Driver implements nothing on this point.
- `check_idle(repo, d, stopped)` refuses only on the record causes and the held agents' causes.
  `STOPPED_HINT` is appended only when a held agent reads as running and is not declared.
- `_declared` (`close --stopped NAME`): a name is accepted only when it is a held agent that reads
  as running. New refusal, exit 2, when the name is a subagent of the sessions that is not held:
  `close --stopped <name>: not an agent <batch> holds; it does not block close, drop the flag.
  Nothing was deleted.` The existing refusals keep their text, with the list after `still
  running:` now naming only the held agents that read as running: unknown name (`no transcript of
  <batch> by that name; still running: ...`), ended (`its transcript shows it ended; drop the
  flag`), cannot be read (`its transcript cannot be read (<path>), and the flag covers only an
  agent that reads as running`).
- Docstrings of `running`, `_declared`, `check_idle` say the new rule.

### CLI: `skills/chantier/scripts/cli/src/chantier/costs/sessions.py`

- `transcript_endings` (or a new reader beside it) gives what `rails.py` needs: the held agents'
  `Ending`s and the other subagents' `Ending`s, read once. The reader of one transcript
  (`transcript_state`) does not change. How the split is coded is the Driver's choice.

### CLI: `skills/chantier/scripts/cli/src/chantier/commands/closing.py`

- `close` (with and without `--yes`, on a paused batch that passes) prints, after the "declared
  stopped" lines and before the final cost, one line per other subagent whose transcript reads as
  running or cannot be read, under one heading line, for example:
  `not agents of <batch>, not judged (no word needed): <n>` then, per agent,
  `- transcript <session> agent-<id> still runs: <cause> (<path>)` (or `cannot be read: ...`).
  Other subagents that ended are not listed. When there are none, the heading is not printed. The
  exact wording is the Driver's, kept to these facts: the label, the state, the cause, the path.
- When `close` refuses (a held agent or a record cause), the refusal's message does not list the
  other subagents.
- Nothing about the other subagents is written to the record: `stopped_agents` in `batch-NN.json`
  and its line under Cost in `batch-NN.md` keep only the `--stopped` declarations, as today
  (`history.stopped_agents`, `history.close_markdown`, `close_archive.py`).
- `close`'s docstring says the new rule.

### CLI: `skills/chantier/scripts/cli/src/chantier/declare/closing.py`

- The `close` help: refused while anything of the batch runs (a held agent whose transcript shows
  it still runs, or that cannot be read); the session's other subagents are listed, never a block;
  `--stopped NAME` passes a held agent that stopped without its hand-back, on the user's word.
- The `--stopped` help: an agent the batch holds (`agents set`) whose transcript reads as running;
  it never passes a recorded stack agent, which always refuses: clear it with `agents set stack -`.

### Cards (`skills/chantier/references/`)

- `concepts.md`, the **Batch** entry (lines 169-176 today): `close` refuses on "an agent the batch
  holds (`agents set`, not cleared with `-`), whose transcript shows it still runs" instead of "an
  agent of the Foreman"; the session's other subagents (grill, spec, critics, Drivers already
  replaced) are listed apart and never block; `--stopped` takes only a held agent. The Foreman's
  own transcript: per open question 1.
- `chief-of-staff.md`, **Closing** (lines 1290-1315 today): the same rule; the listed other
  subagents need no question to the user and no `--stopped`; ask the user for `--stopped` only for
  a held agent the refusal names. **Recovery** (lines 1326-1332 today): state the rule once, for
  any Driver whose id was cleared with `agents set <cr> -` (an app restart, a Driver stopped from
  outside, a context restart): it is never a blocker at `close`, and needs no `--stopped`. Drop
  "that is the case for `close --stopped`" for those Drivers (the old Foreman's own session: per
  open question 1). The pending P1 CR `driver-resume-after-stop` edits the same bullet: whichever
  of the two merges second rebases onto the other's Recovery text and keeps both rules.
- `foreman.md` needs no change (line 26 stays true); the Driver checks it.
- No agent file (`agents/`, `com.github.copilot/agents/`) changes.

### Docs

- `docs/planning-folder.md` (lines 78-81), `docs/use-cases-foreman.md` (line 114),
  `docs/tutorial-claude-code.md` (line 190): "an agent whose transcript shows it still runs"
  becomes an agent of the batch (one it recorded and still holds); the session's other subagents
  are listed, not a block.
- `scenario/README.md` (lines 306-314): the close steps as below.

## Out of scope

- Copilot: its session-file rule (5 minutes, `not measured`) is unchanged; it has no per-agent
  reading.
- The reader of one transcript (`transcript_state`, what ends and what runs) is unchanged.
- The record causes (CR not merged or cancelled, open order, recorded stack agent) are unchanged.
- `pause`, `status` and the board are unchanged; the `ended, no hand-back recorded` row of
  `status` stays.
- No new command and no automatic clearing of a merged CR's `agent` at `order merged`.

## Evidence

- `just check` passes (Linux, macOS, Windows).
- The CLI changes: `just scenario` green on the pipeline's `just scenario (ubuntu-latest)` job at
  the PR's head, and locally on Windows per the project's rules when this CR is on top of the
  stack. No `hooks/` or `types/` change, so no `just mod`.
- Scenario, `close_refusals` and `close_batch` in `scenario/run_scenario.py` (the subagents under
  `uuid-foreman/subagents/`), each with and without `--yes` where it refuses:
  1. a held agent (a CR's `agent` set to its id) whose transcript reads as running refuses, naming
     it, its cause and its file, with the `--stopped` hint;
  2. the same transcript once the CR's agent is cleared (`agents set <cr> - --epoch <n>`, or the
     record edited the same way): `close` passes, prints the final cost, and lists the agent under
     the "not agents of the batch" heading with its cause and path; nothing is declared stopped
     and `stopped_agents` is absent from the record after `--yes`;
  3. a subagent never recorded (a grill or spec subagent) that reads as running, and one whose last
     line is cut JSON: neither refuses; both are listed apart;
  4. a held QA order agent (`O-k` done, `agent` still set) that reads as running refuses;
  5. `--stopped` of a held running agent passes it (stem and bare id), says "declared stopped" and
     keeps it in `stopped_agents` with `--yes`, as today;
  6. `--stopped` of a non-held subagent is refused with `not an agent <batch> holds`; of an
     unknown name, refused with `still running:` naming only held running agents; of a held ended
     agent and of a held unreadable one, refused as today;
  7. two held running agents with one declared: refuses on the other;
  8. a held agent's transcript cut JSON refuses as `cannot be read`, and `--stopped` does not
     pass it;
  9. the existing record-cause refusals (CR ready, open order, stack agent) and the Copilot steps
     still pass unchanged.
- `tests/`: no new test file is needed; if the Driver adds a check of the split, it goes in an
  existing parametrized test (`skills/chantier/scripts/cli/tests/test_transcript_end.py`), within
  the `just test` time bound.

## Open questions (for the Chief of Staff to take to the user)

1. **The Foreman's own transcript.** Today `close` also reads the main transcript of every Foreman
   session the batch recorded (`foreman_transcripts`), not only subagents: a Foreman whose last
   call waits on a tool refuses, and an earlier Foreman, replaced after an app restart, reads as
   running and needs `--stopped <session id>`. The Foreman is recorded by `foreman set`, not
   `agents set`. Should (a) the current Foreman's main transcript (the last recorded) still block
   while the earlier, replaced Foremans' are listed apart (recommended: the current one is the
   batch's own steering agent; replaced ones are what the user asked not to be asked about), (b)
   every Foreman session still block as today, or (c) none block?
2. **A held agent's own subagents.** A Driver may start subagents of its own (their `.meta.json`
   names the Driver as `parentAgentId`). When the held Driver's transcript has ended but one of its
   own subagents still reads as running, should that child (a) be listed apart, as the answer's
   literal rule says (recommended: the Driver that holds the CR has handed back), or (b) block as
   part of the held agent?
3. **A held agent with no transcript found.** A held id with no `agent-<id>.jsonl` in the sessions
   `close` reads (a Driver started from another session of the user's, or a mistyped id) would be
   judged as today's "the file is missing": `cannot be read`, refused, and `--stopped` does not
   pass it; the way out is `agents set <cr> - --epoch <n>`. Should it (a) refuse that way, with
   the refusal naming `agents set <cr> - --epoch <n>` (recommended: a held agent the CLI cannot
   read is not known to have ended), or (b) be listed apart and not block?
