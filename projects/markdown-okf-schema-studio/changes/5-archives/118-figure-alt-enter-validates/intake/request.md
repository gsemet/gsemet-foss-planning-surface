# 118 — Enter in the figure alt text validates and moves after the figure

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-enter-on-after-figure-image-edit`

## Intent (user)

When i paste or or edit a picture the alt text is selected

![image.png](../evidence/image.png)

In this case, when i hit enter i would expect to validate and move the cursor to the right, instead it replace the text by enter. this is logical BUT for human this is not expected.

we need to find a way to distinguish enter = add a enter in this altext (probably not possible in this inline mode) or enter = validate and move the caret just after the figure (kind of equivalent of cmd+enter). probably if there where no modification in the text = enter is acceptable

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- In the inline alt-text field, Enter always validates (the field is single-line, so a newline is never wanted) and moves the caret just after the figure; Shift+Enter does nothing special.
- Same behaviour after paste and after edit.
