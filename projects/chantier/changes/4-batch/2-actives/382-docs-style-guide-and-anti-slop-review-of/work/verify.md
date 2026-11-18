Head: 787400ea5f95752e6383e7e54878cc23b3fffba7

# CR-382 verification at 787400e

1. `just check` (UV_PYTHON=3.13) at 787400e: "All checks passed!", "649 passed in 32.97s", docs build succeeded with -W. Log: verifier/check.log. CI `gh pr checks 347`: 5 checks pass (3x just check, eval-dry-run, scenario). PASS.
2. Pages: built HTML has 21 pages (find on docs/_build/html, minus genindex/search); 22 .md under docs minus demo/release-notes/texts includes STYLE.md (excluded). review-table.md has 21 page rows plus a 22nd row "reference/web-board.md (images)" which is not a page, and its title says "22 site pages". Every page of the spec's list is in it. The PR body says 21. FAIL (minor): the table's title and last row are wrong.
3. `chantier rules` run from the worktree (with and without --project) resolves its root to the main checkout (main's AGENTS.md, old paths docs/use-cases-direct.md, docs/release-process.md), so it shows main, not the head. Its output lists no docs/STYLE.md. At the head, the test's `linked()` walk on the worktree's AGENTS.md (depth 2) leaves no docs/STYLE.md in `seen` (test passes). PASS, with that limit stated.
4. `pytest test_docs_site.py -k style_guide` at head: "1 passed". With AGENTS.md's backticked path replaced by a Markdown link: "1 failed ... AssertionError: AGENTS.md does not name `docs/STYLE.md`"; reverted with git checkout, tree clean. PASS. (The test lives in test_docs_site.py, not test_plugin_files.py as the spec says; the PR names this under Autonomous decisions.)
5. Screenshots verifier/evidence/gates-before.png (base 22519166) and gates-after.png (head), opened: after shows a one-line opening and sections; before the restated subtitle and 50-word bullets. No username or home path visible. PASS.
6. `git diff --name-status base..head`: only M, plus A docs/STYLE.md; no D, R or image. PASS.
7. STYLE.md is 69 lines, S1-S16 cover every listed rule. AGENTS.md:93 and CONTRIBUTING.md:176,256 use backticks, no link; conf.py excludes STYLE.md. PASS.
8. Review box: log shows "r1 approved at 22519166, committed as 787400ea". PASS.
9. PR description (forge body at 787400e): FAIL. It says "21 pages reviewed ... (table below)" and "Review table: see the Details section", but no review table is in the body; the spec requires it quoted there. Known gaps says the screenshots are "not attached yet": they are captured now (evidence) but not attached; update when attached.
10. Read the Docs preview: not a listed check, not run; no RTD check appears on the PR.

(pass 1: NOT VERIFIED, superseded below)

## Pass 2 at 787400ea5f95752e6383e7e54878cc23b3fffba7 (head unchanged; claims 1, 3-8, 10 carried from pass 1, same head)

2. review-table.md: `grep -c '^| [a-z]'` gives 21 rows, title says 21 site pages; `find docs -name '*.md'` minus demo, release-notes, texts, STYLE, _build gives 21. PASS.
9. Forge body (`gh pr view 347 --json body`, headRefOid 787400e): the review table (21 rows) is quoted under Changes; Deliverables embeds two images; `curl -sL` on both user-attachments URLs gives 200 image/png, 156637 and 166942 bytes, equal to gates-before.png and gates-after.png sizes. Opened gates-after.png: one-line opening, short sections, no username or home path. Known gaps lists the planning-modes/planning-folder contradiction and the missing RTD preview; no UNVERIFIED claim remains. SHAs named (2251916, 787400e) are base and head. PASS.

VERIFIED

## Description pass at 787400ea5f95752e6383e7e54878cc23b3fffba7
PR 347 description checked: matches diff (27 files, STYLE.md 69 lines, 16 rules S1-S16, conf.py exclude, AGENTS/CONTRIBUTING wiring, test), images on user-attachments, Verified box ticked at 787400e, 5 checks SUCCESS, internal refs only under Internal references. VERIFIED.
