# Bug: the Write tool refuses files named report.md

## The user's words (2026-11-10, batch-09)

Quoting the Chief of Staff: "L'outil Write refuse les fichiers nommés report.md ; le Coder a dû
écrire la carte avec PowerShell. Je n'ai pas encore cherché pourquoi." The user: "note en bug P1".

## What happened

- In CR-159 (status-command, PR 96), the Coder had to create
  `skills/chantier/references/report.md`.
- The Write tool refused any file named `report.md`, so the Coder wrote it through PowerShell.
- The Inspector and the Verifier found the file intact.
- The Driver warned that any future CR that edits this card will meet the same block.

## What is known

- The project's `.claude/*.json` holds no rule naming `report`. The refusal comes from elsewhere:
  - a host or harness rule,
  - a user setting,
  - a hook,
  - or the agent definitions' tool settings.
- The cause is not investigated yet.

## The request

- Find why Write refuses `report.md`.
- Fix it where it belongs, in chantier or in its documented setup, so that agents can write and edit
  `report.md` with their normal tools.
- If the cause is outside chantier's reach, rename the card, or document the limit with the reason.
