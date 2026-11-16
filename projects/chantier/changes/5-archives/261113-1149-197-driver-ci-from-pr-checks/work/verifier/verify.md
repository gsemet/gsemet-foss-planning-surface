# Verify CR-197

Head: 01e1288bf77064ffab2ea998379656a6d993e866

Claims, each judged at 01e1288:
- Gate: work/gates/20261112-232844.log, first line "gate CR-197 ... head 01e1288bf77064ffab2ea998379656a6d993e866"; just check 50 passed, release-notes ok; just scenario github 586/586, gitlab 586/586; "result: pass at 01e1288...".
- driver.md `CI:` bullet (git diff origin/main...HEAD): only-source, rules-do-not-replace-the-look with `note`, head-first (`gh pr view --json headRefOid`), two looks with second a minute after the push, one bounded wait named as the exception to rule 8 (once, never a loop), note naming command and 7-char head. Diff only adds lines apart from re-wrapping one sentence ("Read the result yourself (`gh pr" kept, text intact); nothing removed. PASS.
- concepts.md rule 8: only the parenthesised pointer to driver.md `CI:` added. PASS.
- pr-template.md: CI item comment carries `No CI: no check listed at <sha7>`, checked, never deleted, never "CI green". PASS.
- SCORECARD.md: row J25 after J24, `by hand`, text as specified. PASS.
- Audit: `audit.scorecard_rows()` at the head parses 45 rows, last J25, how "by hand". `audit.py <empty workspace>` stops with "no batch in 4-batch/" (no workspace to audit), before the scorecard stage; no UNKNOWN RAIL or missing-row error. PASS for the parsing; a full audit needs an eval run, not possible here.
- Scope: changed files are exactly the four above; nothing under agents/, com.github.copilot/agents/, skills/chantier/scripts/ or evals/kit/. PASS.
- PR description on the forge (gh pr view 142, headRefOid = 01e1288): renders, Summary/Deliverables/Changes match the diff, no change unmentioned. Open point, not a failure of a claim: the Test plan boxes still read `<sha7>` and are unchecked except Review; the Driver must fill Local gates, Evidence, Verified and CI at 01e1288 before hand-back. CI at 01e1288 on the forge: check, eval-dry-run success; scenario (ubuntu) still in progress when read; not waited for.

Evidence: a card-only change with nothing to see; before-after.md says so.

VERIFIED
