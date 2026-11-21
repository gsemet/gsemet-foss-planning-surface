# Verify CR-420

Head: ca5a4a4d76352b74edad94782e16384f1049da0e

Quiet-machine window: no `just check`, `just test`, pytest, scenario or eval-dry-run was run. Proof is read-only (a Python read of the shipped files, grep, git, gh).

## Claims

1. Byte limits hold on the shipped card (LF bytes, opening plus sections) - ca5a4a4 - VERIFIED
   Command: python -I script splitting driver.md at `## `, summing opening and the manifest's sections.
   Output: opening 2475 (<=2500); first coder 16224 (<=18000); whole common path 35410 (<=36000); resume-closing restart 9435 (<=13000); "Means: a Driver started again" 1412 (<=2000). Matches the PR body figures.
2. Manifest lines resolve, share no reading, one `CR driver: ...` section each - ca5a4a4 - VERIFIED
   Same script: shared readings 0; CR driver sections in the three lines: CR driver, CR driver: ship and proof, CR driver: the closing (file order matches spec); stack/qa/release lines: no unresolved heading. `git diff 4ed0d56c..HEAD -- startup-manifest.json` equals the spec's three lines, other Drivers only swap worktree/rebase.
3. Threshold 115,000 in four places, 100,000 in none - ca5a4a4 - VERIFIED
   `grep -n "100,000" driver.md foreman.md`: no output. `grep -n "115,000"`: driver.md 113, 301, 860, 877; foreman.md 764. Scenario diff reads `"115,000 tokens" in flat_driver and "100,000 tokens" not in flat_driver/flat_foreman` (the scenario itself not run here: UNVERIFIED locally; CI `just scenario (ubuntu-latest)` SUCCESS at ca5a4a4 per `gh pr view 390`).
4. Every quoted section link resolves - ca5a4a4 - VERIFIED
   Script over driver.md, foreman.md, concepts.md, hosts/*.md: "checked 76 unresolved 0". `grep -rn "worktree, rebase and push"` over skills, docs, scenario, agents: nothing.
5. concepts.md level-3 headings, text unchanged - ca5a4a4 - VERIFIED
   `grep -n "^## \|^###"`: Starting an agent (466) then The agent and the model, The prompt, The Chief of Staff's subagents, An agent that ends before its part is done, The specification's agents and the Retro critic, A Driver's prompt. Diff shows only added headings and the bold lead-in turned into one.
6. Agent files and CLI src untouched - ca5a4a4 - VERIFIED
   `git diff --stat 4ed0d56c..HEAD -- agents com.github.copilot skills/chantier/scripts/cli/src`: empty.
7. Tests as specified (parametrized 3 cases, opening limit, line checks, MOVED_IN row) - ca5a4a4 - VERIFIED by diff reading; passing run UNVERIFIED locally (not run, quiet window); CI check x3 SUCCESS at ca5a4a4.
8. No rule dropped (spec claim 4) - UNVERIFIED by me: the Inspector's and Coder's `r<n>.md` moves tables are not proof, and a section-by-section comparison of a 709-line diff was not redone here.
9. PR description consistent with the diff, clean, no image - ca5a4a4 - VERIFIED. Known gaps names the unverified real-Driver effect.
10. Review box `Review: approved at ca5a4a4` - ca5a4a4 - VERIFIED
   `chantier log CR-420` line 28: `2026-11-20T23:59:20Z driver note note=r4 approved at ca5a4a4d76352b74edad94782e16384f1049da0e (inspector APPROVE on the test-only split commit ca5a4a4 ...)`. HEAD is still ca5a4a4d76352b74edad94782e16384f1049da0e (`git rev-parse HEAD`). Earlier NOT VERIFIED on this claim is cleared.

## Verdict

VERIFIED (all claims proved or marked UNVERIFIED for the quiet window: tests and scenario not run locally, CI green at the head; "no rule dropped" not re-checked section by section).
