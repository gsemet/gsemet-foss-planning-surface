# Task: Restricted Mode images: test gaps

## Files (start here)

`baselineDiff.ts` and its tests; `requirements/tiers/swrs/trust-security/SwRS-MDOKFSTUDIO-TRUST-002.md`.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

The new `baselineDiff.ts` test fails when the workspace-root change is reverted.

## Requirements

Update or add the SwRS of scope `trust-security` (new ones `proposed`), markers
per `rules.md`. A test-only CR adds `@tests_req` markers to the requirement it checks.
A change to a rendered syntax also updates the writing skill (constitution, section 6).

## Changelog

Add one user-facing line under `## Unreleased` in `CHANGELOG.md` (skip for
test-only CRs).

## Gates (foreground)

- `just check`
- The e2e group `trust-security`, simulated (no real VS Code window).
- `just requirements-update`
