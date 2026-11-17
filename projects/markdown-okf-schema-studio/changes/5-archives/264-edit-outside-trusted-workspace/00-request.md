# 264: edit a document whatever the workspace trust

Other VS Code editors edit in an untrusted workspace, so Studio should too. Trusted or not, the
document is editable: in Restricted Mode, and for a standalone file outside every workspace folder.
Trust never makes a document read-only. Intent: [backlog-item/01-intent.md](backlog-item/01-intent.md).

## Owner's decisions (2026-11-05)

| Topic | Decision |
| --- | --- |
| Editing the open document | Always on: block edit, block move, frontmatter, checkboxes, radio groups |
| Image paste | On: the file goes in the document's folder, as in a trusted workspace |
| Comments | On: the sidecar next to the document is read and written |
| Reads | Restricted Mode limits stay, and a standalone file in a trusted window keeps them too: includes and resources in the document's folder, no dot-directories, no schema resolution |
| Features that need trust | Stay off, disabled with their reason (PlantUML with Java, for example) |
| Signal | The reason at each disabled feature and the existing diagnostics; no banner |
| Delivery | An independent PR from `main`, not stacked on CR 263: no shared file |

A file VS Code itself holds read-only (`files.readonlyInclude`) stays read-only, with its existing reason.

## Approved requirements

The owner (`default_owner_email`) agreed on 2026-11-06 to change StRS BLOCK-025, REVIEW-003, REVIEW-015
and TABLE-001: "read-only preview" becomes a file VS Code holds read-only. No other approved requirement
changes.
