# Image copy proof (2026-11-17)

Method: `01-image-copy-proof.py`, Playwright driving the installed browsers, board served over
127.0.0.1 on a copy of docs/demo (closed batch-02 of mobile-app), a real click on "Copy as image",
clipboard read back as image/png.

| Browser | `blob:` | `data:` |
| --- | --- | --- |
| Chrome (stable, installed) | fails: "Tainted canvases may not be exported", clipboard holds no image/png | works: image/png, 936x1566 px, `02-clipboard-data-chrome.png` |
| Edge | not installed, not run | not installed, not run |
| Firefox | not installed, not run | not installed, not run |

`02-clipboard-data-chrome.png` is the ticket with the Inter font, no button, scalloped edge.
Kept: `data:` (SOURCE in `costs-image.js`, `img-src 'self' data:` in `reply.py`, the test line).
Two code faults found and fixed on the way (both hid the ticket in the first runs): the box's
`style` attribute was set as text, which the page's `style-src 'self'` refuses (now set through
`box.style`); and the ticket was measured after `update({copying:true})` redrew the page, so it was
detached and 0 px wide (now measured and cloned first).
Open: Edge and Firefox unproven here; the user's own browsers remain to check.
