## 2026-11-24 — batch-09 (CR-467 to CR-479, release v1.12.1)

- [chantier] `asks`, `stack`, `note` and `order done` disagree on `--epoch`; a refused `note --epoch` exits 2 silently: dropped by the critic: the only source is the CoS's account, no event or note shows it, and nothing lost reached the user.
- [chantier] A conflict-resolver pushed a branch itself against its card (CR-479): dropped: no work note or event shows it, one unproven occurrence with no cost.
- [chantier] (release) The release procedure says the tag is a main-checkout step but CI's tag-release job creates it: dropped: it happened once and cost nothing ("no just tag needed").
- [project] (release) The version push heavy run takes about 17 minutes with integration last: dropped: its own author says there is nothing to fix.
- [chantier] The watcher ends after 2 h without an event and the board stops with it: merged into the serve/junction point (same result for the user, same component).

## 2026-11-27 — batch-09 (CR-484 to CR-519)

- [chantier] The card's one CI re-run conflicts with the project's CI rules 9 and 12: dropped by the critic: one occurrence (2981), the instruction precedence already made the project rule win, no ask and no cost.
- [project] The CI visual job ran at its 15-minute limit and was cancelled on six CRs: dropped: Drivers flagged the margin hours before A-33 and nothing changed, so a report warning would change nothing; visual is fixed by CR-515 and integration is covered by 2-backlog/P1/split-heavy-ci-jobs.
- [project] Heavy and CI runs went red on flakes and network: dropped: both flakes are filed (1-inbox/flaky-preview-group-lock-real-input, 1-inbox/trusted-suite-launch-deadline-flake); the ETIMEDOUT and LFS timeouts happened once each and cost one re-run each.
- [project] PRs touching session or real-window paths reached ready without the heavy CI run: dropped: covered by 2-backlog/P1/local-dev-ci-judges, and the guideline rule was already kept on 2026-11-24.
- [project] The heavy-run re-dispatch rule counts the last green run only when the head is unchanged: dropped: one occurrence with no cost (4384).
- [project] A renderer change broke the clips of other CRs (CR-500): dropped: the break was not silent, CR-503 saw it and left the hunk for CR-500, so a CI clip check would not have saved the round.
- [project] The merge-commit check read a stack's chained test merge as branch merges: dropped: already done, CR-510 added seven tests including four chained-merge cases.
- [chantier] refused `gh pr edit 535 --base <branch>`: merged into the forge-stack point: same fix, forge-stack retargets its own placed PRs.
- [chantier] refused `next stack --lease <n>`: merged into the changed-cards point: the same card command.
- [chantier] refused a stray redirect onto the worktree's `.git` file (CR-504): dropped: one event logged three times, refused, nothing ran, no cost.
- [chantier] refused a verifier's `python -I work/scratch/verify-cdp.py` re-run (CR-509): dropped: one occurrence, not retried, no defect reaching the user.
- [chantier] refused a probe on downloaded browser shells (CR-517): dropped: one occurrence, stopped by the classifier, downloads deleted, no defect reaching the user.
- [chantier] refused `rm "$L"/*.log` in a verifier clean-up: merged into the card-rules point: a scratch folder the CLI removes means no `rm` over variable paths.
- [chantier] refused shell writes outside the writes folders: merged into the card-rules point: the same fix, a scratch folder on each worker's writes line.
- Counts corrected by the Foreman in two kept points, after the critic: the forge-stack point has five asks (A-21, A-25, A-43, A-44, A-75), not seven; the cleanup point has 23 merged worktrees left in place (CR-495 to CR-517), not 22.
