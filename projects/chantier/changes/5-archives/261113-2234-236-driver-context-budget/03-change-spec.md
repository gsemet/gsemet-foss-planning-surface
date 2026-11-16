# Change Specification: the Driver's context threshold, set from the measure

No issue.

## Goal

From batch-16's retro (point 1), reviewed by an advisor. Two CR Drivers ended near 90k tokens. The
CR-216 Driver handed back `blocked context:`, and the CR-215 Driver ended with no hand-back in the
record. The Driver card's threshold is 150,000 tokens. The request asks to compare the printed
`context:` figures with the transcripts, set the threshold from that measure so that a Driver hands
back `context:` well before its end every time, and cap the Inspector's JSON reply. The CLI changes
only if the measure shows it is wrong.

Decisions (`02-answers.md`, 2026-11-13): the proposal as filed is the scope ("ok pour tout. fait ca
maintenant"). Points the request leaves open take this specification's defaults, listed at the end.
The CR joins the running batch-17.

## The measure (done while writing this specification)

Source: the batch-16 and batch-17 steering session
`C:/Users/gaeta/.claude/projects/C--Users-gaeta-Projets-chantier/bd1945f6-9982-485f-b29f-477277e80753/subagents/`,
one `agent-<id>.jsonl` and `agent-<id>.meta.json` per agent. Method, which the Verifier repeats:
for each `assistant` entry whose `message.model` is not `<synthetic>`, keep the last `usage` per
`message.id`. A call's prompt is `input_tokens` + `cache_creation.ephemeral_5m_input_tokens` +
`cache_creation.ephemeral_1h_input_tokens` + `cache_read_input_tokens`, the sum `costs.agent_context`
makes. A compaction is a `system` entry with `subtype` `compact_boundary`. Every agent runs
`claude-sonnet-5-5` with `autoCompactWindow: 200000` from its agent file.

**1. The `context:` line reads right.** The only `context:` figure a Driver printed in these runs
was `context: 44582 tokens (agent a24a1d7ed6df52bc3)` (CR-215's second Driver). The call just
before it had a prompt of exactly 44,582 tokens. In all five CR-215 and CR-216 Driver runs,
`cache_creation_input_tokens` equals the sum of the `cache_creation` breakdown on every call, so the
CLI misses no token. **The CLI does not change.**

**2. Neither end was a context end.** No Driver of the session compacted. Driver runs reached 46k to
122k tokens (the highest, CR-220's Driver, ended `ready` at 122,042).

| Driver run (agent) | Calls | Last prompt | How it ended |
| --- | --- | --- | --- |
| CR-215 Driver (`a84859a1c5ddb9d7a`) | 14 | 92,125 | It resumed its Inspector with `SendMessage`, then called the host's hand-back at once, with no `$CHANTIER handback`: the record shows no hand-back. |
| CR-216 Driver (`ac87782157e90d829`) | 12 | 91,771 | It resumed its Coder with `SendMessage`, then ended its turn with a text ("I'm waiting for its reply"). The host at once asked for its hand-back (`[handback-send-enforce] Your report has not been delivered…`), and the Driver handed back `blocked context:` at 91,159 tokens, a cause the figure does not support. |

Both ends follow a worker resumed by a message and a Driver that stopped to wait for its reply.
CR-230 of batch-17 (`.agents/changes/4-batch/2-actives/230-worker-reply-contract/`) already adds
"a worker is never resumed by a message" to `driver.md`. This CR does not repeat that rule.

**3. Where compaction really starts.** Three Coders with the same model and window compacted. Their
last prompt before the compaction was 161,951 tokens (CR-224 round 1), 164,772 (CR-221 round 1) and
166,684 (CR-216 round 1). That is the "165 to 170k" the host reference saw for sessions set to
300000, and it is about 35k below the 200,000 the card counts on. The card's 150,000, "three
quarters of the 200,000", leaves only about 12k before the first compaction measured.

**4. How fast a Driver grows.** A Driver starts at about 15.5k tokens and reaches 72k to 74k after
its opening reads (`driver.md`, the specification, `concepts.md`, `hosts/claude-code.md`). Past
60k, the largest growth between two calls of a Driver is 5,702 tokens. The largest Driver step
overall is 50,382 (CR-221's Driver, during its opening reads).

**5. Worker replies.** The Inspector's JSON replies were 4,307 to 9,343 characters, and the largest
(CR-216 round 1) had seven `minor` items, several of them paragraphs and one reporting no defect.
The request says the other replies are already capped at ten lines (`worker.md`, line 20-21). The
measure says that cap is not kept: the Coders' replies were 93 to 105 lines (about 11,000 to 12,500
characters), and a Verifier's 69. See open point O4.

## What changes

Only cards: `skills/chantier/references/driver.md`, `skills/chantier/references/worker.md` and
`skills/chantier/references/hosts/claude-code.md`. No CLI, no hook, no type, no agent file
(`agents/`, `com.github.copilot/agents/`), no scenario step.

### 1. `driver.md`, "Your means", the Context bullet (line ~37-41)

- The threshold becomes **130,000** tokens (default O1). The reason in brackets changes from "three
  quarters of the 200,000 `autoCompactWindow`" to the measure: the host compacted agents carrying
  200,000 from about 162,000 tokens (the host's reference, section "Compacting"), and 130,000 leaves
  room for several steps, the note and the hand-back.
- `blocked context:` is handed back only when the last `context:` line read 130,000 or more. A
  Driver that stops for any other reason names that reason, never `context:` (the CR-216 case).
- A new sentence, in the same bullet: never end your turn to wait for a child. A child runs in the
  foreground, and its reply is the result of the call that started it. The one turn end that waits
  is the long CI wait, with the forge's watch running in a background shell (the "CI" bullet,
  line ~155-158). On Claude Code, a turn that ends with nothing running in the background ends your
  run: the host asks for your hand-back at once (the host's reference).
- A new sentence: when the host asks for your hand-back while the CR's work remains, record your
  state with `$CHANTIER note <cr> "…"`, then `handback <cr> blocked context: host asked the hand-back
  at <n> tokens: <where it stopped, what is next>`, then the host's hand-back (default O2). The
  `<n>` is the last `context:` figure. Never call the host's hand-back with no `$CHANTIER handback`
  first (the CR-215 case).

The rest of the bullet (`context: not measured`, the rules on large outputs) stays as written. The
text `` `context: <where it stopped `` stays in `driver.md`, because the scenario's card check at
`scenario/run_scenario.py:2840-2847` looks for it. Lines ~214 and ~229-231 (the `context:` reason in
the list of `handback` reasons) stay as written.

### 2. `worker.md`, "Inspector": the JSON is capped (line ~49-53)

After the JSON example, add (defaults O3):

- Each item in `blocking` and `minor` is one sentence of at most 300 characters, starting with
  `file:line:` or `pr-body.md: <section>:` when it has a place.
- `minor` holds at most five items. When there are more, the fifth says `and <n> more of the same
  kind` and names the kind.
- An item states a defect. What was checked and found right does not go in the reply.
- The whole reply stays under 3,000 characters. The measured largest was 9,343.
- `blocking` is not limited in number: each item there is worth a round. Each one still keeps the
  300-character limit.

The "Extra review step" section (line ~178-182) already replies "with the Inspector's JSON", so the
cap applies to it with no new text. The reply's format check that CR-230 adds to `driver.md`
(parseable JSON, `verdict`, `head`) is unchanged by this CR. A reply over the cap is still read: it
is not a "reply out of format" that a restart repairs (default O3).

### 3. `hosts/claude-code.md`, "Compacting" (line ~346-356)

- The **Unproved** paragraph (line ~346-348) keeps the trial for the main sessions and gains the
  measured point for subagents. It becomes a **Measured** line: agents set to `autoCompactWindow:
  200000` on `claude-sonnet-5-5` compacted after a last prompt of 161,951 to 166,684 tokens (three
  Coders, batch-16 and batch-17, 2026-11-13). Sessions set to 300000 compacted around 165 to 170k.
  This matches a window capped at the model's 200,000 with a reserve of about 35k, but the cap's
  value stays unproved until the trial reads it back with `/autocompact`.
- The **Recommendation** paragraph (line ~350-356) is unchanged, apart from pointing to the
  measured line.

### 4. `hosts/claude-code.md`, a host fact on ending a turn

Add one row to the table of capabilities that holds "Resume a stopped subagent" (line ~503), or one
bullet next to it, in the same style:

- A background subagent that ends its turn with nothing running in the background is asked for its
  hand-back at once (`[handback-send-enforce] Your report has not been delivered. Call
  SubagentHandback…`), before a resumed worker's reply arrives. Status: proved, batch-16 (the CR-216
  Driver, agent `ac87782157e90d829`; the CR-215 Driver's Inspector reply came after its hand-back).
  A background shell's end wakes it (the CI wait of `driver.md`).

## Out of scope

- The CLI (`skills/chantier/scripts/cli/`): the measure found it right (section 1 of the measure).
  No new command or output, and no change to `costs.agent_context` or `_context_line`.
- The agents' `autoCompactWindow: 200000` and their model.
- "A worker is never resumed by a message": CR-230 carries it.
- The ten-line cap on the other workers' replies, which the measure shows is not kept (default O4).
- The cost of a Driver's opening reads, about 58k of its first 74k (default O5).
- Copilot: `context:` is `not measured` there (`Copilot gives no per-agent record`), and the
  threshold reads a figure Copilot does not print. `hosts/copilot.md` does not change.
- New scenario checks or eval scorecard rows (the evidence is the cards' diff and the measure).

## Batch-17, CR-221 and CR-230

This CR touches no CLI file, so **it does not wait for CR-221** (`.agents/changes/4-batch/2-actives/221-python-inline-deps/`),
whose out-of-scope list excludes any change to the cards. No `depends.json`.

CR-230 also edits `driver.md` (a new bullet after line ~36, a forge bullet near the Push bullet, the
Inspector paragraph of "CR driver") and `worker.md` (the shared paragraph, "Verifier", "Conflict
resolver"). This CR edits the Context bullet of `driver.md` and the "Inspector" section of
`worker.md`. These are shared files, not a need: the second to land rebases. This CR relies on
CR-230's "never resumed by a message" only for its explanation, not for its text. If CR-230 were
dropped, the gap it fills would reopen; the Chief of Staff would then file it again.

## Evidence

- `just check` passes (Linux, macOS and Windows in CI).
- `just scenario` passes at the PR's head, as `AGENTS.md` asks for a change to the cards. Its card
  check at `scenario/run_scenario.py:2840-2847` still finds `` `context: <where it stopped `` in
  `driver.md`.
- `git diff --stat <base>..HEAD` lists only `driver.md`, `worker.md` and `hosts/claude-code.md` (and
  the CR's archive when the project asks for it).
- The Verifier quotes, with `git grep -n` at the pushed head: `130,000` and the "never end your
  turn" sentence in `driver.md`; the 300-character, five-item and 3,000-character limits in
  `worker.md`'s "Inspector"; the measured compaction point and the `handback-send-enforce` fact in
  `hosts/claude-code.md`. `git grep -n "150,000"` under `skills/` finds nothing.
- The measure is repeatable: the Verifier runs the method of "The measure" on the session folder
  named there, with a short script in its notes folder, and finds the figures of the table and of
  points 1, 3 and 4. A later session may have removed the transcripts. In that case, `verify.md`
  says so and carries the figures from this specification.
- The PR's Deliverables carry the measure's table and the three compaction points. Nothing runs to
  show before and after: the before/after is the cards' diff.
- Known gaps: the 130,000 threshold is not yet seen working in a real batch. It is proved only when
  a Driver of a later batch hands back `context:` at or past 130,000 with no compaction before it.
  The PR's Known gaps names it.

## Open points, with the default taken

- **O1. The threshold's value.** Default: 130,000. The first compaction measured was at 161,951.
  130,000 leaves about 32k, which is five of the largest Driver steps past the opening reads
  (5,702), plus the note and the hand-back. It stays above the highest Driver run seen to end well
  (122,042). Lower values (120,000) would have stopped that run; 150,000 leaves about 12k.
- **O2. The cause a Driver gives when the host asks its hand-back early.** Default: the existing
  `context:` route, with the text `host asked the hand-back at <n> tokens`. The CLI already sends a
  `context:` hand-back to a fresh Driver from the recorded state, with no ask, and the text keeps
  the real cause apart from the threshold. A new reason word (for example `ended:`) would change
  the CLI's `handback` and the Foreman's card, which this CR avoids.
- **O3. The Inspector cap's numbers, and an over-long reply.** Default: 300 characters an item,
  five `minor` items, 3,000 characters in all, and `blocking` not limited in number. A reply over
  the cap is read as it is, not restarted: restarting an Inspector costs 15k to 60k tokens of a new
  worker, more than the reply it would save.
- **O4. The ten-line cap the Coders and the Verifier do not keep** (93 to 105 lines, 69 lines).
  Default: out of scope. The request takes the cap as kept, and CR-230 is rewriting the reply
  contract. The Chief of Staff offers it as an inbox item, with these figures.
- **O5. The Driver's opening reads** (`hosts/claude-code.md` alone is 46,326 characters, and
  `concepts.md` 33,964), which take about 58k tokens before any work. Default: out of scope. It is
  an inbox item, for example to read only the host reference's sections a Driver uses.
