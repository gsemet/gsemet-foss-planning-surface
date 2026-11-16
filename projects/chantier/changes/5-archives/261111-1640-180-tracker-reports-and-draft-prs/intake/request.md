# Report back on tracker issues, and keep a PR a draft until it is mergeable

Source: https://github.com/gsemet/chantier/issues/101

## What

Five process rules a project adopted for its change requests. They are generic and should live in
Chantier's cards.

When a CR comes from a tracker issue (GitHub, GitLab, Jira):

1. **Grill comment.** When the grill ends and the CR opens, the Chief of Staff posts a short
   comment on the issue: what was understood, the scope in two to five bullets, what is left out,
   and "the pull request will be linked here". A Markdown plan and an HTML demo go with it when the
   tracker allows attachments.
2. **Links both ways.** The CR records the issue as an `issue: <link>` line in the `01-intent.md`
   front matter, carried into `03-change-spec.md` and the PR body. The PR body uses the tracker's
   closing keyword (`Fixes #N`, `Closes #N`, the Jira key). When the PR opens, the issue gets a
   one-line comment with the PR link.
3. **Transition.** The issue closes through the closing keyword on merge, never by hand.
4. **Release.** Once a release is published, each issue it ships gets "Released in <release
   notes link>".

For every CR:

5. **Draft until mergeable.** A PR opened before it is mergeable is a draft. It turns ready for
   review only when the owner can merge it: CI green at its head, review done, CR handed back
   `ready`. In a stack, each PR turns ready on its own as soon as it is mergeable, without waiting
   for the rest of the stack; it goes back to draft if its CR returns to a Driver.

Who and approval: only the Chief of Staff posts on an issue (never a Driver, the Foreman or a
griller), and only text the user approved. At a release, one approval covers the whole list of
"Released in" comments. An item with no issue skips these steps.

## Where it would go

- `skills/chantier/references/concepts.md`: the words "tracker issue" and "ready to merge"; the
  rule that only the Chief of Staff posts on an issue.
- `chief-of-staff.md`: `issue:` at the grill; a "Tracker comments" paragraph (grill comment, PR
  link comment); in "Releases", the "Released in" list; in "Never", posting without approval and
  closing an issue by hand. This replaces the planning item `tracker-grill-summary`.
- `driver.md`: the PR body carries the closing keyword; a Driver never comments on or closes an
  issue; the stack driver's "on another base, a draft" becomes "each PR turns ready on its own";
  the release driver's hand-back lists the issues the release closed.
- `foreman.md`: the asks `ready` and `released` carry the CR's `issue:` link.
- `pr-template.md`: the closing keyword line when the CR has an `issue:`.
- `griller.md` and `spec-writer.md`: carry the `issue:` line; the griller never posts on an issue.

Keep it generic: name the tracker's closing keyword, and the `gh` / `glab` command only where a
card already does.

## Dependent PR outside a stack

A PR based on another CR's branch outside a stack (an `after` dependency, no stack driver) stays a
draft until it is rebased onto the default branch, as today: merging it would land in the
dependency's branch. "Ready on its own" applies to stacks only.

