# Task: Make the atomic-save rename test deterministic

## Files (start here)

The unit test "linked target replaced by a rename (atomic save)" and the code it covers.

## Change

What `00-request.md` decides, and nothing more. The smallest change wins.

## Tests first

A repeat run (for example 200 iterations) before and after.

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
