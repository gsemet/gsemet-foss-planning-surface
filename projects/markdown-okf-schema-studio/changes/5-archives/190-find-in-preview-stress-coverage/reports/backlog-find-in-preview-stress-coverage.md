# Find in preview is not covered by the stress suite

Source: release 1.0.0 hotfix (PR #183, https://github.com/gsemet/markdown-okf-schema-studio/pull/183).
After 1.0.0.

`test/integration/findInPreview.test.ts` runs only in the trusted suite, so a timing race in it
(late block editor focus) surfaced only as a one-off heavy failure on main. Add the find scenario
(cream and dark, including replace) to the stress plan so timing regressions show up as a stress
verdict.
