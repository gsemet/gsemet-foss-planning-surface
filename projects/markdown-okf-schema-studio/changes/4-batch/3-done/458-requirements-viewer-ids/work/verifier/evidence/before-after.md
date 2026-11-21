# Before and after, CR-458

Before: detached worktree of origin/main at 9c70477acdc79625be4a4fbcbaa52041cbae1a6c (test/site has no diff from the CR's base e0c7836c). After: 4ddd1ded94b3b2c4de59d6830d37af1e0aa73811.
Site: `writeViewerPages` over `frozenReport()` with titles replaced by "<Use case|Behaviour> demo number N of <scope>" (made-up, no ID in them), loaded by file URL in Chromium (1280x800, then 390x844). Script: work/scratch/capture.cjs (`node capture.cjs <repo> <label> <outDir> <siteDir>`). Facts: before-facts.json, after-facts.json.

| Step | Before | After | What it shows |
|---|---|---|---|
| 1 use case page | before-step1-use-case.png | after-step1-use-case.png | eyebrow, crumbs |
| 2 behaviour page | before-step2-behaviour.png | after-step2-behaviour.png | eyebrow, four crumbs |
| 3 search `StRS-MDOKFSTUDIO-BLOCK-014` | before-step3-search.png | after-step3-search.png | Nothing matches / use case |
| 4 `block-14`, `BLOCK-014` | before-step4a-search.png, before-step4b-search.png | after-step4a-search.png, after-step4b-search.png | Nothing matches / use case then behaviour |
| 5 `14`, `014` | before-step5-search.png, before-step5b-search.png | after-step5-search.png, after-step5b-search.png | short IDs / full IDs, ID matches first |
| 6 390 px | before-step6-behaviour-390.png, before-step6-usecase-390.png | after-step6-behaviour-390.png, after-step6-usecase-390.png | wraps inside the page |

Images show no local path and no username (page content only). The header logo is a broken image: the file-URL capture has no site assets, same before and after.
