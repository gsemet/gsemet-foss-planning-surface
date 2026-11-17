# 137 — PlantUML JAR includes stay inside the workspace

Type: fix · Priority: P3 · From backlog: `02-backlog/P3/plantuml-jar-include-confinement.md`

## Intent (user)

See [01-intent.md](../01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "rajoute tout ça dans les requêtes à faire dans une stack … livre-moi tout ça sur la stack en cours, dans des nouvelles PR; s'il y a des changements impactants tu peux t'organiser pour optimiser les livraisons". List these in the PR body under "Autonomous decisions".
- Placed first above CR 135: it finishes CR 135's T2 (same code) and closes the last security point of the audit.
- Compare paths by path segments after realpath (never a string prefix), resolve `!include` in the extension before the JAR runs, refuse an include that leaves the root with a visible message.
