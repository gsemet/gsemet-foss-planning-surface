# Verify CR-493 (SC07 help topics)

Head: 64ff139f561c626ef17ca5b8325ce26434782c04

All claims judged at 64ff139 (worktree clean, `git rev-parse HEAD` = the full SHA above). Verdict: NOT VERIFIED (description only; the code claims hold).

## Claims proved at 64ff139

1. `chantier help` lists topics: `$C help | head` prints `topics: 38; help <topic> prints one, help --for <role> lists a role's`, then `lease: ... (cr-driver, ..., chief-of-staff)`, in file order. (Spec says 41 but its table lists 38; the table was followed, noted under Autonomous decisions.)
2. `help --for cr-driver` lists only that role's topics (`lease`, `checkpoints`, ..., `matrix`), no roles column. `help --for coder` prints `no topic for coder; help lists them all`, exit 0. `help --for nobody` exits 1: `no role nobody; roles: cr-driver, ...`.
3. `help lease` run from /tmp (no project, no batch): exit 0, first line `topic lease: ... (roles)`, then `--- references/driver-session.md#Means: the lease ---` and the section; `grep -c "claim lost"` = 2.
4. `help leas` exits 1: `error: no topic leas; did you mean help lease or help release?; help lists them all`. `help lease --for foreman` exits 1: `error: help takes a topic or --for, not both`. `help --host copilot stack-merge` prints `topic stack-merge: ...` and the `## After a merge` section.
5. Named topics exist: `grep -rhoE '`help [a-z][a-z0-9-]*`' src` finds board 4, lease 6, merge 1, refused-push 1, stack-merge 2, watcher 5 (19 spans; every name is a topic, enforced by the test below).
6. Tests: `python -m pytest tests/test_help_topics.py test_leases test_push test_ready_line test_restack_line test_watch_board test_watch_stream test_refusal_gate test_scenario_coverage test_startup_manifest -q` -> `189 passed in 30.14s` (M9 gate: 36 refusals scanned, 6 allow-listed).
7. Wiring: diff stat shows `core/remote_wire.py` (NEVER_REMOTE), `cli.py`, `declare/help.py`, `commands/help.py`, scenario step (`run_scenario.py:1170 w.chantier("help","lease")`) and README coverage bullet, AGENTS.md (cli.run list, login paragraph, `help` paragraph at lines 133, 211, 222).
8. CI at 64ff139 (`gh pr checks 478`): check macos/ubuntu/windows pass, eval-dry-run pass, scenario (ubuntu) pass. No Windows local scenario owed (not stack top).

## Claim that fails: the PR description (posted at 64ff139)

- Known gaps holds one bullet only (role read of a topic unproved). The spec's gate, "seconds its tests add to `just test`, measured before and after on the same machine", is not met: the description says "about 0.3 s ... measured on its own", and the whole-suite before/after was not measured. That unmeasured claim has no Known gaps bullet. Per the card, a missing bullet is NOT VERIFIED. Fix: add the bullet (or measure before/after and quote it).
- Test plan still holds `<sha7>` placeholders (Local gates, Evidence, Review, Verified, CI); to be filled at closing.
- The 41-versus-38 topic count departure is only an Autonomous decision, which is acceptable.
- No images in the description.

## Evidence

No before/after pairs: a CLI addition with no UI; the commands above are the after. The before is the base (`help` absent), not captured.
