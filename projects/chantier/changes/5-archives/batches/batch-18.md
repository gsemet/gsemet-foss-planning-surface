# batch-18

Opened 2026-11-14T18:41:48Z, closed 2026-11-15T16:18:18Z, parallel, steered by Foreman, budget $450, final cost $183.92. [batch-18.json](batch-18.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-253](../261115-0000-253-baseline-and-legacy/) | Change Specification: a green long gate on main, and no backward compatibility | merged | https://github.com/gsemet/chantier/pull/206 | 4 | $6.25 |
| [CR-254](../261115-0056-254-fast-scenario/) | `just scenario` under 5 minutes: independent units run in parallel | merged | https://github.com/gsemet/chantier/pull/211 | 5 | $12.49 |
| [CR-255](../261115-0740-255-epoch-required-everywhere/) | Change Specification: every steering command refuses a missing `--epoch` | merged | https://github.com/gsemet/chantier/pull/213 | 2 | $6.02 |
| [CR-256](../261114-2334-256-worker-reply-length/) | Change Specification: workers reply in an exact template, and `verdict` names its words | merged | https://github.com/gsemet/chantier/pull/202 | 1 | $1.88 |
| [CR-257](../261115-0740-257-cr-folder-self-contained/) | Change Specification: a CR's folder is self-contained | merged | https://github.com/gsemet/chantier/pull/203 | 1 | $4.66 |
| [CR-258](../261114-2145-258-push-refusal-lessons/) | Change Specification: a refused force push is recorded with its exact text, and its Driver hands back instead of waiting | merged | https://github.com/gsemet/chantier/pull/204 | 1 | $1.83 |
| [CR-259](../261115-0740-259-retro-critic/) | Change Specification: a retro critic cuts every list of changes chantier proposes on its own | merged | https://github.com/gsemet/chantier/pull/207 | 2 | $4.35 |
| [CR-260](../261114-2015-260-driver-opening-reads/) | Change Specification: a Driver's opening reads cost a third less | merged | https://github.com/gsemet/chantier/pull/201 | 1 | $1.50 |
| [CR-261](../261115-0740-261-board-cr-step/) | Change Specification: each working CR shows the step it is at, and the board shows the next CR to start | merged | https://github.com/gsemet/chantier/pull/208 | 4 | $5.18 |
| [CR-262](../261115-0740-262-board-ui-review/) | Change Specification: the web board after the user's first page-by-page tour | merged | https://github.com/gsemet/chantier/pull/209 | 2 | $7.64 |
| [CR-263](../261115-0740-263-b17-card-fixes/) | Change Specification: batch-17 retro, card fixes | merged | https://github.com/gsemet/chantier/pull/205 | 1 | $4.10 |
| [CR-264](../261115-0740-264-b17-cli-fixes/) | Change Specification: batch-17 CLI fixes | merged | https://github.com/gsemet/chantier/pull/210 | 1 | $5.77 |
| [CR-265](../261115-0740-265-gate-rules/) | Change Specification: three long-gate rules (the next merge first, early push, clean rebase) | merged | https://github.com/gsemet/chantier/pull/214 | 1 | $3.51 |
| [CR-266](../261115-0740-266-stack-gate-waiver/) | Change Specification: the stack's one long gate, and a long-gate waiver recorded per CR | merged | https://github.com/gsemet/chantier/pull/215 | 3 | $10.78 |
| [CR-267](../261115-0740-267-batch-mode-switch/) | A running batch switches between any two modes | merged | https://github.com/gsemet/chantier/pull/212 | 1 | $3.94 |
| [CR-268](../261115-0855-268-gate-race-on-merge/) | Change Specification: `order merged` stops the CR's gate before it moves the folder | merged | https://github.com/gsemet/chantier/pull/218 | 1 | $1.63 |
| [CR-269](../261115-0924-269-gate-on-pipeline/) | Change Specification: a project's rule may name a pipeline job as its long gate | merged | https://github.com/gsemet/chantier/pull/220 | 1 | $1.32 |
| [CR-270](../261115-0953-270-ship-reads-forge/) | `ship` always reads the PR's base and draft state from the forge | merged | https://github.com/gsemet/chantier/pull/222 | 1 | $3.94 |
| [CR-271](../261115-0939-271-early-conflicts/) | Change Specification: the Foreman finds a conflict between ready PRs at the second one | merged | https://github.com/gsemet/chantier/pull/221 | 1 | $2.10 |
| [CR-272](../261115-0858-272-ask-supersedes/) | Change Specification: a CR's new readiness ask supersedes its earlier one | merged | https://github.com/gsemet/chantier/pull/217 | 1 | $1.19 |
| [CR-273](../261115-0924-273-verdict-head/) | Change Specification: `verdict VERIFIED` refuses a verify note that does not name the head | merged | https://github.com/gsemet/chantier/pull/219 | 1 | $1.49 |
| [CR-274](../261115-0939-274-workers-read-card/) | Change Specification: every worker reads its card before it works | merged | https://github.com/gsemet/chantier/pull/223 | 1 | $2.05 |
| [CR-275](../261115-1352-275-evals-run-b18/) | Change Specification: run the real-foreman and real-direct evals on the chantier batch-18 leaves on main | merged | https://github.com/gsemet/chantier/pull/225 | 1 | $3.70 |
| [CR-276](../261115-1409-276-eval-cost-readme/) | Change Specification: the README says what a batch costs, Foreman or direct | merged | https://github.com/gsemet/chantier/pull/226 | 1 | $1.17 |
| [CR-277](../261115-1521-277-stacked-ready-line-names-cr/) | Change Specification: the ready line of a stacked CR names the CR it waits on | merged | https://github.com/gsemet/chantier/pull/231 | 1 | $1.74 |
| [CR-278](../261115-1433-278-paused-batch-messages/) | Change Specification: commands name a paused batch and the way out | merged | https://github.com/gsemet/chantier/pull/229 | 1 | $1.68 |
| [CR-279](../261115-1521-279-spend-fresh-at-budget-check/) | Change Specification: the spend is fresh when the budget is checked | merged | https://github.com/gsemet/chantier/pull/233 | 1 | $2.85 |
| [CR-280](../261115-1433-280-direct-mode-cost-report/) | Change Specification: direct mode's cost report says "Chief of Staff" and its lines add up | merged | https://github.com/gsemet/chantier/pull/230 | 1 | $1.65 |
| [CR-281](../261115-1410-281-release-merge-native-stack/) | chantier's merge route works for a PR of a native GitHub stack | merged | https://github.com/gsemet/chantier/pull/227 | 1 | $1.29 |
| [CR-282](../261115-1525-282-scenario-stack-unit-budget/) | The scenario's stack unit fits its budget | merged | https://github.com/gsemet/chantier/pull/238 | 3 | $4.74 |
| [CR-283](../261115-1433-283-eval-judge-follows-pr-head/) | Change Specification: the eval judge follows a PR whose head was replaced | merged | https://github.com/gsemet/chantier/pull/228 | 1 | $1.27 |
| [CR-284](../261115-1433-284-eval-audit-no-false-fails/) | Change Specification: the eval audit gives no false FAIL | merged | https://github.com/gsemet/chantier/pull/232 | 1 | $1.60 |
| [CR-285](../261115-1559-285-eval-sandbox-restack-wait/) | The sandbox merge waits for the restack's checks | merged | https://github.com/gsemet/chantier/pull/236 | 2 | $4.26 |
| [CR-286](../261115-1524-286-write-guard-git-bash-paths/) | Change Specification: the write guard reads Git Bash paths | merged | https://github.com/gsemet/chantier/pull/234 | 1 | $0.90 |
| [CR-287](../261115-1540-287-stack-driver-when-stack-forms/) | Change Specification: the stack driver starts when the stack can form | merged | https://github.com/gsemet/chantier/pull/242 | 1 | $4.33 |
| [CR-288](../261115-1521-288-campaign-exercises-release/) | Change Specification: the eval campaign exercises what a release claims | merged | https://github.com/gsemet/chantier/pull/235 | 1 | $1.20 |
| [CR-289](../261115-1521-289-driver-handback-and-context/) | Change Specification: a Driver always hands back, within its context | merged | https://github.com/gsemet/chantier/pull/239 | 1 | $1.67 |
| [CR-290](../261115-1521-290-clean-rebase-light-verify/) | Change Specification: a clean rebase carries the Verifier's verdict | merged | https://github.com/gsemet/chantier/pull/240 | 1 | $2.77 |
| [CR-291](../261115-1604-291-short-worker-cards/) | One short card per worker role | merged | https://github.com/gsemet/chantier/pull/244 | 2 | $2.56 |
| [CR-292](../261115-1536-292-cos-quiet-on-foreman-turns/) | The Chief of Staff stays quiet on a Foreman's turn end | merged | https://github.com/gsemet/chantier/pull/237 | 1 | $1.68 |
| [CR-293](../261115-1524-293-evals-self-sufficient/) | The evals folder is self-sufficient: anyone can run a campaign from it | merged | https://github.com/gsemet/chantier/pull/243 | 1 | $3.47 |
| [CR-294](../261115-1536-294-close-sees-finished-agent/) | close sees a finished agent as finished | merged | https://github.com/gsemet/chantier/pull/241 | 2 | $4.14 |

## Cost

- Total: $183.92 of a $450 budget
- Foreman $41.38 (22%), Drivers $63.52 (35%), workers $79.02 (43%)
- Most: CR-254 $12.49, CR-266 $10.78, CR-262 $7.64
- Foreman: 226 wakes, context 166,848 tokens on average, 265,766 at its peak
- Driver chantier:cr-driver with its workers: $142.29 (6092 calls)
- Driver chantier:stack-driver with its workers: $0.26 (8 calls)
- Chief of Staff, steering the batch (outside the budget): $49.39 since the batch opened (760 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $45.92 since the batch opened (1039 calls, 34 spec-writers, 0 spec critics)
- Chief of Staff, whole session: $694.33, context 236,151 tokens; not counted: 6 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)
- Declared stopped on the user's word: agent-aa7881ed0014ba980 (its last record is a prompt with no answer yet)

## Retro

# Retro

## 2026-11-15 — batch-18, CR-253 to CR-267

- retro not checked: the agent type chantier:retro-critic is not loaded in the Foreman's session (it landed with CR-259, merged this pause; agent files load at the next session); the 14 drafted points are in retro-dropped.md
