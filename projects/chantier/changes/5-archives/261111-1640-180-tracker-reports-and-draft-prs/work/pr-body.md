## Summary

When a change request comes from an issue in the project's tracker, the issue's readers had no
way to hear what happened to it. The cards now tell the agents how to report back: a short
comment once the request is understood, the pull request linked on the issue through the forge's
own closing keyword, the issue closed by the merge, and "Released in <link>" once a release ships
it. Nothing is tied to one tracker, the project's own rules rank above it, and a change request
with no issue skips all of it. Only the planning agent that talks with the user posts, and only text the user approved.

Closes #101

## Deliverables

The `issue:` line travels from the request to the pull request:

| Step | Guidance file | What it does |
| --- | --- | --- |
| Filing / grill | planning and grilling guides | writes `issue: <link>` under the title of `01-intent.md` |
| Specification | specification guide | copies the line under the title of `03-change-spec.md` |
| Pull request | PR template and delivery guide | ends the Summary with `Closes <reference>` (or `Issue: <link>` for a tracker the forge does not know) |
| After the grill | planning guide | shows the user a text-only comment, posts it on the user's yes |
| After a release | planning guide | lists the shipped issues, one yes, "Released in <link>" on each |

Choices: the line sits under the title, never as front matter (the CLI reads the title from the
first non-empty line); no "PR opened" comment (the closing keyword already shows it); no agent
closes or reopens an issue by hand; a comment names no change request, batch, agent or cost.

## Blast radius

Cards only; a plain `git revert` restores the previous behaviour.

Grade: 1

## Autonomous decisions

None

<details>
<summary>Details</summary>

## Changes

- `concepts.md`: the "Tracker issue" word and who may post on an issue.
- `chief-of-staff.md` (the planning guide): record `issue:`, "Tracker comments", the "Released in" list, two "Never" lines.
- `griller.md`: record `issue:`, write the proposed comment for the planning agent, never post.
- `spec-writer.md`: carry the `issue:` line into the specification.
- `pr-template.md`: the closing line in the Summary, template comment, precedence and a ninth audit line.
- `driver.md`: the body carries the closing line; the delivery agent never comments on, closes or reopens an issue.

## Human decisions

- The merge closes the issue through the pull request's closing line; no agent does it by hand.
- The grill comment is text only and is posted only on the user's yes; there is no "PR opened" comment.
- One yes from the user covers the whole "Released in" list; "auto" never covers these comments.
- Where the posting agent's CLI does not reach the tracker, the user gets the text to post.

## Impacts

No visual change. Projects with issues get comments and closing lines; others are unaffected.

## Test plan

- [x] New or changed tests: No behaviour change (cards only)
- [x] Local gates at `9cb4cc7`: `just check` and `just scenario` passed (github 480/480, gitlab 480/480)
- [x] Evidence: the specification's greps, diff stat and read-through at `9cb4cc7`
- [x] Review: approved at `24cc7eb` (worktree; carried over a rebase to `9cb4cc7`, patch unchanged)
- [x] Verified at `9cb4cc7`
- [x] CI green at `9cb4cc7`

## Internal references

- CR-180 tracker-reports-and-draft-prs

</details>




