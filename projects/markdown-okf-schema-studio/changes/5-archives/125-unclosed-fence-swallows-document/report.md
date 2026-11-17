# Report — unclosed-fence-swallows-document

Status: **done** (2026-10-27, branch `change-requests/125-unclosed-fence-swallows-document`, PR #132, merge commit 78e518d3).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | fix(preview): show an unclosed fence as raw source instead of hiding the rest of the document (see `reports/`, `reviews/`) | 78e518d3 |

## Proof of completion

- Merged through gh stack (PRs #132–#138) on 2026-10-27; stack CI green, heavy CI run 40507920933.
- Last coder round (T1-r1.md): `just check`: all green except the last recipe. check-boundaries 261 modules, check-limits 702 files, check-settings 17, check-markers ok, unit 2769 pass / 0 fail, contracts 2/2, security 48/48, release tests 31 passed.
- Screenshots and details in `reports/` and `reviews/`; PR body in `reports/PR-BODY.md`.

## Open items

- None recorded here; open points of the last round are in `reports/T1-r1.md`.
