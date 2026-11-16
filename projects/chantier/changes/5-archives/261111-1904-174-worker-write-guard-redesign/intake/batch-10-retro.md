# batch-10 retro

## 2026-11-11: CR-172 handback-after-rebase, CR-173 heartbeat-odd-values (stopped on the user's word)

- The worker write guard (CR-171 rail, `hooks/register.tsx`) refused every worker Edit/Write, even inside the CR's own worktree, with an empty path in its message: it reads `e.input.file_path` while a `tool.call` event carries the arguments flat. CR-172's round 1 was spent with no code; CR-173 held at round 0: test the guard against a real `tool.call` event's shape (not a hand-built one) in `hooks/register.test.tsx`, and run one real worker write as a smoke check before a batch relies on a new hook.
- The guard also refused a read-only worker: the investigator's Write of its own `work/` note was refused, so the CR-173 Driver wrote it itself (a parent doing a child's write): once the guard is fixed this stops; until then a guard refusal is a stop for every worker, said in the card.
- A worker's PowerShell write of its `work/` note was refused by the auto-mode classifier with no reason given, while a one-word probe passed: record the refusal's exact text when the host gives one, and keep workers on Write/Edit for files.
- The batch stopped before any gate, verdict, handback ready or push: the other CR-171 rails (one command per `gate` argument, `handback ready` gated on long gate and VERIFIED) are still untried in a real batch: run them first in the next real eval.
