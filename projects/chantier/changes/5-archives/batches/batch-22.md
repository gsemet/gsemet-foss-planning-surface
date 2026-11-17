# batch-22

Opened 2026-11-16T19:45:52Z, closed 2026-11-17T06:42:10Z, stack, steered by direct (the Chief of Staff), no budget, final cost $61.78. [batch-22.json](batch-22.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-297](../261116-2017-297-copilot-role-models/) | Change Specification: Copilot role model defaults | merged | https://github.com/gsemet/chantier/pull/248 | 2 | $1.59 |
| [CR-302](../261117-0627-302-pr-monitor/) | Change Specification: a live, read-only view of the batch's PRs on the web board | merged | https://github.com/gsemet/chantier/pull/251 | 2 | $6.91 |
| [CR-298](../261116-2119-298-copilot-model-catalog/) | Change Specification: Copilot model catalog from GitHub's own tables | merged | https://github.com/gsemet/chantier/pull/250 | 1 | $2.38 |
| [CR-303](../261117-0627-303-pr-merge-signal/) | Change Specification: the board signals a merge it sees | merged | https://github.com/gsemet/chantier/pull/252 | 1 | $2.37 |
| [CR-299](../261116-2138-299-model-defaults-board-config/) | Change Specification: chantier's configuration in layers, and the shipped defaults | merged | https://github.com/gsemet/chantier/pull/253 | 2 | $6.70 |
| [CR-304](../261117-0627-304-ui-feedback-large-screen/) | Change Specification: the web board on a large screen | merged | https://github.com/gsemet/chantier/pull/249 | 3 | $4.79 |
| [CR-300](../261116-2239-300-role-model-per-host/) | Change Specification: a model per role on each host | merged | https://github.com/gsemet/chantier/pull/255 | 2 | $5.34 |
| [CR-305](../261117-0627-305-board-surface-selector/) | Change Specification: the web board's selector shows the surface, and each project its paths | merged | https://github.com/gsemet/chantier/pull/254 | 3 | $3.99 |
| [CR-301](../261116-2341-301-board-config-page/) | Change Specification: the web board's Configuration page | merged | https://github.com/gsemet/chantier/pull/256 | 4 | $7.81 |
| [CR-306](../261117-0627-306-board-config-lf/) | Change Specification: the board's Configuration page writes the project file with LF | merged | https://github.com/gsemet/chantier/pull/257 | 1 | $1.07 |
| [CR-307](../261117-0628-307-release-0-11-0/) | Version PR for chantier v0.11.0 | merged | - | 0 | $1.44 |

## Cost

- Total: $61.78, no budget
- Chief of Staff, steering the batch $15.99 (26%), Drivers $15.33 (25%), workers $30.46 (49%)
- Most: CR-301 $7.81, CR-302 $6.91, CR-299 $6.70
- Chief of Staff, steering the batch: 61 wakes, context 180,750 tokens on average, 266,181 at its peak
- Driver chantier:cr-driver with its workers: $41.99 (1843 calls)
- Driver chantier:stack-driver with its workers: $2.36 (134 calls)
- Driver chantier:release-driver with its workers: $1.44 (55 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $5.10 since the batch opened (93 calls, 2 spec-writers, 1 spec critics)
- Chief of Staff, whole session: $829.29 ($61.78 of it in the batch's spend), context 228,467 tokens; not counted: 3 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)
- Declared stopped on the user's word: agent-a0106566b6aa3f0cb (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a0efdc32dca6c61a7 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a103955deaf241307 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a164f7a02355addd0 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a20c37340cb1f40bf (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a22025d94b0425f76 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a2527633954813a84 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a4481a8d0b396f19f (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a82a4e8172fa0b0d4 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-aa2b04a9ea02a0446 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-aa835f48f2788b16f (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-aa9c906f13b56448b (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-aaf5f1a3bd386a2cf (its last record is a prompt with no answer yet)

## Retro

## 2026-11-17, CR-297..CR-307 (critic: kept 11, dropped 7)

- [chantier] Three Drivers (CR-299, CR-303, CR-304) stopped at once around a compaction of the steering session; `SendMessage` refused to resume them, so the batch waited on the user's word: document `take <cr> --note "resume: <cause>"` as the steering session's own path after an outside stop, covered by the batch's go, and have the heartbeat detect a Driver recorded but stopped.
- [chantier] `close` refused until the user declared 13 subagents of the steering session stopped (`--stopped`), though every CR was merged and every batch agent cleared: it counts every unanswered subagent transcript of the session (the Chief of Staff's own grill and spec subagents, Drivers already replaced): `close` judges only the agents the batch recorded and still holds, and lists the session's other subagents apart, not as blockers.
- [chantier] The batch was not paused when its last CR merged: in direct mode the Chief of Staff skipped "The pause" (cleanup, retro, `pause`) and the close offer; the user had to ask, and `close` refused "running, not paused": the last `order merged` / `handback` of a batch prints the pause as the next step, and `status` and the heartbeat flag "every CR merged, not paused".
- [project] `just test` measured 61–63 s on the Windows machine, head and base alike, above AGENTS.md's budget (18.5 s + 30 s): profile and trim the slow tests, or restate the budget.
- [chantier] CR-305 uploaded screenshots of the live board showing a local path with the username to PR 254: the Driver and Verifier cards require made-up paths in any image, checked before any upload.
- [project] `ruff format --check scripts` flags mod.py, release_notes.py, version.py, because `just check` checks only `skills`: `just check` format-checks `scripts` too.
- [chantier] The Chief of Staff gave the release Driver a `writes:` line, which a release driver never gets; the guard refused its worktree writes and it has no Agent tool, so one Driver was lost and taken back (release): `take` prints, for a release, stack or QA CR, that its Driver's prompt holds no `writes:` line, or prints the prompt skeleton per role.
- [chantier] The stack driver read "PR in draft" as "not handed back ready" and stopped before making the forge stack; a second take was needed: `take stack` and `stack` print the hand-back state apart from the PR's draft flag ("ready, PR draft"), and the stack-driver card says it.
- [chantier] The two eval campaigns chosen for v0.11.0 could not start: the app refuses to start the operator session under Remote Control (the new workspace's trust needs the desk); the release shipped with every claim "not exercised" (release): a way to start an eval operator away from the desk (a workspace root the user trusts once), or the release CR waits for the campaigns' reports.
- [chantier] The post-merge release Driver tagged and published but left `release published`, `work/retro.md` and `handback ready` undone until told: the release-driver card lists the end steps as a checklist in its hand-back section.
- [chantier] The steering share was $14.93 (25%) with the Chief of Staff's context averaging 180,000 tokens (peak 266,181) over 60 wakes and 3 compactions, high across batches (batch-17, 18, 21 alike): study handing a long batch's steering to a fresh session at a threshold.

See the release retro: 3-done/307-release-0-11-0/work/retro.md.

Release retro: ../261117-0628-307-release-0-11-0/work/retro.md
