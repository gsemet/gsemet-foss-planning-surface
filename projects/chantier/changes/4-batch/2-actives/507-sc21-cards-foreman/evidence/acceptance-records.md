# Acceptance records

Base: `24111e6d9920a7ff3e8f210613186dd65d802ec8` (origin/main). Head: `03f973e4f0d0756c9b5fa77ed0f888f941745dbe`, plus the uncommitted changes of rounds 7 to 14 unless a line says otherwise.

## `just test`, base and head (Part 1.7, Part 2.8, Part 3.9)

No test is added or changed. Same machine, one run after the other (`work/verify.md`, C25):

```text
base 24111e6d: 2932 passed, 20 skipped in 192.40s (wall 197.9 s)
head 03f973e4:  2932 passed, 20 skipped in 171.16s (wall 172.6 s)
```

0 seconds added; the difference between the two is run-to-run variation, not a speed-up.

`just check` on round 14's working tree (tests beside the other checks, so not a timing comparison): `2933 passed, 19 skipped in 156.49s`.

## Brief bytes beside the old start readings (Part 1.3, Part 2.3)

Old start readings, as the specification gives them (study-fable-v2; not measured again):

| role | declared | measured |
| --- | ---: | ---: |
| Foreman | 91 KB | 144 KB |
| Chief of Staff | 202 KB | 218 KB |
| Griller | 145 KB | 36 KB |

`brief`, batch-31, host claude, today's cards (old) and `--cards <worktree>/skills/chantier/cards-next` (new), the working tree's cards. LF bytes of the brief file (round 10's run, `work/r10/briefs8.py`; a unit's brief also holds the unit's facts from the record, so the `coder` bytes move with it):

```text
foreman | new exit 0 bytes 22276 host claude
foreman | old exit 0 bytes 55206 host claude
chief-of-staff | new exit 0 bytes 24657 host claude
chief-of-staff | old exit 0 bytes 22322 host claude
griller | new exit 0 bytes 6747 host claude
griller | old exit 0 bytes 6349 host claude
foreman --epoch 1 | new exit 0 bytes 22276 host claude
foreman --epoch 1 | old exit 0 bytes 55206 host claude
coder CR-507 | new exit 0 bytes 6569 host claude
coder CR-507 | old exit 0 bytes 9575 host claude
```

| reading | old | new |
| --- | ---: | ---: |
| `brief foreman` | 55,206 | 22,276 |
| `brief chief-of-staff` | 22,322 | 24,657 |
| `brief griller` | 6,349 | 6,747 |
| direct mode: `brief chief-of-staff` + `brief foreman --epoch 1` | 77,528 | 46,933 |

## `just quiz --plan` (Part 1.4, Part 2.4, Part 3.5)

Round 7's run: no case and no `roles.yaml` line changed since, but cards did, so the cost figures are those of round 7's cards. Plan only: `--plan` stops before any model call, so no model run and no spend. `claude-opus-5-5` is the session roles' `--model`, as the Verifier ran it. The three Driver roles cannot be planned on this set: `roles.yaml` names `driver.md`, which `cards-next/` does not hold. The session roles' plans are above the default `--max-usd 10`. `inspector`, `investigator` and `qa-driver` have no folder under `evals/quiz/`.

```text
$ just quiz chief-of-staff griller --model claude-opus-5-5 --plan --cards skills/chantier/cards-next
uv run --locked python evals/kit/quiz.py chief-of-staff griller --model claude-opus-5-5 --plan --cards skills/chantier/cards-next
plan: chief-of-staff 17 cases x 3 runs on claude-opus-5-5 + 51 judge calls on claude-fable-5-2: ~$24.02
plan: griller 1 cases x 3 runs on claude-opus-5-5 + 3 judge calls on claude-fable-5-2: ~$1.32
plan total: 54 runs, ~$25.34 (cap $10)
exit 0
$ just quiz foreman --model claude-opus-5-5 --plan --cards skills/chantier/cards-next
uv run --locked python evals/kit/quiz.py foreman --model claude-opus-5-5 --plan --cards skills/chantier/cards-next
plan: foreman 11 cases x 3 runs on claude-opus-5-5 + 33 judge calls on claude-fable-5-2: ~$15.40
plan total: 33 runs, ~$15.40 (cap $10)
exit 0
$ just quiz coder conflict-resolver debugger demo-explorer verifier --plan --cards skills/chantier/cards-next
uv run --locked python evals/kit/quiz.py coder conflict-resolver debugger demo-explorer verifier --plan --cards skills/chantier/cards-next
plan: coder 3 cases x 3 runs on claude-sonnet-5-5 + 9 judge calls on claude-fable-5-2: ~$3.19
plan: conflict-resolver 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.06
plan: debugger 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.06
plan: demo-explorer 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.06
plan: verifier 2 cases x 3 runs on claude-sonnet-5-5 + 6 judge calls on claude-fable-5-2: ~$2.13
plan total: 24 runs, ~$8.51 (cap $10)
exit 0
$ just quiz cr-driver --plan --cards skills/chantier/cards-next
uv run --locked python evals/kit/quiz.py cr-driver --plan --cards skills/chantier/cards-next
error: brief: cannot read <worktree>/skills/chantier/cards-next/driver.md: No such file or directory
quiz.py: `chantier brief cr-driver` exited 2
error: recipe `quiz` failed on line 41 with exit code 1
exit 1
$ just quiz release-driver --plan --cards skills/chantier/cards-next
uv run --locked python evals/kit/quiz.py release-driver --plan --cards skills/chantier/cards-next
error: brief: cannot read <worktree>/skills/chantier/cards-next/driver.md: No such file or directory
quiz.py: `chantier brief release-driver` exited 2
error: recipe `quiz` failed on line 41 with exit code 1
exit 1
$ just quiz stack-driver --plan --cards skills/chantier/cards-next
uv run --locked python evals/kit/quiz.py stack-driver --plan --cards skills/chantier/cards-next
error: brief: cannot read <worktree>/skills/chantier/cards-next/driver.md: No such file or directory
quiz.py: `chantier brief stack-driver` exited 2
error: recipe `quiz` failed on line 41 with exit code 1
exit 1
```

## `git diff origin/main -- skills/chantier/cards-next/griller.md` (Part 2.1)

```diff
diff --git a/skills/chantier/cards-next/griller.md b/skills/chantier/cards-next/griller.md
index 6e6b3d39..460dcbd9 100644
--- a/skills/chantier/cards-next/griller.md
+++ b/skills/chantier/cards-next/griller.md
@@ -4,11 +4,11 @@
 
 The surface server starts you headless, one run per message typed in the web board, each resumed from the run before. The conversation is shared by every holder of the private key: the words may come from more than one person. You take no seat and start no watcher, server or hub.
 
-Your brief names the CR's folder (the inbox, `2-backlog/P1` to `P4` or `3-ready`): you grill that CR only, and re-read its folder at each run. You may read the project, the planning folder and the plugin's skill folder, nothing else. You write only in that CR's folder.
+Your brief names the CR's folder (the inbox, `2-backlog/P1` to `P4` or `3-ready`): you grill that CR only, and re-read its folder at each run. You may read the project, the planning folder and the plugin's skill folder, nothing else. You write only in that CR's folder, never a secret or personal data.
 
 You run only these commands, and no other `chantier` command: `$CHANTIER rules`, `$CHANTIER access`, `$CHANTIER summary lint <the CR's folder>` and `$CHANTIER summary set <the CR's folder> ...`. A tool your limits refuse: say it in one line, never go another way.
 
-You grill that CR: questions in the user's language, each answer recorded in `02-answers.md` at once, a restatement before you ask "grilled enough?"; at "grilled enough" you ask and record the destination (next batch or running batch).
+You grill that CR: questions in the user's language, each answer recorded in `02-answers.md` at once, a restatement before you ask "grilled enough?"; at "grilled enough" you ask and record the destination (next batch or running batch). How you grill is `griller-skill.md`'s `## How you grill`, read by its path; the limits of this section override it where they differ.
 
 You never:
 - open, pause, order or steer anything, run a git command or message a session;
```

## `git diff --stat origin/main` (Part 1.1, Part 2.1, Part 3.1)

Every path is under `skills/chantier/cards-next/` but the 9 under `evals/quiz/`. `--stat=200` keeps the paths whole.

```text
 evals/quiz/chief-of-staff/a8-ask-delete.json                    |    9 +
 evals/quiz/chief-of-staff/a8-ask-release.json                   |    9 +
 evals/quiz/chief-of-staff/a8-ask-stop-process.json              |    9 +
 evals/quiz/chief-of-staff/a8-chained-subcommand-refused.json    |    9 +
 evals/quiz/chief-of-staff/a8-gh-pr-edit-base-refused.json       |    9 +
 evals/quiz/chief-of-staff/a8-gh-pr-ready-refused.json           |    9 +
 evals/quiz/chief-of-staff/a8-push-refused-cr-branch.json        |   10 +
 evals/quiz/chief-of-staff/a8-push-refused-default-branch.json   |    9 +
 evals/quiz/chief-of-staff/a8-rebase-refused-cr-branch.json      |    9 +
 skills/chantier/cards-next/chief-of-staff.md                    |   41 +++
 skills/chantier/cards-next/coder.md                             |    1 +
 skills/chantier/cards-next/concepts.md                          |  147 +++++++++
 skills/chantier/cards-next/conflict-resolver.md                 |    1 +
 skills/chantier/cards-next/cr-driver.md                         |    9 +-
 skills/chantier/cards-next/debugger.md                          |    1 +
 skills/chantier/cards-next/demo-explorer.md                     |    1 +
 skills/chantier/cards-next/foreman.md                           |   38 +++
 skills/chantier/cards-next/forges/github.md                     |   11 +
 skills/chantier/cards-next/forges/gitlab.md                     |   11 +
 skills/chantier/cards-next/griller-skill.md                     |   31 ++
 skills/chantier/cards-next/griller.md                           |    4 +-
 skills/chantier/cards-next/hosts/claude-code.json               |  697 +++++++++++++++++++++++++++++++++++++++++++
 skills/chantier/cards-next/hosts/claude-code.md                 |  158 ++++++++++
 skills/chantier/cards-next/hosts/copilot.json                   |  687 ++++++++++++++++++++++++++++++++++++++++++
 skills/chantier/cards-next/init.md                              |   42 +++
 skills/chantier/cards-next/inspector.md                         |    4 +-
 skills/chantier/cards-next/investigator.md                      |    1 +
 skills/chantier/cards-next/pr-template.md                       |  138 +++++++++
 skills/chantier/cards-next/qa-driver.md                         |    4 +-
 skills/chantier/cards-next/release-driver.md                    |   11 +-
 skills/chantier/cards-next/release-template.md                  |   81 +++++
 skills/chantier/cards-next/retro-critic.md                      |    2 +
 skills/chantier/cards-next/review-step.md                       |   18 ++
 skills/chantier/cards-next/routing.md                           |   36 +++
 skills/chantier/cards-next/skills/chantier-SKILL.md             |   30 ++
 skills/chantier/cards-next/skills/chief-of-staff-SKILL.md       |   35 +++
 skills/chantier/cards-next/skills/griller-SKILL.md              |   32 ++
 skills/chantier/cards-next/skills/status-SKILL.md               |   39 +++
 skills/chantier/cards-next/spec-critic.md                       |    2 +
 skills/chantier/cards-next/spec-writer.md                       |    4 +-
 skills/chantier/cards-next/stack-driver.md                      |   10 +-
 skills/chantier/cards-next/status-layout.md                     |   90 ++++++
 skills/chantier/cards-next/sync-checkout.md                     |   21 ++
 skills/chantier/cards-next/ticket-summary-example.md            |   44 +++
 skills/chantier/cards-next/topics.json                          | 2079 ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++-
 skills/chantier/cards-next/topics/allow-rules-more-p1.md        |    7 +
 skills/chantier/cards-next/topics/allow-rules-more-p2.md        |    3 +
 skills/chantier/cards-next/topics/allow-rules.md                |    7 +
 skills/chantier/cards-next/topics/ask-lines.md                  |   17 ++
 skills/chantier/cards-next/topics/asks.md                       |    3 +
 skills/chantier/cards-next/topics/batch-close-p1.md             |    4 +
 skills/chantier/cards-next/topics/batch-close-p2.md             |    4 +
 skills/chantier/cards-next/topics/batch-close-stopped-p1.md     |    7 +
 skills/chantier/cards-next/topics/batch-close-stopped-p2.md     |    5 +
 skills/chantier/cards-next/topics/batch-pause.md                |    6 +
 skills/chantier/cards-next/topics/batch-plan-cut-p1.md          |    4 +
 skills/chantier/cards-next/topics/batch-plan-cut-p2.md          |    5 +
 skills/chantier/cards-next/topics/batch-plan-mode-p1.md         |    4 +
 skills/chantier/cards-next/topics/batch-plan-mode-p2.md         |    5 +
 skills/chantier/cards-next/topics/batch-plan-mode-p3.md         |    5 +
 skills/chantier/cards-next/topics/batch-plan-show-p1.md         |    3 +
 skills/chantier/cards-next/topics/batch-plan-show-p2.md         |    5 +
 skills/chantier/cards-next/topics/batch-plan.md                 |    7 +
 skills/chantier/cards-next/topics/board-lines.md                |    9 +
 skills/chantier/cards-next/topics/board-p1.md                   |    7 +
 skills/chantier/cards-next/topics/board-p2.md                   |    4 +
 skills/chantier/cards-next/topics/board-restart.md              |    9 +
 skills/chantier/cards-next/topics/chain-conflict.md             |    4 +
 skills/chantier/cards-next/topics/chain.md                      |    5 +
 skills/chantier/cards-next/topics/cleanup.md                    |    4 +
 skills/chantier/cards-next/topics/compacting-p1.md              |    5 +
 skills/chantier/cards-next/topics/compacting-p2.md              |    3 +
 skills/chantier/cards-next/topics/config-p1.md                  |    3 +
 skills/chantier/cards-next/topics/config-p2.md                  |    4 +
 skills/chantier/cards-next/topics/config-p3.md                  |    5 +
 skills/chantier/cards-next/topics/conflict-check.md             |    6 +
 skills/chantier/cards-next/topics/cost.md                       |    3 +
 skills/chantier/cards-next/topics/cr-review-step.md             |   17 ++
 skills/chantier/cards-next/topics/cr-rounds.md                  |    2 +-
 skills/chantier/cards-next/topics/delivery-time-p1.md           |    7 +
 skills/chantier/cards-next/topics/delivery-time-p2.md           |    6 +
 skills/chantier/cards-next/topics/demo-p1.md                    |    5 +
 skills/chantier/cards-next/topics/demo-p2.md                    |    4 +
 skills/chantier/cards-next/topics/direct-mode-accept-p1.md      |    7 +
 skills/chantier/cards-next/topics/direct-mode-accept-p2.md      |    4 +
 skills/chantier/cards-next/topics/direct-mode-back.md           |    7 +
 skills/chantier/cards-next/topics/direct-mode-epoch-p1.md       |    3 +
 skills/chantier/cards-next/topics/direct-mode-epoch-p2.md       |    4 +
 skills/chantier/cards-next/topics/direct-mode-p1.md             |    6 +
 skills/chantier/cards-next/topics/direct-mode-p2.md             |    6 +
 skills/chantier/cards-next/topics/direct-mode-p3.md             |    4 +
 skills/chantier/cards-next/topics/direct-mode-switch-p1.md      |    5 +
 skills/chantier/cards-next/topics/direct-mode-switch-p2.md      |    5 +
 skills/chantier/cards-next/topics/direct-mode-switch-p3.md      |    3 +
 skills/chantier/cards-next/topics/direct-mode-switch-p4.md      |    6 +
 skills/chantier/cards-next/topics/driver-question.md            |    7 +
 skills/chantier/cards-next/topics/drop.md                       |    6 +
 skills/chantier/cards-next/topics/escalation.md                 |    7 +
 skills/chantier/cards-next/topics/first-turn-p1.md              |    7 +
 skills/chantier/cards-next/topics/first-turn-p2.md              |    6 +
 skills/chantier/cards-next/topics/foreman-start-more.md         |    5 +
 skills/chantier/cards-next/topics/foreman-start-p1.md           |    3 +
 skills/chantier/cards-next/topics/foreman-start-p2.md           |    4 +
 skills/chantier/cards-next/topics/forge-permissions-gitlab.md   |    8 +
 skills/chantier/cards-next/topics/forge-permissions-p1.md       |    8 +
 skills/chantier/cards-next/topics/forge-permissions-p2.md       |    6 +
 skills/chantier/cards-next/topics/forge-permissions-say.md      |    3 +
 skills/chantier/cards-next/topics/grill-backlog-p1.md           |    6 +
 skills/chantier/cards-next/topics/grill-backlog-p2.md           |    4 +
 skills/chantier/cards-next/topics/grill-critic-steps.md         |    8 +
 skills/chantier/cards-next/topics/grill-critic.md               |    6 +
 skills/chantier/cards-next/topics/grill-example.md              |   26 ++
 skills/chantier/cards-next/topics/grill-options.md              |    7 +
 skills/chantier/cards-next/topics/grill-outside-pr.md           |    7 +
 skills/chantier/cards-next/topics/grill-restate.md              |    6 +
 skills/chantier/cards-next/topics/grill-series.md               |    9 +
 skills/chantier/cards-next/topics/grill-specify-p1.md           |    7 +
 skills/chantier/cards-next/topics/grill-specify-p2.md           |    5 +
 skills/chantier/cards-next/topics/grill-surface.md              |    6 +
 skills/chantier/cards-next/topics/griller-cost.md               |    3 +
 skills/chantier/cards-next/topics/griller-worktree.md           |    5 +
 skills/chantier/cards-next/topics/handover.md                   |    4 +
 skills/chantier/cards-next/topics/hold.md                       |    9 +
 skills/chantier/cards-next/topics/host-allow-add-lines.md       |   16 +
 skills/chantier/cards-next/topics/host-allow-add.md             |   18 ++
 skills/chantier/cards-next/topics/host-allow-broad.md           |   19 ++
 skills/chantier/cards-next/topics/host-allow-extra.md           |    9 +
 skills/chantier/cards-next/topics/host-allow-not-add.md         |    9 +
 skills/chantier/cards-next/topics/host-allow-rules-copilot.md   |    7 +
 skills/chantier/cards-next/topics/host-allow-rules.md           |   23 ++
 skills/chantier/cards-next/topics/host-auto-fix.md              |   22 ++
 skills/chantier/cards-next/topics/host-auto-mode-steering.md    |   20 ++
 skills/chantier/cards-next/topics/host-auto-mode-trials.md      |   20 ++
 skills/chantier/cards-next/topics/host-auto-mode.md             |   19 ++
 skills/chantier/cards-next/topics/host-claude-only.md           |    4 +
 skills/chantier/cards-next/topics/host-compact-copilot.md       |    6 +
 skills/chantier/cards-next/topics/host-compact.md               |   20 ++
 skills/chantier/cards-next/topics/host-configuration-copilot.md |   19 ++
 skills/chantier/cards-next/topics/host-configuration.md         |   19 ++
 skills/chantier/cards-next/topics/host-driver-silence.md        |   18 ++
 skills/chantier/cards-next/topics/host-for-you-sessions.md      |   13 +
 skills/chantier/cards-next/topics/host-for-you.md               |   19 ++
 skills/chantier/cards-next/topics/host-foreman-worktree.md      |    8 +
 skills/chantier/cards-next/topics/host-heartbeat-copilot.md     |   16 +
 skills/chantier/cards-next/topics/host-heartbeat.md             |   17 ++
 skills/chantier/cards-next/topics/host-refused.md               |   19 ++
 skills/chantier/cards-next/topics/host-remote.md                |   19 ++
 skills/chantier/cards-next/topics/host-reuse-foreman.md         |   14 +
 skills/chantier/cards-next/topics/host-sessions-copilot.md      |    8 +
 skills/chantier/cards-next/topics/host-sessions-more.md         |   16 +
 skills/chantier/cards-next/topics/host-sessions.md              |   17 ++
 skills/chantier/cards-next/topics/host-subagent-signs.md        |   18 ++
 skills/chantier/cards-next/topics/host-surfaces.md              |   21 ++
 skills/chantier/cards-next/topics/host-turn-end.md              |   20 ++
 skills/chantier/cards-next/topics/host-write-guard-shell.md     |   16 +
 skills/chantier/cards-next/topics/host-write-guard.md           |   16 +
 skills/chantier/cards-next/topics/init-checks.md                |    8 +
 skills/chantier/cards-next/topics/init-tools.md                 |    7 +
 skills/chantier/cards-next/topics/lease-steering.md             |   10 +
 skills/chantier/cards-next/topics/lease.md                      |    4 +-
 skills/chantier/cards-next/topics/local-gate.md                 |    8 +
 skills/chantier/cards-next/topics/long-gate-waiver.md           |    5 +
 skills/chantier/cards-next/topics/long-gate.md                  |    8 +
 skills/chantier/cards-next/topics/lost-context.md               |    5 +
 skills/chantier/cards-next/topics/lost-driver.md                |    9 +
 skills/chantier/cards-next/topics/lost-outside.md               |    8 +
 skills/chantier/cards-next/topics/lost-restart.md               |    7 +
 skills/chantier/cards-next/topics/lost-silent.md                |    6 +
 skills/chantier/cards-next/topics/main-checkout-p1.md           |    3 +
 skills/chantier/cards-next/topics/main-checkout-p2.md           |    9 +
 skills/chantier/cards-next/topics/merge-gaps-p1.md              |    6 +
 skills/chantier/cards-next/topics/merge-gaps-p2.md              |    7 +
 skills/chantier/cards-next/topics/merge-github.md               |    3 +
 skills/chantier/cards-next/topics/merge-recorded.md             |    7 +
 skills/chantier/cards-next/topics/merge-series-stack-p1.md      |    5 +
 skills/chantier/cards-next/topics/merge-series-stack-p2.md      |    4 +
 skills/chantier/cards-next/topics/merge-stack-gitlab.md         |    5 +
 skills/chantier/cards-next/topics/merge-stack-ready-p1.md       |    5 +
 skills/chantier/cards-next/topics/merge-stack-ready-p2.md       |    6 +
 skills/chantier/cards-next/topics/merge-under-grant.md          |    7 +
 skills/chantier/cards-next/topics/merge-words-p1.md             |    4 +
 skills/chantier/cards-next/topics/merge-words-p2.md             |    4 +
 skills/chantier/cards-next/topics/merge.md                      |   11 +
 skills/chantier/cards-next/topics/mode-switch-p1.md             |    8 +
 skills/chantier/cards-next/topics/mode-switch-p2.md             |    8 +
 skills/chantier/cards-next/topics/options.md                    |    7 +
 skills/chantier/cards-next/topics/order-drop.md                 |    6 +
 skills/chantier/cards-next/topics/order-verbs-p1.md             |    7 +
 skills/chantier/cards-next/topics/order-verbs-p2.md             |   12 +
 skills/chantier/cards-next/topics/orders-queue.md               |    5 +
 skills/chantier/cards-next/topics/orders.md                     |    8 +
 skills/chantier/cards-next/topics/park-back.md                  |    5 +
 skills/chantier/cards-next/topics/park.md                       |    8 +
 skills/chantier/cards-next/topics/pr-extras.md                  |   10 +-
 skills/chantier/cards-next/topics/pr-gitlab.md                  |    4 +-
 skills/chantier/cards-next/topics/pr-template-own.md            |    3 +
 skills/chantier/cards-next/topics/project-rules-p1.md           |    6 +
 skills/chantier/cards-next/topics/project-rules-p2.md           |    4 +
 skills/chantier/cards-next/topics/qa-order.md                   |    3 +
 skills/chantier/cards-next/topics/ready-asks.md                 |    3 +
 skills/chantier/cards-next/topics/recovery.md                   |    6 +
 skills/chantier/cards-next/topics/refusals-to-say-more.md       |    6 +
 skills/chantier/cards-next/topics/refusals-to-say-p1.md         |    6 +
 skills/chantier/cards-next/topics/refusals-to-say-p2.md         |    3 +
 skills/chantier/cards-next/topics/refused-answer.md             |    6 +
 skills/chantier/cards-next/topics/refused-forge-chain.md        |    5 +
 skills/chantier/cards-next/topics/refused-push-chief-more-p1.md |    4 +
 skills/chantier/cards-next/topics/refused-push-chief-more-p2.md |    4 +
 skills/chantier/cards-next/topics/refused-push-chief-p1.md      |    6 +
 skills/chantier/cards-next/topics/refused-push-chief-p2.md      |    3 +
 skills/chantier/cards-next/topics/refused-push-gate.md          |    6 +
 skills/chantier/cards-next/topics/refused-push-judgement.md     |    8 +
 skills/chantier/cards-next/topics/refused-push-route.md         |    6 +
 skills/chantier/cards-next/topics/refused-push-run.md           |    6 +
 skills/chantier/cards-next/topics/refused-push-steering.md      |    7 +
 skills/chantier/cards-next/topics/refused-rebase-chief.md       |    6 +
 skills/chantier/cards-next/topics/refused-rebase-run.md         |    5 +
 skills/chantier/cards-next/topics/refused-rebase.md             |    6 +
 skills/chantier/cards-next/topics/release-chief-after-p1.md     |    4 +
 skills/chantier/cards-next/topics/release-chief-after-p2.md     |    5 +
 skills/chantier/cards-next/topics/release-chief-approve-p1.md   |    6 +
 skills/chantier/cards-next/topics/release-chief-approve-p2.md   |    3 +
 skills/chantier/cards-next/topics/release-chief-auto-p1.md      |    7 +
 skills/chantier/cards-next/topics/release-chief-auto-p2.md      |    4 +
 skills/chantier/cards-next/topics/release-chief-p1.md           |    4 +
 skills/chantier/cards-next/topics/release-chief-p2.md           |    5 +
 skills/chantier/cards-next/topics/release-evidence.md           |    9 +
 skills/chantier/cards-next/topics/release-notes.md              |   10 +-
 skills/chantier/cards-next/topics/release-stale.md              |    6 +
 skills/chantier/cards-next/topics/release-tag.md                |    4 +
 skills/chantier/cards-next/topics/release-take.md               |    6 +
 skills/chantier/cards-next/topics/release-thread.md             |    3 +
 skills/chantier/cards-next/topics/reload.md                     |    3 +
 skills/chantier/cards-next/topics/remote-login.md               |    5 +
 skills/chantier/cards-next/topics/retro-critic-write.md         |    5 +
 skills/chantier/cards-next/topics/retro-critic.md               |    6 +
 skills/chantier/cards-next/topics/retro-lines.md                |    5 +
 skills/chantier/cards-next/topics/retro-route-chantier-p1.md    |    8 +
 skills/chantier/cards-next/topics/retro-route-chantier-p2.md    |    4 +
 skills/chantier/cards-next/topics/retro-route-p1.md             |    5 +
 skills/chantier/cards-next/topics/retro-route-p2.md             |    4 +
 skills/chantier/cards-next/topics/retro.md                      |    6 +
 skills/chantier/cards-next/topics/rounds-exception.md           |    3 +
 skills/chantier/cards-next/topics/seat-handover.md              |    8 +
 skills/chantier/cards-next/topics/seat-p1.md                    |    5 +
 skills/chantier/cards-next/topics/seat-p2.md                    |    7 +
 skills/chantier/cards-next/topics/session-shell-p1.md           |    6 +
 skills/chantier/cards-next/topics/session-shell-p2.md           |    7 +
 skills/chantier/cards-next/topics/session-start-surface-p1.md   |    7 +
 skills/chantier/cards-next/topics/session-start-surface-p2.md   |    3 +
 skills/chantier/cards-next/topics/session-start.md              |    5 +
 skills/chantier/cards-next/topics/stack-asks.md                 |    6 +
 skills/chantier/cards-next/topics/stack-changes-chief-p1.md     |    4 +
 skills/chantier/cards-next/topics/stack-changes-chief-p2.md     |    3 +
 skills/chantier/cards-next/topics/stack-checks.md               |    7 +
 skills/chantier/cards-next/topics/stack-deliver.md              |    4 +
 skills/chantier/cards-next/topics/stack-drop.md                 |    4 +
 skills/chantier/cards-next/topics/stack-ends.md                 |    5 +
 skills/chantier/cards-next/topics/stack-grows.md                |    6 +
 skills/chantier/cards-next/topics/stack-merge.md                |    8 +
 skills/chantier/cards-next/topics/stack-outside.md              |    5 +
 skills/chantier/cards-next/topics/stack-run.md                  |    5 +
 skills/chantier/cards-next/topics/stack-takes.md                |    5 +
 skills/chantier/cards-next/topics/stack.md                      |    7 +
 skills/chantier/cards-next/topics/status-notes-more.md          |    6 +
 skills/chantier/cards-next/topics/status-notes.md               |    5 +
 skills/chantier/cards-next/topics/steering-reports-p1.md        |    6 +
 skills/chantier/cards-next/topics/steering-reports-p2.md        |    4 +
 skills/chantier/cards-next/topics/sync-offer-p1.md              |   16 +
 skills/chantier/cards-next/topics/sync-offer-p2.md              |   13 +
 skills/chantier/cards-next/topics/take-back.md                  |    7 +
 skills/chantier/cards-next/topics/ticket-summary-p1.md          |    7 +
 skills/chantier/cards-next/topics/ticket-summary-p2.md          |    7 +
 skills/chantier/cards-next/topics/ticket-summary-post-p1.md     |    9 +
 skills/chantier/cards-next/topics/ticket-summary-post-p2.md     |    5 +
 skills/chantier/cards-next/topics/titles.md                     |    8 +
 skills/chantier/cards-next/topics/trials-p1.md                  |    6 +
 skills/chantier/cards-next/topics/trials-p2.md                  |    4 +
 skills/chantier/cards-next/topics/trouble-gate.md               |    2 +-
 skills/chantier/cards-next/topics/wakes-forge.md                |    6 +
 skills/chantier/cards-next/topics/wakes-p1.md                   |    6 +
 skills/chantier/cards-next/topics/wakes-p2.md                   |    4 +
 skills/chantier/cards-next/topics/watcher-board-p1.md           |    6 +
 skills/chantier/cards-next/topics/watcher-board-p2.md           |    4 +
 skills/chantier/cards-next/topics/watcher-events-p1.md          |    5 +
 skills/chantier/cards-next/topics/watcher-events-p2.md          |    7 +
 skills/chantier/cards-next/topics/watcher-lines-p1.md           |    5 +
 skills/chantier/cards-next/topics/watcher-lines-p2.md           |    6 +
 skills/chantier/cards-next/topics/watcher-pull.md               |    6 +
 skills/chantier/cards-next/topics/watcher.md                    |    7 +
 skills/chantier/cards-next/topics/where-cr-goes.md              |    8 +
 skills/chantier/cards-next/topics/worker-shell.md               |    4 +-
 skills/chantier/cards-next/topics/writer-off.md                 |    5 +
 skills/chantier/cards-next/topics/writer.md                     |    9 +
 skills/chantier/cards-next/verifier.md                          |    1 +
 295 files changed, 6405 insertions(+), 42 deletions(-)
```
