# Answers

Short name: `ci-gallery-dispatch`

## 2026-11-17: owner's go (no grill)

1. ci-gallery-dispatch-Q1: **Add this finding to the running batch?** Owner, 2026-11-17: add the
   inbox items to the running batch-06 now. That is the go for this finding of CR-342's Verifier;
   no grill was held. The specification is written from the intake, `.github/workflows/ci.yml`
   and `.agents/guidelines/ci.guidelines.md`.
2. ci-gallery-dispatch-Q2: **Goal.** From the Chief of Staff's brief: on
   `gh workflow run ci.yml --ref <branch> -f heavy=true` the site artifact is built, and the
   `gallery` job does not run when a job it needs failed. The Driver proves it with a dispatch run
   on the PR branch and links that run in the PR.
3. ci-gallery-dispatch-Q3: **Spec critic?** No.
