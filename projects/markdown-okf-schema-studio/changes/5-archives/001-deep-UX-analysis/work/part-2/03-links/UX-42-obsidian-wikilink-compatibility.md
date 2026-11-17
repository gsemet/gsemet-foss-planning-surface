# UX-42 — Wikilinks diverge from Obsidian on case and special characters

| Field | Value |
| --- | --- |
| Severity | Low |
| Confidence | Measured on a Markdown-only copy of a real Obsidian vault (no private content in this report) |
| Area | Wikilink resolution |

## Observed

On a 137 KB vault note with 750 wikilinks, link discovery is lazy (only links in the viewport are
resolved, which is fine for performance). Of the seven broken links in the first viewport:

- five point to notes that do not exist in the vault (correct);
- one points to a note that exists with **different letter case**. Obsidian resolves it
  (case-insensitive); the extension reports it unavailable (case-sensitive by design, as the
  README states);
- one is reported as **"The navigation target could not be decoded safely."**: its name contains
  characters (spaces, parentheses, percent-like sequences) that the request decoding rejects, so
  the link cannot even be checked.

## Impact

Vault authors see false "unavailable" links, which erodes trust in the dead-link signal of
[UX-41](UX-41-broken-links-look-valid.md).

## Suggested direction

Offer case-insensitive fallback resolution (exact match first, then a unique case-insensitive
match, with an "ambiguous" state otherwise), and URL-encode wikilink targets before embedding them
in navigation requests so any legal file name round-trips.

## Done when

A vault that has no broken links in Obsidian shows none in the preview.
