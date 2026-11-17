# 187 — Table cell editor takes focus late

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # Table cell editor: late editor takes focus unconditionally
> 
> Source: release 1.0.0 hotfix (PR #183). After 1.0.0.
> 
> PR #183 stops a late block-source textarea from taking focus once focus has moved to a text field
> outside the editor (SwRS-MDOKFSTUDIO-BLOCK-255, proposed). The table cell editor
> (`src/page/features/tableCellEditor.ts`) has the same late-focus pattern and was left unchanged.
> Apply the same guard, with a headless unit test that fails on the current code.
