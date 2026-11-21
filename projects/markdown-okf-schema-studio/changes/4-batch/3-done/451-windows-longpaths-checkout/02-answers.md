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
- Owner, 2026-11-21: "Et tout ça partira dans le batch en cours": once final and ready, added to the running batch-07.

## Owner's answers, 2026-11-21 (Fable spec critic's questions)

- lp-Q3 (what the CR proves). Owner: "Aussi just dev + un test": the Evidence also runs `just dev` and one unit test inside a base worktree past 260 characters (e.g. the CR's work/scratch/base); if that fails, the CR comes back with the result.
- lp-Q4 (guard test against `-s` in CONTRIBUTING). Owner: "Non, la doc suffit": text fix only, no new test.
- Settled by the Chief of Staff from the critic (not behaviour): no `git clone -c` advice (all failures were worktree adds); no SwRS and no tiers/log entry (constitution section 1, contributor tooling, check-markers does not scan the justfile); the `git config` step is skipped outside a Git work tree; one sentence in CONTRIBUTING "Windows" section.
