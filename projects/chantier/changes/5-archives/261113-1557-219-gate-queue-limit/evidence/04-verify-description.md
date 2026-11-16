# CR-219 description pass at 0c4838f: NOT VERIFIED

Checked: `gh pr view 162 --json body` against the diff (7 files), pr-template audit, proofs, `gh pr checks 162`.

- Clean and renders: yes. Details block well formed, nothing after it.
- Role names: "Drivers" is a product term here (driver.md changes): accepted.
- Diff covered: commands.py, state.py, cli.py, driver.md, concepts.md, docs/gates.md, scenario: all listed.
- Proofs name 0c4838f; five CI checks pass at that head. No STALE or UNVERIFIED marks.
- FAIL: the "Known gaps" section is missing. The template (layout rule and audit item 10) requires it,
  visible right after Autonomous decisions, "None" when there is none.

Fix: add `## Known gaps` with "None" (or the gaps recorded) after Autonomous decisions, then re-check.
