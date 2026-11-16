Given by the user on 2026-11-13 ("est-ce que tu peux rajouter cette demande aussi"), to run in
batch-16. Their text, as given:

# Post the grill summary, plan and demo on the source ticket

When a change comes from a ticket (GitHub, GitLab, Jira or other), Chantier proposes to post on it
what was understood and what will be done, after the owner approves.

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
- **Two-way link**: the PR body names the ticket with the tracker's closing keyword (`Fixes #336` on
  GitHub, `Closes #12` on GitLab, the Jira key in the title or body), and the ticket gets a comment
  with the PR link when it opens.

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

## 2026-11-13, the user's question to the Chief of Staff

- "Est-ce que ticket-summary-on-source couvrira les issues Jira et GitLab, et surtout, respectera
  les instructions mises dans AGENTS.md (ex: 'ticket in this project shall use Closes
  JIRAJPT-1245') ?"
- Restated, in scope: GitHub, GitLab and Jira are all covered in this CR, not GitHub first. Jira
  goes through the CLI the user has installed (or the project's rules name); none installed is
  "a tracker Chantier cannot write to": skip and say so in one line, naming what to install.
- The project's rules rank above this CR's defaults: the form of the ticket reference in the PR
  body or title, the closing keyword, the comment's language or template, which tracker and
  which project key, as `AGENTS.md` (and what it links, `$CHANTIER rules`) says. The defaults
  (`Fixes #336`, `Closes #12`, the Jira key in the title or body) apply only where the project
  says nothing. The draft shown to the user quotes the rule it followed.
- Then: "gh et glab sont souvent utilisés, mais pour Jira c'est parfois plus compliqué, la méthode
  d'accès pourra être différente (MCP, CLI...). Ce sera le projet ou une configuration à
  déterminer plus tard de le dire. Sache juste qu'il y a cette capacité à trouver et à utiliser."
- Restated: GitHub and GitLab go through `gh` and `glab`. For Jira (and any other tracker) the
  access method is not fixed: an MCP server, a CLI or another tool. The project's rules say which
  (a configuration for it may come later, out of this CR's scope); until then the Chief of Staff
  finds the capability it has (the session's MCP tools, an installed CLI) and uses it. None found:
  skip and say so in one line. No hard-coded Jira CLI.
- Then, the reference's default form: "Pour Jira : Closes JIRAJPT-1245. Pour GitLab et GitHub,
  le verbe n'est pas nécessaire, #123 suffit. Dans une section de la PR appelée 'Issues
  References', section cachée si pas de référence."
- Restated (chantier's default, below the project's rules):
  - The PR body has a section `## Issues References`, written only when the CR has a source
    ticket; with none, the section is left out entirely (no heading, no "None").
  - Jira: `Closes <KEY>-<n>` (e.g. `Closes JIRAJPT-1245`).
  - GitHub and GitLab: the bare reference `#<n>`, no verb (`#123`); another repository's issue:
    `owner/repo#<n>` (GitHub) or `group/project#<n>` (GitLab).
  - Note for the user, given by the Chief of Staff on 2026-11-13: on GitHub and GitLab a bare
    `#123` links the issue but does not close it when the PR merges (only `Fixes`, `Closes` or
    `Resolves` do).
- Then: "Tu as raison, il faut mettre les verbes sur GitLab et GitHub." Decided: the default is
  `Closes #<n>` (`Closes owner/repo#<n>`, `Closes group/project#<n>` for another repository) on
  GitHub and GitLab, as `Closes <KEY>-<n>` on Jira; the issue closes at the merge.
