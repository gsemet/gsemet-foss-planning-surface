# Change Specification: answers recorded at once, a shared understanding before "grilled enough?", and a CR named by number and slug

## Goal

Three rules the user made hard, written where the roles read them.

## What changes (cards only)

### 1. Record at once (`skills/chantier/references/chief-of-staff.md`, "Backlog and grill")

Every human answer and decision about a CR is written into that CR's folder (`02-answers.md`,
with the date and the user's words) immediately after it is given: before the next question,
before any other work, in the same turn. This covers decisions given outside a grill (a
priority, "left aside", "same batch", "later"). A grill round with several answers is one write
per CR touched. Nothing waits in the conversation only.

### 2. The shared understanding (same section)

The Chief of Staff may ask whether a CR is grilled enough only after a **complete restatement**
of it, in the user's language: what it changes, every decision taken (from `02-answers.md`),
what is still open. The user corrects it; a correction is an answer (rule 1). The Chief of Staff
never decides on its own that a CR is grilled enough: it asks, and the user decides, as the user
alone sets priorities and picks what runs.

### 3. A CR's name (`skills/chantier/references/concepts.md`, with one line in
`chief-of-staff.md` and `foreman.md` where they describe reports)

A CR is always named by its number and its short slug together, e.g. **"CR-142 grill-rules"**,
wherever an agent names it to a person or in a report: messages to the user, batch reports and
their tables, asks, PR titles and bodies where the project allows. Never the number alone or the
slug alone. An item not yet numbered (inbox, backlog) is named by its slug. The CLI's own outputs
are not changed by this CR.

## Evidence

Read the three cards: each rule is stated once, in plain words, where its role reads it; no card
contradicts it (grep "02-answers", "grilled", "CR-"). `just check` passes; `just scenario`
passes.
