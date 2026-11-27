# Dry run of the self-check on the 1.12.1 note (round 1)

File: `docs/releases-notes/2026-11-24-v1.12.1/release-notes.md` at b9b29c5a, unchanged by this
change. Word counts: tokens holding a letter or a digit, headings included; links and HTML tags
left out of the visible part (the `<sub>` text is counted).

| # | Question | Answer | Why (note lines) |
| --- | --- | --- | --- |
| 1 | Subtitle names the kind first | no | line 4 names no kind |
| 2 | Title carries `X.Y.Z` | no | line 1: `1.12` |
| 3 | Tone of the kind everywhere | no | feature-style headings (18, 24); `Smoother editing` in a patch (28) |
| 4 | Every fix starts "Fixed:" | no | none does (30-32) |
| 5 | Every restore owns the earlier break | no | "as it did before 1.11.0" (20) and "as in 1.12.0" (32) name no release that broke it |
| 6 | Bad news on labelled lines | no | two settings removed and a deferred ability sit in paragraphs (20, 22) |
| 7 | One sentence per line, budgets kept | no | bold lead plus a second sentence (30-32); subtitle 18/16; first highlight 111/40; bullets 23 and 26/20; folded 27, 28, 21/20; visible 243/120 |
| 8 | Consequence, no banned construction | no | "Studio no longer watches the files you open" (20); bad news buried |
| 9 | Pictures within bounds, no sentence on a missing one | yes | no picture and no such sentence |
| 10 | Version matches the kind, or the PR says not | no | a patch that removes two settings; the note does not say so (the 1.12.1 PR body was not read) |
