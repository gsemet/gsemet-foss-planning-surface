# Windows setup and release doc fixes: core.longpaths in `just dev`, no sign-off in CONTRIBUTING

See intake/request.md (long paths, batch-06 retro) and intake/request-contributing-release-signoff.md
(CONTRIBUTING release step 3 still shows `-s` on the version commit, CR-434 release Driver). The
owner merged the two small fixes into this CR (2026-11-21).

## Grill, 2026-11-21 (owner's answers, asked by the Chief of Staff)

- lp-Q1 (how to fix "Filename too long"). Owner: "just dev le règle": on Windows, `just dev` runs
  `git config core.longpaths true` in the repository, so every new worktree is covered; AGENTS.md
  (Setup) and the local-worktree guideline say so.
- lp-Q2 (CONTRIBUTING sign-off). Owner: "Avec longpaths": same CR. CONTRIBUTING "How to Release"
  matches release-process.guidelines.md: the version commit carries no Signed-off-by (today line
  629 runs `git commit --amend --no-edit -s CHANGELOG.md`).
