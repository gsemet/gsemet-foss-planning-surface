# Check the "security overrides" note in CONTRIBUTING.md

`CONTRIBUTING.md` (line ~37) says: "Security overrides keep the MyST dependency tree on patched
parser releases". The overrides live in `package.json` `overrides`: `csv-parse ^7.0.3`,
`linkify-it ^5.0.2`, `markdown-it ^14.3.1`.

Found during the Dependabot CR: the note does not say where the overrides are, nor which advisory
each one answers, so a contributor cannot tell when one can be removed.

## Expected

- For each override: the advisory or reason, whether it is still needed with the current
  dependency versions (`npm ls`), and remove those no longer needed.
- Rewrite the note: where the overrides are, one line per override with its reason, and when to
  revisit them.

Docs and `package.json` only; no `src/` change.
