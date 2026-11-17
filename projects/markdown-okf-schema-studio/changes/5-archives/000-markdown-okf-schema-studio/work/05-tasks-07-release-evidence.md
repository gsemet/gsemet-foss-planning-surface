# Independent Inspector Review

**Initial verdict: REWORK.** Commit `613f0d0` documented the unperformed current-window and
VoiceOver checks honestly, but its aggregate recipe did not preserve the per-stage logs or
machine-readable reports named by the evidence, and the recorded VSIX size/count was stale. The
referenced artifacts predated the inspected aggregate run. The inspector added reproducible
artifact capture, an explicit source-mapping check, and a lockfile audit stage.

**Final inspector verdict: ACCEPTED with release blocked.** The corrected campaign passed and
fresh artifacts are reviewable. The installed-VSIX current-window observation and VoiceOver or
assistive-technology speech check remain unperformed or unobservable; neither is inferred as a
pass. The defensible decision remains `NO RELEASE`.

# Task 07: Release Evidence and Repository Gates

**Depends on**: Task 06

## Important Information

Before coding, Read FIRST -> Load [05-task-00-READBEFORE.md](05-task-00-READBEFORE.md)

## Applicable Guidelines

| Rule | Application |
| ---- | ----------- |
| [Repository constitution](../../../../CONSTITUTION.md) | Run required book gates for shared Sphinx/build changes and preserve full-Sphinx output. |
| [Build-system guideline](../../../guidelines/build-system-setup.guideline.md) | Validate normal production/development behavior and fail loudly. |
| Evidence discipline | Record command, environment, result, and artifact for every release claim. |
| Release boundary | State that fixed-file, native MyST diff, and editing modes are not included. |

## Objective

Verify direct use of the active-file MyST preview in the current VS Code window, its hard gates,
and stock-preview non-regression. Document what was tested without claiming book-wide or stock parity.

## Files to Modify/Create

- `docs/release-evidence.md`
- `docs/active-file-checks.md`
- `docs/security-evidence.md`
- `docs/known-limitations.md`
- `README.md`
- `CHANGELOG.md`
- `test/release/*`
- `justfile` only if final check/package recipes need correction

## Detailed Steps

1. Record tested VS Code, Node, Python, Sphinx, and extension versions.
2. Before installing, capture basic stock preview behavior on a Markdown file. Repeat after
   installing and with both stock and MyST previews open; do not claim full stock parity.
3. Run every Task 01 hard-security probe and record CSP, trust, resource-root, raw HTML, active SVG,
   event attribute, `srcset`, CSS URL/import, font/media, scheme, traversal, encoded traversal, and
   symlink results.
4. Open a normal Markdown file with MyST syntax, edit it without saving, switch to another file,
   and verify only the active document appears. Cover stale cancellation, diagnostics, recovery,
   resource safety, and no source writes.
5. Run focused MyST output checks for headings, admonitions, math, a directive, and a local image;
   verify a missing input produces a diagnostic rather than triggering a book build.
6. Test two-way scrolling on a long file before and after insertion, resize, and rapid scrolling.
7. Check links, find, theme, keyboard access, reload, and missing/deleted active sources.
8. Record observed results for these active-file checks and all hard gates. Do not create a
   P01-P24 release matrix; native MyST diff is out of scope.
9. Run focused compile, unit, integration, browser, accessibility, and package checks through
   the targeted just recipe. Run `just check-justfile` for justfile changes.
   Verify `npm ci` from the nested extension package uses its Artifactory `.npmrc` and Node 24;
   inspect the lockfile for public registry URLs or credentials before packaging.
   Run `just vscode-sphinx-liveview-build` and `just vscode-sphinx-liveview-install` to package
   and install the local VSIX in the profile used by the current window, passing an explicit profile
   when needed (or using the documented manual Install from VSIX fallback). Reload this white-paper
   workspace window and exercise the command on a real chapter. Document update/reinstall steps;
   development-host tests alone do not establish current-window usability.
10. If shared Sphinx configuration or book output changed, run `just book-check` and
   `just preflight`; do not make normal book builds depend on the extension.
11. Document install commands, trust behavior, diagnostics, known gaps, and deferred modes.
12. Record `RELEASE` only if hard gates and required checks pass; otherwise record `NO RELEASE`.

## Acceptance Criteria

- [ ] Evidence records exact tool versions, commands, results, and artifact paths.
- [ ] The stock Markdown preview still works after installation with both views open.
- [ ] All five hard release gates have passing automated and/or explicit manual evidence.
- [ ] The active unsaved file renders the newest MyST output without source/output writes.
- [ ] Missing referenced content produces diagnostics without a book-wide build.
- [ ] Long-file mapping shows stable two-way block/line behavior with no invented locations.
- [ ] The active preview passes editor-switch, reload, failure, theme, link, and accessibility checks.
- [ ] Focused compile, tests, integration, browser, accessibility, and packaging checks pass.
- [ ] Nested-package install and VSIX packaging use the corporate npm registry and Node 24;
   the lockfile has no public registry URLs or committed credentials.
- [ ] The locally installed VSIX works in the current white-paper workspace after window reload;
   the README explains the `just` targets, manual fallback, updating, and profile-wide scope.
- [ ] `just check-justfile` passes for justfile changes; book checks pass if shared build code changed.
- [ ] Normal book builds contain no preview metadata and do not depend on the extension.
- [ ] README and limitations do not claim full book, fixed-file, native MyST diff, stock parity,
      or first-release editing support.
- [ ] `release-evidence.md` ends with an evidence-backed `RELEASE` or `NO RELEASE` decision.

## Testing Strategy

Use one reproducible release script or test entry point to aggregate focused checks without hiding
individual failures. Preserve machine-readable reports and reviewable screenshots. Manual checks
must state setup, exact actions, expected result, observed result, and reviewer/date.

## Notes

This task validates and documents; it must not conceal defects with evidence formatting. If a
hard gate fails, the result is `NO RELEASE`. Optional editing remains outside the first release and
requires a separate specification for caret mapping, IME, paste/drop, undo, synchronization, and
accessibility.
