# CR-513 before and after

- Before: base `9d7e788a479dec70fd882d295bf0d5e78f4f6b98` (source of the base; the head's tests and
  fixtures copied over it, so both sides render the same documents).
- After: head `1fa9587eb1f6a5e53ef5bce5269d292bc2517859`.
- `<W>` = the CR worktree at the head, `<B>` = a detached worktree of the base (removed at the end),
  `<S>` = the CR folder's `work/scratch`, `<E>` = this folder.
- All documents are made up. Every image was opened: none shows a username or a home folder path.

## Visual scenarios (rendered page of the visual harness, 900 px)

Reproduce, in `<B>` (after `just dev`) and in `<W>`:
`fnm exec -- npm.cmd run visual:render`, then
`uv run --no-sync --group docs python test/visual/capture.py --group frontmatter-schema`.

| Before | After | Shows |
| --- | --- | --- |
| before-v32-field-issue-rows-light-900.png | after-v32-field-issue-rows-light-900.png | `status` (error) and `bonus_field` (warning): plain rows, then coloured name and wavy underline, light |
| before-v33-field-issue-rows-dark-900.png | after-v33-field-issue-rows-dark-900.png | the same, dark |
| before-v34-schema-warning-row-light-900.png | after-v34-schema-warning-row-light-900.png | "Schema could not be parsed" row: plain, then warning colour on a light background across the table, light |
| before-v35-schema-warning-row-dark-900.png | after-v35-schema-warning-row-dark-900.png | the same, dark |

The harness themes set none of the four severity tokens, so these pictures show the fallback colours.

## Edit mode (same rendered pages, driven with Playwright)

Reproduce: `uv run --no-sync --group docs python <S>/ver_edit_probe.py <W> <B> <E>`.

| Before | After | Shows |
| --- | --- | --- |
| before-edit-hover-error-name-{light,dark}.png | after-edit-hover-error-name-{light,dark}.png | pointer over the error name cell: hover background, the name keeps the error colour |
| before-edit-hover-warning-name-{light,dark}.png | after-edit-hover-warning-name-{light,dark}.png | the same for the warning name cell |
| before-edit-open-error-value-{light,dark}.png | after-edit-open-error-value-{light,dark}.png | open editor on the error value: no wavy underline on the editor or its menu |
| before-edit-open-warning-value-{light,dark}.png | after-edit-open-warning-value-{light,dark}.png | the same on the warning value |

## Narrow page, 360 px

Reproduce: `uv run --no-sync --group docs python <S>/ver_wrap_probe.py <W> <B> <E>`.

| Before | After | Shows |
| --- | --- | --- |
| before-wrap-360-v34-light.png | after-wrap-360-v34-light.png | the whole-table warning message wraps (3 lines) inside the table; coloured after |
| before-wrap-360-v35-dark.png | after-wrap-360-v35-dark.png | the same, dark |

## After only

- `after-tokens-set-{v32-light,v33-dark,v34-light,v35-dark}.png`: the four `--vscode-*` severity
  variables set on the page root with artificial test colours, to show the rows follow them.
  Reproduce: `uv run --no-sync --group docs python <S>/ver_token_probe.py <W> <E>`. No before: the base
  has no rule that reads these variables for the rows.
- `real-window-*.png` (33 images): the specification's walk in a real VS Code 1.148.0 window
  (Extension Development Host, isolated user-data and extensions folders). Reproduce:
  `fnm exec -- npm.cmd run bundle`, then `fnm exec -- node <S>/ver_walk_run.js <W> <scratch project> <E>`.
  No real-window run on the base: these are extra proof of the head, not a pair the plan named; the
  unmarked rows of the same picture show what a row looked like before.
  - `step1-enum-error-{light,dark}`: VS Code light and dark theme, preview in its default Cream mode.
    The dark one shows the defect: a dark red name on a dark maroon background on the cream page.
  - `step2-undeclared-warning-{light,dark}`, `step2-workbench-dark` (whole window).
  - `step2-modes-host-{light,dark}-mode-{cream,current,dark,white}`: both VS Code themes times the
    four preview theme modes.
  - `edit-hover-{error,warning}-{light,dark}`, `edit-open-{error,warning}-{light,dark}`.
  - `step3-fixed-{light,dark}`: value fixed and field removed, no marks, no badge.
  - `step4-schema-warning-{light,dark}`, `step4-modes-host-{light,dark}-mode-{cream,current,dark,white}`.

## Images to use in the PR body

The four visual pairs show the change. They do not show the Cream mode on a dark VS Code theme, which
fails today: after a fix, the real-window `step1` pictures are to be captured again at the new head.
