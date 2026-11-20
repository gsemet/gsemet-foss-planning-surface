## Summary

Nothing checked a change request's title length, so items filed with a one-paragraph request and no heading showed that whole paragraph as their title on the board. A title is now at most 72 characters, with the description below it, and the tools enforce it: `validate` and `summary lint` refuse a long or missing title, `file` never files a request without a short one, the New dialog has a Title field, and the board draws a title on one line.

## Deliverables

The limit, in one constant (`TITLE_MAX`, 120 lowered to 72), and where each tool applies it:

| Tool | A long or missing title |
| --- | --- |
| `validate` | error (exit 3) for items not yet in a batch; gap for batch, archive and trash items |
| `summary lint` | gaps `no heading` and `long title` (exit 2), ranked after `late` |
| `file` | `--title "<short>"` files `# <title>`, a blank line, the text; a short one-line text gets its own heading; anything else is refused (exit 1, the value of `EXIT_USAGE`) |
| fix files filed as inbox items | refused without a short `# Title` |
| board New dialog | optional Title field, sent as `title` |
| board display | one line, ellipsis, full text in the `title` attribute (cards, rows, table cells) |

A request with no heading and several lines is refused with the long-title message, quoting the length of its first line (for example `its title is 16 characters; the limit is 72`), then asks for `--title`.

**UNVERIFIED:** no screenshots of a post-it and of a costs table with a long title cut on one line (no screenshot at `50722b7`).

## Blast radius

Grade: 2. The shared title check and `file_idea` serve the CLI and the board; a revert restores the old behaviour. Existing not-yet-batched items with long titles become `validate` errors until fixed.

## Autonomous decisions

- `short_heading` and the title source (`TITLE_MAX`) live in `summaries/title.py`, not `core/files.py`: `records` imports `files`, and the code-targets test refuses the import cycle.
- `titled_request` counts prose that comes before a later heading as part of the request, so such a request is refused rather than filed under the wrong title.
- In the trash, title findings carry no closing hint, as `summary_findings` already does.
- The scenario's board idea text now starts with a heading, so the scenario keeps filing through the board with the new rule.

## Known gaps

- No screenshots of a post-it and of a costs table with a long title cut on one line; a screenshot from the running board would close it.
- The refusal exits with 1 (`EXIT_USAGE` in `core/errors.py`) where the specification text says 2; the code follows the constant.
- The scenario no longer posts a single-line request with a duplicate slug through the board; the unit tests still cover the board write API.
- The refusal of a several-line request with no heading reads `its title is 16 characters; the limit is 72` (the first line's length), as specified, although that request has no heading.

<details>
<summary>Details</summary>

## Changes

- `core/records.py` and `declare/summary.py`: limit 72 (a test keeps the two equal).
- `summaries/title.py`: `title_findings`, `short_heading`; `status/views.py`: `folder_title` public.
- `commands/validate.py`, `summaries/gaps.py`, `summaries/format.py`: severity by stage, new gap kinds.
- `file --title`, `file_idea`, `titled_request` (`lifecycle/backlog.py`), `filed_fix`, board `_new`, New dialog field and i18n keys.
- Board CSS and JS: one-line titles; `DESIGN.md` rule "One-line titles".
- Cards: chief-of-staff, griller, spec-writer, concepts.
- `scenario/run_scenario.py`: the board idea text starts with a heading.

## Impacts

Agents write a short title with the description below it; the board shows one line per title. The board's post-it and costs-table look is not shown (no screenshot).

## Test plan

- [x] New or changed tests (they fail on the previous code): `tests/test_titles.py` and the validate, summary lint, design and journal tests, 112 passed at `50722b7`
- [x] Local gates at `50722b7`: `just check` (1094 passed), surface-board unit 262/262, `just scenario` pass; `just eval-dry-run` 18 of 18 at `9c68a3c` (carried to `50722b7`, whose change touches `lifecycle/backlog.py` and `tests/test_titles.py` only)
- [ ] Evidence: no before/after screenshots (see Known gaps); text rows run at `50722b7`
- [x] Review: approved at `50722b7` (reviewed at `9c68a3c`, committed as `50722b7`)
- [x] Verified at `50722b7`
- [x] CI green at `50722b7`: 5 jobs, `just scenario (ubuntu-latest)` included

## Internal references

CR-412 a-cr-s-title-stays-short.

</details>
