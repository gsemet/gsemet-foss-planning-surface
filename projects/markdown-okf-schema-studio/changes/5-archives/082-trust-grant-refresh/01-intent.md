# A preview opened in Restricted Mode stays read-only after the folder is trusted

User decision (2026-10-25): P2.

Current behaviour (SwRS-MDOKFSTUDIO-TRUST-001 (was SwRS-MDOKFSTUDIO-LIFE-155) and TRUST-001, Known issue; read from the code, not
run): `readOnly`, the resource root and the navigation roots are fixed when the session is created
(`src/session/previewManager.ts`, around line 245). Nothing resets them on a trust grant, so the
preview stays read-only until a document switch or a reopen creates a new session.

## Expected

- On a trust grant, open previews switch to the trusted session state (editing, checkboxes,
  palette, workspace resource roots) without being reopened, and re-render once.
- Integration test in the Restricted Mode window (grant trust, then edit); update LIFE-155 and
  TRUST-001 in the same change. Do after `P1/restricted-mode-capability`.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
