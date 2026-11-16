Moves the version to 0.7.0 in the 30 files that carry it, by `just release minor`, on top of 55d32c7, the head of `main`.

`just check` passes on Windows (28 tests). `just scenario` passes at 55d32c7 and at this head (312/312 on github and on gitlab). Main's CI was green at 55d32c7.

The `real` eval campaign was not run for this release, on the user's decision: this departs from `CONTRIBUTING.md`.

After the merge, by rebase: `just tag`, then `gh release create v0.7.0 --generate-notes`, each on the user's approval.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
