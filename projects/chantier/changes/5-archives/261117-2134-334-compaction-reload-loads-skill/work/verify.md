# Verify CR-334

Head: 6cb7984413b39a8aa03bb2e19f36fe536d8a52ae

All claims judged at 6cb7984 (full SHA above).

- `just check` at the head, detached worktree: exit 0, "455 passed", release-notes ok (work/verifier-check.log). 6cb7984.
- `just mod` at the head: exit 0, "65 pass, 0 fail" (work/verifier-mod.log). 6cb7984.
- Three compaction messages: `git diff <base> HEAD -- hooks/register.tsx` shows `reloadLine(role)` producing exactly the spec's three lines (Chief of Staff, Griller, router); test constants TAIL/RELOAD equal them. 6cb7984.
- Roles move-to-end: diff shows `[...list.filter(n => n !== name), name]`; hook picks last non-`chantier`, else `chantier`; tag roles-1 unchanged. 6cb7984.
- Tests: chief-of-staff for auto and manual (toBe cos line); three generated role-choice cases (chantier,griller; griller,cos,griller; chantier) with not.toContain('chantier:'). Pass in just mod. 6cb7984.
- Card edits (diff read): three SKILL.md reload sentences + router delegation + descriptions; session-start "5. Reload" seat-first, no uv sync; claude-code.md skills row and "Reload after a compaction"; copilot.md line; README line; types doc comment. Wording shortened for the 12288-byte limit, disclosed in pr-body Autonomous decisions and Known gaps; meaning kept (dropped: explicit rename and "take no seat" clauses, "take" stays forbidden). 6cb7984.
- CI: `gh pr checks 293`: check (macos, ubuntu, windows), eval-dry-run, scenario (ubuntu) all pass. 6cb7984.
- PR description (work/pr-body.md): renders, Summary/Deliverables/Changes match the diff, Known gaps lists the unproved real-session behaviour and the shortened wording; no images. Test plan SHAs are placeholders for the Driver.

VERIFIED
