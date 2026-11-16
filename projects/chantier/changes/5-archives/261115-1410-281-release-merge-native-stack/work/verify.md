Head: 37fa1409807bbf3e86429e6bf1b720b64abcf9bc

Judged at 37fa140 (full SHA above), worktree clean (`git status --porcelain` empty).

1. New samples matched by their rules, P10 names merge-async (release and fixes).
   Command: `python -m pytest tests/test_cli_runs.py -q` in skills/chantier/scripts/cli. Output: `12 passed in 11.84s`.
   The diff (`git diff origin/main`) shows: 3 SAMPLES per capability (release, fixes) in permissions.py, a RECOMMENDED_ALLOW exclusion assert,
   and P10 asserts for `--autonomous-releases 1` and `--grant-fixes` naming `gh api -X PUT repos/*/pulls/*/merge-async*`. Host table test (rules per capability = SAMPLES) passes.
2. Scenario step: scenario/run_scenario.py checks the merge-async rule in the P10 release line; CI `just scenario (ubuntu-latest)` pass at 37fa140.
3. Cards vs spec: foreman.md "Merging on GitHub" has steps 1-4 as spec (stacks read, no stack -> gh pr merge --match-head-commit, open PRs below -> ask and no merge, lowest -> merge-async PUT with sha, merged/pending/other handling, state read before retry). concepts.md rule 8 second named exception (single sleep <= 30 s, once per merge) and Words sentence added; chief-of-staff.md refers without repeating commands; claude-code.md rows, Auto mode bullet updated; unproved mark in foreman.md (Copilot included) and host table. GitLab unchanged. Matches spec.
4. CI: `gh pr checks 227`: just check (macos, ubuntu, windows), eval-dry-run, scenario (ubuntu) all pass at 37fa140.
5. PR description: posted body equals work/pr-body.md (differs by a trailing newline only); Summary/Deliverables/Changes match the diff (7 files); Known gaps names the unproved route (02-answers.md accepts: no live trial). Test-plan boxes carry `<sha7>` placeholders as the template. No screenshot rule applies (no pane change).
6. Review note: `chantier log 281`: "r1 approved at 9d4136c, committed as 37fa140" (inspector approved at 9d4136c29...).
Note: the ship line says no local long gate passed at 37fa140; the CI scenario job is green; the Windows local `chantier gate` for the top-of-stack CR is a pre-merge step (AGENTS.md), not a verifier claim. The route stays unproved by an agent, as accepted.

VERIFIED

## Description pass (head 37fa1409807bbf3e86429e6bf1b720b64abcf9bc, unchanged)
Command: `gh pr view 227 --json body,headRefOid`; `git diff --stat origin/main...HEAD` (7 files).
- Posted body: sections render (mermaid, table, details fold); Changes lists exactly the 7 files of the diff.
- Test plan SHAs all `37fa140` = head; "190 tests" matches gate note (`just check` pass, 190 tests); review note `approved at 9d4136c, committed as 37fa140` per `chantier log`.
- "Proof by use" claim backed by `evals/results/real-foreman-2026-11-15-run2.md` lines 64-91 (merge-async route merged the stack).
- Internal references hold only CR-281; no role doer outside it (foreman.md / chief-of-staff.md are product files of the change).
- Known gaps: unproved route and no harmless trial named; no UNVERIFIED claim or missing evidence pair otherwise.
Description pass: VERIFIED
