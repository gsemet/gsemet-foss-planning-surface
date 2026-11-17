# Verify CR-298

Head: a180e4dded169fa8b583b891d398431db7600218

Judged at a180e4dded169fa8b583b891d398431db7600218 (restack onto origin/main faa4719; tree clean, `git status --short` empty).

## Move
`git range-diff 9d6484e...a180e4d` -> `1: 943fcb4 = 1: faa4719`, `2: 9d6484e = 2: a180e4d`: the CR's patch is unchanged. The base gained CR-297 (faa4719), so the proofs that run the code were run again.

## 1. just check (judged again at a180e4d)
`just check` in the worktree: mypy "no issues found in 169 source files", biome "Checked 98 files ... No fixes applied", `272 passed in 47.17s`, `release-notes: ... v0.10.0 ... ok`. PASS (Linux/macOS: CI green on all 5 jobs per the Driver).

## 2. Playbook behaviour with a catalog model (judged again at a180e4d)
Covered by `test_playbook_config.py` inside the 272 passed above: a `model: gpt` and `model: opus` under a role on `--host copilot` exit 2 with "ambiguous" (and the matching models listed); no chantier.yaml prints the plugin's agents, exit 0 (my manual run in a scratch repo, cwd = project: `playbook: no chantier.yaml, the plugin's agents and models`, `coder: agent=chantier-coder model=(its file's)`). My hand-written chantier.yaml in a scratch repo was not picked up by the CLI (output stayed "no chantier.yaml"), so I do not cite it; the tests are the proof for the refusals.

## 3. Carried from 9d6484e (patch unchanged per range-diff; the base change, CR-297, touches agents/costs not the catalog files)
- Tests of the CR and drift test (`test_the_committed_catalog_is_what_the_committed_tables_build`): part of the full suite above, passing at a180e4d.
- No network in copilot_catalog.py: carried from 9d6484e (file unchanged by range-diff).
- Diff scope (costs/, session_usage.py, agents untouched; 18 files matching the PR's Changes): carried from 9d6484e, range-diff identical.
- PR description (Summary, Deliverables, Changes, Known gaps, no STALE): carried from 9d6484e; proofs naming `9d6484e`/`943fcb4` are carried via the unchanged patch. The Driver's note and the Review box are the Driver's to match with `$CHANTIER log`.
- Not re-run: the 30-model refresh (needs network); the drift test covers the committed JSON.

## 4. Evidence
No before/after pairs: no visual change.

VERIFIED
