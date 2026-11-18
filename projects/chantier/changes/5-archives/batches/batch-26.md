# batch-26

Opened 2026-11-18T12:16:06Z, closed 2026-11-18T14:29:30Z, parallel, steered by Foreman, budget $60, final cost $17.30. [batch-26.json](batch-26.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-354](../261118-1243-354-driver-stops-background-tasks/) | Change Specification: a CR Driver starts in its worktree, background tasks stop when done | merged | https://github.com/gsemet/chantier/pull/320 | 1 | $2.08 |
| [CR-355](../261118-1243-355-cost-receipt-after-switch/) | Change Specification: the cost receipt after a steering switch | merged | https://github.com/gsemet/chantier/pull/322 | 1 | $1.64 |
| [CR-356](../261118-1244-356-pane-shows-batch-shape/) | Change Specification: the CR board pane shows the batch's shape (`shape`) | merged | https://github.com/gsemet/chantier/pull/321 | 1 | $1.41 |
| [CR-357](../261118-1233-357-t3-project-icon/) | Change Specification: a project icon for T3 Code through `t3.json` | merged | https://github.com/gsemet/chantier/pull/319 | 1 | $1.20 |
| [CR-358](../261118-1425-358-surface-forge-hub/) | Change Specification: one forge hub per surface and machine, and watchers that wake each session | merged | https://github.com/gsemet/chantier/pull/323 | 3 | $7.04 |

## Cost

- Total: $17.30 of a $60 budget
- Foreman $3.93 (23%), Drivers $5.48 (32%), workers $7.89 (45%)
- Most: CR-358 $7.04, CR-354 $2.08, CR-355 $1.64
- Foreman: 28 wakes, context 212,653 tokens on average, 262,303 at its peak
- Driver chantier:cr-driver with its workers: $13.37 (647 calls)
- Chief of Staff, steering the batch (outside the budget): $5.20 since the batch opened (94 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $4.64 since the batch opened (65 calls, 1 spec-writers, 1 spec critics)
- Chief of Staff, whole session: $1079.46, context 138,876 tokens; not counted: 1 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro

## 2026-11-18, CR-354, CR-355, CR-356, CR-357, CR-358

- nothing worth changing (critic: 5 points dropped)
