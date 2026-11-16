# batch-21

Opened 2026-11-16T16:30:53Z, closed 2026-11-16T19:42:34Z, parallel, steered by direct (the Chief of Staff), no budget, final cost $7.10. [batch-21.json](batch-21.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-296](../261116-1726-296-improve-skill-boot/) | Proposal: improve skill boot | merged | https://github.com/gsemet/chantier/pull/247 | 2 | $3.10 |

## Cost

- Total: $7.10, no budget
- Chief of Staff, steering the batch $4.00 (56%), Drivers $1.85 (26%), workers $1.25 (18%)
- Most: CR-296 $3.10
- Chief of Staff, steering the batch: 9 wakes, context 187,068 tokens on average, 257,695 at its peak
- Driver chantier:cr-driver with its workers: $3.10 (137 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $34.76 since the batch opened (662 calls, 16 spec-writers, 5 spec critics)
- Chief of Staff, whole session: $760.61 ($7.10 of it in the batch's spend), context 160,360 tokens; not counted: 2 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)
- Declared stopped on the user's word: agent-a0efdc32dca6c61a7 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a22025d94b0425f76 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a2527633954813a84 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a4481a8d0b396f19f (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-a82a4e8172fa0b0d4 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-aa2b04a9ea02a0446 (its last record is a prompt with no answer yet)
- Declared stopped on the user's word: agent-aa835f48f2788b16f (its last record is a prompt with no answer yet)

## Retro

# Retro

## 2026-11-16, batch-21: CR-296 (PR 247)

- [chantier] A batch opened and stopped on another machine cannot be taken over here: batch-20's batch.json, events.jsonl and brief.md were local and unpublished, `pause` refused it because CR-296 was unmerged though nothing ran, so its record stays `running` in 5-archives/batches, the CR had to go back to 3-ready into a new batch-21, and the Driver pushed one head to two branches (batch-20's PR branch and the batch-21 name the CLI expects): a takeover path (`pause` accepts a batch whose remaining CRs are stopped or blocked by the user; what a resume needs is published; a takeover closes or supersedes the old batch's record and lets the CR keep its existing PR branch).
