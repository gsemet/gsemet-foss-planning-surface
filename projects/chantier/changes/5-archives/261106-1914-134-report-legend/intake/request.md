# A report tells blocked from waiting, with a legend and a short explanation

The user, reading a batch report where CR-123 said "waits for the stack driver" and CR-125 and CR-126
said "local base": "ce n'est pas clair qu'ils sont en attente du stack driver. je pense qu'il faut une
legende des couleurs au dessus et une petite explication en dessous de ce qui est bloqué, et je pense
un code couleur différent entre bloqué (rouge) et en attente."

Found:

- `chief-of-staff.md` line 138 lists the report's icons: ⚪ waiting, 🟡 working, 🔵 to review, 🔴 blocked.
  Nothing tells a CR that needs a decision from a CR that waits for something already on its way.
- The three CRs had one cause; a Driver's own `blocked` text gave it in different words.
- `status.py` and `hooks/register.tsx` hold their own `ICON` table, with no orange, and the record has
  one `blocked` state for both.
