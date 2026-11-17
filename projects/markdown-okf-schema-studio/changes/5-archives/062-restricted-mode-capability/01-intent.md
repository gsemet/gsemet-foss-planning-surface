# The packaged extension may be disabled in Restricted Mode

User decision (2026-10-25): P1, verify first, then fix.

Current behaviour (SwRS-MDOKFSTUDIO-TRUST-001 (was SwRS-MDOKFSTUDIO-TRUST-071), Known issue; also TRUST-001, 007, 011): `package.json`
declares no `capabilities.untrustedWorkspaces`. VS Code (1.143.1 bundle, read, not run) then
disables the extension in an untrusted folder unless the user overrides it with
`extensions.supportUntrustedWorkspaces`. README, CHANGELOG and package.json claim Restricted Mode
support, and the code has a full read-only path for it. The Restricted Mode test window probably
passes because the extension is loaded as a development extension.

## Steps

1. Verify: `just package`, install the VSIX in a clean profile, open a cloned folder with
   "Don't Trust", run "Open Preview" on a `.md`. Record what happens (extension disabled or not),
   with a screenshot.
2. If confirmed: add `"capabilities": {"untrustedWorkspaces": {"supported": "limited",
   "description": "…what is read-only or off in Restricted Mode…"}}`, list the restricted
   settings in `restrictedConfigurations` if any apply, and a unit test that reads package.json.
3. Make the Restricted Mode integration window run the extension the way a VSIX does, if
   possible, so this cannot regress silently.
4. Update TRUST-071 (and TRUST-001/007/011 if their Known issue lines change) in the same PR.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
