Head: 79cc74a4a6f7da65f724a2c7d8332fd3c57ac6ed

Gates at 79cc74a (work/gates/20261111-230017.log): `just check` 45 passed; `just scenario` github 548/548
(scenario/results/github-20261111-232131.md in the worktree), gitlab 548/548 (gitlab-20261111-232840.md).
PR 122 head on the forge is 79cc74a (gh pr view), draft.

Spec Evidence checks, each judged at 79cc74a. Steps are in `driver_liveness` (scenario/run_scenario.py
~2326-2412); each "[x]" line below is in the github transcript.

1. PROVED. Three working CRs, a lock naming the third: the step asserts one `activity <cr>` line per CR
   (`\d+ min`, `not measured`, `gate running`) and no `longest silent` line. Transcript: "[x] `status
   --refresh` gives one activity age per working CR, and no longest silent Driver".
2. PROVED. Session record removed: "[x] with no readable session record the line says not measured, and
   the exit code is the spend's own" (asserts code 4 = the spend's own, line `not measured`).
3. PROVED. "[x] `take` of a working CR without a note is refused (exit 2)".
4. PROVED. "[x] `take` of a CR with an agent recorded is refused, naming `agents set <cr> -`" (exit 2,
   stderr names it).
5. PROVED. "[x] status flags a working CR with no Driver recorded" and "[x] after `agents set <cr> -` the
   restart is accepted: same slots held, no round counted, the note in the facts, the take logged as a
   restart" (asserts "3 of 3 slots held", round unchanged, `back to a Driver: resume: x` in notes and in
   `handoff`, event `restart: true`).
6. PROVED, with a nuance. Slots: the restart is made with 3 of 3 slots held (the restarted CR counts among
   them: slots count working CRs, and `check_take` skips the slot check on a working CR, rails.py diff).
   Budget: "[x] a restart past the budget is refused (exit 5)". The case "all slots held by *other* CRs"
   is the same code path (no slot check on a working CR); no separate step.
7. PROVED. "[x] `handback blocked context:` leaves the CR blocked and prints the restart line, not the ask
   line" and "[x] a fresh Driver takes it back with the note, the round unchanged" (after `agents set
   <cr> -`).
8. PROVED. foreman.md (diff) has the Suspect rule (30 min), Proof of death (two), new-epoch rule, restart
   path, `blocked context:` case, and "ended twice" counting (only silent ends of the Driver itself;
   host death and `context:` do not). driver.md lists `context: <where it stopped, what is next>` in the
   reasons and says when. Scenario check "[x] foreman.md names the suspect rule ..." passes. Host tool
   names: grep of references/*.md and src/chantier/*.py for SendMessage|TaskStop|Task tool|
   run_in_background|spawn_agent|read_agent|write_agent finds only commands.py:187
   (`("SendMessage",)`), which is not in the diff (pre-existing, outside this CR); the diff's added
   lines name none.

Extra probes (python import of `commands._activity` on a scratch events log, scratchpad probe.py, no
batch touched), at 79cc74a:
- claude host: `activity CR-1 40 min`, `activity stack 40 min`, `activity O-2 qa not measured` (an agent
  recorded for the order and no readable record: not measured, never a guess).
- copilot host with a session age of 600 s (idle_seconds stubbed): `activity CR-1 10 min (session-level)`,
  same for stack and O-2 qa. With no readable session: `not measured`.
So the stack, QA and session-level lines claimed in the PR body behave as stated. No scenario step covers
them (probe only).

pr-body.md vs the diff at 79cc74a:
- Summary, Deliverables, Changes match the diff: `_activity`/`_refresh`, `status` "no Driver recorded",
  `take` restart mark and note, `handback` `context:`, `check_take` refusals, `costs.py` per-agent
  records, `cli.py` help, four cards (foreman, driver, concepts, chief-of-staff), scenario. No delivered
  change unmentioned.
- Mermaid block renders on GitHub; sections and the fold are well formed.
- "no data format changes": the `take` event gains an optional `restart` field; additive, disclosed in
  Autonomous decisions. Acceptable.
- Test plan: the boxes are unchecked and `<sha7>` is still a placeholder in four lines; "Review: approved
  at 79cc74a" is the Inspector's claim, not judged here. The Driver fills these at hand-back (card rule
  on a posted description); the posted description must then carry the SHAs. Not a defect of the diff.
- The `context:` second-time ask and the epoch restart are card rules, proved by the card text only
  (no CLI behaviour exists for them, by design).

UNVERIFIED: the Foreman's behaviour when it follows the cards (a judging agent, not testable here);
the posted description's SHAs (placeholders now).

VERIFIED
