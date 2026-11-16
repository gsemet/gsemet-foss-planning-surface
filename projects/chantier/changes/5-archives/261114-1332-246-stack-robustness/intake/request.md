The stack driver handles the cases that break a stack mid-way: a CR dropped from it, merges of its bottom PRs, and its own restart.

Found by the critic's review (Fable, 2026-11-14), none covered by another item:
- A CR dropped mid-stack: `chain()` removes it (`commands/facts.py:34`), but its PR stays in the forge's stack and its commits sit in every branch above. The card has an insertion procedure (`driver.md:472-489`) and no removal one.
- Intermediate heads are untested: heavy CI runs "once at the top" (`driver.md:413, 458`), while CR-233 (merge-any-time) lets the user merge bottom PRs alone. Decide which heads must be green before a bottom PR is offered for merge.
- Restack cost per partial merge: every remaining PR force-pushed, plus a Verifier or an Inspector per touched PR (`driver.md:420-427`), in one stack driver under the 130,000-token rule (`driver.md:65-70`); no record of a restack's progress lets a restarted stack driver resume where the last stopped.
- Sibling CRs started on one base conflict when the stack is linearised; all surface at the end, one by one, at the stack driver (`driver.md:419`).
After CR-233 and stack-grows-from-bottom.