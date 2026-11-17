## Summary

A document containing an unclosed directive (for example a lone ```` ```{list-table} ````), an unclosed
`:::{table}` block, a dangling label `(name` / `)=`, or an empty directive at the end of the file made
the preview fail to render. The preview now shows the offending lines as a plain code block and
renders the rest of the document normally.

## Deliverables

```mermaid
flowchart LR
  P[MyST parser] --> E[directive error node] --> N[neutralizeDirectiveErrors] --> C[raw source code block]
```

- New pass `neutralizeDirectiveErrors` (`src/core/render/mystDirectiveErrors.ts`), wired into the
  MyST renderer, replaces every directive error node with a code block of its source lines.
- 11 unit tests for syntax errors: unclosed backtick and colon directives, unclosed label, label
  without target, nested unclosed directive, empty directive at end of file.
- Two visual end-to-end scenarios (cream and dark) on a new fixture.

After (cream / dark): raw lines shown, the rest of the page rendered. There is no "before"
screenshot because the fixture did not render at all.

- shots/after-cream.png
- shots/after-dark.png

## Autonomous decisions

- Any unclosed fence or directive, dangling label or empty trailing directive renders its raw source
  lines as a code block; no visible hint is added.
- Syntax-error coverage added as parser unit tests plus one preview end-to-end scenario per theme.

## Internal references

CR 111 (from backlog item bug-crash-extension); requirement SwRS-MDOKFSTUDIO-MYST-096.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
