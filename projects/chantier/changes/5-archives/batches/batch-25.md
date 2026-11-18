# batch-25

Opened 2026-11-18T10:09:33Z, closed 2026-11-18T11:56:53Z, parallel, steered by Foreman, budget $25, final cost $8.91. [batch-25.json](batch-25.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-353](../261118-1107-353-switch-batch-to-direct/) | Change Specification: switch a Foreman batch to direct mode, with CRs in flight | merged | https://github.com/gsemet/chantier/pull/318 | 2 | $4.93 |

## Cost

- Total: $8.91 of a $25 budget
- Chief of Staff, steering the batch and Foreman $3.98 (45%), Drivers $1.64 (18%), workers $3.29 (37%)
- Most: CR-353 $4.93
- Chief of Staff, steering the batch and Foreman: 14 wakes, context 197,182 tokens on average, 261,128 at its peak
- Driver chantier:cr-driver with its workers: $4.93 (207 calls)
- Chief of Staff, steering the batch (outside the budget): $2.74 since the batch opened (55 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $0.21 since the batch opened (3 calls, 0 spec-writers, 0 spec critics)
- Chief of Staff, whole session: $1063.69 ($3.26 of it in the batch's spend), context 150,702 tokens; not counted: 1 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro

## 2026-11-18, CR-353 switch-batch-to-direct

- [chantier] AGENTS.md owes a local Windows `just scenario` on "the CR on top of the stack"; in a parallel one-CR batch the Driver handed back `--no-gate`, the Chief of Staff held the ask and sent the CR back for the gate (an extra take, a resume, a second ask A-1 then A-2, 498 s of gate after the hand-back instead of before it): driver.md says only "the stack's top"; the cards say what "top" means for a batch with no stack (the batch's last CR to be merged), so the Driver runs the local gate before its first hand-back. (critic: kept 1, dropped 1)
