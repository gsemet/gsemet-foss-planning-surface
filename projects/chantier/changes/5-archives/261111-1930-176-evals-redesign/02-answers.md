# Answers: evals-redesign

Grilled with the user on 2026-11-11. The option they picked is quoted.

1. **Campaigns:** three. `real-foreman` (today's `real`), `real-direct` (the same, steered by
   the Chief of Staff in direct mode), and `claude-planted`, which merges `claude-smoke` and
   `claude-full` for the planted failures a real run does not produce. `copilot` stays as it is.
   (Picked: "3 campagnes".)
2. **Reports:** every report has the same scorecard: each rail marked seen and right, seen and
   wrong, or not seen, plus the cost and the steering share, so two runs compare line by line.
   (Picked: "Oui, par garde-fou".)
3. **Audit:** the real campaigns get an automatic audit that reads the batch's log and cost
   before `close` and fills the part of the scorecard it can check; the rest is read by hand.
   (Picked: "Oui".)
4. **CRs of the real campaigns:** real small items from the inbox, picked by the Chief of Staff
   with the user's go; their PRs stay the user's to decide. (Picked: "Vraies CRs".)
5. **After each eval's report, each of its PRs is merged or closed within the day,** so real
   CRs opened as "do not merge" drafts do not go stale. (Decided by a Fable advisor, on the
   user's word: "Utilise un advisor fable pour te répondre".)

## The specification's open questions, settled the same day

Decided by a Fable advisor, on the user's word ("Utilise un advisor fable pour te répondre").

6. **The two `3-ready` CRs prepared for `real`** (`handback-after-rebase`,
   `heartbeat-odd-values`) run in `real-foreman`; `real-direct` takes fresh items. The Chief of
   Staff updates their `evals/real/` citations after the merge, before `open`: the planning
   folder is not in the PR.
7. **The cheap check after a role or flow change:** one real campaign with one small CR, in the
   mode the change touched; no fourth campaign. Before a release, both real campaigns;
   `claude-planted` after a change to how a batch handles failures.
8. **Copilot's report stays as today;** the scorecard applies to the three Claude campaigns.
9. **A real campaign may take an item already specified** (backlog or `3-ready`); it skips the
   grill.
10. **A CR still blocked at the report is kept** for a later batch, its reason in the report;
    `order drop` only if the user no longer wants it.
11. **No rail ids or scorecard on Copilot's audit** (the spec contradicted its own out of scope).
12. **No audit exit on an unchecked row and no "retired rows" rule:** the Inspector's check that
    the ids match is enough.
