# Verify CR-308

Head: eb9350030e6d22e63cb1c3ea64ff6399cb744ead

All claims judged at eb93500 (E1 at the base 3df17b9 plus the justfile line).

- E1 (3df17b9 + only the justfile change, detached worktree): `just lint` ran `uvx ruff@0.17.5 format --check skills scripts`,
  output: `3 files would be reformatted, 218 files already formatted`, naming scripts\mod.py, scripts\release_notes.py,
  scripts\version.py; `error: recipe lint failed on line 57 with exit code 1`. PROVED.
- E2 (eb93500): `uvx ruff@0.17.5 format --check skills scripts` -> `221 files already formatted`.
  `git diff --stat origin/main HEAD` -> justfile, scripts/mod.py, scripts/release_notes.py, scripts/version.py only
  (4 files, 41 insertions, 11 deletions). PROVED.
- E3 (eb93500): `just version-show` -> 0.11.0; `just release-notes` -> `release-notes: ... ok`;
  `uv run --script scripts/version.py --help` exit 0; mod.py ast.parse exit 0. PROVED.
- E4 (eb93500): local Windows `just check` exit 0 (369 passed, release-notes ok).
  `gh pr checks 261`: just check on macos, ubuntu, windows pass; eval-dry-run and scenario (ubuntu) pass. PROVED.
- Review box `approved at eb93500`: Driver log "r1 approved at 3df17b9..., committed as eb93500". PROVED.
- PR description (posted, head eb93500): renders; Summary, Deliverables, Changes match the diff (justfile line, three scripts);
  Known gaps "None" is right (no UNVERIFIED claim, all evidence captured); no role names outside Internal references.
  The unchecked Verified and CI boxes carry `<sha7>` placeholders: the Driver fills them. OK.

VERIFIED

## Description pass (head eb9350030e6d22e63cb1c3ea64ff6399cb744ead)

PR 261 body checked at eb93500 against `git diff origin/main HEAD` (justfile + 3 scripts) and the pr-template audit: sections, fold, no internal refs outside the fold, Review box matches the driver note "committed as eb93500", CI green (gh pr checks 261). VERIFIED.
