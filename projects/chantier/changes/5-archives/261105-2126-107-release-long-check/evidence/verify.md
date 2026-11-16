# Verify CR-107

Head: 9c56f7b5e6fcd83d56327ec49664b881269ffe0d (worktree HEAD equals PR headRefOid)

1. chief-of-staff.md, Releases: `git diff origin/main` adds the ask (no long check on the default branch's exact head before the version commit), the why (per-CR gates miss what CRs break together, skipped checks go unseen), the offer to write it in the project, and "The user's answer rules; chantier imposes no gate." OK
2. docs/use-cases.md, "Make a release": one sentence added saying so. OK
3. Only those 2 files changed (`git diff origin/main --stat`); CLI, agents, Release driver card untouched. OK
4. `just check`: 25 passed. `just scenario`: github 164/164 and gitlab 164/164 (work/gates/20261105-183359.log). CI at head: 4 checks (check on ubuntu, macos, windows; scenario on ubuntu) all SUCCESS. OK
5. Never merged (read only via `gh pr view 40`): state OPEN, isDraft true, autoMergeRequest null, body's first line is exactly `**Eval run: do not merge.** The maintainer decides what happens to this PR.` OK

VERIFIED
