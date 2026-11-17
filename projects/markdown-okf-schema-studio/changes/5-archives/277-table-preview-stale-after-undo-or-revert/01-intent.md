---
title: Table preview stale after an undo or a revert
description: From QA campaign 271 (tables), QA271-05, QA271-06 (Medium).
status: inbox
date: 2026-11-10
---

# Table preview stale after an undo or a revert

Source: QA campaign 271, QA271-05, QA271-06 (Medium). Sheet: `4-archives/271-qa-campaign-tables-2026-11-10/02-table-structure/c3-2.md and 04-table-concurrency/c6-1.md` (index: `4-archives/271-qa-campaign-tables-2026-11-10/00-index.md`).
Priority set by the owner's triage on 2026-11-10: P2.

Probably one cause: the render is skipped while a cell session is or was active. The preview must match the buffer.
