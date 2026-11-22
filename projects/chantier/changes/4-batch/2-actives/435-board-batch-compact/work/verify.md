# CR-435 verify

Head: 6c8cd35b567ad814556b15745a60eb5a1f74343a

Scope: re-verification after the restack (2004e52 -> 6c8cd35). The first pass is kept in work/verifier/verify-2004e52.md.log.

## Claims

1. Title-row tests pass. SHA 6c8cd35b. Command: uv run --no-sync --project . pytest skills/chantier/scripts/cli/tests/test_board_title_row.py skills/chantier/scripts/cli/tests/test_board_design.py -q
   Output: 40 passed in 0.18s. VERIFIED.
2. Layout measured again at 6c8cd35b (demo board, scratch run, removed). Command: uv run --no-project --with "playwright>=1.49" python work/verifier/measure.py <worktree> after <scratch out> <scratch tmp>.
   Output: pc: tabs top 263 (before 353, base 33d1045), figures top 143, scrollWidth 1400; tips mpill and lgpill inViewport true. phone: figures top 176, scrollWidth 375, both tips inViewport true. VERIFIED (same numbers as at 2004e52).
3. Docs pictures retaken (diff HEAD~1 = 11 PNGs + docs_screenshots.py). Opened batch-pc.png, batch-phone.png, panel-pc.png: title row shows "Stack - Foreman" and "States and arrows" pills, hint and Stack/Series/Parallel at right on pc; phone shows both pills on one line, PRs column first as drawn; panel opens on the Kanban tab; paths are made up (shop-api), no username. VERIFIED.
4. Long gate: work/gates/20261122-012724.log first line "gate CR-435 ... head 6c8cd35b567ad814556b15745a60eb5a1f74343a", last line "result: pass at 6c8cd35b567ad814556b15745a60eb5a1f74343a". VERIFIED.
5. CI: gh pr view 408 statusCheckRollup at 6c8cd35b: 5 checks SUCCESS (check x3, scenario, eval-dry-run). VERIFIED.
6. Review box "approved at 6c8cd35 (r2 inspector approved at e499aa7, committed as 6c8cd35)": $CHANTIER log has "r2 approved at e499aa7, committed as 6c8cd35". VERIFIED.
7. PR description: Summary, Deliverables, Changes match the diff; Known gaps present; no stale marks; SHAs carried with reasons. BUT images do not resolve: gh api (Accept: application/vnd.github.full+json) repos/gsemet/chantier/pulls/408 body_html gives <img src="./batch-pc-before.png" ...> (and the 7 other images): relative paths, never attached with `gh pr edit --attach`, so they render broken on the forge. NOT VERIFIED.

## Verdict

NOT VERIFIED (claim 7: the description's images are not uploaded).
