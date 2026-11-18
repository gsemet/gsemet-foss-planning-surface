Head: 4833e30c8afe3e9f4bdb0338ea5c461d041263b2

# CR-367 verification (all judged at 4833e30c)

1. New tests fail on the base, pass on the head. Command: `uv run --no-sync --project <checkout> python -m pytest tests/test_batch_end.py test_board_prs_release.py test_external_archive.py test_board_prs.py test_forge_hub.py -q`.
   Base (main checkout, HEAD 380eca4f, head's tests): `4 failed, 65 passed` (the release-PR cases: handoff/status/STATUS.json, stack line, board prs why_not, delivery.md `- PR: none`).
   Head: `69 passed in 31.84s`. test_forge_hub and test_board_prs pass unchanged. PASS.
2. Real CLI flow, scratch project (own git repo, `open`, `foreman set`, record patched only to make CR-101 a ready release CR with a PR, then real `order merged`). PASS:
   - before merge: `PR: https://example.com/pr/1;`
   - after `order merged CR-102` then `CR-101`: `handoff CR-101` -> `PR: https://example.com/pr/1 (merged);`
   - `status` row: `CR-101 queued r0/3 https://example.com/pr/1 | ...` (plain link)
   - STATUS.json `"pr": {"url": "https://example.com/pr/1", "number": 1}`; STATUS.md `[PR](https://example.com/pr/1)`
   - record: `pr None, merged_pr https://example.com/pr/1`; `release go CR-101` -> `go: merged (the release PR https://example.com/pr/1 was merged)`.
   - merged_pr "the release PR" (record patched): `handoff` -> `PR: none;`, `status` shows `-` in the PR column. The STATUS.json null case was not re-seen by hand (the file was not rewritten after my patch); it is covered by the passing parametrized test (`pr` null asserted, claim 1).
3. Board (not served: no background shell allowed; I called the board's own `project_state` on the scratch batch, the data `/api` serves, then node on the head's semantics.js; evidence/board-rows.json, board-lists.log). PASS:
   - rows: CR-101 `state queued, pr .../pr/1, pr_merged true`; CR-102 `state ready, pr .../pr/2, pr_merged false`.
   - home open PRs `['CR-102']`, PRs nav count `1`, mergeOrder `['CR-102']`; cards with a PR: both (CR-101 still shows its link). Old filter would list both.
   - Not seen: the rendered page (home-prs.js and registry.js diffs read, they only call `openPr`).
4. Pane screenshot: none from a real session; named in the PR's Known gaps. Not a fail.
5. PR description vs diff: Summary, Deliverables (shown_pr, reader table, pr_merged), Changes list (records, facts, batch_status, views, steps, stages, history, board/crs, board/prs, js, 3 test files) match the 15 files of `git diff main...HEAD`. Autonomous decision on cancelled CRs is accurate (CLOSED = merged, cancelled). Known gaps lists the screenshot and no JS test. No image, no role name misused. Test-plan boxes keep `<sha7>` placeholders for the Driver. PASS.
6. Not run by me: `just check`, scenario, CI (the Driver's gates).

VERIFIED

## Description pass at 4833e30c8afe3e9f4bdb0338ea5c461d041263b2

Head: 4833e30c8afe3e9f4bdb0338ea5c461d041263b2

- Posted body (gh pr view 332 --json body, head 4833e30) equals work/pr-body.md (normalized compare: SAME).
- Diff file list (git diff main...HEAD --stat, 15 files) matches the Changes section; Summary/Deliverables match.
- 4 failed/65 passed at 380eca4 and 69 passed at 4833e30: in verifier/evidence/before-after.md.
- Gates: log note "just check: pass; just eval-dry-run: pass (17 of 17)" at 4833e30.
- CI: statusCheckRollup, 5 jobs SUCCESS at 4833e30.
- Review box: log note "approved at 380eca4..., committed as 4833e30" matches the box.
- Internal reference only under Internal references; Known gaps (no pane screenshot, no JS test) right.

VERIFIED
