# CR-379 verify

Head: a1d165dd36301353ef5d65d82acfe587124fffb3

All claims judged at a1d165d (first verification).

1. Tests: `uv run --no-sync --project . pytest -s -q skills/chantier/scripts/cli/tests/test_startup_manifest.py test_plugin_files.py test_cli_stop.py` -> `92 passed in 9.81s` (log: work/verifier-tests.log).
2. Bytes: the 38 `startup-bytes` lines (19 roles x 2 hosts) equal work/r1-bytes.md and the PR table; maximum reload 8,664 (chief-of-staff, copilot), boot max 7,870; goal 11,290 held, limit 12,544 untouched (the three constants are not in the diff).
3. Agent bodies identical per role across hosts: python comparison of 14 roles, `diffs 0`.
4. No "defer all other card sections" / "Read this short role contract" in skills, agents or Copilot agents except the test's own negative phrases (grep lists only test_startup_manifest.py).
5. Rules in place: startup-core.md holds "never in a shell variable" (line 4); CoS SKILL.md line 26 `watch: not running` under Startup core, reload sentence has "with `$CHANTIER` as this file defines it" and "but its Startup core" (line 32); CoS and Griller "At the session's start" present; router seat bullets (lines 20, 24) and status "You change nothing" (line 22); session-start.md "starts no service twice" (240) and archive clause (212); concepts.md prompt rule (454); role-core.md holds the deferral rule; manifest version 2 with `paths`.
6. No CLI `src/` change: `git diff --stat <base>...HEAD -- scripts/cli/src` is empty.
7. PR description: head SHA matches (`gh pr view 344`), sections match the diff (56 files: cards, agents, manifest, SKILL.md, tests), Known gaps names the missing real Claude Code session, Copilot, zsh/sh; no images; no role-name misuse seen. Review/Verified boxes unchecked pending.
8. UNVERIFIED: Evidence 6, a real Claude Code boot, reload and Driver start at this head, cannot be run by the Verifier; it is a named Known gap in the PR (decision 10 allows a named gap). Does not alone change the verdict.
9. Gates: just check and just scenario per Driver, CI green (not rerun here).

VERIFIED (with item 8 UNVERIFIED as a named gap)

## Description pass (posted body, Test plan boxes checked) at a1d165d

Head: a1d165dd36301353ef5d65d82acfe587124fffb3

- `gh pr view 344 --json headRefOid` -> a1d165dd36301353ef5d65d82acfe587124fffb3; body matches the diff and the byte tables of item 2 (judged at a1d165d).
- Review box: `chantier log 379` -> "r1 approved at a1d165dd... committed as a1d165d" (proves the box).
- CI green box: log note "CI green at a1d165d (5 jobs)"; gate passes `just check` and `just scenario` at the full head SHA.
- Every proof in the body names a1d165d; no images; no STALE mark.
- Known gaps: the UNVERIFIED claim (real Claude Code boot/reload/Driver start), Copilot, zsh/dash all have bullets; the unchecked Evidence box matches.

VERIFIED
