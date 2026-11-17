---
title: Tracker issues and draft pull requests in the change request process
description: Change specification of CR 276, two pull requests (this project and Chantier); process and guidelines only.
issue: none
date: 2026-11-10
---

# Tracker issues and draft pull requests: change specification

## Goal

When a change starts from a tracker issue, the reporter hears from it at each step: the grill
result, the pull request, the release. The issue closes when the pull request merges. Every pull
request is a draft until the owner can merge it. The generic rules (when, who) go in the process
guideline and in Chantier; the GitHub specifics (how) stay in this project's guidelines.

## The five rules, with the owner's answers

| # | Rule | Who | When |
| --- | --- | --- | --- |
| R1 | Grill comment: what was understood, what will be done; a Markdown plan and an HTML demo attached when the tracker supports it | Chief of Staff | When the CR opens, after the owner approves the text |
| R2 | Links both ways: `issue:` in the `01-intent.md` front matter, carried into `03-change-spec.md` and the PR body (closing keyword); a comment on the issue with the PR link | Chief of Staff (comment), driver (PR body) | PR opened, after the owner approves the comment text |
| R3 | The issue closes by the closing keyword on merge, never by hand | Nobody | Merge |
| R4 | Release comment "Released in <release link>" on each issue shipped | Chief of Staff | After publication, one owner approval for the whole list |
| R5 | A PR is a draft until mergeable (CI green at its head, review done); in a stack, each PR turns ready on its own when it is mergeable, without waiting for the rest | CR driver; stack driver in a stack | PR opened as draft; ready at `ready` |

Common to all: only the Chief of Staff posts on an issue. Drivers, the Foreman and sub-agents
never do. No comment is posted without the owner's approval of its text. An item with no issue
skips R1, R2 and R4 with one line in its notes. CI already runs on drafts (`ci.yml` has a plain
`pull_request:` trigger): no workflow change.

## PR 1: this project (`gsemet/markdown-okf-schema-studio`)

Branch from fresh `origin/main`. Files:

1. `.agents/guidelines/change-requests-lifecycle.guidelines.md` (process, generic: when and who)
   - Vocabulary: **Tracker issue**: the issue an item comes from, if any, recorded as an `issue:`
     line in the `01-intent.md` front matter (`issue: none` when there is none).
   - Lifecycle table:
     - 2 Grill: carry the `issue:` line into `03-change-spec.md`.
     - 3 Open: new sentence: with a tracker issue, the Chief of Staff drafts the grill comment
       (R1), shows it to the owner, posts it after approval, and records the comment link in
       `02-answers.md`.
     - 8 PR: the driver opens the PR as a draft, its body naming the issue with the tracker's
       closing keyword (R2, R5). The Chief of Staff, on hearing the PR link, drafts the one-line
       comment with that link and posts it after approval.
     - 10 Notify: CI green at the head and the review approved: the driver marks the PR ready for
       review, then writes `status: ready`. A CR sent back for a new round goes back to draft
       first.
     - 11 Land: the issue closes by itself on merge; nobody closes it by hand (R3). The Foreman
       checks it is closed and writes it in `report.md`; an issue left open is reported, not
       closed.
   - "Stack mode": the stack driver marks each PR of the stack ready on its own, as soon as its
     CI is green at its head and its CR is `ready`, without waiting for the rest (R5). Add the same
     words to the stack driver prompt.
   - "Release driver": the release driver lists, in the release folder, the issues the release
     closed; it never comments. The Chief of Staff drafts the "Released in" comments (R4).
   - "Constraints": only the Chief of Staff posts on a tracker issue, and only text the owner
     approved; drivers, the Foreman and sub-agents never comment on issues.
   - `report.md` format: one line "Issue: <link> (closed on merge)" or "Issue: none".
   - No GitHub command in this file; it points to the project guidelines for the how.

2. `.agents/guidelines/pull-request.guidelines.md` (project: how)
   - New section "Draft until mergeable": `gh pr create --draft`; `gh pr ready <n>` only when CI is
     green at the head, the review is approved and `ready` is reported; `gh pr ready <n> --undo`
     when a CR goes back to a round. In a stack, each PR turns ready on its own. The release
     version PR and its fix PRs follow `release-process.guidelines.md`.
   - New section "GitHub issues": the issue number comes from the `issue:` line. The PR body ends
     its Summary with `Fixes #N` (one line per issue); this is not an internal reference. The
     comments are posted by the Chief of Staff only, after the owner approves the text:
     `gh issue comment <n> --body-file <file>`; the plan and the demo with
     `gh issue artifact create <n> <file> --type plan` and `--type embedded_html`, file names
     without a colon. Read back the comment URL and artifact list after posting. Never
     `gh issue close`: GitHub closes the issue on merge.

3. `.agents/guidelines/release-process.guidelines.md` (project: how)
   - Step 7 (archive): the `report.md` also lists the issues the release closed (from the PRs'
     closing references, `gh pr view <n> --json closingIssuesReferences`, and the CRs' `issue:`
     lines).
   - New step 8: the Chief of Staff drafts "Released in
     https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/vX.Y.Z" for each listed
     issue, gets one owner approval for the whole list, posts with `gh issue comment`, and reads
     the comments back. This comes after publication, so it does not break "nothing is asked of
     the owner between the notes review and the publication".

4. `.github/PULL_REQUEST_TEMPLATE.md`: in Summary, one comment line:
   `<!-- Fixes #N when the change closes a GitHub issue -->`.

5. `AGENTS.md`, "Guidelines": one bullet: "When a change comes from a GitHub issue, or when
   opening or marking ready a pull request: [pull-request.guidelines.md] ("GitHub issues", "Draft
   until mergeable")". No other change.

Commit: `docs: link change requests to their GitHub issues and open pull requests as drafts`
(type `docs`, no scope: scopes are only for `feat` and `fix`), per
`git-commit-message.guidelines.md` with its `Assisted-by:` trailer.

Acceptance:
- `just check` passes (formatting of the Markdown and the template); `just preflight` passes
  (constitution, section 4).
- No change under `src/`, `test/`, `requirements/` or `.github/workflows/`:
  `git diff --stat origin/main` lists only the five files above.
- `grep -n "gh " .agents/guidelines/change-requests-lifecycle.guidelines.md` finds no new GitHub
  command (the how stays in the project guidelines).
- The PR is opened with `gh pr create --draft`, its body follows the template, and it turns ready
  by the new rule.

## Chantier: an issue, not a PR

Owner, 2026-11-10: no PR on Chantier. The Chief of Staff opens one issue on `gsemet/chantier`
carrying the generic rules (draft in `chantier-issue.md`, posted after the owner approves its
text). No Driver touches the Chantier repository.

## How it ships

- One PR in this project, opened with `gh pr create --draft`, turning ready when its CI is green
  at its head and its review is done.
- No product code, no requirements change, no workflow change, no `tiers/log.md` entry.
- This CR has no tracker issue (`issue: none`), so it posts no comment itself.

## Out of scope

- GitLab and Jira specifics in this project (it uses GitHub only).
- Chantier CLI changes (`rails.py`, `commands.py`): the rules are judged by the roles, not refused
  by the CLI; a CLI check would come from measured cost, per Chantier `AGENTS.md`.
- Chantier's own `docs/release-process.md` (Chantier's project rules, not the generic cards).
- Comments on issues of past releases.

## Blast radius

Grade 1: text only, read by agents. What could break: an agent opens a PR
ready instead of draft, or a stacked PR turns ready too early; the owner still merges by hand, so
nothing merges by mistake. Roll back with `git revert` of the one commit.

## Open questions

None. (Q1, a Chantier dependent PR outside a stack, left with the Chantier PR; it is noted in the
Chantier issue.)
