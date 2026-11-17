# UX-48 — On large chapters, the preview lags about 350 ms behind every keystroke

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Measured (`scripts/latency-probe.mjs` in the QA skill) |
| Area | Live preview while typing in the source |
| Related | PERF-01 (main-thread render), PERF-05 (document replacement), [UX-28](../../06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md) |

## Measurement

Time from a key press in the source editor until the preview text contains the typed characters:

| Document | Size | p50 | p90 | max |
| --- | --- | --- | --- | --- |
| `book/chapters/08-research-plan-implement.md` | 107 KB | 346 ms | 365 ms | 477 ms |
| `fixtures-visual/01-handbook-overview.md` | 6 KB | 86 ms | 88 ms | 90 ms |

Typing next to three Mermaid diagrams (`synth/diagrams-and-math.md`) caused about **2.6 webview
navigations per keystroke** (90 for 34 characters). The DOM sampler (about 500 samples per second)
saw a missing Mermaid image or a scroll offset change in only 1-2 samples per burst, so VS Code's
frame double-buffering hides most of the churn from view. The cost shows up as latency and
extension-host load, not as visible flicker.

## Impact

At 350 ms, the preview visibly trails fast typing on the book's own chapters, and the extension
host (shared with every other extension) is busy for most of each second while typing.

## Suggested direction

As in PERF-01/PERF-05: render off the main thread or incrementally (per changed block), and patch
the webview content instead of replacing the document. Track the two numbers above as a
performance budget in CI (for example p50 < 150 ms on chapter 08).

## Done when

p50 key-to-preview latency on chapter 08 is under 150 ms.
