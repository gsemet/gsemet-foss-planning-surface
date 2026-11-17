## Summary

The board's Configuration page lists each role with the agent and model to run it, but not what the role does, so a user setting a model had to know the roles by heart. Each role now shows, in grey under its name, the one-line description its agent file already carries. No text is written for the board: the agent files stay the single source.

## Deliverables

Under each role name of both host tables (Claude Code and Copilot), the role's description appears in small grey text, without the "Prompt starts with" sentence that agent files end with. For example, the Coder row shows "Implements one round of one chantier CR in its worktree; never commits. Started by a Driver."

```text
role (td.role)
  coder
  Implements one round of one chantier CR in its worktree; never commits. Started by a Driver.   <- new, grey, wraps at 360px
```

- **UNVERIFIED:** no screenshot of the page at the head yet.
- The configuration view's role rows gain a `description` field (the text, or `null` when the agent file gives none); the page shows it escaped, and omits the line when it is `null`.
- The text is not translated and is the agent file's English wording.

## Blast radius

Grade: **1**. A read-only addition to the configuration view and one CSS rule; the write route and the written file are unchanged. A plain `git revert` restores the previous page.

## Autonomous decisions

- The `description` field is added where each host's rows are built (`_host`) rather than inside `_row`, because `_row` already has as many arguments as the linter allows; the field is still in every view the module builds.

## Known gaps

- **UNVERIFIED:** no screenshot of the page from a real browser at this head; the Configuration page's look is not proven, only the data it shows.

<details>
<summary>Details</summary>

## Changes

- `plugin_files.py`: new `plugin_role_descriptions(host)` reads each agent file's frontmatter `description` (YAML, so quoting is undone) and cuts it before `Prompt starts with:`; a file with no frontmatter, no description, or one that does not parse gives no entry.
- `playbook/edit.py`: each host's role rows carry `description`, in the `GET` answer and in the `view` of a `PUT` answer.
- `board/web/js/views/config.js` and `css/views/config.css`: the role cell shows the description in grey, small, normal weight, bounded to 360px and wrapping.
- `tests/test_board_config.py`: an existing test asserts the Coder's description on both hosts, no "Prompt starts with" in any, and one per role; a case with no description answers `null`.

## Human decisions

- The description shown is the `description` line of the role's agent file, in grey under the role's name; nothing is written for the board.

## Impacts

Users see what each role does on the Configuration page; nothing else changes.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Local gates at `5041a0c`: `just check` (443 passed, run before the commit)
- [ ] Evidence: none yet, no screenshot of the page (see Known gaps)
- [x] Review: approved at `5041a0c`
- [x] Verified at `5041a0c`
- [x] CI green at `5041a0c`

## Internal references

- CR-325 board-config-role-descriptions

</details>
