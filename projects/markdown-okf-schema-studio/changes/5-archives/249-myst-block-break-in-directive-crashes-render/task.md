# Task: A +++ line inside a container no longer crashes the MyST render

## Files (start here)

MyST parsing of `+++` and containers in `src/core/render`, `src/core/syntax/blockQuoteRange.ts` (`lazyLineAsText`).

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

One render unit test per input of `01-intent.md` (they throw today).

## Requirements

Update or add the SwRS of scope `myst` (new ones `proposed`), markers
per `rules.md`. A test-only CR adds `@tests_req` markers to the requirement it checks.
A change to a rendered syntax also updates the writing skill (constitution, section 6).

## Changelog

Add one user-facing line under `## Unreleased` in `CHANGELOG.md` (skip for
test-only CRs).

## Gates (foreground)

- `just check`
- The e2e group `myst`, simulated (no real VS Code window).
- `just requirements-update`
