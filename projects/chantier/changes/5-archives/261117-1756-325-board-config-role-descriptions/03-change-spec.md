---
type: change-spec
description: The web board's Configuration page shows each role's description, read from its agent file.
---

# Change Specification: role descriptions on the board's Configuration page

Origin: verbal, the user's board feedback of 2026-11-17 (`intake/request.md`). No issue.

## Goal

On the web board's Configuration page, each role of each host's table shows what the role does,
so the user knows which role they are setting an agent or a model for. The text is the
`description` line the role's agent file already holds, shown in grey under the role's name. One
source, already kept up to date: no text is written for the board.

## Decisions carried from `02-answers.md`

- scope-Q1: this CR is one of four cut from the board feedback of 2026-11-17
  (board-picker-surface-item, board-batch-navigator, board-kanban-priority-colours,
  board-config-role-descriptions), all for the next batch. This CR covers the role descriptions
  only.
- config-Q6: the description each role shows is the `description` line of the role's agent file,
  for example the Coder's "Implements one round of one chantier CR in its worktree; never commits.
  Started by a Driver.", in grey under the role's name.

## What changes

### Where the text comes from (CLI, `skills/chantier/scripts/cli/src/chantier/plugin_files.py`)

- Each host's agent files are already found by `_agent_files(host)` (`agents/*.md` for `claude`,
  `com.github.copilot/agents/*.md` for `copilot`), and `plugin_roles(host)` derives the role names
  from them. Add one role-free function beside them, for example
  `plugin_role_descriptions(host) -> dict[str, str]`: for each agent file of the host, the role
  (named as `plugin_roles` names it) mapped to the shown description.
- The description is the `description` value of the file's YAML frontmatter (the block matched by
  the existing `FRONTMATTER` pattern), read with `ruamel.yaml` (already a dependency), so YAML
  quoting is undone (`''` becomes `'`). `ruamel` is imported inside the new function, as
  `playbook/yaml_subset.py`'s `_events` does: `pyproject.toml` bans a module-level `ruamel` import
  (`banned-module-level-imports`), and `plugin_files.py` is imported by most commands.
- The shown text is that value cut before its `Prompt starts with:` sentence, trimmed, as the
  user's example shows: "Implements one round of one chantier CR in its worktree; never commits.
  Started by a Driver." Every agent file of both hosts holds that sentence last today; a
  description without it is shown whole.
- A file with no frontmatter, no `description`, or one that does not parse gives no description
  for that role (no entry); nothing is invented and no error is raised. `agent_problems` is not
  changed.
- The CLI knows no role: the function reads whatever agent files the plugin installs, as
  `plugin_roles` does.

### The configuration view (`skills/chantier/scripts/cli/src/chantier/playbook/edit.py`)

- `_host` reads the host's descriptions once and `_row` adds one field to each role's row:
  `"description": <the shown text>` or `null` when the role's file gives none. The field is in
  every view this module builds, so in both the `GET .../config` answer and the `view` of a `PUT`
  answer (dry run or write) of `board/config_api.py`, which needs no change.
- The Claude Code table reads `agents/`, the Copilot table reads `com.github.copilot/agents/`;
  their descriptions are identical today (AGENTS.md keeps the two hosts' agent files alike), and
  each table shows its own host's file.

### The page (`skills/chantier/scripts/cli/src/chantier/board/web/js/views/config.js`)

- `roleRow` renders, in the role cell (`td.role`), the role's name and, under it when
  `row.description` is set, `<div class="desc">${row.description}</div>`. With no description, the
  cell shows the name alone, as today.
- The text goes through the `html` template of `core/dom.js`, as every other value of the view, so
  it is escaped.
- The description is the agent file's English text, not translated: no new key in
  `js/i18n/*.js`.

### The style (`skills/chantier/scripts/cli/src/chantier/board/web/css/views/config.css`)

- `.config .role .desc`: grey and small, as the page's other secondary lines (`color:
  var(--ink3); font-size: var(--text-small);`), normal weight (the role cell is `font-weight:
  500`), with a little space above it, and a bounded width (for example `max-width: 360px`) so the
  role column does not push the agent and model columns off a narrow screen; it wraps.

### What does not change

- No agent file and no card changes: the descriptions are used as they are.
- The `PUT` route, its checks, the journal line and the written file are unchanged; the board
  still edits only `agent` and `model`.
- The Timing tab and the read-only "others" table are unchanged.

## Out of scope

- The three other CRs of the same feedback (picker, batch navigator, kanban colours).
- Any text written for the board, a tooltip, a translation of the descriptions, or descriptions
  anywhere else on the board.
- Editing a description from the board.
- The CR board pane (`hooks/register.tsx`): not touched, so AGENTS.md's pane screenshot rule does
  not apply.

## Evidence

- `skills/chantier/scripts/cli/tests/test_board_config.py`: extend an existing test (no new test
  function, to keep `just test` fast) to assert, on the `GET` view, that the Claude `coder` row's
  `description` is "Implements one round of one chantier CR in its worktree; never commits.
  Started by a Driver.", that the Copilot `coder` row holds the same text, that no row's
  description contains `Prompt starts with`, and that every role of both hosts has a non-empty
  description (all shipped agent files have one). Read the expected Coder text from
  `agents/coder.md` rather than hard-coding it only if the test helpers already reach the plugin's
  files; otherwise the literal above holds.
- Add one case where an agent file has no `description` (a temporary plugin root with
  `CHANTIER_PLUGIN_ROOT`, or a parametrized case of a unit test of the new function) and the row's
  `description` is `null`; the view still answers 200.
- `just check` passes (lint, Biome on the JS and CSS, tests, release notes).
- The change touches the CLI, so the pipeline's `just scenario (ubuntu-latest)` job is green at the
  PR's head, per AGENTS.md.
- A look at the page: `$CHANTIER board`, open Configuration, Models tab: under each role name of
  both host tables, the grey description, without the "Prompt starts with" sentence; a narrow
  window keeps the table readable (it scrolls inside `.scroll` as today). The PR's Deliverables
  carry one screenshot of the Configuration page at the head.

## Open questions

None. The cut before `Prompt starts with:` follows the user's own example in `02-answers.md`.
