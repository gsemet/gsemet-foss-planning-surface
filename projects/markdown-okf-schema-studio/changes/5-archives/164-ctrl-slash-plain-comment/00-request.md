# Ctrl+/ in the block editor toggles a plain HTML comment, not a TODO

Type: fix · Priority: P1 · Filed 2026-10-28 from the user's report · Part of release 1.0.0 (CR 163):
run in parallel from `origin/main`, not stacked.

## User report (verbatim, French)

> un bug dans l'editeur: quand je fais Ctrl+/, ca place un toto au lieu commentaire.

## Current behaviour

In the preview's block editor (and table cell editor if it shares the binding), Ctrl+/ (Cmd+/ on
macOS) toggles `<!-- TODO: … -->` around the current line or the selected lines. This is
documented in CHANGELOG.md ("Ctrl+/ (Cmd+/) toggles a `<!-- TODO: … -->` comment") and likely in
requirements and user docs.

## Decision (user, 2026-10-28)

- Ctrl+/ (Cmd+/) toggles a **plain** HTML comment `<!-- … -->` around the current line or the
  selected lines, like VS Code's text editor "Toggle Line Comment". One undo step. Toggling off
  removes a plain comment; it must also remove an existing `<!-- TODO: … -->` wrapper? -> decide
  autonomously (list it under "Autonomous decisions"), prefer: only remove what Ctrl+/ adds.
- The palette's TODO button keeps inserting `<!-- TODO: … -->`; its tooltip no longer shows Ctrl+/.
- Update tests, requirements (amend the existing SwRS, okfreq), user docs, the Unreleased
  CHANGELOG entry (rewrite the existing entry rather than adding a contradicting one), and the
  shortcut shown in any tooltip or help.
