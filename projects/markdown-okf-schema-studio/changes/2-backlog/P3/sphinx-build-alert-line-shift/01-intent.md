# Sphinx build path: alert rewrite still shifts later lines

`src/node-services/build/sourceTransforms.ts` has its own alert rewrite that shifts later lines by
one for each alert followed directly by text. The preview path was fixed in PR #185; align the
build path (diagnostic line numbers in builds).

Note 2026-11-01 (CR 223 round 2 and round 3): the same module, `src/node-services/build/sourceTransforms.ts:22-56`
(`expandGithubAlerts`, used by `snapshotWorkspace.ts:397`), also keeps the old "alert ends at the first
unquoted line" rule. Since CR 223 the preview ends the alert with `blockQuoteEnd` (lazy continuation lines),
so a built snapshot and the preview disagree on lazy lines. Fix both together: make the build path use
`blockQuoteEnd`, and keep line numbers stable. No requirement covers that file today.
