# 148 — MyST cards, tabs and version directives render like MyST, and the README shows them

Type: feat · Priority: P1 · From the user, 2026-10-27 (overnight run)

## Intent (user)

See [01-intent.md](../01-intent.md). The user: "rajoute ça comme nouvelle CR à faire après toutes les
autres dans la stack, tout en haut (à la fin quoi)".

## Autonomous decisions

- Decided by the main session on 2026-10-27; list these in the PR body under "Autonomous decisions".
- Placed on top of the stack, above CR 147.
- The `}::` in the user's example was a typo: no lenient parsing (user decision). Only the valid
  form is checked; its title has no trailing colon.
