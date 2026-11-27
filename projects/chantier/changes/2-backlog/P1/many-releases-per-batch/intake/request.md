# A batch can have as many releases as the user wants

## The owner's words (2026-11-27), verbatim

"Ah met un CR pour chantier: un batch peut avoir autant de release qu'il le souhaite, en P1"

## What happened

In the project markdown-okf-schema-studio (chantier 0.15.1), batch-09 (shape stack) already held a
release CR, a patch release done early in the batch (CR-478). At the end of the same batch the owner
asked for a second release of the later work. Adding it was refused, exact text:

> order add --release: CR-478 is already the release CR of batch-09; a batch has one. Put the second
> release in the next batch, once this one is closed

The batch then had to be closed, and a new one opened, only to release.

## What is asked

A batch can have as many release CRs as the user wants.

## To settle in the grill

- Which CRs a release waits for when the batch holds several (today it waits for every other CR,
  later ones included).
- What the cards and help topics that say "one per batch" become (`help release-chief` among them),
  and how the grant, the approvals and the close treat several releases.
