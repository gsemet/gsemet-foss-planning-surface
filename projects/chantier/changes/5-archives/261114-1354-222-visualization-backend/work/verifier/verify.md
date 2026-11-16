# Verify CR-222 (with CR-247 and the lazy summary parser riding in the branch)

Head: bd99c574bcefb08b88ab21123ff1da6b4943e904

Delta from the verdict at ac130ba (rebased onto main effb478; summary parser made lazy; shutil import fix). Live run in a scratch repo with HOME/USERPROFILE/CLAUDE_CONFIG_DIR in scratch.

- `just check` (worktree, bd99c57): ruff clean, mypy "no issues found in 118 source files", `uv lock --check`, Biome "Checked 21 files", pytest "68 passed", release-notes ok. PASS.
- Live board (bd99c57): `chantier --version` = 0.9.0; `board --port 0 --clock ...` prints `board on http://192.168.5.45:59060/?k=<key> over <folder>` and the `listens on the local network (0.0.0.0)` line; `/api/board` without key -> 401; with `X-Chantier-Board-Key` -> 200 JSON (`board:true, surface:false`); `/` CSP `default-src 'none'; script-src 'self'; ...`. PASS.
- Lazy parsers: `chantier summary --help` prints the lazy `summary` parser (lint|set|label|group). PASS.
- Key exchange, cookie, 304, path escapes, costs POST/Origin/405, seats, port errors, start-up time: carried from ac130ba (judged there PASS); the board/ code is unchanged by the rebase except what `git diff --stat effb478..HEAD` shows, and the live run above re-exercises the start and the key.
- CI at bd99c57: check x3 pass, eval-dry-run pass, `just scenario (ubuntu)` PENDING when judged. The waiver (batch-17) needs it green before ready.
- Evidence E6 frame screenshots: not captured; named in Known gaps. E3 phone: user's.
- PR description (as posted, bd99c57): previous defects fixed (CR-247 named, "project views" overclaim gone, Known gaps names the waiver and the head). Still FAILS:
  1. A delivered change is unmentioned: the diff carries rewritten docs and rules (AGENTS.md board exception and git-exception rule, CONTRIBUTING.md +39, docs/boards.md -47, README, docs/agents-and-models.md, chief-of-staff.md, session-start.md, hosts/claude-code.md, hosts/copilot.md), the scenario step driving the real server (`scenario/run_scenario.py`, 375 lines changed), `biome.json`, `.gitattributes`, `justfile`. Summary, Changes and Impacts ("No visual change yet") name none (AGENTS.md appears only in Known gaps). Command: `git diff --stat effb478..HEAD`.
  2. Changes lists the board modules without `backlog`, `guard`, `routes`, `reply`, `static`, `context`, which the diff adds (minor).

NOT VERIFIED
- Failed: PR description (unmentioned docs/rules/scenario changes). Not captured: E6 screenshots, E3, E5, E7; before/after not captured (the before is the old read-only board without an API).
