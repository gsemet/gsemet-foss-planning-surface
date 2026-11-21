# Verify description CR-408

Head: cd99f0a7ed1ff0d66e917a29429c7c3936e1bb47

Judged at cd99f0a (gh pr view 382: headRefOid cd99f0a7ed1ff0d66e917a29429c7c3936e1bb47; body read with `gh pr view 382 --json body`).

1. Layout per pr-template audit: Summary, Deliverables, Blast radius (grade 1), Autonomous decisions, Known gaps visible in order; one Details fold with Changes, Human decisions, Impacts, Test plan, Internal references; blank lines after summary and before details; nothing after. No Issues References (no `issue:` line expected). Pass.
2. Diff match (`git diff --stat origin/main...HEAD`, 16 files): every file is named in Changes, Autonomous decisions or Deliverables (access.py x2, cli.py, take_checks, driver.py take change, leases drop mode, writer/lines, autostart + seat holds_seat, five cards, AGENTS.md, test_access.py). Nothing claimed missing. `--epoch` option exists in commands/access.py; chief-of-staff.md diff shows the `access` exception named. Pass.
3. Proof SHAs: all Test plan items cite cd99f0a (the head). Test count 38 matches verify.md; 72 s run and 10.6 s / 3.8 s timings are in work/gates/check-r1.log and work/coder/r1.md. Review item: log note "r2 approved at 9841318..., committed as cd99f0a7" proves Review at cd99f0a. CI note at cd99f0a: all 5 jobs pass. Pass.
4. Known gaps: timing gap and missing release-branch case declared; no UNVERIFIED or STALE mark in the body; no failed claim accepted. Pass.
5. Internal references: the CR name and the planning-server split appear only in Internal references; role names (Chief of Staff, Foreman... cards) are product terms of a change to those cards; no doer role, no batch/round/path outside the last section. Pass.
6. Images: none attached. Pass.

VERIFIED
