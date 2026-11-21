# An ordered stack is checked as a git chain

From Studio's Chief of Staff (markdown-okf-schema-studio, batch-07 retro, kept by a Fable retro-critic, 2026-11-21); the owner's word relayed in that session: "Oui envoie au CoS de chantier à mettre en P1".

The ordered stack CR-439..CR-445 was not a git chain: CR-440, CR-442 and CR-444 were cut from main; only the forge bases were linear. `take CR-446` was refused, a first stack-driver wrongly concluded that no restack was needed, and two restacks followed, voiding the gates and verdicts of five CRs (about +$15-25).

Proposed fix: at each `ship` of an ordered batch, the CLI checks that the CR's branch is based on the previous CR's head; the stack-driver card verifies with `git merge-base` before concluding that no restack is needed.

Evidence: projects/markdown-okf-schema-studio/changes/4-batch/retro.md (batch-07 section) and CR-446's retro.md on the planning surface.
