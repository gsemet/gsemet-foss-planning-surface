# Change Specification: an ended or refused agent is restarted once, from the recorded state

## Goal

An agent that ends before its part is done, or is refused at its start, comes back exactly once
and never in silence: one restart from what the record holds, by one way (a message that resumes
it, or a new start, never both), with a note that says why. Three batch-15 cases show the gap:

- CR-213's first Driver was ended by a host API error (403, Cloudflare) right after its long gate;
  the Foreman restarted it and a second Driver finished. The cards do not say whether such an end
  is a silent end (two of which block the CR) or something else.
- Switching the batch from direct to Foreman mode lost the Drivers of CR-196 to CR-199 when the
  direct session stopped; the Foreman restarted them by the restart path, which no card asked for.
- A spec-writer refused a prompt without its first line; the Chief of Staff sent the line by
  `SendMessage`, which resumed that agent with its context, and also started a second one: two
  spec-writers wrote the same `03-change-spec.md`.

No `02-answers.md` exists: the request (`intake/request.md`, merged from three batch-15 retro
items on the user's word) is the only input, and the user ordered the CR done now.

## Measured: what a host failure lost on CR-213

From the archive `5-archives/261113-1149-213-stack-merges-in-one-go/STATUS.json`: the long gate
passed at `548e0f7` at 10:10:39Z (one log, `work/gates/20261113-105001.log`), `ship` ran at
10:11:02Z, then the Driver was ended by the host. The steering session's note reads `resume: the
Driver was ended by the host (API 403 error) after the long gate passed at 548e0f7; the verdict,
CI and hand-back remain`. The next Driver recorded the verdicts from 10:27:50Z and handed back at
10:30:05Z; the round count stayed 2 and the long gate was not run again.

So the record kept everything that binds to a head: the gate's pass, the shipped head, the round
count, the notes. What the end lost was the Driver's context, any uncommitted change in the
worktree, any worker it was running, and about 16 minutes. The restart path already costs no round
and no slot. This change therefore adds no CLI state: it names the case in the cards.

## Decisions taken here (nothing the user sees changes)

1. **After a first-line refusal: always a new start, never a message.** The request offers either.
   A new start is chosen because the plugin's write guard and its `cwd` rewrite read only the
   spawn's prompt (`hosts/claude-code.md`, "A worker's writes stay in its CR": no rewrite on a
   resume), so a resumed worker would run unguarded; because Copilot's resume of an ended agent is
   not recorded; and because the cards already say it since CR-213. What changes is that it is
   made true on Claude Code, where a `SendMessage` to a stopped subagent does resume it with its
   context: the refused agent answers any later message with the same refusal and does nothing
   else, so a message can never turn into a second worker beside the new start.
2. **One spec-writer per CR is guarded by the card, not the CLI.** `work/specifying` already marks
   a spec-writer at work and the CLI already reads it (`spec: specifying`). The CLI starts no
   agent and knows no role (AGENTS.md), and a new CLI tool needs a measured token cost, which one
   incident is not. The card makes `work/specifying` the guard.
3. **A host failure takes the existing restart path** (`foreman.md`, "A lost Driver"), with its
   own cause word, `host failure`, and does not count as a silent end. The request says "not a
   silent end".

## What changes

### `skills/chantier/references/concepts.md`

- "Starting an agent", the paragraph on a refused prompt: the quoted answer becomes
  "I run inside a chantier batch only. My prompt must start with `<its first line>`; a message to
  me gets this same answer: start a new agent with that line." Add: a refused agent answers every
  later message with that same answer and does nothing else, whatever the message holds (on Claude
  Code a message resumes a stopped agent with its context; the refusal holds there too). The parent
  starts one new agent with the line; it sends no message to the refused one.
- New paragraph after it, **"An agent that ends before its part is done"**, for every parent and
  every agent (a Driver of any kind, a worker, a spec-writer, a Demo explorer):
  - Each such end is restarted **once**, from the recorded state (`handoff`, `log`, the CR's
    notes, the worktree's commits, the folder's files), and the parent records why first: for a CR,
    `$CHANTIER note <cr> "restart: <cause>"`; for a spec-writer, the line of `work/specifying`.
  - The causes, one word each: `host failure: <the host's exact text>` (an API error, an
    overloaded or refused service, a network error the host reports as the agent's end, not the
    agent's own words), `refused first line`, `switch to Foreman mode`, plus those `foreman.md`
    already names (`context`, a proven death, a new epoch, a silent end).
  - **One way, never both.** A restart is either a message that resumes the ended agent, where a
    card names that way (only the `taken back:` note of `foreman.md` does), or a new start; never a
    message and a new start for the same end. The parent starts nothing while the agent it would
    replace may still run (the host lists it running, or it answered a `ping`).
  - A worker ended by a host failure: its Driver starts one new worker of the same role with the
    same brief and the note `restart: host failure: <text>`; no new `round` (`round` is run only
    before a Coder of a new round, `driver.md`).
- Rule 3 ("A parent restarts a failing child") points to that paragraph.

### Every agent file, both hosts, the bodies kept identical

`agents/*.md` and `com.github.copilot/agents/chantier-*.agent.md` (13 roles each; the files that
hold "a message to me does not restart me" today): the refusal text becomes the one above, ending
"a message to me gets this same answer: start a new agent with that line." and then "and stop. Any
later message gets the same answer." The frontmatter and the `# chantier-agent:` version line are
not touched (never edit a version by hand).

### `skills/chantier/references/foreman.md`, "A lost Driver"

- **The restart path** lists `a host failure` among its causes, with
  `take <cr> --note "resume: host failure: <exact text>" --epoch <n>`.
- New bullet **"A host failure"**: a Driver (CR, stack, release, QA) whose end carries the host's
  error rather than a hand-back takes the restart path at once, with no ping round. It is not a
  silent end: it does not count toward `driver ended twice`, nor toward "blocked twice" in
  Escalation. The new Driver reads from `handoff` what the record kept (a gate passed at the
  shipped head, verdicts, the PR) and does not redo it when the worktree's head is that head and
  the tree is clean. A second host failure on the same CR with no new head, round or note since
  the first: see open question Q1 (written here with its recommended answer, an ask
  `question <cr> host failure twice: <text>`, until the user answers).
- **After a switch to Foreman mode** (with the bullet "After an app restart, at a new epoch"): when
  the Foreman claims the batch from a direct batch, every CR whose Driver the switch stopped, the
  recorded stack driver and every open QA order with an agent id are restarted at once by the
  restart path, with `resume: switch to Foreman mode`; this is a death by the host in the sense of
  "A silent end" (it does not count). A CR the Chief of Staff's Driver handed back
  `blocked stopped` with the switch's note is taken back the same way and counts toward nothing.

### `skills/chantier/references/chief-of-staff.md`

- "Switching to Foreman mode": replace "let the running ones hand back (or stop them: a new Driver
  resumes with `handoff`)" with: before the Foreman starts, stop each live Driver you own (CR,
  stack, QA, release) by the host's stop, after `$CHANTIER note <cr> "switch to Foreman mode:
  Driver stopped; the Foreman restarts it"`; then start the Foreman with the next epoch and add to
  its prompt "Resume: restart every CR the switch stopped by the restart path, `resume: switch to
  Foreman mode`". No Driver of yours runs once the Foreman claims (two Drivers on one CR is what
  this prevents). See open question Q2.
- The bullet **"An agent's prompt starts with its first line, copied."** adds: the refused agent
  stays refused, a message to it included; the new start is the only way.
- "Backlog and grill", the spec-writer paragraph: `work/specifying` is the guard. Write it before
  the start (the time), add the agent id once started. While it exists, start no spec-writer on
  that CR. A first-line refusal ends that agent: replace the line with
  `<time> <new agent id> restart: refused first line` and start one new spec-writer; no message to
  the refused one. A spec-writer ended by a host failure: the same, with
  `restart: host failure: <text>`, once. Remove `work/specifying` when the (last) one ends,
  whatever the result.
- "Steering a batch yourself" reads `foreman.md` for lost Drivers: no change beyond the above.

### `skills/chantier/references/griller.md`

"What you do", the spec-writer item: add "one spec-writer per CR, `work/specifying` as the guard,
and a refused start restarted by a new start only", pointing to chief-of-staff.md.

### `skills/chantier/references/driver.md`

- "Your means", the Children item: a worker refused for its first line, or ended by a host
  failure, gets one new start of the same role with the same brief, `note <cr> "restart: <cause>"`
  first, no `round`; a second refusal of the same start is `handback blocked refused <exact text>`
  (unchanged rule for a refused start).
- `stop` (the line "`stop`: stop a long gate of yours …, then `handback blocked stopped`"): when the
  steering session's stop comes with a switch, the note says so; no other change for the Driver.

### `skills/chantier/references/hosts/claude-code.md`

Tools table, a row: "Resume a stopped subagent | `SendMessage` to its agent id resumes it with its
context | proved, batch-15 (a refused spec-writer resumed by a message); chantier uses it only for
the `taken back:` note of `foreman.md`: a refused agent answers it with its refusal".

### `docs/use-cases-direct.md`, "Switch to Foreman mode"

"No new Driver starts; the running ones hand back (or are stopped and resumed later)" becomes: "No
new Driver starts; the running ones are stopped, and the Foreman restarts each of them from where
the record stands as soon as it takes over the batch."

### `skills/chantier/scripts/cli/tests/test_structure.py`

Line 146: the asserted phrase becomes `a message to me gets this same answer: start a new agent
with that line`, and a second assert checks `Any later message gets the same answer.` in the body.
The comment above it says so.

## Out of scope

- Any CLI change: no new command, no new state, no `spec-writer` guard in `rails.py`, no change to
  `handoff`, `take` or `agents`.
- The hooks and `types/` (so no `just mod`).
- The other batch-15 retro items (the long gate queue, a Driver's context, a Driver's writes, the
  stack driver's id race, force pushes).
- Copilot's resume of an ended agent: not recorded, not trialled here.

## Evidence

- `just check` passes (Linux, macOS, Windows through CI), `test_structure.py` included with the new
  phrase on all 13 roles of both hosts, the bodies identical.
- `just scenario` passes (the cards change), unchanged.
- A grep shows no file left with "does not restart me" or "let the running ones hand back".
- A read-through of `concepts.md`, `foreman.md`, `chief-of-staff.md`, `griller.md`, `driver.md`
  shows each of the three cases answered once: host failure, switch, first-line refusal, with one
  way each, and no contradiction with "A silent end", "Escalation" and the `taken back:` flow.

## Open questions

- **Q1. A host failure that repeats.** Each host failure is one restart. If the same CR is ended by
  the host twice in a row with nothing new recorded in between, should the second become an ask to
  you (`question <cr> host failure twice`) rather than a third Driver? Recommended: yes, an ask,
  like a Driver out of context twice. The other choice: restart on every host failure, without
  limit.
- **Q2. A switch to Foreman mode stops the running Drivers at once.** The card today lets the
  running Drivers finish and hand back before the Foreman starts (or stops them). The request says
  the switch restarts every live CR. Recommended: stop them at once and let the Foreman restart
  them (the switch is immediate; a worker's unfinished, uncommitted step is redone). The other
  choice: wait for each running Driver to hand back, then start the Foreman (no work redone, but
  the switch may wait hours).
