# close sees a finished agent as finished

Short name: `close-finished`

## Goal

`chantier close` tells whether an agent of the batch still runs by reading the end of its
transcript, not by the age of the file. An agent that has handed back is finished, even if its
file was written a second ago. An agent waiting on a tool call is running, even if its file has
not changed for an hour. `close` refuses only when an agent still runs or its transcript cannot be
read, and it names that agent and file.

Some agents stop without handing back: an app restart cuts them mid-step, or the user stops them.
Their transcripts read as running forever. For those, `close` takes the user's word: the Chief of
Staff asks the user, and on their yes passes a flag that names those agents as stopped. The flag
is recorded in the batch's record. `close` never guesses from a file's age.

The user's word, 2026-11-15: read the transcript rather than wait 5 minutes; ask the agent only as
a last resort (a finished subagent cannot be messaged, and the CLI messages no agent).

Why: in both of batch-18's real eval runs of 2026-11-15, `close` refused 4 times because of agents
that had already handed back. The waits added up to 530 s, and run 2's final cost rose from $11.47
to $11.91 because the prompt cache expired while it waited. The 5-minute rule also misses a silent
tool call that lasts longer than 5 minutes. Evidence: all 94 finished agent transcripts of the two
runs end with the hand-back and its result (audits:
`C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md`,
`real-direct-2026-11-15.audit.md`).

## What changes

### 1. The CLI: `running()` reads each transcript's end (`skills/chantier/scripts/cli/src/chantier/rails.py`)

- Remove the age test on Claude transcripts from `running()`. The record-based causes stay
  unchanged and come first: a CR not merged or cancelled, an open order, a recorded stack agent.
- For the session files, `running()` asks a new reader for each transcript's state, in place of
  `idle_seconds()`. It reads the same set of files as today, chosen by the same rules:
  - The Foreman's transcript(s): `d.foreman_transcripts`, else `d.foreman_transcript`.
  - Every `subagents/agent-*.jsonl` beside each of those transcripts, whatever the agent's type.
  - On a direct batch, the Chief of Staff's own main transcript stays skipped (`chief_sessions(d)`,
    the `own` argument of today), and its subagents are still read.
  - A Driver started from another session of the user's is still not seen.
- Place the reader in `skills/chantier/scripts/cli/src/chantier/costs/sessions.py`, beside
  `idle_seconds()`. Write it as a function of its own: a later CR uses the same reader to detect
  "a Driver ended with no recorded hand-back" (see Out of scope). For each transcript it returns:
  the label (session and agent), the agent's name as the flag accepts it (section 4), the file's
  path, and one state. The state is ended, still running (with its cause) or cannot be read (with
  its reason).
- `idle_seconds()` stays as it is: `commands/activity.py` (`status --refresh`'s activity lines)
  still uses it, and its behaviour does not change.

### 2. The rule: when a Claude transcript shows the agent has ended

Only the `user` and `assistant` records count. Skip every other record type: Claude Code writes
records such as `api-request`, `api-request-blob` and `attachment` after or between them. The
transcript shows the agent has **ended** when its last `user`/`assistant` record is one of these:

- (a) **The hand-back and its result.** A `user` record holds the `tool_result` of the
  transcript's last `tool_use`, and that `tool_use` is the host's hand-back tool
  (`SubagentHandback` on Claude Code). This is a subagent's end, as the 94 transcripts show.
- (b) **A turn ended with no tool call.** An `assistant` record has no `tool_use` block and its
  `message.stop_reason` is `end_turn` or `stop_sequence`. This covers a subagent that ends with a
  plain final message, and a steering session (the Foreman) that is idle between turns or after
  its loop stopped.

Anything else means the agent **still runs**, whatever the file's age. Each case has its own cause
line:

- An `assistant` `tool_use` with no `tool_result` yet: the agent waits on a tool. This is how the
  new rule catches the silent tool call that lasts longer than 5 minutes.
- The last record is a `user` record (a tool's result other than the hand-back's, or a prompt) with
  no `assistant` record after it: the model is producing its next step.
- An `assistant` record whose `stop_reason` is `tool_use`, null, or any other value than the two
  above.

An agent cut by an app restart, or stopped by the user, also reads as still running. Only the
user's word (section 4) passes it.

A transcript **cannot be read** in these cases, and each one refuses:

- the file is missing (today this reads `not measured`);
- the file cannot be opened or decoded (an OSError or UnicodeError);
- the last non-empty line is not complete JSON;
- the file holds no `user`/`assistant` record at all.

The flag does not pass a transcript that cannot be read.

Before you settle on the rule, check it against real transcripts, read-only: the user's
`~/.claude/projects/<slug>/<session>.jsonl` and `.../subagents/agent-*.jsonl`. Every finished
subagent must read as ended, and a subagent caught mid-run must read as running. A tally of this
project's older transcripts gives these `stop_reason` values: `tool_use`, `end_turn`,
`stop_sequence`, and a few `null`.

### 3. The refusal

The refusal keeps its frame: `cannot close <batch>, something still runs: <causes>. Nothing was
deleted.` (exit 2, `EXIT_PRECONDITION`, from `check_idle()`). Each session cause names the session,
the agent (the name the flag takes) and the file's path. Replace the old cause `... was written N s
ago (under 5 min)` with one of these:

- `transcript <session> agent-<id> still runs: its tool call <ToolName> has no result yet (<path>)`
- `transcript <session> agent-<id> still runs: its last record is <a tool's result | a prompt>
  with no answer yet (<path>)`
- `transcript <session> agent-<id> still runs: its last call stopped on <stop_reason> (<path>)`
- `transcript <session> agent-<id> cannot be read: <reason> (<path>)`

For the Foreman's own transcript, the agent part is left out (`transcript <session> ...`), as
today.

When at least one cause is "still runs", the refusal ends with one more sentence: `an agent stopped
without its hand-back (an app restart, the user's stop) passes only on the user's word: close
--stopped <name> for each`. The exact wording is the Driver's. What each cause must carry: the
session, the agent's name, the file's path, and why the CLI judges that it runs or cannot be read.

### 4. The way out: `close --stopped <name>`, on the user's yes

Declare the flag in `skills/chantier/scripts/cli/src/chantier/declare/closing.py`:

```
--stopped NAME   (repeatable) an agent the user declares stopped: its transcript reads as running
                 but it ended without its hand-back; on the user's word only
```

How it behaves:

- **What a name is.**
  - A subagent's file stem (`agent-<id>`). The bare `<id>` resolves to the same agent.
  - A main transcript's session id (an earlier Foreman's `<uuid>`, after an app restart).
  - The name must be one that the same run's check reads as **still runs**.
- **What it passes.** Each named agent drops out of the session causes. Every other cause still
  refuses: the record causes, other agents that still run, any transcript that cannot be read. It
  works on both callers of `check_idle()` (`close`, and `_close_target()` on a batch that is not
  paused). There, once nothing else runs, the "`pause --epoch <n>` comes first" refusal follows as
  today.
- **Refusals.** Each one exits 2 (`EXIT_PRECONDITION`), comes with or without `--yes`, and ends
  with "Nothing was deleted."
  - A name that matches no transcript of the batch: `close --stopped <name>: no transcript of
    <batch> by that name; still running: <names, or none>`.
  - A name whose transcript reads as ended: `close --stopped <name>: its transcript shows it ended;
    drop the flag`.
  - A name whose transcript cannot be read: `close --stopped <name>: its transcript cannot be read
    (<path>), and the flag covers only an agent that reads as running`.
- **Without `--yes`** (the check). Nothing is written, as today. The preview adds one line per
  declared agent before the cost lines: `declared stopped on the user's word: <name>: <its cause>
  (<path>)`.
- **With `--yes`.** The declaration is recorded in the batch's record, the part that outlives
  `close`. The batch's `events.jsonl` is one of the batch's own files that `close --yes` deletes, so
  an event appended there would be deleted in the same command. The record gets the declaration as
  follows:
  - `5-archives/batches/batch-NN.json` (`history.close_record()`): a `stopped_agents` list, one
    entry per agent: `{"agent": <name>, "transcript": <path as the CLI read it>, "cause": <the
    still-runs cause>, "declared": <the close time>}`. The key is present only when the flag was
    given.
  - `5-archives/batches/batch-NN.md` (`history.close_markdown()`): under `## Cost`, a line
    `- Declared stopped on the user's word: <name> (<cause>)` for each agent. This is the batch's
    log of the declaration.
  - The `closed ...` output of `close --yes` repeats the same lines.
- The CLI cannot tell whether the user said yes: the card carries that rule (section 6). The CLI
  only refuses a name that the check does not read as running.

### 5. Copilot

The user's decision: Copilot's session file (`events.jsonl`) keeps today's rule. That is the
file's modification time with the 5-minute bound, and `not measured` when the file is missing.
Reading the end of Copilot's `events.jsonl` is a later inbox item. Keep the 300-second constant
for Copilot only: move it next to the Copilot branch, under a name that says it is Copilot's.
`--stopped` does not apply to a Copilot session: a Copilot cause is never "still runs" in this
CR's sense. A name given on a Copilot batch is refused by the "no transcript by that name" rule.

### 6. The cards and docs

- `skills/chantier/references/chief-of-staff.md`, **Closing** (lines 1265-1283):
  - Replace the 5-minute cause with these causes: an agent of the Foreman, or the Foreman itself,
    whose transcript shows it still runs (a tool call with no result, or a step under way); a
    transcript that cannot be read; on Copilot, a session file written in the last 5 minutes
    (`not measured` refuses).
  - Add the way out. When the refusal names an agent that still runs, wait for that agent's
    hand-back (its notification), then run `close` again, never on a timer. When you know the
    agent will not hand back, or the user says so, ask the user. Ways to know: an app restart cut
    it, the user stopped it, or its hand-back already reached you while its transcript reads as
    running. In the question, quote each agent's name, cause and file, as the refusal gives them.
    Ask the agent itself only as a last resort: a finished subagent cannot be messaged.
  - On the user's yes, in that turn, run `close --batch <batch> --stopped <name> ...` (the check).
    Show the bilan with the "declared stopped" lines, and ask for the close as today. On that
    second yes, run `close --batch <batch> --stopped <name> ... --yes`. Never pass `--stopped`
    without the user's yes for each named agent, and never to get past a transcript that cannot be
    read.
  - "Report a refusal to the user with its cause, do not retry in a loop" stays.
- **Recovery** in the same card (around line 1287), the app-restart path. Add one line: the old
  Foreman's session and its Drivers stay in the batch's transcripts and will read as running at
  `close`. That is the case for `--stopped`, on the user's yes.
- `skills/chantier/references/concepts.md`, **Batch** (around line 160): replace the 5-minute
  clause with the same causes as the Closing card. Add: "an agent that stopped without its
  hand-back passes only on the user's word (`close --stopped <name>`), recorded in the batch's
  record".
- `docs/planning-folder.md`, lines 79-80: replace "a session written in the last 5 minutes" with
  "an agent whose transcript shows it still runs (one that stopped without handing back passes on
  your word, and the batch's record keeps it)".
- `docs/tutorial-claude-code.md` (line 190) and `docs/use-cases-foreman.md` (line 114): add half a
  sentence saying an agent stopped without handing back passes on the user's word.
- `scenario/README.md`, lines 282-284: rewrite the closing bullet to list the new steps (Evidence).
- The docstrings of `running()`, `check_idle()`, `close()` and the new reader state the rule in
  section 2 and the flag in section 4. The command's help in `declare/closing.py` names
  `--stopped`.

No agent file changes (`agents/`, `com.github.copilot/agents/`): the role's contract is in the
cards. No `hooks/` or `types/` change, so `just mod` is not needed.

## Decisions carried from `02-answers.md`

1. The request's scope stands as written: `close` judges by the transcript's end. It refuses only
   when an agent still runs or its transcript cannot be read, naming the file. The CR is planned
   in the next batch, a parallel one, before the release.
2. close-finished-Q1, option A: an agent cut mid-step (app restart) or stopped by the user is
   refused and named. The Chief of Staff asks the user, and on their yes runs `close` with a flag
   naming those agents as stopped, recorded in the log. Nothing is guessed from age.
   - The flag is `--stopped` (section 4).
   - Its refusals are in section 4.
   - The batch's record (`batch-NN.json` and `.md`) is where it is logged, because `close --yes`
     deletes `events.jsonl`.
   - The Chief of Staff card (Closing and Recovery) says when to ask.
3. Copilot keeps the 5-minute file-time rule here. Reading the end of Copilot's `events.jsonl` is
   a later inbox item (the Fable advisor, on the user's word).

## Out of scope

- `pause`. It reads no transcript today: it refuses only on the record (live, queued, ready or
  blocked CRs, pending orders, a stack driver). The request's title names "close and pause", but
  its body names only `close`'s quiet check (`running()`). `pause` stays unchanged.
- Copilot's transcript end: a later inbox item (decision 3).
- The detector for "a Driver ended with no recorded hand-back" (batch-18 retro, 4 occurrences).
  This CR only writes the reader so that a later CR can use it.
- `status --refresh`'s activity lines (`commands/activity.py`), `agent_records()` and
  `idle_seconds()`: unchanged.
- Any way past a transcript that cannot be read, or past a record cause.
- Messaging an agent from the CLI: never.

## Evidence

### Scenario (`scenario/run_scenario.py`, `close_refusals()`, around lines 2481-2556; `close_batch()`)

Replace the two age-based steps (line 2495, "a transcript written within 5 minutes", and line
2499, "an agent's transcript written within 5 minutes, whatever its type") with the steps below.
Each step runs with and without `--yes`. Refusals go through the existing `refused()` helper,
extended to pass extra arguments.

1. The Foreman's transcript (`uuid-foreman.jsonl`) ends with an `assistant` `tool_use` that has no
   result, and the file is aged 10 minutes (`age_sessions`). `close` refuses, naming `uuid-foreman`
   and the tool, with the `--stopped` sentence. This is the silent long tool call the old rule
   missed.
2. A subagent's transcript (the first `agent-*.jsonl`) ends with a `tool_result` of a tool other
   than the hand-back, with no `assistant` record after it, and the file was just written. `close`
   refuses, naming the agent's stem.
3. A subagent's transcript ends with `SubagentHandback` and its result, the file just written
   (`os.utime(f, None)`), and nothing else runs. `close` passes this check and prints the final
   cost (without `--yes`). This is the case batch-18's runs hit.
4. A subagent's transcript ends with an `assistant` text record (`stop_reason: end_turn`, no tool
   call), just written. `close` passes this check.
5. A subagent's transcript whose last line is cut JSON: `close` refuses, saying it cannot be read
   and giving the path. `--stopped <that stem>` is refused with "cannot be read" too.
6. A recorded Foreman transcript that is missing: `close` refuses, saying it cannot be read and
   giving the path.
7. `--stopped`:
   - (a) With step 2's running subagent, `close --stopped <its stem>` (no `--yes`) exits 0 and
     prints the "declared stopped on the user's word" line. The bare `<id>` gives the same result.
     Nothing is written: the batch's folder and `5-archives/batches/` are byte for byte the same.
   - (b) `--stopped` with a name that is not in the batch is refused with "no transcript of
     <batch> by that name" and the list of agents still running.
   - (c) `--stopped` with the name of an ended agent (step 3's) is refused with "shows it ended".
   - (d) With two running agents and one named, `close` still refuses, naming the other one.
   - (e) With a record cause present (an open order) and the running agent named, `close` still
     refuses on the order.
8. In `close_batch()`, the close that passes runs once with `--stopped <a running agent> --yes`.
   - `batch-NN.json` holds `stopped_agents` with that agent's name, transcript, cause and time.
   - `batch-NN.md` holds the "Declared stopped on the user's word" line under `## Cost`.
   - The `closed ...` output repeats the line.
   - A record closed without the flag (another unit) has no `stopped_agents` key.

Then:

- Keep the existing step at line 2555: the Chief of Staff's own transcript, written now, never
  blocks its own close. Its subagents are still read.
- The Copilot steps (lines 2535-2552) stay, with the same texts (`Copilot session uuid-foreman was
  written`, `not measured`).
- Fixtures: the scenario's seeded transcripts (Foreman, Chief of Staff, subagents) must end as
  ended under the new rule wherever a later step expects `close` to pass. Give their last
  `assistant` record a `stop_reason: end_turn` with no tool call, or end them with a hand-back and
  its result. Step 8 is the exception: it leaves one agent running on purpose. The
  `age_sessions()` calls that only existed to beat the 5-minute bound can go where the new rule
  does not need them. Keep them where Copilot still needs them.

### Tests (`skills/chantier/scripts/cli/tests/`)

Add one parametrized test of the reader, in-process, on prepared transcript files: the hand-back
with its result, `end_turn` text, `stop_sequence`, a pending `tool_use`, a trailing tool result, a
trailing prompt, `stop_reason: tool_use` with nothing after it, trailing `api-request` records
after a hand-back (still ended), a cut last line, a missing file, and a file with no user or
assistant record. One case per row; the test stays fast. The scenario carries `close`, its
refusals and `--stopped`.

### Gates

- `just check` passes (Linux, macOS, Windows).
- `just scenario` is green at the PR's head on the pipeline's `just scenario (ubuntu-latest)` job:
  the CR changes the CLI, the cards and the scenario. Following AGENTS.md, the top CR of the batch
  also passes `just scenario` locally on Windows.

## Questions for the user

None left open.
