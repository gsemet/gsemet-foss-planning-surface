---
title: Block ids and tokens at the end of a table row
description: From QA campaign 271 (tables), QA271-02, QA271-10 (Medium, Low).
status: inbox
date: 2026-11-10
---

# Block ids and tokens at the end of a table row

Source: QA campaign 271, QA271-02, QA271-10 (Medium, Low). Sheet: `4-archives/271-qa-campaign-tables-2026-11-10/01-stray-anchors/c1b-1-column-move-carries-last-cell-block-id-into-row.md and c1b-2-token-after-last-pipe-table-handles-inert.md` (index: `4-archives/271-qa-campaign-tables-2026-11-10/00-index.md`).
Priority set by the owner's triage on 2026-11-10: P2.

Owner (2026-11-10): he never writes `^id` anchors in table rows; such tokens come from other tools or agents. A column move must not carry them into the middle of the row, and a trailing token must not make the handles inert. Absorbs the former P1 item `stray-anchors-block-editing` (its intent is kept here as `00-origin.md`): QA never saw editing blocked; if the owner meets it again, one real example reopens it. Promote the QA271-02 replay.
