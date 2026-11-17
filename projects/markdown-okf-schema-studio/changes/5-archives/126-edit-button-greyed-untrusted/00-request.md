# 126 — Trust-only buttons are greyed with the reason instead of hidden

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-edit-button-hidden-untrusted`

## Intent (user)

See [01-intent.md](01-intent.md) (moved from the backlog, verbatim).

## Autonomous decisions

- Decided by the main session on 2026-10-27 under the user's instruction "lance 4 CR max en parallèle pour fixer tout ça et finaliser une nouvelle stack PR" (same autonomous mode as the previous run). List these in the PR body under "Autonomous decisions".
- Every toolbar button that needs a trusted workspace (edit mode first; the driver lists the others from the code) stays visible, disabled (greyed, `aria-disabled`), with a tooltip "Editing is unavailable: this file is not in a trusted workspace" (or the matching wording per feature).
- Docs and SwRS updated.
- Before/after screenshots in an untrusted real window.
- Coder decision (T1 round 1): the only toolbar button that needs trust/editing is the Edit button; it is now greyed with `aria-disabled="true"` (not `disabled`, so it stays focusable and its hover tooltip shows). Other trust-dependent items found in the code and left unchanged, because they are not toolbar buttons that vanish silently: the Diff toggle (marks need a trusted workspace; the button stays and just shows nothing in Restricted Mode), the Comments toggle (works read-only), the Comment selection button and the edit palette (appear only on selection or in edit mode, which a read-only preview never enters), checkboxes (already disabled with a reason title), thread reply/resolve/delete controls (absent in read-only popovers).
- Two reasons are distinguished: untrusted workspace gives "Editing is unavailable: this file is not in a trusted workspace"; a file outside every workspace folder gives "Editing is unavailable: this file is not in a folder opened in the VS Code workspace" (the page swaps the tooltip from its boot-context `readOnlyReason`).
