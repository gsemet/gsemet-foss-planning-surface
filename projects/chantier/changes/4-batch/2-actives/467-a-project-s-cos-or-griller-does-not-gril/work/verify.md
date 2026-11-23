# Verify CR-467

Head: 0ec62a92f29463f173260fa69d1607ea7f508995

All claims judged at 0ec62a92 (worktree HEAD = pushed head).

1. session-start.md "2. The seat and the role" holds the paragraph, opening verbatim and "waits for that project's own Chief of Staff or Griller" (session-start.md lines 60-66, read with sed). PASS.
2. chief-of-staff.md "Backlog and grill" holds "Another project's CR." paragraph (lines 276-292): relay with --project, file line unchanged and not followed, the one-line phrase, nothing more (no 01-intent.md, no summary set), exception to summary rule, user's word lifts grill/spec/triage, launches outside. "Never" bullet at line 2250. PASS.
3. griller.md: Never line with the verbatim board parenthesis (lines 67-71) and the summary-paragraph exception (lines 44-45). PASS.
4. Five MOVED_IN entries in test_startup_manifest.py (OWN_PROJECT x3, CRS_A+CRS_B, RUN_WORD, lines 331-350). PASS.
5. `uv run --project . python -m pytest skills/chantier/scripts/cli/tests/test_startup_manifest.py -q` -> `46 passed in 0.67s`. PASS.
6. "Started from the board" unchanged: `git diff origin/main...HEAD -- skills/chantier/references/griller.md | grep -c "^[-+].*Started from"` -> 0. PASS.
7. No CLI src change: `git diff --name-only origin/main...HEAD -- skills/chantier/scripts/cli/src | wc -l` -> 0. Diff stat: 4 files (3 cards, 1 test). PASS.
8. CI at head (`gh pr checks 444`): check macos/ubuntu/windows, eval-dry-run, scenario ubuntu all pass. PASS.
9. PR description (`gh pr view 444 --json body`): FAIL. Known gaps says "None", but the local Windows long gate failed twice on surface-board webui (unrelated, accepted, not fixed): that accepted failure needs its bullet. The Test plan lines also still carry unfilled `<sha7>` placeholders.

NOT VERIFIED (description only; the cards, the tests and the CI claims are proved).
