# A CR's new readiness ask supersedes its earlier one

Filed 2026-11-15 by the Chief of Staff from batch-18's retro (kept by the retro critic and by a Fable review), on the user's word "lance le tout dans le batch actuel".

Problem: each restack re-sent a ready-to-merge ask for the same CR (6 pairs in batch-18: A-10/A-15, A-11/A-18, A-12/A-17, A-13/A-20, A-14/A-19, A-16/A-21); 17 asks were left unread (45 in batch-17).

Fix (CLI, `asks`, `batch_status.py`; one line in foreman.md): a new ask whose first word is a readiness word (`ready-to-merge`, `pr-in-draft`, `ready-locally`, `stack-ready-to-merge`) marks the earlier unread ask of the same CR and word family as read, logged "superseded by A-n". Never for `question` or `blocked`. Asks carry `"cr": null` today: key on the CR the ask names. Neutral on host and forge.
