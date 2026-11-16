## Name probe

Date: 2026-11-10. Write tool, subagent context, under a temp folder. Refusal text R = "Subagents should return findings as text, not write report files. Include this content in your final response instead." Accepted text A = "File created successfully at: <path> (file state is current in your context — no need to Read it back)".

| path | result | tool result text | date |
|---|---|---|---|
| report.md (control) | refused | R | 2026-11-10 |
| 03-change-spec.md | accepted | A | 2026-11-10 |
| work/investigator/investigation.md | accepted | A | 2026-11-10 |
| work/coder/r1.md | accepted | A | 2026-11-10 |
| work/debugger/diagnosis.md | accepted | A | 2026-11-10 |
| work/verifier/verify.md | accepted | A | 2026-11-10 |
| work/verifier/evidence/before-after.md | accepted | A | 2026-11-10 |
| work/conflict-resolver/conflicts.md | accepted | A | 2026-11-10 |
| 4-batch/demo/demo.md | accepted | A | 2026-11-10 |
| work/pr-body.md | accepted | A | 2026-11-10 |
| intake/request.md | accepted | A | 2026-11-10 |
| 01-intent.md | accepted | A | 2026-11-10 |
| 02-answers.md | accepted | A | 2026-11-10 |
| delivery.md | accepted | A | 2026-11-10 |
| STATUS.md | accepted | A | 2026-11-10 |
| findings.md | refused | R | 2026-11-10 |
| work/release/release-notes.md | accepted | A | 2026-11-10 |
| work/release/tweet.md | accepted | A | 2026-11-10 |
| work/retro.md | accepted | A | 2026-11-10 |
| work/fix-1.md | accepted | A | 2026-11-10 |
| skills/chantier/references/report-format.md | refused | R | 2026-11-10 |
| progress-report.md | accepted | A | 2026-11-10 |

## Round 2 probe

Date: 2026-11-10. Write tool, subagent context, temp folder. Exact tool text for each: "File created successfully at: <path> (file state is current in your context — no need to Read it back)".

| path | result |
|---|---|
| status-layout.md | accepted |
| qa-notes.md | accepted |
| skills/chantier/references/status-layout.md | accepted |

## Round 3 probe

Date: 2026-11-10. Write tool, subagent context, folder Temp/name-probe-162c/ (removed after). Accepted text: "File created successfully at: <path> (file state is current in your context - no need to Read it back)". Refused text: "Subagents should return findings as text, not write report files. Include this content in your final response instead." (tool_use_error).

| name | result |
|---|---|
| 04-result.md | accepted |
| 04-summary.md | accepted |
| 04-findings.md | accepted |
| 04-analysis.md | accepted |
| 04-report.md | accepted |
| summary.md | refused |
| analysis.md | refused |

Consistent with the starts-with rule: only the bare names are refused; a numbered prefix passes.
