---
title: Post the grill summary, plan and demo on the source ticket
description: When a change comes from a ticket (GitHub, GitLab, Jira or other), Chantier proposes to post on it what was understood and what will be done, after the owner approves.
status: backlog
priority: P1
date: 2026-11-10
---

# Post the grill summary, plan and demo on the source ticket

## Why

A change often starts from a ticket opened by someone else. Today the decisions of the grill stay in
the local change folder: the reporter learns nothing until a pull request appears. Tried by hand on
Markdown OKF-Schema Studio issue #336 (2026-11-10): one short comment, a Markdown plan and an HTML
demo told the reporter exactly what was accepted, before any code.

## What Chantier does

When the grill of an item ends and the item has a source ticket, the Chief of Staff proposes, in one
step, to publish on that ticket:

1. **A comment**: what was understood and what will be done. Short: accepted or not, the scope in
   two to five bullets, what is left out, and "no date yet; the pull request will be linked here".
   Written for the reporter: no internal terms (CR numbers, roles, requirement IDs, rounds).
2. **A plan** in Markdown: the decisions of the grill, rewritten for an outside reader (what changes
   for the user, limits, safety, what the docs will say).
3. **A demo** as a self-contained HTML page, when the change is visible and can be imitated without
   the product: one file, no external resource, no script if possible, using the product's real
   colours or wording. Its first line says it imitates the planned result.

The plan and the demo go where the tracker allows: GitHub issue artifacts
(`gh issue artifact create <n> plan.md --type plan`, `demo.html --type embedded_html`), else
attachments, else a collapsed section of the comment. The comment links them when they are separate.

## Rules

- **Always on human approval.** Chantier drafts the comment, the plan and the demo locally, shows
  them (texts in chat, files sent to the user), and publishes only after an explicit "yes" for that
  ticket. The owner may edit, drop the demo, or decline. Nothing is posted from a sub-agent or a
  Foreman without that approval.
- **Language**: the ticket's language (English by default), whatever the chat language.
- **Check before publishing**: the ticket is the one the item names; the texts contain no private
  path, internal link or other person's data.
- **Verify after publishing**: read back the comment URL and the artifact list; report what is
  visible to whom (for example GitHub artifacts in private preview may be hidden from the reporter).
- **Record** in the item: the comment URL, the artifact numbers, and the date. When the pull request
  opens, Chantier proposes a one-line follow-up comment with its link (same approval rule).
- No ticket, or a tracker Chantier cannot write to: skip and say so in one line.
- **Two-way link**: the PR body names the ticket with the tracker's closing keyword (`Fixes #336` on GitHub, `Closes #12` on GitLab, the Jira key in the title or body), and the ticket gets a comment with the PR link when it opens.

## Where it fits

| Step | Change |
| --- | --- |
| Intake | Record the source ticket (URL, tracker, number) in `01-intent.md` when the request names one. |
| Grill end | New sub-step "Ticket summary": draft, show, ask, publish, record. |
| PR open | Propose the follow-up comment with the PR link. |
| Land | Optional: propose a closing comment ("shipped in X.Y.Z") when the release is out. |

Trackers: GitHub (`gh issue comment`, `gh issue artifact`), GitLab (`glab issue note`, uploads),
Jira (comment and attachment through its CLI or API). Start with GitHub; the others follow the same
draft, approve, publish, verify sequence.

## Done when

- The Chief of Staff skill and the lifecycle describe the sub-step and its approval rule.
- A test or eval shows: no post without approval; the draft holds the three parts; a ticket-less
  item skips the step.
- The example of issue #336 is kept as the reference (comment, plan, demo).
