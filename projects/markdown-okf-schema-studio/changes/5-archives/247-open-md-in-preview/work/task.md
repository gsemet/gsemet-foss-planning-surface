# Task: A document always opens in preview mode, and E switches to edit mode

## Files (start here)

Edit-mode state across document switches: `src/page/runtime.ts`, `src/page/features/pageRuntime.ts`, the session side in `src/session`.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

Page test: edit mode on document A, open document B → preview mode (fails today); E in preview enters edit mode; E in a text field types an E.

## Requirements

Update or add the SwRS of scope `lifecycle-sync` (new ones `proposed`), markers
per `rules.md`. A test-only CR adds `@tests_req` markers to the requirement it checks.
A change to a rendered syntax also updates the writing skill (constitution, section 6).

## Changelog

Add one user-facing line under `## Unreleased` in `CHANGELOG.md` (skip for
test-only CRs).

## Gates (foreground)

- `just check`
- The e2e group `lifecycle-sync`, simulated (no real VS Code window).
- `just requirements-update`
