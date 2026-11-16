## Summary

On Windows, the plugin's write guard refused a write to a path in the Git Bash drive form (`/c/Users/...`) even when it sat inside an allowed folder written as `C:/Users/...`: it compared the two spellings as different paths. The guard now reads a Git Bash drive path as its drive form before it judges, so an agent may write anywhere inside its folders whatever the form of the path.

## Deliverables

The mapping, as the guard applies it (`hooks/register.tsx`):

| Path an agent writes | Folder in its `writes:` line | Before | After |
| --- | --- | --- | --- |
| `/c/Work/notes/a.md` | `C:\Work\notes` | refused | passes |
| `/C/work/notes/a.md` (letter and folder case) | `C:\Work\notes` | refused | passes |
| `C:/Work/repo/a.py` | `/c/Work/repo` | refused | passes |
| `/d/Work/notes/a.md` | `C:\Work\notes` | refused | refused (other drive) |
| `/c/work/repo/a.py` | `/work/repo` (POSIX) | refused | refused (no drive form on either side: unchanged) |

The same rule covers Write, Edit, NotebookEdit and the shell targets of Bash and PowerShell. Refusal messages are unchanged and still quote the path as written. The board pane's use of `isInside` is untouched.

## Blast radius

Grade: 1. A guard-only helper in the hooks; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The mapping applies only when one side of the compare is in drive form, so on Linux and macOS `/c/x` stays a real POSIX path.

## Known gaps

- No release-notes entry is written in this PR: the project builds release notes from the git log at release time.
- The new sentence in the host reference card is one long line in a hard-wrapped paragraph (cosmetic, accepted).
- The folders are mapped on each guarded call rather than once per spawn (harmless).

<details>
<summary>Details</summary>

## Changes

- `hooks/register.tsx`: `fromGitBash` and `guardInside`, used by both guard branches of the `tool.call` handler.
- `hooks/register.test.tsx`: cases for the Git Bash form on Write, Edit, NotebookEdit and the shell, a folder given in the Git Bash form, and an unchanged POSIX agent.
- `skills/chantier/references/hosts/claude-code.md`: one sentence in "The write guard".

## Impacts

No visual change. WSL (`/mnt/c`), Cygwin (`/cygdrive/c`) and UNC forms are not mapped.

## Test plan

- [x] New or changed tests (two of the three fail on the previous code, checked at 8c6964d)
- [x] Local gates at 8c6964d: `just mod` (62 tests, 3 new) and `just check` pass
- [x] Evidence: the mod's tests at 8c6964d
- [x] Review: approved at 8c6964d (reviewed state 842b800 plus the commit)
- [x] Verified at 8c6964d
- [x] CI green at 8c6964d (gh pr checks 234: 5 of 5 pass)

## Internal references

- CR-286 "Change Specification: the write guard reads Git Bash paths", batch-18.

</details>
