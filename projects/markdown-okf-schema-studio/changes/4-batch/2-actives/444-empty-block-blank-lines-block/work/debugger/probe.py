import sys
from playwright.sync_api import sync_playwright
def html(marker):
    ps = "".join(f"<p>p{i}</p>" for i in range(200))
    return f"<body><div id='sphinx-myst-preview-content'>{ps}{marker}</div><style>[data-okf-blank-runs]{{display:none}}#sphinx-myst-preview-content{{padding-bottom:80vh}}</style></body>"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":900,"height":600})
    pg.close()
    for name, marker in (("without marker", ""), ("with hidden marker", '<div hidden data-okf-blank-runs=""></div>')):
        pg = b.new_page(viewport={"width":900,"height":600}); pg.set_content(html(marker))
        pg.evaluate("""() => { const m = document.getElementById('sphinx-myst-preview-content'); const l = m.lastElementChild; if (l) { l.scrollIntoView({block:'end'}); window.scrollBy(0, 40); } }""")
        box = pg.locator('#sphinx-myst-preview-content > :last-child').bounding_box()
        print(name, "scrollY", pg.evaluate("scrollY"), "last-child box", box)
    b.close()
