# Verify CR-325

Head: 5041a0c274b453df17f64d4f0d981c650863fb8a

All claims judged at 5041a0c (the head).

1. Tests at the head: `uv run --no-sync pytest skills/chantier/scripts/cli/tests/test_board_config.py -q` -> `10 passed in 6.55s`.
2. Same test file against the base's source (detached worktree of origin/main 33a2305, `PYTHONPATH=<base>/skills/chantier/scripts/cli/src`): `1 failed, 9 passed`; failure `KeyError: 'description'` at the description assertion of `test_a_dry_run_and_a_stale_hash_write_...`. So it fails on the base.
3. Real view (`edit.config_view(Repo.find(scratch git repo))`, scratch folder removed after): all 14 roles of claude and of copilot have a non-empty description, none contains "Prompt starts with" (`empty: []  bad: []` for both hosts); coder = "Implements one round of one chantier CR in its worktree; never commits. Started by a Driver." on both. With a plugin root whose `coder.md` has no description: `('coder', None)`, view returned (no error); a quoted description `'It''s <b>x</b>. Prompt starts with: ...'` gives `It's <b>x</b>.` (quoting undone, cut done). JS escapes via `html` template (diff read: `${row.description}` inside `html`).
4. Diff matches spec: plugin_files.plugin_role_descriptions (ruamel imported inside the function), edit._host adds the field, config.js shows `div.desc` only when set, config.css rule, test extended in an existing function, no i18n key, no agent/card change.
5. PR #283 description: renders (sections, details fold), Summary/Deliverables/Changes match the diff; no image attached, so no username leak; Known gaps carries the screenshot as UNVERIFIED, consistent with this note. Role names appear only as product terms (the change is about roles). Test plan boxes unchecked/`<sha7>` are the Driver's to fill.
6. Page in a real browser: NOT captured. `chantier board` is a server and my card forbids background shells, so I could not serve it and open it at once. No screenshot kept; before-after.md says so. The spec asks for one in the PR's Deliverables; the PR names it as UNVERIFIED. AGENTS.md's screenshot rule applies to the CR board pane only, not here, so this does not change the verdict.
7. CI: not re-run by me; the Driver reports 5 jobs green incl. scenario (ubuntu-latest) at this head (carried from the prompt, not proven here).

VERIFIED

## Description pass at 5041a0c (PR 283 body as posted)

Judged at 5041a0c274b453df17f64d4f0d981c650863fb8a; earlier claims carried (no code move).

- `gh pr view 283 --repo gsemet/chantier --json body,headRefOid`: head is 5041a0c274b4...; body read against `git diff origin/main...HEAD` (5 files: config.css, config.js, edit.py, plugin_files.py, test_board_config.py). Summary, Deliverables, Changes and Autonomous decisions (`_host` vs `_row`) match the diff; nothing delivered is unmentioned.
- Internal references: the CR name appears only in the last section; the body text names no CR, batch or path. Role names and "Driver" appear only inside the quoted product text of the Coder description. Sections in order, fold and Known gaps present.
- SHAs: all `5041a0c`, the head. Review box: log has `r1 approved at 33a2305, committed as 5041a0c`, matching. CI: `gh pr checks 283` shows 5 jobs pass.
- Screenshot gap stated: Known gaps and Deliverables both carry **UNVERIFIED** (no screenshot); Test plan Evidence box unchecked. No image attached.
- Minor, not failing: Test plan says "Local gates at `5041a0c`: just check (443 passed, run before the commit)"; the count is the Driver's and not re-run here.

VERIFIED
