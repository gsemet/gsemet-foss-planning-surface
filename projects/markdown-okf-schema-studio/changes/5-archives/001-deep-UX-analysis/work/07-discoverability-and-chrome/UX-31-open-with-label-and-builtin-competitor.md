# UX-31 — "Open With" shows a duplicated label next to VS Code's built-in Markdown Editor

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Observed (VS Code 1.141.0) |
| Area | Naming, positioning |
| Evidence | [r2-p3.jpg](../../evidence/r2-p3.jpg) |

## Observed

**View: Reopen Editor With…** lists:

```text
Text Editor              Active and Default, Built-in
Markdown Preview         Built-in
Markdown Editor          Built-in
Markdown OKF-Schema Studio   Markdown OKF-Schema Studio
```

- The Studio row repeats its name because the custom editor `displayName` and the extension
  `displayName` are identical (the README documents this, but users still read it as a glitch).
- VS Code 1.141 ships a built-in "Markdown Editor". Users now choose between three Markdown views
  without guidance on what Studio adds (MyST directives, OKF schema table, x-okf-link navigation).

## Suggested direction

Rename the custom editor entry to describe the role ("MyST + OKF Studio" or "Studio (MyST/OKF)"),
and state the difference from the built-in editors in the README and the extension description.
Track the built-in Markdown Editor's capabilities as a competitive baseline in the next analysis.

## Done when

The picker row reads as one clear, distinct choice.
