# Change Specification: driver-liveness

Source: `intake/request.md` (batch-11 retro; folds the inbox items drivers-killed-by-app-restart,
dead-driver-slot and driver-context-exhaustion), `01-intent.md`, `02-answers.md` (2026-11-11, the
Fable advisor's decisions, accepted by the Chief of Staff on the user's delegation; answers 19-21
decided by the Chief of Staff on the spec-writer's questions). Code paths are relative to
`skills/chantier/scripts/cli/src/chantier/`, cards to `skills/chantier/references/`, line numbers
as on `main` at 24cc7eb.

## Goal

A Driver that dies (the desktop app cut, a host crash, its context exhausted) is seen by the
steering session within one or two heartbeats, on any host, and restarted from the CR's recorded
state with no round counted and no extra slot. Today it goes unseen: in batch-11 four Drivers died
with the app and only the Chief of Staff noticing that no worktree file had changed for 40 minutes
revealed it; and CR-182's Driver ran out of context and handed back "not ready, restart me", a case
no card names.

The split of the work: the CLI states measured facts (the last activity of each working CR,
whether a Driver is recorded) and refuses an ambiguous `take`; the Foreman card judges death and
restarts; context exhaustion becomes a named hand-back, distinct from a silent end. It must work
for any project and host, with no host detail hard-coded.

Finding of the grill, which shapes the scope: a restart already needs no second slot. Slots count
`working` CRs and open QA orders, not agents (`rails.py:69-71`, `held`), and `take` on a working
CR skips the slot check (`rails.py:180-181`). The real gaps are that nothing flags a dead Driver,
and a bare `take` on a working CR is silently accepted.

## What changes

### 1. CLI: the activity of each working CR in `status --refresh` (answers 1-5, 17, 19)

Where: `_refresh` in `commands.py:1140-1166` (today it prints only `longest silent Driver <cr>
<n> min`, from `c["updated"]`, lines 1150-1154), and the session-record reader
`costs.idle_seconds` (`costs.py:255-286`).

- The per-CR activity lines **replace** the `longest silent Driver` line (answer 19): they carry
  the same fact per CR. The scenario check (`run_scenario.py:3041-3044`) and `foreman.md:70-71`
  follow.
- For each `working` CR (a release CR included), `status --refresh` prints one line with the age
  of its last activity. That age is the most recent of:
  - its last CR event in the batch's `events.jsonl` (any kind: `take`, `round`, `note`, `gate`,
    `verdict`, `ship`, `handback`, `agent`...). This matters because `c["updated"]` moves only on
    take, round, note, ship and handback (`Batch.touch`, `state.py:503-505`); `gate` and `verdict`
    only log, so the former "longest silent Driver" was blind during a Coder pass or a gate;
  - the last write of the session records attributable to the CR: on a host with per-agent
    records (Claude Code: `subagents/agent-<id>.jsonl` beside each recorded steering transcript,
    as `idle_seconds` already reads them), the record of every agent the CR ever had (the `agent`
    events of the log, as `_cost_groups` maps them, `commands.py:2169-2174`) and of every worker
    whose chain of parents leads to one (the `parentAgentId` of each `.meta.json`, as `cr_of`
    follows it, `commands.py:2178-2182`).
- Also covered, each with its own line, when an agent id is recorded: the stack driver
  (`stack_agent`) and an open QA order (`orders[].agent`, set by `agents set O-<k>`,
  `commands.py:1261-1269`).
- **A host with no per-agent record** (Copilot: one `events.jsonl` per session, the only record
  the CLI reads): every working CR's line gives the session-level age, and the line says it is
  session-level, not the CR's own.
- **An unreadable record** (missing file, `OSError`: `idle_seconds` returns `None`) makes that
  line "not measured", never a guess (the same word as `rails.py:46-47`; no fallback). The exit
  code of `status --refresh` is unchanged by it.
- **A running long gate is activity.** When the long-gate lock names the CR (`_lock_holder`,
  `commands.py:1625-1632`; the text `<cr> pid <n> pg<m>` written by `lock.holding`,
  `commands.py:1716`, and parsed the same way by `cancel`, `commands.py:1867`), the CR's line
  says "gate running": the `gate` event is written only at the gate's end
  (`commands.py:1721-1724`).
- **The CLI never decides death.** It prints ages and the words above, never "dead", "suspect"
  or a threshold (`concepts.md:147-148`: no activity date is ever taken as proof of life; the CLI
  knows no role).
- Worktree file times are **not** a signal (answer 3): unbounded to scan, and the session records
  already move.

The exact form of the line is the Driver's to choose, within these words; an example, for
illustration only: `activity CR-104 12 min`, `activity CR-105 gate running`, `activity CR-106 not
measured`, `activity CR-107 31 min (session-level)`, `activity stack 4 min`, `activity O-2 qa 9
min`. `status` is already exempt from the ten-line output limit (`cli.py:13`). Update the help of
`status --refresh` (`cli.py:110-112`, "the silent Drivers and the spend") to name the activity
lines.

### 2. CLI: `status` flags a working CR with no Driver recorded (answer 12)

Where: the row loop of `status`, `commands.py:1197-1212`.

- A `working` CR with no `agent` recorded gets "no Driver recorded" in its row, with or without
  `--refresh`. The CLI cannot ask a host whether an id is alive: it flags what it records, nothing
  more.

### 3. CLI: `take` on a CR (answers 10, 11, 20)

Where: `check_take` (`rails.py:170-193`) and `take` (`commands.py:1408-1446`); the help of
`take --note` (`cli.py:127`, "why a ready or blocked CR goes back to a Driver").

- `take <cr>` on a `working` CR **without `--note`** is refused, exit 2 (precondition; the
  default code of `ChantierError`).
- `take <cr>` of a CR **whose agent id is still recorded** is refused, exit 2, whatever its
  state (working or blocked), not a working CR only (answer 20): one rule. The message names
  `agents set <cr> -` first. Precedent: `take stack` refuses while a stack driver is recorded
  (`commands.py:1424-1426`). Two Drivers on one CR thus become impossible by accident.
- When accepted on a working CR, it keeps the slot (no slot check, as today), counts no round
  (the round stays as it was), records `back to a Driver: <note>` in the CR's notes (as `take`
  already does for a ready or blocked CR, `commands.py:1437-1438`), so `handoff` shows it, and
  logs the take as a restart (the `take` event marks it so; the field's form is the Driver's).
- The budget still applies (`check_budget`, `rails.py:155-161`, called in `check_take` before
  the slot): a restart past the budget is refused with exit 5, and the Foreman makes it a
  `budget` ask.

### 4. CLI: the `context:` hand-back (answers 13, 14)

Where: `handback` (`commands.py:1467-1493`).

- The usage text of a bare `handback <cr> blocked` (`commands.py:1475-1477`) lists `context:
  <where it stopped, what is next>` among the reasons.
- `handback <cr> blocked context: …` leaves the CR `blocked` with that reason, as any blocked
  hand-back. Like `waits:` (`commands.py:1491-1492`), the CLI recognises the prefix only to print
  a different second line: it says the Foreman restarts a fresh Driver, with no ask to the Chief
  of Staff, instead of `<cr> blocked; the Foreman asks the Chief of Staff`.

### 5. Card: `foreman.md` (answers 6-9, 15-21)

Rewrite the lines on a lost Driver (`foreman.md:147-151`) and the `status` means
(`foreman.md:70-71`, "names the longest silent Driver": it now names each working CR's activity,
answer 19), and name the `take` refusal near `foreman.md:72-77`:

- **Suspect.** A working CR (or the stack driver, or an open QA order) whose activity line shows
  no activity and no running gate for one full heartbeat interval (30 minutes) is suspect. This
  replaces the 90-minute rule of `foreman.md:149`. The threshold is in the card, not in
  `chantier.yaml` (which holds only `roles`); a project's `AGENTS.md` ranks above the card. A
  line "not measured" or "no Driver recorded" is read for what it says, never as activity.
- **Proof of death**, one of two: the host refuses a message to the agent because it no longer
  exists (dead at once); or a `[foreman→driver <cr>] ping` to a suspect gets no `pong` by the next
  wake (`driver.md:112-114`).
- **Kept:** a `pong` proves a Driver alive, not that it moves: one with no new round, head or note
  for 3 hours gets `stop` (`foreman.md:150-151`).
- **After an app restart or at a new epoch.** Every Driver started by an earlier steering
  session is restarted at once, without a ping round: Drivers are background children of the
  steering session and die with it. Read literally (answer 21): when a new Foreman epoch is
  claimed, every `working` CR, the recorded stack driver and every open QA order with an agent id
  is restarted. The CLI shows no epoch per agent.
- **The restart path**, for every restart (a proven death, a new epoch, a silent end, a
  `context:` hand-back), always starting with `agents set <cr> -` (answer 20):
  `agents set <cr> - --epoch <n>`, `handoff <cr>`, `take <cr> --note "resume: <cause>" --epoch
  <n>`, a new Driver, `agents set <cr> <id> --epoch <n>`. No round is counted; the budget
  applies (a refusal with exit 5 is a `budget` ask). This is the path that worked in batch-11.
- **A `context:` hand-back.** The Foreman restarts a fresh Driver on that CR before any queued CR
  (a blocked CR holds no slot, so it takes the next free one): `agents set <cr> - --epoch <n>`,
  then `take <cr> --note "resume: context" --epoch <n>`, no round, no ask. A second `context:` on
  the same CR with no new head, round or note since the first is an ask: `question <cr> driver
  out of context twice`.
- **"Driver ended twice"** (`handback <cr> blocked driver ended twice`, `foreman.md:148`) counts
  only silent ends of the Driver itself. A death by the host (the new-epoch case above, or all
  Drivers lost at one wake) and a `context:` hand-back do not count.
- **Covered Drivers:** the rule covers every kind (CR, release, stack, QA).
- **Direct mode:** the same rules hold; the Chief of Staff steering a direct batch reads the
  Foreman card (`foreman.md:12-13`).
- Nothing names a host tool: how a message is refused, and how a Driver is started, stay in the
  host's reference.

### 6. Card: `driver.md` (answer 13)

- In "Your end" (`driver.md:92-95`), add `context:` to the list of blocked reasons, and say when:
  a Driver whose context is ending first records its state with `$CHANTIER note <cr> "…"`, then
  `handback <cr> blocked context: <where it stopped, what is next>`; the steering session restarts
  a fresh Driver from it. How a Driver sees its context ending is its host's business: the card
  does not say.
- `driver.md:17` already lists `resume:` among the notes a Driver goes on from: keep it.

### 7. Card: `concepts.md` (Touches)

- Exit codes (`concepts.md:167-169`): exit 2 also covers a `take` on a working CR without
  `--note`, and a `take` of a CR whose agent id is still recorded (working or blocked).
- Where `concepts.md` lists the hand-back reasons, add `context:`. (Today the reasons are listed in
  `driver.md:93-94`; `concepts.md:154-156` describes the hand-back generally. Add `context:`
  where a list of reasons exists, and nowhere new.)

### 8. Card: `chief-of-staff.md` recovery line

- In **Recovery** (`chief-of-staff.md:435-441`), only the "Resume" sentence changes: the new
  Foreman relaunches each CR still working by the restart path (`agents set <cr> -`, `handoff`,
  `take <cr> --note "resume: <cause>"`, a new Driver, `agents set <cr> <id>`). The rest of the
  recovery text stays as it is.

### 9. Scenario (`scenario/run_scenario.py`)

The change touches the CLI: `just scenario` is required. Existing steps affected:

- `Foreman.driver_died` (`run_scenario.py:381-385`) takes a working CR with a `resume:` note
  while the scripted Foreman has recorded an agent (`take` records `agent-<n>`, line 248): with
  the new rule it is refused. It runs `agents set <cr> - --epoch <n>` first, as the card's
  restart path does (answer 20); the check at lines 658-661 stays.
- The check "a wake names the longest silent Driver" (`run_scenario.py:3041-3044`) follows its
  replacement by the per-CR activity lines (answer 19).

New steps: the acceptance checks below.

No agent file changes (`agents/`, `com.github.copilot/agents/`).

## Out of scope

- Detecting a dead Foreman or reviving the heartbeat (`chief-of-staff.md:435-441` stays, except
  its "Resume" sentence, which names the restart path).
- Any host-specific liveness tool, or a new capability row in a host card.
- A `chantier.yaml` key (the threshold stays in the card).
- Killing orphan processes (already `cancel`).
- A "plugin reload needed" block cause (another CR).
- Automatic restarts by the CLI.
- Worktree file times as a liveness signal.
- An epoch shown per agent (answer 21).

## Evidence

`just check` passes (Linux, macOS, Windows), and `just scenario` passes on both forges with these
new checks:

1. In a scenario batch with two working CRs, `status --refresh` prints one activity age per
   working CR (and no `longest silent Driver` line); a CR whose last event is old but whose
   long-gate lock is held names it shows "gate running".
2. With no readable session record, the line says "not measured" and the exit code is unchanged.
3. `take <working cr>` without `--note` exits 2.
4. With an agent recorded, `take <working cr> --note "resume: x"` exits 2 and the message names
   `agents set <cr> -`.
5. After `agents set <cr> -`, the take succeeds with the same slots-held count, the round
   unchanged, the note in `handoff`'s notes, and `status` showing "no Driver recorded" until the
   next `agents set`.
6. The same restart with all slots held by other CRs succeeds; with the budget spent it exits 5.
7. `handback <cr> blocked context: …` leaves the CR `blocked` with that reason and prints the
   restart line, not the "asks the Chief of Staff" line; `agents set <cr> -`, then `take --note
   "resume: context"`, puts it back to `working` with the round unchanged (answer 20).
8. `foreman.md` names the suspect rule, the two proofs of death, the new-epoch rule, the
   `context:` case and what counts toward "ended twice"; `driver.md` lists `context:` among the
   reasons. Nothing in a card or the CLI names a host tool.

## Scheduling

Runs in parallel with gate-proof-cli-fixes; no `depends.json` (they share `commands.py` and
`driver.md`, which is no dependency).

## Open questions

None: the three raised by the first draft are decided in `02-answers.md`, answers 19-21.
