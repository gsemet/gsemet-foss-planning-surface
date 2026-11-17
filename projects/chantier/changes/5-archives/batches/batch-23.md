# batch-23

Opened 2026-11-17T10:11:33Z, closed 2026-11-17T14:32:40Z, stack, steered by Foreman, budget $200, final cost $63.94. [batch-23.json](batch-23.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-308](../261117-1028-308-just-check-scripts-format/) | Change Specification: `just check` format-checks `scripts` | merged | https://github.com/gsemet/chantier/pull/261 | 1 | $0.83 |
| [CR-309](../261117-1053-309-just-test-budget/) | `just test` back within its budget | merged | https://github.com/gsemet/chantier/pull/265 | 1 | $2.09 |
| [CR-315](../261117-1351-315-take-prompt-skeleton-per-role/) | Change Specification: `take` prints each Driver role's prompt skeleton | merged | https://github.com/gsemet/chantier/pull/270 | 1 | $4.41 |
| [CR-310](../261117-1103-310-release-driver-end-checklist/) | The release Driver's end steps as a checklist | merged | https://github.com/gsemet/chantier/pull/262 | 1 | $0.83 |
| [CR-316](../261117-1351-316-close-batch-agents-only/) | Change Specification: `close` judges only the batch's own agents | merged | https://github.com/gsemet/chantier/pull/272 | 1 | $4.18 |
| [CR-311](../261117-1103-311-screenshot-made-up-paths/) | Change Specification: images use made-up paths, checked before they are kept or uploaded | merged | https://github.com/gsemet/chantier/pull/263 | 1 | $1.14 |
| [CR-317](../261117-1351-317-auto-pause-last-merge/) | Change Specification: the batch pauses when its last CR ends, and the close is offered | merged | https://github.com/gsemet/chantier/pull/277 | 6 | $7.35 |
| [CR-312](../261117-1130-312-eval-operator-away-from-desk/) | Change Specification: evals that start away from the desk | merged | https://github.com/gsemet/chantier/pull/266 | 2 | $3.86 |
| [CR-318](../261117-1351-318-driver-resume-after-stop/) | --- | merged | https://github.com/gsemet/chantier/pull/273 | 2 | $3.03 |
| [CR-313](../261117-1130-313-forge-stack-rebuild-empty-unstack/) | Change Specification: `forge-stack rebuild` takes the forge's empty unstack reply as a success | merged | https://github.com/gsemet/chantier/pull/267 | 1 | $1.90 |
| [CR-319](../261117-1351-319-board-visual-refresh/) | Change Specification: the web board, lighter and more elegant | merged | https://github.com/gsemet/chantier/pull/275 | 3 | $7.47 |
| [CR-314](../261117-1130-314-stack-handback-state-vs-draft/) | Change Specification: the stack shows a CR's hand-back apart from its PR's draft flag | merged | https://github.com/gsemet/chantier/pull/264 | 1 | $2.55 |
| [CR-320](../261117-1351-320-timing-settings/) | Change Specification: timing and retry settings in the configuration, per host and model family | merged | https://github.com/gsemet/chantier/pull/276 | 2 | $6.44 |
| [CR-321](../261117-1351-321-cost-receipt/) | Change Specification: the web board's Costs page shows the batch's cost as a supermarket receipt | merged | https://github.com/gsemet/chantier/pull/279 | 2 | $4.41 |
| [CR-322](../261117-1351-322-session-title-batch-suffix/) | Session titles: the batch number last, in parentheses | merged | https://github.com/gsemet/chantier/pull/274 | 1 | $0.81 |
| [CR-323](../261117-1351-323-two-sessions-one-machine/) | Two chantier sessions on one machine | merged | https://github.com/gsemet/chantier/pull/278 | 1 | $3.66 |

## Cost

- Total: $63.94 of a $200 budget
- Foreman $7.29 (11%), Drivers $20.10 (32%), workers $36.55 (57%)
- Most: CR-319 $7.47, CR-317 $7.35, CR-320 $6.44
- Foreman: 75 wakes, context 176,158 tokens on average, 265,553 at its peak
- Driver chantier:cr-driver with its workers: $53.51 (2279 calls)
- Driver chantier:stack-driver with its workers: $3.14 (190 calls)
- Chief of Staff, steering the batch (outside the budget): $8.45 since the batch opened (192 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $10.95 since the batch opened (168 calls, 2 spec-writers, 1 spec critics)
- Chief of Staff, whole session: $913.66, context 191,823 tokens; not counted: 2 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro

## 2026-11-17, CR-308 to CR-323 (batch-23)

- [chantier] The batch's PRs formed a tree on the forge, not one stack: Drivers based later CRs on branches with no PR or no commit yet, merges of CR-309..314 moved the bases, and three stack-driver runs (one failing on the forge's empty unstack reply, fixed by CR-313) were needed to restack: make `take` base a CR on the nearest earlier CR that has a PR, and let one stack-driver run own the final ordering.
- [chantier] A rebase with an identical patch-id was refused by the CLI as "does not carry" (CR-316), and six CRs ended with no verdict at their final heads: make the carry check compare the patch-id, not the diff text, and record the carry at the restack.
- [chantier] CR-317 ran six rounds (the user's standing word granted rounds 4 to 6): after a rebase onto CR-316 its `end_blockers` pushed rails.py over the 400-line test, then `just eval-dry-run` went red because the dry run paused a batch that now pauses itself, then the Verifier found the spec's card edits missing: the Driver card should run `just check` and `just eval-dry-run` before the first push of a CLI-behaviour change, and the Coder's round prompt should carry the spec's card-edit list as a checklist.
- [chantier] refused `git push --force-with-lease` (git write on a chantier/ branch a Driver owns; CR-318, "Destructive or Unwanted Actions"), which went Driver → Foreman → Chief of Staff → the user: let the hosts' capability table allow it on `chantier/` branches the Driver owns.
- [chantier] A Coder could not write its round file because the prompt's `writes:` line carried a parenthetical (CR-317 r6), and a Verifier wrote C:/cvscratch outside its writes and could not delete it (CR-315): the Driver prompt skeleton should print `writes:` as a bare path and name a scratch folder inside work/ for Verifiers. (critic: kept 5, dropped 3)
