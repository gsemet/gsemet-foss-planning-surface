# T03 implementation — round 1

STATUS: DONE

## Summary
Added a shared plain-JavaScript geometry checker (`test/shared/geometry-checks.js`) with the four
checks from the task (`overlay-covers-text`, `overlay-clipped`, `identifier-split`,
`status-two-lines`). It is wired into the real-input `Evidence.capture` (new `options.checks`,
`required` throws after the note and screenshot are written) and into the static visual campaign
`check_final_frame` (`machineChecks` stored per scenario; only scenarios that list a check in
`machineChecks` fail on it). No scenario opts in, so nothing becomes required. Each visual sidecar
and real-input note has a `Machine checks` section. The visual run also writes `MACHINE-CHECKS.md`
and links it from `INDEX.md`. The `visibleHeaders` probe now ignores button glyphs, as the task asks.

## Files changed
- `test/shared/geometry-checks.js` (new) — `studioGeometryChecks(options)`, one function, layout reads only.
- `test/webview/geometryChecks.test.ts` (new) — vm-context load; four check ids; all not-applicable/pass with an empty fake DOM.
- `test/integration/realInput/harness.ts` — `CaptureChecks` type; `Evidence.capture(..., options?)` evaluates the checker in the frame, writes `## Machine checks`, throws for a failing required check after writing.
- `test/visual/capture.py` — `GEOMETRY_SOURCE`; checker call in `check_final_frame`; `machine_check_lines`; `Machine checks` sidecar section; `MACHINE-CHECKS.md` writer; INDEX link line; `visibleHeaders` `.map` ignores buttons.
- `test/visual/scenarios.ts` — optional `machineChecks?: string[]` on `Scenario`.

`renderFixtures.ts` was not changed: the manifest spreads each whole scenario (`...scenario`), so the field reaches Python.

## Tests written first (failing before the fix)
- Not applicable. T03 adds tooling, not a bug fix. The two new unit tests were written with the file they test and passed on the first run.

## Tests added or changed
- `geometry checks define one function that reports the four check ids` — the file evaluates in `vm` and defines the function with the four ids.
- `without any DOM content every geometry check is not applicable and passes` — the fake-document contract from the task.

## Existing assertions changed
- `test/visual/capture.py` `OKF_SCHEMA_CHECKS` `visibleHeaders` probe (not an assertion; the `["Name", "Value"]` comparison is unchanged) — old: `cell.textContent?.trim()` → new: clone the cell, remove buttons, then read text — required by the T00 follow-up in the task. Effect: the baseline line `narrow schema headers are ['Name', 'Value◀▶']` now passes.

## Verification
- `scripts/gate.sh T03-impl unit` → PASS (`logs/T03-impl-unit.log`; compile PASS, both new tests ran and passed)
- `scripts/gate.sh T03-impl trusted` → PASS (`logs/T03-impl-trusted.log`, build `logs/T03-impl-trusted-build.log`; no `Frame was detached` flake this run)
- `scripts/gate.sh T03-impl visual` → PASS vs baseline (0 new failure lines; 2 baseline lines now passing; `logs/T03-impl-visual.log`, failures `logs/T03-impl-visual-failures.txt`, copy of screenshots `logs/visual-T03-impl/`)
  - The two now-passing lines are (a) `08-okf-schema--dark--sticky-3--default.html: narrow schema headers ... expected Name/Value`, the intended fix, and (b) the summary line `failed: okf-schema-narrow (alias of frontmatter-scroll-feedback)`, which only exists because the alias had that header failure. Run status in `INDEX.md` stays `failed` because of the existing baseline failures.
- Note checks: 5 real-input notes from `real-input-RKFDgZ` each have `## Machine checks`; 90 visual sidecars each have `Machine checks`.

## Evidence for reviewers
- Machine check report: `logs/visual-T03-impl/MACHINE-CHECKS.md`; linked from `logs/visual-T03-impl/INDEX.md`.
- Real-input note sample: `.artifacts/real-input-RKFDgZ/01-paragraph-blur-commit.md`.
- Visual sidecar sample: `logs/visual-T03-impl/01-okf-schema--dark--sticky-3--default.txt`.
- Report-only failures in `MACHINE-CHECKS.md` (baseline for UI tasks, not fixed here): 45 rows, `identifier-split` 35 and `overlay-covers-text` 10. Examples: `code-dark-top` identifier-split (`2024-03-11`, `FAR-RIGHT-ACCESS`, `nw-02`); `okf-schema-narrow` identifier-split (`type(enum)`, `title(text)`, ...). The list is in the file itself.

## Feedback addressed (rounds 2–3)
- Not applicable (round 1).

## Open points / STOP reason
1. **MACHINE-CHECKS.md is not kept after the gate.** The `visual` gate restores `test/visual/screenshots/` and deletes untracked files there, so the file the task asks to exist is removed after the run. It exists during the run and in `logs/visual-T03-impl/MACHINE-CHECKS.md`. The orchestrator must decide where the file should live (for example, tracked output or a fixed path outside the screenshots folder). I did not change `gate.sh` (not an allowed file).
2. **Some real-input-style notes are not covered.** `test/integration/previewEditing.test.ts` (`frontmatter-e2e-*`) and `test/integration/checkboxToggle.test.ts` (`checkbox-e2e-*`) write their own PNG and note files and do not use `Evidence.capture`, so their notes have no `Machine checks` section. Both files are outside Allowed files, so I did not change them. The task's Done-when item "every real-input note" is met for the T02 harness (`realInput`) only. The reviewer should decide whether these suites must also get the section; that needs an allowed-file change in a follow-up.
3. Design choice: a required check that is not applicable does not fail (matches the visual rule "applicable and failing"). No check is required in this task.
