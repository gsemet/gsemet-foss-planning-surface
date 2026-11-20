## Summary

Requirement markers link a requirement to the code or test that carries it, but two kinds of bad link passed `just check`: an in-force SwRS with no `@implements_req` at all (DIAG-128 was one), and long lists of IDs piled on a file header or in a marker-only file, which point at no code or test in particular. `just check` (so the `static` jobs on Linux and Windows) now refuses both. Existing offenders are frozen in a baseline that can only shrink.

## Deliverables

The three rules of `scripts/check-marker-companions.mjs`:

| Rule | Refuses | Baseline |
| --- | --- | --- |
| 1 | an in-force (`draft`, `proposed`, `approved`), non-exempt SwRS with no `@implements_req` in a source dir | none |
| 2 | a marker block naming more than 3 distinct IDs | `blocks` in `scripts/marker-baseline.json` |
| 3 | a companion marker line without ` — <scenario or code point>`, or whose name is not found in the host file or its folder | `unnamedCompanionLines` |

A marker block is the markers that sit together with no code line between them, blank and prose comment lines included. A companion is a file under `src/` or `test/` named `*.markers.ts` or holding a `// Companion of:` line.

## Changes

- `scripts/check-marker-companions.mjs`: pure functions exported, `--root <dir>`, the three rules, the ratchet (`--update` only lowers or removes entries).
- `scripts/marker-baseline.json`: today's offenders.
- DIAG-128 gets its `@implements_req` where the export waits for diagrams; the stale `@tests_req` on LAYOUT-021 is removed.
- The four `*.markers.ts` companions name their code point; the plantuml bundle companion now points at `esbuild.mjs`.
- Docs: marker block definition in the glossary and in the requirements project guidelines ("Marker placement"), `CONTRIBUTING.md`, `justfile` comment, requirements log entry.

## Human decisions

- An in-force, non-exempt SwRS with no `@implements_req` fails `just check`, with no baseline.
- A marker block names at most 3 IDs; today's offenders sit in a baseline that can only shrink.
- A companion marker line names its scenario or code point after an em dash, and the name must occur in the host file or its folder; a fully named companion escapes the 3-ID cap.
- Any tracked file with a `// Companion of:` line is a companion, not only `*.markers.ts`.
- The check stays in Studio, extending the existing script.

## Autonomous decisions

- The code point named in each of the four existing companions, and the `embedImages` marker for DIAG-128, were chosen by reading the code.
- The name lookup is done by the script, outside the companion file.

## Impacts

Developers: a new marker list over 3 IDs, or an unnamed companion line, now fails `just check`. No behaviour or visual change for users.

## Blast radius

Grade: 1. The check is one script plus a baseline and no workflow file changes; it only adds refusals to the existing `static` jobs, and a plain `git revert` restores the previous gate.

## Test plan

- [x] New or changed tests: `test/build/checkMarkers.test.ts` (rules 1 to 3 and the ratchet, each on a scratch git repository)
- [x] Requirements: DIAG-128 marked, stale marker removed, `just requirements-update` run
- [x] Changelog: No user-facing change
- [x] Local gates: `just preflight` (static stage on Windows) passed at 10c9233; the unit test 6/6; `just requirements-lint`
- [x] Review: approved at 10c9233 (committed from the reviewed state)
- [x] CI green at 10c9233: static, static-windows, visual, checks pass
- [x] Verified at 10c9233

## Known gaps

None.
