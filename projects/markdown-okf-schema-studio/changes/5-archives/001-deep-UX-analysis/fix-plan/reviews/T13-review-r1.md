# T13 review — round 1

Base: a39ebb4 · Reviewed diff: 4 files, +~48/-~41

## Gates
unit: PASS · full: PASS (logs/T13-full.log, exit 0; includes trusted/real-input, scroll, reload). No new failure vs T00 baseline.

## Done-when
- [x] unit and full gates pass — logs/T13-impl-unit.log, logs/T13-full.log.
- [x] RI-T13 passes — `scenarioPreviewKeepsMarkdown` in realInput.test.ts; failed before the fix (logs/T13-impl-pre-trusted.log: documentUri was tool.py).
- [x] "Open a Markdown file to use the Sphinx preview." gone — `rg` in src/test finds it only in the git-ignored `extension.ts.orig`.
- [x] README sentence added in "Use the Preview".

## Protected features checked
P-L1: RI-T13 reveals second.md and asserts the panel title switches; lifecycle test returns to secondDocument.
P-L2: `followActiveEditor` still filters `followsActiveEditor`; Open With path untouched.
P-L3: no change to restoration; reload gate passed.
P-L4: `setMissingSource`, `handleRenames`, dependency `onDidDelete` untouched (diff only removes `showUnavailableDocument`, which had no other caller).

## Findings
1. [MINOR] reports/T13-implementation-r1.md — the new lifecycle block was not run against unmodified code; RI-T13 already proves the bug, so acceptable.
2. [NIT] lifecycle.test.ts — long `assert.ok(... status ...)` line exceeds usual width.

Screenshot 19-preview-keeps-markdown (real-input-17EVoV): tool.py active in column One, preview tab "first.md" shows "First heading T13"; nothing clipped, toolbar intact.

## Existing assertions changed
- lifecycle.test.ts package.json block (missing-source, documentUri=package.json, content gone, outputDirectory undefined) → replaced with "preview unchanged" + requestId unchanged. Listed in the task's Expected changes — OK. Not weakened: new assertions are stricter (requestId equality).

VERDICT: PASS
