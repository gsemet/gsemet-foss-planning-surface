# CR-502 stack restack, 2026-11-25

`git rebase --onto chantier/batch-09/cr-506-gallery-a-stable-link-for-each-screensho b0e6c6d9`

- Old base b0e6c6d9, old head 3df0c861.
- New base c2f55938 (CR-506), new head 316f283e. Commits: 4769fe64 (was 756d8565), 316f283e (was 3df0c861).
- Rebase finished, tree clean, not pushed, not shipped.

## Conflicted hunks

1. 756d8565, CHANGELOG.md, top of "Unreleased": HEAD had the CR-506 entry, the commit added the
   CR-502 entry. Kept both, CR-502 first (newest on top), CR-506 next. The CR-508 entry is untouched.
2. 756d8565, requirements/tiers/log.md, under "## 2026-11-25": HEAD had the CR-506 and CR-508
   sections, the commit added the CR-502 section. Kept the three, CR-502 first, under the single date
   heading.
3. 3df0c861, CHANGELOG.md, same place: the commit turns "PR #TBD" into "PR #520". Applied that
   change and kept the CR-506 entry below it.

## Checks

- `git range-diff b0e6c6d9..3df0c861 c2f55938..HEAD`: differences only in the CHANGELOG.md and
  log.md context. The five clip commits (e0d723d5..b0e6c6d9) are not in the branch and no entry of
  theirs was added.
- No byte-order mark added (the resolved files differ from the base only by added lines).
- `just requirements-update`: 0 files updated.
- `just requirements-lint`: pass, 1227 requirements, 0 errors, 26 warnings (broken cross-link W2).
- Fast gate, `just -f <worktree>/justfile -d <worktree> check`, at 316f283e: pass (exit 0). Node
  tests 5269 (5249 pass, 0 fail, 20 skipped) and 107 (105 pass, 0 fail, 2 skipped), clip kit 35 pass,
  pytest build tests 205 passed. Tree clean afterwards.
