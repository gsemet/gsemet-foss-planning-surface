# Task: Every rendered syntax can be inserted from the slash menu and the toolbar

## Files (start here)

The rendered syntax list (`src/core/render`, the writing skill `skills/writing-for-markdown-okf-schema-studio/`) against the slash and toolbar definitions.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

A unit test that fails when a rendered syntax has no slash entry (with an explicit, documented exception list).

## Requirements

Update or add the SwRS of scope `palette-slash` (new ones `proposed`), markers
per `rules.md`. A test-only CR adds `@tests_req` markers to the requirement it checks.
A change to a rendered syntax also updates the writing skill (constitution, section 6).

## Changelog

Add one user-facing line under `## Unreleased` in `CHANGELOG.md` (skip for
test-only CRs).

## Gates (foreground)

- `just check`
- The e2e group `palette-slash`, simulated (no real VS Code window).
- `just requirements-update`
