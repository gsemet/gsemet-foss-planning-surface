# The Chief of Staff ends some messages with a line of tips

A short "Tips:" line tells the user what they can do now. The change is in `chief-of-staff.md`
only: the CLI does not change. It builds on CR-113, which gives the context size and the advice on
compacting, and on CR-114, which gives the "For you" line.

## The line

- It comes last, after the "For you" line, in the user's language, and starts with 💡 to stand
  apart: one or two tips, each a sentence with the exact words to type.
- It appears when a tip fits the moment: at the end of a piece of work, a report, or a quiet turn. A
  message with a question to answer or a blocker carries none, so the question stays last in mind.
- A tip already given and not used is not repeated in the same session, except the one on
  compacting, whose rule stays CR-113's.

## The tips

The card lists them as examples; the Chief of Staff judges and may say another that fits:

- `/compact`, on CR-113's rule, with its line to copy.
- "Status", for a progress table at once.
- `/chantier-board`, to show or hide the CR board, on Claude Code only.
- "What did it cost?", once a CR has spent.
- "File this", when the user raises an idea in passing.
- "Run the P2s", when the backlog holds prepared CRs and no batch runs.

A tip only names what chantier really answers, and never a command the host refuses in this
session.

## Done when

- `chief-of-staff.md` has this, and `just check` and `just scenario` pass.
