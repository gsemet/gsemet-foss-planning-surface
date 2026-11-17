# Report — 051-perf-zero-reloads

Status: **done** (2026-10-23, branch `changes-requests/051-perf-zero-reloads`,
[PR #47](https://github.com/gsemet/markdown-okf-schema-studio/pull/47), rebase-merged by the user;
main at 144c341).

## Delivered

| Task | Change |
| --- | --- |
| T1 r1–r2 | Reproducible probe; status, content and properties table sent by `postMessage` with a keyed DOM morph (no `webview.html` assignment while typing); runtime script and CSS as cacheable files; no reload during edits, with explicit stale-edit errors; Mermaid loaded once; geometry-free scroll frames |
| T1 r2 rebase | Conflict fixes after the 050 preview changes |
| T1 r3 | The page sends `previewReady` once its listener is registered and the host answers with the live state (fixes a pairing/theme message lost when the bundle loads slowly; heavy CI failure) |

## Proof of completion

- 3/3 rounds, reviewer APPROVE (r2, rebase, r3).
- Local: `just check` exit 0 (unit 2042/2042, pytest 31), `just visual` 320 scenarios, no baseline
  changed; real VS Code `npm run test:integration` 123 PASS (under the window lock).
- CI: [run 40016137463](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40016137463)
  `checks` pass; heavy [run 40016132398](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40016132398)
  integration pass, stress (advisory) fail: image-paste round 4/20 saved an empty file (feature from main).
- Autonomous decisions (in the PR body): text-editor changes held while an inline editor is open;
  an unsaved inline editor is not moved by outside changes; one PR, not a stack; Mermaid not
  lazy-loaded; no stress scenario for the round-3 race.

## Open items

- Image-paste stress flake (empty saved file) → proposed P2 backlog item.
- Out of scope by decision: PERF-10 (`retainContextWhenHidden`), STAB-05.
