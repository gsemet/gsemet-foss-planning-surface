## Summary

Studio keeps each Markdown file's original line endings: a CRLF file stays CRLF, an LF file stays LF. The repository stores Markdown as LF (`* text=auto eol=lf`), and that same rule would silently turn any CRLF fixture into LF, so tests meant to run on CRLF would prove nothing. This PR keeps CRLF and mixed fixtures byte-exact whatever the OS or git configuration, guards them with a test, and adds tests that check a block save keeps every untouched byte and line ending.

## Deliverables

Real fixtures stored with their own endings, in `test/fixtures/markdown-line-endings/`:

| Fixture | Stored bytes |
| --- | --- |
| `document.lf.md` | LF only |
| `document.crlf.md` | CRLF only, final newline |
| `no-final-newline.crlf.md` | CRLF only, no final newline |
| `document.mixed.md` | CRLF and LF mixed |

`.gitattributes` gets two lines after the general rule, so git never converts them:

```gitattributes
* text=auto eol=lf
**/*.crlf.md -text
**/*.mixed.md -text
```

## Changes

- `.gitattributes`: `-text` rules for `*.crlf.md` and `*.mixed.md`.
- `test/build/lineEndingFixtures.test.ts`: fails when a `*.crlf.md` holds a bare LF (or none exists), when a `*.mixed.md` does not hold both kinds, when git does not leave the files unconverted, or when any other tracked Markdown file is stored with a CR.
- `test/core/edits/lineEndingPreservation.test.ts` and `test/session/lineEndingSave.test.ts` (real preview manager): on each fixture, edit one block and leave the rest alone; the edited block changes, every byte before and after is identical, no LF is added to a CRLF file and no CR to an LF file, including the last block with and without a final newline.
- `test/shared/lineEndingFixtures.ts`: shared loader for these tests; `test/session/blockFixture.ts`: the fixture helper of `blockReq.requirements.test.ts` moved out unchanged to keep that file under the size limit.
- Requirements: a scenario added to the block-editing requirement on line endings (wording of the normative sentence unchanged), requirements log entry.

## Impacts

No visual change and no runtime change; tests, fixtures and git attributes only.

## Blast radius

Grade: **1**. Test and repository configuration only; a `git revert` restores the previous state.

## Autonomous decisions

- The two `-text` rules also cover mixed-ending fixtures, so their bytes survive `git add --renormalize`.
- The guard checks the index (`git ls-files --eol`) for "no other Markdown stored with CR", because a Windows working tree can show CRLF on an LF-stored file.
- The page-level test of the editor turning CRLF into LF and the "stays on Saving Markdown..." tests are left to the fix for that bug; they fail on the current code.

## Known gaps

- The exploratory QA scenario `ux-35` was not re-run; its source file stays LF in git and the QA setup script converts it to CRLF when it prepares the workspace.
- The save-ends (no stuck "Saving Markdown...") tests on CRLF are not part of this PR: they need the fix for that bug.

<details><summary>Details</summary>

## Test plan

- [ ] New or changed tests (they fail on the previous code): the guard and byte-preservation tests fail on an LF-planted CRLF fixture and without the `-text` rules (at <sha7>)
- [x] Requirements: SwRS updated, markers in tests, `just requirements-update`
- [x] Changelog: No user-facing change
- [ ] Local gates: `just check` at <sha7>
- [ ] Review
- [ ] CI green

## Internal references

CR-435 (batch-07), investigation and round notes under the CR's `work/` folder; red-proof log `work/evidence-red.log`.

</details>
