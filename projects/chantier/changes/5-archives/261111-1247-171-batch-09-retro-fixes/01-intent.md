# Intent: the batch-09 retro's fixes, in one CR and one PR

2026-11-11, the user, after the batch-09 retro (`4-batch/retro.md`): a fix strategy that
"fonctionne quand chantier sera déployé dans n importe quel type de projet", without making the
process rigid or costly ("Ce qui me gène c'est pourquoi parce que l on rigidifie le process et
ça augmente les coûts"). The user kept points 5, 6, 8, 9, 10, 11, 14 and 16 and wanted them in
one CR ("Une seule CR").

The request (`intake/request.md`) has eight parts, each with what happened and the proposed fix:

1. A worker cannot write outside its CR's worktree. The guard is a hook and costs no token.
2. `handback ready` refuses unless two things hold at the PR's head: a passed long gate, and a
   verdict `VERIFIED`. The verdict is recorded as JSON by a new `verdict` command, and `take`
   lists both gates up front.
3. `order add` queues a CR on a running direct batch.
4. `cost` gives an agent with no CR its own line.
5. `gate` takes one command per argument, the same way on every OS.
6. Every command accepts a CR's bare number.
7. The CLI prints the spec-writer's exact first prompt line.
8. A brief states a past fact only with its source.

The point is fewer retries and fewer skipped proofs. Only part 2 adds a refusal, and it covers
two gates; every other step stays the Driver's judgement.

Open for the grill:

- Does the hook refuse the write, or only warn?
- How does a CR the project exempts from the long gate (docs only, here) pass part 2?
- What does the Copilot host get instead of the hook?
- The CR's priority.
