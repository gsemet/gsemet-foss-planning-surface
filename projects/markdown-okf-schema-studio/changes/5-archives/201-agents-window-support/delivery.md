# Report: CR 201, Studio in the VS Code Agents window

Landed: #223, merge commit 57ec42e1 (2026-10-29).

- Manifest declares `capabilities.agentsWindow.supported`; Studio is enabled in the Agents window
  with no user setting (spike v5, VS Code 1.144).
- A read-only preview becomes editable on the same panel when a folder holding its file is added;
  removing a folder keeps the tab open read-only (main window too).
- Requirements: new SwRS-MDOKFSTUDIO-LIFE-171; TRUST-001 and LIFE-143 updated.
- Gates: preflight green; PR CI and heavy run green (run 40896825598). Review: APPROVE, round 1.
- Follow-ups: review findings 1-3 (remove during render, untested LIFE-143 rows, pending
  follow-the-editor switch dropped on session replace) not filed; diff views tracked in
  02-backlog/P2/studio-in-diff-views.
