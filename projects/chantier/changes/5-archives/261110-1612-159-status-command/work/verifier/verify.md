# Verify, CR-159 status-command, head cd4b7cd

VERIFIED.

1. `just check` run in the worktree: 36 passed, release-notes ok. Gate log work/gates/20261110-164450.log: check plus scenario github 379/379 and gitlab 379/379. `gh pr checks 96`: check on macOS, Ubuntu, Windows and scenario all pass.
2. report.md vs the old "Reports", "Status" and "Cost" bullets of origin/main: every rule is present (name by number+slug, same shape, MR/PR, six icons copied from `label`, 🟠/⚪/🔴 definitions, Progress items, 🔵 rule, chain line, demo offer, Completion items, cost lines and `cost --explain`, Tips, refresh with no epoch). Only dropped: the "as for P9" aside; added: STATUS.md as the icon source, slug-only naming for items with no number (also in concepts.md). chief-of-staff.md points to it in Status, Reports, Cost, chain, offer.
3. skills/status/SKILL.md: reads report.md only, runs refresh (no epoch), status, cost per active batch, takes icons from batch STATUS.md, no-active line with backlog count, changes nothing. Registered in .github/plugin/plugin.json, scripts/version.py, test_structure.py (skill list and report card).
4. Evidence: evidence/progress-report.md (live batch-09, checked item by item). No-active path on a fresh init-ed temp repo: `status` errors "no running batch" (evidence/no-active.txt); the index `.agents/changes/STATUS.md` does not exist until a lifecycle command like `file` runs, then it shows "No batch" and the backlog table. Observation only: on a repo that was just init-ed, the skill has no index to read for the count; an agent can say 0.

Notes: the old evidence files live-batch-09.txt, live-batch-09-cost-rerun.txt could not be deleted (removal blocked); they are overwritten with a "superseded" line. Current files: status-cost-raw.txt, v-*.txt, batch-STATUS.md, no-active.txt, progress-report.md. PR description not checked, as asked.

## PR description check, PR 96 as posted, head cd4b7cd

NOT VERIFIED.

Clean (renders): OK. Sections in order, fold present with blank lines after `</summary>` and before `</details>`, nothing after it, mermaid and text code blocks closed, title has no internal reference.

Failed claims (pr-template.md rules and audit item 3: no internal reference outside Internal references):
1. Deliverables sample block, outside the fold's Internal references: "Batch 09 (direct mode)", "CR-158 changes-tree-v2", "CR-159 status-command", "batch-09", "6 CRs of 7": CR names, numbers, slugs and a batch name.
2. Summary and Deliverables name agent roles: "the Chief of Staff", "the Griller's", and the file `chief-of-staff.md`; Autonomous decisions: "a Chief of Staff rule", "as for P9". Changes (inside the fold, but not Internal references): `chief-of-staff.md`.
3. Deliverables and Autonomous decisions say "batch `STATUS.md`" and "active batch": batch term outside Internal references.

Consistency with the diff: OK for the claims. Unmentioned minor: `skills/chantier/SKILL.md` description gets a `/chantier:status` mention (router), not in Changes. Otherwise report.md, skills/status/SKILL.md, chief-of-staff.md pointers, version.py, plugin.json, tests, README, CONTRIBUTING, tutorial, both host references all match.

Fix: rewrite the sample with neutral names (no CR/batch ids), reword roles (the orchestrating agent, the grilling command), move names to Internal references, mention the router description line in Changes.

## PR description re-check, PR 96 as reworded

VERIFIED. The earlier failures are gone: no CR number, slug, batch name or agent role outside Internal references (the sample uses "Run 09" and neutral change names); the router description line is now in Changes. Rendering unchanged and clean (fold blank lines, closed blocks, title clean). Summary, Deliverables and Changes match the diff.
