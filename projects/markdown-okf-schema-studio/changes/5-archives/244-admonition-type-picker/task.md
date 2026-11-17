# Task: Pick an admonition's type from a list above it

## Files (start here)

Block editor caret handling and popups in `src/page/modules` (see how the edit palette shows popups); the admonition type list from CR 243.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

Page tests: caret on the type opens the list; a pick changes only the type text; Escape closes. GFM and MyST.

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
