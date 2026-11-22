
## Grill, 2026-11-21

Decided by the Chief of Staff under the owner's autonomy rule (owner, 2026-11-20: "tu es maintenant autonome. plus de question. tu grilles tout seul avec un fable"; 2026-11-21: "Ensuite les autres P1 et inbox de Studio?").

- hc-Q1 Where: Studio's process guideline .agents/guidelines/change-requests-lifecycle.guidelines.md (the Driver reads it), not chantier.yaml: it is Studio-specific (Windows preflight skips visual, integration and report).
- hc-Q2 Rule: a CR that adds or changes visual, integration or stress scenarios pushes its branch (draft PR) after round 1 and dispatches gh workflow run ci.yml --ref <branch> -f heavy=true; the next round reads that run. Other CRs unchanged.
- hc-Q3 Cost: one heavy run per such CR early; no extra run on every round.

## Owner's answers, 2026-11-21

- hc-Q1 confirmed by the owner: "Studio's CR guideline".
- hc-Q4 (a CR inside a stack). Owner, 2026-11-21: "Push, draft PR and heavy run": in a stack, the stack driver pushes that CR's branch after round 1, opens its draft PR against the branch below, and dispatches the heavy run.

## Owner's answers, 2026-11-21 (Fable spec critic's questions)

- hc-Q5 (when the early push happens). Owner: "After round 1, any verdict": checkpoint commit, fast gate, push without the long gate, draft PR with a provisional body; the requirements check and `just preflight` stay where they are; the bullet says it overrides the Driver card's "gate before the first push".
- hc-Q4 REVISED (who pushes in a stack). Owner: "The CR's own Driver": as outside a stack, it pushes and opens the draft against the base `take` gave; the stack driver only restacks later. No exception to the stack driver's role.
- hc-Q3 REVISED (re-dispatch). Owner: "Only after such a fix": once after round 1, then once after each round that fixes a red integration or stress job of the early heavy run; never when the last heavy run is green. Rule 13's pre-merge run is that last green run if the head is unchanged.
- hc-Q6 (open-PR cap). Owner: "Yes; at cap, no PR yet": the early draft counts; at the cap the Driver pushes the branch and dispatches the heavy run without opening the PR.
- Owner, 2026-11-21: "Ready + run with Foreman": moved to 3-ready and run in a stack with the existing Foreman.
