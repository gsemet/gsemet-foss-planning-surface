## Summary

Nothing checked a change request's title length, so items filed with a one-paragraph request and no heading showed that whole paragraph as their title on the board. A title is now at most 72 characters, with the description below it, and the tools enforce it: `validate` and `summary lint` refuse a long or missing title, `file` never files a request without a short one, the New dialog has a Title field, and the board draws a title on one line.

## Deliverables

The limit, in one constant (`TITLE_MAX`, 120 lowered to 72), and where each tool applies it:

| Tool | A long or missing title |
| --- | --- |
| `validate` | error (exit 3) for items not yet in a batch; gap for batch, archive and trash items |
| `summary lint` | gaps `no heading` and `long title` (exit 2), ranked after `late` |
| `file` | `--title "<short>"` files `# <title>`, a blank line, the text; a short one-line text gets its own heading; anything else is refused (exit 2) |
| fix files filed as inbox items | refused (exit 2) without a short `# Title` |
| board New dialog | optional Title field, sent as `title` |
| board display | one line, ellipsis, full text in the `title` attribute (cards, rows, table cells) |

**UNVERIFIED:** no screenshots yet of a post-it and a costs table with a long title cut on one line.

## Blast radius

Grade: 2. The shared title check and `file_idea` serve the CLI and the board; a revert restores the old behaviour. Existing not-yet-batched items with long titles become `validate` errors until fixed.

## Autonomous decisions

- `short_heading` and the title source live in `summaries/title.py`, not `core/files.py`: `records` imports `files`, and the code-targets test refuses the import cycle.
- In the trash, title findings carry no closing hint, as `summary_findings` already does.

## Known gaps

- No screenshots yet of a post-it and a costs table with a long title cut on one line.

<details>
<summary>Details</summary>

## Changes

- `core/records.py` and `declare/summary.py`: limit 72 (a test keeps the two equal).
- `summaries/title.py`: `title_findings`, `short_heading`; `status/views.py`: `folder_title` public.
- `commands/validate.py`, `summaries/gaps.py`, `summaries/format.py`: severity by stage, new gap kinds.
- `file --title`, `file_idea`, `filed_fix`, board `_new`, New dialog field and i18n keys.
- Board CSS and JS: one-line titles; `DESIGN.md` rule "One-line titles".
- Cards: chief-of-staff, griller, spec-writer, concepts.

## Impacts

Agents write a short title with the description below it; the board shows one line per title.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates at `<sha7>`: `just check`
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-412 a-cr-s-title-stays-short.

</details>
