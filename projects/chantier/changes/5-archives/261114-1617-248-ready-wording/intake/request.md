# A CR is not "ready" while its PR is a draft

The user (2026-11-14), reading the `ready` asks of batch-17's stack, where each ready CR's PR stays a draft on the CR under it: "Il faut revoir le vocabulaire: "prêt" alors que la PR est en draft. Revoyons les termes possible".

Today `ready` means the CR's work is done and proven (long gate, CI green, Verifier `VERIFIED`), whether its PR is a draft (in a stack, on an unmerged CR) or open on the default branch. The user reads "ready" as "I can merge it".