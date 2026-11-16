## Summary

The retro that chantier leaves after a batch offered every point as an inbox item of the project the batch ran in, even when the cause was in chantier's own cards, CLI, agents or host use. Those points then sat in a backlog that cannot fix them. Each retro point now carries a tag, `project` or `chantier`: project points stay inbox items, chantier points are offered as a GitHub issue on chantier's repository (a draft the user posts, or lets the Chief of Staff post on their yes), never filed in the project's backlog.

## Deliverables

A retro line becomes `- [<tag>] <problem>: <long-term fix>`, and the Completion report numbers the points in one sequence across both tags. A problem with a cause on both sides is written as two lines, one per tag. Worked example, written by hand from the cards (no issue is posted anywhere for it):

Sample retro section (lines 1 and 2 are one problem split in two):

```
- [project] The integration suite takes 14 minutes and the gate timed out twice: split the slow tests into a nightly job.
- [chantier] The same gate timeout left a Driver waiting with no rule to hand back: the Driver card should tell it to hand back before waiting on a gate longer than 10 minutes.
- [project] A rebase conflict on the lockfile cost a round: regenerate the lockfile in CI instead of committing it.
- [chantier] The Foreman could not tell a live session from a stale one: `chantier status` lacks a line naming the last live session per CR.
```

Completion report lines it yields:

```
Retro
1. [project] The integration suite takes 14 minutes ...
2. [chantier] The same gate timeout left a Driver waiting ...
3. [project] A rebase conflict on the lockfile cost a round ...
4. [chantier] The Foreman could not tell a live session from a stale one ...

For you
- Project points to file as inbox items: 1, 3.
- chantier points to draft as an issue on chantier's GitHub repository: 2, 4.
```

Draft issue file for point 2 (checked against the public-repository list: no project name, path, CR or batch id):

```
Bug: the Driver card has no rule to hand back before a long gate wait

What happened: a gate timed out after a long run and a Driver kept waiting on it with no rule telling it to hand back, which cost a round.
Long-term fix proposed: the Driver card tells it to hand back before a gate wait over 10 minutes.
chantier version: 0.9.0. Host: Claude Code (version not known).
This came from a batch retro.
```

When the project is chantier itself (its `origin` equals the plugin manifest's `repository`, `https://github.com/gsemet/chantier`, checked in this repository), the report says so in one line and the inbox is the default route for chantier points, an issue on the user's word.

## Blast radius

Grade: **1**. Cards and one doc page only; no code. A plain `git revert` restores the previous retro.

## Autonomous decisions

- The specification's open points took their defaults: `[project]`/`[chantier]` head tags; inbox as the default route when the project is chantier; drafts in `4-batch/chantier-issue-<n>.md`, deleted by `close`, the posted link said in the chat only; `Bug:`/`Feature:` titles, no label; host problems tagged `chantier`; duplicate check on open issues only.

## Known gaps

- No issue was posted on chantier's repository: the draft and posting steps are proven by reading the cards (worked example above), not by a live `gh issue create`.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/foreman.md`: the retro line format, the two tags, the two-lines rule, the offer by route.
- `skills/chantier/references/chief-of-staff.md`: the pause split into the project route and the chantier route (repository from the manifest, duplicate check, draft, public-repository check, show and ask per issue, post on the yes only, no record); the "project is chantier itself" case; direct-mode pause and release paragraph aligned.
- `skills/chantier/references/status-layout.md`: Completion report Retro and "For you" by tag.
- `skills/chantier/references/concepts.md`: the Paused item of the batch lifecycle.
- `skills/chantier/references/driver.md`: the release's `work/retro.md` uses the same format.
- `docs/use-cases-foreman.md`: the retro sentence.

## Human decisions

- Retro points about the target project stay inbox items; points about chantier's own way of working go through a feature request or bug report on GitHub; posting an issue stays the user's yes, per point.

## Impacts

No visual change. A batch's Completion report shows tagged retro points and offers two routes.

## Test plan

- [x] No behaviour change in code (cards and docs only)
- [x] Local gates at `0778400`: `just check` pass, `just scenario` pass (github 695/695, gitlab 676/676)
- [x] Evidence at `0778400`: worked example above, written from the cards; origin equals the manifest `repository` (`https://github.com/gsemet/chantier`)
- [x] Review: approved at `4c0c6d7` (the move onto main), carried from `4c0c6d7` over a clean rebase to `0778400`
- [x] Verified at `0778400`
- [x] CI at `0778400`: `gh pr checks 167`: just check (ubuntu, macos, windows), just scenario (ubuntu) and just eval-dry-run all pass

## Internal references

- CR-231 retro-target-vs-chantier; worked example file `work/e4-example.md`.

</details>
