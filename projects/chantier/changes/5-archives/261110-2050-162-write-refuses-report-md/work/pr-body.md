## Summary

Claude Code refuses a subagent's Write of a report-like file name before any permission check ("Subagents should return findings as text, not write report files. Include this content in your final response instead."). This CR renames what chantier subagents write under such names, and records the guard.

- The card `report.md` is now `status-layout.md` (100% rename), every link follows.
- The QA driver's `findings.md` is now `04-result.md` (`driver.md`, scenario).
- `hosts/claude-code.md` records the guard: its text, its rule (a `.md` name starting with report, summary, findings or analysis; from user reports in claude-code issues #44657 and #101519, unproved by Anthropic) and the probe that proves it here.
- `concepts.md` tells every subagent that writes a file not to start a `.md` name with those four words (for example `04-result.md`).
- The Chief of Staff's own `report.md` (a session, not a subagent) is unchanged; concepts rule 7 is unchanged.

## Deliverables

Name probe by a subagent's Write tool (2026-11-10): `report.md`, `findings.md`, `report-format.md`, `summary.md`, `analysis.md` refused with the guard's text; `04-summary.md`, `04-findings.md`, `04-analysis.md`, `04-report.md`, `04-result.md`, `status-layout.md`, `progress-report.md` and every other name chantier subagents write accepted. The user's first card choice `report-format.md` was refused, so the Chief of Staff picked `status-layout.md` (order note O-20). See `evidence/name-probe.md`.

## Test plan

- [x] `just check`
- [x] `just scenario`
- [x] No stale link to `references/report.md`

## Internal references

`.agents/changes/4-batch/2-actives/162-write-refuses-report-md/evidence/name-probe.md`
