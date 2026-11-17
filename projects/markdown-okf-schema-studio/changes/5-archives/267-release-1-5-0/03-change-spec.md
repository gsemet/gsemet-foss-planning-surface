# CR 267, release 1.5.0

## Request

The owner asked for a release on 2026-11-06 and agreed on the version **1.5.0**. Follow
`.agents/guidelines/release-process.guidelines.md` (from step 3) on `origin/main`.

## Scope

Landed before the release (all on `main`, merged by the owner):

| CR | PR | Change |
| --- | --- | --- |
| 264 | #327 | Edit a document whatever the workspace trust; read-only file answer |
| 266 | #328 | Highlight a comment quote that crosses a soft line break |
| 265 | #329 | Keep the comment editor visible and easy to dismiss |

The changelog lines of the release are in PR #331 (opened by the main session, merged by the owner only).
Previous release: 1.4.0 (`docs/releases-notes/2026-11-05-v1.4.0/`).

## Decisions

- Version 1.5.0, agreed with the owner.
- Start the release driver only once PR #331 is on `main`; every other merge is held until publication.
- The heavy run must be green on the exact `main` HEAD after that merge (`integration` and `stress`).
- The owner reviews the notes, the thread and the version PR, and merges it. Nothing is posted: the owner posts.
- The release driver is a general-purpose agent (`chantier:*` agents refuse outside a batch). It never codes or
  reviews; fixes go through the Foreman as a fix CR.
