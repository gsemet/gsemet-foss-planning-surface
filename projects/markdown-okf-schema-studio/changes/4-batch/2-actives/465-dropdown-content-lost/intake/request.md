# Dropdown content lost in the preview

Found by the spec critic of blank-runs-inside-quotes-admonitions (2026-11-21): ':::{dropdown} Dd' renders as an empty, unmapped <details></details> on origin/main 2d3187b6: its content is lost in the preview. Probe: a colon-fence dropdown with a title and a paragraph body. Fix: render and map the dropdown body.
## Added by the Chief of Staff (2026-11-22, owner asked for the fix)

- Expected: a MyST `:::{dropdown} Title` (colon fence, and the backtick form) renders its body in the preview like Sphinx does, mapped to its source lines so it can be edited and commented like any other block. Closed by default unless `:open:`.
- The source stays byte for byte as written ("Markdown studio doit respecter le format original").
- Add or fix the SwRS for the dropdown, with tests (unit and the simulated window), and update the writing skill only if a syntax changes.
