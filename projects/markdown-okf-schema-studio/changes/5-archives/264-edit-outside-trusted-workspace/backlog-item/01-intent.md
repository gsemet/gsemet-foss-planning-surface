# Allow editing outside a trusted workspace, with trust-only features disabled

User request (2026-10-27): allow block editing for files that are not in a trusted workspace
(Restricted Mode, files opened from outside the workspace). Features that need trust stay
disabled, and their buttons show as disabled with the reason (see the P1 item
bug-edit-button-hidden-untrusted for the disabled-button pattern).

To decide when it is picked up: the list of features that really need trust (for example
PlantUML with Java, includes, running tools) versus those that only edit the text of the
open document, and how the SwRS for Restricted Mode changes.

## Raised to P1 (2026-11-05)

Owner: other VS Code editors allow editing in an untrusted workspace, so Studio should allow at
least the simple edits. Today SwRS-MDOKFSTUDIO-TRUST-001 makes the preview read-only in Restricted
Mode and for a standalone file in a trusted window, and `package.json`
(`capabilities.untrustedWorkspaces.description`) says the same.

- Owner's decision: trusted or not, the document is editable. This covers Restricted Mode and a
  standalone file outside any workspace folder. Trust never makes a document read-only.
- Only features that really need trust stay off, disabled with their reason (for example PlantUML
  with Java). Editing the text of the open document is never one of them.
- To decide at the grill: which affordances that write other files (image paste, for example) count
  as needing trust.
- Keep the Restricted Mode limits on reads: includes and resources stay in the document's folder.
- Changes: TRUST SwRS, `resource-policy.ts` (`readOnly` also narrows resources, so editing must be
  separated from that narrowing), the `untrustedWorkspaces` description, the README.
