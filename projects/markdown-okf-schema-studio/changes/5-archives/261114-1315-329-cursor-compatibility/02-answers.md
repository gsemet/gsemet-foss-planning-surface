# Answers

## 2026-11-14: picked for batch-04

Owner, 2026-11-14: « Faisons les 3 CR. Uniquement pose moi les questions impactantes ». The
three open items after v1.9.1 (lost edit-toggle clicks, palette focus bounce, Cursor
compatibility) go into batch-04. Priority P1. The Chief of Staff decides every question without a
user impact; only questions with a user impact go to the owner.

Decided by the Chief of Staff (no user impact):

- Close the report's open points that can be closed without Cursor installed: the VS Code engine
  version Cursor, VSCodium and Windsurf ship (their public release notes or docs), compared with
  `engines.vscode` `^1.95.0`; whether `capabilities.agentsWindow` is ignored elsewhere.
- Document the result in the user docs (`docs/user/open-studio.md`, README install section): which
  editors are expected to work, and that they install from Open VSX.
- Questions with a user impact go to the owner: lowering `engines.vscode` (it changes who can
  install), and installing Cursor on this machine for a smoke test (a download).

## 2026-11-14: after the spec

Decided by the Chief of Staff: `engines.vscode` stays `^1.95.0` (no change, so no user impact:
every current fork is above it). The docs say "expected to work"; the smoke test in a real fork is
left to the owner after merge, as an offer, and does not block the CR.
