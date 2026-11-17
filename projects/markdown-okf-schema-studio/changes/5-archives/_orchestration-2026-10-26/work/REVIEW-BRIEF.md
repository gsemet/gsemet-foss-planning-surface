# Reviewer brief
Read STACK-BRIEF.md (same folder), .agents/constitution.md, requirements/guidelines/requirements.guidelines.md.
Review HEAD commit (git show HEAD) of the CR branch in its worktree. Check: code vs constitution (layers, file size);
SwRS <-> code <-> test consistency (markers, Known issue lines removed correctly incl. leftovers for the same
behaviour, no backlog/CR names in requirement text, requirement text states current behaviour); the new test fails on
the previous code (reason, or verify in a scratch copy; never leave edits); commit message vs
git-commit-message guideline (trailer exactly `Assisted-by: Claude:Sonnet-5.5`, no Co-Authored-By, scope allowed);
PR body (pr-body.md in the CR folder) vs .github/PULL_REQUEST_TEMPLATE.md (external reader, no internal ids outside
"Internal references"; the orchestrator appends the Generated-with line); scope creep (only the CR's behaviour).
Re-run okfreq gates with UV_PROJECT_ENVIRONMENT=/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.venv
and the touched unit tests (`check:boundaries` may fail on local Node 25: environment, ignore).
Do NOT edit files. Reply: PASS, or a numbered list of required fixes. Max 12 lines.
Reviewers: check that the PR body has '## Deliverables' (renamed from 'Deliverable showcase').
