# Release v0.15.1

Patch release of chantier shipping the session-folder fix (P6 and P7 accept the project's or the
surface's main checkout as the session folder).

- Version: 0.15.1, set by the user (a patch).
- Procedure: `CONTRIBUTING.md` "Release" and `docs/release-process.md` (release folder, notes,
  anonymisation, claims file).
- No eval before it and no local long gate: the user's words, 2026-11-23. The release notes' "Not
  exercised by an eval" bullet and the claims file say so as the process requires.
- It runs on its own: the user is asleep. The steering session merges the release PR and runs
  `just tag` and `gh release create` under the grant recorded for this release; the announcement
  stays a draft, never posted.
- After it, the batch pauses.
