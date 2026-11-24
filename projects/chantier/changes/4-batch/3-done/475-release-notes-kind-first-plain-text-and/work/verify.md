# Verify CR-475

Head: 6773a4db1531fe98bf934a8c0e80a10c1322ca16

All claims judged at 6773a4d.

- Structure test passes, reads shipped files: `python -m pytest test_release_template_card.py test_startup_manifest.py -q` -> `53 passed`. Base template has 0 matches for `**restore**|Known issue:` (the test's claims fail on the old text).
- Bullet found in `driver-pr-extras.md` (moved by CR-471), exception added; the test finds it by text.
- Gone sentences: `grep -c "the highlight says so in one line\|cannot crop stays whole" release-template.md` -> 0.
- Not touched: `git diff origin/main...HEAD --stat -- startup-manifest.json agents com.github.copilot` -> empty; diff stat lists only the 4 expected files.
- Four doc lines of docs/release-process.md: diff read, matches section 4 (h1 X.Y.Z, kind-first line, highlight heading, known issues out of contributors + Bad news line).
- Card content (kinds, order, Fixed/Removed/Changed/Known issue, budgets, ten questions, banned table, image protocol Q2/Q5/Q10/Q12): diff read against spec sections 1-2, all present.
- `just check` in worktree: `2416 passed, 20 skipped`; `release-notes: ... ok`.
- Review box: `chantier log 475` shows `r3 approved at a94085d3..., committed as 6773a4db`: proves the box.
- PR body (pr-body.md) read against the template: Summary/Deliverables match the diff, no image, Known gaps names the long gate; reading check present (subtitle 11 words, Fixed/Restored/Known issue lines, ten answers). Minor note: the subtitle names "bug-fix" though the situation holds a restore, which the card's order would name first; the spec itself calls it a fix release, so not failed.
- CI at head: all five jobs pending when checked (`gh pr checks 451`); the long gate is not yet proved by me.

VERIFIED
