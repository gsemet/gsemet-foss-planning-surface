One rule for a worker reply that breaks its format

From batch-16's retro (points 6, 7, 8, 9 and the Inspector part of 11), reviewed by an advisor.

Every specific rule already exists: a fresh child per round (concepts.md around 321-322, 376), the
Inspector's JSON only (worker.md around 49), a Verifier proof with its command (worker.md around 91), the
conflict resolver without BOM and with a fast gate after (worker.md around 147-149), the Inspector re-run
after a rebase that resolved a conflict (driver.md around 308-310). In batch-16 they were broken: a
round-2 Coder resumed instead of fresh, a refusal proof without its command, an Inspector verdict in
prose, a BOM left by a conflict resolution, no Inspector re-run after three rebases.

- Fix, the Driver's side: a reply not in its section's format, or a proof without its command, output
  and SHA, is a failed worker: one new start with the same brief (as driver.md around 28-30), never
  interpreted, never resumed by message. A new round is always a new child.
- `conflicts.md` names the fast gate run and its result.
- Point 8: one line in driver.md: a forge 5xx or network failure runs the same command once more, then
  `blocked infra:`.
- Lands: driver.md and worker.md. No CLI: it knows no role.