# Verify CR-425

Head: 66d9b1ca28a4220691648132d851a2c943fd8982

All claims judged at 66d9b1c (pushed head, `git rev-parse HEAD` in the worktree; `gh pr view 398` headRefOid is the same).

1. Tests at the head: `uv run --no-sync --project . pytest test_running_batch test_batch_end test_open_empty_batch test_came_back test_opening_and_restore test_open_no_clone -q` -> `55 passed in 35.20s`. They cover the mark (written, refused ungrilled/3-ready/no batch, cleared by other destinations, stale), `open --factory` and `order factory on` refused (exit usage), no `factory` key or `Factory:` token on `open`, old record with `"factory": true` and a done `factory` order: `status` prints no factory word and `close` is not refused, the ordinary `next:` line, and the web files' absence of the factory words.
2. `uv run --no-sync --project . chantier open --factory` -> `chantier: error: unrecognized arguments: --factory`.
3. No factory text left: `git grep` for `factory (mode|batch|on|off)|--factory|factory:|order factory|#factory-mode|steeringFactory|no_cr_yet_factory|factory_on` (release notes, eval and scenario results excluded) leaves only plugin descriptions ("Software Factory"), the scenario/tests that assert its absence or refusal. `commands/factory.py` is deleted (diff stat); `BatchRecord.factory` gone from `core/records.py`.
4. README: `## Running batch or next batch` at line 119; the three use-case docs link `../README.md#running-batch-or-next-batch`; the release notes keep their pinned v0.14.0 link.
5. Cards: `chief-of-staff.md`, `griller.md` carry `--running-batch`, the `Destination:` recording; no factory word in `skills/chantier/references`.
6. Gates: `work/check.log` (just check) and `work/dry.log` (`dry run: 18 of 18 cases as expected`, exit 0) at the Driver's head; CI green at this head per the brief (check x3, eval-dry-run, scenario ubuntu). Carried as the Driver's, not rerun by me.
7. PR description: posted body equals `work/pr-body.md` (one trailing blank line); renders, sections present; Summary/Deliverables/Changes match the diff (48 files: cards, CLI, web client, docs, scenario, tests); no image. Known gaps lists the scenario/Windows gate as UNVERIFIED; the Windows `chantier gate` is owed by AGENTS.md when this CR is on top.

Not proved by me: the full scenario locally and the Windows gate (named in Known gaps).

VERIFIED

## Description pass (PR 398 body, judged at 66d9b1ca28a4220691648132d851a2c943fd8982)

Command: `gh pr view 398 --repo gsemet/chantier --json body -q .body`; compared with `git diff --stat origin/main...HEAD` (48 files) and pr-template.md.

- Renders: sections in order, one `<details>` fold with blank lines after `</summary>` and before `</details>`, nothing after it. No image attached.
- Consistent with the diff: Deliverables names (`triage --running-batch`, `order add --note`, `lifecycle/running_batch.py`, `commands/factory.py` deleted, `BatchRecord.factory`) match the diff stat; cards, docs, web client, tests and scenario all listed.
- No internal reference outside Internal references; "spec-writer" is a product term of a change to that card.
- Proofs name `66d9b1c`; Known gaps holds the UNVERIFIED Windows scenario bullet.
- Note: the Test plan has no Review or Verified item (template lists them); no Review box to judge.

VERIFIED (description)
