## Summary

T3 Code shows a project with the icon named by the `iconPath` field of a `t3.json` at the repository's root. The repository had no file T3 Code finds on its own and no logo, so it showed a default icon. This PR draws a small building-site logo and points a new `t3.json` to it.

## Deliverables

The final `t3.json`, at the repository's root:

```json
{
  "$schema": "https://t3.codes/schema/t3.json",
  "iconPath": "docs/logo.svg"
}
```

The logo, `docs/logo.svg` (a 64 x 64 square: a crane in amber on a dark rounded tile, a hanging load, a red safety cone on an amber ground line; bold filled shapes and thick strokes, a four-colour palette, so it stays legible at 16 px). Its source, 520 bytes, is the whole file:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">
  <rect width="64" height="64" rx="10" fill="#1f2937"/>
  <path d="M10 54V12h6v42z" fill="#f59e0b"/>
  <path d="M10 14h44v6H10z" fill="#f59e0b"/>
  <path d="M46 20v14" stroke="#f9fafb" stroke-width="3"/>
  <rect x="40" y="34" width="12" height="8" fill="#f9fafb"/>
  <path d="M6 58h52" stroke="#f59e0b" stroke-width="4"/>
  <path d="M24 56l6-14h4l6 14z" fill="#ef4444"/>
  <path d="M27 50h10" stroke="#f9fafb" stroke-width="3"/>
</svg>
```

The logo rendered at 256 px (left) and 16 px (right) is shown below (at `1ed0389`).

![The logo at 256 px and 16 px at 1ed0389](https://github.com/user-attachments/assets/d17e215a-cb58-4ce8-8ad0-55401cc8395b)

`scripts` entries T3 Code could run, proposed from the `justfile` and deliberately not added to `t3.json` (the maintainer decides):

```json
"scripts": [
  { "name": "Check", "command": "just check", "icon": "lint" },
  { "name": "Test", "command": "just test", "icon": "test" },
  { "name": "Scenario", "command": "just scenario", "icon": "test" }
]
```

A setup entry could also be a candidate, run when T3 Code creates a worktree: `{ "name": "Setup", "command": "uv sync --locked --group dev", "runOnWorktreeCreate": true }` (the first line of the `justfile`'s `tools` recipe). Nothing of this is in the repository.

## Blast radius

Grade: 1. Two new files that only T3 Code reads; nothing in the CLI, the cards or the build reads them. A plain `git revert` removes them.

## Autonomous decisions

None

## Known gaps

None

<details>
<summary>Details</summary>

## Changes

- `docs/logo.svg` (new): the logo above; plain SVG, square `viewBox`, no text, font, image, script or external reference.
- `t3.json` (new, repository root): `$schema` and `iconPath` only.

## Human decisions

- The logo is drawn as a simple square SVG on the building-site theme, at `docs/logo.svg`, and `t3.json` points to it (no logo existed in the repository).
- The change goes through a normal PR that the maintainer merges, with the final `t3.json` shown in its description, rather than an uncommitted edit.
- `t3.json` holds `$schema` and `iconPath` only; the scripts are proposed here and not added.

## Impacts

T3 Code shows the new icon for this repository. No other visible change.

## Test plan

- [ ] New or changed tests: none; a one-off check instead: `t3.json` parses with exactly the keys `$schema` and `iconPath`; `docs/logo.svg` parses as XML, root `{http://www.w3.org/2000/svg}svg`, `viewBox` `0 0 64 64`, no `text`, `image`, `script` or `foreignObject` element, no `font-family`, `href` or `data:`
- [ ] Local gates at `1ed0389`: `just check` passes (578 passed)
- [ ] Evidence: logo render and source in Deliverables
- [ ] Review: approved at `1ed0389`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-357 "a project icon for T3 Code through `t3.json`".

</details>
