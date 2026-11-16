# Verify CR-214

Head: ec84275b087da448681a8bc58ac08c9d34049363

All claims judged at ec84275 (full sha above).

- Gate: `work/gates/20261113-142812.log` first line "gate CR-214 ... head ec84275b..."; just check 58 passed; just scenario github 650/650, gitlab 638/638, pass at ec84275. VERIFIED.
- P10 judged by equivalence (ran `chantier.py preflight` from the worktree with a temp HOME per case; P6/P7 FAIL and exit 2 come only from running inside a linked worktree, not from P10):
  - (a) no settings: P10 warn 16 of 16, names force-push rules and SendMessage, with Bash and PowerShell rules to add. OK.
  - (b) user's equivalent force-push forms (`-u origin chantier/*`, `=chantier/* origin *chantier/*`): 14 of 16, the two covered samples no longer named, the `git -C ... --force-with-lease` sample still named. OK.
  - (c) `Bash(*)` + `PowerShell(*)` only: 16 of 16 (not P10 ok). OK.
  - (d) deny on `git push --force-with-lease*`: force-push samples named as "denied: ... by ...". OK.
  - (e) full RECOMMENDED_ALLOW: "P10 ok". OK.
  - Real settings (HOME=user): "14 of 16", no longer "19 of 19"; matches work/04-p10-real-settings.txt. OK.
- Cards vs spec Areas 2-6 and docs (diff origin/main..HEAD read): Forge permissions (P9) section GitHub/GitLab (GitLab marked unproved with trial), alert sentence, D6 publication either/or, concepts rule 8 with push forms, driver stack push forms and release publication handback, CoS refused-force-push step 3, session-start, init, copilot, claude-code table/JSON/auto-mode evidence/Paste-You should see, tutorial. All present. OK.
- Stored evidence (evidence/04-*): ADMIN, scopes gist/read:org/repo/workflow, rules endpoint raw and %2F both `[]`; card keeps raw form and says both answered. Consistent.
- PR description: posted body equals work/pr-body.md; renders (sections, fold). Summary/Deliverables/Changes match the diff (11 files). Autonomous decision (gh stack detected by extension folder, not `gh extension list`) is declared and matches the observed behaviour (gh-stack installed here, `gh stack` sample shown). Review box carries placeholder `<sha7>`; the Driver's log notes "r1 approved at 7705f00, committed as ec84275" - to be filled by the Driver. Not a failed claim.
- Note (not a failure): the posted PR is still draft.

VERIFIED
