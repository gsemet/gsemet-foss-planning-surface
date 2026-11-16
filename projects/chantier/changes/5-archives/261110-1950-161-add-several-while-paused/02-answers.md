# Answers

## Grill of 2026-11-10

The request: "on peut rajouter n CR quand le batch est en pause avant de le relancer".

1. **What starts the batch again.**
   - The user chose "Au premier lancement" (recommended).
   - `order add` on a paused batch leaves it paused.
   - The batch runs again when the first added CR starts (its `take`).
   - No new command.
2. **Which steering.**
   - The user chose "Les deux modes" (recommended).
   - The rule holds in direct and in Foreman mode alike, as the pause does today.
3. **The refusal message.**
   - The user chose "Non, juste la pause" (recommended).
   - When a running direct batch refuses `order add`, the message says to add the CR once the batch
     is paused. It no longer names Foreman mode.
   - The reason: which steering fits is the Chief of Staff's judgement. For example, a user on
     Remote Control cannot steer a Foreman session.
4. **Priority.** The user chose P1 (recommended).

## 2026-11-10, later

- This CR was first merged into the P2 CR `chief-of-staff-keeps-its-rules`, on the user's word.
- In that CR's grill the user chose "Couper en deux (Recommandé)". This CR is its own again, in P1, with the grill above unchanged.
- The Chief of Staff listed this CR as grilled, without a specification. The user: "Lance le reste". That is the user's go for the spec-writer.

## The specification's open question (2026-11-10)

- The user, before it was asked: "Plus de question. Livre le max".
- The Chief of Staff kept the specification as written: `order qa` on a paused batch still sets it running at once, because its QA driver holds a slot from the order on.
- The user may change this when reviewing the PR.
- The same words are the user's go to deliver this CR: it goes into batch-09.
