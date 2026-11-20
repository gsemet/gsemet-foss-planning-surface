# Before and after: CR-349

Before: base `e5b4b27e957250b609bbccdfa3a4138d7459c0c0`. After: head
`abeb761a9ea8815888f2bb59d3e114ef83979598`.

No pair captured. The change is test-harness code with no visual or product effect, so there is no
screen to compare. The one behaviour that differs (the error of a capture whose toolbar tooltip
stays shown) needs a stuck tooltip in a real VS Code window, which runs only in CI (Linux, xvfb) and
cannot be forced there without the very instability it diagnoses (spec, Evidence 4). The path is
judged by reading the code in `../../verify.md`, claim 4, and stays in the PR's Known gaps.
