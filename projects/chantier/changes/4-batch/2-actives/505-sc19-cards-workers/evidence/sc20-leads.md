# SC20 evidence: the three leads of the inbox item `driver-card-leads-left-by-role-cards-sti`

Source: `1-inbox/driver-card-leads-left-by-role-cards-sti/intake/request.md`, lines 4 to 6.

| lead | quoted (request.md) | where it landed |
| --- | --- | --- |
| 1 | line 4: "The Release driver section should point to the typed `pipeline` wait for a long run on main: not in `driver.md`." | `cards-next/release-driver.md:8`: "A step that waits on a pipeline job is recorded with a typed wait: `handback <cr> blocked <reason> --wait pipeline[=<sha>] --lease <n>`." |
| 2 | line 5: "Read a project guideline by section, not whole: not in `driver.md`." | one sentence ending "by section." at `cr-driver.md:5`, `stack-driver.md:5` and `release-driver.md:5` (the three Drivers that push), after "Read the project's first instruction file whole and its other guidelines ..." |
| 3 | line 6: "Wait only in a background shell: half there ...; nothing says a Monitor is unproved for a subagent." | `cr-driver.md:10`: "A long wait is one command in a background shell, then `$CHANTIER lease <cr> hold --lease <n>`, then `$CHANTIER host end-turn-background`; the end of the command wakes you (`help ci`)." and `topics/ci.md`: "A Monitor tool used from a subagent is unproved; use the background shell." |

Greps that prove them: `grep -n 'pipeline' cards-next/release-driver.md`; `grep -n 'by section' cards-next/cr-driver.md cards-next/stack-driver.md cards-next/release-driver.md`; `grep -n 'unproved' cards-next/topics/ci.md`.
