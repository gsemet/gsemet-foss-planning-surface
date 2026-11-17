# Independent FullCycle Inspector Feedback

**Initial verdict: REWORK.** The coder commit passed its existing scenarios, but did not prove or
enforce several Task 05 lifecycle invariants: theme changes did not queue a bounded render, a
renamed dependency could leave stale output, switching to a non-Markdown editor retained the old
document, serializer requests could build non-Markdown files, and workspace removal left the
watcher/panel lifecycle alive. The inspector adds focused host coverage and repairs only those
paths. Task 06 is not started.

**Final inspector verdict: GO after REWORK.** The inspector repaired the identified lifecycle paths,
added real extension-host coverage for theme changes, non-Markdown editor transitions, and project
workspace removal, and verified source mapping when the preview temporarily owns focus. The trusted
and untrusted host suites pass, the unit suite passes all 36 tests, packaging succeeds, and the
repository checks are clean. Task 06 is not started.

# Task 05: Preview Lifecycle Integration

**Depends on**: Tasks 02, 03, and 04

## Important Information

Before coding, Read FIRST -> Load [05-task-00-READBEFORE.md](05-task-00-READBEFORE.md)

## Applicable Guidelines

| Rule | Application |
| ---- | ----------- |
| VS Code supported APIs | Use Webview panels, serializers, commands, events, and custom editor APIs only where Stable. |
| Stock non-regression | Keep native commands, shortcuts, settings, Markdown plug-ins, and editor associations untouched. |
| Latest-version rule | Bind each result to panel, URI, and document versions before display. |
| Failure behavior | Show progress/diagnostics and visibly stale last-good output; never swap another document. |
| Process hygiene | Cancel builds and remove temporary state when panels close or the extension deactivates. |

## Objective

Integrate the proven build, security, rendering, and source-mapping components into one side preview
that follows the currently active Markdown file and updates from unsaved text.

## Files to Modify/Create

- `package.json`
- `src/extension.ts`
- `src/commands/*`
- `src/preview/*`
- `src/state/*`
- `src/navigation/*`
- `src/diagnostics/*`
- `test/integration/lifecycle*.test.ts`

## Detailed Steps

1. Implement one command opening the active Markdown file's MyST preview to the side, without
      changing default editor associations or stock Markdown commands.
2. Follow the active Markdown editor in this workspace. When the active editor changes to a
      different file, show that file's preview; never show another file's output as the current one.
3. Preserve the last active URI and scroll anchor across hide/show and reload. Missing or moved
      source produces an explicit error, not another document's content.
4. Wire active unsaved edits, relevant local asset changes, theme changes, and explicit refresh
      into the Task 02 build queue without refresh loops.
5. Show pending state during builds. Parse actionable Sphinx diagnostics with source file and line.
   On failure retain last-good HTML, label it stale, and recover on the next valid edit or refresh.
6. Route links actually present in the active file through the validated navigation policy.
      Prevent arbitrary local-file or hostile-scheme navigation.
7. Preserve find support, selectable rendered text, keyboard focus, anchor, scroll, and disclosure
   state across ordinary updates where the corresponding content still exists.
8. Ensure closure, source deletion, workspace removal, reload, and deactivation cancel builds,
   clean temporary roots, and reject late results.
9. Add extension-host tests for open, switch, edit, refresh, failure, and dispose. Do not build
      an unrelated stock-preview feature matrix.

## Acceptance Criteria

- [ ] The side preview follows the active Markdown file and renders its unsaved text.
- [ ] Commands and menus are distinct from stock Markdown IDs and appear only in intended contexts.
- [ ] Reload restores the last source and scroll anchor without cross-document content leakage.
- [ ] Dirty edits, referenced local assets, themes, rename/delete, and explicit
      refresh trigger correct bounded updates without loops.
- [ ] Pending, success, stale, diagnostic, missing-source, and recovery states are visually
      and programmatically distinguishable.
- [ ] Same-page, local-file, and external links used by the active file follow the validated policy.
- [ ] Find, copy, focus, anchor, scroll, and disclosure state survive ordinary updates where
      applicable.
- [ ] Close/reload/deactivate leaves no process, watcher, late message, or temporary-root leak.
- [ ] Focused active-file lifecycle tests pass in an isolated extension host.

## Testing Strategy

Switch between two Markdown editors in the extension host. Use delayed and failing builds to
test active-file identity, stale-result rejection, disposal, and recovery.

## Notes

This task integrates previously proven components. Fixed-file, native diff, and optional editing
remain outside scope.
