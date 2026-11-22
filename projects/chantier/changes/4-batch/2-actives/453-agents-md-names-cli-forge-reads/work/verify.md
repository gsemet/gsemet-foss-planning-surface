# Verify CR-453

Head: 88904189072602202fe74bfedba88f0394e9200d

All claims judged at 8890418 (worktree HEAD = PR 425 headRefOid, `gh pr view 425`). Gate: CI green at this head (check x3, eval-dry-run, scenario) per the Driver; text-only change, no gate run by me.

1. Spec sections 1-5 applied. `git diff main...HEAD -U0` shows: AGENTS.md no-setup clause and scope clause ("but for the forge calls named below") and the new named-exception paragraph placed before "The surface server's writer" with the spec's text; CONTRIBUTING.md two edits; README Install addition; concepts.md; driver.md twice ("The CLI reads no CI"); the three docstrings (commands/__init__.py, forge_base.py, moveout.py). Wording matches the spec. `git diff --check main...HEAD` prints nothing (clean). 8 files, 27 insertions, 15 deletions; no code line changed.
2. Inventory check: `rg -n '"gh"|"glab"|connectors\.read\(|stacked_read\(|read_state\(|read_base\(|pr_state\(|\bgh\(|\bglab\(' .../src/chantier --glob '!clients/**'` hits only: connectors/github.py, gitlab.py, hub/cycle.py (rows 1-2), commands/delivery.py (row 3), forge_base.py, facts.py (row 4), forge_stack*.py (row 5), permissions.py `gh extension list` (listed as not a forge call). 10 files, as the PR says. No new caller.
3. Word check: `rg -n -i "no forge command|forge included|needs no network|reads no forge" AGENTS.md CONTRIBUTING.md README.md skills/chantier/references skills/chantier/scripts/cli/src` shows only this CR's qualified sentences, hub/watch.py (true, spec-allowed), hub/issue_refs.py ("needs no network", about the issue refs, unrelated), and commands/__init__.py line 8 "git and the forge included" (pre-existing, same sentence qualified two lines later; spec does not ask to change it). No unqualified "no forge command" or "reads no forge" about the CLI.
4. PR description (`gh pr view 425 --json body`): renders (sections, table, details fold, no images); Summary/Deliverables/Changes match the diff (8 files all listed); Known gaps present (no test, flaky Windows test); no role name outside Internal references; no STALE mark; no Review box claimed. Deliverables' "10 files" matches claim 2.

## Description pass (PR 425 body), judged at 88904189072602202fe74bfedba88f0394e9200d

Head: 88904189072602202fe74bfedba88f0394e9200d

- Body matches the diff (`git diff main...HEAD`, 8 files: AGENTS.md, CONTRIBUTING.md, README.md, concepts.md, driver.md x2, three docstrings): every row of the table and the Changes list is in the diff, nothing unmentioned. Head 8890418.
- Test plan SHAs: `gh pr checks 425` at head 8890418: check (macos, ubuntu, windows), eval-dry-run, scenario all pass. Review box: `chantier log 453` note "r1 approved at 42063735, committed as 8890418" and verdict VERIFIED at 88904189.
- Known gaps names the flaky Windows test and the no-test decision; no UNVERIFIED claim or STALE mark; no images; role names only in the Review box.

VERIFIED
