# Answers

## Grill of 2026-11-10 (batch-09 paused; the user: "Grillons tous les P1 et P2")

1. **When the head moves.**
   - The user chose "Seulement ce qui a bougé (Recommandé)".
   - After a new round, a rebase or a restack, only the part the move touched is judged again.
   - The PR says which SHA each proof covers, and a stale proof is marked as stale.
2. **The visual check for a UI project.**
   - The user chose "Le Verifier lui-même (Recommandé)".
   - The Verifier checks that the screenshots show what the PR claims. It never wrote the code, and it already takes the before and after captures at the pushed head.
   - No new role.
3. **One long wait during CI.**
   - The question: measure first what a Driver spends waiting on CI today, then choose the means.
   - The user: "Je ne comprend pas reexplique moi". The Chief of Staff explains again.
   - **The explanation:**
     - After a push, a Driver waits 5 to 15 minutes for GitHub CI.
     - Each time it checks, it reads its whole context again, which costs tokens.
     - The idea: do everything else first (the PR body, notes), then wait once until the end.
   - The user chose "Juste la fiche".
   - The Driver's card says it at once: do the other work first, then one long wait. No measure first, and no CLI tool.

## Grilled enough (2026-11-10)

- **The full restatement:**
  1. Each proof names its SHA. When the head moves, only what moved is judged again. The PR says which SHA covers each proof, and a stale proof is marked.
  2. A claim in the PR with no proof is marked UNVERIFIED, or narrowed honestly.
  3. A cost or time not observed shows as unknown, never 0.
  4. The Driver's card says: everything else first, then one long wait for CI.
  5. For a UI project, the Verifier itself checks that the screenshots show what the PR claims.
- The user chose "Oui, grillé (Recommandé)".

## The specification's open questions (2026-11-10)

The user had said "Oui lance les spec et le batch. Fait une stack", so the Chief of Staff took the specification's default on each question. The user may change them while reviewing the PR.

1. **A batch's spend before its first priced refresh.** The spend shows as unknown, and the budget rail still lets a Driver start, as today.
2. **What wakes a waiting Driver.** Left out: the Driver does not add a note saying what ended its wait.
