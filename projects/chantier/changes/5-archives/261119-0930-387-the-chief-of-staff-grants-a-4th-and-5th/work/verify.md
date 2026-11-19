# Verify CR-387
Head: 04494781c99ace5f0572cffd0406d28f1858723e

Claims, all judged at 0449478 (git diff 9c3fb6dd HEAD, 4 files, cards + SCORECARD only; grep of the Evidence section's phrases):
- "rounds exception" present in chief-of-staff.md (5), concepts.md (3), foreman.md (5), SCORECARD.md (1): grep -c output. PASS.
- Cap stated: settings.max_rounds, +1 per grant, never above max_rounds + 2 (chief-of-staff.md Steering paragraph, row G). PASS.
- `order note <cr> --note "rounds exception: ..."` in chief-of-staff.md; take with that note and no escalation in foreman.md; no hold rule in foreman.md (grep for hold/rounds: none). PASS.
- Blocked-twice exclusion in concepts.md and foreman.md (diff). PASS.
- Search for old phrasings (unless the user grants more, stays the user's, the one the user granted, on the user's word beside order rounds): none left without the exception (concepts 308, 613; chief-of-staff 1038, row G; SCORECARD C4). PASS.
- CI at this head (gh pr checks 349): just check macos/ubuntu/windows pass, eval-dry-run pass, just scenario (ubuntu-latest) pass. PASS.
- PR description (pr-body.md): clean, matches diff (4 files, sections), Known gaps None is right (no unverified claim). Test plan boxes carry <sha7> placeholders to fill at ship; Review/Verified boxes pending. PASS.

VERIFIED

## Description pass (posted body of PR 349)

Head: 04494781c99ace5f0572cffd0406d28f1858723e

- Judged at 0449478: `gh pr view 349 --json body,headRefOid` returns head 04494781c99a...; body checked against the pr-template audit.
- Sections and order: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps outside the fold; one details block holding Changes, Human decisions, Impacts, Test plan, Internal references; blank lines after summary and before details; nothing after. PASS.
- Deliverables: a before/after table with names matching the cards. PASS. Blast radius: one grade with explanation. PASS.
- Test plan: every item names 0449478; Review cites 9c3fb6d committed as 0449478, matching the Driver notes in `chantier log 387` ("r1 approved at 9c3fb6dd, committed as 04494781"). PASS. No STALE, no UNVERIFIED mark; Known gaps "None" is consistent.
- Internal references: CR name only inside Internal references. Role names (Chief of Staff, Foreman) are product terms of the cards the diff changes. PASS.

VERIFIED
