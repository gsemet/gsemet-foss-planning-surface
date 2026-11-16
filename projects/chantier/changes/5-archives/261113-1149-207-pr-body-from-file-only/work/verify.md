Head: 94c27be58a4de591f0900a928d21dfa670658e96

Delta assessment after a restack with a conflict: aa74650 (on origin/main d178c7e) to 94c27be (on CR-206's head f1fb10d), conflicts in work/conflicts.md. The long gate is not run here (the stack's top gets it once).

Claims:

1. just check passes: judged again at 94c27be, 58 passed, release-notes ok.
2. just scenario passes, github and gitlab: carried from aa74650: the scenario, the CLI and the tests are unchanged by the move; `git diff --stat f1fb10d HEAD` shows only concepts.md, driver.md, chief-of-staff.md. The stack's top runs the long gate.
3a. concepts.md rule 9 holds the new rule: carried from aa74650: concepts.md has no conflict and the range-diff shows the hunk unchanged (8 lines added at rule 9).
3b. driver.md and chief-of-staff.md hold no `--description`, `--message`, `--body `, `--notes `: judged again at 94c27be, git grep returns nothing for these.
3c. GitLab form marked unproved with its trial: judged again, driver.md lines 79-82 ("unproved; trial: a GitLab MR opened and edited ..."), pointers at lines 309 and 378.
3d. Push bullet points to rule 9: judged again, driver.md line 79; the release bullet cites rule 9 at line 379.
3e. chief-of-staff.md `glab issue note <id>` reads a file, marked unproved: judged again, lines 196-198.
4. Diff touches only the three cards: judged again, `git diff --stat f1fb10d HEAD` lists exactly concepts.md, driver.md, chief-of-staff.md.
5. Resolved hunks (range-diff aa74650 vs 94c27be): the three driver.md hunks keep the base's new wording (Release driver PR "as the base says", inspector-approval note and Review box, `handback ready <pr link>`) and the CR's file form. Consistent with work/conflicts.md; nothing lost from either side.

Notes (not failures): driver.md lines 309 and 378-379 exceed the usual wrapping width; the PR table's "to rule 9" for the stack bullet points to the Push bullet, which cites rule 9.

VERIFIED
