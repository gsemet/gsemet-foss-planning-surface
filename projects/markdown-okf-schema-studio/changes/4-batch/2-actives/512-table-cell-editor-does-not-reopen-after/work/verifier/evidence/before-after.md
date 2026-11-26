# CR-512 before and after

- Before (base): `9d7e788a479dec70fd882d295bf0d5e78f4f6b98`
- After (head): `54d1da6268e9a4fbe059c6cdb8b1160d94b4b558`

## No visible change, so no before/after pair

`git diff --name-only 9d7e788a 54d1da62 -- src sphinx skills CHANGELOG.md docs/releases-notes
package.json` (from the worktree) prints nothing. The change holds a real-window test, the stress
list, the script and notes of one demo clip, one guideline sentence and requirement bookkeeping.
The clip's output files and frames are unchanged. The product looks and behaves the same on both
commits, so a pair would show two identical screens. The pull request states "No visual change: no
product code changes", with its reason.

## After-only image (proof of one matrix cell, not a comparison)

| File | Shows | Commit |
| --- | --- | --- |
| `after-autosave200-header-editor-open-4.26s.jpg` | Real VS Code window, frame at 4.26 s of a clip take (paste at 3.81 s, Done click at 4.43 s): the table has the columns Task, Owner, Due, and the cell editor is open in the header cell "Task" ("Header, column 1 of 3", Done and Cancel). The take's profile has `files.autoSave: afterDelay`, delay 200 ms. The title bar shows the file and workspace names only: no user name, no home folder. | `e76c084`, carried to `54d1da6`: the product code, the clip kit, the scenario, its stage and the lock file are identical at both commits |

Reproduce, from the worktree in Git Bash, with no other test or clip VS Code instance running
(`<scratch>` is any short empty folder of the worktree's `out/`, `<Code.exe>` a VS Code 1.147.0 or
1.148.0 executable; this take used 1.148.0 from the worktree's `.vscode-test`):

```sh
fnm exec -- just package
env CLIP_SCRATCH=<scratch> DEMO_CODE=<Code.exe> fnm exec -- just clip paste-spreadsheet-cells setup --vsix out/reports/package/markdown-okf-schema-studio.vsix
env CLIP_SCRATCH=<scratch> DEMO_CODE=<Code.exe> fnm exec -- just clip paste-spreadsheet-cells take
```

The take's records are `../head-clip-take-verify.json` and `../head-clip-take-events.json`.
