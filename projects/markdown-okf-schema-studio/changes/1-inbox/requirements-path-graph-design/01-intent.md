# Intent: a smaller, readable use case path graph

The owner likes the path graph of the requirements viewer but finds it far too big (viewed at 50%)
and hard to read where side branches stack and overlap. This item redesigns it, keeping its look
(cream, rust main path, pills with test counts, coloured scenario dots, Play path).

The owner rejected proposal 1 (one row per path, grey copies of shared states; kept in
`work/rounds/proposal-1/`): a state shared by two paths must be one node, the paths joining into it
and splitting out of it, each in its colour ([02-answers.md](02-answers.md)).

Done here (2026-11-20, design study, no merged change): proposal 2, the joined map, prototyped in a
throw-away worktree, checked on six use cases at two widths through three critic rounds by a Fable
model. Maps are 30 to 65 % shorter, with no overlapping text. Result and proof in
[work/design.md](work/design.md); patch in [work/graph-design.patch](work/graph-design.patch);
before and after shots in `work/before/` and `work/after/`.

Next: the owner approves the joined map and its open points (narrow screens scroll, BLOCK-014 a
little wider than the page), then a change request applies the patch with its SwRS (CORE-081, plus
Play over joined states) and tests (buildMetroMap unit test, no-overlap check, visual capture per
shape, Play test).
