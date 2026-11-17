# An `{include}` with no path fails the whole render

User decision (2026-10-25): P2.

Current behaviour (SwRS-MDOKFSTUDIO-CORE-012 (was SwRS-MDOKFSTUDIO-CORE-014), Known issue): an `{include}` directive with an empty
argument does not leave the include placeholder: the writer fails on the missing argument text and
the whole render is refused with an error. It happens every time a writer types a new include,
since the preview re-renders while typing. The `:literal:` and other-option forms already leave
the placeholder.

## Expected

- An include with no path renders the include placeholder with a warning, like the other
  incomplete forms; the rest of the document renders.
- Render test; update CORE-014 in the same change.

Requirement ids older than the baseline merge map to their current tile in `.agents/changes/archives/059-requirements-okfreq/reduction/mapping.csv`.
