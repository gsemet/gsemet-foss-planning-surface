# T1 — Change bar in the margin, square TOC accent, commit guidelines in .agents/guidelines

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-026 (branch
`fix/change-bar-and-guidelines` from origin/main). Work ONLY there; `node_modules`/`.venv` are
symlinks to the main checkout: never delete or stage them. Read `00-request.md` and `rules.md`.

## Change

1. Guidelines: `git mv .github/guidelines/git-commit-allowed-scopes.md .agents/guidelines/` and the
   same for `git-commit-message.guidelines.md` (remove `.github/guidelines/` if empty). Update every
   reference (AGENTS.md lines ~35-36, grep the repo excluding node_modules/out/.agents/changes) and
   `guidelines.lock.json` (`target_path` of the guideline and of its file → `.agents/guidelines`).
   Check `guidelines.yml` for a target setting (the ai-guidelines tool may live in
   /Users/az02065/Projects/DevTools/ai-guidelines: read its docs/README read-only to find how the
   target directory is configured, and configure it the supported way). Do not edit the guideline
   files' content.
2. Change bar (src/preview/previewStyles.ts ~2508, `[data-sphinx-preview-changed]`): see the
   decision update in 00-request.md — ONE column for every bar, as close as possible to the page's
   left margin (same x for list items, nested blocks, code, headings), square ends (never follow
   the block's border-radius). Draw the 3px green bar in the margin, without changing the layout of the
   block or its neighbours (no padding/margin change on the block; e.g. a pseudo-element positioned
   outside, or an outset shadow offset). Check: it must not be clipped by an ancestor
   (overflow hidden/auto), must stay visible in narrow panes and at the first element, must not
   overlap the fold/comment/edit affordances in the left margin, must work for every block kind
   that gets the attribute (paragraph, heading, list, table, code, admonition, image), RTL
   (inline-start), and light/dark/cream themes. Keep consecutive changed blocks reading as one bar
   if they did before.
3. TOC current item (~2184): keep the bar and tint but square corners on that item only (other TOC
   buttons keep their 4px rounding).

## Tests

- Unit (test/webview/previewStyles.test.ts): assert the change bar rule no longer uses an inset
  shadow at the text edge and is offset ~12px; the TOC current rule has border-radius 0. Fail first.
- Visual (test/visual/scenarios.ts): find the scenario(s) showing the incoming-change mark and the
  TOC (grep `data-sphinx-preview-changed`, `toc`); add assertions: the bar's computed left edge is
  >= 10px left of the block's text left edge, the block's text left edge is unchanged vs an
  unchanged block, and the TOC current button has 0 radius. Capture screenshots (change bar light +
  dark, TOC open) for the PR and report their paths.

## Docs

CHANGELOG Unreleased bullet(s) (user-facing: change bar no longer touches the text; TOC current
section square). AGENTS.md updated for the guidelines.

## Gates (foreground, windowless only)

`npx tsc -p .`, `just check`, `just visual`. No integration/e2e/preflight locally.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/026-change-bar-toc-corners-guidelines/reports/T1-r<round>.md`.
