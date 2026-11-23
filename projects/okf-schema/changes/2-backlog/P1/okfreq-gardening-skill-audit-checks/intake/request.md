# okfreq-gardening: audit what markers and links mean, not only that they exist

Owner's request (2026-11-17), from the requirements gardening of markdown-okf-schema-studio (CR requirements-gardening in projects/markdown-okf-schema-studio/changes, evidence/audit-synthesis.md and the six audit-*.md reports). That audit found many defects that okfreq's numbers (99.8% source, 100% test links) and the current skills/okfreq-gardening/SKILL.md do not ask to look for. The improvements below are generic; project-specific rules (Studio's Main paths, its diagram section and site) stay in that project's guideline.

Add to the gardening skill:
1. Marker placement: flag marker blocks in file headers, comments listing many IDs, companion files that list IDs attached to no test, one declaration carrying many unrelated IDs, and markers on a test that checks another requirement.
2. Tests against scenarios: for each SwRS, compare the marked tests with its GIVEN-WHEN-THEN scenarios (nominal, boundary, refusal) and list scenarios no test checks; list real tests cited in verification notes that carry no marker.
3. Parent fit: check that each SwRS derives from the use case it serves; a shared rule derived by many StRS should be cited with depends_on instead.
4. StRS consistency: StRS text that contradicts its SwRS or the code (counts, settings, known issues already fixed); an approved StRS is only reported, its fix needs the owner.
5. Missing StRS: compare the in-force StRS with the product surface (commands, settings, docs, release notes, e2e groups) and report use cases with no StRS and umbrella StRS.
6. Human readability of StRS: length, and an optional diagram where the project defines one.
7. Large bundles: a read-only audit fanned out by scope to sub-agents with one shared brief and one table per StRS, then a synthesis, before any change.

Question for okfreq itself: Studio's SwRS-MDOKFSTUDIO-DIAG-128 (in force, not exempt) had no @implements_req and no check failed. Find whether okfreq can already fail on a non-exempt SwRS with no source or test marker (and on marker-block patterns); if not, add an option to lint/validate, documented in the skill.

After an okf-schema release, markdown-okf-schema-studio refreshes its copy at .agents/skills/okfreq-gardening/ (it is already one line behind: approved_on vs approved_at).
