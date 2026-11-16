<!-- Title: docs: post multi-line forge texts from a file written with the Write tool -->

## Summary

An agent that built a pull request body inside a shell string got a form-feed character in the description: PowerShell reads a backtick as an escape, and Markdown is full of backticks. Two description checks failed before the body was posted again from a file. The cards showed the file form only as an example, and for GitLab they showed only the unsafe form (the text as a command argument).

The cards now state it as a rule every role reads: a multi-line text sent to the forge is written to a file with the host's Write tool and the forge command takes it from that file.

## Deliverables

The rule, added once to the shared rules (rule 9, "Commands and files"), directly after the no-BOM sentence:

> A multi-line text sent to the forge (a PR or MR body, a PR, MR or issue comment, release notes) is a file written with the host's Write tool (Edit to change it) ... and the forge command takes it from that file (`--body-file`, `--notes-file`, or the forge CLI's equivalent). Its text is never typed, built or escaped in a shell command, in any shell, and the file is never written by the shell ...

| Where | Before | After |
| --- | --- | --- |
| Driver card, Push bullet | GitLab: `glab mr update --description`, body as an argument | always from `pr-body.md`; GitLab uses `glab`'s option that reads the description from a file, marked unproved with its trial |
| Driver card, stack and release bullets | `glab mr update --description` | point to the Push bullet's file form (the release bullet also to rule 9) |
| Chief of Staff card, "How to post" | `glab issue note <id> --message ...` | `glab issue note <id>` with the option that reads a file, marked unproved with its trial |

Choices: it covers every multi-line text sent to the forge, not only the PR body; one-line texts (a PR title, a note) and commit messages are not covered; any shell, not PowerShell only. No CLI refusal and no test enforce it.

## Blast radius

Grade: 1. Three Markdown cards change and no code does; a plain `git revert` restores the previous wording.

## Autonomous decisions

- The GitLab form is written generically ("`glab`'s option that reads the description from a file"), because `glab` is not installed where the work ran, so its flag could not be checked. It is marked unproved, with the trial that settles it.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/concepts.md`: rule 9 holds the new rule.
- `skills/chantier/references/driver.md`: the Push, stack and release bullets use the file form and point to rule 9.
- `skills/chantier/references/chief-of-staff.md`: the one `glab` example reads a file.

## Human decisions

- The rule covers every multi-line text sent to the forge (bodies, comments, release notes), not only the PR body.
- One-line texts with no Markdown and commit messages stay out of scope.
- The file is written with the host's Write tool, never by the shell, in any shell.
- GitLab follows the same rule; its exact `glab` form is marked unproved until a trial.
- The rule lives once, in the shared rules, and is not enforced by the CLI or a test.

## Impacts

No visual change. Agents posting a PR body, a comment or release notes are told to write the file first.

## Test plan

- [x] New or changed tests: No behaviour change
- [x] Local gates at `94c27be`: `just check` (50 passed), `just scenario` carried from `aa74650`: patch unchanged; the long gate runs once at the top of the stack, PR 152 (GitHub and GitLab, 586/586 each at `aa74650`)
- [x] Evidence: text checks of the new rule and of the forge examples at `94c27be`
- [x] Review: approved at `94c27be` (after a move review of the restack)
- [x] Verified at `94c27be`
- [x] CI green at `94c27be`

## Internal references

- CR-207 pr-body-from-file-only

</details>
