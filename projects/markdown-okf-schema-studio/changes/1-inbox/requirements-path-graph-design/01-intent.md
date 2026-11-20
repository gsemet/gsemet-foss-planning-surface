# Intent: a smaller, readable use case path graph

The owner likes the path graph of the requirements viewer but finds it far too big (viewed at 50%)
and hard to read where side branches stack and overlap. This item redesigns it, keeping its look
(cream, rust main path, pills with test counts, coloured scenario dots, Play path).

Done here (2026-11-20, design study, no merged change): a prototype in a throw-away worktree,
checked on six use cases of different shapes at two widths, through three critic rounds by a Fable
model. Result and proof in [work/design.md](work/design.md); patch in
[work/graph-design.patch](work/graph-design.patch); before and after shots in `work/before/` and
`work/after/`.

Next: the owner chooses the open points of `work/design.md` (pill count vs dots, the lost
"paths merge" picture), then a change request applies the patch with its SwRS (CORE-081) and tests
(visual capture per shape, no-overlap check).
