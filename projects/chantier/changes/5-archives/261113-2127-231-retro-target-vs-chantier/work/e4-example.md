# E4 worked example (hand-written from the cards; nothing posted)

## Sample `4-batch/retro.md` section (four lines)

```
## 2026-11-13, CRs of this pause
- [project] The integration test suite takes 14 minutes and the gate timed out twice: split the slow tests into a nightly job.
- [chantier] The same gate timeout left a Driver waiting with no rule to hand back: the Driver card should tell it to hand back before waiting on a gate longer than 10 minutes.
- [project] A rebase conflict on the lockfile cost a round: regenerate the lockfile in CI instead of committing it.
- [chantier] The Foreman could not tell a live session from a stale one: `chantier status` lacks a line naming the last live session per CR.
```

(Lines 1 and 2 are one real problem with a cause on both sides, the long gate that timed out: two lines per the two-lines rule, each with its own fix; line 1 is the project's side, line 2 chantier's. Lines 3 and 4 are two other, separate problems, one per tag.)

## Completion report, Retro and For you

```
Retro
1. [project] The integration test suite takes 14 minutes and the gate timed out twice: split the slow tests into a nightly job.
2. [chantier] The same gate timeout left a Driver waiting with no rule to hand back: the Driver card should tell it to hand back before waiting on a gate longer than 10 minutes.
3. [project] A rebase conflict on the lockfile cost a round: regenerate the lockfile in CI instead of committing it.
4. [chantier] The Foreman could not tell a live session from a stale one: `chantier status` lacks a line naming the last live session per CR.

For you
- The batch is paused. Project points to file as inbox items: 1, 3.
- chantier points to draft as an issue on chantier's GitHub repository: 2, 4 (one issue each, or both in one if you prefer).
- Inbox ideas ready for a grill: <slugs>. Say "close the batch" when done; the Retro is offered before it.
```

(A point matching an open issue would read `... (already reported: <issue link>)`; none matches here.)

## Draft issue file for point 2: `4-batch/chantier-issue-2.md`

```
Bug: the Driver card has no rule to hand back before a long gate wait

What happened: during a batch, a gate timed out after a long run and a Driver kept waiting on it with no rule telling it to hand back, which cost a round.

Long-term fix proposed: the Driver card should tell the Driver to hand back before it waits on a gate longer than 10 minutes.

chantier version: 0.9.0. Host: Claude Code (version not known).

This came from a batch retro.
```

Check against step 4: no project name, no private path, no project code or text, no CR number, slug or batch id, no person's name. The
"integration test suite" detail of the project was left out (it belongs to point 1). Passes.

`4-batch/chantier-issue-2-body.md` holds the same text without the first line (the title); the post would be
`gh issue create --repo gsemet/chantier --title "Bug: the Driver card has no rule to hand back before a long gate wait" --body-file <path>`, run only on the user's yes.

## E5: remote against manifest, run in this repository

```
$ git remote get-url origin
https://github.com/gsemet/chantier
manifest repository (.claude-plugin/plugin.json):   https://github.com/gsemet/chantier
manifest repository (.github/plugin/plugin.json):   https://github.com/gsemet/chantier
```

Both compared without a trailing `.git` or `/`, ignoring case: they match, so this project is chantier itself and the "For you" line is:

> This project is chantier: its `chantier` points are filed here as inbox items, like the project's; say 'as an issue' for a point to go to GitHub instead.
