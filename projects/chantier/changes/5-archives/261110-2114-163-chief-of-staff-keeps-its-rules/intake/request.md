# The Chief of Staff keeps its rules, through compaction

## The user's words (2026-11-10, batch-09)

- "Il faut merger les 2 CR grill et add, car c'est le même genre de violation de guidelines. Tu
  vas mettre ça en P2 que l'on traitera plus tard et il faudra trouver une solution qui résiste aux
  compaction"
- Asked which items, the user chose "Les trois ensemble".
- On triage while steering: "Ah si tu peux trier mais pas démarrer. Il faut vraiment que l'on
  reprenne point par point dans cette CR ce qui est possible".

## What this CR merges

The three earlier inbox items are kept whole in `intake/`:

1. `no-grill-while-steering` (`intake/no-grill-while-steering-request.md`). The Chief of Staff
   grilled while steering a running direct batch, against `chief-of-staff.md`. The user asked
   for a gate in the CLI.
2. `options-by-environment` (`intake/options-by-environment-request.md`). The Chief of Staff
   offered the user, on Remote Control, options they could not take: Foreman mode, "run this in
   a terminal", `--host 0.0.0.0`. The user asked for a checklist by environment and coding
   agent, with the reason for each entry. A draft table is in that file.
3. `add-several-while-paused` (`intake/add-several-while-paused-request.md`, with its grilled
   `intake/add-several-while-paused-01-intent.md` and `-02-answers.md`). This is the CLI change
   that lets a paused batch take n CRs before it runs again.
   - Its answers: the first `take` starts the batch again; both steering modes; the refusal
     message no longer names Foreman mode.

## The problem they share

The rules are written in the cards. After a context compaction, the session keeps only a summary
of the cards and acts against rules it no longer sees. The fix must hold through compaction:
either the CLI enforces the rule, or the rule comes back into context when it matters.

## What the CR must settle, point by point

- **What the steering session may do while its direct batch runs, and what it may not.** The
  user's first correction: it may triage, but not start (no new work begins). Every other point
  is to be gone through one by one: file, triage, grill, specification, demo, discussion,
  `order add`, and others.
- **What it may offer the user, by surface, host and session,** each with its reason.
- **Which of these the CLI enforces,** and which come back into context another way.
- **The add-several-while-paused CLI change.**

Priority P2, to be worked on later.
