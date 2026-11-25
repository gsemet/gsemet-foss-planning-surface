Head: 4564806aa8fc1af19fcd696525ae9651e9d3dcfc

Judged at 4564806aa8fc1af19fcd696525ae9651e9d3dcfc unless noted.

1. Spec Evidence list (start state, Tab/Shift-Tab cycles wide and narrow, resize, newest first, per-panel scroll and offsets, fits-does-not-move, maximize and restore, Tab while maximized, Ready title cut later, Ago narrow and right-aligned, key_name, HELP, footer).
   Command (worktree, skills/chantier/scripts/cli): `uv run --no-sync python -m pytest tests/test_live_model.py tests/test_live_ready.py tests/test_live_panels.py -q`
   Output: `102 passed in 2.68s`. The tests read (test_live_panels.py: start state, Tab cycle parametrized by width, resize, newest first, maximize, Ago right-aligned and freed columns; test_live_ready.py: per-panel scroll, fits, maximized Ready title) match each Evidence bullet.
   VERIFIED.

2. Long gate pass at the head: `work/gates/20261125-000536.log` first line `gate CR-485 branch chantier/batch-31/cr-485-tui-tab-zones-per-panel-scroll-newest-fi head 4564806aa8fc1af19fcd696525ae9651e9d3dcfc`, last line `result: pass at 4564806aa8fc1af19fcd696525ae9651e9d3dcfc`. VERIFIED.

3. Scope: `git diff --stat origin/main...HEAD` touches only clients/tui/ (view, screen, ready, parts, new boxes), tests, and docs/boards.md; no server, API, web or commands/live.py change. VERIFIED.

4. PR description (work/pr-body.md) against the diff: Summary, Deliverables (m key, Tab/Shift-Tab, Ago 3 to 8, boxes.py) and Changes list match the 10 changed files; Known gaps carries the one UNVERIFIED (no real terminal); no images; Review/Verified boxes are the template's unchecked ones for the Driver to fill. VERIFIED.

UNVERIFIED (named in Known gaps): real-terminal behaviour; no screenshot captured (in-process proof only, no images).

VERIFIED

5. Posted description of PR 461 (gh pr view 461 --json body) at 4564806aa8fc1af19fcd696525ae9651e9d3dcfc: audit items 1-10 pass (sections in order, fold in place, CR name only in Internal references, Deliverables key table matches the diff, Blast radius grade 1, Autonomous decisions, Known gaps with the one UNVERIFIED, no Issues References since the spec has no issue line, no Human decisions since 02-answers records only a Chief of Staff note); Test plan boxes cite 4564806; no images. VERIFIED.

VERIFIED
