# Retro — 287-cr-retro

| What happened | Root cause | Process fix |
| --- | --- | --- |
| `just orchestrator` failed after the CR was registered | The Chief of Staff wrote `status: active` by hand in a direct-mode CR; the header allows only working, wait-ci, ready, blocked, landed | None to the guideline (the header values are listed there); direct mode copies the header from an existing CR instead of writing it from memory |
| Rebase after #355 merged, no conflict | Both PRs touched `release-process.guidelines.md` in different places | None: worked as intended |
