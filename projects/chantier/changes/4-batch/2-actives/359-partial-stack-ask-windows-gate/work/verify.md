# Verify CR-359

Head: 79c3fe0e981f68688f62f89e64cd9f53f608caf6

Verdict: VERIFIED

All claims judged at 79c3fe0 (worktree clean, `git rev-parse HEAD` above).

1. Diff touches only the three cards. `git diff --name-only origin/main..HEAD` ->
   skills/chantier/references/chief-of-staff.md, driver.md, foreman.md. No CLI, hook, agent file, doc.
2. Clause form identical in three cards. `grep -n "local gate <cr> at"` on the three cards:
   driver.md:916 `local gate <cr> at <head7>: passed|failed`, :943 `... not run`, :955 `[ local gate <cr> at <head7>: passed|failed|not run]`;
   foreman.md:325 `local gate <cr> at <sha7>: passed to come:`, :415 `... passed|failed|not run`;
   chief-of-staff.md:1078 `local gate <cr> at <sha7>: passed|failed|not run`.
3. Invariant wired into every path (diff read): first stack (paragraph "The local gate at the mergeable top"), draft turned ready (driver.md ~927 "under the rule, its local gate passed at its head"), restack step 4, insertion step 5, drop step 6, Deliver by a time, hand-back line. Failed-gate anomaly present in driver.md paragraph and foreman.md bullet (take <cr> note).
4. Foreman edits: partial ask form + condition, no-clause = failed check, deliver-by override, asks list: all in diff. Complete ask unchanged.
5. Chief of Staff: clause quoted before the merge sentence, not-run/failed/no-clause told, merge stays user's choice: in diff.
6. Docs grep `partial stack mergeable below` outside scenario/CLI src: only chief-of-staff.md, foreman.md (edited) and status-layout.md:96,100, which quote the report's partial-stack line, not the ask form: no change owed.
7. PR body (pr-body.md) matches diff: Deliverables table, Changes list, cards-only, Known gaps names the unproved trial. Role names appear only as cards' product terms of this change. No images.
8. Note: the driver.md paragraph sits after the stack-anomaly text, before "A CR that joins", not in "Making the stack" as the spec's line hint said; its content and the wiring are as specified. Not a failure.
9. CI: green at this head per the Driver's note (5 jobs); not re-run here.
