# Pasted image sometimes saved as an empty file

Seen in the advisory stress job of the manual heavy run on the PR "update the preview without
reloading" ([run 40016132398](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40016132398)):
the image-paste scenario failed at round 4/20 because the saved image file was empty (0 bytes).
The real VS Code integration job passed. Attempt 1 also had an infrastructure `ETIMEDOUT`.

The image-paste feature was already on main (pasted image as its own paragraph); the PR did not
touch it, so this is a flake of the feature or of its test.

## Expected

- Find the cause with evidence (ci.guidelines.md rule 12): when the file is created vs written,
  whether the page sends the bytes before the host writes, a race between write and the stress
  scenario's read, or a test-side read too early.
- Fix at the cause with a deterministic readiness signal (no retry, no sleep), add diagnostics to
  the failure message, and prove it with the stress mode.

Note: touches `src/` — wait for the end of the refactor freeze (CR 056).
