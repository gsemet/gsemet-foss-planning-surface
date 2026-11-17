## Summary

Dropdown admonitions (`:class: dropdown`) gave no hint of whether they were collapsed or expanded.
The preview now shows a chevron at the right of the title: it points right when collapsed and down
when expanded, and rotates on toggle. It applies to every admonition kind and every theme.

## Deliverables

Before (no indicator) and after (chevron), cream theme, collapsed:

| Before | After |
| --- | --- |
| ![before](reports/shots/before-cream-collapsed.png) | ![after](reports/shots/after-cream-collapsed.png) |

Expanded, dark theme:

| Before | After |
| --- | --- |
| ![before](reports/shots/before-dark-expanded.png) | ![after](reports/shots/after-dark-expanded.png) |

(Screenshots to be pushed to the assets branch and linked by raw URL by the stack driver.)

The change is CSS in `src/core/directives/admonition.ts`, with a unit test on the generated styles,
a new assertion in the MyST gallery visual scenario, a requirement scenario and a changelog entry.

## Autonomous decisions

- Chevron at the right of the title, right when collapsed, down when expanded.
- Default state follows MyST: `:class: dropdown` starts collapsed.
- The renderer only supports `:open: true` for starting expanded, not a `dropdown-open` class;
  that class is left out and can be a follow-up.
- `just check` passes except the requirements-lint step, which fails only inside the worktree
  because `uv run` resolves an okfreq without `--check-links`; validated with the main checkout's
  binary (0 errors). One unrelated flaky wikilink-search unit test passed on re-run.

## Internal references

CR 108, backlog item bug-dropdown-state.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
