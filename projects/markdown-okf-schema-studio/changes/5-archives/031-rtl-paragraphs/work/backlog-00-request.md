# RTL paragraphs — K2 (P3, decided 2026-10-22)

Plain Hebrew and Arabic paragraphs are left-aligned (no `dir="auto"`); GitHub right-aligns them.
Raw `<p dir="rtl">` is stripped by the sanitizer, so RTL is impossible today. Scenarios
rendering-core/v17, v18 (fixture 35-cjk-rtl). Fix: emit `dir="auto"` on block elements and allow
`dir` in the sanitizer allow-list.
