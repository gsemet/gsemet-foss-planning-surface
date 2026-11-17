# 190 — Find in preview: stress coverage

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # Find in preview is not covered by the stress suite
> 
> Source: release 1.0.0 hotfix (PR #183, https://github.com/gsemet/markdown-okf-schema-studio/pull/183).
> After 1.0.0.
> 
> `test/integration/findInPreview.test.ts` runs only in the trusted suite, so a timing race in it
> (late block editor focus) surfaced only as a one-off heavy failure on main. Add the find scenario
> (cream and dark, including replace) to the stress plan so timing regressions show up as a stress
> verdict.
