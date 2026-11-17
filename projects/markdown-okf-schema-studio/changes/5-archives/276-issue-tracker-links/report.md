# Report — 276-issue-tracker-links

Status: **done** (2026-11-10, branch `change-requests/276-issue-tracker-links`, PR #344, merge commit `a12a16bc`; no GitHub issue in this project; the Chantier part is issue gsemet/chantier#101, not done here).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Process guidelines text: change requests link to GitHub issues, and PRs are opened as drafts until mergeable; five files only (`change-requests-lifecycle.guidelines.md`, `pull-request.guidelines.md`, `release-process.guidelines.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `AGENTS.md`) | `a12a16bc` |

## Proof of completion

- One round: Sonnet coder, Sonnet Inspector. The coder fixed a first `just check` failure (`test_no_project_rule_names_a_process_role`: constitution section 8 forbids role names in project guidelines) by wording the two project guidelines as "the agent that talks to the owner"; role names stay only in the lifecycle file.
- `just check` and `just ci-static` passed locally. A full `just preflight` timed out locally (580 s) during its visual stage; CI covered the rest.
- CI at head `9e349314`: PR run 42902375667 green (static, static-windows, visual, report, checks); heavy jobs skipped, no heavy run needed for text.
- The Chantier repository was not touched.

## Process notes

- The Inspector's single blocker was the commit subject length (82 characters, limit 71). The driver amended it to 67 characters without a second Inspector round; the content was unchanged.
- The auto-mode classifier refused two actions in the driver (a `pkill` of the timed-out preflight, and `gh pr edit` plus `gh pr ready`). `gh pr edit` and `gh pr ready` were then run by the Chief of Staff on the owner's explicit go; the Foreman did not run them.

## Open items

- Two minor wording suggestions from the Inspector were left: in `pull-request.guidelines.md`, "Draft until mergeable" says "CR" and "`ready` is reported", which are process vocabulary.
