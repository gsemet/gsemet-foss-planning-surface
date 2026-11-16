# Verification, CR-223

Head: f3727480a4a8ff9be4a5f754d7f27e70a71e101a

Note: at this head the CLI is the root project's script, so every command ran as
`uv run --project <worktree> --locked chantier ...`; `skills/chantier/scripts/cli/chantier.py` no longer exists
in the worktree (the brief's `$CHANTIER` form is the main checkout's older CLI, used only for `rules`).

## E1 - f372748 (head)
- `uv run --locked --group dev pytest -q`: `63 passed in 16.88s` (evidence/e1-pytest.txt).
- `mypy --strict` through `uv run --locked --group dev --with mypy==1.20.0 --with types-psutil mypy --platform {linux,darwin,win32}`: `Success: no issues found in 84 source files`, three times (e1-mypy.txt).
- `uvx ruff@0.17.5 format --check skills`: 104 files already formatted; `ruff check skills`: All checks passed.
- PASS.

## E2 - f372748
- `uv run --locked python scenario/run_scenario.py --forge github`: exit 0, `github: 730/730 checks passed in 1148.1 s`
  (evidence/e2-scenario-github.txt, transcript github-20261114-075647.md). Section 21 holds 33 checks, all [x], covering items 1-12;
  item 13 is the `## 20` check "`summary set` and `lint` with --project ... does not ignore summary.json", [x].
- Hand spot-checks through the real CLI on temp repos outside the repo (e2-spot-basic.txt, e2-spot-origins.txt, e2-spot-late.txt):
  - newline in summary: exit 1; 301-char summary: exit 1; `--unchanged` on a new item: exit 1 ("--title is required" fires first, still a refusal);
    `--tracker` with no `issue:`: exit 1; `STATUS.md` path: exit 1 "not a CR folder"; `6-trash` folder: exit 1 "a dropped CR keeps its summary as it is: restore it first"; label "no way": exit 1.
  - origins: github #41, gitlab #12, jira CHT-118; `tracker.example.org/t/7` exit 1 without `--tracker`, `gitlab #7` with it.
  - late: `02-answers.md new` is named; STATUS.md and work/ changes give no gap; `--title` alone stays late; `--unchanged` closes it; CRLF+BOM rewrite gives `no gap`.
  - unreadable summary.json: `lint` names it (exit 2), `set` exits 2 and leaves `{bad` as it was.
  - label/group lines and `sources` unchanged as the spec says.
- PASS (GitLab forge not run, as the brief asked for github only).

## E3 - f372748
Copy of `.agents/changes` (without work/, lock files) in a scratch git repo outside the repo; the main checkout's `git status` was identical before and after.
`summary lint` run time 0.99 s, exit 2, first line: `39 gap(s) in 39 CRs` (evidence/e3-lint.txt). Archives are out of the default walk as the
decision after the specification says (so not E3's original 2 + 18 + 103 counts); a named archive folder is still checked:
`1 gap(s) in 1 CRs` for `5-archives/261105-1059-101-forge-auth-status`. PASS.

## E4 - f372748
Fixture (e4-fixture-commands.txt) built through the commands from the prototype's cases; `summary_view` output (e4-summary-view.txt):

| slug | kind | ref | labels | late |
| --- | --- | --- | --- | --- |
| docs-sphinx-rtd | github | #41 | docs | False |
| landing-page | gitlab | #12 | docs | False |
| epoch-required-everywhere | jira | CHT-118 | cli | False |
| visualization-backend | verbal | - | board | True |
| planning-server | verbal | - | board | False |
| audit-force-upstream-exemption | verbal | - | none | True |

Matches DEMO_SRC, DEMO_LATE and T0().lab of the prototype. PASS.

## PR body (work/pr-body.md) vs the diff against its base
Modules, command forms, the STATUS `files` count skipping `summary.json`, the cards and docs listed, scenario section 21 = 33 checks: all match the diff.
Stale lines to update: Known gaps "No run of summary lint on the repository's own planning folder, and no fixture of the prototype's data, yet" is now
covered by E3 and E4 above; the Test plan's "Verified at <sha7>" can be ticked at f372748.

## Verdict
VERIFIED at f3727480a4a8ff9be4a5f754d7f27e70a71e101a.

# Delta pass at 955e7d6a0868c303e1cfd3105cc40cff984bd040

Head: 955e7d6a0868c303e1cfd3105cc40cff984bd040

Move: clean restack onto main (febd917). `git range-diff e54e299...f372748 febd917...955e7d6` shows `1: f372748 = 1: 955e7d6` (patch identical).
`git diff --name-only e54e299 febd917`: only skills/chantier/references/chief-of-staff.md and status-layout.md (cards text), which no proof runs.

- E1 re-run at 955e7d6: `uv run --locked --group dev pytest -q`: `63 passed in 28.98s`.
- E2 spot at 955e7d6: temp repo, `summary lint` -> `1 gap(s) in 1 CRs`, exit 2; `summary set ... --title T --summary S` -> `(origin verbal; 1 files)`; `lint` -> `no gap (1 CRs)`, exit 0.
- E2 scenario (730/730 github, 711/711 gitlab), E3, E4, description claims: carried from f372748 (patch identical; base change touches cards text only). Gate pass log 20261114-054649.log at f372748; user waiver Rebase-Q1 A covers the local gate at this head.

VERIFIED at 955e7d6a0868c303e1cfd3105cc40cff984bd040.
