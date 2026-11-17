# The code-block copy button cannot be reached with the keyboard

User decision (2026-10-24): fix, P2.

Current behaviour (F-CODE-028, specified as-is with "Known issue"): `src/page/modules/codeCopy.ts`
shows the copy button only on `mouseover`/`mousemove` and hides it otherwise. Tab skips it, so a
keyboard or screen-reader user cannot copy a code block.

## Expected

- The button is in the tab order (or the code block is focusable and reveals it), visible on
  focus, triggered by Enter or Space, with an accessible label ("Copy code").
- Page test for focus, reveal and keyboard activation; one visual scenario of the focus state in
  light and dark; update the code-blocks SwRS in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
