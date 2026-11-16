# Before and after: the cards CR-120 changes

Technique: card text, so the sections are extracted by one command at each side.
Before: detached worktree at 49135f5 (origin/main, this branch's base; removed at the end). After: pushed head 585379d.
Command (per file/heading): print the lines from the heading to the next `## ` heading; for the two grep pairs, `Select-String -Pattern 'evidence|Workers never create|worktree of the base'` / `'evidence/'`.

| Pair (before / after) | What it shows | Reproduce |
|---|---|---|
| worker-investigator.before.txt / .after.txt | Investigator output now ends with an evidence plan; the project's rules rank above it, no question to the user | section `## Investigator` of skills/chantier/references/worker.md |
| worker-verifier.before.txt / .after.txt | Verifier captures before (detached worktree of the base) and after (pushed head) into work/verifier/evidence/ with before-after.md; absent evidence changes the verdict only if the project requires it | section `## Verifier` of worker.md |
| driver-cr-driver.before.txt / .after.txt | CR Driver answers for the plan, passes it to the Verifier, puts evidence in the PR before handback | section `## CR driver` of driver.md |
| driver-stack-driver.before.txt / .after.txt | Each stack CR keeps its own plan | section `## Stack driver` of driver.md |
| driver-evidence-lines.before.txt / .after.txt | The evidence step and `gh pr edit --attach` (confirmed by `gh pr edit --help`, gh 2.103.3) appear | grep of driver.md |
| concepts-tree.before.txt / .after.txt | concepts.md folder tree points to work/verifier/evidence/ | grep of concepts.md |

Nothing else is shown: the change is text only, and the CLI is untouched (git diff 49135f5..585379d lists only three card files).

