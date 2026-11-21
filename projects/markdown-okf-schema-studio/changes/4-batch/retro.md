## 2026-11-21 - CR-435, CR-436, CR-439..CR-446 (batch-07)

- [chantier] The ordered stack 439..445 was not a git chain (440/442/444 cut from main, only the forge bases linear): `take CR-446` was refused, a first stack driver wrongly said no restack was needed, and two restacks followed (also the CR-446 release retro's stack point): have the CLI check at each `ship` that an ordered batch's branch is based on the previous CR's head, and have the stack-driver card verify with `git merge-base` before concluding.
- [project] CR-439 needed 5 rounds and CR-445 6 rounds; the later rounds were visual and integration tests red only in CI, because `just preflight` skips the visual, integration and report stages on Windows (also the CR-445 point of the release retro): dispatch the heavy CI (`gh workflow run ci.yml --ref <branch> -f heavy=true`) after the first round of a CR that adds visual or integration tests, and push after round 1 so the visual job runs early, not only at the end.

(critic: kept 2, dropped 8)
