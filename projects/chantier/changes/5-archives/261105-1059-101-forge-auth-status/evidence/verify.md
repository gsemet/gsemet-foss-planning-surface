# Verify CR-101

Head: d8db5da3bfbf2c78aeb73aa54dd8dc69dd7fddc9 (worktree clean, equals PR 21 headRefOid)

## Claim 1: `forge.py auth status` exits 0, `pr close 1` exits 1
Env: FAKE_GH_STATE and LIVE_ORIGIN set (temp bare repo, empty state).

    $ uv run --script evals\kit\forge.py auth status
    Logged in to forge.local as eval (fake forge)
    auth exit=0
    $ uv run --script evals\kit\forge.py pr close 1
    fake forge: `gh pr close 1` is not allowed here
    close exit=1
    $ uv run --script evals\kit\forge.py auth login
    fake forge: `gh auth login` is not allowed here
    login exit=1

Diff also shows `["auth", "status"]` in FORGE_ALLOWED (audit.py) and the docstring updated (forge.py).

## Claim 2: `just check` passes
    25 passed in 3.75s ; check exit=0

## Claim 3: CI green on three systems at head
    gh pr checks 21: just check (macos-latest) pass; (ubuntu-latest) pass; (windows-latest) pass

## PR conditions
gh pr view 21: isDraft=true, state=OPEN, autoMergeRequest=null, headRefOid=d8db5da...
Body first line: `**Eval run: do not merge.** The maintainer decides what happens to this PR.` (exact match).
Main checkout is on `main`.

VERIFIED
