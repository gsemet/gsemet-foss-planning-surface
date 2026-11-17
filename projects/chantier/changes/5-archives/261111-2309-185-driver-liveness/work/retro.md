# Retro

## 2026-11-11 — CR-174 worker-write-guard-redesign (batch-11, stopped by the user in round 2)

- The epoch-1 Foreman's session still ran the old CR-171 write guard after main's 24cc7eb removed it, so round 1's Coder Edit inside its own worktree was refused and a round was spent for nothing: a guard that can refuse a worker's legitimate write must be removable without restarting the sessions that loaded it, or the Chief of Staff must restart the Foreman before a batch whenever a hook of the plugin changed on main.
- The epoch-1 Foreman was replaced and the Driver restarted (epoch 2): a CR blocked by a stale loaded plugin should be a named block cause ("plugin reload needed") that the CLI offers a `take --note` path for, instead of an ad hoc replacement of the Foreman.
- The user stopped the batch in round 2, with CR-174 unmerged and no PR: the branch and worktree stay for the user's word; the work is unfinished.

## 2026-11-11 — batch-11 paused with all nine CRs merged (CR-174 to CR-182)

- The desktop app was cut while four Drivers ran: their agents died with no signal, and only the Chief of Staff noticing that no worktree file had changed for 40 minutes revealed it. A Driver's liveness should be checkable by the Foreman (a last-activity time in `status`), and `handoff` plus a `take --note "resume: ..."` worked as the restart path.
- A Driver ran out of context mid-flow (CR-182) and handed back "not ready, restart me": the card has no name for this end, so the "second silent end is blocked" rule was applied by judgement. A context-exhaustion hand-back should be a named case in the Foreman card.
- A `take` on a CR that already runs is accepted and only records the note, so a dead Driver keeps its slot until the Foreman takes it again: `status` could flag a taken CR whose agent id is gone.
- Parallel mode made every merge cost a rebase pass (CR-181, CR-176 and CR-182 went back to Drivers; CR-176's and CR-182's patches were identical or clean), and the rebase of a CR that has used all its rounds can only end in a clean rebase or `blocked rounds`. A CR PR that GitHub reports MERGEABLE needs no rebase note, so the Foreman checks `gh pr view` first.
- CR-181 shipped without the `claude-fable-5-2` price its spec asks for, because no Driver had a network tool to read a price page and none invented one: a spec that needs an external fact should name its source or the Driver's tools.
- CR-174's trial step 2 (a relative write inside the worktree) could not be seen live, because the host asks "sensitive file" in a non-interactive session; only the unit test proves it. The main checkout still shows `hooks/register.test.tsx` emptied and untracked `commands.py`, `concepts.md`, `state.py`, none from this batch.
- CR-176 found that `driver.md` says `round` is refused past the budget while the code refuses only on the round limit: a card and code mismatch, no fix CR yet.

## 2026-11-11 — CR-183 driver-liveness cancelled by its own Driver (batch-11, resumed with CR-183 to CR-185)

- The CR-183 Driver ran `chantier.py cancel CR-183 --batch batch-11` itself at 21:36:40Z (its transcript, agent a9c8325f982ed169f, one PowerShell call: `cancel CR-183 ...; git fetch origin main; git rebase origin/main`). It meant to stop its own long gate after the Foreman's note that PR 120 had changed the cards and a rebase came first, but `cancel` kills the gate's process group and moves the CR to 6-trash, and a cancelled CR is never revived: round 1 was approved, and the Chief of Staff had to file CR-185 with the same specification, started from CR-183's head 79cc74a. A Driver must never run `cancel` to stop its own gate: the card must say that `cancel` is the Foreman's, on the Chief of Staff's word, and give the Driver a way to say "stop my gate" (a `gate --stop`, or a note to the Foreman, who stops it).
- The Foreman's rebase note told the Driver to rebase "before the long gate" while its gate was running, with nothing saying how to stop a running gate; the note should have said "let the running gate end, then rebase and re-gate" (CR-184's Driver read it that way).

## 2026-11-12 — batch-11 paused again, CR-184 and CR-185 merged (CR-183 cancelled, replaced by CR-185)

- A cancelled CR's approved work survived only because its branch head could seed the new CR: CR-185 started from CR-183's head 79cc74a and went straight to the long gate with no coder. `cancel` has no undo, so a CR cancelled by mistake costs a new CR number, a new folder and a spec copy; the CLI could keep a cancelled CR revivable until the batch pauses.
- CR-185's PR body went through two Inspector passes that asked for changes on wording (roles and batch terms outside the internal references) and a third pass was skipped; the Driver card could say that a PR body is written for an outside reader from the first draft.
- CR-184's Inspector blocked a plain-text number file because chantier writes only JSON and Markdown in the planning folder; it became `restored.json`. The rule was caught by the Inspector, not by a gate: a structure test for the planning folder's file types would catch it earlier.
- A rebase after another CR's merge was clean or context-only in both CR-184 and CR-185: the gate re-run, not the rebase, was the cost (about 13 minutes of the long gate each time).
