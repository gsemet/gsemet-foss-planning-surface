# 139 — An edit made by another tool to the active document glows

Type: fix · Priority: P3 · From backlog: `02-backlog/P3/external-edit-glow`

## Intent (user)

See [01-intent.md](01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "rajoute tout ça dans les requêtes à faire dans une stack … livre-moi tout ça sur la stack en cours, dans des nouvelles PR; s'il y a des changements impactants tu peux t'organiser pour optimiser les livraisons". List these in the PR body under "Autonomous decisions".
- Rule: a change is foreign when no keystroke reached the text editor or the preview in the last 500 ms, or when its range does not touch any cursor or selection; document the rule in SwRS LIFE-094.
