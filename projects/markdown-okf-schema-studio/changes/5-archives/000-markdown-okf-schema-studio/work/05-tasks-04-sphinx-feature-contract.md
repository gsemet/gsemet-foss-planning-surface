# Task 04: Sphinx Feature Contract

**Depends on**: Task 02 (`GO` required), Task 03 (`GO` required)

## Important Information

Before coding, Read FIRST -> Load [05-task-00-READBEFORE.md](05-task-00-READBEFORE.md)

## Applicable Guidelines

| Rule | Application |
| ---- | ----------- |
| [Repository constitution](../../../../CONSTITUTION.md) | Validate actual full-Sphinx HTML and MyST behavior. |
| [Build-system guideline](../../../guidelines/build-system-setup.guideline.md) | Keep normal book builds unchanged. |
| HTML target boundary | Classify non-HTML extensions; do not promise PDF, RevealJS, or Confluence output. |
| No silent degradation | Assert an expected HTML artifact, not parser recognition alone. |
| Fixture isolation | Keep test content outside book chapter sources and stage one active fixture. |

## Objective

Prove that representative MyST syntax in the currently open file produces actual HTML through the
project's Sphinx configuration, with actionable diagnostics when that file needs an unavailable input.

## Files to Modify/Create

- `tests/fixtures/sphinx-liveview-features/*`
- `test/rendering/*`
- `test/integration/projectFeatures.test.ts`
- `docs/active-file-rendering.md`
- Extension build/diagnostic modules from Task 02 only where fixture execution exposes a defect

## Detailed Steps

1. Create a compact Markdown fixture with headings, admonitions, math, a directive, links, and a
   local image; open it as the active document without saving an edit.
2. Assert actual semantic HTML and resource output for those constructs using the project's
   MyST/Sphinx configuration. Do not treat an exit code or recognized syntax as proof of rendering.
3. Add a fixture with a missing include or unsupported directive and verify an actionable error,
   while retaining a visibly stale last-good render without a Markdown fallback.
4. If the active file uses a citation or another project-specific extension, verify it with an
   existing referenced input. Do not regenerate `refs.bib`, navigation, or the whole book as part
   of this fixture.
5. Record which active-file MyST constructs were checked and any unsupported syntax. Do not claim
   parity with all configured extensions or other output builders.

## Acceptance Criteria

- [ ] One active unsaved Markdown fixture renders real MyST headings, admonitions, math, directives,
   links, and a local image with checks against their resulting HTML.
- [ ] A missing referenced input or unsupported directive yields a useful diagnostic and leaves
   the last good preview visibly stale, without a Markdown fallback.
- [ ] A file without citations previews without bibliography regeneration or a book-wide build.
- [ ] No unsupported syntax is emitted through a Markdown fallback or raw-source placeholder.
- [ ] Focused rendering unit and extension-host integration tests pass.

## Testing Strategy

Use DOM-aware assertions against the active-file staging path. Check resulting elements and local
resources, plus a negative missing-input case; do not invoke the multipage book server.

## Notes

This task closes the active-file rendering gate. Third-party Markdown-It syntax remains in the
stock preview; it is not required in the MyST view.
