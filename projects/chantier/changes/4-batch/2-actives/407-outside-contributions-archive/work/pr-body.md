## Summary

A pull request (or merge request) merged on the project without chantier leaves no trace in the
planning folder, so the archives tell only part of the project's story. On the user's word
("archive <link>"), the Chief of Staff now turns such a PR into a short report in
`5-archives/`, and `chantier validate` checks that an archive claiming this form is named right.
Nothing is asked of the outside author, and no new CLI command is added.

## Deliverables

The archive of one outside PR, and the name `validate` checks:

```text
5-archives/261120-1015-outside-42-fix-typo-in-readme/
├── intake/request.md   the PR's description, as received
├── delivery.md         PR link, author, merge time (UTC), `Archive in the PR: no`, what changed
└── summary.json        written by `summary set`
```

- `<YYMMDD-HHMM>` is the merge time, so the archives keep the merge order; `<number>` is the
  forge's PR or MR number; `<slug>` is the title as `file` makes a slug.
- `validate` errors (exit 3) on a folder of `5-archives/` whose name starts with `outside-`
  (alone or after a date or stamp) and is not in that form. Other archive names stay unchecked,
  so existing archives are unaffected.
- With a planning surface and no running writer, nothing is written, and the Chief of Staff says so.
  In-project mode has no writer and writes in `.agents/changes/5-archives/`.

## Blast radius

Grade: **1**. One added check in `validate` (only names that claim the outside form) and card
and docs text; `git revert` restores the previous behaviour.

## Autonomous decisions

- The "An outside PR" paragraph of the Chief of Staff's card sits after the whole first paragraph
  of "With a planning surface", not mid-paragraph, because that paragraph also holds an unrelated
  rule.

## Known gaps

- **UNVERIFIED:** the GitLab read (`glab mr view`) is unproved: no real merged MR was at hand.
- The text of the Chief of Staff's card is agent judgement; no test guards it.

<details>
<summary>Details</summary>

## Changes

- `lifecycle/layout_check.py`: two regex constants and `_outside_names`, added by `placement`.
- `declare/validate.py`: help text names "outside archives' names".
- `references/chief-of-staff.md`: an Entry points row and the "An outside PR" paragraph.
- `references/concepts.md`, `docs/planning-folder.md`, `docs/planning-modes.md`: the new name and
  the new check.
- `tests/test_validate.py`: one parametrized test over eight names (one valid, five malformed,
  two that do not claim the form).

## Impacts

No visual change. A planning folder with a malformed outside archive name now makes `validate`
exit 3 (none exists on the known surfaces).

## Test plan

- [ ] New or changed tests (they fail on the previous code): `test_an_outside_archive_is_named_in_its_form`
- [ ] Local gates at `<sha7>`:
- [ ] Evidence: `gh pr view 380 --json number,title,url,author,state,mergedAt,files,body` returns every field the card names (keys: author, body, files, mergedAt, number, state, title, url), read at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-407 outside-contributions-archive (Part G of seven).

</details>
