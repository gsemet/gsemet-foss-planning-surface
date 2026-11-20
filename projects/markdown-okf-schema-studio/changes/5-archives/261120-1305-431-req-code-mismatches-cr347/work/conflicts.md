# Conflicts: CR-431 rebase onto origin/main e05f0b51

Commit 7c18c704 rebased to b2bdd721. Only `CHANGELOG.md` conflicted.

## CHANGELOG.md, `## Unreleased`

Both sides appended bullets at the same spot. Choice: kept every entry of both sides, origin/main's
two bullets (list item editing, `preview.listItemsInToc`) first, then the CR's bullet ("When a render
fails without a message ..."). No other file conflicted. No byte-order mark added (file starts `# C`
before and after). Commit message unchanged.

## Gates

- Fast gate, `just check` at the rebased head: pass, exit 0 (only the existing W2 broken cross-link
  warnings in palette-slash SwRS files; "0 indexes would change", "0 files would change", main paths
  valid, use case diagrams all parse).
- `just requirements-update`: exit 0, `git status --short` empty afterwards, so nothing changed.
