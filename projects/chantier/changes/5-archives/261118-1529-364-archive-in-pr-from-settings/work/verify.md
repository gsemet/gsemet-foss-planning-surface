# Verify CR-364

Head: 7a6f279db67cc7a54ad25a12b67a5f648c0b76a6

All claims judged at 7a6f279 (pushed head = worktree HEAD, tree clean).

1. Code: `Repo._external` gives `archive_in_pr` true only for `yes`; field default False; docstring updated.
   Command: `git diff origin/main...HEAD -- .../core/repo.py .../plugin_files.py`
   Output: `-not (mine and mine[1].lower() == "no")` / `+bool(mine and mine[1].lower() == "yes")`; `archive_in_pr: bool = True` -> `False`. PASS.
2. New parametrized test (6 cases: no file, no line, no, no (comment), yes, Yes) and the external-surface test
   parametrized (no project.md / yes) with one `ship` each. Command (worktree):
   `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_external_archive.py -q` -> `8 passed in 4.74s`. PASS.
3. The tests fail on the old code. Command: same file copied into a detached worktree of origin/main
   (4a49d5c7c782b769887c7fe5a4f120b8ee3271c6), same pytest -> `3 failed, 5 passed` (no file, no line, external-surface
   no-project.md case); log: verifier/evidence/before-tests.log. PASS.
4. `just check` at 7a6f279: `609 passed in 27.87s`, `release-notes ... ok`. PASS (test time within budget).
5. Scenario `other` project drops the line; check relabelled and asserts writes holds only the CR folder
   (diff of scenario/run_scenario.py). Run: pipeline job `just scenario (ubuntu-latest)` green at 7a6f279 (Driver's
   `log` note "all 5 jobs pass", `gh pr checks`); demo keeps `yes`. PASS (not rerun locally; CI is the gate).
6. Matrix: external no line / no (comment) / yes covered by claims 2-3; in-project: `archive_path` returns None when
   `repo.external` is false (unchanged code, `git diff` shows no change there). PASS.
7. Cards/docs edits match the spec: concepts.md, driver.md (writes paragraph, "archive: not in the PR" sentence replaced,
   CI paragraph, CR driver), pr-template.md bullet, planning-modes.md (3 spots), scenario/README.md. `git diff origin/main...HEAD`
   inspected. agents/ untouched. PASS.
8. Change record: commit body of 7a6f279 holds the `Default change:` paragraph (`git log -1 --format=%B`); pr-body.md and the
   posted PR #330 description (`gh pr view 330 --json body`) hold it in the Summary. No CHANGELOG or release-notes folder added. PASS.
9. PR description: renders (sections, table, fold), Summary/Deliverables/Changes match the diff, no images, no role names,
   Known gaps None (no UNVERIFIED claim, no uncaptured evidence). Note: the posted body still has unchecked Test plan boxes and
   `<sha7>` placeholders; the Driver fills them in its final form. Review box to be judged then against the log
   (`r1 approved at ee80f03, committed as 7a6f279`). PASS for now.

VERIFIED

## Description pass (PR 330 body as posted, judged at 7a6f279db67cc7a54ad25a12b67a5f648c0b76a6)

Command: `gh pr view 330 --json body,headRefOid` -> head 7a6f279db67cc7a54ad25a12b67a5f648c0b76a6.
- Renders: sections, table, details fold well formed; no images. PASS.
- Consistent with `git diff --stat main...HEAD` (10 files: repo.py, plugin_files.py docstring, cards, docs, scenario, tests). PASS.
- Proofs name 7a6f279; Known gaps "None" right (no UNVERIFIED, no accepted failure, no STALE). PASS.
- Review box "approved at 7a6f279 (reviewed at ee80f03, committed as 7a6f279)" vs `chantier log CR-364`: "r1 approved at ee80f03, committed as 7a6f279d". PASS.
- Role names: none outside Internal references. PASS.

VERIFIED
