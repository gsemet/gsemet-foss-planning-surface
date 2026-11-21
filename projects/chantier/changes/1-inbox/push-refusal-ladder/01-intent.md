# A refused push climbs: Foreman tries, then Chief of Staff, then the user

When the host's classifier refuses a legitimate push to a subagent (a Driver's
`git push --force-with-lease` on its own `chantier/` branch, in delegation), the push climbs a
ladder instead of stopping on the user:

1. the Foreman tries the same legitimate push itself;
2. if the Foreman is refused, the Chief of Staff tries it, without asking the user (as its card
   already says for a refused force push);
3. only if the Chief of Staff is refused too, it asks the user; the user's own yes in the
   conversation is what lets the classifier see the push is really wanted; then it pushes.

Why: on 2026-11-21 CR-434's Driver was refused a legitimate force push (same tree, rebased onto
main); the Foreman relayed it and the Chief of Staff asked the user at once. The user: "Tu dois
d'abord essayer dans ces cas au lieu de me demander."

Done when the cards (driver, foreman, chief of staff, and the Claude Code host reference for the
host's specifics) carry the ladder, each session that pushes judges the push first (the Foreman,
then the Chief of Staff again), and a refusal at each step is recorded with its exact text.
