# A stack batch keeps its shape after the Foreman's compactions

From Studio's Chief of Staff (2026-11-21), with Studio's owner's yes. Owner's words: "il faut un mécanisme pas trop lourd mais systématique"; the cause is the long session.

Incident (Studio batch-07, shape stack, Foreman reused for a second wave, several compactions): after the morning's stack merge, the Foreman shipped every new CR as its own PR on main with a per-CR ready ask: no `take stack`, no stack driver, no native stack. Each owner merge left the other PRs behind main; the owner got PRs not rebased. Caught only when the owner asked "Le mode stack marche pas ou le foreman oublie ?". Root cause: foreman.md line ~15, after a compaction the Foreman rereads only the startup sections; the shape's section (the stack part, ~line 425) is deferred, so the shape survives as a word, not as a procedure.

Proposed fix, CLI-enforced rather than memory-based:
1. Reminder at each wake: `status --refresh --epoch <n>` (the Foreman's heartbeat) prints one fixed line for the shape, e.g. `shape stack: next take stack; stack driver: none; native stack: absent`.
2. Guard: in a stack batch, `asks` refuses a per-CR `ready-to-merge` ask and accepts only `stack-ready-to-merge` (a fix CR excepted).
3. Reload: the post-compaction reread list includes the card section of the batch's shape.
4. CoS: the CoS card checks each Foreman ask against the shape, not only "rebased and green".
1 and 2 are the core.
