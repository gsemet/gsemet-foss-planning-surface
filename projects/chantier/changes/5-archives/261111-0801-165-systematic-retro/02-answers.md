# Answers

## Grill of 2026-11-10 (batch-09 paused; the user: "Grillons tous les P1 et P2")

1. **When a retro is made.**
   - The question: besides each release and each batch closed without a release, should a retro also come when a batch is paused with every CR merged (as batch-09 was)?
   - The user chose "Aussi à cette pause (Recommandé)".
   - A retro comes as soon as every CR of the batch is merged, whether the batch is paused or closed, and at each release.
   - Each point is offered to the user as an inbox item.
2. **The Chief of Staff's cost.**
   - The user chose "Séparer en deux lignes (Recommandé)".
   - The cost reports split the Chief of Staff's cost into two lines, each with its measured cost: "grill and specifications with the user" and "steering the batch".
   - A part that cannot be measured is shown as unknown, never estimated.

## Grilled enough (2026-11-10)

- **The full restatement:**
  1. A retro comes at each release, and as soon as every CR of a batch is merged, whether the batch is paused or closed. It lists each problem met with its long-term fix in one line. The Chief of Staff offers each point as an inbox item.
  2. The Chief of Staff's cost is split into "grill and specifications with the user" and "steering the batch". A part that cannot be measured is marked unknown.
  3. The report, `status` and the batch's `STATUS.md` say who steers the batch (direct mode or a Foreman) and its shape (a stack or parallel).
- The user chose "Oui, grillé (Recommandé)".

## The specification's open questions (2026-11-10)

The user had said "Oui lance les spec et le batch. Fait une stack", so the Chief of Staff took the specification's recommendation on each question. The user may change them while reviewing the PR.

1. **The grill turns in direct mode.** They leave the batch's spend and budget, as the spec-writer already does.
2. **The name of the Chief of Staff's other calls** (in Foreman mode too). The name stays "steering the batch".
3. **Where the retro lives.** In `4-batch/retro.md` only. It is deleted at close, once its points have been offered.
4. **A retro point about chantier itself, found in another project.** It is offered as an inbox item of that project.

## A warning from the user, after the restatement (2026-11-10)

- The user: "Attention pour les sessions longues avec plusieurs compactions et le coût peut être mal calculé".
- The cost split must hold in a long Chief of Staff session with several compactions.
- **What is known today** (batch-09's `cost`): compaction calls leave no record and are not counted, at about $0.12 each. The Chief of Staff's session spans several batches: $171.35 over the whole session, $12.01 since batch-09 opened.
- **What the CR must do:**
  - The split ("grill and specifications" against "steering") stays right across compactions and across batches in one session.
  - What chantier cannot see, such as compactions, is shown as unknown with its count when known, never as 0 and never silently left out.
