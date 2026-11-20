# Verify CR-412

Head: 50722b7f189877b10bf8a534640c035788987978

Judged at 9c68a3c4d0f123959d347d7f2718d59ed95ae057 unless noted. CI green at this head (Driver's note); the scenario was not re-run by the Verifier.

## Claims

1. Tests for the change pass. Command: `uv run --no-sync --project . pytest tests/test_titles.py test_validate.py test_summary_lint.py test_board_design.py test_board_journal.py -q`
   Output: `112 passed in 6.96s`.
2. TITLE_MAX is 72 in both places: `grep -rn TITLE_MAX src` shows `core/records.py:23: TITLE_MAX = 72` and `declare/summary.py:11: TITLE_MAX = 72`.
3. `file` rows (scratch project under work/scratch, removed after):
   - `--title "Short one"` with a two-line text: filed `# Short one`, blank line, `body`, `more` (bytes as spec).
   - `file "one short line"`: filed `# one short line`.
   - 73-char heading: refused, `the request has no short title (its title is 73 characters; the limit is 72): give --title ...` (matches spec text), nothing filed.
   - several lines, no heading, no --title: refused, nothing filed, BUT the message differs from the spec (see Failed).
4. `validate` on the live planning surface prints title/no-heading findings in `6-trash` as gaps (`gap 6-trash/...: title is 172 characters: the limit is 72`, `no "# " heading`), exit not 3: history only gaps, as spec.
5. `filed_fix`, summary lint, validate error/gap severity, board write API, board design: covered by the tests of claim 1 (read the diff: `commands/crs.py` message matches the spec text; `commands/validate.py` severity by stage and gap-kind exclusions as spec).
6. PR description (pr-body.md): consistent with the diff; Known gaps names the missing screenshots.

## Second pass at 50722b7f189877b10bf8a534640c035788987978

Move 9c68a3c -> 50722b7 touches only `lifecycle/backlog.py` (`titled_request`) and `tests/test_titles.py` (`git diff --stat 9c68a3c 50722b7`). Claims 2, 4, 5, 6 carried from 9c68a3c: the move touches nothing they exercise except the file refusal.

- Claim 1 re-run at 50722b7: same pytest command, `112 passed in 7.19s`.
- Claim 3, several-line text with no heading: the diff makes the refusal use the long-title message with the first line's length (`size = len(heading) if heading is not None else len(line.split("
")[0].strip())`), as spec part 5; the test case `A line
and another` now asserts `REFUSAL.format(6)` and passes (claim 1 run). Failed item resolved.

## Notes

- Spec says refusal "exit 2 (EXIT_USAGE)"; `EXIT_USAGE` is 1 in `core/errors.py` and the code exits 1. The spec contradicts itself; the code follows the constant. Not counted as a failure.

## Unproved

- Two board screenshots (Triage post-it, costs table with a long title cut on one line): not capturable by the Verifier; named in the PR's Known gaps.

VERIFIED
