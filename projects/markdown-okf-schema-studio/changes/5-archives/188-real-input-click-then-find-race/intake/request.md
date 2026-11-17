# 188 — Real-input click then Find race

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # Real-input proof: click a block, then Cmd+F immediately, then type
> 
> Source: Chief of Staff review of PR #183. After 1.0.0.
> 
> The integration test in PR #183 now sidesteps the race (it waits for the block editor, presses
> Escape, then opens find), so the product fix (late block-source textarea does not steal focus,
> SwRS-MDOKFSTUDIO-BLOCK-255) has only headless unit proof. Add a real-input scenario: in edit
> mode, click a block, press Cmd/Ctrl+F at once, type a query; assert the text lands in the find
> field, the match count appears, and the Markdown source on disk is unchanged.
