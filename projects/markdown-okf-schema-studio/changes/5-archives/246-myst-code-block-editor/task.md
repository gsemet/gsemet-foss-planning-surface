# Task: A form for MyST code-block options

## Files (start here)

MyST palette forms (`src/page/modules/editPalette`); code block rendering in `src/core/render`.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

Unit tests on the generated directive and on reading options back; page test of the form.

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
