# Coverage note — C0 (sweeps on real documents)

Revision b9118506, window c0.

| Document | Sweep | Result |
| --- | --- | --- |
| synth/tables.md | blocks 6, cells 26 | 0 CHANGED |
| synth/frontmatter-edge.md | blocks 3, fields 11 | 0 CHANGED |
| fixtures-visual/73-grid-card-editing.md | blocks 8 | 0 CHANGED |
| fixtures-visual/68-cards-tabs-version.md | blocks 16 (2 not editable, cards/tabs wrappers) | 0 CHANGED |
| book/chapters/15-road-ahead.md | blocks 52 (last one navigated, see c0-1); cells not exercised (no table; sweep was on the glossary) | 0 CHANGED |
| book/chapters/06-guidelines-governance.md | blocks 37 opened before a link navigation derailed the run | 0 CHANGED, rest not exercised |
| book/chapters/02-foundations.md | blocks 0-25 (25 opened), then slice 60-100 (19 opened before a navigation) | 0 CHANGED, rest not exercised |
| vault/wiki/benchmarks/uber-ai-cost-6x-increase.md (vault copy) | blocks 8/10, cells 16, fields 13/14 | 0 CHANGED, 1 unexplained error (c0-gap-1) |

Latency (12 keystrokes, source editor focused, cursor at line 1): small fixture synth/tables.md
p50 about 56 ms, max 57 ms; 02-foundations.md (1709 lines) p50 272 ms, p90 463 ms, max 582 ms
(4.5-5x slower, visible lag per key but under 1 s). Typed text was undone; buffer back to mark.

No buffer change was seen anywhere: the no-op invariant held on every target that was really exercised.
Not exercised: the 06/02/15 documents beyond the slices above, 02-foundations cells/fields,
long-chapter tables (06 has 21 table rows), a second wrap of `--from` ranges after the navigation fix.
