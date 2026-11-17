# Promote the QA 210 replay scenarios to product real-input E2E tests

Campaign 210 (2026-10-31) wrote replay scenarios for the QA skill's driver. They should become product real-input E2E tests, so the next campaign does not explore these journeys again.

## Failing today (12): add each as a test that fails until its fix lands (or with the fix's CR)

- [c6-1-invalid-commit-strands-editor](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-1-invalid-commit-strands-editor.json)
- [ux-38-invalid-field-does-not-block-others](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-38-invalid-field-does-not-block-others.json)
- [c1-1-link-card-not-editable](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c1-1-link-card-not-editable.json)
- [c0-1-link-only-paragraph-navigates](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c0-1-link-only-paragraph-navigates.json)
- [c1-2-card-header-enter-adds-blank-line](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c1-2-card-header-enter-adds-blank-line.json)
- [c3-1-alert-lazy-continuation-outside](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c3-1-alert-lazy-continuation-outside.json)
- [c4-1-replace-all-skips-list-with-hidden-url-match](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c4-1-replace-all-skips-list-with-hidden-url-match.json)
- [c5-1-wide-table-tab-editor-offscreen](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c5-1-wide-table-tab-editor-offscreen.json)
- [c6-2-link-hint-ignores-document-folder](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-2-link-hint-ignores-document-folder.json)
- [c6-3-schemaless-number-editor-cannot-commit](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-3-schemaless-number-editor-cannot-commit.json)
- [c7-1-toolbar-covers-first-lines-narrow](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c7-1-toolbar-covers-first-lines-narrow.json)
- [c2-1-comments-toggle-keeps-threads](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c2-1-comments-toggle-keeps-threads.json)

## Guards for campaign 001 fixes (6): pass today, add as regression tests

- [ux-03-open-with-undo-keeps-inline-editor](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-03-open-with-undo-keeps-inline-editor.json)
- [ux-12-cell-edit-minimal-diff](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-12-cell-edit-minimal-diff.json)
- [ux-16-field-edit-minimal-diff](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-16-field-edit-minimal-diff.json)
- [ux-17-enter-commits-text-field](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-17-enter-commits-text-field.json)
- [ux-25-preview-survives-non-markdown-editor](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-25-preview-survives-non-markdown-editor.json)
- [ux-35-crlf-inline-edit-keeps-all-keys](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/ux-35-crlf-inline-edit-keeps-all-keys.json)

Acceptance: each scenario has an equivalent in `test/integration/realInput/` using real input (no injected messages), with its fixture under the test fixtures; `c2-1` waits for the REVIEW-152 intent decision.
Campaign index: [210 00-index.md](../../../4-archives/210-qa-campaign-2026-10-31/00-index.md)
