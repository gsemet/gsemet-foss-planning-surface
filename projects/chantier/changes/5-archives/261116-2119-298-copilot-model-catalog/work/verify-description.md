Head: 9d6484e18d519e9f1f936fca251a6c32972b34f4

Description pass of PR 250, posted body read with `gh pr view 250 --repo gsemet/chantier --json body`, judged at 9d6484e.

- Layout: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible; one Details fold with Changes, Human decisions, Impacts, Test plan, Internal references last. OK.
- Internal references: CR-298 and CR-297 names and work/r1.md appear only in Internal references (work/r1.md exists). OK.
- Claims vs diff (`git diff --stat <base>..HEAD`, 18 files): Changes list matches every changed file (tables + SOURCE.json, copilot_catalog.py, copilot-models.json, models.py, scripts/copilot_models.py, justfile, docs, CONTRIBUTING, tests, .gitattributes). No missing or unmentioned change. OK.
- Proofs name SHAs: `9d6484e` for gates, review, verify, CI; refresh output run at `943fcb4`'s tree, committed unchanged. `gh pr checks 250`: all 5 jobs pass. OK.
- Review box: log shows "r1 approved at 943fcb4, committed as 9d6484e", which matches "approved at 9d6484e". OK.
- Known gaps: the derived-identifier gap is present; no UNVERIFIED claim or uncaptured evidence pair elsewhere. OK.
- No STALE mark. Mermaid diagram is fenced as mermaid.

VERIFIED
