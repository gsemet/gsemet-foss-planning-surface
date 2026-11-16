# Verify CR-261 at ae256d0

- pytest in skills/chantier/scripts/cli: 103 passed (phase_text, next_to_start, phase refusals incl. queued CR, review with no detail, 41-char detail).
- `chantier phase CR-1 bogus --batch batch-x`: argparse invalid choice, exit 2.
- Code read against the spec: records, command, `round`/`take`/`handback` clearing, status views/markdown, `chantier status` row, board row, batch graph node, kanban card, Slots sub-line, pane columns and sheet line, cards, docs, demo batch.
- Scenario checks read: coder r1, inspector, gate scenario (JSON, status, STATUS.md both files), event in events.jsonl and not in Progress, null after handback ready, `phase ci` then take clears, board next_to_start and budget spent.
- Not proven: no real-session pane screenshot (E5), no web board screenshots (E6), `just mod` not re-run at this head.
- Deviation: the exit-2 refusals (queued CR, review with no detail) are in pytest, not in the scenario; the handback blocked "waits for the user" is covered by the unit test and the board read data, not by a handback in the scenario.

## Re-run at ae256d0319cc634c1ce1bb840c0eeadd0cf734ed
- Command: uv run --locked python -m pytest -q skills/chantier/scripts/cli (in the worktree). Output: 103 passed in 36.77s.
- Long gate passed and CI green at this head (per the Foreman).

## Re-verify at 6c75aaaa20700464d116aa61538b5b6092480dec
Head: 6c75aaaa20700464d116aa61538b5b6092480dec
- Move: rebase onto CR-267's branch, no new CR code. Base brought forge_stack, orders_apply, docs and cards changes (git diff ae256d0 HEAD --name-only); none touches the phase command, status, board, hooks or types. driver.md is shared; its phase bullets (step bullet, release driver step) are still present.
- pytest, from skills/chantier/scripts/cli at 6c75aaa: `uv run --locked python -m pytest -q .` -> 109 passed in 26.27s (includes phase_text, next_to_start, phase refusals).
- `uv run --no-sync --project . chantier phase CR-1 bogus --batch batch-x` -> argparse invalid choice, exit 2.
- Claims on the record, status views, `chantier status`, board, pane, cards, docs, scenario checks: carried from ae256d0 (the CR's patch is unchanged by the clean rebase; base files do not overlap).
- Long gate and CI: per the Foreman, CI green at this head; gate pass at ae256d0 (log 20261115-020509), carried.
- Known gaps accepted by the caller: no real-session pane screenshot (E5), no web board screenshots (E6). just mod not re-run here.
VERIFIED
