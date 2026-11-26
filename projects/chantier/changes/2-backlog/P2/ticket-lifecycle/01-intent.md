# What chantier does with a ticket, from first reading to release

The user wants the duties chantier owes a tracker ticket encoded, from the first analysis to the release (their words in `intake/request.md`). The Chief of Staff performs them: it shows the user each message verbatim and posts only on their agreement. Filed and set to P2 on the user's word (2026-11-27). Not grilled. A large part is already in the cards; what is left is the difference below.

## Asked, and what the cards already say (read 2026-11-27 at `4d12a5be`)

1. **After a first analysis, say what was understood, rephrased, briefly.** In part: `help ticket-summary` has the reporter told what was accepted before any code (accepted or not, the scope in two to five bullets, what is left out, a plan and sometimes a demo). The Griller drafts, the Chief of Staff shows and posts. Difference: its only trigger is the user's "grilled enough", which may come well after a first analysis.
2. **The PR names the ticket with a closing verb.** Present: the PR template's `## Issues References`, one line per ticket, `Closes #<n>` on GitHub and GitLab, `Closes <KEY>-<n>` on Jira, or the project's own form.
3. **After implementation, say on the ticket where it was implemented (the PR or PRs).** In part: one line "The pull request is open: <PR link>." is proposed when the PR link is first seen, and only for a CR with a recorded post. Difference: no message once the work is implemented, and none after a declined or skipped first summary.
4. **After a release, annotate each ticket it delivered with "Released in version xxx" and the link.** In part: `help release-chief` has the Chief of Staff list, once the release is published, the issues it ships (the `issue:` lines of the CRs it contains) with "Released in <the release's link>"; one yes covers the list. Differences: the user says the Release driver finds the tickets; the text carries no version number; by that rule a ticket named only in a PR, on no CR's `issue:` line, is not listed.

Showing the exact text and waiting for a yes: present for the first summary, the PR line and the release list.

## Also observed

- The posting routes for GitHub, GitLab and Jira are marked "unproved" in `help ticket-summary-post`.
- A search of the CLI's Python source for these topic names and texts found nothing: the cards alone carry these duties.

## Open for a grill

- What "encode" covers: closing the differences in the cards, or also having the CLI track and remind each duty.
- The first line of the request stops at "giving briefly": what is given.
- When the first message goes out.
- The Release driver finds the delivered tickets (point 4) and the Chief of Staff does the actions (last line): read here as the driver listing, the Chief of Staff showing and posting.

## Related items

- `2-backlog/P4/tracker-import`: tickets come into the inbox by a setting, per tracker.
