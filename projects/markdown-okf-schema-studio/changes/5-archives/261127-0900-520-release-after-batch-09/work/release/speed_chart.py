"""Render the release picture of the comment rendering measures (PR 549 and 550)."""

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

PANELS = [
    (
        "Page elements restyled by one new comment",
        [("Before", 3109, "3,109"), ("1.13", 4, "4")],
    ),
    (
        "Time until its highlight is drawn",
        [("Before", 53.4, "53 ms"), ("1.13", 45.9, "46 ms")],
    ),
]
TRACK = 280


def panel(title: str, rows: list[tuple[str, float, str]]) -> str:
    top = max(value for _, value, _ in rows)
    bars = "".join(
        f'<div class="row"><span class="name">{name}</span>'
        f'<span class="bar {"new" if name != "Before" else "old"}" '
        f'style="width:{max(3, value / top * TRACK):.1f}px"></span>'
        f'<span class="value">{label}</span></div>'
        for name, value, label in rows
    )
    return f'<section><h2>{title}</h2><div class="plot">{bars}</div></section>'


html = f"""<!doctype html><meta charset="utf-8"><style>
body {{ margin: 0; background: #fcfcfb; color: #0b0b0b;
  font: 15px/1.4 "Segoe UI", system-ui, sans-serif; }}
main {{ width: 880px; padding: 22px 26px 18px; box-sizing: border-box; }}
.panels {{ display: grid; grid-template-columns: 1fr 1fr; gap: 36px; }}
h2 {{ margin: 0 0 14px; font-size: 15px; font-weight: 600; }}
.plot {{ display: grid; gap: 10px; }}
.row {{ display: flex; align-items: center; }}
.name {{ width: 54px; color: #52514e; border-right: 1px solid #c3c2b7;
  margin-right: 0; line-height: 28px; }}
.bar {{ height: 22px; border-radius: 0 4px 4px 0; }}
.old {{ background: #8a8981; }}
.new {{ background: #2a78d6; }}
.value {{ margin-left: 8px; font-weight: 600; }}
p {{ margin: 18px 0 0; color: #52514e; font-size: 12.5px; }}
</style><main><div class="panels">{"".join(panel(*p) for p in PANELS)}</div>
<p>Medians of three runs in VS Code on a Linux CI runner, on a generated document of 464 lines with
22 tables, 11 images and 9 comment threads. The time was measured with the first of the two changes;
the second moved it by less than the runs vary.</p></main>"""

with sync_playwright() as playwright:
    browser = playwright.chromium.launch()
    page = browser.new_page(viewport={"width": 880, "height": 200}, device_scale_factor=1.5)
    page.set_content(html)
    page.locator("main").screenshot(path=str(Path(sys.argv[1])))
    browser.close()
print("written")
