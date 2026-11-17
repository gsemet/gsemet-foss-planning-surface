# An unclosed directive in the middle of a document hides the rest of it

Found during the demo tour of the P1 stack (2026-10-27), on top of the fix "render unclosed
directives and labels as raw source instead of crashing".

Repro: a document with an unclosed fence followed by more sections.

````md
## 3. Unclosed directive

```{list-table}

This paragraph should still render.

## 4. Table
...
````

Seen: no crash, but the preview shows nothing after the heading: the raw ```` ```{list-table} ````
line is not shown, and every section after it is gone.

![image.png](evidence/image.png)

Cause: in Markdown an unclosed fence runs to the end of the file, so the whole rest of the
document becomes the body of the `list-table`, which is not a list and renders empty. The
earlier fix only tests the case where the unclosed directive is the last line of the file.

Expected (user intent: "just print the raw line"): an unclosed directive renders its opening line
as a raw code block, and the rest of the document renders normally, as if that line were absent.
Add tests for the mid-document case (backtick and colon fences, nested), plus a preview e2e.
