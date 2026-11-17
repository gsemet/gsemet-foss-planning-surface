# CR 212 driver report

Commit f2c55c692d7bbb1f223c1e1d97cc1e56f77c2f8f (parent b9118506), branch
change-requests/212-rich-tickets-and-generated-orchestrator, not pushed, no PR (Foreman stacks).

## Rounds

- r1 Coder (sonnet) -> Inspector (opus) APPROVE, 6 non-blocking findings.
- r2 Coder fixed findings 1,2,3,4,6 -> Inspector APPROVE, 4 small non-blocking findings.
- r3 Coder fixed findings 1-4 (count=1 alert mask, exact drift assertion, wait-ci/landed icons, non-UTF-8 STATE.md) -> Inspector APPROVE.
- Remaining non-blocking: non-UTF-8 archive report.md still raises; long Python lines (style).

## Gates (driver run)

- py_compile OK; just check exit 0: unit 3288/3288, contracts 0 tests (suite empty on base too), security 71/71, release-tests 153 passed (14 new), requirements-lint OK.
- okfreq validate --check-links --project-root . exit 0 (pre-existing W2 broken-link warnings).

## Dry run on a copy of live .agents/changes (copy deleted)

- Exit 1: 211 STATE.md line 2 unparsable (`status: handed back`), 170 has no STATE.md. Both rows marked.
- Second run with --today 2030-01-01: mtime unchanged (no-op).
- Active 4 rows (adds 213, missing from the live table). Backlog 43 vs 42: drops stale qa-skill-drivers-and-new-feature-coverage (already moved to CR 211), adds radio-choice-lists and radio-list-palette-button; file counts are real (evidence folders counted). P1 unnecessary-table-margin-breakage title `—` (its 01-intent.md has no H1).
- Landed 204 rows vs 157: all archives listed with correct ../04-archives/ links (live has 59 stale ../archives/ links); 65 rows undated and 73 without PR (older report.md formats; no guessing).
- Lost: the hand-written paragraphs under Active/Backlog and the "Planner-tick mode" section, unless moved into ORCHESTRATOR-NOTES.md first.
