## Summary

On Windows, checking out the base or adding a worktree of this repository could fail with "Filename too long" (paths past 260 characters). `just dev`, the command every new checkout or worktree runs first, now turns on `core.longpaths` for the repository. CONTRIBUTING.md "How to Release" also stops signing off the version commit, as the release guideline already says.

## Deliverables

```just
dev: _git-long-paths      # runs first; Windows: git config core.longpaths true (inside a Git work tree)
                          # Linux and macOS: empty twin, no git config
```

## Changes

- `justfile`: private `_git-long-paths` recipe in two twins (`[windows]`, `[unix]`); `dev` depends on it. Outside a Git work tree the Windows step does nothing and exits 0.
- `AGENTS.md`, `CONTRIBUTING.md` ("Windows"), `.agents/guidelines/local-worktree.guidelines.md`: name the setting and why.
- `CONTRIBUTING.md` "How to Release": the version commit amend is `git commit --amend --no-edit CHANGELOG.md`, with no `-s`.
- `test/build/test_workflows.py`: three tests run the shipped justfile (dry-run order, real run in a git repository, real run outside one).

## Impacts

No visual change. Contributors on Windows no longer hit "Filename too long" once `just dev` has run in the main checkout; other hosts are unaffected.

The setting lives in the repository's shared config, so it applies to every worktree once `just dev` has run in the main checkout; it is already `true` in the author's main checkout.

## Blast radius

Grade: 1. Contributor tooling and docs only; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code): `test/build/test_workflows.py`, 81 passed on Windows
- [x] Requirements: No behaviour change (contributor tooling, outside the product contract)
- [x] Changelog: No user-facing change
- [ ] Local gates: <to fill>
- [ ] Review
- [ ] CI green

## Internal references

- CR-451, batch-07.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
