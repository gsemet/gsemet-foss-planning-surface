# Machine checks

Failing applicable geometry checks per scenario. `required` checks fail the run; `report-only` checks are recorded and do not.

Scenarios: 95; failing applicable checks: 45.

| Scenario | Check | Mode | Detail |
| --- | --- | --- | --- |
| code-dark-top | identifier-split | report-only | 10 split identifier(s): 2024-03-11, FAR-RIGHT-ACCESS, nw-02, 2024-01-28, nw-03 |
| code-dark-table | identifier-split | report-only | 10 split identifier(s): 2024-03-11, FAR-RIGHT-ACCESS, nw-02, 2024-01-28, nw-03 |
| code-light-full | identifier-split | report-only | 10 split identifier(s): 2024-03-11, FAR-RIGHT-ACCESS, nw-02, 2024-01-28, nw-03 |
| okf-schema-narrow | identifier-split | report-only | 9 split identifier(s): type(enum), title(text), status(enum), owner(text), priority(number) |
| preview-toolbar-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| okf-schema-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| okf-schema-table | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| okf-schema-missing-required-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), priority(number), reviewed_on(date), derives_from(list) |
| okf-schema-missing-required-light | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), priority(number), reviewed_on(date), derives_from(list) |
| schema-validation-error-dark | identifier-split | report-only | 4 split identifier(s): Description◀▶, type(enum), title(text), tested_in_files(list) |
| schema-validation-error-narrow | identifier-split | report-only | 3 split identifier(s): type(enum), title(text), tested_in_files(list) |
| schema-validation-error-light | identifier-split | report-only | 4 split identifier(s): Description◀▶, type(enum), title(text), tested_in_files(list) |
| standalone-frontmatter-dark | identifier-split | report-only | 1 split identifier(s): namesummary |
| standalone-frontmatter-light | identifier-split | report-only | 1 split identifier(s): namesummary |
| frontmatter-link-details-dark-460 | identifier-split | report-only | 3 split identifier(s): type(enum), title(text), references(list) |
| frontmatter-links-loading | identifier-split | report-only | 4 split identifier(s): Description◀▶, type(enum), title(text), references(list) |
| frontmatter-links-loaded | identifier-split | report-only | 4 split identifier(s): Description◀▶, type(enum), title(text), references(list) |
| frontmatter-link-details-dark-900 | identifier-split | report-only | 4 split identifier(s): Description◀▶, type(enum), title(text), references(list) |
| frontmatter-link-details-white-460 | identifier-split | report-only | 3 split identifier(s): type(enum), title(text), references(list) |
| frontmatter-link-details-white-900 | identifier-split | report-only | 4 split identifier(s): Description◀▶, type(enum), title(text), references(list) |
| edit-table-wrapped-dark-460 | overlay-covers-text | report-only | 2 covered text excerpt(s): "Expected behavior", "Evidence" |
| edit-table-wrapped-dark-460 | identifier-split | report-only | 9 split identifier(s): type(enum), title(text), status(enum), owner(text), priority(number) |
| frontmatter-scroll-feedback-edit | identifier-split | report-only | 9 split identifier(s): type(enum), title(text), status(enum), owner(text), priority(number) |
| edit-mode-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-paragraph-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-admonition-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-table-cell-dark | overlay-covers-text | report-only | 2 covered text excerpt(s): "Expected behavior", "Evidence" |
| edit-table-cell-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-table-wrapped-dark-900 | overlay-covers-text | report-only | 2 covered text excerpt(s): "Expected behavior", "Evidence" |
| edit-table-wrapped-dark-900 | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-frontmatter-key-dark | overlay-covers-text | report-only | 4 covered text excerpt(s): "type", "(enum)", "title", "(text)" |
| edit-frontmatter-key-dark | identifier-split | report-only | 9 split identifier(s): Description◀▶, type(enum), title(text), owner(text), priority(number) |
| edit-frontmatter-value-dark | overlay-covers-text | report-only | 2 covered text excerpt(s): "swrs", "Brake pedal release detection" |
| edit-frontmatter-value-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-frontmatter-list-dark | overlay-covers-text | report-only | 1 covered text excerpt(s): "2026-09-28" |
| edit-frontmatter-list-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-table-wrapped-light-460 | overlay-covers-text | report-only | 2 covered text excerpt(s): "Expected behavior", "Evidence" |
| edit-table-wrapped-light-460 | identifier-split | report-only | 9 split identifier(s): type(enum), title(text), status(enum), owner(text), priority(number) |
| edit-table-wrapped-light-900 | overlay-covers-text | report-only | 2 covered text excerpt(s): "Expected behavior", "Evidence" |
| edit-table-wrapped-light-900 | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-frontmatter-list-light | overlay-covers-text | report-only | 1 covered text excerpt(s): "2026-09-28" |
| edit-frontmatter-list-light | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| edit-frontmatter-boolean-dark | overlay-covers-text | report-only | 2 covered text excerpt(s): "Chassis Platform", "2" |
| edit-frontmatter-boolean-dark | identifier-split | report-only | 10 split identifier(s): Description◀▶, type(enum), title(text), status(enum), owner(text) |
| frontmatter-scroll-feedback | identifier-split | report-only | 9 split identifier(s): type(enum), title(text), status(enum), owner(text), priority(number) |
