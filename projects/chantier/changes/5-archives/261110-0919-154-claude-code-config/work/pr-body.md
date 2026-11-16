## Summary

Running chantier on Claude Code meant many auto-mode refusals of routine commands (pushes after a rebase, `chantier.py` calls, PR creation) and errors caused by the agents' own habits (long chained commands, writes to unread files, leading assignments). chantier now says what to configure, checks it at start, and gives the exact JSON block to add. It never writes the user's settings.

## Deliverables

The preflight gains a non-failing line next to its other host checks:

```text
P5  ok    chantier <v>, uv and git found
P10 warn  19 of 19 recommended allow rules not found as written in your settings (...): <rule>, ...
```

| Area | Before | After |
| --- | --- | --- |
| Host reference (Claude Code) | tools, heartbeat, short compaction note | adds "Configuration" (prerequisites, allow rules with their risk and mark, what stays refused, auto mode, what the docs do not say), rewritten "Compacting", and an "Allow rules to add" block |
| Command hygiene | per host | one host-neutral rule for every agent (one command per call, read before overwrite, no leading assignment, `git -C` accepted) |
| Preflight | P5 checks `uv` | P5 checks `uv` and `git`; P10 warns on missing allow rules (Claude Code only) |

## Changes

- Host references: new "Configuration" sections (Claude Code, Copilot), rewritten "Compacting", new "Allow rules to add" block. Each claim is marked proved, documented or unproved.
- Shared rules: `git -C <worktree>` accepted; new rule 9 "Commands and files".
- CLI: `RECOMMENDED_ALLOW`, a settings reader (home, project, local), P5 with `git`, P10 and a `warn` state. It reads only, never fails the exit code.
- Chief of Staff card and `init` tour: run the check at the first turn and give the block for missing rules.
- Tests, scenario and tutorial: a test compares the JSON block with the CLI list; P10 tests; two scenario checks; tutorial section 5 updated.

## Impacts

No visual change. Evidence: preflight on Windows prints `P10 warn 19 of 19 ...` and the exit code is the same with and without the P10 line (checked against the Copilot host). Users on Claude Code see a `P10` line at preflight and receive a block to paste; a missing rule never blocks a batch.

## Blast radius

Grade: 1. Documentation plus one added, non-failing preflight line. A plain `git revert` restores the previous behaviour; the only failing addition is a missing `git`, which every batch needs.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates: `just check` (34 passed), `just scenario` (350/350 on GitHub and GitLab)
- [x] Evidence: preflight output at the pushed head with the real settings
- [x] Review
- [x] CI green

## Autonomous decisions

- Each rule's Bash form is followed by its PowerShell form, then `SendMessage`, in the list and the JSON block.
- On POSIX, P10 compares only the Bash rules and `SendMessage`.
- Added an "unproved" bullet: whether a running session picks up a settings change.

## Internal references

CR-154 claude-code-config, batch-09.

Evidence files (not uploaded): work/verifier/evidence/preflight-claude.txt, preflight-copilot.txt, just-check.txt, links.txt.

