## Summary

Users do not know what chantier can do, and a release asks for approval at every irreversible step. This change makes the assistant session that talks to the user show two things at the right moments, without noise:

- During a release, it offers "auto": say the word and this release merges its version PR, tags and publishes without asking. Announcement posts stay drafts for the user.
- Tips are limited to four key moments (first use, after a status, end of a batch, during a release): one short line, at most once per moment and per session. "plus de conseils" turns them off for the session.

## Deliverables

Documentation cards only; no CLI code changes (the existing `order grant` and `release go` mechanics are reused).

| Before | After |
| --- | --- |
| One or two tips at "the end of a piece of work, a report, a quiet turn" | One 💡 line at four moments, once per moment and session, off on "plus de conseils" |
| Every irreversible release action waits for approval unless a grant was set at the start | The user can say "auto" mid-release: the assistant reads the published count, asks for a budget if none, runs `order grant <release> --note "releases=<k+1>"` |

What "auto" covers: merging the version PR, the tag, every publication step of the project's procedure, for this release only. It never covers posting an announcement, starting or merging a fix, the `order confirm` word or a budget raise. The "auto" answer also appears in a release approval question, which is not a tip and stays after tips are off.

## Blast radius

Grade: 1

Only instruction cards change; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- No prior investigation was needed: the touched files are known.
- The open questions took their recommended answers, which the user may change in review.

<details>
<summary>Details</summary>

## Changes

- The assistant's card: Releases (the offer, the approval-question answer, the five steps on "auto", its scope), an entry-points row, and the Tips rule replaced by the four-moment rule with examples per moment.
- `status-layout.md`: the Tips section states the same rule.
- `driver.md`: one sentence on `release go` under a grant and the announcement staying a draft.
- `session-start.md` and `init.md`: the introduction's and the tour's closing lines count as the first-use tip.

## Human decisions

- "auto" covers merge of the version PR, the tag and the publication of the release, without asking; announcements stay drafts for the user.
- Tips: one per key moment per session, as one short line; "plus de conseils" turns them off.
- "auto" is listed as an answer in the approval question; with no batch budget, a budget is asked first; tips exist only at the four moments; "auto" covers every publication step of a procedure, never an announcement post.

## Impacts

No visual change; the assistant's wording and prompts change.

## Test plan

- [x] New or changed tests (they fail on the previous code) <!-- No behaviour change in the CLI; cards only -->
- [x] Local gates: `just check` passes; `just scenario` passes
- [x] Evidence: the diff read against the specification
- [x] Review
- [x] CI green

## Internal references

- CR-166 "release auto and contextual tips", batch-09.

</details>




