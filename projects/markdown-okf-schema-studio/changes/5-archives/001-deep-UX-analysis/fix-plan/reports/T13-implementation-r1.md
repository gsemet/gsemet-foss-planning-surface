# T13 implementation — round 1

STATUS: DONE

## Summary
`followActiveEditor` now returns without touching the preview when the active editor is not an
eligible Markdown document, so the side preview keeps its last Markdown document (like the built-in
preview). `showUnavailableDocument` had no other caller and was deleted, so the string "Open a
Markdown file to use the Sphinx preview." is gone. `setMissingSource` callers are untouched (P-L4).
README gets the one sentence in "Use the Preview".

## Files changed
- src/extension.ts — early return in `followActiveEditor`; removed `showUnavailableDocument`
- test/integration/lifecycle.test.ts — package.json block replaced with "preview unchanged" assertions
- test/integration/realInput.test.ts — added RI-T13 (`scenarioPreviewKeepsMarkdown`) and import of extensionApi helpers
- README.md — one sentence in "Use the Preview"

## Tests written first (failing before the fix)
- RI-T13 (trusted gate, unmodified src) — failure: `AssertionError: the preview keeps the Markdown file` actual `.../realinput-t13-Kg6Sxz/tool.py` expected `.../first.md` (log: logs/T13-impl-pre-trusted.log)
- Lifecycle block: not reached in the pre-fix run, because the trusted suite aborts at the RI-T13 failure first. Its old version asserted the bug (`missing-source`); the new version was not run separately against unmodified code.

## Tests added or changed
- RI-T13 — Python file shown in column One: preview documentUri, status and panel title still name the Markdown file, frame still shows the heading; then a second Markdown file switches the preview (P-L1).
- lifecycle.test.ts — after showing package.json: documentUri, status (success/recovery), html marker, outputDirectory, requestId unchanged after 750 ms; returning to the Markdown editor keeps the same requestId.

## Existing assertions changed
- lifecycle.test.ts:the `package.json` non-Markdown block — old: `status === "missing-source"`, `documentUri === package.json`, html without markers, `outputDirectory === undefined` → new: preview unchanged as described above — required by: UX-25 intended behaviour change.

## Verification
- `scripts/gate.sh T13-impl unit full` → PASS (logs/T13-impl-unit.log, logs/T13-impl-full.log)

## Evidence for reviewers
- Screenshot `19-preview-keeps-markdown` produced by the real-input evidence run.

## Open points / STOP reason
- `src/extension.ts.orig` exists in the tree (pre-existing, untouched).
- A different string, "Open a Markdown file to use Markdown OKF-Schema Studio." (command with no Markdown editor), is unrelated and unchanged.
