# Conflicts: CR-211 restack onto CR-210 head deae40a

- concepts.md, CR dependency paragraph ("A CR stands on another only by a dependency"): the base added the release CR as the top of the stack and kept the fix CR outside; the CR added "or the plan proposed and the user's go approved". Kept the base's text and inserted the CR's clause.
- driver.md, `note rebase:` while working: the base stops a running long gate (`gate <cr> --stop`) before the rebase; the CR makes it one rebase per push however many notes came. Merged both into one sentence.

Fast gate: `just check` passed (58 tests).
