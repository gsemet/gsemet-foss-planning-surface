# Conflicts: rebase of CR-245 onto CR-244 (403887f)

## skills/chantier/references/driver.md, "Stack driver", first paragraph (one hunk)

- HEAD (CR-244): "merges in one go ... merged in one action from the top PR".
- CR-245: "merges in one action from the top PR or one PR at a time from the bottom ... on GitHub, a chain of PRs".
- Choice: kept CR-244's wording and added "(on GitLab, one MR at a time from the bottom, below)", since the GitLab chain paragraph that follows (kept from CR-245) already says it. No other hunk conflicted.

## Result

Rebase finished: 5daab2e (feat, GitLab chain) and 5ccb5e0 (fix) on 403887f. Not pushed.

Fast gate: `just check` (HOME, USERPROFILE, CLAUDE_CONFIG_DIR in a scratch folder): ruff format and check clean, mypy 79 files ok, uv lock ok, 63 tests passed, release notes ok. Exit 0.
mypy --strict --platform linux, darwin, win32 (`uv run --locked --group dev --with mypy==1.20.0 --with types-psutil mypy --strict --platform X`): no issues in 79 files, each.
