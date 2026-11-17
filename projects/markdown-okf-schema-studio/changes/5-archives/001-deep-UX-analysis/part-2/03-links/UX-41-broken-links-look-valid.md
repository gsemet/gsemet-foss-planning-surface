# UX-41 — Broken links look exactly like valid links

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (synthetic fixture and vault copy) |
| Area | Link rendering and navigation |
| Evidence | [p2-links.jpg](../evidence/p2-links.jpg) |

## Use case

An author maintaining a knowledge base wants to spot dead links while reading, as Obsidian shows
unresolved links dimmed.

## Observed

- `[[Missing Note]]` in `synth/links.md` and broken relative links render in the same blue as
  valid links. The only cue is the `title` tooltip ("The wikilink target is unavailable.").
- Clicking one shows a warning toast: "Sphinx preview navigation blocked: The wikilink target is
  unavailable." "Blocked" reads like a security refusal, and "Sphinx" is stale naming
  ([UX-26](../../05-preview-lifecycle/UX-26-status-page-text-and-stale-naming.md)).
- There is no "Create note" action for a missing wikilink.
- Link tooltips show absolute filesystem paths (`/private/tmp/…/synth/tables.md`) and drop the
  fragment (`#aligned-and-padded`, `#L5`). This also appears in the security review as SEC-11.
- Positive: relative links with `#heading` open the target with the heading line selected,
  same-document anchors scroll smoothly, and code spans keep `[[not-a-link]]` literal.

## Suggested direction

Style links by resolution state (`data-sphinx-preview-link-state`): dimmed/dashed for unavailable
targets. Offer "Create <name>.md" on click for missing wikilinks. Show workspace-relative paths with
the fragment in tooltips. Reword the toast ("Link target not found: Missing Note").

## Done when

A reader can see dead links without hovering, and a missing note can be created from its link.
