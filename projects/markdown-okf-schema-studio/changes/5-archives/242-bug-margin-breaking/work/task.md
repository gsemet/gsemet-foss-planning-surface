# Task: Tables stay in the column when they fit, and break out when they need to

## Files (start here)

The width modes and breakout: `src/page/modules/widthMode.ts`, `src/core/preview/previewStyles`; table measuring code near the breakout.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

Page tests per prototype case (1-12) at a 720 px column that fail today for the cases the rule changes; the code-block-in-cell case. Light and dark screenshots before/after.

## Requirements

Update or add the SwRS of scope `layout-width` (new ones `proposed`), markers
per `rules.md`. A test-only CR adds `@tests_req` markers to the requirement it checks.
A change to a rendered syntax also updates the writing skill (constitution, section 6).

## Changelog

Add one user-facing line under `## Unreleased` in `CHANGELOG.md` (skip for
test-only CRs).

## Gates (foreground)

- `just check`
- The e2e group `layout-width`, simulated (no real VS Code window).
- `just requirements-update`
