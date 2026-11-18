# A release is finished after the user publishes it by hand

## The problem

When the host refuses the Release driver's publication command (for chantier, CONTRIBUTING.md
"Release" step 5, `gh release create vX.Y.Z --verify-tag --notes-file ...`), the Release driver
hands back `blocked approval: publish: <the exact command>` and the steering session gives the
user the command ("the publication is yours"). The user runs it by hand. Then nobody finishes the
release: no `release published` is recorded, no `work/retro.md` is written, no `handback ready`
moves the release CR to `3-done`, so the batch never pauses, the "Released in" comments are never
offered and the release's retro never reaches the Completion report.

## What the user wants

After the user's publication, the steering session takes the release back to a Driver, which runs
the end checklist of the Release driver ("Release driver: the end" in `driver.md`): `release
published`, the procedure's checks, `retro.md`, `handback ready`. The user says once that the
release is published; the rest goes on with no further word from them.

## Today, at main (2026-11-18, after CR-368)

- `driver.md`, "Release driver": the refusal route exists (`handback blocked approval: publish:
  <the exact command>`, try nothing else), and the end checklist exists (CR-310). Nothing says what
  a Driver does once the publication was done by someone else.
- `chief-of-staff.md`: P9 tells the user at the start that a refused publication is theirs; no
  text says what to do once the user has published. "Releases" handles approval asks with `order
  approve` (CR-368: the post-merge word is asked with the merge go), which does not fit here: the
  step is done, not approved.
- `foreman.md`: an order note on a `blocked` CR is taken back with that note; nothing names this
  case for a release.
- The CLI needs nothing: `order note` on a `blocked` release is accepted, the Foreman's `take
  --note` reopens it, `release published` and `handback ready` end it as today.

Split off from release-driver-end-checklist (CR-310) on 2026-11-17 (release-checklist-Q1).
