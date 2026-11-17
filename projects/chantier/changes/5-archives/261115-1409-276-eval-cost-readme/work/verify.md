# Verify CR-276

Head: d7baadd20bab0143a4e666597b7c14fdf788c34c

All claims judged at d7baadd (full SHA above).

1. `just check` passes. Command: `just check` in the worktree. Output tail: "All checks passed! ... Success: no issues found in 164 source files ... 190 passed in 43.96s ... release-notes ... ok". The relative-link test covers docs/costs.md.
2. The diff touches README.md only. Command: `git diff --name-only origin/main...HEAD`. Output: `README.md`. `git status --short` is empty.
3. Reading check on the section `## What a batch costs` (git diff origin/main...HEAD -- README.md):
   - Table rows match the spec exactly: $10.28; $11.52 ($11.91 once closed); $2.10 (20%); $3.39 (30%); about $4.67; $0.05; about $14.6-15.0; about $11.5-11.9.
   - Lists match: over 60%, coding 7-8%, about 70k tokens, $2.10 against $3.39, about $3 more all in; about 200k tokens context line.
   - Plain words: "one run each", "No general conclusion that a Foreman is cheaper or dearer than direct mode".
   - Names `chantier cost`, `chantier cost --by cr`, `chantier cost --explain`; links [Costs and budgets](https://github.com/gsemet/chantier/blob/main/docs/costs.md); asks "what did it cost?".
   - Command: grep for local paths, session ids, names over the section lines: output NO_MATCH.
4. PR description (pr-body.md, equal to posted head d7baadd per `gh pr view 226 --json headRefOid`): Summary, Deliverables and Changes match the diff (one new section, README only); table identical; Known gaps "None" is consistent (no UNVERIFIED claim; evidence none, docs-only per plan). Review box "approved at d7baadd": the driver note in `chantier log` says "r1 approved at 9d4136c, committed as d7baadd", which matches.
5. Evidence plan docs-only: no before/after captured (nothing to show); no long gate needed per AGENTS.md.

VERIFIED

## Description pass (posted PR 226 body, judged at d7baadd20bab0143a4e666597b7c14fdf788c34c)

Commands: `gh pr view 226 --json headRefOid,body`; `git diff main...HEAD -- README.md`; `grep -n '^## ' README.md`.
- headRefOid equals the worktree HEAD d7baadd. Section sits at README.md line 116, between "Batch modes" (84) and "Change Requests Lifecycle" (159): as claimed.
- Table in the body is identical to the README's; figures match. Content lists match the diff (frame sentence, table, shows, does not show, measuring, costs.md link). Diff is README.md only, 43 insertions: "no other edit" true.
- Known gaps "None": no UNVERIFIED claim, evidence none by plan. Review box d7baadd matches the driver note (committed as d7baadd). CR-276 appears only under Internal references. Renders: sections, table, details fold, no images.
VERIFIED
