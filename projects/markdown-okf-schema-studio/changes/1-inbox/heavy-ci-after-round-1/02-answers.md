
## Grill, 2026-11-21

Decided by the Chief of Staff under the owner's autonomy rule (owner, 2026-11-20: "tu es maintenant autonome. plus de question. tu grilles tout seul avec un fable"; 2026-11-21: "Ensuite les autres P1 et inbox de Studio?").

- hc-Q1 Where: Studio's process guideline .agents/guidelines/change-requests-lifecycle.guidelines.md (the Driver reads it), not chantier.yaml: it is Studio-specific (Windows preflight skips visual, integration and report).
- hc-Q2 Rule: a CR that adds or changes visual, integration or stress scenarios pushes its branch (draft PR) after round 1 and dispatches gh workflow run ci.yml --ref <branch> -f heavy=true; the next round reads that run. Other CRs unchanged.
- hc-Q3 Cost: one heavy run per such CR early; no extra run on every round.

## Owner's answers, 2026-11-21

- hc-Q1 confirmed by the owner: "Studio's CR guideline".
