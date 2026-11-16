# Answers: driver-liveness

2026-11-11. The user's word: "fais les 2 CR maintenant", after the batch-11 retro; the user
delegates every design decision ("Grille tout avec une session fable ... je veux juste que
Chantier fonctionne et soit suffisamment générique"). The answers below are the Fable advisor's
decisions, from the code and cards on main; the Chief of Staff accepted them. File references are
to `skills/chantier/scripts/cli/src/chantier/` and `skills/chantier/references/`.

1. **The CLI's signal.** For each `working` CR, `status --refresh` prints the age of its last
   activity: the latest of its last CR event and the last write of the session records
   attributable to it. Today `updated` moves only on take, round, note, ship and handback
   (state.py:503-505), and gate and verdict only log, so the "longest silent Driver"
   (commands.py:1150-1154) is blind during a Coder pass or a gate. Record ages are already read by
   `costs.idle_seconds` (costs.py:255-285); agents are already mapped to CRs (commands.py:2169-2182).
2. **A host with no per-agent record.** The CLI prints the session-level age for every working CR
   and says so; an unreadable record is "not measured", never a guess (rails.py:46-47; no fallback).
3. **Worktree file times.** Not a signal: unbounded to scan, and session records already move.
4. **A running long gate is activity.** The row says "gate running" when the long-gate lock names
   the CR (commands.py:1716, 1867); the gate's event is written only at its end.
5. **The CLI never decides death.** It prints ages, never a "dead" word or a threshold
   (concepts.md:147-148; the CLI knows no role).
6. **Proof of death (card).** Either the host refuses a message because the agent no longer exists
   (dead at once), or a `ping` to a suspect gets no `pong` by the next wake (driver.md:112-114,
   foreman.md:149).
7. **Threshold (card).** A working CR is suspect when it shows no activity and no running gate for
   one full heartbeat interval (30 minutes); this replaces the 90-minute rule of foreman.md:149.
   Not in `chantier.yaml` (it holds only `roles`); a project's AGENTS.md ranks above the card. The
   "no new round, head or note for 3 hours gets `stop`" rule (foreman.md:150-151) stays.
8. **After an app restart or a new Foreman epoch.** Every `working` CR whose Driver was started by
   an earlier steering session is restarted at once, without a ping round: Drivers are background
   children of the steering session and die with it (chief-of-staff.md:438-441 names no path).
9. **Restart path.** `agents set <cr> -`, `handoff`, `take <cr> --note "resume: <cause>"`, a new
   Driver, `agents set <cr> <id>` (worked in batch-11; foreman.md:147-148).
10. **`take` on a working CR.** Refused (exit 2) without `--note`, and refused while an agent id is
    still recorded ("`agents set <cr> -` first"). When accepted it keeps the slot, records "back to
    a Driver: resume: …" in the CR's notes, and logs it as a restart. Precedent: `take stack`
    (commands.py:1424-1426). Two Drivers on one CR become impossible by accident.
11. **Rounds and budget on a restart.** No round counted; the budget still applies (rails.py:155-157):
    a restart past the budget is a `budget` ask.
12. **`status` flags a working CR with no agent recorded** ("no Driver recorded"), with or without
    `--refresh`. The CLI cannot ask a host whether an id is alive; it flags what it records.
13. **Context-exhaustion hand-back.** `handback <cr> blocked context: <where it stopped, what is
    next>`, after a `note` of the state. How a Driver sees its context ending is its host's
    business, not written in the card.
14. **The CLI knows `context:`** only as it knows `waits:` (commands.py:1475-1477, 1491-1493): the
    usage text lists it, and the printed line says the Foreman restarts a fresh Driver, with no ask
    to the Chief of Staff.
15. **The Foreman on `context:`.** It restarts a fresh Driver before any queued CR (a blocked CR
    holds no slot, rails.py:69-71), `take <cr> --note "resume: context"`, no round, no ask. A
    second `context:` on the same CR with no new head, round or note since the first is an ask
    (`question <cr> driver out of context twice`).
16. **"Driver ended twice"** counts only silent ends of the Driver itself; a death by the host
    (Q8, or all Drivers lost at one wake) and a `context:` hand-back do not count (foreman.md:148).
17. **Covered Drivers.** Every kind in the card rule; the CLI's activity line covers working CRs
    (release included), the stack driver and an open QA order where an agent id is recorded
    (commands.py:1261-1269).
18. **Direct mode.** Same rules; the Chief of Staff reads the Foreman card (foreman.md:12-13).

## The spec-writer's open questions (2026-11-11, decided by the Chief of Staff under the user's delegation)

19. **The `longest silent Driver` line** (commands.py:1150-1154) is replaced by the per-CR activity
    lines, which carry the same fact per CR; the scenario check (run_scenario.py:3041-3044) and
    foreman.md:70-71 follow.
20. **The refusal of answer 10 applies to every `take` of a CR whose agent id is still recorded**,
    whatever its state (working or blocked), not to working CRs only: one rule, and two Drivers on
    one CR stay impossible. The restart path always starts with `agents set <cr> -`, the `context:`
    case included; acceptance check 7 runs `agents set <cr> -` before its `take`. The scenario's
    `Foreman.driver_died` (run_scenario.py:381-385) runs `agents set <cr> -` first.
21. **"Started by an earlier steering session" (Q8) is read literally:** when a new Foreman epoch
    is claimed, every working CR, the recorded stack driver and every open QA order with an agent
    id is restarted, because Drivers are the steering session's background children and die with
    it. The CLI shows no epoch per agent.

## Out of scope

Detecting a dead Foreman or reviving the heartbeat (chief-of-staff.md:435-441 stays, except its
"Resume" sentence names the Q9 path); any host-specific liveness tool or new host-card capability
row; a `chantier.yaml` key; killing orphan processes (already `cancel`); a "plugin reload needed"
block cause (another CR); automatic restarts by the CLI.

## Touches

The CLI (`status`, `take`, `handback` text): `just scenario` required. Cards: foreman.md,
driver.md, concepts.md (exit-code and hand-back lists), chief-of-staff.md recovery line. No agent
file changes.

## Acceptance checks

1. In a scenario batch with two working CRs, `status --refresh` prints one activity age per working
   CR; a CR whose last event is old but whose gate lock is held shows "gate running".
2. With no readable session record, the line says "not measured" and the exit code is unchanged.
3. `take <working cr>` without `--note` exits 2.
4. With an agent recorded, `take <working cr> --note "resume: x"` exits 2 and names `agents set <cr> -`.
5. After `agents set <cr> -`, the take succeeds with the same slots-held count, the round unchanged,
   the note in `handoff`'s notes, and `status` showing "no Driver recorded" until the next `agents set`.
6. The same restart with all slots held by other CRs succeeds; with the budget spent it exits 5.
7. `handback <cr> blocked context: …` leaves the CR `blocked` with that reason and prints the
   restart line, not the "asks the Chief of Staff" line; `take --note "resume: context"` puts it
   back to `working` with the round unchanged.
8. foreman.md names the suspect rule, the two proofs of death, the new-epoch rule, the `context:`
   case and what counts toward "ended twice"; driver.md lists `context:` among the reasons. Nothing
   in a card or the CLI names a host tool. `just check` passes.

Runs in parallel with gate-proof-cli-fixes; no `depends.json` (they share `commands.py` and
`driver.md`, which is no dependency).

## Restarted after a cancel no one ordered (2026-11-11)

22. CR-183 (this specification) was cancelled at 21:36:44Z by a `cancel` that neither the user,
    the Chief of Staff nor the Foreman ordered, while its Driver's long gate ran; its round 1 work
    was approved and committed. The Chief of Staff re-adds it under the user's go ("fais les 2 CR
    maintenant"). The new CR resumes from CR-183's branch
    `chantier/batch-11/cr-183-change-specification-driver-liveness`, head 79cc74a (round 1,
    rebased on main fbe0166, inspected and approved): the Driver starts its branch from that
    commit, reruns the long gate there and ships; no new code unless the gate or CI is red.
