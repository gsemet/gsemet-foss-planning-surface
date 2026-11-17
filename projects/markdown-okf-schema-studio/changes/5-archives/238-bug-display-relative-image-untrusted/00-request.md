# 238 — Relative images show in Restricted Mode

Type: fix · Priority: P1 · Approved by the owner on 2026-11-03 · Worktree
`../markdown-okf-schema-studio-wt-238`, branch `change-requests/238-bug-display-relative-image-untrusted`.

## Intent

From [01-intent.md](01-intent.md): in a workspace that is not trusted, relative images are not
rendered. Render them while staying untrusted.

![Broken relative images](image.png)

The file names in the screenshot hold spaces (`Screenshot 2022-09-09 at 10.49.17.png`): the cause
may be the path encoding rather than the trust policy. The investigation decides.

## Owner decisions (2026-11-03)

> [!IMPORTANT]
> The owner (gaetan@xeberon.net) agrees to change the TRUST requirements for this, within the
> limits below.

- Restricted Mode shows images (png, jpg, jpeg, gif, webp, svg as `<img>`) from the document
  folder and the workspace root.
- Includes stay refused in Restricted Mode, and so do dot-segment paths (`.ssh`, `.aws`…).
- Broad roots (the home folder and above) stay refused, except the document's own folder.
