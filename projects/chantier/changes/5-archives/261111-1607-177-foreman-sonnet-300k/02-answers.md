# Answers: foreman-sonnet-300k

Grilled with the user on 2026-11-11. The option they picked is quoted.

1. **Roles on Sonnet 5.5 by default:** the Foreman, the stack driver and the release driver join
   the CR and QA drivers and the workers. The spec-writer stays on Opus 5.5. (Picked: "Foreman +
   drivers".)
2. **The Chief of Staff's session stays on Opus 5.5.** (Picked: "Reste en Opus".)
3. **Escalation to Opus 5.5 on named triggers,** written in the cards: a CR blocked twice; the
   rounds used up with the Inspector still FIX-REQUIRED; a red check the Debugger could not
   explain; a conflict the resolver could not settle; a restack that failed. The task then goes
   to a new agent on Opus, and the report says so. Never a silent swap. (Picked: "Déclencheurs
   nommés".)
4. **Auto-compact:** the recommended window is 300K for both the Foreman's and the Chief of
   Staff's sessions. (Picked: "300K pour les deux".)
5. **Left to the Chief of Staff** (implementation or out of scope): the effort stays "medium";
   Copilot is untouched (the user's "laisse copilot dans son coin"); the escalation model may be
   set per role in `chantier.yaml` like the other models.

## Decided by a Fable advisor on the user's delegation

2026-11-11, on the user's words: "Grille tout avec une session fable je ne sais pas te répondre.
Je veux juste que Chantier fonctionne et soit suffisamment générique pour qu'il fonctionne dans
n'importe quel projet…, je ne veux pas que tu hardcode des choses trop précises, mais il faut
que ça marche vraiment."

6. **"A CR blocked twice" counts** `refused`, `infra:` after its one re-run, `driver ended
   twice` and `stopped`; not `question:`, `approval:`, `merge:`, `waits:`, `fix:`, `budget:`,
   nor `rounds:`. Reason: only trouble in the work is a reason to pay for a stronger model, and
   `rounds:` already has its own trigger.
7. **The `escalate` key in `chantier.yaml`: later, not in this CR.** One escalation model per
   host, the same for every role. Reason: no project has asked for it, and the cards name no
   model, so the rule is already generic.
8. **One escalation per trigger and per task: confirmed.** An escalated agent that fails the
   same way takes the existing route, never escalates again, never swaps back. Reason: it
   bounds the cost and keeps the user in the loop.
9. **The CLI prints the escalation model once,** as the last line of `playbook` and `playbook
   --batch`; `take`, `round` and `handoff` are unchanged. Reason: an escalation is rare, and a
   printed value in one place is enough to keep "never a model typed from memory".
10. **The structure test's `OPUS_ROLES` split per host stays.** Reason: the hosts' agent files
    now differ in model, and it is the smallest change that keeps the test true.
