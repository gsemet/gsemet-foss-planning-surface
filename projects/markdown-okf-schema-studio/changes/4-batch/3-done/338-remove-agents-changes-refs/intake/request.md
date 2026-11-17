Remove the Studio repository's remaining references to `.agents/changes/`, now that its change requests live in the planning surface. One PR, draft until CI is green; the owner merges by rebase.

Sent on the owner's behalf by the OKF Studio Chief of Staff session ([Mac], 2026-11-17), the mission order the owner announced earlier in this session.

Context:
- PR #405, merged (16105e0f): AGENTS.md has a `## chantier` section with `- planning: https://github.com/gsemet/gsemet-foss-planning-surface, projects/markdown-okf-schema-studio`, and "Process" names the planning folder instead of `.agents/changes/`.
- In the surface (main, pushed): the Studio CRs are migrated to chantier 0.11's layout (29486f6): stages 1-inbox, 2-backlog/P1..P4, 3-ready, 4-batch/{1-pending,2-actives,3-done}, 5-archives, 6-trash; in a CR folder intake/, 01-intent.md, 02-answers.md, 03-change-spec.md, summary.json, evidence/, experiments/, prototypes/, work/ (rules, tasks, rounds, reports, reviews, PR bodies), and an archive's delivery.md. The old names 3-requests, 4-archives, 5-trash are gone. `just validate` there runs `chantier summary lint`.

References left on main (grep -rn '\.agents/changes'):
- .agents/guidelines/change-requests-lifecycle.guidelines.md (9)
- .agents/guidelines/pull-request.guidelines.md (2)
- .agents/guidelines/owner-review.guidelines.md (1)
- docs/demo-video/guidelines/short-demo-process.guidelines.md (1)
- .agents/skills/markdown-studio-exploratory-qa-claude/: SKILL.md (5), references/harness-pitfalls.md (1), references/charters.md (1), scripts/new-features.py (1), scripts/coverage-map.py (2)
- justfile:188-189, the `orchestrator` recipe (CHANGES=".agents/changes", writes 3-requests/ORCHESTRATOR.md), and scripts/generate_orchestrator.py (1). Decide with the owner whether the generator still has a use now that chantier keeps the batch state; if not, remove both.

Point each reference to the planning folder named by AGENTS.md's `planning:` line (the surface's projects/markdown-okf-schema-studio/changes/), with the new stage and file names; where a rule describes the old lifecycle that chantier now runs, say so rather than keep the old steps. Rules: the project's constitution and AGENTS.md (commit guideline, PR template, just preflight before calling it done).
