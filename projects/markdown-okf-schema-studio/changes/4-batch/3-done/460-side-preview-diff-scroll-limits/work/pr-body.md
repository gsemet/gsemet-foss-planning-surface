## Summary

The side preview follows the scroll of a diff's real-file side. Two cases were not covered by a real-window test: the inline diff layout, and a staged-like diff with no real-file side (the button opens the working-tree preview with no scroll following). This adds that coverage; no behaviour changes.

## Deliverables

None (tests only).

## Changes

- `test/integration/diffPreviewScroll.test.ts`: real-window tests D1 (inline layout scroll follows) and D2 (staged-like diff opens the working-tree preview, no scroll following), registered in the trusted suite and the e2e groups.
- `test/host/diffPreview.requirements.test.ts`: host test for the no-scroll rule of a diff with no real-file side.
- Requirements markers and a log entry for the existing behaviour.

## Impacts

No visual change.

## Blast radius

Grade: 1. Tests and requirement markers only; a plain `git revert` restores the previous state.

## Test plan

- [x] New or changed tests (tests only: they cover existing behaviour)
- [x] Requirements: SwRS markers added, `just requirements-update`
- [x] Changelog: No user-facing change
- [ ] Local gates: `just check` passed; real-window tests run in heavy CI only
- [ ] Review
- [ ] CI green

## Internal references

CR-460, follow-up of CR-455.
