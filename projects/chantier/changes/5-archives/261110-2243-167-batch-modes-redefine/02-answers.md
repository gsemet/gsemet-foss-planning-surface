# Answers

## Grill of 2026-11-10 (batch-09 paused; the user: "Grillons tous les P1 et P2")

1. **Series: do the Drivers work at the same time?**
   - The recommendation was at the same time, each branch on the previous one.
   - The user: "En mode série elles ne peuvent pas travailler en même temps car les commits sur laquelle la deuxième va se basé n'existe pas encore. Ou alors explique moi".
   - The user reads series as one after the other: the next CR needs the previous one's commits.
   - Still open: whether the next CR starts when the previous one is handed back ready (its commits pushed) or when it is merged. Asked next.
2. **Parallel: which PRs are rebased after a merge.**
   - The user chose "Toutes les ouvertes (Recommandé)".
   - After each merge, every PR still open is rebased onto main and its checks run again, conflict or not. The proof stays bound to the current head.
3. **The default mode.**
   - The user chose "Parallèle (Recommandé)".
   - A batch with no mode named is parallel: independent CRs from main.
   - Series or stack only when the user asks, or when a CR depends on another.
4. **Series: when the next CR starts.**
   - The user chose "Quand la précédente est prête (Recommandé)".
   - The next CR starts from the previous CR's pushed branch once that CR is handed back ready. Its PR is a draft.
   - After the previous CR merges, the next one is rebased onto main and turns ready.
   - If the previous CR changes during review, the next one is rebased.
5. **"Switch everything to a stack at once", for a series batch.**
   - The user chose "Un stack driver prend la suite (Recommandé)".
   - Every remaining CR starts at once, each on the previous one, and a stack driver keeps the stack up to date (restack).
   - The user merges from the bottom up.

## Grilled enough (2026-11-10)

- **The full restatement:**
  - **Parallel (the default):** everything starts from main at once, and the first one ready wins. After each merge, every open PR is rebased and checked again.
  - **Series:** a precise order. The next CR starts from the previous CR's branch once that one is ready, as a draft. After the previous one merges, it is rebased onto main and turns ready. The Chief of Staff guides the user merge by merge.
  - **Stack:** every CR at once, each on the previous one, with a stack driver. On request, a series batch switches to a stack at once.
  - **The docs:** a new SVG of the three modes in the README (not the lifecycle one), and clear explanations in the README and the docs.
- The user chose "Oui, grillé (Recommandé)".

## The specification's open questions (2026-11-10)

The user had said "Oui lance les spec et le batch. Fait une stack", so the Chief of Staff took the specification's default on each question. The user may change them while reviewing the PR.

1. **Stack: where each CR starts.** Today's behaviour stays: each CR starts on the default branch, and the stack driver stacks the PRs afterwards. A CR does not start on a branch that is still being written; that is the user's own objection to series.
2. **The demo offer.** It stays for stacks only, not for a series batch.
3. **Parallel: a CR blocked on a question.** It is rebased after each merge too, then handed back blocked with the same reason.
