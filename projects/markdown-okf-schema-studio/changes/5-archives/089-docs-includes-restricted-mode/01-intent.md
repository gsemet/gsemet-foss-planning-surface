# known-limitations says includes need trust; the code reads them in Restricted Mode

User decision (2026-10-24): the code is right, fix the doc.

`docs/known-limitations.md` (line ~36) says workspace-local file includes work only when the
workspace is trusted. The code (SwRS-MDOKFSTUDIO-CORE-020, archived by the baseline in favour of TRUST-001/TRUST-007; Known issue on TRUST-088) renders read-only in an untrusted
workspace or a standalone file, with the resource root reduced to the document's folder: an
include next to the document is read and shown; an include outside that folder is refused with
a warning.

## Expected

Rewrite the sentence to match: trusted workspace → includes inside the workspace that pass the
resource policy; Restricted Mode or standalone file → only files inside the document's folder.
Docs only.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
