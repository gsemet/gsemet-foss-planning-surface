# CR-513 before and after

Two verification passes. The current one is at head `cd3b8e6`; the earlier one, at `1fa9587`, is kept
below because the PR body still shows its "before" pictures.

- `<W>` = the CR worktree at the head, `<B>` = a detached worktree of the base (removed at the end),
  `<S>` = the CR folder's `work/scratch`, `<E>` = this folder.
- All documents are made up. Every picture listed here was opened: none shows a username or a home
  folder path.

## Pass at head cd3b8e6

- Before: base `abfa71e58f2f150d028781beaeecc2bede4c8182` (source of the base; the head's `test/`
  folder checked out over it, so both sides render the same documents).
- After: head `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f`.

### Visual scenarios (rendered page of the visual harness, Current mode, 900 px)

Reproduce, in `<B>` (`npm ci`, `uv sync`) and in `<W>` (`just dev`):
`fnm exec -- npm.cmd run visual:render`, then
`uv run --no-sync --group docs python test/visual/capture.py --group frontmatter-schema`.

| Before | After | Shows |
| --- | --- | --- |
| cd3b8e6-before-v32-field-issue-rows-light-900.png | cd3b8e6-after-v32-field-issue-rows-light-900.png | `status` (error) and `bonus_field` (warning): plain rows, then coloured name and wavy underline, light |
| cd3b8e6-before-v33-field-issue-rows-dark-900.png | cd3b8e6-after-v33-field-issue-rows-dark-900.png | the same, dark |
| cd3b8e6-before-v34-schema-warning-row-light-900.png | cd3b8e6-after-v34-schema-warning-row-light-900.png | "Schema could not be parsed" row: plain, then warning colour on a tinted background across the table, light |
| cd3b8e6-before-v35-schema-warning-row-dark-900.png | cd3b8e6-after-v35-schema-warning-row-dark-900.png | the same, dark |

The harness themes of the head set the status colours of a VS Code theme (in the light theme the
warning colour is a darker stand-in).

### After only, real VS Code window

`window-cd3b8e6/real-window-*.png` (33 pictures): the specification's walk in VS Code 1.148.0
(Extension Development Host, its own user-data and extensions folders), default Dark Modern and
Light Modern themes. Reproduce: `fnm exec -- npm.cmd run bundle`, then
`fnm exec -- node <S>/ver2_walk_run.js <W> <S>/walk2 <E>/window-cd3b8e6`
(`<S>/walk2` is the made-up walk project written by `ver2_walk_derive.py`). No run on the base: the
unmarked rows of the same picture show what a row looked like before.

- `step1-enum-error-{light,dark}`: the preview in its default Cream mode; the dark one is the cell
  that failed at `1fa9587` and now reads dark red on light red.
- `step2-undeclared-warning-{light,dark}`, `step2-workbench-dark` (whole window).
- `step2-modes-host-{light,dark}-mode-{cream,current,dark,white}`.
- `edit-hover-{error,warning}-{light,dark}`, `edit-open-{error,warning}-{light,dark}`.
- `step3-fixed-{light,dark}`: value fixed and field removed, no marks, no badge counts.
- `step4-schema-warning-{light,dark}`, `step4-modes-host-{light,dark}-mode-{cream,current,dark,white}`.

### Why an edited cell has no underline

`cd3b8e6-underline-rule-off-on.png`: the open editor and its field menu with the shipped rule that
drops the underline overridden (left, "rule-off": wavy lines under the placeholder, the text and the
menu items) and as shipped (right, "rule-on": none). Reproduce:
`uv run --no-sync --group docs python <S>/ver2_underline_probe.py <W> <S>/ver2-underline-shots`.

### Pictures posted on the PR

The ten pictures of the PR body are the files of the CR folder's `evidence/` (same sha256) and
differ by no pixel from the top of the captures of this pass (`<S>/ver2-posted-compare.log`): the
four "before" ones from the base `abfa71e`, the six "after" ones from the head `cd3b8e6`.

## Earlier pass, head 1fa9587 (base 9d7e788)

- Before: base `9d7e788a479dec70fd882d295bf0d5e78f4f6b98` (source of the base; the head's tests and
  fixtures copied over it).
- After: head `1fa9587eb1f6a5e53ef5bce5269d292bc2517859`. These "after" pictures are superseded.

### Visual scenarios

| Before | After | Shows |
| --- | --- | --- |
| before-v32-field-issue-rows-light-900.png | after-v32-field-issue-rows-light-900.png | `status` (error) and `bonus_field` (warning): plain rows, then coloured name and wavy underline, light |
| before-v33-field-issue-rows-dark-900.png | after-v33-field-issue-rows-dark-900.png | the same, dark |
| before-v34-schema-warning-row-light-900.png | after-v34-schema-warning-row-light-900.png | "Schema could not be parsed" row: plain, then warning colour on a light background across the table, light |
| before-v35-schema-warning-row-dark-900.png | after-v35-schema-warning-row-dark-900.png | the same, dark |

The harness themes of that head set none of the four severity tokens (fallback colours).

### Edit mode (rendered pages, driven with Playwright)

Reproduce: `uv run --no-sync --group docs python <S>/ver_edit_probe.py <W> <B> <E>`.

| Before | After | Shows |
| --- | --- | --- |
| before-edit-hover-error-name-{light,dark}.png | after-edit-hover-error-name-{light,dark}.png | pointer over the error name cell: hover background, the name keeps the error colour |
| before-edit-hover-warning-name-{light,dark}.png | after-edit-hover-warning-name-{light,dark}.png | the same for the warning name cell |
| before-edit-open-error-value-{light,dark}.png | after-edit-open-error-value-{light,dark}.png | open editor on the error value: no wavy underline on the editor or its menu |
| before-edit-open-warning-value-{light,dark}.png | after-edit-open-warning-value-{light,dark}.png | the same on the warning value |

### Narrow page, 360 px

Reproduce: `uv run --no-sync --group docs python <S>/ver_wrap_probe.py <W> <B> <E>`.

| Before | After | Shows |
| --- | --- | --- |
| before-wrap-360-v34-light.png | after-wrap-360-v34-light.png | the whole-table warning message wraps (3 lines) inside the table; coloured after |
| before-wrap-360-v35-dark.png | after-wrap-360-v35-dark.png | the same, dark |

### After only (1fa9587)

- `after-tokens-set-{v32-light,v33-dark,v34-light,v35-dark}.png`: the four `--vscode-*` severity
  variables set on the page root with artificial test colours.
- `real-window-*.png` in this folder (33 pictures): the walk at `1fa9587`; `step1-enum-error-dark`
  shows the defect of that head (dark red on dark maroon on the cream page).
