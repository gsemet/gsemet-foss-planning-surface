# Answers: worker-write-guard-redesign

Grilled with the user on 2026-11-11, after batch-10 stopped on the guard bug. The user's words
are quoted where they gave them; the rest is the option they picked.

1. **Shell writes.** The hook guards Write, Edit and NotebookEdit only. Before hand-back, the
   Driver checks that the main checkout has not changed (`git status`) and reports any trace.
   (Picked: "Driver vérifie".)
2. **A call the guard cannot read** (no path, an unknown shape): the guard refuses, and its
   message says the guard is at fault, not the worker. The Driver reports it to the steering
   session as a bug, with no round spent. (Picked: "Refuser, l'annoncer".)
3. **The Driver writing for a refused worker:** allowed for a worker's `work/` note only, never
   for code. (Picked: "Notes work/ seulement".)
4. **The hook's tests:** run by hand. CONTRIBUTING.md asks for them on a machine with the
   `claude` CLI before a hook change merges, and the Verifier keeps the proof. (Picked: "À la
   main".)
5. **Who runs them for this CR:** the user, by hand (the `claude` CLI is not on this machine's
   PATH). The Driver asks the user to run the command and pastes the user's output as the
   proof; its hand-back waits for that answer. (Picked: "Toi, à la main".)
6. **How the next eval proves the guard:** by normal use. The relaunched eval shows that
   legitimate writes pass; the hook's tests prove the refusals. No refusal is planted.
   (Picked: "Usage normal".)
7. **Priority:** P1, before anything else. It runs alone, before the eval is relaunched and
   before the v0.9.0 release, which cannot ship with this bug. (Picked: "P1, avant tout".)

## Superseded: the second grill (2026-11-11, later the same day)

A critical review (a Fable subagent, at the user's request: "J'ai peur qu'on over design cette
partie alors qu'il faut mettre en place de manière générale un mécanisme le plus simple et
efficace et extensible") found the specification over-designed. The user kept one CR and
postponed the release ("On fait dans la même CR ?", "On décale la release"), then answered again.
These answers replace 1 to 5 and 8 to 11 where they differ; 6 (proof by normal use) stands, and
7 becomes P1 with the release postponed until this CR merges.

12. **Fix the cause at spawn:** the hook starts each guarded agent in the worktree its prompt
    names. The Driver tries it with a real worker in the first round; if a worker can then no
    longer write its notes in the planning folder, the CR ships without this piece and says so
    in its hand-back. (Picked: "Essai d'abord".)
13. **A call the guard cannot read, or a guard that throws:** the call passes, and a visible note
    goes on the CR board. This replaces answer 2. (Picked: "Laisser passer, signaler".)
14. **Who is guarded:** any agent whose prompt holds a `writes:` line naming the folders it may
    write in; no role list in the hook, no parsing of a card's wording. A new role or a stricter
    rule is a card writing its own `writes:` line. (Picked: "Ligne writes:".)
15. **The hook's tests:** a `just mod` recipe runs `claude plugin validate` and
    `claude plugin test`; the agent runs it itself through the session's `claude`. If it cannot,
    it stops and says so, with no workaround. This replaces answers 4, 5 and 11. (Picked:
    "L'agent, just mod".)
16. **Detection of writes outside the worktree, the shell's included:** the steering session
    (the Foreman, or the Chief of Staff in direct mode) runs `git status` on the main checkout
    before each report and names anything outside the planning folder. This replaces answers 1
    and 10 (the Driver's before/after check). (Picked: "Le steering session".)
17. **Removed:** the Driver's copy of a refused worker's note (answer 3) and the "the guard is at
    fault" marker. One refusal message: the path is outside the allowed folders, write there.
    (Picked: "Oui, retirer".)

The rewritten specification's open questions (written by a Fable spec-writer, at the user's
request: "Fait faire le design par fable"), settled the same day:

18. **Unblocking:** the broken guard on main refuses every worker write, so it would block this
    CR too. A first small PR removes the guard from main, with nothing else to test; the user
    merges it; then this CR runs as usual and puts the new guard back. (Picked: "Retirer
    d'abord".)
19. **A trial that cannot run at all:** the CR ships everything but the start-folder rewrite and
    says so in its hand-back, as for a failed trial. (Picked: "Livrer sans".)
20. **When `git status` runs:** before each of the Chief of Staff's Progress and Completion
    reports, in both modes; one place. (Picked: "Mes rapports".)
21. **The audit check of the `writes:` line:** kept, in the eval audit. (Picked: "Oui,
    garder".)

After these, the user said "Je n'ai aucune idée de ce dont je réponds. Utilise un advisor fable
pour te répondre": a Fable advisor decided the rest, on the user's word.

22. **The trial's step 4 is required:** a real refusal in a real session must be seen before
    hand-back; if it cannot be, `handback blocked`. Only the start-folder rewrite stays
    optional. (Advisor: answers 6, 13 and 19 together would let a guard that never refuses
    ship unseen.)
23. **`just mod` stays outside CI;** the Inspector checks that the gate record holds it for any
    `hooks/` diff. (Advisor.)
24. **README's layout tree line** about the guard is among the texts this CR checks. (Advisor.)
25. **This CR runs in its own batch,** not in batch-10, which is an eval where nothing merges.
    (Advisor.)

## The first grill's open questions, settled the same day (partly superseded above)

8. **The refused round:** it stays counted; the steering session adds one with the existing
   order if the CR runs short. No CLI change. (Picked: "Compté, +1 si besoin".)
9. **The report of a guard fault:** `handback blocked`, with the exact refusal text; the Driver
   ends. (Picked: "handback blocked".)
10. **A trace in the main checkout:** reported only, never blocking `handback ready`; the
    steering session judges, since another Driver or the user may be its cause. (Picked:
    "Signaler seulement".)
11. **The hook tests for this CR:** the Driver hands back `blocked question:`; a new Driver takes
    the CR back with the user's output saved in `work/gates/`, and a Verifier judges it.
    (Picked: "Oui, ainsi".)
