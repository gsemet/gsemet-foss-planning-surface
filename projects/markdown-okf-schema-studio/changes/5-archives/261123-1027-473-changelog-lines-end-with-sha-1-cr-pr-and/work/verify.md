# Verify CR-473

Head: c9712e21cc89fb34fd496bce918d2b83980fece3

All claims judged at d86fd914.

1. Spec tests 1-11. `uv run --no-sync python -m pytest test/build/test_changelog_refs.py -v`: 11 passed (group, GitLab/Jira, no group, multi-line, two bullets, second run, dirty file, not on base, empty section, LF, --skip-missing).
2. Guideline isolation. `pytest test/build/test_guideline_isolation.py -q`: 9 passed.
3. Scenario step 1 (scratch repo, prepared Unreleased, origin/main ref = HEAD, script run directly): output `commit cfcf0d9: Alpha line ...`, `commit 8605489: Beta line with no group`, `2 line(s) updated`; file now `(commit cfcf0d9, CR-1 alpha, PR #2, issue #3)` and `(commit 8605489)`; `git log -S` shows cfcf0d9 and 8605489 for the same lines. Older section untouched.
4. Step 2: after committing the result, a second run printed "No line to update", exit 0, `git diff --stat` empty.
5. Step 3: uncommitted edit, run: "CHANGELOG.md has uncommitted changes: commit or discard them first", exit 1, file unchanged.
6. Diff review: pull-request guideline "CHANGELOG line" section and ready-bullet condition, release-process steps 2, 5, stack step 1 and release-notes clause, CONTRIBUTING steps 2-3, justfile recipe and release-tests entry, SwRS CORE-094, all as specified. Section 7 (rewrite Unreleased lines): Unreleased is empty on this base, nothing to rewrite.
7. PR #489 description: renders, sections consistent with the diff, no images, Known gaps not needed (no unverified claim).
Not run: the `just changelog-refs` recipe itself (script run directly with the same arguments); `just check` / CI reported green by caller for static jobs.

VERIFIED

## Description pass at d86fd914705b4be0e9a674a68905677a70f31064

Command: gh pr view 489; chantier log CR-473 | grep -i -E "inspect|approv"
- Summary, Deliverables, Changes match the diff (10 files): OK.
- Review box says "approved at d86fd91"; the only approval note in the log is "r1 inspector approved at d9b3cd6bef9659f401b24337159691b7306fe907" (the base SHA, no note for d86fd91). NOT VERIFIED: box SHA matches no note.
- Box also names "inspector" as doer outside Internal references.

NOT VERIFIED (description)

## Description pass 2 at d86fd914705b4be0e9a674a68905677a70f31064

Commands: `gh pr view 489 --json body,...`; `git diff --stat origin/main...HEAD`; `chantier log CR-473`; reads of scripts/changelog_refs.py and the justfile diff.
- Summary, Deliverables, Changes match the diff (10 files: script, 11 tests added to release-tests, justfile recipe, guidelines, CONTRIBUTING, SwRS): OK. Claimed behaviours (git blame, base check, dirty file stop, --skip-missing, idempotent) found in the script.
- Review box "approved, committed as d86fd91" matches the log note "r1 approved at d9b3cd6b, committed as d86fd914": OK. No role name outside Internal references; CR-463 in examples is the product format shown: OK.
- No images; Impacts "No user-facing change" with reason; Known gaps not needed (no unverified claim): OK.

VERIFIED (description)

## Move d86fd914..c9712e21 (restack onto CR-472), judged at c9712e21cc89fb34fd496bce918d2b83980fece3

- Touched: justfile `release-tests` line and the tests. `uv run --no-sync python -m pytest test/build/test_changelog_refs.py test/build/test_guideline_isolation.py test/build/test_no_merge_commits.py -q`: 32 passed. `grep release-tests justfile` line 213 lists both test_no_merge_commits.py and test_changelog_refs.py (both kept).
- `git diff --stat 4802edf6 HEAD`: the same 10 files as before the move (script, tests, justfile, two guidelines, CONTRIBUTING, SwRS, log, index); worktree clean.
- Claims 1, 3-6 (script behaviour, scenario steps, diff review): carried from d86fd91: script and its tests unchanged by the move (only the justfile test list conflicted).
- Description (gh pr view 489): Review box "approved at c9712e2" matches log note "move d86fd91..c9712e2 (restack) inspector approved at c9712e21"; box "CI green" deliberately unticked; no images; content matches the 10-file diff.

VERIFIED
