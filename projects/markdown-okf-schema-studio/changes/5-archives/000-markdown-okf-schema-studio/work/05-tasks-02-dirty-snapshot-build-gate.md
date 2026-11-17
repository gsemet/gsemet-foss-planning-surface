# Task 02 Inspector Review

**Verdict: ACCEPTED.** The implementation satisfies the dirty-buffer and isolated-build gate after
inspector corrections. The inspector found two reproducible gaps: missing-input diagnostics did
not identify the source Markdown file, and edits to a referenced file were ignored when that file
was closed. The fix propagates source-file context through recursive staging, tracks missing local
dependencies, canonicalizes dependency paths, and refreshes referenced paths through a
workspace-bounded file watcher. Preview setup now also disposes the panel, watcher, and queue
together if resource creation fails.

Independent validation passed: `fnm exec -- npm run compile`; 21 unit tests; trusted and untrusted
extension-host integration tests, including closed-include refresh and newest-request behavior;
real-Sphinx include and missing-input probes; `fnm exec -- npm run package`; `just check-justfile`;
and `just book-check`. The final integration rerun measured 787 ms initial render, 515 ms normal
edit refresh, and a 500 ms injected obsolete-build delay, with no residual Sphinx process or
temporary stage. Task 02 is `GO`; Tasks 03-07 remain blocked by their own stated gates.

## Task 02: Dirty Snapshot and Isolated Build Gate

**Depends on**: Task 01 (`GO` required)

## Important Information

Before coding, Read FIRST -> Load [05-task-00-READBEFORE.md](05-task-00-READBEFORE.md)

## Applicable Guidelines

| Rule | Application |
| ---- | ----------- |
| [Repository constitution](../../../../CONSTITUTION.md) | Preserve full-Sphinx rendering, determinism, and `uv run` usage. |
| [Build-system guideline](../../../guidelines/build-system-setup.guideline.md) | Keep normal book builds unchanged. |
| Source integrity | Never save buffers or write generated files into the worktree. |
| Latest-version rule | Version every snapshot request and discard canceled or obsolete build results. |
| Loud failure | Surface Sphinx diagnostics; never substitute another renderer. |

## Objective

Prove the unsaved text of the currently open Markdown file can be rendered by the project's
MyST/Sphinx HTML configuration in temporary staging, without changing that file or book outputs.

## Files to Modify/Create

- `src/build/snapshotWorkspace.ts`
- `src/build/sphinxBuild.ts`
- `src/build/buildQueue.ts`
- `test/build/*`
- `test/integration/dirtySnapshots.test.ts`
- `docs/feasibility-dirty-snapshots.md`

## Detailed Steps

1. Stage only the active `TextDocument` text and inputs it references in a writable temporary
   project. Preserve relative paths for local images or includes when present. Do not require
   regenerated bibliography, toctree, or release metadata to preview an ordinary file.
2. Invoke the project's MyST/Sphinx HTML configuration against this staged input with isolated
   doctree and output paths. If the configuration cannot render one file without a whole-book
   build, record the specific blocker and stop rather than writing book sources.
3. Keep writable staging directories separate from linked read-only inputs so generated output
   cannot follow a symlink into the worktree. Do not call `just book-prepare`.
4. Track the active document version and build request ID. Debounce, terminate or supersede obsolete
   work, and discard any result whose snapshot versions no longer match current documents.
5. Refresh for edits to the active buffer and any local image or include it references. Report
   missing inputs without silently regenerating them or starting a book-wide build.
6. Prove unsaved edits, rapid changes, newest-version wins, cancellation, and recovery after a
   failing directive. Measure initial and edit-to-render latency for a representative file.
7. Compare hashes before and after to prove the active source and production outputs are unchanged.

## Acceptance Criteria

- [x] Unsaved edits to an open file render as authentic MyST/Sphinx HTML without saving it.
- [x] A different open Markdown file can be selected and previewed without rebuilding the book.
- [x] Referenced local images and includes resolve when present; missing inputs are diagnosed.
- [x] A slow obsolete build cannot replace a newer result; cancellation/disposal leaves no process
      or temporary-directory leak.
- [x] Sphinx errors return actionable file/line diagnostics and preserve the prior successful result
      as explicitly stale; no fallback renderer is used.
- [x] Preview execution never calls `just book-prepare`.
- [x] Hash/diff assertions prove the source file and production output are unchanged.
- [x] The feasibility report records measured latency, dependency cases, commands, and `GO` or
      `NO-GO` evidence.

## Testing Strategy

Use TypeScript unit tests for active snapshots, queue supersession, and cleanup. Use extension-host
integration tests with an unsaved file and a controllably delayed build to prove latest-version
behavior and source immutability.

## Notes

Do not reuse `_build/livereload/` or production doctrees. Stop if active unsaved rendering or
source integrity cannot be proven; unrelated dirty documents are not part of this gate.
