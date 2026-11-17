# Task 263

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-263. Branch: change-requests/263-lifecycle-generic-split. One PR, one or more commits, documentation and tooling only.
The approved audit is `02-audit.md` in this folder: its classification table, precedence, release
split and vocabulary table are the specification. `00-request.md` holds the owner's decisions and
wins over the audit's recommendations. Line numbers in the audit refer to commit `8e08d00f`.

## Change

1. New project guidelines in `.agents/guidelines/`: `pull-request.guidelines.md`,
   `stacked-prs.guidelines.md`, `local-worktree.guidelines.md`, `owner-review.guidelines.md`. Move
   the text the audit assigns to them, plus a "During a change" section in
   `requirements/guidelines/requirements.guidelines.md`.
2. `change-requests-lifecycle.guidelines.md` keeps only the generic parts, with Chantier's vocabulary
   and folder names. It absorbs `state-file.guidelines.md` (delete that file, update the references)
   and the release role moved out of the release guideline. Its opening says that it is the process
   guideline and ranks below the project guidelines. It may link to project guidelines.
3. `release-process.guidelines.md`: split as in the audit's "Release split". What stays uses no role
   name.
4. `.agents/constitution.md`: opening line names the order; a short new section states that the
   process never overrides a project rule; section 4 "Details" links to `pull-request.guidelines.md`
   and no longer to the lifecycle.
5. `AGENTS.md`: precedence list with the process guideline as level 4; a "Process" section holding the
   only link to the lifecycle guideline; one "When..." line per new guideline; the `STATE.md` entry
   removed.
6. `ci.guidelines.md` rule 10 points to `pull-request.guidelines.md`.
7. New names in `scripts/generate_orchestrator.py`, `test/build/test_generate_orchestrator.py`, the
   `justfile` if needed, `.agents/skills/markdown-studio-exploratory-qa-claude/` (SKILL and
   `scripts/coverage-map.py`). `STATE.md` becomes `STATUS.md`. The script reads the new stage folders;
   an archived CR's spec is `03-change-spec.md`, else `00-request.md`, since archives keep their old
   file names.
8. Correct the inconsistencies of the audit's section. Check `approved_at` against okfreq before
   changing it. Change no other rule.
9. New test in `test/build/` (and in the `justfile` target that lists those tests): no project
   guideline, nor the constitution, links to the lifecycle guideline or names a process role
   (Chief of Staff, Foreman, driver, Inspector); `AGENTS.md` links to it exactly once.

## Isolation rule

Project guidelines say "the agent that opens the PR", never a role. No Markdown link to the lifecycle
guideline outside the `AGENTS.md` "Process" section.

## Not in this task

Do not touch `.agents/changes/`: its folders are renamed locally after the merge. Do not adopt
anything from the audit's "Differences kept out". PRs 320 and 321 are unrelated.

## Tests first

Write the isolation test first and show that it fails on the unchanged guidelines. Update the script's
tests to the new names before the script.

## Gates

`just check`, then `uv run --group docs --group release --group requirements pytest test/build/test_generate_orchestrator.py`
and the new test. No SwRS change: no product behaviour changes. The PR body says that the constitution
changes and needs the maintainer's approval, and states whether `just preflight` ran.
