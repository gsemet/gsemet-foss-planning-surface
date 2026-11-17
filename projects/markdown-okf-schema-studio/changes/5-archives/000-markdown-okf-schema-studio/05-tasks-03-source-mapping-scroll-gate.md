## Independent FullCycle Inspector Review

**Initial verdict: REWORK.** The Sphinx attribute gate and focused interpolation tests passed,
but the host accepted messages from the old stage after the active editor changed and the
host-side `ScrollSyncController` was not on the production path. Those gaps could permit a
wrong-editor reveal and made the loop-suppression evidence incomplete.

The inspector repair adds an active-panel/stage identity guard, uses the controller to suppress
the source-side echo caused by preview reveals, and adds an extension-host regression test for the
editor-transition race. The final verdict is recorded after the focused checks are rerun.

## Final Inspector Verdict

**GO.** The repair was validated independently. The active panel and stage must agree before a
Webview message is accepted, and source-side visible-range updates use the same document, version,
and request context as the programmatic reveal. The generated Webview runtime is executed against a
fake DOM for source/preview scroll, rapid replacement, image load, window resize, visual-viewport
resize, body resize observation, click/double-click reveal, and stale-document rejection.

Passing focused checks:

- `uv run pytest tests/test_sphinx_preview_mapping.py`: 4 tests.
- `fnm exec -- npm run compile`: TypeScript compile.
- `fnm exec -- npm run test:unit`: 29 tests.
- `fnm exec -- npm run test:integration`: isolated extension-host scenarios, including the
   active-editor transition race.
- `just check-justfile` and `just book-check`.

The full `uv run pytest` run has 9 unrelated failures in `src/sphinx_animation/`; all 4 Task 03
mapping tests pass. No Task 04 work is included in this verdict.

# Task 03: Source Mapping and Scroll Gate

**Depends on**: Task 01 (`GO` required)

## Important Information

Before coding, Read FIRST -> Load [05-task-00-READBEFORE.md](05-task-00-READBEFORE.md)

## Applicable Guidelines

| Rule | Application |
| ---- | ----------- |
| [Repository constitution](../../../../CONSTITUTION.md) | Keep preview hooks within the full-Sphinx architecture. |
| [Build-system guideline](../../../guidelines/build-system-setup.guideline.md) | Ensure normal builders are unchanged when preview mode is disabled. |
| Honest mapping | Never assign a fabricated source line to generated or originless output. |
| Required fidelity | Prove stable block/line synchronization; pixel precision is not required. |
| Existing transformations | Preserve active-file line origins if the draft-banner hook runs. |

## Objective

Add a preview-only Sphinx source-position hook and prove stable editor-to-preview and
preview-to-editor block/line synchronization on a long active Markdown file, including directives,
figures, hidden blocks, and inserted text.

## Files to Modify/Create

- `sphinx/preview_source_mapping.py`
- `sphinx/conf.py`
- `tests/fixtures/sphinx-preview-mapping/*`
- `tests/test_sphinx_preview_mapping.py`
- `src/mapping/*`
- `src/webview/scrollSync.ts`
- `test/mapping/*`
- `test/integration/sourceMapping.test.ts`
- `docs/feasibility-source-mapping.md`

## Detailed Steps

1. Implement a Sphinx extension/hook that is enabled only by an explicit preview-mode environment or
   config flag. Normal HTML, single HTML, PDF, RevealJS, and Confluence builds must not receive
   mapping attributes or changed output.
2. During doctree/HTML processing, attach source identity and one-based line metadata to mappable
   blocks of the active file, such as headings, paragraphs, lists, directives, figures, and code.
3. Account for the existing draft banner inserted in `_on_source_read`. Ensure added banner lines do
   not shift mappings for the original chapter body. Mark the generated banner itself non-navigable
   unless it has an explicit real origin.
4. For included or generated blocks with no trustworthy source location, omit clickable mapping
   metadata rather than inventing a position in the active file.
5. Parse mapping metadata into an ordered block index and route mapped preview interactions to
   the active `TextDocument` without confusing one open file with another.
6. Implement source-to-preview and preview-to-source block/line synchronization with interpolation
   between mapped blocks. Add loop suppression, stale-document checks, image-load stabilization, and
   active-document identity checks so rapid scrolling never targets the wrong editor.
7. Preserve the nearest mapped block and proportional position across ordinary rerenders. Test long
   pages, top/middle/end, inserted text, images, code fences, collapsed disclosure blocks,
   `{only}`/`{exclude}` hidden content, zoom, resize, and rapid alternating scroll.
8. Add pytest HTML assertions for mapping attributes and normal-build non-regression. Add extension
   integration tests for click/double-click reveal and both scroll directions.
9. Record drift and a `GO` only if long-page synchronization remains stable at block/line
   granularity with no oscillation, wrong editor, cumulative drift, or invented locations.

## Acceptance Criteria

- [ ] Preview-mode HTML exposes real source file and one-based line metadata for mappable blocks
   from the active Markdown file.
- [ ] Generated or originless fragments contain no fabricated navigation target.
- [ ] The draft banner does not shift mappings for original source content.
- [ ] Included content without a trustworthy origin does not navigate to a fabricated line.
- [ ] Normal Sphinx builders produce no preview mapping attributes and retain equivalent relevant
      body output, excluding known nondeterministic metadata if any is documented.
- [ ] Long-file editor-to-preview and preview-to-editor tests pass after inserted text, images,
      hidden blocks, resize, and zoom.
- [ ] Rapid alternating scroll produces no feedback loop, wrong-editor reveal, or cumulative drift.
- [ ] Unmappable content interaction is inert or explains that no source location exists.
- [ ] Focused pytest, TypeScript unit, and isolated extension-host tests pass.
- [ ] The feasibility report records fixtures, commands, observed drift, unmappable cases, and an
      evidence-backed `GO` or `NO-GO`.

## Testing Strategy

Use compact Sphinx fixtures for exact mapping assertions and one representative long file for
browser/extension-host behavior. Instrument host/Webview messages to assert URI, document version,
panel identity and echo suppression. Capture images at top/middle/end before and after insertion
to make mapping drift reviewable.

## Notes

This is a hard gate. Pixel-level equality is not required. Stable block/line behavior is required;
failure means the specified preview must not proceed to product integration.
