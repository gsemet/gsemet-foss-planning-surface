# Task: TOC rail polish

## Files (start here)

See the CR 239 archive report and `01-intent.md`.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

Escape scoped to the overlay (test fails today); padding at the rail width; split of `capture_layout_checks.py` keeps every check.

## Requirements

Update or add the SwRS of scope `toolbar-navigation` (new ones `proposed`), markers
per `rules.md`. A test-only CR adds `@tests_req` markers to the requirement it checks.
A change to a rendered syntax also updates the writing skill (constitution, section 6).

## Changelog

Add one user-facing line under `## Unreleased` in `CHANGELOG.md` (skip for
test-only CRs).

## Gates (foreground)

- `just check`
- The e2e group `toolbar-navigation`, simulated (no real VS Code window).
- `just requirements-update`
