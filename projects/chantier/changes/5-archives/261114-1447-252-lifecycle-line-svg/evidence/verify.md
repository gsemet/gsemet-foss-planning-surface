# Verify CR-252

Head: a4d342b490e06d496cac050a51ba1dbb4e5b5de0 (diff against 1bb3931: README.md +2, docs/cr-lifecycle-line.svg, docs/cr-lifecycle-line-texts.md; no other file)

Command for 1-3, 5: a one-off Python script (`uv run python -I`) parsing docs/cr-lifecycle-line.svg and its texts file.

| # | Claim | Output | Result |
| --- | --- | --- | --- |
| 1 | parses as XML; viewBox matches width/height | `viewBox 0 0 1000 290 1000 290` | pass |
| 2 | ten steps in order with small lines; Spec critic dashed (#94a3b8, 6 4) with `🧐 spec critic` / `when impactful`; states `🟣 Ready locally`, `🟤 PR in draft`, `🟢 Ready to merge` green #f0fdf4/#16a34a; no 🔵; no `mergeable`; no folder names | read in file; dashed rects = spec critic and 🟣 only; `ready` only in the two state titles; blue False; folders [] | pass |
| 3 | every `<text>` in the texts file; title and first paragraph equal `<title>`, `<desc>` | `missing in md: []`, title True, desc True | pass |
| 4 | README image just before cr-lifecycle-simple.svg, simple unchanged | `git diff 1bb3931 HEAD -- README.md`: +2 lines (image and blank) at the right place | pass |
| 5 | 🟣 dashed (#7c3aed, 6 4) with `rare:` / `no PR yet`; 🧐 in legend and step 4; no approve/go | approve/go [] | pass |
| sizes | viewBox 1000; step titles 17; smallest text 13.5; nothing over the column | font sizes {13.5, 16, 17, 30}; rightmost box edge 992 of 1000 | pass |

No long gate (user waiver); CI green 5/5 at a4d342b (per caller).
Verdict: VERIFIED
