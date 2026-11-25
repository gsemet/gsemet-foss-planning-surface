# Verify CR-493 (SC07 help topics)

Head: 64ff139f561c626ef17ca5b8325ce26434782c04

All claims judged at 64ff139 (worktree clean, `git rev-parse HEAD` = the full SHA above). Verdict: see the second pass.

## Claims proved at 64ff139

1. `chantier help` lists topics: `$C help | head` prints `topics: 38; help <topic> prints one, help --for <role> lists a role's`, then `lease: ... (cr-driver, ..., chief-of-staff)`, in file order. (Spec says 41 but its table lists 38; the table was followed, noted under Autonomous decisions.)
2. `help --for cr-driver` lists only that role's topics (`lease`, `checkpoints`, ..., `matrix`), no roles column. `help --for coder` prints `no topic for coder; help lists them all`, exit 0. `help --for nobody` exits 1: `no role nobody; roles: cr-driver, ...`.
3. `help lease` run from /tmp (no project, no batch): exit 0, first line `topic lease: ... (roles)`, then `--- references/driver-session.md#Means: the lease ---` and the section; `grep -c "claim lost"` = 2.
4. `help leas` exits 1: `error: no topic leas; did you mean help lease or help release?; help lists them all`. `help lease --for foreman` exits 1: `error: help takes a topic or --for, not both`. `help --host copilot stack-merge` prints `topic stack-merge: ...` and the `## After a merge` section.
5. Named topics exist: `grep -rhoE '`help [a-z][a-z0-9-]*`' src` finds board 4, lease 6, merge 1, refused-push 1, stack-merge 2, watcher 5 (19 spans; every name is a topic, enforced by the test below).
6. Tests: `python -m pytest tests/test_help_topics.py test_leases test_push test_ready_line test_restack_line test_watch_board test_watch_stream test_refusal_gate test_scenario_coverage test_startup_manifest -q` -> `189 passed in 30.14s` (M9 gate: 36 refusals scanned, 6 allow-listed).
7. Wiring: diff stat shows `core/remote_wire.py` (NEVER_REMOTE), `cli.py`, `declare/help.py`, `commands/help.py`, scenario step (`run_scenario.py:1170 w.chantier("help","lease")`) and README coverage bullet, AGENTS.md (cli.run list, login paragraph, `help` paragraph at lines 133, 211, 222).
8. CI at 64ff139 (`gh pr checks 478`): check macos/ubuntu/windows pass, eval-dry-run pass, scenario (ubuntu) pass. No Windows local scenario owed (not stack top).

## Second pass at 64ff139 (re-run)

- `help` prints `topics: 38; ...`; `help lease` prints `topic lease: ...`, `--- references/driver-session.md#Means: the lease ---`; `help leas` exits 1 with `no topic leas; did you mean help lease or help release?`.
- `pytest tests/test_help_topics.py tests/test_refusal_gate.py -q` -> `21 passed in 30.72s` (M9: 36 refusals scanned, 6 allow-listed).
- Other claims 1-8 above carried from the first pass at the same head (no move).

## PR description (work/pr-body.md, to be posted)

- Known gaps now has the bullet "whole-suite seconds of `just test` before and after were not measured": the gap is named, so not a failure.
- Summary, Deliverables, Changes match the diff (topics.json, help command, wiring, line suffixes, tests, scenario step, AGENTS.md); the 38 count is in Autonomous decisions.
- Test plan `<sha7>` boxes are filled at the closing. No images.

Verdict: VERIFIED.

## Evidence

No before/after pairs: a CLI addition with no UI; the commands above are the after. The before is the base (`help` absent), not captured.

## Description-only pass at 64ff139f561c626ef17ca5b8325ce26434782c04 (posted body, `gh pr view 478`)

The code claims above are kept as judged. Of the description:
- Summary, Deliverables, Changes, Known gaps match the diff and this note; the 38-topic count (topics.json `topics`), `help` outputs, Review box (`approved at ab5099e`, matches the Driver note `r2 inspector approved at ab5099e3...`), CI at 64ff139 (all five checks pass) hold.
- FAILED: the ticked Test plan box "Evidence: before at 3c29dd7, after at 64ff139" has no proof: no `evidence/` folder and no `work/verifier/evidence/before-after.md` exist, and the first pass says "No before/after pairs". Also 3c29dd7 is not the merge-base (`git merge-base HEAD origin/main` = 8a960d34).
Fix: untick or reword the box (no before/after captured), or capture the pair.

Verdict (description): NOT VERIFIED.

## Description-only pass 2 at 64ff139f561c626ef17ca5b8325ce26434782c04 (posted body, `gh pr view 478`)

- Evidence box now unticked and says none captured (no visual change): consistent, no pair owed.
- 38 topics: `topics.json` topics length 38; `chantier help` prints "topics: 38" (run in worktree at 64ff139).
- 17 tests: `pytest test_help_topics.py` -> 17 passed in 0.55s (includes startup; ~0.3 s claim is from the author's own timing, Known gaps admits whole-suite is unmeasured).
- Lines naming a topic: leases.py/push.py `help lease`, push.py `help refused-push`, orders_merged.py `help stack-merge`, ready_line.py `help merge`, watch_lines.py 9 lines `help watcher`/`help board`: match.
- Allowed count 7 -> 6 in test_refusal_gate.py: matches diff.
- Review ab5099e: log note "r2 inspector approved at ab5099e". Local gates note at 64ff139 and ab5099e (eval-dry-run) in log. CI: all five checks pass at head.
- Renders: sections, mermaid, details fold fine. No image. Role names only in product terms.
VERIFIED
