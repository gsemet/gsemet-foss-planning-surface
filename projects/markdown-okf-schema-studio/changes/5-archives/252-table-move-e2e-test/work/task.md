# Task: End-to-end test of a table row drag

## Files (start here)

`src/page/features/tableRowMove.ts` and the e2e harness of group `table-editing`.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

The scenario fails when the CR 240 fix is reverted.

## Requirements

Update or add the SwRS of scope `table-editing` (new ones `proposed`), markers
per `rules.md`. A test-only CR adds `@tests_req` markers to the requirement it checks.
A change to a rendered syntax also updates the writing skill (constitution, section 6).

## Changelog

Add one user-facing line under `## Unreleased` in `CHANGELOG.md` (skip for
test-only CRs).

## Gates (foreground)

- `just check`
- The e2e group `table-editing`, simulated (no real VS Code window).
- `just requirements-update`
