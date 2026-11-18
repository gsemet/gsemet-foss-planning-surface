# Verify CR-330

Head: 54cd5a41cd575e82a3ee179a7e5291f28761680f

All claims judged at 54cd5a4 by `git diff chantier/batch-24/cr-326-cr HEAD` (6 files, 43+/9-) and rg.

1. driver.md has the "Before the first push" bullet (fast gate again at rebased head + rules' pre-push checks, own commands, never `gate`, failure = round, note format, nothing-to-run case, three push paths, not a third gate): present in the diff at "Your means". VERIFIED
2. "CR driver" sequence: `rebase, the checks before the first push (see "Your means"), the long gate ... push`, and the `ci: beside the long gate` variant `rebase, the checks before the first push, push`: present in the diff. VERIFIED
3. No project command in new driver.md text: `git diff ... -- driver.md | grep '^+' | grep -n -E "just |eval-dry-run"` -> no output, rc=1. VERIFIED
4. Checklist in the Coder's prompt only, `--note` stays the one-line brief, round 2+ carries open/unmarked/sent-back items, no files -> none, Inspector/Verifier read the spec: in the diff at the reading rule and the round step. VERIFIED
5. coder.md: `r<n>.md` marks each item `done` or `open: <why>`, checklist never in the reply; the reply template (`rg -n "Reply with this template" -A12`) is unchanged, ten-line cap kept. VERIFIED
6. docs/gates.md and init.md: fast gate runs again before first push; extra pre-push check may be named; example line given; `rg -n -i "third gate|three gates"` on both -> no output. VERIFIED
7. AGENTS.md: `just check` before first push; `just eval-dry-run` for `src/` or `evals/kit/`; cards-only not owed; "before you hand back" bullet kept. CONTRIBUTING.md agrees and keeps its two lines. VERIFIED
8. Not touched: diff stat lists only AGENTS.md, CONTRIBUTING.md, docs/gates.md, coder.md, driver.md, init.md; no CLI, agents/ or inspector/verifier card. VERIFIED
9. Dogfooding: `$CHANTIER log CR-330` shows notes "before first push at 54cd5a4: just check: pass" and "just eval-dry-run: pass, 17 of 17 cases as expected on Windows". VERIFIED (Driver's notes; I did not rerun the commands, the diff is docs/cards only, CI green).
10. Review box `approved at 54cd5a4`: log note "r1 approved at de0993f..., committed as 54cd5a4" matches. VERIFIED
11. PR description on the forge (`gh pr view 288 --json body`): renders, headRefOid is 54cd5a4, Summary/Deliverables/Changes match the diff, no images, no STALE mark, Known gaps lists the UNVERIFIED table and the untested-in-batch gap. The `**UNVERIFIED:**` mark and the `Verified at <sha7>` / `CI green at <sha7>` boxes are the Driver's to update after this verdict. VERIFIED
12. Evidence pairs: none (docs/cards only); see verifier/evidence/before-after.md.

## Description-only pass (re-run at 54cd5a41cd575e82a3ee179a7e5291f28761680f)

Command: `gh pr view 288 --json body -q .body`, `gh pr view 288 --json headRefOid` -> 54cd5a41cd575e82a3ee179a7e5291f28761680f; `git diff --stat chantier/batch-24/cr-326-cr HEAD` -> 6 files, 43+/9-.
Description renders (sections, table, fold), no images, no STALE mark. Changes list matches the six files of the diff, nothing delivered unmentioned. Role names are product terms of a change to those cards. Known gaps holds the one untested-in-batch gap; no UNVERIFIED claim or missing evidence pair exists. Review box `approved at 54cd5a4` matches the log note (claim 10). Proofs name 54cd5a4.
Verdict: VERIFIED
