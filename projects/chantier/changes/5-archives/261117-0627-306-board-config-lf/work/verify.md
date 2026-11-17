# CR-306 verify

Head: d15df0b9165dda066b7233d6abd9561d7158cfe1

Verdict: VERIFIED

1. Test fails on base, passes at head (judged at d15df0b). Base = 51a3c8e (detached worktree, code from its src via PYTHONPATH, the new test file run from the CR worktree; the base worktree was removed).
   - Base: `pytest skills/chantier/scripts/cli/tests/test_playbook_edit.py -q` -> `2 failed, 3 passed` (`assert b"\r" not in data`, both bom params).
   - Head: same command -> `5 passed in 3.63s`.
   - The test saves through edit.edit_surface_file onto a CRLF chantier.yaml (with and without BOM), asserts no `\r`, BOM kept, `# top` and `port: 8123 # port` kept, `model: gpt-6.1-terra` set, returned sha256 equals sha256 of the disk bytes, and a second save with that hash succeeds (the 409 check is not tripped by the save's own LF conversion).
2. Scratch probe (d15df0b): CRLF bytes `# keep me\r\nboard:\r\n  port: 8123 # port\r\n` through edit_text.new_text + file_bytes -> `\r in old: True, \r in new: False`; output `b'# keep me\nboard:\n  port: 8123 # port\nhosts:\n  copilot:\n    roles:\n      coder:\n        model: m1\n'`. Scratch folder removed.
3. Only caller (d15df0b): `Select-String edit_text|file_bytes|new_text` over chantier/*.py and playbook/*.py -> the only call sites are in playbook/edit.py (`edit_text.new_text`, `edit_text.file_bytes`). The PR's "only caller, CRLF branch removed with no other test to drop" holds; the diff matches the PR's Changes (edit_text.py and test_playbook_edit.py only, `git diff --stat` base..head).
4. `just check` at d15df0b: mypy ok, `uv lock --check` ok, biome ok, `369 passed in 74.47s`, release-notes ok.
5. CI: green at d15df0b per the prompt (all 5 jobs including just scenario ubuntu); not re-run by me.
6. PR description (PR 257): clean, consistent with the diff, Known gaps "None" fits (no UNVERIFIED claim). The Test plan boxes still carry `<sha7>` placeholders and unchecked boxes: the Driver fills them at ready. Review box judged by the Driver's note, not by me here.
7. Description-only pass (PR 257 body, judged at d15df0b9165dda066b7233d6abd9561d7158cfe1; `gh pr view 257 --json body,headRefOid` -> headRefOid d15df0b9...).
   - Clean: sections render, details fold closed properly, no images, no placeholders left, no STALE mark.
   - Summary, Deliverables and Changes match `git diff --stat <base> HEAD`: only edit_text.py (8 lines) and test_playbook_edit.py (+23). The quoted file_bytes body is the head's; the test described is the one proved in claim 1.
   - Test plan SHAs: `just check` 369 passed at d15df0b matches claim 4; CI all five jobs at d15df0b matches Driver note `gh pr checks 257 at d15df0b: all 5 pass`; Verified at d15df0b matches claim 1-4.
   - Review box `approved at d15df0b (reviewed before the commit at 51a3c8e plus the change)`: `$CHANTIER log CR-306` has `r1 inspector approved at 51a3c8e...` and `r1 approved at 51a3c8e, committed as d15df0b`; proves it.
   - Known gaps "None": no UNVERIFIED claim, no missing evidence pair (no visual change), no accepted failed claim. Role names: none in the body.
   Verdict for this pass: VERIFIED.
