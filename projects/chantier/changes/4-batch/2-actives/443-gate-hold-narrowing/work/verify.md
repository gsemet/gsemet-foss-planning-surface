# Verify CR-443

Head: 11f98d99491df051a9ed0b8b32fcca0e10991532

Restack move: a13f35f -> 11f98d99 onto CR-442's local head 648dac86 (not pushed yet). Judged again at 11f98d9.

- Patch unchanged but one commit: `git range-diff 2a5dcf40^..2a5dcf40 83fa6bfd^..83fa6bfd` shows the only difference of the feat commit is the conflict in `skills/chantier/references/hosts/claude-code.md` (CR-442's force-push rows kept; the `uv run ... chantier *` row carries this CR's text "`gate` runs only the long gates the code repository's `chantier.yaml` names, and `lease hold` runs nothing"). The two fix commits are `=` (same patch). PASS.
- Full CLI suite at 11f98d9, `uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests -q -n 4`: `1774 passed, 20 skipped in 183.01s`. It holds the gate refusals, hold limits, no `.lease-hold.*` file, shipped files and the startup manifest. PASS.
- `uv run --no-sync python evals/kit/dry_run.py`: `dry run: 19 of 19 cases as expected`. PASS.
- `git grep -n "lease-hold\|HOLDS" -- skills/chantier/scripts/cli/src`: only `core/files.py:216` (`IGNORED`), as intended. `git grep "until the CR .gate-hold-narrowing"`: no leftover. PASS.
- Long suite: carried from a13f35f only for the logic (patch unchanged); the pipeline `just scenario (ubuntu-latest)` must be green at the pushed head 11f98d9 after the push (CI at the new head still runs); not claimed here.
- PR description: carried from a13f35f (renders, matches diff); only SHAs stale, which the Driver updates. No images.

VERIFIED
