---
title: QA campaign on table usability
description: Use Markdown tables and the front matter table as a user would; report what e2e does not assert.
status: inbox
date: 2026-11-10
---

# QA campaign on table usability

Owner: a QA stress test dedicated to the usability of tables, testing everything the e2e campaign
does not, to find the bad behaviours that are not asserted today. Only tables and the front matter
table.

## Scope

- Markdown tables and the front matter (properties) table only.
- Use them as a user would, aim at what e2e does not assert, report every bad behaviour.
- Also try to reproduce `stray-anchors-block-editing`.
