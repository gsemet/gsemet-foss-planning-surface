# Change Specification: a project icon for T3 Code through `t3.json`

## Goal

T3 Code shows chantier's repository with its own icon. T3 Code reads the `iconPath` field of a
`t3.json` at the repository's root first; the repository has no file T3 Code would find on its own
(no favicon, `app/icon.*`, `assets/icon.*`, `assets/logo.*`, `.idea/icon.svg` or `index.html`
icon) and no tracked logo (its images are diagrams and screenshots). So the change draws a logo and
points `t3.json` to it.

## What changes

All paths are relative to the code repository's root (`C:/Users/gaeta/Projets/chantier`).

### 1. `docs/logo.svg` (new)

A simple square SVG logo on the theme of a building site (chantier), drawn by hand by the Coder:

- Square: the root `<svg>` has `xmlns="http://www.w3.org/2000/svg"` and a square `viewBox`
  (for example `0 0 64 64`); `width`/`height`, if given, are equal.
- Legible at 16 px: a few bold shapes (for example a crane, a hard hat, a safety cone or a
  stripe band), thick strokes or filled shapes, a small palette with clear contrast; no fine
  detail that vanishes at 16 px.
- Plain SVG only: no `<text>`, no font reference (no `font-family`, no `@font-face`), no
  `<image>`, no raster data (no `data:` URI), no external reference (no `href` to a URL), no
  script.
- UTF-8, small (a few hundred bytes to a few kilobytes).

### 2. `t3.json` (new, at the repository's root)

It holds exactly these two fields, nothing else:

```json
{
  "$schema": "https://t3.codes/schema/t3.json",
  "iconPath": "docs/logo.svg"
}
```

`iconPath` is relative to the repository's root and stays inside it, as T3 Code requires. The file
is UTF-8 with a final newline, two-space indentation.

### 3. The PR's description

- It shows the final `t3.json` in a JSON code block, as the request asks ("Montre-moi le
  `t3.json` final").
- It shows the logo (the image of `docs/logo.svg` at the PR's head) so the user sees it before
  merging.
- It proposes, without adding them to `t3.json`, the `scripts` entries T3 Code could run, taken
  from the `justfile`. Each entry has `name`, `command` and, where one fits, `icon` (one of `play`,
  `test`, `lint`, `configure`, `build`, `debug`). The proposal is:

  ```json
  "scripts": [
    { "name": "Check", "command": "just check", "icon": "lint" },
    { "name": "Test", "command": "just test", "icon": "test" },
    { "name": "Scenario", "command": "just scenario", "icon": "test" }
  ]
  ```

  The Driver may also name, as a candidate only, a setup entry with `"runOnWorktreeCreate": true`
  (for example `uv sync --locked --group dev`, the first line of the `justfile`'s `tools` recipe),
  saying that the user decides. Nothing of this goes into the repository.

## Decisions carried from `02-answers.md`

- t3-Q1 A: the Coder draws a simple square SVG logo on the building-site theme at
  `docs/logo.svg`; `t3.json` points to it. (Sections 1 and 2.)
- t3-Q2 A: the change goes through the batch as a normal PR that the user merges, not an
  uncommitted edit; the final `t3.json` is shown in the PR's description. (Section 3.)
- Settled: `t3.json` holds `$schema` and `iconPath` only; the scripts (`just check`, `just test`,
  `just scenario`) are proposed in the PR's description and not added. (Sections 2 and 3.)
- Settled: the logo is a plain SVG, legible at 16 px, with no text, no external font and no raster
  image. (Section 1.)

## Out of scope

- Any `scripts` entry in `t3.json`, and any other field.
- A favicon, `assets/` folder, `.idea/icon.svg` or any other icon file T3 Code's fallbacks read.
- Using the logo elsewhere (the README, the web board, the plugin manifests, the docs pages,
  `.gitattributes`).
- A new test or check for `t3.json` or the logo: the evidence below is a one-off check the Driver
  runs and reports in the PR; `just test` stays as it is.
- The CLI, the cards, the hooks, the agents, the scenario and the release notes.

## Evidence

Run in the CR's worktree, at the rebased head the Driver pushes:

1. `t3.json` parses as JSON and its keys are exactly `$schema` and `iconPath`, with the values
   above.
2. `iconPath` resolves, from the repository's root, to a file tracked by git
   (`git ls-files docs/logo.svg` prints it) that stays inside the repository.
3. `docs/logo.svg` parses as XML, its root is `svg` in the SVG namespace, its `viewBox` is square,
   and it holds no `text`, `image`, `script` or `foreignObject` element, no `font-family` and no
   `href` to a URL or `data:` URI. (The Driver checks this with a short one-off command, for
   example a Python one-liner with `xml.etree.ElementTree`, and quotes its output in the PR.)
4. The logo, rendered at 16 px and at a larger size, is legible: the PR's description shows it.
5. `just check` passes.

No host and default matrix: nothing here depends on the host or on a configured value. No check
guards a shipped file: the change adds none.

## Gates (AGENTS.md)

- `just check`, in the worktree, at the rebased head the Driver pushes, before the first push; it
  must pass (Linux, macOS and Windows in CI).
- No `just eval-dry-run`: the change touches neither the CLI's `src/` nor `evals/kit/`.
- No `just scenario` for this CR: it touches neither the CLI, nor the cards, nor the scenario (a
  root configuration file and a docs image only). The batch's own rule, that the CR on top of the
  stack passes `just scenario` locally (`chantier gate`) before the user merges, stays the batch's
  and is not owed by this change's content.
- No `just mod`: nothing under `hooks/` or `types/`.
- No pane screenshot: the CR board pane is not touched.
- `main` is protected: a branch, a PR, merged by rebase when CI is green, by the user.

## Open questions

None.
