# Refuse a batch CR that depends on work deferred past the batch

A CR of the running batch must not depend on work deferred to after the batch; the CLI should refuse it.

Asked by the owner, 2026-11-26, verbatim: "Envoi à CoS Chantier le control à rajouter sur les tâches:
on ne peut pas dépendre dans le batch en cours d’une tâche renvoyée pour après le batch. Le CLI aurait
du générer une erreur" (send chantier's Chief of Staff the check to add on tasks: a task of the running
batch cannot depend on a task sent to after the batch; the CLI should have raised an error).

The case, in another project's stack batch:

1. CR A's specification held a prerequisite: "the CR starts only when its parent carries" a switch that
   CR B was to deliver. CR A joined the running batch with that clause, and its `depends.json` placed it
   after CR B.
2. During the batch the user sent that part of CR B's scope (the switch) to the batch after this one,
   recorded as an order note on CR B. CR B went on with the rest.
3. Neither the CLI nor the Chief of Staff flagged that CR A now depended on work that could no longer
   happen in the batch.
4. The gap showed only when the Foreman came to start CR A: it parked CR A with no round run and asked
   whether to drop it or amend its specification.

Wanted: when a task of the running batch depends on a task that is deferred to after the batch (or when
scope another task depends on is deferred), the CLI raises an error at that moment, naming both, so the
user decides then: drop or amend the dependent CR, or keep the work in the batch.

Open point for chantier's grill: here the dependency was on part of a CR's scope, written in prose in
the specification, while the CR itself stayed in the batch; a check on `depends.json` alone would not
have caught it. Not grilled.
