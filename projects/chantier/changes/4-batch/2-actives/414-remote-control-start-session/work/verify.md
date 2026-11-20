# Verify CR-414

Head: dc4beb21c3024cb15783ec5f1f87c6d0df4fd6f4

All claims judged at dc4beb2 (git rev-parse HEAD in the worktree; tree clean).

1. Stale-wording search: `grep -rnF "<pattern>" skills docs README.md --include=*.md --include=*.svg`, run for the 9 spec patterns at dc4beb2: every one returned nothing (rc=1). Wrapped wordings: `grep -rn -i "outside a worktree\|nested sessions" README.md docs skills` returns only claude-code.md:585/602 (worktree-session rows, still true), no old rule.
2. Section 1 (claude-code.md) at dc4beb2: Foreman-start row (l.22: no cwd, no preset, proved 2026-11-20), move row (l.50: change_directory, no AGENTS.md reload, clear_session denied, not-recorded list), classes rows Remote Control (l.583) and planning surface (l.588, both setups), rule paragraph (l.609-), remote paragraph (l.629), settled trial (l.642), surfaces table (l.669, l.678), For-you blocks (l.747, l.799-808): all present by grep.
3. Sections 2, 3, 4: `git diff --stat d7b5a019 HEAD` shows chief-of-staff.md, session-start.md, README.md, planning-modes.md/-texts.md/.svg, use-cases*.md, hosts.md changed; copilot.md, SKILL.md, tutorial, CLI, hooks untouched.
4. SVG text vs texts file: the Remote panel lines (svg l.37-42) and the `<desc>` (svg l.3) equal the texts file's Remote panel and description paragraph, read side by side.
5. Test keeping host tools out of cards: `pytest test_plugin_files.py -k host_has_its_reference` -> `1 passed`; `grep start_session skills/chantier/references/*.md` returns nothing (cards name no host tool).
6. Gate: gate log pass at head dc4beb21c3024cb15783ec5f1f87c6d0df4fd6f4 (`just scenario`, run 20261120-212450-27732, from `chantier log 414`); CI 5 jobs pass recorded by the Driver.
7. PR description: posted body equals work/pr-body.md (only a trailing blank line differs); sections render, Summary/Deliverables/Changes match the diff (11 files), Known gaps names the unproved items, no images, no role-name misuse. The Review/Verified/CI boxes still hold `<sha7>` placeholders: the Driver fills them at hand-back (Review note exists: "r1 approved at d7b5a019, committed as dc4beb21").

VERIFIED
