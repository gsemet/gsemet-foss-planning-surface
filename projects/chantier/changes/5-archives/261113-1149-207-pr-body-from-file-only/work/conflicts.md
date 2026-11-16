# Conflicts: CR-207 restack onto CR-206 head f1fb10d

File skills/chantier/references/driver.md, three hunks, all resolved keeping both intents.

1. Push bullet (PR opening): kept the base's "a Release driver opens its PR as the base says: ready on the default branch, a draft on another base", and the CR's "`glab mr create --draft` with the form below".
2. Stack driver restack paragraph: kept the base's inspector-approval note and Review-box sentence; replaced `glab mr update --description` with the CR's "`glab mr update` with the file form of the Push bullet (unproved there)".
3. Body refresh bullet: kept the base's closing `handback ready <pr link>` (instead of the old `handback blocked merge`); carried in the CR's file-form wording and the concepts rule 9 link.

Fast gate: `just check` passed (58 tests).
