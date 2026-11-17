# Before / after (grid card in a list item)
| case | before (origin/main) | after (head) | expected |
|---|---|---|---|
| bullet, star, ordered, two-digit, nested, list-in-quote, quote-in-list (6 rows) | card 4, title 4, body 5 (one row 5/5/6) | 5/5/6 (one row 6/6/7) | card 5, title 5, body 6 |
| standalone card in list item | card 3, title 3, body 4 | 3/3/5 | body 5 |
| tab panel in list item | data-line 4 | 5 | 5 |
Before: 26 pass / 9 fail. After: 35 pass / 0 fail. Raw output in before.txt, after.txt.
