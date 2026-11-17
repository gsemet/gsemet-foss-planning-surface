# The version commit carries a Signed-off-by

`just bump-version` creates the version commit with a `Signed-off-by` trailer (justfile comment:
"create a signed-off version commit"). The commit guideline
(`.agents/guidelines/git-commit-message.guidelines.md`) does not allow it; the v1.9.0 version
commit carries one.
