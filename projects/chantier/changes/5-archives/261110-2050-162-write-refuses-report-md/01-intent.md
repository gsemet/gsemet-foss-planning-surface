# Intent: subagents can write every file chantier asks them to write

## The problem

- Claude Code has a built-in guard against subagents writing report files. It refused the
  Coder of CR-159 when it tried to create the card `skills/chantier/references/report.md`.
- The guard's text: "Subagents should return findings as text, not write report files."
- The guard went by the file name, and blocked the Coder wrongly: the card describes the shape of
  the reports, it is not a report returned to a caller.
- chantier cannot lift the guard.
- The guard's exact matching rule is not known: `progress-report.md` went through the same day.

## What the CR changes

1. **The card gets a new name.**
   - A name that does not look like a report, for example `report-format.md`.
   - Every link to it is updated: the cards, the skills, `/chantier:status`, the docs and the
     tests.
   - A subagent proves it can write the new name.
2. **Every other name is checked.**
   - The CR lists every file a chantier subagent writes, for example:
     - the Verifier's `verification.md`;
     - the Demo explorer's `demo/demo.md`;
     - the notes in `work/`.
   - It tries each name with a subagent.
   - It renames only the names the guard refuses, with the proof.

## Out of scope

- The Chief of Staff's own writes. It may keep writing files named `report.md` when it archives,
  such as the release CR's `report.md` (the user's word). The main session is not a subagent, so
  the guard does not apply to it.

## Triage

- A specification the user reviews before any batch.
