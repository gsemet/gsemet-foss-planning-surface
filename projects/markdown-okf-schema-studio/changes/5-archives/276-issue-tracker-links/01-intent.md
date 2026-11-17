---
title: Tracker issues and draft pull requests in the change request process
description: Comments and links between a CR and its tracker issue, from grill to release, and draft PRs until mergeable; generic rules apart from this project's specifics.
status: inbox
date: 2026-11-10
---

# Tracker issues and draft pull requests in the change request process

> [!NOTE]
> Owner's requests, 2026-11-10, after CR 272 (#336) and CR 273 (#334). To do after CR 273 and the
> P1 table Escape CR. Process and guidelines only, no product code.

## The requests

When a CR comes from a tracker issue (GitHub, Jira, GitLab or other):

1. **Grilled and ready.** When the grill is done and the item becomes a CR, post a short comment on
   the issue: what was understood and what will be done (plus a Markdown plan and an HTML demo as
   attachments when the tracker supports it, as done on #336).
2. **Links both ways.** The CR files and the PR name the issue; the PR body uses the tracker's
   closing keyword; a comment on the issue links the PR when it opens.
3. **Transition.** The issue closes by itself when the PR merges; nobody closes it by hand.
4. **Release.** At the release, each issue fixed in it gets a comment
   "Released in <link to the release notes>".

For every CR, issue or not:

5. **Draft until mergeable.** A PR opened before it is ready is a draft. It turns ready for review
   only when the owner can merge it (CI green at the head, review done, `ready` reported).

## Split: generic process versus this project

The owner asks to keep apart what any project using the process needs from what is specific to this
one. The process guideline (`change-requests-lifecycle.guidelines.md`, swappable with Chantier) says
**when** and **who**; the project guidelines and `AGENTS.md` say **how** here.

| Rule | Generic (process guideline, and Chantier) | This project (project guidelines, `AGENTS.md`) |
| --- | --- | --- |
| Tracker | "the item's tracker issue, if any", recorded in the intent | GitHub issues of `gsemet/markdown-okf-schema-studio`, through `gh` |
| Grill comment | Post what was understood and what will be done when the CR opens, after the owner approves the text; attach a plan and a demo when the tracker can | `gh issue comment`; `gh issue artifact create` (`plan`, `embedded_html`), names without a colon |
| Links both ways | The PR names the issue with the tracker's closing keyword; the issue gets a comment with the PR link | `Fixes #N` in the PR body (`pull-request.guidelines.md`) |
| Transition | Closes on merge through the tracker; never by hand | GitHub's closing keyword does it |
| Release comment | Each issue shipped gets "Released in <release notes>" after the release is published, after one owner approval for the list | The GitHub release URL; a step of `release-process.guidelines.md` |
| Draft PR | A PR is a draft until the owner can merge it; the driver (or the stack driver) marks it ready at `ready` | `gh pr create --draft`, `gh pr ready` (`pull-request.guidelines.md`; check that the CI still runs on drafts) |
| Who posts | The Chief of Staff only; drivers and the Foreman never comment on issues | — |

## For the grill

| Question | First recommendation |
| --- | --- |
| Approval | Every issue comment is drafted by the Chief of Staff and posted after the owner approves its text; at release, one approval for the whole list. |
| Where the issue is recorded | An `issue:` line in the `01-intent.md` front matter, carried into `03-change-spec.md` and the PR body. |
| Draft and CI | Check that `ci.yml` runs on draft PRs (`pull_request` types) before making drafts the rule; else add `ready_for_review`. |
| Draft and stacks | A stack's PRs stay drafts until the whole stack is mergeable; the stack driver marks them ready together. |
| Chantier | Port the generic column to Chantier with its backlog item `tracker-grill-summary`. |
