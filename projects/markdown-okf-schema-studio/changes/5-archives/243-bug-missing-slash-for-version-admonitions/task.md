# Task: Every MyST admonition is in the MyST slash menu

## Files (start here)

The slash menu definition and the MyST palette (`src/page/modules/editPalette`, `src/page/modules/editActions`); the admonition icons used by the renderer.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

Unit test listing the MyST slash entries (fails today for the missing ones); inserting `versionadded` yields a valid `:::{versionadded} <version>` block.

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
