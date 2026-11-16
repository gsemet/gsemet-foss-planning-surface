Head: dc13efef01c093032b98b696c12db56ccc7a6661

1. Cards carry the rule, with GitLab/Copilot "unproved" (judged at dc13efe): `git show dc13efe` shows concepts.md (rule + "Copilot host's path is unproved", glab unproved), driver.md (run no gate, --no-gate quoting the rule, "GitLab and Copilot: unproved"), foreman.md (reads job via gh pr checks, glab unproved, Copilot unproved), chief-of-staff.md (skip gate check, "GitLab and Copilot: unproved"). Pass.
2. `Select-String skills/chantier/references/*.md "declare none or exempt"`: no match. Pass.
3. docs/gates.md: paragraph + "- Long gate: the pipeline's `test` job, green at the PR's head." present. Pass.
4. AGENTS.md names `just scenario (ubuntu-latest)`; .github/workflows/ci.yml:35 `name: just scenario (ubuntu-latest)`. Pass.
5. CR's own commit `git show --stat dc13efe`: 6 files (AGENTS.md, docs/gates.md, 4 cards); no CLI, tests, scenario. Note: `git diff --stat origin/main` is wider (CLI files) only because the branch is stacked on CR-262/265 commits (merge-base afd42be vs origin/main is not the base); not this CR's change. Pass.

Short pass on the posted description at dc13efe: Summary/Deliverables/Changes match git show --stat dc13efe (6 files); gh pr checks 220: all five pass at head; gate log line 1 names CR-269 and dc13efef01c093032b98b696c12db56ccc7a6661; Known gaps present. VERIFIED
Head: dc13efef01c093032b98b696c12db56ccc7a6661
