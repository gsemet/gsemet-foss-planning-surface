## Summary

The CR Driver and the stack driver, on Claude Code, could write a file with Write but had no Edit tool. A Driver that needed to change one line of its PR description had to rewrite the whole `pr-body.md`. Both agents now get Edit, as the Release driver already has, and the Driver card no longer says the body is "always written with the Write tool".

## Deliverables

Before and after, the `tools:` line of both agent files:

```diff
-tools: Agent, Bash, PowerShell, Read, Write, Grep, Glob, SendMessage, Monitor
+tools: Agent, Bash, PowerShell, Read, Edit, Write, Grep, Glob, SendMessage, Monitor
```

The card's sentence (Push bullet of `skills/chantier/references/driver.md`) now says the body is a file written with Write, changed with Edit and posted from that file, never as text in the command.

The write guard needs no change: `hooks/register.tsx` already judges `Edit` on `file_path` as it does `Write`, so a CR Driver's Edit stays inside its `writes:` folders. The existing cases in `hooks/register.test.tsx` (the loops over `['Write', 'Edit', 'NotebookEdit']`) pass in `just check` and prove an Edit outside those folders is refused.

## Blast radius

Grade: **1**. Two tool names in agent frontmatter and one sentence of a card; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- No Copilot change: its `edit` tool covers writing and editing a file, and both Driver agents there already list it, so the agent bodies stay identical across hosts.
- The QA driver and the other roles that have Write but no Edit are left out: the request names only the CR Driver and the stack driver.
- No new test: the frontmatter is read by the host, and the guard's Edit cases already exist.

## Known gaps

- No real use of Edit by a Driver is shown in this PR: its own Driver runs the agent file from before the merge. It can only be seen on a Driver started after this lands (or after `/reload-plugins`).

<details>
<summary>Details</summary>

## Changes

- `agents/cr-driver.md` and `agents/stack-driver.md`: `Edit` added to the `tools:` line, after `Read`.
- `skills/chantier/references/driver.md`: the Push bullet's sentence on the body, reworded.
- Not changed: `hooks/`, the CLI, the Copilot agent files, the version.

## Human decisions

- The Drivers get their editing tools, so they can change part of a file instead of rewriting it.
- The scope is the request as filed (the CR Driver and the stack driver); other roles can be offered separately.

## Impacts

No visual change. A Driver on Claude Code can change part of a file with Edit instead of rewriting it; the stack driver is not guarded, so its Edit is unguarded as its Write already is.

## Test plan

- [x] New or changed tests (they fail on the previous code): No behaviour change; the guard's existing Edit cases cover the refusal
- [x] Local gates at `82f6941`: `just check` and `just scenario` pass (GitHub 677/677, GitLab 658/658 checks)
- [x] Evidence: none, no visible change
- [x] Review: approved at `82f6941`
- [x] Verified at `82f6941`
- [x] CI green at `82f6941`: all five checks pass

## Internal references

CR-229 driver-edit-tool (specification `03-change-spec.md` in the CR's folder), from the retro of the previous batch.

</details>
